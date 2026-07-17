-- ERIP PostgreSQL 完整持久化 Schema。
-- 所有时间字段使用 TIMESTAMPTZ；可扩展元数据使用 JSONB；事实表通过唯一约束防止重复写入。

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS tasks (
    task_id TEXT PRIMARY KEY,
    question TEXT NOT NULL,
    mode TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('queued', 'running', 'completed', 'failed')),
    error TEXT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 通用事件流不依赖 Task 外键。stream_id 可以是 task/upload/document/import/retrieval/RAG scope。
CREATE TABLE IF NOT EXISTS events (
    id BIGSERIAL PRIMARY KEY,
    stream_id TEXT NOT NULL,
    sequence INTEGER NOT NULL CHECK (sequence > 0),
    event_type TEXT NOT NULL,
    message TEXT NOT NULL,
    data_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (stream_id, sequence)
);

CREATE TABLE IF NOT EXISTS reports (
    task_id TEXT PRIMARY KEY REFERENCES tasks(task_id) ON DELETE CASCADE,
    markdown TEXT NOT NULL,
    provider TEXT NOT NULL,
    approval_status TEXT NOT NULL DEFAULT 'generated' CHECK (
        approval_status IN (
            'generated', 'draft', 'pending_approval', 'approved', 'rejected',
            'revised', 'published', 'archived'
        )
    ),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- report_versions 只由 ApprovalRepository 写入，是报告版本事实的唯一来源。
CREATE TABLE IF NOT EXISTS report_versions (
    id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL REFERENCES tasks(task_id) ON DELETE CASCADE,
    version_no INTEGER NOT NULL CHECK (version_no > 0),
    markdown TEXT NOT NULL,
    status TEXT NOT NULL,
    revision_reason TEXT NULL,
    revised_from_version_id TEXT NULL REFERENCES report_versions(id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT NULL,
    UNIQUE (task_id, version_no)
);

CREATE TABLE IF NOT EXISTS approval_requests (
    id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL REFERENCES tasks(task_id) ON DELETE CASCADE,
    report_version_id TEXT NOT NULL REFERENCES report_versions(id) ON DELETE RESTRICT,
    status TEXT NOT NULL,
    requested_by TEXT NULL,
    requested_by_username TEXT NULL,
    requested_by_role TEXT NULL,
    requested_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    approver_id TEXT NULL,
    approver_username TEXT NULL,
    approver_role TEXT NULL,
    decision_at TIMESTAMPTZ NULL,
    decision_reason TEXT NULL,
    revision_no INTEGER NOT NULL DEFAULT 1 CHECK (revision_no > 0),
    revised_from_version_id TEXT NULL REFERENCES report_versions(id) ON DELETE RESTRICT,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS approval_events (
    id TEXT PRIMARY KEY,
    approval_id TEXT NOT NULL REFERENCES approval_requests(id) ON DELETE CASCADE,
    task_id TEXT NOT NULL REFERENCES tasks(task_id) ON DELETE CASCADE,
    event_type TEXT NOT NULL,
    actor_id TEXT NULL,
    reason TEXT NULL,
    from_status TEXT NULL,
    to_status TEXT NULL,
    actor_username TEXT NULL,
    actor_role TEXT NULL,
    report_version_id TEXT NULL REFERENCES report_versions(id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 兼容旧 Approval 表：只增列，不覆盖既有审批、版本和历史事实。
ALTER TABLE approval_requests ADD COLUMN IF NOT EXISTS requested_by_username TEXT NULL;
ALTER TABLE approval_requests ADD COLUMN IF NOT EXISTS requested_by_role TEXT NULL;
ALTER TABLE approval_requests ADD COLUMN IF NOT EXISTS approver_username TEXT NULL;
ALTER TABLE approval_requests ADD COLUMN IF NOT EXISTS approver_role TEXT NULL;
ALTER TABLE approval_events ADD COLUMN IF NOT EXISTS from_status TEXT NULL;
ALTER TABLE approval_events ADD COLUMN IF NOT EXISTS to_status TEXT NULL;
ALTER TABLE approval_events ADD COLUMN IF NOT EXISTS actor_username TEXT NULL;
ALTER TABLE approval_events ADD COLUMN IF NOT EXISTS actor_role TEXT NULL;
ALTER TABLE approval_events ADD COLUMN IF NOT EXISTS report_version_id TEXT NULL
    REFERENCES report_versions(id) ON DELETE RESTRICT;

CREATE TABLE IF NOT EXISTS audit_logs (
    id TEXT PRIMARY KEY,
    operation_type TEXT NOT NULL,
    actor_id TEXT NULL,
    actor_username TEXT NULL,
    actor_role TEXT NULL,
    organization_id TEXT NULL,
    department_id TEXT NULL,
    resource_type TEXT NOT NULL,
    resource_id TEXT NOT NULL,
    result TEXT NOT NULL CONSTRAINT audit_logs_result_check
        CHECK (result IN ('success', 'failure', 'denied')),
    permission TEXT NULL,
    http_method TEXT NULL,
    api_path TEXT NULL,
    status_code INTEGER NULL,
    request_id TEXT NOT NULL,
    trace_id TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    error_code TEXT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 兼容已经由旧 schema 创建的 audit_logs：只增列、回填结果，不删除历史数据。
ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS actor_username TEXT NULL;
ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS actor_role TEXT NULL;
ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS permission TEXT NULL;
ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS http_method TEXT NULL;
ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS api_path TEXT NULL;
ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS status_code INTEGER NULL;
UPDATE audit_logs SET result = 'failure' WHERE result = 'failed';
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

CREATE TABLE IF NOT EXISTS documents (
    document_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NULL,
    owner TEXT NOT NULL,
    version INTEGER NOT NULL CHECK (version > 0),
    language TEXT NOT NULL,
    document_type TEXT NOT NULL,
    status TEXT NOT NULL,
    tags JSONB NOT NULL DEFAULT '[]'::jsonb,
    source JSONB NOT NULL,
    checksum TEXT NOT NULL UNIQUE,
    content TEXT NOT NULL,
    approval_status TEXT NOT NULL,
    metadata_created_at TIMESTAMPTZ NOT NULL,
    metadata_updated_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS document_chunks (
    chunk_id TEXT PRIMARY KEY,
    document_id TEXT NOT NULL REFERENCES documents(document_id) ON DELETE CASCADE,
    version INTEGER NOT NULL CHECK (version > 0),
    chunk_index INTEGER NOT NULL CHECK (chunk_index >= 0),
    content TEXT NOT NULL,
    character_count INTEGER NOT NULL CHECK (character_count >= 0),
    metadata JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    embedding vector(384) NULL,
    UNIQUE (document_id, version, chunk_index)
);

CREATE TABLE IF NOT EXISTS document_imports (
    import_id TEXT PRIMARY KEY,
    document_id TEXT NOT NULL REFERENCES documents(document_id) ON DELETE CASCADE,
    status TEXT NOT NULL CHECK (status IN ('pending', 'running', 'completed', 'failed')),
    error_code TEXT NULL,
    error_message TEXT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    UNIQUE (document_id)
);

CREATE TABLE IF NOT EXISTS upload_sessions (
    upload_id TEXT PRIMARY KEY,
    document_id TEXT NOT NULL REFERENCES documents(document_id) ON DELETE CASCADE,
    checksum TEXT NOT NULL UNIQUE,
    idempotency_key TEXT NULL UNIQUE,
    status TEXT NOT NULL,
    progress INTEGER NOT NULL CHECK (progress BETWEEN 0 AND 100),
    error_code TEXT NULL,
    error_message TEXT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS upload_idempotency_keys (
    idempotency_key TEXT PRIMARY KEY,
    upload_id TEXT NOT NULL REFERENCES upload_sessions(upload_id) ON DELETE CASCADE,
    checksum TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- LLM 成本事实只在 PostgreSQL 企业模式使用；普通 API 不提供更新或删除入口。
CREATE TABLE IF NOT EXISTS llm_usage_ledger (
    usage_id TEXT PRIMARY KEY,
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    request_id TEXT NOT NULL,
    idempotency_key TEXT NOT NULL,
    actor_user_id TEXT NOT NULL,
    actor_username TEXT NOT NULL,
    actor_role TEXT NOT NULL,
    provider_name TEXT NOT NULL,
    model_name TEXT NOT NULL,
    operation TEXT NOT NULL CHECK (operation IN ('ai_analysis', 'executive_report')),
    route_tier TEXT NOT NULL DEFAULT 'low_cost' CHECK (route_tier IN ('low_cost', 'high_quality')),
    selected_provider TEXT NULL,
    selected_model TEXT NULL,
    policy_snapshot JSONB NOT NULL DEFAULT '{}'::jsonb,
    token_limit_snapshot JSONB NOT NULL DEFAULT '{}'::jsonb,
    price_snapshot JSONB NOT NULL DEFAULT '{}'::jsonb,
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
    currency CHAR(3) NOT NULL,
    latency_ms INTEGER NULL CHECK (latency_ms IS NULL OR latency_ms >= 0),
    provider_request_id TEXT NULL,
    finish_reason TEXT NULL,
    error_code TEXT NULL,
    task_id TEXT NULL,
    document_ids JSONB NOT NULL DEFAULT '[]'::jsonb,
    evidence_refs JSONB NOT NULL DEFAULT '[]'::jsonb,
    analysis_id TEXT NULL,
    ai_analysis_id TEXT NULL,
    report_id TEXT NULL,
    report_version_id TEXT NULL,
    fallback_used BOOLEAN NOT NULL DEFAULT FALSE,
    attempt_count INTEGER NOT NULL DEFAULT 0 CHECK (attempt_count >= 0),
    completed_at TIMESTAMPTZ NULL,
    UNIQUE (actor_user_id, idempotency_key)
);

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
);

CREATE TABLE IF NOT EXISTS llm_provider_circuit_state (
    provider_name TEXT PRIMARY KEY,
    state TEXT NOT NULL CHECK (state IN ('closed','open','half_open')),
    failure_count INTEGER NOT NULL DEFAULT 0 CHECK (failure_count >= 0),
    opened_at TIMESTAMPTZ NULL,
    half_open_probes INTEGER NOT NULL DEFAULT 0 CHECK (half_open_probes >= 0),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS llm_quota_buckets (
    bucket_date DATE NOT NULL,
    scope_type TEXT NOT NULL CHECK (scope_type IN ('user','global')),
    scope_id TEXT NOT NULL,
    route_tier TEXT NOT NULL DEFAULT 'low_cost' CHECK (route_tier IN ('low_cost', 'high_quality')),
    request_count BIGINT NOT NULL DEFAULT 0 CHECK (request_count >= 0),
    token_count BIGINT NOT NULL DEFAULT 0 CHECK (token_count >= 0),
    cost NUMERIC(20,8) NOT NULL DEFAULT 0 CHECK (cost >= 0),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (bucket_date, scope_type, scope_id, route_tier)
);

CREATE TABLE IF NOT EXISTS ai_analysis_results (
    analysis_id TEXT PRIMARY KEY,
    usage_id TEXT NOT NULL UNIQUE REFERENCES llm_usage_ledger(usage_id) ON DELETE RESTRICT,
    answer TEXT NOT NULL,
    citations JSONB NOT NULL,
    provider_name TEXT NOT NULL,
    model_name TEXT NOT NULL,
    input_tokens INTEGER NOT NULL,
    output_tokens INTEGER NOT NULL,
    total_tokens INTEGER NOT NULL,
    actual_cost NUMERIC(20,8) NOT NULL,
    currency CHAR(3) NOT NULL,
    status TEXT NOT NULL CHECK (status = 'succeeded'),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_events_stream_sequence ON events (stream_id, sequence);
CREATE INDEX IF NOT EXISTS idx_events_type_created ON events (event_type, created_at);
CREATE INDEX IF NOT EXISTS idx_report_versions_task_version ON report_versions (task_id, version_no DESC);
CREATE INDEX IF NOT EXISTS idx_approval_requests_task_status ON approval_requests (task_id, status);
CREATE INDEX IF NOT EXISTS idx_approval_events_approval_created ON approval_events (approval_id, created_at);
CREATE UNIQUE INDEX IF NOT EXISTS ux_approval_requests_one_pending_per_task
    ON approval_requests (task_id)
    WHERE status = 'pending_approval';
CREATE INDEX IF NOT EXISTS idx_approval_events_task_created_id
    ON approval_events (task_id, created_at ASC, id ASC);
CREATE INDEX IF NOT EXISTS idx_audit_logs_resource_created ON audit_logs (resource_type, resource_id, created_at);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_id_desc ON audit_logs (created_at DESC, id DESC);
CREATE INDEX IF NOT EXISTS idx_audit_logs_actor_created ON audit_logs (actor_id, created_at DESC, id DESC);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action_created ON audit_logs (operation_type, created_at DESC, id DESC);
CREATE INDEX IF NOT EXISTS idx_audit_logs_request_id ON audit_logs (request_id);
CREATE INDEX IF NOT EXISTS idx_documents_status_updated ON documents (status, updated_at);
CREATE INDEX IF NOT EXISTS idx_document_chunks_document_version ON document_chunks (document_id, version, chunk_index);
CREATE INDEX IF NOT EXISTS idx_document_chunks_embedding_hnsw
    ON document_chunks USING hnsw (embedding vector_cosine_ops)
    WHERE embedding IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_document_imports_status_updated ON document_imports (status, updated_at);
CREATE INDEX IF NOT EXISTS idx_upload_sessions_document ON upload_sessions (document_id);
CREATE INDEX IF NOT EXISTS idx_upload_idempotency_upload ON upload_idempotency_keys (upload_id);
CREATE INDEX IF NOT EXISTS idx_llm_usage_actor_occurred ON llm_usage_ledger (actor_user_id, occurred_at DESC);
CREATE INDEX IF NOT EXISTS idx_llm_usage_status_occurred ON llm_usage_ledger (status, occurred_at DESC);
CREATE INDEX IF NOT EXISTS idx_llm_usage_request_id ON llm_usage_ledger (request_id);
CREATE INDEX IF NOT EXISTS idx_llm_usage_route_tier_occurred ON llm_usage_ledger (route_tier, occurred_at DESC);
CREATE INDEX IF NOT EXISTS idx_llm_usage_operation_occurred ON llm_usage_ledger (operation, occurred_at DESC);
CREATE INDEX IF NOT EXISTS idx_llm_usage_analysis_id ON llm_usage_ledger (ai_analysis_id);
CREATE INDEX IF NOT EXISTS idx_llm_usage_report_id ON llm_usage_ledger (report_id);
CREATE INDEX IF NOT EXISTS idx_llm_provider_attempts_usage ON llm_provider_attempts (usage_id, attempt_number);
CREATE INDEX IF NOT EXISTS idx_llm_provider_attempts_request ON llm_provider_attempts (request_id);
CREATE INDEX IF NOT EXISTS idx_llm_provider_attempts_provider ON llm_provider_attempts (provider_name, created_at DESC);
