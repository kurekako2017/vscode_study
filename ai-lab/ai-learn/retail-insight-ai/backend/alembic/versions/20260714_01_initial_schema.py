"""Initial ERIP schema migration.

Revision ID: 20260714_01_initial_schema
Revises: 
Create Date: 2026-07-14
"""

from __future__ import annotations

from pathlib import Path

from alembic import op

revision = "20260714_01_initial_schema"
down_revision = None
branch_labels = None
depends_on = None

_SCHEMA_PATH = Path(__file__).resolve().parents[2] / "db" / "schema.sql"


def upgrade() -> None:
    """把 `schema.sql` 作为初始基线执行，避免 migration 和手写 DDL 分叉。"""

    op.execute(_SCHEMA_PATH.read_text(encoding="utf-8"))


def downgrade() -> None:
    """按依赖反向删除所有业务表，回到空 schema。"""

    op.execute(
        """
        DROP TABLE IF EXISTS
            upload_idempotency_keys,
            upload_sessions,
            document_imports,
            document_chunks,
            documents,
            audit_logs,
            approval_events,
            approval_requests,
            report_versions,
            reports,
            events,
            tasks
        CASCADE
        """
    )
