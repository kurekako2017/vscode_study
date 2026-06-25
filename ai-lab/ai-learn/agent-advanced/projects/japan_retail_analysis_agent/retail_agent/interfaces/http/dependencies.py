from __future__ import annotations

"""FastAPI dependency functions.

教学要点：
- Router 通过 Depends 获取 service/event_bus/metrics。
- 这样测试或生产环境可以替换 app.state 中的实现。
"""

from fastapi import Request

from ...application.task_service import TaskService
from ...events.bus import EventBus
from ...infrastructure.observability.metrics import InMemoryMetrics


def get_task_service(request: Request) -> TaskService:
    """Return the application service from app state."""
    return request.app.state.task_service


def get_event_bus(request: Request) -> EventBus:
    """Return the shared event bus."""
    return request.app.state.event_bus


def get_metrics(request: Request) -> InMemoryMetrics:
    """Return metrics collector."""
    return request.app.state.metrics
