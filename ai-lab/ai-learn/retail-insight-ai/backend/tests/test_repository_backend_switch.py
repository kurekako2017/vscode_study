from __future__ import annotations

import unittest
from unittest.mock import patch

from app.config.container import build_container
from app.config.settings import Settings
from app.repositories.implementations.in_memory.event_repository import InMemoryEventRepository
from app.repositories.postgres.event_repository import PostgresEventRepository
from app.repositories.postgres.approval_repository import PostgresApprovalRepository
from app.repositories.postgres.audit_repository import PostgresAuditRepository
from app.repositories.postgres.document_repository import PostgresDocumentRepository
from app.repositories.postgres.document_chunk_repository import PostgresDocumentChunkRepository
from app.repositories.postgres.document_import_repository import PostgresDocumentImportRepository
from app.repositories.postgres.upload_session_repository import PostgresUploadSessionRepository


class RepositoryBackendSwitchTest(unittest.TestCase):
    """验证组合根能在 InMemory 与 PostgreSQL Repository 之间切换。"""

    def test_inmemory_backend_remains_default(self) -> None:
        container = build_container(
            Settings(
                repository_backend="inmemory",
                workflow_step_delay_seconds=0,
                log_level="CRITICAL",
            )
        )

        self.assertEqual(container.repository_backend, "inmemory")
        self.assertIsInstance(container.event_repository, InMemoryEventRepository)

    def test_postgres_backend_builds_postgres_repositories(self) -> None:
        with (
            patch("app.config.container.PostgresConnectionFactory.initialize_schema") as initialize_schema,
            patch("app.config.container.PostgresConnectionFactory.health_check") as health_check,
        ):
            container = build_container(
                Settings(
                    repository_backend="postgres",
                    workflow_step_delay_seconds=0,
                    log_level="CRITICAL",
                )
            )

        initialize_schema.assert_called_once()
        health_check.assert_called_once()
        self.assertEqual(container.repository_backend, "postgres")
        self.assertIsInstance(container.event_repository, PostgresEventRepository)
        self.assertIsInstance(container.approval_repository, PostgresApprovalRepository)
        self.assertIsInstance(container.audit_repository, PostgresAuditRepository)
        self.assertIsInstance(container.document_repository, PostgresDocumentRepository)
        self.assertIsInstance(container.document_chunk_repository, PostgresDocumentChunkRepository)
        self.assertIsInstance(container.document_import_repository, PostgresDocumentImportRepository)
        self.assertIsInstance(container.upload_session_repository, PostgresUploadSessionRepository)


if __name__ == "__main__":
    unittest.main()
