CREATE TABLE IF NOT EXISTS tasks (
    task_id TEXT PRIMARY KEY,
    question TEXT NOT NULL,
    mode TEXT NOT NULL,
    status TEXT NOT NULL,
    error TEXT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS task_events (
    id BIGSERIAL PRIMARY KEY,
    task_id TEXT NOT NULL REFERENCES tasks(task_id) ON DELETE CASCADE,
    sequence INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    message TEXT NOT NULL,
    data_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (task_id, sequence)
);

CREATE TABLE IF NOT EXISTS reports (
    task_id TEXT PRIMARY KEY REFERENCES tasks(task_id) ON DELETE CASCADE,
    markdown TEXT NOT NULL,
    provider TEXT NOT NULL,
    approval_status TEXT NOT NULL DEFAULT 'generated',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (
        approval_status IN (
            'generated',
            'draft',
            'pending_approval',
            'approved',
            'rejected',
            'revised',
            'published',
            'archived'
        )
    )
);

CREATE TABLE IF NOT EXISTS report_versions (
    id BIGSERIAL PRIMARY KEY,
    task_id TEXT NOT NULL REFERENCES tasks(task_id) ON DELETE CASCADE,
    version_no INTEGER NOT NULL,
    markdown TEXT NOT NULL,
    status TEXT NOT NULL,
    revision_reason TEXT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT NULL,
    UNIQUE (task_id, version_no)
);

CREATE TABLE IF NOT EXISTS data_imports (
    id BIGSERIAL PRIMARY KEY,
    import_type TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    schema_version TEXT NOT NULL,
    status TEXT NOT NULL,
    record_count INTEGER NOT NULL DEFAULT 0,
    started_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMPTZ NULL,
    created_by TEXT NULL
);

CREATE TABLE IF NOT EXISTS import_errors (
    id BIGSERIAL PRIMARY KEY,
    data_import_id BIGINT NOT NULL REFERENCES data_imports(id) ON DELETE CASCADE,
    error_code TEXT NOT NULL,
    field_name TEXT NULL,
    row_number INTEGER NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS approval_requests (
    id BIGSERIAL PRIMARY KEY,
    report_version_id BIGINT NOT NULL REFERENCES report_versions(id) ON DELETE CASCADE,
    requested_by TEXT NULL,
    requested_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL,
    approver_id TEXT NULL,
    decision_at TIMESTAMPTZ NULL
);

CREATE TABLE IF NOT EXISTS approval_events (
    id BIGSERIAL PRIMARY KEY,
    approval_request_id BIGINT NOT NULL REFERENCES approval_requests(id) ON DELETE CASCADE,
    event_type TEXT NOT NULL,
    actor_id TEXT NULL,
    reason TEXT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_task_events_task_sequence
    ON task_events (task_id, sequence);

CREATE INDEX IF NOT EXISTS idx_report_versions_task_version
    ON report_versions (task_id, version_no);

CREATE INDEX IF NOT EXISTS idx_import_errors_data_import
    ON import_errors (data_import_id);

CREATE INDEX IF NOT EXISTS idx_approval_requests_report_version
    ON approval_requests (report_version_id);

CREATE INDEX IF NOT EXISTS idx_approval_events_request
    ON approval_events (approval_request_id);
