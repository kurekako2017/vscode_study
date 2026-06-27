from fastapi import Request

from app.config.container import AppContainer
from app.events.publisher import EventPublisher
from app.repositories.interfaces.event_repository import EventRepository
from app.services.task_service import TaskService


async def get_container(request: Request) -> AppContainer:
    """从 FastAPI 应用状态取得本次 App 独享的依赖容器。"""

    return request.app.state.container


async def get_task_service(request: Request) -> TaskService:
    """向路由注入 TaskService，避免路由直接构造业务依赖。"""

    return request.app.state.container.task_service


async def get_event_repository(request: Request) -> EventRepository:
    """向 SSE 路由暴露事件读取接口，而不是具体存储细节。"""

    return request.app.state.container.event_repository


async def get_event_publisher(request: Request) -> EventPublisher:
    """按需构造轻量事件发布器；底层 Repository 仍由容器统一持有。"""

    return EventPublisher(request.app.state.container.event_repository)
