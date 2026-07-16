"""Enhance PostgreSQL approval workflow, history and concurrency controls.

Revision ID: 20260717_04_enterprise_approval
Revises: 20260716_03_persistent_audit
Create Date: 2026-07-17
"""

from __future__ import annotations

from alembic import op

revision = "20260717_04_enterprise_approval"
down_revision = "20260716_03_persistent_audit"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """增量扩展 actor/history 字段，并增加审批并发的数据库最后防线。"""

    op.execute(
        "ALTER TABLE approval_requests "
        "ADD COLUMN IF NOT EXISTS requested_by_username TEXT NULL"
    )
    op.execute(
        "ALTER TABLE approval_requests "
        "ADD COLUMN IF NOT EXISTS requested_by_role TEXT NULL"
    )
    op.execute(
        "ALTER TABLE approval_requests "
        "ADD COLUMN IF NOT EXISTS approver_username TEXT NULL"
    )
    op.execute(
        "ALTER TABLE approval_requests "
        "ADD COLUMN IF NOT EXISTS approver_role TEXT NULL"
    )
    op.execute(
        "ALTER TABLE approval_events ADD COLUMN IF NOT EXISTS from_status TEXT NULL"
    )
    op.execute(
        "ALTER TABLE approval_events ADD COLUMN IF NOT EXISTS to_status TEXT NULL"
    )
    op.execute(
        "ALTER TABLE approval_events ADD COLUMN IF NOT EXISTS actor_username TEXT NULL"
    )
    op.execute(
        "ALTER TABLE approval_events ADD COLUMN IF NOT EXISTS actor_role TEXT NULL"
    )
    op.execute(
        """
        ALTER TABLE approval_events
        ADD COLUMN IF NOT EXISTS report_version_id TEXT NULL
        REFERENCES report_versions(id) ON DELETE RESTRICT
        """
    )
    op.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS ux_approval_requests_one_pending_per_task
        ON approval_requests (task_id)
        WHERE status = 'pending_approval'
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_approval_events_approval_created_id
        ON approval_events (approval_id, created_at ASC, id ASC)
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_approval_events_task_created_id
        ON approval_events (task_id, created_at ASC, id ASC)
        """
    )


def downgrade() -> None:
    """删除本轮兼容列和索引，不删除 Approval、History 或 ReportVersion 行。"""

    op.execute("DROP INDEX IF EXISTS idx_approval_events_task_created_id")
    op.execute("DROP INDEX IF EXISTS idx_approval_events_approval_created_id")
    op.execute("DROP INDEX IF EXISTS ux_approval_requests_one_pending_per_task")
    op.execute(
        "ALTER TABLE approval_events DROP COLUMN IF EXISTS report_version_id"
    )
    op.execute("ALTER TABLE approval_events DROP COLUMN IF EXISTS actor_role")
    op.execute("ALTER TABLE approval_events DROP COLUMN IF EXISTS actor_username")
    op.execute("ALTER TABLE approval_events DROP COLUMN IF EXISTS to_status")
    op.execute("ALTER TABLE approval_events DROP COLUMN IF EXISTS from_status")
    op.execute("ALTER TABLE approval_requests DROP COLUMN IF EXISTS approver_role")
    op.execute(
        "ALTER TABLE approval_requests DROP COLUMN IF EXISTS approver_username"
    )
    op.execute(
        "ALTER TABLE approval_requests DROP COLUMN IF EXISTS requested_by_role"
    )
    op.execute(
        "ALTER TABLE approval_requests DROP COLUMN IF EXISTS requested_by_username"
    )
