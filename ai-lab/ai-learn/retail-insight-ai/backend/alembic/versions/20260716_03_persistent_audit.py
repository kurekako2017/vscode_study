"""Enhance PostgreSQL audit logs for persistent enterprise audit.

Revision ID: 20260716_03_persistent_audit
Revises: 20260714_02_chunk_embeddings
Create Date: 2026-07-16
"""

from __future__ import annotations

from alembic import op

revision = "20260716_03_persistent_audit"
down_revision = "20260714_02_chunk_embeddings"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """只增列并兼容旧结果值，不删除或重写既有审计事实。"""

    op.execute("ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS actor_username TEXT NULL")
    op.execute("ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS actor_role TEXT NULL")
    op.execute("ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS permission TEXT NULL")
    op.execute("ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS http_method TEXT NULL")
    op.execute("ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS api_path TEXT NULL")
    op.execute("ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS status_code INTEGER NULL")
    op.execute("UPDATE audit_logs SET result = 'failure' WHERE result = 'failed'")
    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'audit_logs_result_check'
                  AND conrelid = 'audit_logs'::regclass
            ) THEN
                ALTER TABLE audit_logs
                ADD CONSTRAINT audit_logs_result_check
                CHECK (result IN ('success', 'failure', 'denied'));
            END IF;
        END
        $$;
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_audit_logs_created_id_desc
        ON audit_logs (created_at DESC, id DESC)
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_audit_logs_actor_created
        ON audit_logs (actor_id, created_at DESC, id DESC)
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_audit_logs_action_created
        ON audit_logs (operation_type, created_at DESC, id DESC)
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_audit_logs_request_id
        ON audit_logs (request_id)
        """
    )


def downgrade() -> None:
    """回退新增查询列与索引；Audit 行本身仍保留。"""

    op.execute("DROP INDEX IF EXISTS idx_audit_logs_request_id")
    op.execute("DROP INDEX IF EXISTS idx_audit_logs_action_created")
    op.execute("DROP INDEX IF EXISTS idx_audit_logs_actor_created")
    op.execute("DROP INDEX IF EXISTS idx_audit_logs_created_id_desc")
    op.execute("ALTER TABLE audit_logs DROP CONSTRAINT IF EXISTS audit_logs_result_check")
    op.execute("UPDATE audit_logs SET result = 'failed' WHERE result = 'failure'")
    op.execute("ALTER TABLE audit_logs DROP COLUMN IF EXISTS status_code")
    op.execute("ALTER TABLE audit_logs DROP COLUMN IF EXISTS api_path")
    op.execute("ALTER TABLE audit_logs DROP COLUMN IF EXISTS http_method")
    op.execute("ALTER TABLE audit_logs DROP COLUMN IF EXISTS permission")
    op.execute("ALTER TABLE audit_logs DROP COLUMN IF EXISTS actor_role")
    op.execute("ALTER TABLE audit_logs DROP COLUMN IF EXISTS actor_username")
