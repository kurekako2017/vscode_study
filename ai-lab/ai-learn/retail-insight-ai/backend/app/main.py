"""FastAPI 应用组合入口。

文件职责：创建应用、请求上下文、异常处理器，并注册匿名与受保护路由。
谁调用它：Uvicorn 读取模块级 ``app``；测试通过 ``create_app()`` 创建隔离应用。
它调用谁：AppContainer、日志/错误设施、各 API Router 与 Security Dependency。
输入：可选 Settings，以及运行时 HTTP Request。
输出：组装完成的 FastAPI application。
设计理由：认证统一挂载，授权由 Router 声明 Permission，业务逻辑不解析 JWT 或判断 role。
日本现场面试：组合根区分匿名入口与 Bearer 业务入口，RBAC 再接在 CurrentUser 后面。
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.audit_logs import router as audit_logs_router
from app.api.security import router as security_router
from app.api.document_chunks import router as document_chunks_router
from app.api.document_retrieval import router as document_retrieval_router
from app.api.document_imports import router as document_imports_router
from app.api.documents import router as documents_router
from app.api.approvals import router as approvals_router
from app.api.internal_rag import router as internal_rag_router
from app.api.ai_analysis import router as ai_analysis_router
from app.api.executive_reports import router as executive_reports_router
from app.api.tasks import router as tasks_router
from app.config.container import build_container
from app.config.settings import Settings
from app.core.learning_trace import (
    configure_learning_trace,
    trace_enter,
    trace_exit,
    trace_source_chain,
)
from app.errors.handlers import register_exception_handlers
from app.security.dependencies import get_current_user
from app.security.errors import register_authentication_exception_handler
from app.observability.logging import (
    bind_request_id,
    configure_logging,
    get_logger,
    log_event,
    reset_request_id,
)

# 模块级 logger，供请求中间件和异常处理使用。
logger = get_logger(__name__)


def create_app(settings: Settings | None = None) -> FastAPI:
    """组装 FastAPI、依赖容器、路由和请求日志上下文。

    使用工厂函数而不是直接堆叠全局对象，测试可以为每个用例创建隔离的 InMemory
    Repository，同时生产部署仍然能使用模块末尾的 ``app`` 入口。
    """
    # 先构建容器。
    container = build_container(settings)  # 创建依赖容器
    # 配置结构化日志。
    configure_logging(container.settings.service_name, container.settings.log_level)
    # 学习调用链默认关闭。
    configure_learning_trace(container.settings.learning_trace)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        """在进程生命周期边界记录启动和停止事件。"""

        log_event(logger, "info", "application_started", "FastAPI application started")
        yield
        log_event(logger, "info", "application_stopped", "FastAPI application stopped")

    # 创建 FastAPI 应用。
    application = FastAPI(
        title=container.settings.app_name,
        version="0.1.0",
        description="Retail Insight AI deployable local backend",
        lifespan=lifespan,
    )
    # 注册 CORS 中间件。
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
        # 为本次 HTTP 请求准备 request_id。
        request_id = request.headers.get("X-Request-ID") or str(uuid4())
        # 绑定 request_id，便于后续日志串联。
        token = bind_request_id(request_id)
        try:
            trace_enter(
                request.method,  # HTTP 方法
                request.url.path,  # API 路径
                node="HTTP Request",  # Learning Trace 分类
                class_name="FastAPI",  # 当前执行类
                file_path="backend/app/main.py",  # 源码文件
                defer_flush=request.method == "POST" and request.url.path == "/api/tasks",  # 仅任务创建延迟打印
            )
            if request.url.path == "/health":
                trace_source_chain(
                    request.method,  # HTTP 方法
                    request.url.path,  # API 路径
                    [
                        ("backend/app/main.py", "create_app()"),  # 应用工厂
                        ("", "（路由已注册）"),  # 路由已注册
                    ],
                )
            elif request.url.path == "/api/tasks":
                trace_source_chain(
                    request.method,  # HTTP 方法
                    request.url.path,  # API 路径
                    [
                        ("backend/app/main.py", "create_app()"),  # 应用工厂
                        ("", "（路由已注册）"),  # 路由已注册
                    ],
                )
            response = await call_next(request)
            trace_exit(
                request.method,  # HTTP 方法
                request.url.path,  # API 路径
                response_status=response.status_code,  # HTTP 状态码
                node="HTTP Response",  # Learning Trace 分类
                class_name="FastAPI",  # 当前执行类
                file_path="backend/app/main.py",  # 源码文件
            )
            response.headers["X-Request-ID"] = request_id
            return response
        finally:
            reset_request_id(token)

    # 容器放到 app.state，供 Depends 直接读取。
    application.state.container = container
    # 注册异常处理器和路由。
    register_exception_handlers(application)
    register_authentication_exception_handler(application)
    # Health、Login 与 OpenAPI/Swagger 保持匿名可达。
    application.include_router(health_router)
    application.include_router(auth_router)
    # 所有业务 API 先统一认证；每个 Router 再声明所需 Permission。
    authentication_dependencies = [Depends(get_current_user)]
    application.include_router(
        security_router, dependencies=authentication_dependencies
    )
    application.include_router(
        audit_logs_router, dependencies=authentication_dependencies
    )
    application.include_router(
        documents_router, dependencies=authentication_dependencies
    )
    application.include_router(
        document_chunks_router, dependencies=authentication_dependencies
    )
    application.include_router(
        document_retrieval_router, dependencies=authentication_dependencies
    )
    application.include_router(
        internal_rag_router, dependencies=authentication_dependencies
    )
    application.include_router(
        ai_analysis_router, dependencies=authentication_dependencies
    )
    application.include_router(
        executive_reports_router, dependencies=authentication_dependencies
    )
    application.include_router(
        approvals_router, dependencies=authentication_dependencies
    )
    application.include_router(
        document_imports_router, dependencies=authentication_dependencies
    )
    application.include_router(
        router=tasks_router, dependencies=authentication_dependencies
    )
    return application


app = create_app()
