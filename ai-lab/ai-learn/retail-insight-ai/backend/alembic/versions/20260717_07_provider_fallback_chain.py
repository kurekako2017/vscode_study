"""Add provider attempt ledger, circuit state, and fallback summary columns.

Revision ID: 20260717_07_fallback_chain
Revises: 20260717_06_dual_route_llm
Create Date: 2026-07-17

注意：alembic_version.version_num 为 VARCHAR(32)，revision id 必须 ≤32。
原候选名 provider_fallback_chain 超长，已缩短为 fallback_chain。
"""

from alembic import op

revision = "20260717_07_fallback_chain"
down_revision = "20260717_06_dual_route_llm"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    ALTER TABLE llm_usage_ledger
      ADD COLUMN IF NOT EXISTS fallback_used BOOLEAN NOT NULL DEFAULT FALSE,
      ADD COLUMN IF NOT EXISTS attempt_count INTEGER NOT NULL DEFAULT 0
    """)
    op.execute("""
    DO $$
    BEGIN
      IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'llm_usage_ledger_attempt_count_check'
      ) THEN
        ALTER TABLE llm_usage_ledger
          ADD CONSTRAINT llm_usage_ledger_attempt_count_check CHECK (attempt_count >= 0);
      END IF;
    END $$;
    """)

    op.execute("""
    CREATE TABLE IF NOT EXISTS llm_provider_attempts (
      attempt_id TEXT PRIMARY KEY,
      usage_id TEXT NOT NULL REFERENCES llm_usage_ledger(usage_id) ON DELETE RESTRICT,
      request_id TEXT NOT NULL,
      idempotency_key TEXT NOT NULL,
      attempt_number INTEGER NOT NULL CHECK (attempt_number >= 1),
      operation TEXT NOT NULL CHECK (operation IN ('ai_analysis', 'executive_report')),
      route_tier TEXT NOT NULL CHECK (route_tier IN ('low_cost', 'high_quality')),
      provider_name TEXT NOT NULL,
      configured_model TEXT NOT NULL,
      actual_model TEXT NULL,
      status TEXT NOT NULL CHECK (status IN (
        'started','succeeded','failed','timed_out','rate_limited',
        'unavailable','configuration_error','cancelled','skipped_circuit_open'
      )),
      started_at TIMESTAMPTZ NULL,
      completed_at TIMESTAMPTZ NULL,
      timeout_seconds DOUBLE PRECISION NULL,
      latency_ms INTEGER NULL CHECK (latency_ms IS NULL OR latency_ms >= 0),
      input_tokens INTEGER NOT NULL DEFAULT 0 CHECK (input_tokens >= 0),
      output_tokens INTEGER NOT NULL DEFAULT 0 CHECK (output_tokens >= 0),
      total_tokens INTEGER NOT NULL DEFAULT 0 CHECK (total_tokens >= 0),
      usage_source TEXT NULL,
      input_unit_price NUMERIC(20,8) NOT NULL DEFAULT 0,
      output_unit_price NUMERIC(20,8) NOT NULL DEFAULT 0,
      estimated_cost NUMERIC(20,8) NOT NULL DEFAULT 0 CHECK (estimated_cost >= 0),
      actual_cost NUMERIC(20,8) NOT NULL DEFAULT 0 CHECK (actual_cost >= 0),
      currency CHAR(3) NOT NULL DEFAULT 'USD',
      provider_request_id TEXT NULL,
      error_category TEXT NULL,
      error_code TEXT NULL,
      fallback_reason TEXT NULL,
      response_received BOOLEAN NOT NULL DEFAULT FALSE,
      charge_possible BOOLEAN NOT NULL DEFAULT FALSE,
      model_mismatch BOOLEAN NOT NULL DEFAULT FALSE,
      created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    """)
    op.execute("""
    CREATE INDEX IF NOT EXISTS idx_llm_provider_attempts_usage
      ON llm_provider_attempts (usage_id, attempt_number)
    """)
    op.execute("""
    CREATE INDEX IF NOT EXISTS idx_llm_provider_attempts_request
      ON llm_provider_attempts (request_id)
    """)
    op.execute("""
    CREATE INDEX IF NOT EXISTS idx_llm_provider_attempts_provider
      ON llm_provider_attempts (provider_name, created_at DESC)
    """)

    op.execute("""
    CREATE TABLE IF NOT EXISTS llm_provider_circuit_state (
      provider_name TEXT PRIMARY KEY,
      state TEXT NOT NULL CHECK (state IN ('closed','open','half_open')),
      failure_count INTEGER NOT NULL DEFAULT 0 CHECK (failure_count >= 0),
      opened_at TIMESTAMPTZ NULL,
      half_open_probes INTEGER NOT NULL DEFAULT 0 CHECK (half_open_probes >= 0),
      updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS llm_provider_attempts")
    op.execute("DROP TABLE IF EXISTS llm_provider_circuit_state")
    op.execute("""
    ALTER TABLE llm_usage_ledger
      DROP CONSTRAINT IF EXISTS llm_usage_ledger_attempt_count_check
    """)
    op.execute("""
    ALTER TABLE llm_usage_ledger
      DROP COLUMN IF EXISTS fallback_used,
      DROP COLUMN IF EXISTS attempt_count
    """)
