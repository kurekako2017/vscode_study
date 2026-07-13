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
    # PostgreSQL 模式执行真实 SELECT 1；失败不会静默回退为 InMemory。
    container.database_health_check()
    trace_source_chain(
        "GET",  # HTTP 方法
        "/health",  # API 路径
        [
            ("backend/app/api/health.py", "router = APIRouter()"),  # 路由器
            ("", '@router.get("/health")'),  # GET 入口
            ("", "health()"),  # 当前执行步骤
            ("backend/app/schemas/health.py", ""),  # 响应模型文件
            ("", "HealthResponse"),  # 响应模型
            ("", "JSON"),  # 返回格式
            ("", "HTTP Response"),  # 响应阶段
        ],
    )
    log_event(logger, "info", "health_check", "Health check completed", status="ok")
    response = HealthResponse(
        status="ok",
        service=container.settings.service_name,
        provider=container.settings.research_provider,
        repository_backend=container.repository_backend,
        request_id=get_request_id(),
    )
    return response
