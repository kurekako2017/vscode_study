from __future__ import annotations

import unittest
import importlib.util
from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory
from app.embeddings.config import EMBEDDING_DIMENSIONS


class AlembicBaselineTest(unittest.TestCase):
    """验证 Alembic 框架存在，并且正式初始 migration 可以被加载。"""

    def test_empty_migration_baseline_is_loadable(self) -> None:
        backend_dir = Path(__file__).resolve().parents[1]
        config = Config(str(backend_dir / "alembic.ini"))

        script = ScriptDirectory.from_config(config)

        self.assertEqual(Path(script.dir).resolve(), (backend_dir / "alembic").resolve())
        self.assertEqual(
            [revision.revision for revision in script.walk_revisions()],
            [
                "20260717_04_enterprise_approval",
                "20260716_03_persistent_audit",
                "20260714_02_chunk_embeddings",
                "20260714_01_initial_schema",
            ],
        )
        self.assertTrue((backend_dir / "alembic" / "env.py").is_file())
        self.assertTrue((backend_dir / "db" / "schema.sql").is_file())

    def test_pgvector_revision_matches_application_dimension(self) -> None:
        """防止 migration 的 vector(N) 与运行时代码维度发生漂移。"""

        migration_path = (
            Path(__file__).resolve().parents[1]
            / "alembic"
            / "versions"
            / "20260714_02_add_document_chunk_embeddings.py"
        )
        spec = importlib.util.spec_from_file_location("erip_chunk_embedding_migration", migration_path)
        assert spec is not None and spec.loader is not None
        migration = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(migration)

        self.assertEqual(migration.EMBEDDING_DIMENSIONS, EMBEDDING_DIMENSIONS)
        source = migration_path.read_text(encoding="utf-8")
        self.assertIn("CREATE EXTENSION IF NOT EXISTS vector", source)
        self.assertIn("USING hnsw (embedding vector_cosine_ops)", source)
        self.assertIn("DROP COLUMN IF EXISTS embedding", source)
        self.assertNotIn("DROP EXTENSION", source)

    def test_initial_revision_uses_frozen_pre_vector_schema(self) -> None:
        """历史基线必须固定，pgvector 只能由后续 revision 引入。"""

        backend_dir = Path(__file__).resolve().parents[1]
        initial_path = backend_dir / "alembic" / "versions" / "20260714_01_initial_schema.py"
        frozen_schema_path = backend_dir / "alembic" / "sql" / "20260714_01_initial_schema.sql"
        initial_source = initial_path.read_text(encoding="utf-8")
        frozen_schema = frozen_schema_path.read_text(encoding="utf-8").lower()

        self.assertIn('"sql" / "20260714_01_initial_schema.sql"', initial_source)
        self.assertNotIn('"db" / "schema.sql"', initial_source)
        self.assertNotIn("create extension", frozen_schema)
        self.assertNotIn("embedding vector", frozen_schema)
        self.assertNotIn("using hnsw", frozen_schema)

    def test_persistent_audit_revision_is_backward_compatible(self) -> None:
        """审计 migration 必须增量升级旧表，并保留 append-only 历史。"""

        migration_path = (
            Path(__file__).resolve().parents[1]
            / "alembic"
            / "versions"
            / "20260716_03_persistent_audit.py"
        )
        source = migration_path.read_text(encoding="utf-8").lower()

        self.assertIn("add column if not exists actor_username", source)
        self.assertIn("update audit_logs set result = 'failure'", source)
        self.assertIn("created_at desc, id desc", source)
        self.assertNotIn("delete from audit_logs", source)
        self.assertNotIn("drop table audit_logs", source)

    def test_database_url_is_not_persisted_in_alembic_ini(self) -> None:
        backend_dir = Path(__file__).resolve().parents[1]
        config = Config(str(backend_dir / "alembic.ini"))

        self.assertEqual(config.get_main_option("sqlalchemy.url"), "")


if __name__ == "__main__":
    unittest.main()
