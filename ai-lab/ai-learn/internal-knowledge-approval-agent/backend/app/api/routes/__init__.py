from fastapi import APIRouter

from app.api.routes.approvals import router as approvals_router
from app.api.routes.events import router as events_router
from app.api.routes.health import router as health_router
from app.api.routes.questions import router as questions_router


router = APIRouter()
router.include_router(health_router)
router.include_router(questions_router)
router.include_router(events_router)
router.include_router(approvals_router)
