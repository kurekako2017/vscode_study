"""Add PostgreSQL-only LLM ledger, quota buckets and analysis results.

Revision ID: 20260717_05_llm_cost_governance
Revises: 20260717_04_enterprise_approval
Create Date: 2026-07-17
"""

from alembic import op

revision = "20260717_05_llm_cost_governance"
down_revision = "20260717_04_enterprise_approval"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """只新增成本治理事实，不改动旧业务数据。"""
    op.execute("""
    CREATE TABLE IF NOT EXISTS llm_usage_ledger (
      usage_id TEXT PRIMARY KEY, occurred_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
      request_id TEXT NOT NULL, idempotency_key TEXT NOT NULL, actor_user_id TEXT NOT NULL,
      actor_username TEXT NOT NULL, actor_role TEXT NOT NULL, provider_name TEXT NOT NULL,
      model_name TEXT NOT NULL, operation TEXT NOT NULL,
      status TEXT NOT NULL CHECK (status IN ('reserved','succeeded','failed','rejected')),
      reserved_input_tokens INTEGER NOT NULL CHECK (reserved_input_tokens >= 0),
      reserved_output_tokens INTEGER NOT NULL CHECK (reserved_output_tokens >= 0),
      input_tokens INTEGER NOT NULL DEFAULT 0 CHECK (input_tokens >= 0),
      output_tokens INTEGER NOT NULL DEFAULT 0 CHECK (output_tokens >= 0),
      total_tokens INTEGER NOT NULL DEFAULT 0 CHECK (total_tokens >= 0),
      input_price_per_million NUMERIC(20,8) NOT NULL,
      output_price_per_million NUMERIC(20,8) NOT NULL,
      estimated_cost NUMERIC(20,8) NOT NULL CHECK (estimated_cost >= 0),
      actual_cost NUMERIC(20,8) NOT NULL DEFAULT 0 CHECK (actual_cost >= 0),
      currency CHAR(3) NOT NULL, latency_ms INTEGER NULL CHECK (latency_ms IS NULL OR latency_ms >= 0),
      provider_request_id TEXT NULL, finish_reason TEXT NULL, error_code TEXT NULL,
      task_id TEXT NULL, document_ids JSONB NOT NULL DEFAULT '[]'::jsonb,
      evidence_refs JSONB NOT NULL DEFAULT '[]'::jsonb, analysis_id TEXT NULL,
      completed_at TIMESTAMPTZ NULL, UNIQUE (actor_user_id, idempotency_key))
    """)
    op.execute("""
    CREATE TABLE IF NOT EXISTS llm_quota_buckets (
      bucket_date DATE NOT NULL, scope_type TEXT NOT NULL CHECK (scope_type IN ('user','global')),
      scope_id TEXT NOT NULL, request_count BIGINT NOT NULL DEFAULT 0 CHECK (request_count >= 0),
      token_count BIGINT NOT NULL DEFAULT 0 CHECK (token_count >= 0),
      cost NUMERIC(20,8) NOT NULL DEFAULT 0 CHECK (cost >= 0),
      updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (bucket_date, scope_type, scope_id))
    """)
    op.execute("""
    CREATE TABLE IF NOT EXISTS ai_analysis_results (
      analysis_id TEXT PRIMARY KEY,
      usage_id TEXT NOT NULL UNIQUE REFERENCES llm_usage_ledger(usage_id) ON DELETE RESTRICT,
      answer TEXT NOT NULL, citations JSONB NOT NULL, provider_name TEXT NOT NULL,
      model_name TEXT NOT NULL, input_tokens INTEGER NOT NULL, output_tokens INTEGER NOT NULL,
      total_tokens INTEGER NOT NULL, actual_cost NUMERIC(20,8) NOT NULL, currency CHAR(3) NOT NULL,
      status TEXT NOT NULL CHECK (status = 'succeeded'), created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP)
    """)
    op.execute("CREATE INDEX IF NOT EXISTS idx_llm_usage_actor_occurred ON llm_usage_ledger (actor_user_id, occurred_at DESC)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_llm_usage_status_occurred ON llm_usage_ledger (status, occurred_at DESC)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_llm_usage_request_id ON llm_usage_ledger (request_id)")


def downgrade() -> None:
    """回滚只删除本 revision 新增的表与索引。"""
    op.execute("DROP TABLE IF EXISTS ai_analysis_results")
    op.execute("DROP TABLE IF EXISTS llm_quota_buckets")
    op.execute("DROP TABLE IF EXISTS llm_usage_ledger")
