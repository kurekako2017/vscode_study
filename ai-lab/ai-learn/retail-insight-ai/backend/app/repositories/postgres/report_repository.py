"""ReportRepository 的 PostgreSQL 实现。

文件职责：
- 保存 reports 当前快照。
- 追加 report_versions 历史版本。
- 当前 approval_status 仅保存 `generated`，不接审批 API。
"""

from __future__ import annotations

from datetime import datetime

from app.db.connection import PostgresConnectionFactory
from app.models.report import Report, ReportStatus


class PostgresReportRepository:
    """ReportRepository 的 PostgreSQL 实现。"""

    def __init__(self, connection_factory: PostgresConnectionFactory) -> None:
        """注入连接工厂。"""

        self._connection_factory = connection_factory

    def save(self, report: Report) -> None:
        """保存当前报告快照，并记录版本历史。"""

        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO reports (task_id, markdown, provider, approval_status, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (task_id)
                    DO UPDATE SET
                        markdown = EXCLUDED.markdown,
                        provider = EXCLUDED.provider,
                        approval_status = EXCLUDED.approval_status,
                        updated_at = EXCLUDED.updated_at
                    """,
                    (
                        report.task_id,
                        report.markdown,
                        report.provider,
                        report.status.value,
                        report.created_at,
                        report.created_at,
                    ),
                )
                cursor.execute(
                    """
                    SELECT COALESCE(MAX(version_no), 0) + 1
                    FROM report_versions
                    WHERE task_id = %s
                    """,
                    (report.task_id,),
                )
                next_version = cursor.fetchone()[0]
                cursor.execute(
                    """
                    INSERT INTO report_versions (
                        task_id, version_no, markdown, status, revision_reason, created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        report.task_id,
                        next_version,
                        report.markdown,
                        report.status.value,
                        None,
                        report.created_at,
                    ),
                )

    def get(self, task_id: str) -> Report | None:
        """读取当前报告。"""

        with self._connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT task_id, markdown, provider, approval_status, created_at
                    FROM reports
                    WHERE task_id = %s
                    """,
                    (task_id,),
                )
                row = cursor.fetchone()
        return self._to_domain(row) if row is not None else None

    def _to_domain(self, row: tuple[str, str, str, str, datetime]) -> Report:
        """把数据库行转换为领域 Report。"""

        task_id, markdown, provider, approval_status, created_at = row
        return Report(
            task_id=task_id,
            markdown=markdown,
            provider=provider,
            status=ReportStatus(approval_status),
            created_at=created_at,
        )
