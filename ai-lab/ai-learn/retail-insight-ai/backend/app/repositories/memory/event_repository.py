from __future__ import annotations

from copy import deepcopy
from threading import RLock
from typing import Any

from app.models.event import TaskEvent


class MemoryEventRepository:
    """线程安全的内存事件仓库，用于教学与测试而非进程间共享。"""

    def __init__(self) -> None:
        """初始化按 task_id 分组的事件集合和进程内互斥锁。"""

        self._events: dict[str, list[TaskEvent]] = {}
        self._lock = RLock()

    def append(
        self,
        task_id: str,
        event_type: str,
        message: str,
        data: dict[str, Any] | None = None,
    ) -> TaskEvent:
        """在锁内分配 sequence 并追加事件，避免并发写入出现重复序号。"""

        with self._lock:
            task_events = self._events.setdefault(task_id, [])
            event = TaskEvent(
                task_id=task_id,
                sequence=len(task_events) + 1,
                event_type=event_type,
                message=message,
                data=data or {},
            )
            task_events.append(event)
            return deepcopy(event)

    def list_after(self, task_id: str, sequence: int = 0) -> list[TaskEvent]:
        """返回事件深拷贝，防止调用方修改仓库内部事实。"""

        with self._lock:
            return [
                deepcopy(event)
                for event in self._events.get(task_id, [])
                if event.sequence > sequence
            ]
