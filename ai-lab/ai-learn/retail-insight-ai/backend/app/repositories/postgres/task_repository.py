"""TaskRepository 的 PostgreSQL 实现。

文件职责：
- 负责 tasks 表的 create / get / save。
- 当前由组合根在 `REPOSITORY_BACKEND=postgres` 时注入。
- 保持与 `TaskRepository` Protocol 一致。

输入：
- `Task`

输出：
- `Task | None`

为什么需要这一层：
- 让 Service 继续依赖抽象接口，而不是依赖 SQL 细节。

日本现场面试怎么讲：
- 当前是最小可行的事务事实持久化实现，后续可接 Alembic、连接池和更细的查询接口。
"""

from __future__ import annotations

from datetime import datetime

from app.db.connection import PostgresConnectionFactory
from app.models.task import Task, TaskStatus


class PostgresTaskRepository:
    """TaskRepository 的 PostgreSQL 实现。"""

    def __init__(self, connection_factory: PostgresConnectionFactory) -> None:
        """注入连接工厂，避免 Repository 自己管理配置。"""

        self._connection_factory = connection_factory

    def create(self, task: Task) -> None:
        """创建任务，并拒绝重复 ID。"""

        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO tasks (
                        task_id, question, mode, status, error, created_at, updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        task.task_id,
                        task.question,
                        task.mode,
                        task.status.value,
                        task.error,
                        task.created_at,
                        task.updated_at,
                    ),
                )

    def get(self, task_id: str) -> Task | None:
        """按 ID 读取任务。"""

        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT task_id, question, mode, status, error, created_at, updated_at
                    FROM tasks
                    WHERE task_id = %s
                    """,
                    (task_id,),
                )
                row = cursor.fetchone()
        return self._to_domain(row) if row is not None else None

    def save(self, task: Task) -> None:
        """保存任务最新状态。"""

        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE tasks
                    SET question = %s,
                        mode = %s,
                        status = %s,
                        error = %s,
                        updated_at = %s
                    WHERE task_id = %s
                    """,
                    (
                        task.question,
                        task.mode,
                        task.status.value,
                        task.error,
                        task.updated_at,
                        task.task_id,
                    ),
                )
                if cursor.rowcount == 0:
                    raise KeyError(task.task_id)

    def _to_domain(self, row: tuple[str, str, str, str, str | None, datetime, datetime]) -> Task:
        """把数据库行转换为领域 Task。"""

        task_id, question, mode, status, error, created_at, updated_at = row
        return Task(
            task_id=task_id,
            question=question,
            mode=mode,
            status=TaskStatus(status),
            error=error,
            created_at=created_at,
            updated_at=updated_at,
        )
