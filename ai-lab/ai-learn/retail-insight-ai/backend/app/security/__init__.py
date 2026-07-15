"""Enterprise JWT authentication boundary.

本目录只负责“凭证 -> JWT -> Current User”的认证链路，不包含权限判断。
未来 RBAC 可以依赖 ``CurrentUser``，但不能把权限规则塞进 Token 解析过程。
"""

from app.security.authentication import AuthenticationService
from app.security.contracts import AccessToken, CurrentUser, TokenPayload
from app.security.jwt_provider import JWTProvider, PyJWTProvider
from app.security.jwt_service import JWTService

__all__ = [
    "AccessToken",
    "AuthenticationService",
    "CurrentUser",
    "JWTProvider",
    "JWTService",
    "PyJWTProvider",
    "TokenPayload",
]
