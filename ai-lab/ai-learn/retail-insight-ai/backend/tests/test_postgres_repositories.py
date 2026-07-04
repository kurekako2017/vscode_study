from __future__ import annotations

import os
import unittest
from pathlib import Path
from uuid import uuid4

from app.db.connection import PostgresConfig, PostgresConnectionFactory
from app.models.report import Report, ReportStatus
from app.models.task import Task
from app.repositories.postgres.event_repository import PostgresEventRepository
from app.repositories.postgres.report_repository import PostgresReportRepository
from app.repositories.postgres.task_repository import PostgresTaskRepository


class PostgresRepositoryIntegrationTest(unittest.TestCase):
    """验证 PostgreSQL Repository 的最小持久化能力。"""

    @classmethod
    def setUpClass(cls) -> None:
        try:
            import psycopg  # noqa: F401
        except ImportError as exc:
            raise unittest.SkipTest("psycopg is not installed in current environment") from exc

        config = PostgresConfig(
            host=os.environ.get("POSTGRES_HOST", "127.0.0.1"),
            port=int(os.environ.get("POSTGRES_PORT", "5432")),
            db=os.environ.get("POSTGRES_DB", "retail_insight_ai"),
            user=os.environ.get("POSTGRES_USER", "retail_user"),
            password=os.environ.get("POSTGRES_PASSWORD", "retail_password"),
        )
        cls.connection_factory = PostgresConnectionFactory(config)
        try:
            cls.connection_factory.initialize_schema(
                Path("db/schema.sql")
            )
            with cls.connection_factory.connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
        except Exception as exc:
            raise unittest.SkipTest(
                f"PostgreSQL is not reachable for integration test: {type(exc).__name__}"
            ) from exc

    def setUp(self) -> None:
        self.task_repository = PostgresTaskRepository(self.connection_factory)
        self.event_repository = PostgresEventRepository(self.connection_factory)
        self.report_repository = PostgresReportRepository(self.connection_factory)
        self._cleanup_tables()

    def test_create_task_append_event_and_save_report(self) -> None:
        task = Task(task_id=str(uuid4()), question="売上を分析", mode="hybrid")
        self.task_repository.create(task)

        loaded_task = self.task_repository.get(task.task_id)
        self.assertIsNotNone(loaded_task)
        self.assertEqual(loaded_task.task_id, task.task_id)

        event = self.event_repository.append(
            task.task_id,
            "status",
            "Task queued",
            {"status": "queued"},
        )
        self.assertEqual(event.sequence, 1)
        self.assertEqual(self.event_repository.list_after(task.task_id, 0)[0].message, "Task queued")

        report = Report(
            task_id=task.task_id,
            markdown="# report",
            provider="static",
            status=ReportStatus.GENERATED,
        )
        self.report_repository.save(report)

        loaded_report = self.report_repository.get(task.task_id)
        self.assertIsNotNone(loaded_report)
        self.assertEqual(loaded_report.markdown, "# report")
        self.assertEqual(loaded_report.status, ReportStatus.GENERATED)

    def _cleanup_tables(self) -> None:
        with self.connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM approval_events")
                cursor.execute("DELETE FROM approval_requests")
                cursor.execute("DELETE FROM import_errors")
                cursor.execute("DELETE FROM data_imports")
                cursor.execute("DELETE FROM report_versions")
                cursor.execute("DELETE FROM reports")
                cursor.execute("DELETE FROM task_events")
                cursor.execute("DELETE FROM tasks")


if __name__ == "__main__":
    unittest.main()
