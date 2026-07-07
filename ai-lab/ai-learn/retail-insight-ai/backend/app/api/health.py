from fastapi import APIRouter, Depends

from app.api.dependencies import get_container
from app.config.container import AppContainer
from app.core.learning_trace import trace_step
from app.observability.logging import get_logger, get_request_id, log_event
from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])
logger = get_logger(__name__)


@router.get("/health", response_model=HealthResponse)
async def health(container: AppContainer = Depends(get_container)) -> HealthResponse:
    """返回轻量健康状态；不在探针中执行昂贵业务逻辑。"""
    # 记录学习调用链日志
    # trace_step 函数用于记录每个步骤的调用信息，包括 HTTP 方法、路径、类名、方法名、文件路径等，最终会在请求结束时统一打印。
    trace_step(
        "GET",
        "/health",
        "Router",
        "health()",
        class_name="health.py",
        method_name="health",
        file_path="backend/app/api/health.py",
    )
    log_event(logger, "info", "health_check", "Health check completed", status="ok")
    # 构造响应模型，返回健康状态、服务名称、提供者名称和请求 ID
    response = HealthResponse(
        status="ok",
        service=container.settings.service_name,
        provider=container.settings.research_provider,
        request_id=get_request_id(),
    )
    # 记录学习调用链日志，记录响应模型的构造过程
    trace_step(
        "GET",
        "/health",
        "Schema(Response Model)",
        "HealthResponse",
        class_name="HealthResponse",
        method_name="model_construct",
        file_path="backend/app/schemas/health.py",
    )
    return response
