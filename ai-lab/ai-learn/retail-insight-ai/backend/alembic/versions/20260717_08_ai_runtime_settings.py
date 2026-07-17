"""Add PostgreSQL-backed AI runtime settings singleton.

Revision ID: 20260717_08_ai_runtime
Revises: 20260717_07_fallback_chain
Create Date: 2026-07-17

表 ai_runtime_settings 只持久化 mode / kill_switch / version / actor。
API Key、Base URL、价格仍只来自环境变量，禁止写入数据库。
"""

from alembic import op

revision = "20260717_08_ai_runtime"
down_revision = "20260717_07_fallback_chain"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS ai_runtime_settings (
          setting_key TEXT PRIMARY KEY,
          mode TEXT NOT NULL
            CHECK (mode IN ('stub', 'openrouter', 'fallback_chain')),
          real_calls_enabled BOOLEAN NOT NULL DEFAULT FALSE,
          kill_switch BOOLEAN NOT NULL DEFAULT FALSE,
          version INTEGER NOT NULL DEFAULT 1 CHECK (version >= 1),
          updated_by_user_id TEXT NULL,
          updated_by_username TEXT NULL,
          updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_ai_runtime_settings_updated
          ON ai_runtime_settings (updated_at DESC)
        """
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_ai_runtime_settings_updated")
    op.execute("DROP TABLE IF EXISTS ai_runtime_settings")
