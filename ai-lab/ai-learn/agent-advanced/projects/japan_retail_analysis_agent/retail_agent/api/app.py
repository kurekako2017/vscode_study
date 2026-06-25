from __future__ import annotations

"""FastAPI application factory.

教学要点：
- `api/app.py` 不直接写业务逻辑，只负责组装 app、middleware、DI 对象和 routers。
- 真实项目中这层通常对应 Spring Boot 的 Application class 或 FastAPI 的 app factory。
- TaskService、Repository、EventBus 都挂到 `app.state`，HTTP 层通过 Depends 获取。
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..application.task_service import TaskService
from ..core.config import AppSettings, get_settings
from ..core.logging import configure_logging
from ..events.bus import EventBus
from ..infrastructure.observability.metrics import InMemoryMetrics
from ..infrastructure.repositories.task_repository import TaskRepository
from ..interfaces.http.routers import health, streams, tasks


def create_app(settings: AppSettings | None = None) -> FastAPI:
    """Create a fully wired FastAPI application.

    这一步完成“基础设施装配”：
    - 配置日志和 CORS。
    - 创建事件总线、metrics、repository、application service。
    - 注册 HTTP router。
    """

    settings = settings or get_settings()
    configure_logging(settings.log_level)
    settings.runtime_dir.mkdir(parents=True, exist_ok=True)

    app = FastAPI(title=settings.app_name, version="0.3.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.allowed_origins),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Infrastructure instances are created once per process and injected into routers.
    event_bus = EventBus()
    metrics = InMemoryMetrics()
    repository = TaskRepository(settings.task_db_path)
    task_service = TaskService(repository, event_bus, metrics)

    app.state.settings = settings
    app.state.event_bus = event_bus
    app.state.metrics = metrics
    app.state.task_service = task_service

    # Routers stay thin: they validate HTTP input/output and delegate use cases.
    app.include_router(health.router)
    app.include_router(tasks.router)
    app.include_router(streams.router)
    return app


app = create_app()

# Backward-compatible import used by tests.
health = health.health
