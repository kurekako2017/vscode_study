from fastapi import APIRouter, Depends

from app.api.dependencies import get_container
from app.config.container import AppContainer
from app.core.learning_trace import trace_source_chain
from app.observability.logging import get_logger, get_request_id, log_event
from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])
logger = get_logger(__name__)


@router.get("/health", response_model=HealthResponse)
async def health(container: AppContainer = Depends(get_container)) -> HealthResponse:
    """返回轻量健康状态；不在探针中执行昂贵业务逻辑。"""
    # 这里不再手写打印格式，只把“源码调用链”数据交给 learning_trace。
    # 终端里先看 main.py，再看这个路由文件，最后看 schema 文件。
    trace_source_chain(
        "GET",
        "/health",
        [
            ("backend/app/api/health.py", "router = APIRouter()"),
            ("", '@router.get("/health")'),
            ("", "health()"),
            ("backend/app/schemas/health.py", ""),
            ("", "HealthResponse"),
            ("", "JSON"),
            ("", "HTTP Response"),
        ],
    )
    log_event(logger, "info", "health_check", "Health check completed", status="ok")
    # 构造响应模型，返回健康状态、服务名称、提供者名称和请求 ID
    response = HealthResponse(
        status="ok",
        service=container.settings.service_name,
        provider=container.settings.research_provider,
        request_id=get_request_id(),
    )
    return response
