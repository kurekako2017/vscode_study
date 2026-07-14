from __future__ import annotations

import unittest
from contextlib import contextmanager
from unittest.mock import patch

from app.config.settings import Settings

from tests.postgres_test_utils import ALLOWED_TEST_DATABASE, reset_postgres_state_if_needed


class _FakeCursor:
    def __init__(self, current_database: str) -> None:
        self.current_database = current_database
        self.executed: list[str] = []

    def execute(self, sql: str, params=None) -> None:  # noqa: ANN001 - 仿真数据库游标签名
        self.executed.append(sql)

    def fetchone(self):
        return (self.current_database,)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None


class _FakeConnection:
    def __init__(self, current_database: str) -> None:
        self.cursor_obj = _FakeCursor(current_database)

    def cursor(self) -> _FakeCursor:
        return self.cursor_obj


class _FakePostgresConnectionFactory:
    def __init__(self, current_database: str) -> None:
        self.connection_obj = _FakeConnection(current_database)

    @contextmanager
    def connection(self):
        yield self.connection_obj


class PostgresTestUtilsTest(unittest.TestCase):
    """验证 PostgreSQL 测试清理只允许作用于专用测试库。"""

    def test_allows_cleaning_only_for_dedicated_test_database(self) -> None:
        settings = Settings(
            repository_backend="postgres",
            database_url="postgresql:///erip_integration_test",
        )
        fake_factory = _FakePostgresConnectionFactory(ALLOWED_TEST_DATABASE)

        with patch("tests.postgres_test_utils.PostgresConnectionFactory", return_value=fake_factory):
            reset_postgres_state_if_needed(settings)

        executed = fake_factory.connection_obj.cursor_obj.executed
        self.assertIn("SELECT current_database()", executed)
        self.assertTrue(any(sql.startswith("TRUNCATE ") for sql in executed))

    def test_rejects_non_test_database_before_truncate(self) -> None:
        settings = Settings(
            repository_backend="postgres",
            database_url="postgresql:///some_other_database",
        )
        fake_factory = _FakePostgresConnectionFactory("some_other_database")

        with patch("tests.postgres_test_utils.PostgresConnectionFactory", return_value=fake_factory):
            with self.assertRaisesRegex(
                RuntimeError,
                "Refusing to truncate PostgreSQL state outside the dedicated test database",
            ) as error:
                reset_postgres_state_if_needed(settings)

        message = str(error.exception)
        self.assertIn("some_other_database", message)
        self.assertIn(ALLOWED_TEST_DATABASE, message)
        executed = fake_factory.connection_obj.cursor_obj.executed
        self.assertEqual(executed, ["SELECT current_database()"])


if __name__ == "__main__":
    unittest.main()
