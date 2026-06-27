from __future__ import annotations

from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI
from fastapi import Request

from app.api.health import router as health_router
from app.api.tasks import router as tasks_router
from app.config.container import build_container
from app.config.settings import Settings
from app.observability.logging import (
    bind_request_id,
    configure_logging,
    get_logger,
    log_event,
    reset_request_id,
)

logger = get_logger(__name__)


def create_app(settings: Settings | None = None) -> FastAPI:
    """组装 FastAPI、依赖容器、路由和请求日志上下文。

    使用工厂函数而不是直接堆叠全局对象，测试可以为每个用例创建隔离的 Memory
    Repository，同时生产部署仍然能使用模块末尾的 ``app`` 入口。
    """

    container = build_container(settings)
    configure_logging(container.settings.app_name, container.settings.log_level)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        """在进程生命周期边界记录启动和停止事件。"""

        log_event(logger, "info", "application_started", "FastAPI application started")
        yield
        log_event(logger, "info", "application_stopped", "FastAPI application stopped")

    application = FastAPI(
        title=container.settings.app_name,
        version="0.1.0",
        description="Retail Insight AI mock backend",
        lifespan=lifespan,
    )

    @application.middleware("http")
    async def request_context(request: Request, call_next):
        """为每个 HTTP 请求建立 request_id，便于跨路由关联日志。"""

        request_id = request.headers.get("X-Request-ID") or str(uuid4())
        token = bind_request_id(request_id)
        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = request_id
            return response
        finally:
            reset_request_id(token)

    # 容器放在 app.state 中，让 Depends 只负责取依赖，不负责重复创建依赖。
    application.state.container = container
    application.include_router(health_router)
    application.include_router(tasks_router)
    return application


app = create_app()
