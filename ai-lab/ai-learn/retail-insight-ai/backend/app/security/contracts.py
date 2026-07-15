"""统一 JWT Contract。

文件职责：定义 Access Token、Token Payload 与 Current User 三个稳定边界。
谁调用它：Login API、JWTService、JWT Dependency 和受保护 API。
它调用谁：仅依赖 Pydantic，不包含密码校验或权限规则。
输入：认证成功后的主体信息及 JWT 标准时间字段。
输出：可校验、可序列化的认证合同。
设计理由：JWT 只携带身份快照；权限判定以后挂在 CurrentUser 后面。
日本现场面试：Authentication 与 Authorization 分层，Token 不承载 permission matrix。
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class AccessToken(BaseModel):
    """登录成功后返回的 Bearer Access Token。"""

    access_token: str
    token_type: str = "bearer"
    expires_in: int = Field(gt=0, description="Access Token 剩余有效秒数")


class TokenPayload(BaseModel):
    """冻结 JWT 身份载荷；不写入 permissions 等授权业务字段。"""

    sub: str = Field(min_length=1)
    user_id: str = Field(min_length=1)
    username: str = Field(min_length=1)
    role: str = Field(min_length=1)
    iat: datetime
    exp: datetime
    jti: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_identity_and_lifetime(self) -> "TokenPayload":
        """保证 subject 与 user_id 一致，且过期时间晚于签发时间。"""

        if self.sub != self.user_id:
            raise ValueError("sub must equal user_id")
        if self.exp <= self.iat:
            raise ValueError("exp must be later than iat")
        return self


class CurrentUser(BaseModel):
    """认证完成后的最小主体，供 API 注入并为未来 RBAC 保留 role。"""

    model_config = ConfigDict(frozen=True)

    user_id: str = Field(min_length=1)
    username: str = Field(min_length=1)
    role: str = Field(min_length=1)

    @classmethod
    def from_payload(cls, payload: TokenPayload) -> "CurrentUser":
        """从已验证 Token Payload 构造当前用户，不执行权限判断。"""

        return cls(
            user_id=payload.user_id,
            username=payload.username,
            role=payload.role,
        )
