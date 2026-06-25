from __future__ import annotations

"""Task repository adapter.

教学要点：
- Application Service 不直接依赖 SQLiteCheckpointStore 的具体实现。
- 后续换 PostgreSQL、DynamoDB 或 Cloud SQL 时，优先替换这个 adapter。
"""

from pathlib import Path
from typing import Any

from ...checkpoint.store import SQLiteCheckpointStore
from ...models import AnalysisState


class TaskRepository:
    """Repository boundary for task persistence.

    这个类看起来只是转发，但它是有意义的边界：Application Service 只依赖
    Repository 接口形状，不关心底层现在是 SQLite，未来是 PostgreSQL 还是云数据库。
    """

    def __init__(self, db_path: Path) -> None:
        """Create the concrete SQLite store used by this teaching project."""
        self.store = SQLiteCheckpointStore(db_path)

    def create(self, task_id: str, question: str, mode: str) -> None:
        """Persist a newly queued task."""
        self.store.create_task(task_id, question, mode)

    def update_status(self, task_id: str, status: str) -> None:
        """Move a task through queued/running/completed/failed states."""
        self.store.update_status(task_id, status)

    def save_event(self, task_id: str, event: dict[str, Any]) -> None:
        """Append one event for streaming replay and audit."""
        self.store.save_event(task_id, event)

    def save_state(self, task_id: str, state: AnalysisState, status: str = "completed") -> None:
        """Persist the final AnalysisState and report markdown."""
        self.store.save_state(task_id, state, status)

    def get(self, task_id: str) -> dict[str, Any] | None:
        """Load one task row."""
        return self.store.get_task(task_id)

    def list(self, limit: int = 20) -> list[dict[str, Any]]:
        """Load recent task rows."""
        return self.store.list_tasks(limit)

    def events(self, task_id: str) -> list[dict[str, Any]]:
        """Load persisted event history for one task."""
        return self.store.get_events(task_id)
