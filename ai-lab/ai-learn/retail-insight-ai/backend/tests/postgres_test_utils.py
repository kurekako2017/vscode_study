from __future__ import annotations

from app.config.settings import Settings
from app.db.connection import PostgresConfig, PostgresConnectionFactory

ALLOWED_TEST_DATABASE = "erip_integration_test"


def reset_postgres_state_if_needed(settings: Settings) -> None:
    """PostgreSQL 模式下清空专用测试库，保持原有 InMemory 级别的测试隔离。"""

    if settings.repository_backend != "postgres" or not settings.database_url:
        return

    factory = PostgresConnectionFactory(
        PostgresConfig(host="", port=5432, db="", user="", password="", database_url=settings.database_url)
    )
    with factory.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT current_database()")
            current_database_row = cursor.fetchone()
            current_database = current_database_row[0] if current_database_row else None
            if current_database != ALLOWED_TEST_DATABASE:
                raise RuntimeError(
                    "Refusing to truncate PostgreSQL state outside the dedicated test database. "
                    f"current_database={current_database!r}, allowed_database={ALLOWED_TEST_DATABASE!r}. "
                    "This guard prevents accidental cleanup of a non-test database."
                )
            cursor.execute(
                """TRUNCATE upload_idempotency_keys,upload_sessions,document_imports,
                document_chunks,documents,audit_logs,approval_events,approval_requests,
                report_versions,reports,events,tasks RESTART IDENTITY CASCADE"""
            )
