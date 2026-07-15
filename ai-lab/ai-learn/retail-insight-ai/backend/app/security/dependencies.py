"""FastAPI JWT / CurrentUser Dependency。

文件职责：统一读取 Authorization Bearer Header 并注入 CurrentUser。
谁调用它：所有需要认证的 API Router。
它调用谁：AppContainer 中的 JWTService。
输入：HTTP Authorization Header。
输出：CurrentUser；缺失/非法/过期统一抛出 401 认证错误。
设计理由：每个 API 不重复解析 JWT，Swagger 自动生成 Bearer Authorize。
日本现场面试：认证是通用 dependency，未来 RBAC dependency 可直接依赖它。
"""

from __future__ import annotations

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.security.contracts import CurrentUser
from app.security.errors import UnauthorizedError

# HTTPBearer 会在 OpenAPI 中生成 type=http, scheme=bearer 的统一安全定义。
bearer_scheme = HTTPBearer(
    scheme_name="BearerAuth",
    description="输入 Login API 返回的 JWT Access Token",
    bearerFormat="JWT",
    auto_error=False,
)


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> CurrentUser:
    """验证 Bearer Header 并返回当前认证用户。"""

    if credentials is None:
        raise UnauthorizedError(reason="missing_bearer_token")
    if credentials.scheme.lower() != "bearer" or not credentials.credentials:
        raise UnauthorizedError(reason="invalid_bearer_header")
    return request.app.state.container.jwt_service.get_current_user(
        credentials.credentials
    )
