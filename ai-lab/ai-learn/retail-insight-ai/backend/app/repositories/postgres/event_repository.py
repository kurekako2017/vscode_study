"""EventRepository 的 PostgreSQL 实现。

文件职责：
- 负责通用 events 表的 append / list_after。
- stream_id 不设 Task 外键，因此上传、文档、导入、检索和 RAG 事件也可持久化。
"""

from __future__ import annotations

from typing import Any

from app.db.connection import PostgresConnectionFactory
from app.models.event import TaskEvent
from app.models.task import utc_now


class PostgresEventRepository:
    """EventRepository 的 PostgreSQL 实现。"""

    def __init__(self, connection_factory: PostgresConnectionFactory) -> None:
        """注入连接工厂。"""

        self._connection_factory = connection_factory

    def append(
        self,
        task_id: str,
        event_type: str,
        message: str,
        data: dict[str, Any] | None = None,
    ) -> TaskEvent:
        """追加事件，并按 stream_id 分配顺序号。"""

        event_data = data or {}
        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                # 事务级 advisory lock 防止同一 stream 并发计算出相同 sequence。
                cursor.execute("SELECT pg_advisory_xact_lock(hashtext(%s))", (task_id,))
                cursor.execute(
                    """
                    SELECT COALESCE(MAX(sequence), 0) + 1
                    FROM events
                    WHERE stream_id = %s
                    """,
                    (task_id,),
                )
                next_sequence = cursor.fetchone()[0]
                cursor.execute(
                    """
                    INSERT INTO events (
                        stream_id, sequence, event_type, message, data_json, created_at
                    ) VALUES (%s, %s, %s, %s, %s::jsonb, %s)
                    RETURNING created_at
                    """,
                    (
                        task_id,
                        next_sequence,
                        event_type,
                        message,
                        self._to_json(event_data),
                        utc_now(),
                    ),
                )
                created_at = cursor.fetchone()[0]
        return TaskEvent(
            task_id=task_id,
            sequence=next_sequence,
            event_type=event_type,
            message=message,
            data=event_data,
            created_at=created_at,
        )

    def list_after(self, task_id: str, sequence: int = 0) -> list[TaskEvent]:
        """读取指定序号之后的事件。"""

        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT stream_id, sequence, event_type, message, data_json, created_at
                    FROM events
                    WHERE stream_id = %s AND sequence > %s
                    ORDER BY sequence ASC
                    """,
                    (task_id, sequence),
                )
                rows = cursor.fetchall()
        return [self._to_domain(row) for row in rows]

    def _to_domain(self, row) -> TaskEvent:
        """把数据库行转换为领域 TaskEvent。"""

        task_id, sequence, event_type, message, data_json, created_at = row
        return TaskEvent(
            task_id=task_id,
            sequence=sequence,
            event_type=event_type,
            message=message,
            data=dict(data_json or {}),
            created_at=created_at,
        )

    def _to_json(self, payload: dict[str, Any]) -> str:
        """延迟导入 json，避免模块级无关依赖。"""

        import json

        return json.dumps(payload, ensure_ascii=False)
