"""Authentication Service。

文件职责：编排用户查找、bcrypt 密码验证与 Access Token 签发。
谁调用它：Login API。
它调用谁：DeterministicTestUserProvider、PasswordService、JWTService。
输入：username、password。
输出：AccessToken。
设计理由：路由不接触 hash/JWT 细节，认证逻辑也不进入业务 services 目录。
日本现场面试：Identity Provider 可替换，HTTP/JWT contract 保持不变。
"""

from __future__ import annotations

from app.security.contracts import AccessToken, CurrentUser
from app.security.errors import InvalidCredentialsError
from app.security.jwt_service import JWTService
from app.security.password import PasswordService
from app.security.user_provider import DeterministicTestUserProvider


class AuthenticationService:
    """完成用户名密码认证并签发 Access Token。"""

    def __init__(
        self,
        user_provider: DeterministicTestUserProvider,
        password_service: PasswordService,
        jwt_service: JWTService,
    ) -> None:
        self._user_provider = user_provider
        self._password_service = password_service
        self._jwt_service = jwt_service

    def login(self, username: str, password: str) -> AccessToken:
        """登录失败统一返回同一错误，避免枚举用户名。"""

        user = self._user_provider.get_by_username(username)
        password_hash = (
            user.password_hash
            if user is not None
            else self._user_provider.get_dummy_password_hash()
        )
        password_matches = self._password_service.verify(password, password_hash)
        if user is None or not password_matches:
            raise InvalidCredentialsError(reason="invalid_username_or_password")

        return self._jwt_service.create_access_token(
            CurrentUser(
                user_id=user.user_id,
                username=user.username,
                role=user.role,
            )
        )
