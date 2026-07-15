"""Login HTTP Contract。

文件职责：定义用户名密码登录输入与 Access Token 输出。
谁调用它：Auth API。
它调用谁：Pydantic 与 security AccessToken contract。
输入：username、password。
输出：access_token、token_type、expires_in。
设计理由：密码只存在请求生命周期中，响应不返回用户权限。
日本现场面试：Login 是认证入口，CurrentUser 是后续 API 身份入口。
"""

from __future__ import annotations

from pydantic import BaseModel, Field, SecretStr

from app.security.contracts import AccessToken


class LoginRequest(BaseModel):
    """用户名密码登录请求。"""

    username: str = Field(min_length=1, max_length=128)
    password: SecretStr


class AccessTokenResponse(BaseModel):
    """Access Token HTTP response。"""

    access_token: str
    token_type: str
    expires_in: int

    @classmethod
    def from_contract(cls, token: AccessToken) -> "AccessTokenResponse":
        """从 security contract 构造 HTTP response。"""

        return cls.model_validate(token.model_dump())
