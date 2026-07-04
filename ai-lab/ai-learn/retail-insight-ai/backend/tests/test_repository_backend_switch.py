from __future__ import annotations

import unittest
from unittest.mock import patch

from app.config.container import build_container
from app.config.settings import Settings
from app.repositories.implementations.in_memory.event_repository import InMemoryEventRepository
from app.repositories.postgres.event_repository import PostgresEventRepository


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
        with patch(
            "app.config.container.PostgresConnectionFactory.initialize_schema"
        ) as initialize_schema:
            container = build_container(
                Settings(
                    repository_backend="postgres",
                    workflow_step_delay_seconds=0,
                    log_level="CRITICAL",
                )
            )

        initialize_schema.assert_called_once()
        self.assertEqual(container.repository_backend, "postgres")
        self.assertIsInstance(container.event_repository, PostgresEventRepository)


if __name__ == "__main__":
    unittest.main()
