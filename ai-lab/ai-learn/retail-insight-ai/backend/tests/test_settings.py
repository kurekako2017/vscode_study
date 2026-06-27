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
            "CORS_ORIGINS": '["http://localhost:5173"]',
        }
        with patch.dict(os.environ, environment, clear=False):
            settings = Settings(_env_file=None)

        self.assertEqual(settings.app_env, "test")
        self.assertEqual(settings.log_level, "WARNING")
        self.assertEqual(settings.cors_origins, ["http://localhost:5173"])

    def test_unknown_provider_is_rejected(self) -> None:
        with patch.dict(os.environ, {"RESEARCH_PROVIDER": "unknown"}, clear=False):
            with self.assertRaises(ValidationError):
                Settings(_env_file=None)


if __name__ == "__main__":
    unittest.main()
