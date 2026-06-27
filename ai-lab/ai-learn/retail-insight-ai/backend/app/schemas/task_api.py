from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from app.models.task import Task, TaskStatus


class TaskCreateRequest(BaseModel):
    """校验创建任务所需的问题长度与受支持模式。"""

    question: str = Field(min_length=1, max_length=1000)
    mode: Literal["hybrid", "kpi", "research"] = "hybrid"


class TaskCreateResponse(BaseModel):
    """创建成功后只返回后续查询需要的 ID 与初始状态。"""

    task_id: str
    status: TaskStatus


class TaskResponse(BaseModel):
    """定义任务状态查询的 HTTP 响应合同。"""

    task_id: str
    question: str
    mode: str
    status: TaskStatus
    error: str | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_domain(cls, task: Task) -> "TaskResponse":
        """显式选择对 API 公开的 Task 字段。"""

        return cls(
            task_id=task.task_id,
            question=task.question,
            mode=task.mode,
            status=task.status,
            error=task.error,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )
