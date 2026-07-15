from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from pydantic import ValidationError

from app.config.settings import Settings


class SettingsTest(unittest.TestCase):
    """验证环境变量解析和非法部署配置的快速失败行为。"""

    def test_environment_values_are_parsed(self) -> None:
        environment = {
            "APP_ENV": "test",
            "LOG_LEVEL": "WARNING",
            "RESEARCH_PROVIDER": "static",
            "DATA_PROVIDER": "static",
            "REPOSITORY_BACKEND": "inmemory",
            "CORS_ORIGINS": '["http://localhost:5173"]',
        }
        with patch.dict(os.environ, environment, clear=True):
            settings = Settings(_env_file=None)

        self.assertEqual(settings.app_env, "test")
        self.assertEqual(settings.log_level, "WARNING")
        self.assertEqual(settings.repository_backend, "inmemory")
        self.assertIsNone(settings.database_url)
        self.assertEqual(settings.cors_origins, ["http://localhost:5173"])

    def test_database_url_is_read_for_explicit_postgres_mode(self) -> None:
        with patch.dict(
            os.environ,
            {
                "REPOSITORY_BACKEND": "postgres",
                "DATABASE_URL": "postgresql+psycopg://user:secret@localhost:5432/example",
            },
            clear=True,
        ):
            settings = Settings(_env_file=None)

        self.assertEqual(settings.repository_backend, "postgres")
        self.assertTrue(settings.database_url.startswith("postgresql+psycopg://"))

    def test_unknown_provider_is_rejected(self) -> None:
        with patch.dict(os.environ, {"RESEARCH_PROVIDER": "unknown"}, clear=True):
            with self.assertRaises(ValidationError):
                Settings(_env_file=None)

    def test_jwt_defaults_to_30_minutes_and_secret_is_masked(self) -> None:
        settings = Settings(_env_file=None)

        self.assertEqual(settings.jwt_algorithm, "HS256")
        self.assertEqual(settings.jwt_access_token_expire_minutes, 30)
        self.assertEqual(str(settings.jwt_secret_key), "**********")

    def test_production_rejects_local_default_jwt_secret(self) -> None:
        with self.assertRaises(ValidationError):
            Settings(app_env="production", _env_file=None)


if __name__ == "__main__":
    unittest.main()
