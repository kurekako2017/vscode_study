"""Approval 专用的可复用审计中间层。

文件职责：
- 统一封装 approval API 的授权、成功、失败和异常审计写入。
- 保留 current user 来源为 SecurityService.get_current_user()。
- 只面向 approval 这条链路，不扩展到其他 API。

谁会调用它：
- approval 路由和对应测试。

它调用谁：
- SecurityService 读取 current user，并复用现有 RBAC guard 进行权限判定。
- AuditService 追加审计事实。
- 结构化日志工具记录写入结果。
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from inspect import isawaitable
from typing import Any, TypeVar

from app.errors.base import AppException
from app.errors.exceptions import PermissionDeniedException
from app.models.audit import AuditLogResult
from app.models.security import User
from app.observability.logging import get_logger, get_request_id, log_event
from app.services.audit_service import AuditService
from app.services.rbac_guard import RBACGuard
from app.services.security_service import SecurityService

logger = get_logger(__name__)

T = TypeVar("T")


@dataclass(frozen=True)
class AuditAction:
    """描述一条 approval 审计动作。"""

    operation_type: str
    resource_type: str
    resource_id: str
    action: str
    metadata: dict[str, Any] = field(default_factory=dict)
    permission: str | None = None
    permissions: tuple[str, ...] = ()
    role: str | None = None
    roles: tuple[str, ...] = ()
    require_all_permissions: bool = True
    require_all_roles: bool = False


class AuditMiddleware:
    """把 approval 的 RBAC + 审计写入收敛成一个可复用入口。"""

    def __init__(
        self,
        audit_service: AuditService,
        security_service: SecurityService,
        rbac_guard: RBACGuard,
    ) -> None:
        self._audit_service = audit_service
        self._security_service = security_service
        self._rbac_guard = rbac_guard

    async def run(
        self,
        *,
        action: AuditAction,
        operation: Callable[[], T | Awaitable[T]],
    ) -> T:
        """先检查 RBAC，再执行业务逻辑，并自动写入成功或失败审计。"""

        self._rbac_guard.require(
            permission=action.permission,
            permissions=action.permissions,
            role=action.role,
            roles=action.roles,
            action=action.action,
            resource_type=action.resource_type,
            resource_id=action.resource_id,
            require_all_permissions=action.require_all_permissions,
            require_all_roles=action.require_all_roles,
        )

        request_id = get_request_id()
        user = self._security_service.get_current_user()
        metadata: dict[str, Any] = dict(action.metadata or {})
        try:
            result = operation()
            if isawaitable(result):
                result = await result
        except PermissionDeniedException:
            raise
        except AppException as exc:
            self._record_audit(
                action=action,
                user=user,
                request_id=request_id,
                result=AuditLogResult.FAILED,
                metadata={
                    **metadata,
                    "exception_type": type(exc).__name__,
                    "error_code": exc.error_code.value,
                },
                error_code=exc.error_code.value,
            )
            raise
        except Exception as exc:
            self._record_audit(
                action=action,
                user=user,
                request_id=request_id,
                result=AuditLogResult.FAILED,
                metadata={
                    **metadata,
                    "exception_type": type(exc).__name__,
                },
                error_code="internal_error",
            )
            raise

        self._record_audit(
            action=action,
            user=user,
            request_id=request_id,
            result=AuditLogResult.SUCCESS,
            metadata=metadata,
        )
        return result

    def _record_audit(
        self,
        *,
        action: AuditAction,
        user: User,
        request_id: str,
        result: AuditLogResult,
        metadata: dict[str, Any],
        error_code: str | None = None,
    ) -> None:
        """把 approval 审计事实写入 append-only audit trail。"""

        stored = self._audit_service.record_audit_log(
            operation_type=action.operation_type,
            actor_id=user.user_id,
            organization_id=user.organization.organization_id,
            department_id=user.department.department_id,
            resource_type=action.resource_type,
            resource_id=action.resource_id,
            result=result,
            request_id=request_id,
            trace_id=request_id,
            metadata=metadata,
            error_code=error_code,
        )
        log_event(
            logger,
            "info",
            "approval_audit_recorded",
            "Approval audit recorded",
            request_id=stored.request_id,
            task_id=stored.audit_log_id,
            status=result.value,
        )


__all__ = ["AuditAction", "AuditMiddleware"]
