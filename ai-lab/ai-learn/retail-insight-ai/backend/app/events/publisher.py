from __future__ import annotations

from typing import Any

from app.models.event import TaskEvent
from app.repositories.interfaces.event_repository import EventRepository


class EventPublisher:
    """把业务层的进度通知写入统一 EventRepository。"""

    def __init__(self, repository: EventRepository) -> None:
        """保存事件仓库接口，使发布方不关心事件存在哪里。"""

        self._repository = repository

    def publish(
        self,
        task_id: str,
        event_type: str,
        message: str,
        data: dict[str, Any] | None = None,
    ) -> TaskEvent:
        """追加不可变任务事件，并返回仓库分配了 sequence 的结果。"""

        return self._repository.append(task_id, event_type, message, data)
