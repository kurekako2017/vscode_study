from __future__ import annotations

from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.tasks import router as tasks_router
from app.config.container import build_container
from app.config.settings import Settings
from app.errors.handlers import register_exception_handlers
from app.observability.logging import (
    bind_request_id,
    configure_logging,
    get_logger,
    log_event,
    reset_request_id,
)

# logger 是模块级别的全局变量，FastAPI 的依赖注入和中间件可以使用它来记录请求日志。
logger = get_logger(__name__)


## FastAPI 应用工厂函数
def create_app(settings: Settings | None = None) -> FastAPI:
    """组装 FastAPI、依赖容器、路由和请求日志上下文。

    使用工厂函数而不是直接堆叠全局对象，测试可以为每个用例创建隔离的 InMemory
    Repository，同时生产部署仍然能使用模块末尾的 ``app`` 入口。
    """
    container = build_container(settings)  # 创建依赖容器
    # 配置日志记录器，使用容器中的设置
    configure_logging(container.settings.service_name, container.settings.log_level)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        """在进程生命周期边界记录启动和停止事件。"""

        log_event(logger, "info", "application_started", "FastAPI application started")
        yield
        log_event(logger, "info", "application_stopped", "FastAPI application stopped")

    # 创建 FastAPI 应用实例，注册中间件、路由和异常处理器
    application = FastAPI(
        title=container.settings.app_name,
        version="0.1.0",
        description="Retail Insight AI deployable local backend",
        lifespan=lifespan,
    )
    # 配置 CORS 中间件，允许跨域请求
    # cors 是 Cross-Origin Resource Sharing 的缩写，允许浏览器从不同域名的服务器请求资源。
    application.add_middleware(
        CORSMiddleware,
        allow_origins=container.settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.middleware("http")
    async def request_context(request: Request, call_next):
        """为每个 HTTP 请求建立 request_id，便于跨路由关联日志。"""
        # request_id 可以从请求头中获取，如果没有则生成一个新的 UUID。
        # request_id 也可以用于追踪请求的生命周期，例如在日志中记录请求的开始和结束。
        # UUID 是通用唯一标识符（Universally Unique Identifier）的缩写，是一种标准的 128 位长的数字，用于唯一标识信息。
        # UUID 的格式通常为 8-4-4-4-12 的十六进制字符串，例如：550e8400-e29b-41d4-a716-446655440000。
        request_id = request.headers.get("X-Request-ID") or str(uuid4())
        # bind_request_id(request_id) 将 request_id 绑定到当前上下文，便于日志记录器使用。
        token = bind_request_id(request_id)
        try:
            response = await call_next(request)  # 调用下一个中间件或路由处理请求。
            response.headers["X-Request-ID"] = request_id
            return response
        finally:
            reset_request_id(
                token
            )  # 重置 request_id，以便其他中间件或请求不会受到影响。

    # 容器放在 app.state 中，让 Depends 只负责取依赖，不负责重复创建依赖。
    application.state.container = container
    # 注册异常处理器和路由
    register_exception_handlers(application)
    # 注册健康检查和任务路由
    application.include_router(health_router)
    application.include_router(router=tasks_router)
    return application


app = create_app()
