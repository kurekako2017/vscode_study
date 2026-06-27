from fastapi import APIRouter, Depends

from app.api.dependencies import get_container
from app.config.container import AppContainer
from app.observability.logging import get_logger, log_event
from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])
logger = get_logger(__name__)


@router.get("/health", response_model=HealthResponse)
async def health(container: AppContainer = Depends(get_container)) -> HealthResponse:
    """返回轻量健康状态；不在探针中执行昂贵业务逻辑。"""

    log_event(logger, "info", "health_check", "Health check completed", status="ok")
    return HealthResponse(
        status="ok",
        service=container.settings.app_name,
        provider=container.settings.mock_provider,
    )
