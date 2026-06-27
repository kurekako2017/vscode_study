from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.models.event import TaskEvent


class TaskEventResponse(BaseModel):
    """定义 SSE data 字段中对前端公开的事件结构。"""

    task_id: str
    sequence: int
    event: str
    message: str
    data: dict[str, Any]
    created_at: datetime

    @classmethod
    def from_domain(cls, event: TaskEvent) -> "TaskEventResponse":
        """显式映射领域事件，避免直接暴露内部对象。"""

        return cls(
            task_id=event.task_id,
            sequence=event.sequence,
            event=event.event_type,
            message=event.message,
            data=event.data,
            created_at=event.created_at,
        )
