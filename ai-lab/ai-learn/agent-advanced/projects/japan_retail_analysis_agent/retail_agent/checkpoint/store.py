from __future__ import annotations

"""Task checkpoint store.

教学要点：
- 这里保存业务层 task、event、final report。
- LangGraph 自己的 node checkpoint 保存在 `runtime/langgraph.sqlite3`。
- 两者分离是现场常见做法：workflow checkpoint 和业务审计表不是一回事。
"""

import json
import sqlite3
from dataclasses import asdict
from pathlib import Path
from typing import Any

from ..models import AnalysisState
from ..settings import PROJECT_DIR


class SQLiteCheckpointStore:
    """Small durable store for task status, events, and final reports.

    它保存的是业务可见状态：任务列表、事件时间线、最终报告。
    不要和 LangGraph 的节点级 checkpoint 混淆。
    """

    def __init__(self, db_path: Path = PROJECT_DIR / "runtime" / "checkpoints.sqlite3") -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _connect(self) -> sqlite3.Connection:
        """Open one short-lived SQLite connection.

        每个方法自己打开连接，避免把同一个 sqlite3 connection 跨线程复用。
        """
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _init(self) -> None:
        """Create tables if this is the first run."""
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    question TEXT NOT NULL,
                    mode TEXT NOT NULL,
                    status TEXT NOT NULL,
                    report_markdown TEXT NOT NULL DEFAULT '',
                    state_json TEXT NOT NULL DEFAULT '{}',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS task_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL,
                    event_json TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def create_task(self, task_id: str, question: str, mode: str) -> None:
        """Insert a queued task."""
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO tasks (task_id, question, mode, status)
                VALUES (?, ?, ?, 'queued')
                """,
                (task_id, question, mode),
            )

    def update_status(self, task_id: str, status: str) -> None:
        """Update task status without touching the report body."""
        with self._connect() as connection:
            connection.execute(
                "UPDATE tasks SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE task_id = ?",
                (status, task_id),
            )

    def save_event(self, task_id: str, event: dict[str, Any]) -> None:
        """Append one event to the task event log."""
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO task_events (task_id, event_json) VALUES (?, ?)",
                (task_id, json.dumps(event, ensure_ascii=False)),
            )

    def save_state(self, task_id: str, state: AnalysisState, status: str = "completed") -> None:
        """Persist final state and report after orchestration completes."""
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE tasks
                SET status = ?,
                    report_markdown = ?,
                    state_json = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE task_id = ?
                """,
                (
                    status,
                    state.report_markdown,
                    json.dumps(asdict(state), ensure_ascii=False),
                    task_id,
                ),
            )

    def get_task(self, task_id: str) -> dict[str, Any] | None:
        """Return one task as a plain dict for Pydantic response models."""
        with self._connect() as connection:
            row = connection.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,)).fetchone()
        return dict(row) if row else None

    def list_tasks(self, limit: int = 20) -> list[dict[str, Any]]:
        """Return most recent task rows first."""
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM tasks ORDER BY created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]

    def get_events(self, task_id: str) -> list[dict[str, Any]]:
        """Return event JSON in insertion order so the UI timeline is stable."""
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT event_json FROM task_events WHERE task_id = ? ORDER BY id",
                (task_id,),
            ).fetchall()
        return [json.loads(row["event_json"]) for row in rows]
