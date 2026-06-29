from __future__ import annotations

from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.config.container import build_container
from app.config.logging import (
    bind_request_id,
    configure_logging,
    get_logger,
    get_request_id,
    log_event,
    reset_request_id,
)
from app.config.settings import Settings
from app.repositories.sqlite_repository import ConflictError


logger = get_logger(__name__)


def create_app(settings: Settings | None = None) -> FastAPI:
    container = build_container(settings)
    configure_logging(container.settings.service_name, container.settings.log_level)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        log_event(logger, "info", "application_started", "Application started")
        yield
        log_event(logger, "info", "application_stopped", "Application stopped")

    application = FastAPI(
        title="Internal Knowledge Approval Agent",
        version="0.1.0",
        lifespan=lifespan,
    )
    application.state.container = container
    application.add_middleware(
        CORSMiddleware,
        allow_origins=container.settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.middleware("http")
    async def request_context(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid4())
        token = bind_request_id(request_id)
        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = request_id
            log_event(
                logger,
                "info",
                "http_request_completed",
                "HTTP request completed",
                request_id=request_id,
                status=str(response.status_code),
                http_method=request.method,
                http_path=request.url.path,
            )
            return response
        finally:
            reset_request_id(token)

    def error_response(request: Request, status_code: int, code: str, message: str) -> JSONResponse:
        request_id = get_request_id()
        log_event(
            logger,
            "warning" if status_code < 500 else "error",
            "http_request_failed",
            message,
            request_id=request_id,
            status=str(status_code),
            error_code=code,
            http_method=request.method,
            http_path=request.url.path,
        )
        return JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "request_id": request_id,
                "data": None,
                "error": {"code": code, "message": message, "detail": {}},
            },
            headers={"X-Request-ID": request_id},
        )

    @application.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, _: RequestValidationError):
        return error_response(request, 422, "VALIDATION_ERROR", "Request validation failed")

    @application.exception_handler(KeyError)
    async def not_found_handler(request: Request, _: KeyError):
        return error_response(request, 404, "RESOURCE_NOT_FOUND", "Resource not found")

    @application.exception_handler(ConflictError)
    async def conflict_handler(request: Request, _: ConflictError):
        return error_response(request, 409, "APPROVAL_CONFLICT", "Approval is no longer pending")

    @application.exception_handler(RuntimeError)
    async def state_handler(request: Request, exc: RuntimeError):
        if str(exc) == "REPORT_NOT_READY":
            return error_response(request, 409, "REPORT_NOT_READY", "Final report is not ready")
        return error_response(request, 500, "INTERNAL_ERROR", "Internal server error")

    @application.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": container.settings.service_name}

    application.include_router(router)
    return application


app = create_app()
