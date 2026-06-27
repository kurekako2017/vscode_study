"""TaskRepository 的单进程内存实现。"""

from __future__ import annotations

from copy import deepcopy
from threading import RLock

from app.models.task import Task


class InMemoryTaskRepository:
    """线程安全的本地任务仓库，实现真实 Repository 合同但不提供持久化。"""

    def __init__(self) -> None:
        """初始化任务映射和保护并发访问的进程内锁。"""

        self._tasks: dict[str, Task] = {}
        self._lock = RLock()

    def create(self, task: Task) -> None:
        """创建任务并拒绝重复 ID，保持 create 的语义明确。"""

        with self._lock:
            if task.task_id in self._tasks:
                raise ValueError(f"Task already exists: {task.task_id}")
            self._tasks[task.task_id] = deepcopy(task)

    def get(self, task_id: str) -> Task | None:
        """返回任务深拷贝，避免绕过 save 修改仓库状态。"""

        with self._lock:
            task = self._tasks.get(task_id)
            return deepcopy(task) if task is not None else None

    def save(self, task: Task) -> None:
        """保存已存在任务；未知 ID 表示调用流程存在错误。"""

        with self._lock:
            if task.task_id not in self._tasks:
                raise KeyError(task.task_id)
            self._tasks[task.task_id] = deepcopy(task)
