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

CREATE INDEX IF NOT EXISTS idx_events_stream_sequence ON events (stream_id, sequence);
CREATE INDEX IF NOT EXISTS idx_events_type_created ON events (event_type, created_at);
CREATE INDEX IF NOT EXISTS idx_report_versions_task_version ON report_versions (task_id, version_no DESC);
CREATE INDEX IF NOT EXISTS idx_approval_requests_task_status ON approval_requests (task_id, status);
CREATE INDEX IF NOT EXISTS idx_approval_events_approval_created ON approval_events (approval_id, created_at);
CREATE UNIQUE INDEX IF NOT EXISTS ux_approval_requests_one_pending_per_task
    ON approval_requests (task_id)
    WHERE status = 'pending_approval';
CREATE INDEX IF NOT EXISTS idx_approval_events_approval_created_id
    ON approval_events (approval_id, created_at ASC, id ASC);
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
