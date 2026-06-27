from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum

from app.errors.exceptions import InvalidTaskStateException


def utc_now() -> datetime:
    """统一生成带时区 UTC 时间，避免服务器本地时区造成排序歧义。"""

    return datetime.now(timezone.utc)


class TaskStatus(StrEnum):
    """定义任务允许公开的生命周期状态。"""

    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    """任务聚合根，负责保护自身状态迁移约束。"""

    task_id: str
    question: str
    mode: str
    status: TaskStatus = TaskStatus.QUEUED
    error: str | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def transition(self, status: TaskStatus, error: str | None = None) -> None:
        """迁移任务状态，并禁止已经终止的任务跳到另一个状态。"""

        terminal = {TaskStatus.COMPLETED, TaskStatus.FAILED}
        if self.status in terminal and status != self.status:
            raise InvalidTaskStateException(self.task_id, self.status.value, status.value)
        self.status = status
        self.error = error
        self.updated_at = utc_now()
