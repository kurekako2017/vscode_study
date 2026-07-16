"""FastAPI JWT / CurrentUser Dependency。

文件职责：统一注入 CurrentUser，并以声明式 Dependency 强制执行 Permission。
谁调用它：所有需要认证的 API Router。
它调用谁：AppContainer 中的 JWTService。
输入：HTTP Authorization Header。
输出：CurrentUser；缺失/非法/过期统一抛出 401 认证错误。
设计理由：每个 API 不重复解析 JWT，Swagger 自动生成 Bearer Authorize。
日本现场面试：认证是通用 dependency，未来 RBAC dependency 可直接依赖它。
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.security.contracts import CurrentUser
from app.security.authorization_service import AuthorizationService
from app.security.errors import AuthenticationError, ForbiddenError, UnauthorizedError
from app.security.rbac_contracts import Permission
from app.observability.logging import get_request_id
from app.services.persistent_audit_service import PersistentAuditContext

# HTTPBearer 会在 OpenAPI 中生成 type=http, scheme=bearer 的统一安全定义。
bearer_scheme = HTTPBearer(
    scheme_name="BearerAuth",
    description="输入 Login API 返回的 JWT Access Token",
    bearerFormat="JWT",
    auto_error=False,
)


async def get_authorization_service(request: Request) -> AuthorizationService:
    """从应用组合根取得唯一 AuthorizationService。"""

    return request.app.state.container.authorization_service


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> CurrentUser:
    """验证 Bearer Header 并返回当前认证用户。"""

    if credentials is None:
        error = UnauthorizedError(reason="missing_bearer_token")
        _record_authentication_failure(request, error)
        raise error
    if credentials.scheme.lower() != "bearer" or not credentials.credentials:
        error = UnauthorizedError(reason="invalid_bearer_header")
        _record_authentication_failure(request, error)
        raise error
    try:
        current_user = request.app.state.container.jwt_service.get_current_user(
            credentials.credentials
        )
    except AuthenticationError as exc:
        _record_authentication_failure(request, exc)
        raise
    # Persistent Audit 只能读取服务端验证后的 CurrentUser，不能接受客户端自报 actor。
    request.state.current_user = current_user
    return current_user


def require_permission(
    permission: Permission,
) -> Callable[..., CurrentUser]:
    """创建可复用权限 Dependency；Router 只声明能力，不解析 JWT 或判断 role。"""

    async def permission_dependency(
        request: Request,
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        service: Annotated[
            AuthorizationService, Depends(get_authorization_service)
        ],
    ) -> CurrentUser:
        try:
            service.require_permission(current_user, permission)
        except ForbiddenError:
            request.app.state.container.persistent_audit_service.record_authorization_denied(
                context=_audit_context(request, current_user=current_user),
                permission=permission.value,
            )
            raise
        return current_user

    return permission_dependency


def _record_authentication_failure(
    request: Request,
    exception: AuthenticationError,
) -> None:
    """记录 401，但绝不把 Authorization Header 或 Token 传给审计层。"""

    request.app.state.container.persistent_audit_service.record_authentication_failure(
        context=_audit_context(request),
        error_code=exception.error_code,
    )


def _audit_context(
    request: Request,
    *,
    current_user: CurrentUser | None = None,
) -> PersistentAuditContext:
    """构造只包含安全 HTTP 元数据的持久审计上下文。"""

    return PersistentAuditContext(
        request_id=get_request_id(),
        http_method=request.method,
        api_path=request.url.path,
        resource_id=request.url.path,
        current_user=current_user,
    )
