"""Add dual-route LLM cost governance fields and per-tier quota buckets.

Revision ID: 20260717_06_dual_route_llm
Revises: 20260717_05_llm_cost_governance
Create Date: 2026-07-17
"""

from alembic import op

revision = "20260717_06_dual_route_llm"
down_revision = "20260717_05_llm_cost_governance"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """补齐 route_tier/policy snapshot/report 关联，并按 tier 拆分额度桶。"""

    op.execute("""
    ALTER TABLE llm_usage_ledger
      ADD COLUMN IF NOT EXISTS route_tier TEXT,
      ADD COLUMN IF NOT EXISTS selected_provider TEXT,
      ADD COLUMN IF NOT EXISTS selected_model TEXT,
      ADD COLUMN IF NOT EXISTS policy_snapshot JSONB NOT NULL DEFAULT '{}'::jsonb,
      ADD COLUMN IF NOT EXISTS token_limit_snapshot JSONB NOT NULL DEFAULT '{}'::jsonb,
      ADD COLUMN IF NOT EXISTS price_snapshot JSONB NOT NULL DEFAULT '{}'::jsonb,
      ADD COLUMN IF NOT EXISTS report_id TEXT,
      ADD COLUMN IF NOT EXISTS report_version_id TEXT,
      ADD COLUMN IF NOT EXISTS ai_analysis_id TEXT
    """)
    op.execute("""
    UPDATE llm_usage_ledger
    SET operation = CASE
          WHEN operation IN ('ai.analysis', 'ai_analysis') THEN 'ai_analysis'
          ELSE operation
        END,
        route_tier = COALESCE(route_tier, 'low_cost'),
        selected_provider = COALESCE(selected_provider, provider_name),
        selected_model = COALESCE(selected_model, model_name),
        ai_analysis_id = COALESCE(ai_analysis_id, analysis_id),
        policy_snapshot = CASE
          WHEN policy_snapshot = '{}'::jsonb THEN jsonb_build_object(
            'operation', 'ai_analysis',
            'route_tier', 'low_cost',
            'migrated_from', '20260717_05_llm_cost_governance'
          )
          ELSE policy_snapshot
        END,
        token_limit_snapshot = CASE
          WHEN token_limit_snapshot = '{}'::jsonb THEN jsonb_build_object(
            'reserved_input_tokens', reserved_input_tokens,
            'reserved_output_tokens', reserved_output_tokens
          )
          ELSE token_limit_snapshot
        END,
        price_snapshot = CASE
          WHEN price_snapshot = '{}'::jsonb THEN jsonb_build_object(
            'input_price_per_million', input_price_per_million::text,
            'output_price_per_million', output_price_per_million::text,
            'currency', currency
          )
          ELSE price_snapshot
        END
    """)
    op.execute("""
    ALTER TABLE llm_usage_ledger
      ALTER COLUMN route_tier SET DEFAULT 'low_cost',
      ALTER COLUMN route_tier SET NOT NULL
    """)
    op.execute("""
    ALTER TABLE llm_usage_ledger
      DROP CONSTRAINT IF EXISTS llm_usage_ledger_route_tier_check
    """)
    op.execute("""
    ALTER TABLE llm_usage_ledger
      ADD CONSTRAINT llm_usage_ledger_route_tier_check
      CHECK (route_tier IN ('low_cost', 'high_quality'))
    """)
    op.execute("""
    ALTER TABLE llm_usage_ledger
      DROP CONSTRAINT IF EXISTS llm_usage_ledger_operation_check
    """)
    op.execute("""
    ALTER TABLE llm_usage_ledger
      ADD CONSTRAINT llm_usage_ledger_operation_check
      CHECK (operation IN ('ai_analysis', 'executive_report'))
    """)

    # 按 route_tier 重建额度桶：旧桶视为 low_cost。
    op.execute("""
    CREATE TABLE IF NOT EXISTS llm_quota_buckets_v2 (
      bucket_date DATE NOT NULL,
      scope_type TEXT NOT NULL CHECK (scope_type IN ('user','global')),
      scope_id TEXT NOT NULL,
      route_tier TEXT NOT NULL CHECK (route_tier IN ('low_cost','high_quality')),
      request_count BIGINT NOT NULL DEFAULT 0 CHECK (request_count >= 0),
      token_count BIGINT NOT NULL DEFAULT 0 CHECK (token_count >= 0),
      cost NUMERIC(20,8) NOT NULL DEFAULT 0 CHECK (cost >= 0),
      updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (bucket_date, scope_type, scope_id, route_tier)
    )
    """)
    op.execute("""
    INSERT INTO llm_quota_buckets_v2 (
      bucket_date, scope_type, scope_id, route_tier, request_count, token_count, cost, updated_at
    )
    SELECT bucket_date, scope_type, scope_id, 'low_cost', request_count, token_count, cost, updated_at
    FROM llm_quota_buckets
    ON CONFLICT DO NOTHING
    """)
    op.execute("DROP TABLE IF EXISTS llm_quota_buckets")
    op.execute("ALTER TABLE llm_quota_buckets_v2 RENAME TO llm_quota_buckets")
    op.execute("CREATE INDEX IF NOT EXISTS idx_llm_usage_route_tier_occurred ON llm_usage_ledger (route_tier, occurred_at DESC)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_llm_usage_operation_occurred ON llm_usage_ledger (operation, occurred_at DESC)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_llm_usage_analysis_id ON llm_usage_ledger (ai_analysis_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_llm_usage_report_id ON llm_usage_ledger (report_id)")


def downgrade() -> None:
    """回滚双路由字段；额度桶合并回旧主键（仅 low_cost）。"""

    op.execute("DROP INDEX IF EXISTS idx_llm_usage_report_id")
    op.execute("DROP INDEX IF EXISTS idx_llm_usage_analysis_id")
    op.execute("DROP INDEX IF EXISTS idx_llm_usage_operation_occurred")
    op.execute("DROP INDEX IF EXISTS idx_llm_usage_route_tier_occurred")
    op.execute("""
    CREATE TABLE IF NOT EXISTS llm_quota_buckets_legacy (
      bucket_date DATE NOT NULL,
      scope_type TEXT NOT NULL CHECK (scope_type IN ('user','global')),
      scope_id TEXT NOT NULL,
      request_count BIGINT NOT NULL DEFAULT 0 CHECK (request_count >= 0),
      token_count BIGINT NOT NULL DEFAULT 0 CHECK (token_count >= 0),
      cost NUMERIC(20,8) NOT NULL DEFAULT 0 CHECK (cost >= 0),
      updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (bucket_date, scope_type, scope_id)
    )
    """)
    op.execute("""
    INSERT INTO llm_quota_buckets_legacy (
      bucket_date, scope_type, scope_id, request_count, token_count, cost, updated_at
    )
    SELECT bucket_date, scope_type, scope_id,
           SUM(request_count), SUM(token_count), SUM(cost), MAX(updated_at)
    FROM llm_quota_buckets
    GROUP BY bucket_date, scope_type, scope_id
    ON CONFLICT DO NOTHING
    """)
    op.execute("DROP TABLE IF EXISTS llm_quota_buckets")
    op.execute("ALTER TABLE llm_quota_buckets_legacy RENAME TO llm_quota_buckets")
    op.execute("ALTER TABLE llm_usage_ledger DROP CONSTRAINT IF EXISTS llm_usage_ledger_operation_check")
    op.execute("ALTER TABLE llm_usage_ledger DROP CONSTRAINT IF EXISTS llm_usage_ledger_route_tier_check")
    op.execute("""
    ALTER TABLE llm_usage_ledger
      DROP COLUMN IF EXISTS route_tier,
      DROP COLUMN IF EXISTS selected_provider,
      DROP COLUMN IF EXISTS selected_model,
      DROP COLUMN IF EXISTS policy_snapshot,
      DROP COLUMN IF EXISTS token_limit_snapshot,
      DROP COLUMN IF EXISTS price_snapshot,
      DROP COLUMN IF EXISTS report_id,
      DROP COLUMN IF EXISTS report_version_id,
      DROP COLUMN IF EXISTS ai_analysis_id
    """)
