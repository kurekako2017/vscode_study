"""Authentication Error Contract 与统一 401 响应。

文件职责：区分缺失/非法凭证、登录失败和 Token Expired，全部安全降级为 401。
谁调用它：Password/JWT Service 与 CurrentUser Dependency。
它调用谁：FastAPI 异常处理器和项目统一响应/结构化日志设施。
输入：稳定错误码与不含敏感凭证的原因。
输出：带 ``WWW-Authenticate: Bearer`` 的统一 401 envelope。
设计理由：认证失败不能落入未知异常处理器变成 500。
日本现场面试：错误分类可观测，但响应不泄露密码、Token 或签名细节。
"""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.observability.logging import get_logger, get_request_id, log_event
from app.schemas.common import ApiError, ApiResponse

logger = get_logger(__name__)


class AuthenticationError(Exception):
    """所有可预期认证失败的基类。"""

    error_code = "authentication_error"
    message = "Authentication failed"
    status_code = 401

    def __init__(self, *, reason: str) -> None:
        super().__init__(self.message)
        self.reason = reason


class UnauthorizedError(AuthenticationError):
    """Token 缺失、格式错误、签名错误或载荷非法。"""

    error_code = "unauthorized"
    message = "Authentication credentials are invalid"


class InvalidCredentialsError(UnauthorizedError):
    """用户名或密码不正确；不向客户端区分具体字段。"""

    error_code = "invalid_credentials"
    message = "Username or password is incorrect"


class TokenExpiredError(AuthenticationError):
    """Access Token 已超过 exp。"""

    error_code = "token_expired"
    message = "Access token has expired"


def register_authentication_exception_handler(application: FastAPI) -> None:
    """注册认证专用处理器，稳定返回 401 而不是 500。"""

    @application.exception_handler(AuthenticationError)
    async def authentication_exception_handler(
        _: Request,
        exception: AuthenticationError,
    ) -> JSONResponse:
        request_id = get_request_id()
        log_event(
            logger,
            "warning",
            "authentication_failed",
            exception.message,
            request_id=request_id,
            error_code=exception.error_code,
            status="401",
        )
        body = ApiResponse[object](
            success=False,
            request_id=request_id,
            data=None,
            error=ApiError(
                code=exception.error_code,
                message=exception.message,
                detail={"reason": exception.reason},
            ),
        )
        return JSONResponse(
            status_code=exception.status_code,
            content=body.model_dump(mode="json"),
            headers={"WWW-Authenticate": "Bearer"},
        )
