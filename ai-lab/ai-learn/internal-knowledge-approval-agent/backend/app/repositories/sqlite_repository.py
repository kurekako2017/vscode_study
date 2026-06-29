"""Question、Approval、Event 的 SQLite Repository。

文件职责：建表，并以短事务保存问题、审批决定和可恢复 SSE 事件。
谁调用它：QuestionService、SSE Generator 和依赖容器；它调用 Python sqlite3。
输入：领域 ID、状态和事件数据；输出：普通 dict/list，或 KeyError/ConflictError。
为什么需要这一层：把 SQL 和事务边界从 Service/Workflow 隔离出来。
初学者重点：questions 是当前快照，events 是有序历史；审批更新带 pending 条件防止重复决定。
日本现场面试：可说明 WAL 支持本地读写并行，BEGIN IMMEDIATE 保证事件序号唯一。
当前实现：单进程 SQLite 具体类；Service 目前直接依赖它，适合 V1 本地基线。
企业级替换：抽取 Repository Interface/Unit of Work，并在 Container 绑定 PostgreSQL + Alembic；
同时增加审批版本、幂等键、不可覆盖 Audit Store 和多实例事务策略。
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ConflictError(Exception):
    """状态已被其他请求修改，调用方应返回 409。"""


class SQLiteRepository:
    """Question、Approval、Event 的单机事务存储。

    每个方法打开短连接，便于初学者看到明确事务边界；WAL 允许 SSE 读取和
    Workflow 写入并行。生产多实例需迁移 PostgreSQL，不共享 SQLite 文件。

    输入是已由 API/Service 校验的领域字段，输出使用 dict 保持教学代码直观；这里不做
    风险分类或 Workflow 路由，因为 Repository 只负责持久化。
    """

    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._database_path, timeout=5)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 5000")
        return connection

    def initialize(self) -> None:
        self._database_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute("PRAGMA journal_mode = WAL")
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS questions (
                    question_id TEXT PRIMARY KEY,
                    question TEXT NOT NULL,
                    status TEXT NOT NULL,
                    risk_level TEXT,
                    report TEXT,
                    error_code TEXT,
                    request_id TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS approvals (
                    approval_id TEXT PRIMARY KEY,
                    question_id TEXT NOT NULL UNIQUE REFERENCES questions(question_id),
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    decided_at TEXT
                );
                CREATE TABLE IF NOT EXISTS events (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id TEXT NOT NULL REFERENCES questions(question_id),
                    sequence INTEGER NOT NULL,
                    event_type TEXT NOT NULL,
                    message TEXT NOT NULL,
                    data_json TEXT NOT NULL,
                    request_id TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    UNIQUE(question_id, sequence)
                );
                CREATE INDEX IF NOT EXISTS idx_approvals_status
                    ON approvals(status, created_at);
                CREATE INDEX IF NOT EXISTS idx_events_question_sequence
                    ON events(question_id, sequence);
                """
            )

    def create_question(self, question_id: str, question: str, request_id: str) -> dict[str, Any]:
        now = utc_now()
        with self._connect() as connection:
            connection.execute(
                """INSERT INTO questions
                   (question_id, question, status, request_id, created_at, updated_at)
                   VALUES (?, ?, 'received', ?, ?, ?)""",
                (question_id, question, request_id, now, now),
            )
        return self.get_question(question_id)  # type: ignore[return-value]

    def get_question(self, question_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM questions WHERE question_id = ?", (question_id,)
            ).fetchone()
            return dict(row) if row else None

    def update_question(
        self,
        question_id: str,
        *,
        status: str,
        risk_level: str | None = None,
        report: str | None = None,
        error_code: str | None = None,
    ) -> dict[str, Any]:
        now = utc_now()
        with self._connect() as connection:
            cursor = connection.execute(
                """UPDATE questions
                   SET status = ?, risk_level = COALESCE(?, risk_level),
                       report = COALESCE(?, report), error_code = ?, updated_at = ?
                   WHERE question_id = ?""",
                (status, risk_level, report, error_code, now, question_id),
            )
            if cursor.rowcount != 1:
                raise KeyError(question_id)
        return self.get_question(question_id)  # type: ignore[return-value]

    def create_approval(self, approval_id: str, question_id: str) -> dict[str, Any]:
        now = utc_now()
        with self._connect() as connection:
            connection.execute(
                """INSERT INTO approvals
                   (approval_id, question_id, status, created_at)
                   VALUES (?, ?, 'pending', ?)""",
                (approval_id, question_id, now),
            )
        return self.get_approval(approval_id)  # type: ignore[return-value]

    def get_approval(self, approval_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                """SELECT a.*, q.question, q.risk_level, q.updated_at
                   FROM approvals a JOIN questions q ON q.question_id = a.question_id
                   WHERE a.approval_id = ?""",
                (approval_id,),
            ).fetchone()
            return dict(row) if row else None

    def get_approval_by_question(self, question_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                """SELECT a.*, q.question, q.risk_level, q.updated_at
                   FROM approvals a JOIN questions q ON q.question_id = a.question_id
                   WHERE a.question_id = ?""",
                (question_id,),
            ).fetchone()
            return dict(row) if row else None

    def list_approvals(self, status: str = "pending") -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """SELECT a.*, q.question, q.risk_level, q.updated_at
                   FROM approvals a JOIN questions q ON q.question_id = a.question_id
                   WHERE a.status = ? ORDER BY a.created_at""",
                (status,),
            ).fetchall()
            return [dict(row) for row in rows]

    def decide_approval(self, approval_id: str, decision: str) -> dict[str, Any]:
        now = utc_now()
        with self._connect() as connection:
            cursor = connection.execute(
                """UPDATE approvals SET status = ?, decided_at = ?
                   WHERE approval_id = ? AND status = 'pending'""",
                (decision, now, approval_id),
            )
            if cursor.rowcount != 1:
                # 必须复用当前连接检查存在性；在写事务中再开连接会等待自己的锁。
                exists = connection.execute(
                    "SELECT 1 FROM approvals WHERE approval_id = ?", (approval_id,)
                ).fetchone()
                if exists is None:
                    raise KeyError(approval_id)
                raise ConflictError("Approval is no longer pending")
        return self.get_approval(approval_id)  # type: ignore[return-value]

    def append_event(
        self,
        question_id: str,
        event_type: str,
        message: str,
        data: dict[str, Any],
        request_id: str,
    ) -> dict[str, Any]:
        now = utc_now()
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT COALESCE(MAX(sequence), 0) + 1 AS next FROM events WHERE question_id = ?",
                (question_id,),
            ).fetchone()
            sequence = int(row["next"])
            connection.execute(
                """INSERT INTO events
                   (question_id, sequence, event_type, message, data_json, request_id, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (question_id, sequence, event_type, message, json.dumps(data), request_id, now),
            )
        return {
            "question_id": question_id,
            "sequence": sequence,
            "event": event_type,
            "message": message,
            "request_id": request_id,
            "created_at": now,
            **data,
        }

    def list_events_after(self, question_id: str, sequence: int) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """SELECT * FROM events WHERE question_id = ? AND sequence > ?
                   ORDER BY sequence""",
                (question_id, sequence),
            ).fetchall()
        events: list[dict[str, Any]] = []
        for row in rows:
            events.append(
                {
                    "question_id": row["question_id"],
                    "sequence": row["sequence"],
                    "event": row["event_type"],
                    "message": row["message"],
                    "request_id": row["request_id"],
                    "created_at": row["created_at"],
                    **json.loads(row["data_json"]),
                }
            )
        return events
