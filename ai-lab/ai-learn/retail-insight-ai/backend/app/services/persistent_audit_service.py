"""PostgreSQL Persistent Audit 应用服务。

文件职责：
- 只在 PostgreSQL backend 启用企业审计；InMemory 保持冻结维护状态。
- 用 Unit of Work 保证“业务成功 + Audit append”同事务提交。
- 业务异常先回滚，再用独立事务保存 failure；审计失败直接升级为请求失败。

谁会调用它：
- FastAPI yield Dependency、JWT Dependency、Login Router。

它调用谁：
- AuditService、UnitOfWork 和 CurrentUser contract。

输入与输出：
- 输入安全 HTTP 上下文、action、permission、resource；输出 append-only AuditLog。

为什么这样设计：
- 避免 Router/Service/Dependency 各写一遍造成重复，同时不扩展 InMemory Audit。

日本现场面试怎么讲：
- Success audit 与业务事实原子提交；Failure/Denied audit 使用独立事务，且任何审计写入失败都不会返回伪成功。
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import Any, AsyncIterator, Callable

from app.errors.base import AppException
from app.errors.exceptions import AuditLogAppendException
from app.models.audit import AuditLog, AuditLogResult
from app.repositories.interfaces.unit_of_work import UnitOfWork
from app.security.contracts import CurrentUser
from app.security.errors import AuthenticationError, PermissionError
from app.services.audit_service import AuditService


@dataclass(frozen=True)
class PersistentAuditSpec:
    """声明一个受控业务动作的固定审计合同。"""

    action: str
    resource_type: str
    success_status_code: int
    permission: str | None = None
    resource_id: str = "collection"
    resource_id_param: str | None = None


@dataclass(frozen=True)
class PersistentAuditContext:
    """一次请求中允许进入 Audit Log 的安全上下文。"""

    request_id: str
    http_method: str
    api_path: str
    resource_id: str
    current_user: CurrentUser | None = None
    actor_username: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class PersistentAuditService:
    """集中执行 PostgreSQL-only 审计写入与敏感字段清洗。"""

    _SENSITIVE_KEY_FRAGMENTS = (
        "authorization",
        "cookie",
        "password",
        "secret",
        "api_key",
        "apikey",
        "access_token",
        "refresh_token",
        "jwt",
        "prompt",
        "document_content",
        "document_body",
        "rag_context",
        "full_context",
    )

    def __init__(
        self,
        audit_service: AuditService,
        unit_of_work: UnitOfWork,
        *,
        enabled: bool,
    ) -> None:
        self._audit_service = audit_service
        self._unit_of_work = unit_of_work
        self._enabled = enabled

    @property
    def enabled(self) -> bool:
        """暴露 backend 开关，供 Dependency 在 InMemory 下零成本跳过。"""

        return self._enabled

    @asynccontextmanager
    async def operation(
        self,
        spec: PersistentAuditSpec,
        context_provider: Callable[[], PersistentAuditContext],
    ) -> AsyncIterator[None]:
        """包围 endpoint：成功同事务写审计，失败回滚后另存 failure。"""

        if not self._enabled:
            yield
            return

        try:
            with self._unit_of_work.transaction():
                yield
                self._record(
                    spec=spec,
                    context=context_provider(),
                    result=AuditLogResult.SUCCESS,
                    status_code=spec.success_status_code,
                )
        except AuditLogAppendException:
            # Repository 不可用时不能再次尝试写“审计失败的审计”，直接让请求失败。
            raise
        except Exception as exc:
            status_code, error_code = self._failure_context(exc)
            with self._unit_of_work.transaction():
                self._record(
                    spec=spec,
                    context=context_provider(),
                    result=AuditLogResult.FAILURE,
                    status_code=status_code,
                    error_code=error_code,
                    extra_metadata={"exception_type": type(exc).__name__},
                )
            raise

    def record_login_success(
        self,
        *,
        context: PersistentAuditContext,
        current_user: CurrentUser,
    ) -> AuditLog | None:
        """登录成功后记录 Token 对应主体，不记录 Token 原文。"""

        if not self._enabled:
            return None
        with self._unit_of_work.transaction():
            return self._record(
                spec=PersistentAuditSpec(
                    action="login.success",
                    resource_type="authentication",
                    resource_id=current_user.user_id,
                    success_status_code=200,
                ),
                context=PersistentAuditContext(
                    request_id=context.request_id,
                    http_method=context.http_method,
                    api_path=context.api_path,
                    resource_id=current_user.user_id,
                    current_user=current_user,
                    actor_username=current_user.username,
                ),
                result=AuditLogResult.SUCCESS,
                status_code=200,
            )

    def record_login_failure(
        self,
        *,
        context: PersistentAuditContext,
        error_code: str,
    ) -> AuditLog | None:
        """登录失败只保存尝试用户名和安全错误码，不保存密码。"""

        if not self._enabled:
            return None
        with self._unit_of_work.transaction():
            return self._record(
                spec=PersistentAuditSpec(
                    action="login.failure",
                    resource_type="authentication",
                    resource_id="login",
                    success_status_code=401,
                ),
                context=context,
                result=AuditLogResult.FAILURE,
                status_code=401,
                error_code=error_code,
            )

    def record_authentication_failure(
        self,
        *,
        context: PersistentAuditContext,
        error_code: str,
    ) -> AuditLog | None:
        """Bearer 认证失败写入持久审计，但不保存 Header 或 Token。"""

        if not self._enabled:
            return None
        with self._unit_of_work.transaction():
            return self._record(
                spec=PersistentAuditSpec(
                    action="authentication.failure",
                    resource_type="api",
                    resource_id=context.api_path,
                    success_status_code=401,
                ),
                context=context,
                result=AuditLogResult.FAILURE,
                status_code=401,
                error_code=error_code,
            )

    def record_authorization_denied(
        self,
        *,
        context: PersistentAuditContext,
        permission: str,
    ) -> AuditLog | None:
        """统一 Permission Dependency 的 403 denied 事实。"""

        if not self._enabled:
            return None
        with self._unit_of_work.transaction():
            return self._record(
                spec=PersistentAuditSpec(
                    action="authorization.denied",
                    resource_type="api",
                    resource_id=context.api_path,
                    success_status_code=403,
                    permission=permission,
                ),
                context=context,
                result=AuditLogResult.DENIED,
                status_code=403,
                error_code="forbidden",
                extra_metadata={"attempted_permission": permission},
            )

    def _record(
        self,
        *,
        spec: PersistentAuditSpec,
        context: PersistentAuditContext,
        result: AuditLogResult,
        status_code: int,
        error_code: str | None = None,
        extra_metadata: dict[str, Any] | None = None,
    ) -> AuditLog:
        """把安全上下文转换成统一 AuditLog。"""

        user = context.current_user
        metadata = {
            **context.metadata,
            **(extra_metadata or {}),
        }
        return self._audit_service.record_audit_log(
            operation_type=spec.action,
            actor_id=user.user_id if user is not None else None,
            actor_username=(
                user.username if user is not None else context.actor_username
            ),
            actor_role=user.role if user is not None else None,
            organization_id=None,
            department_id=None,
            resource_type=spec.resource_type,
            resource_id=context.resource_id or spec.resource_id,
            result=result,
            request_id=context.request_id,
            trace_id=context.request_id,
            metadata=self._sanitize(metadata),
            error_code=error_code,
            permission=spec.permission,
            http_method=context.http_method,
            api_path=context.api_path,
            status_code=status_code,
        )

    def _sanitize(self, value: Any) -> Any:
        """递归删除敏感键，并限制字符串长度，避免正文或凭证落库。"""

        if isinstance(value, dict):
            sanitized: dict[str, Any] = {}
            for key, item in value.items():
                normalized = str(key).strip().lower().replace("-", "_")
                if any(
                    fragment in normalized
                    for fragment in self._SENSITIVE_KEY_FRAGMENTS
                ):
                    continue
                sanitized[str(key)] = self._sanitize(item)
            return sanitized
        if isinstance(value, (list, tuple)):
            return [self._sanitize(item) for item in value[:50]]
        if isinstance(value, str):
            return value[:512]
        if value is None or isinstance(value, (bool, int, float)):
            return value
        return type(value).__name__

    def _failure_context(self, exc: Exception) -> tuple[int, str]:
        """从已知异常合同提取安全 status/error_code，不保存异常正文。"""

        if isinstance(exc, AppException):
            return exc.status_code, exc.error_code.value
        if isinstance(exc, AuthenticationError):
            return exc.status_code, exc.error_code
        if isinstance(exc, PermissionError):
            return exc.status_code, exc.error_code
        status_code = getattr(exc, "status_code", 500)
        return int(status_code), "internal_error"


__all__ = [
    "PersistentAuditContext",
    "PersistentAuditService",
    "PersistentAuditSpec",
]
