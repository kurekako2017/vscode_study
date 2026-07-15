"""JWT Provider 抽象与 PyJWT 实现。

文件职责：只负责 JWT 编码、签名验证和标准异常映射。
谁调用它：JWTService。
它调用谁：PyJWT，不调用 API、业务 Service 或 Repository。
输入：TokenPayload 字典或 JWT 字符串。
输出：签名后的字符串或已验证的 payload 字典。
设计理由：第三方 JWT 库被隔离在 Provider，未来可替换算法/密钥托管实现。
日本现场面试：Service 管生命周期，Provider 管密码学库边界。
"""

from __future__ import annotations

from typing import Any, Protocol

import jwt

from app.security.config import JWTConfig
from app.security.errors import TokenExpiredError, UnauthorizedError


class JWTProvider(Protocol):
    """JWT 编解码 Provider Contract。"""

    def encode(self, payload: dict[str, Any]) -> str: ...

    def decode(self, token: str) -> dict[str, Any]: ...


class PyJWTProvider:
    """使用集中配置完成 HS256 签名与验证。"""

    def __init__(self, config: JWTConfig) -> None:
        self._config = config

    def encode(self, payload: dict[str, Any]) -> str:
        """签发 JWT；密钥和完整 payload 都不会进入日志。"""

        return jwt.encode(
            payload,
            self._config.secret_key,
            algorithm=self._config.algorithm,
        )

    def decode(self, token: str) -> dict[str, Any]:
        """验证签名、exp、iat 和必需 claims，并映射为稳定认证错误。"""

        try:
            return jwt.decode(
                token,
                self._config.secret_key,
                algorithms=[self._config.algorithm],
                options={
                    "require": ["sub", "user_id", "username", "role", "iat", "exp", "jti"],
                    "verify_exp": True,
                    "verify_iat": True,
                },
            )
        except jwt.ExpiredSignatureError as exception:
            raise TokenExpiredError(reason="token_expired") from exception
        except jwt.InvalidTokenError as exception:
            raise UnauthorizedError(reason="invalid_token") from exception
