"""SSE 对外事件结构；不使用普通 API envelope。"""

from datetime import datetime

from pydantic import BaseModel

from app.models.event import TaskEvent


class TaskEventResponse(BaseModel):
    """扁平化任务事件，让前端无需再解析嵌套 data。"""

    task_id: str
    sequence: int
    event: str
    status: str
    message: str
    request_id: str
    error_code: str | None = None
    node: str | None = None
    report_path: str | None = None
    created_at: datetime

    @classmethod
    def from_domain(cls, event: TaskEvent) -> "TaskEventResponse":
        """从内部 TaskEvent 选择 SSE 允许公开的标准字段。"""

        return cls(
            task_id=event.task_id,
            sequence=event.sequence,
            event=event.event_type,
            status=str(event.data.get("status", "unknown")),
            message=event.message,
            request_id=str(event.data.get("request_id", "-")),
            error_code=event.data.get("error_code"),
            node=event.data.get("node"),
            report_path=event.data.get("report_path"),
            created_at=event.created_at,
        )
