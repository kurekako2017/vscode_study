from __future__ import annotations

import unittest
from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory


class AlembicBaselineTest(unittest.TestCase):
    """验证 Alembic 框架存在且 versions 为空；测试不会连接或升级数据库。"""

    def test_empty_migration_baseline_is_loadable(self) -> None:
        backend_dir = Path(__file__).resolve().parents[1]
        config = Config(str(backend_dir / "alembic.ini"))

        script = ScriptDirectory.from_config(config)

        self.assertEqual(Path(script.dir).resolve(), (backend_dir / "alembic").resolve())
        self.assertEqual(list(script.walk_revisions()), [])
        self.assertTrue((backend_dir / "alembic" / "env.py").is_file())
        self.assertTrue((backend_dir / "db" / "schema.sql").is_file())

    def test_database_url_is_not_persisted_in_alembic_ini(self) -> None:
        backend_dir = Path(__file__).resolve().parents[1]
        config = Config(str(backend_dir / "alembic.ini"))

        self.assertEqual(config.get_main_option("sqlalchemy.url"), "")


if __name__ == "__main__":
    unittest.main()
