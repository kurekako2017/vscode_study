from typing import Any, Protocol

from app.models.event import TaskEvent


class EventRepository(Protocol):
    """定义任务事件的追加和按序读取合同。"""

    def append(
        self,
        task_id: str,
        event_type: str,
        message: str,
        data: dict[str, Any] | None = None,
    ) -> TaskEvent:
        """追加事件并分配任务内递增的 sequence。"""

        ...

    def list_after(self, task_id: str, sequence: int = 0) -> list[TaskEvent]:
        """返回指定 sequence 之后的事件，用于 SSE 续传。"""

        ...
