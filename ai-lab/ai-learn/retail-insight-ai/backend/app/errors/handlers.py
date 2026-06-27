"""把应用异常、校验异常和未知异常转换为统一 API envelope。"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.errors.base import AppException
from app.errors.error_codes import ErrorCode
from app.errors.exceptions import ValidationAppException
from app.observability.logging import get_logger, get_request_id, log_event
from app.schemas.common import ApiError, ApiResponse

logger = get_logger(__name__)


def _error_response(exception: AppException) -> JSONResponse:
    """从 AppException 生成稳定失败 envelope，并补齐当前 request_id。"""

    request_id = exception.request_id or get_request_id()
    body = ApiResponse[Any](
        success=False,
        request_id=request_id,
        data=None,
        error=ApiError(
            code=exception.error_code.value,
            message=exception.message,
            detail=exception.detail,
        ),
    )
    level = "error" if exception.status_code >= 500 else "warning"
    log_event(
        logger,
        level,
        "api_error",
        exception.message,
        request_id=request_id,
        task_id=exception.task_id,
        error_code=exception.error_code.value,
        status=str(exception.status_code),
    )
    return JSONResponse(status_code=exception.status_code, content=body.model_dump(mode="json"))


def register_exception_handlers(application: FastAPI) -> None:
    """注册全局处理器，避免各路由重复 try/except 和响应拼装。"""

    @application.exception_handler(AppException)
    async def app_exception_handler(_: Request, exception: AppException) -> JSONResponse:
        """处理业务层主动抛出的标准应用异常。"""

        return _error_response(exception)

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        _: Request,
        exception: RequestValidationError,
    ) -> JSONResponse:
        """把 Pydantic/FastAPI 校验错误映射为 VALIDATION_ERROR。"""

        detail = {"errors": jsonable_encoder(exception.errors())}
        return _error_response(ValidationAppException(detail=detail))

    @application.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        _: Request,
        exception: StarletteHTTPException,
    ) -> JSONResponse:
        """统一框架 404 等错误，避免返回 FastAPI 默认 detail 结构。"""

        app_exception = AppException(
            ErrorCode.HTTP_ERROR,
            "HTTP request failed",
            exception.status_code,
            detail={"reason": str(exception.detail)},
        )
        return _error_response(app_exception)

    @application.exception_handler(Exception)
    async def unexpected_exception_handler(_: Request, exception: Exception) -> JSONResponse:
        """兜底未知异常，但不把原始异常正文暴露给客户端。"""

        app_exception = AppException(
            ErrorCode.INTERNAL_ERROR,
            "Internal server error",
            500,
            detail={"exception_type": type(exception).__name__},
        )
        return _error_response(app_exception)
