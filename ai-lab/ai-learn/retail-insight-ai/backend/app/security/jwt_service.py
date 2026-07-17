"""JWT Service。

文件职责：创建 Access Token、解析 TokenPayload，并产出 CurrentUser。
谁调用它：AuthenticationService 与 FastAPI CurrentUser Dependency。
它调用谁：JWTProvider 和统一 JWT Contract。
输入：认证主体或 Bearer Token。
输出：AccessToken、TokenPayload、CurrentUser。
设计理由：生命周期、jti 与时间注入属于 Service，不散落在路由。
日本现场面试：Token 只证明身份，权限逻辑留给后续 RBAC 层。
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from pydantic import ValidationError

from app.security.config import JWTConfig
from app.security.contracts import AccessToken, CurrentUser, TokenPayload
from app.security.errors import TokenExpiredError, UnauthorizedError
from app.security.jwt_provider import JWTProvider


def utc_now() -> datetime:
    """返回带时区 UTC 时间，便于测试注入固定时钟。"""

    return datetime.now(timezone.utc)


class JWTService:
    """管理 JWT 身份载荷与 Access Token 生命周期。"""

    def __init__(
        self,
        provider: JWTProvider,
        config: JWTConfig,
        *,
        clock: Callable[[], datetime] = utc_now,
    ) -> None:
        self._provider = provider
        self._config = config
        self._clock = clock

    def create_access_token(self, current_user: CurrentUser) -> AccessToken:
        """生成默认 30 分钟（由配置决定）的唯一 Access Token。"""

        issued_at = self._clock().astimezone(timezone.utc)
        expires_at = issued_at + timedelta(
            minutes=self._config.access_token_expire_minutes
        )
        payload = TokenPayload(
            sub=current_user.user_id,
            user_id=current_user.user_id,
            username=current_user.username,
            role=current_user.role,
            iat=issued_at,
            exp=expires_at,
            jti=str(uuid4()),
        )
        token = self._provider.encode(payload.model_dump(mode="python"))
        return AccessToken(
            access_token=token,
            expires_in=self._config.access_token_expire_minutes * 60,
        )

    def parse_token(self, token: str) -> TokenPayload:
        """解析并二次校验载荷；非法 payload 稳定返回 401。

        Provider 层已按 leeway 校验 exp/iat。这里的 exp 二次校验同步应用
        同一 leeway，避免 Provider 接受后 Service 因时钟抖动再次误杀。
        """

        try:
            payload = TokenPayload.model_validate(self._provider.decode(token))
        except (ValidationError, ValueError, TypeError) as exception:
            raise UnauthorizedError(reason="invalid_token_payload") from exception

        now = self._clock().astimezone(timezone.utc)
        leeway = timedelta(seconds=max(0, self._config.leeway_seconds))
        if payload.exp + leeway <= now:
            raise TokenExpiredError(reason="token_expired")
        return payload

    def get_current_user(self, token: str) -> CurrentUser:
        """把已验证 payload 转成 API 可注入的 CurrentUser。"""

        return CurrentUser.from_payload(self.parse_token(token))
