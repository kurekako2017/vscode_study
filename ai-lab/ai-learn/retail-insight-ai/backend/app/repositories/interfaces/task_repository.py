from typing import Protocol, runtime_checkable

from app.models.task import Task


@runtime_checkable
class TaskRepository(Protocol):
    """定义 Task 聚合的创建、读取与保存合同。"""

    def create(self, task: Task) -> None:
        """创建新任务，重复 ID 应被拒绝。"""

        ...

    def get(self, task_id: str) -> Task | None:
        """按 ID 读取任务；不存在时返回 None。"""

        ...

    def save(self, task: Task) -> None:
        """保存已存在任务的最新状态。"""

        ...
