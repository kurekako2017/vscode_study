from fastapi import APIRouter, Depends

from app.api.routes.dependencies import get_container
from app.config.container import AppContainer


router = APIRouter()


@router.get("/health")
async def health(container: AppContainer = Depends(get_container)) -> dict[str, str]:
    return {"status": "ok", "service": container.settings.service_name}
