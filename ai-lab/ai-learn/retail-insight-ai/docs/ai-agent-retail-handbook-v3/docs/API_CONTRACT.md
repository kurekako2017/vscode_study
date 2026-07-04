# API Contract / API 契约 / API 契約

## 1. Scope / 范围 / 範囲

This document freezes HTTP API rules for `Retail Insight AI`.
本文件冻结 `Retail Insight AI` 的 HTTP API 规范。
本書は `Retail Insight AI` の HTTP API 規約を凍結します。

## 2. Versioning Rules / 版本规则 / バージョン規則

- Existing endpoints keep current paths and behavior unless a documented breaking change is approved.
- New APIs must be versioned, for example `/api/v1/...`.
- A breaking request or response change requires a new version.
- Additive optional fields are allowed only when old clients continue to work.

## 3. Naming Rules / 命名规则 / 命名規則

- Path segments: lowercase plural nouns where possible.
- JSON fields: `snake_case` on backend contracts unless an existing frozen contract already differs.
- IDs: `task_id`, `request_id`, `trace_id`, `report_id`, `approval_request_id`, `upload_id`, `document_id`.
- Time fields: ISO 8601 UTC strings.

## 4. Frozen Current APIs / 当前冻结 API / 現在凍結 API

### 4.1 `POST /api/tasks`

Purpose:
Create a new analysis task.

Request:

```json
{
  "question": "売上と在庫の状況を分析してください",
  "mode": "hybrid"
}
```

Rules:

- `question`: required, non-empty string.
- `mode`: required, enum `kpi | research | hybrid`.

Success Response `202 Accepted`:

```json
{
  "task_id": "uuid-or-equivalent-id",
  "status": "queued"
}
```

Error Response:

```json
{
  "error_code": "validation_error",
  "message": "mode must be one of kpi, research, hybrid",
  "request_id": "req-123"
}
```

### 4.2 `GET /api/tasks/{task_id}`

Purpose:
Read task status.

Success Response `200 OK`:

```json
{
  "task_id": "task-123",
  "status": "running",
  "mode": "hybrid",
  "question": "売上と在庫の状況を分析してください"
}
```

Status enum:
`queued | running | completed | failed`

### 4.3 `GET /api/tasks/{task_id}/events`

Purpose:
Subscribe to server-sent events for a task.

Success Response:

- HTTP `200 OK`
- `Content-Type: text/event-stream`

Contract:

- Event envelope follows `docs/EVENT_CONTRACT.md`.
- Current event families are `started | status | done | error`.

### 4.4 `GET /api/tasks/{task_id}/report`

Purpose:
Read the generated report for a completed or partially available task.

Success Response `200 OK`:

```json
{
  "task_id": "task-123",
  "status": "generated",
  "content": "# Report\n...",
  "sources": [
    {
      "label": "market_trend_2026_06",
      "url": "https://example.invalid/source"
    }
  ]
}
```

Notes:

- `status` here is report approval status, not task execution status.
- Current implemented report status is `generated`.

### 4.5 Document Upload APIs / 文档上传 API / 文書アップロード API

All document upload endpoints are frozen under `/api/v1`.
所有文档上传接口都冻结在 `/api/v1`。
すべての文書アップロード API は `/api/v1` 配下で凍結します。

- `POST /api/v1/documents` accepts `multipart/form-data` with `file` and `metadata`.
- `POST /api/v1/documents` may include `Idempotency-Key` for future-safe retries.
- Upload responses return a `DocumentUploadSession` snapshot that reflects the completed synchronous MVP upload.
- `GET /api/v1/documents` keeps `next_cursor` as a planned pagination placeholder; `include_archived=true` or `status=archived` can expose archived documents.
- `DELETE /api/v1/documents/{document_id}` is archive / soft delete, and archived documents remain readable.

DocumentUploadSession:

```json
{
  "upload_id": "upl-123",
  "document_id": "doc-123",
  "status": "completed",
  "progress": 100,
  "created_at": "2026-07-04T12:34:56Z",
  "updated_at": "2026-07-04T12:34:56Z",
  "error_code": null,
  "error_message": null
}
```

Statuses:
`accepted | validating | storing | completed | failed`

- Same checksum returns the existing document result instead of creating a second record.
- Same key + same checksum returns the existing upload result.
- Same key + different checksum returns `409 Conflict` with `idempotency_conflict`.
- Future production should require `Idempotency-Key`.

#### 4.5.8 `POST /api/v1/documents/{document_id}/import`

Purpose:
Run the document import pipeline for an already uploaded document and mark successful imports as validated.

Request:

- Path parameter: `document_id`

Response `201 Created`:

```json
{
  "import_id": "imp-123",
  "document_id": "doc-123",
  "status": "completed",
  "created_at": "2026-07-04T12:34:56Z",
  "updated_at": "2026-07-04T12:34:56Z",
  "error_code": null,
  "error_message": null
}
```

Status codes:
`201 Created`, `404 Not Found`, `409 Conflict`, `415 Unsupported Media Type`, `422 Unprocessable Entity`, `500 Internal Server Error`.

Error codes:
`document_not_found`, `document_archived`, `unsupported_document_type`, `invalid_metadata`, `import_already_running`, `repository_error`, `internal_error`.

Validation rules:
- The document must already exist in the document repository.
- Archived documents must not be imported.
- Allowed import document types are `markdown`, `text`, `csv`, and `json`.
- Planned-only types such as `pdf`, `word`, `excel`, and `image` return `unsupported_document_type`.
- Successful import marks the document as `validated`.
- Repeated import of the same document is deterministic and returns the same import record.

Versioning rule:
- Import semantics are frozen under `/api/v1`.

Future approval relationship:
- Import prepares the document for future chunking, retrieval, and approval, but does not create approval records.

#### 4.5.9 `GET /api/v1/document-imports/{import_id}`

Purpose:
Read the status and error state of a previously created document import record.

Request:

- Path parameter: `import_id`

Response `200 OK`:

```json
{
  "import_id": "imp-123",
  "document_id": "doc-123",
  "status": "completed",
  "created_at": "2026-07-04T12:34:56Z",
  "updated_at": "2026-07-04T12:34:56Z",
  "error_code": null,
  "error_message": null
}
```

Status codes:
`200 OK`, `404 Not Found`, `500 Internal Server Error`.

Error codes:
`document_import_not_found`, `repository_error`, `internal_error`.

Versioning rule:
- Import record reads are frozen under `/api/v1`.

## 5. HTTP Status Rules / 状态码规则 / HTTP ステータス規則

- `200 OK`: successful read.
- `201 Created`: document upload creation.
- `202 Accepted`: accepted async task creation.
- `400 Bad Request`: malformed or invalid input.
- `404 Not Found`: resource not found.
- `409 Conflict`: state conflict or duplicate operation.
- `422 Unprocessable Entity`: semantically invalid payload when adopted by new versioned APIs.
- `500 Internal Server Error`: unexpected server failure.
- `503 Service Unavailable`: temporary dependency or provider failure.

## 6. Error Contract / 错误契约 / エラー契約

Standard error body:

```json
{
  "error_code": "string_code",
  "message": "human readable summary",
  "request_id": "req-123",
  "details": {}
}
```

Frozen error code families:

- `validation_error`
- `task_not_found`
- `report_not_found`
- `document_not_found`
- `document_import_not_found`
- `document_archived`
- `import_already_running`
- `unsupported_document_type`
- `invalid_metadata`
- `repository_error`
- `provider_error`
- `workflow_error`
- `internal_error`

Future approval/import/retrieval APIs must add explicit error codes without reusing unrelated ones.

## 7. Backward Compatibility / 向后兼容 / 後方互換

- Do not remove current required response fields from frozen endpoints.
- Do not rename current fields in-place.
- New optional fields must be additive and documented.
- New endpoint families must use explicit version prefixes.

## 8. Trilingual Key Terms / 三语术语 / 三言語用語

| English | 中文（简体） | 日本語 |
|---|---|---|
| Request | 请求 | リクエスト |
| Response | 响应 | レスポンス |
| Status Code | 状态码 | ステータスコード |
| Error Code | 错误码 | エラーコード |
| Backward Compatibility | 向后兼容 | 後方互換 |
| Task | 任务 | タスク |
| Report | 报告 | レポート |
| Approval Status | 审批状态 | 承認ステータス |

## 9. API Change Checklist / API 变更清单 / API 変更チェックリスト

1. Is the API new or existing?
2. If new, did you version it?
3. If existing, is the change additive and backward-compatible?
4. Did you update tests, docs, task, backlog, changelog, and handbook mirror?
5. Did you review SSE or prompt impact if the endpoint changes workflow behavior?
