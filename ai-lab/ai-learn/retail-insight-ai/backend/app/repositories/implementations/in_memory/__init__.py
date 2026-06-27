"""适合单进程本地部署的 InMemory Repository 实现。"""

from app.repositories.implementations.in_memory.event_repository import InMemoryEventRepository
from app.repositories.implementations.in_memory.report_repository import InMemoryReportRepository
from app.repositories.implementations.in_memory.task_repository import InMemoryTaskRepository

__all__ = ["InMemoryEventRepository", "InMemoryReportRepository", "InMemoryTaskRepository"]
