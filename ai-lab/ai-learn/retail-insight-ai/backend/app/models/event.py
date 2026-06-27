from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from app.models.task import utc_now


@dataclass(frozen=True)
class TaskEvent:
    """表示任务时间线中的不可变事件，sequence 用于 SSE 顺序与续传。"""

    task_id: str
    sequence: int
    event_type: str
    message: str
    data: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=utc_now)
