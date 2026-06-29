"""API Router 汇总入口。

文件职责：把 health、question、event、approval 子路由合并成一个 Router。
谁调用它：``app.main.create_app``；它调用各 ``routes/*.py`` 模块。
输入：各子路由声明；输出：供 FastAPI 注册的 ``router``。
初学者重点：这里没有业务逻辑，只负责组织 URL 边界。
日本现场面试：可称为 API 模块的聚合入口；企业级可按版本挂载 ``/api/v1``。
"""

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
