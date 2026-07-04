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

Shared request rule:

- `POST /api/v1/documents` accepts `multipart/form-data` with `file` and `metadata`.
- `GET`, `DELETE`, and chunk `POST` endpoints use path parameters only; chunk `POST` has no request body.
- `metadata` must include the frozen document domain fields from `docs/MASTER_PROMPT.md` and `docs/ARCHITECTURE.md`.

Shared response rule:

- Response bodies must stay document-centric.
- Approval state is not embedded as an active workflow object in this freeze.
- `POST /api/v1/documents/{document_id}/chunks` and `GET /api/v1/documents/{document_id}/chunks` expose chunk snapshots; chunk payloads are not embedded in upload or list responses.
- Upload responses return a `DocumentUploadSession` snapshot that reflects the completed synchronous MVP upload.
- List responses expose `next_cursor` as a planned pagination placeholder; it is not an implemented cursor-based pagination contract yet.

DocumentUploadSession:

```json
{
  "upload_id": "upl-123",
  "document_id": "doc-123",
  "status": "accepted",
  "progress": 0,
  "created_at": "2026-07-04T12:34:56Z",
  "updated_at": "2026-07-04T12:34:56Z",
  "error_code": null,
  "error_message": null
}
```

Statuses:
`accepted | validating | storing | completed | failed`

#### 4.5.1 `POST /api/v1/documents`

Purpose:
Create a new document record, validate metadata, compute or verify checksum, and freeze the first document version boundary.

Request:

```json
{
  "file": "<binary>",
  "metadata": {
    "title": "June Sales Review",
    "description": "Monthly document upload",
    "owner": "analysis-team",
    "version": 1,
    "language": "en",
    "document_type": "markdown",
    "tags": ["sales", "monthly"],
    "source": {
      "source_type": "local_file",
      "source_uri": "backend/data/documents/june_sales_review.md"
    },
    "checksum": "sha256-..."
  }
}
```

Response `201 Created`:

```json
{
  "document_id": "doc-123",
  "upload_id": "upl-123",
  "status": "completed",
  "progress": 100,
  "created_at": "2026-07-04T12:34:56Z",
  "updated_at": "2026-07-04T12:34:56Z",
  "error_code": null,
  "error_message": null
}
```

Status codes:
`201 Created`, `400 Bad Request`, `409 Conflict`, `413 Payload Too Large`, `415 Unsupported Media Type`, `422 Unprocessable Entity`, `500 Internal Server Error`.

Error codes:
`missing_title`, `empty_file`, `unsupported_document_type`, `invalid_metadata`, `duplicate_checksum`, `repository_error`, `idempotency_conflict`, `upload_too_large`, `unsupported_encoding`, `internal_error`.

Validation rules:
- `title` is required and must not be blank.
- `file` must not be empty.
- `document_type` must be one of the frozen document types.
- `language` must be one of `en`, `ja`, `zh-CN`, `unknown`.
- `checksum` must be present and unique for the repository scope.
- Future approval is not auto-created by this endpoint.
- A duplicate checksum returns the existing document result instead of creating a second record.

Versioning rule:
- This endpoint is frozen as `/api/v1/documents`.
- Breaking request or response changes require `/api/v2/documents`.

Future approval relationship:
- Upload creates the document domain boundary only.
- Approval remains a separate future API and must not be implied by upload success.

Idempotency rule:
- `Idempotency-Key` is optional in MVP but recommended.
- Same key + same checksum returns the existing upload result.
- Same key + different checksum returns `409 Conflict` with `idempotency_conflict`.
- Future production should require `Idempotency-Key`.

#### 4.5.2 `GET /api/v1/documents`

Purpose:
List uploaded documents with frozen metadata filters.

Request:

- Query parameters: `status`, `document_type`, `language`, `owner`, `tag`, `include_archived`, `limit`, `cursor`.

Response `200 OK`:

```json
{
  "items": [],
  "next_cursor": null
}
```

Status codes:
`200 OK`, `400 Bad Request`, `500 Internal Server Error`.

Error codes:
`validation_error`, `repository_error`, `internal_error`.

Validation rules:
- `limit` must stay within the frozen pagination range.
- Filters must use frozen enum values when supplied.
- `cursor` is documented as a planned pagination placeholder and does not change response pagination yet.
- Archived documents are excluded by default and can be included with `include_archived=true` or by setting `status=archived`.

Versioning rule:
- List semantics stay frozen under `/api/v1/documents`.

Future approval relationship:
- Approval metadata must not become a hard dependency of list retrieval.

#### 4.5.3 `GET /api/v1/documents/{document_id}`

Purpose:
Read one document and its frozen metadata snapshot.

Request:

- Path parameter: `document_id`

Response `200 OK`:

```json
{
  "document_id": "doc-123",
  "title": "June Sales Review",
  "description": "Monthly document upload",
  "owner": "analysis-team",
  "created_at": "2026-07-04T12:34:56Z",
  "updated_at": "2026-07-04T12:34:56Z",
  "version": 1,
  "language": "en",
  "document_type": "markdown",
  "status": "uploaded",
  "tags": ["sales", "monthly"],
  "source": {
    "source_type": "local_file",
    "source_uri": "backend/data/documents/june_sales_review.md"
  },
  "checksum": "sha256-..."
}
```

Status codes:
`200 OK`, `404 Not Found`, `500 Internal Server Error`.

Error codes:
`document_not_found`, `repository_error`, `internal_error`.

Validation rules:
- `document_id` must be a valid resource identifier.

Versioning rule:
- Detail response stays backward compatible within `/api/v1`.

Future approval relationship:
- Future approval data, if added, must be an additive expansion only.

#### 4.5.4 `GET /api/v1/documents/{document_id}/versions`

Purpose:
Read the frozen version history for one document.

Request:

- Path parameter: `document_id`

Response `200 OK`:

```json
{
  "document_id": "doc-123",
  "items": []
}
```

Status codes:
`200 OK`, `404 Not Found`, `500 Internal Server Error`.

Error codes:
`document_not_found`, `document_version_not_found`, `repository_error`, `internal_error`.

Validation rules:
- Version items must be ordered by `version_no`.
- Version history must never be rewritten in place.

Versioning rule:
- New version metadata fields must be additive only.

Future approval relationship:
- Approval is version-aware in the future, but this endpoint does not create approval records.

#### 4.5.5 `POST /api/v1/documents/{document_id}/chunks`

Purpose:
Create or replace the deterministic chunk set for a validated document.

Request:

- Path parameter: `document_id`
- No request body.

Response `201 Created`:

```json
{
  "document_id": "doc-123",
  "version": 1,
  "items": [
    {
      "document_id": "doc-123",
      "version": 1,
      "chunk_id": "chk-123",
      "chunk_index": 0,
      "content": "Paragraph one.",
      "character_count": 14,
      "metadata": {
        "document_id": "doc-123",
        "title": "June Sales Review",
        "description": "Monthly document upload",
        "owner": "analysis-team",
        "created_at": "2026-07-04T12:34:56Z",
        "updated_at": "2026-07-04T12:34:56Z",
        "version": 1,
        "language": "en",
        "document_type": "markdown",
        "status": "validated",
        "tags": ["sales", "monthly"],
        "source": {
          "source_type": "local_file",
          "source_uri": "backend/data/documents/june_sales_review.md"
        },
        "checksum": "sha256-..."
      },
      "created_at": "2026-07-04T12:34:56Z"
    }
  ],
  "next_cursor": null
}
```

Status codes:
`201 Created`, `404 Not Found`, `409 Conflict`, `415 Unsupported Media Type`, `500 Internal Server Error`.

Error codes:
`document_not_found`, `document_archived`, `document_not_validated`, `unsupported_document_type`, `chunk_failed`, `repository_error`, `internal_error`.

Validation rules:
- `document_id` must reference an existing document.
- The document must be in `validated` status.
- Archived documents are rejected.
- Only `markdown` and `text` are supported in the current chunk pipeline.
- Repeated chunking replaces the stored chunk set with the same deterministic output for the same document version.

Versioning rule:
- Chunk output fields must remain additive only within `/api/v1`.

Future approval relationship:
- Chunk generation is a preprocessing step only and does not create approval state.

#### 4.5.6 `GET /api/v1/documents/{document_id}/chunks`

Purpose:
Read the stored chunk set for a validated document version.

Request:

- Path parameter: `document_id`

Response `200 OK`:

```json
{
  "document_id": "doc-123",
  "version": 1,
  "items": [],
  "next_cursor": null
}
```

Status codes:
`200 OK`, `404 Not Found`, `409 Conflict`, `415 Unsupported Media Type`, `500 Internal Server Error`.

Error codes:
`document_not_found`, `document_archived`, `document_not_validated`, `unsupported_document_type`, `repository_error`, `internal_error`.

Validation rules:
- The document must exist and be validated.
- Archived documents are rejected.
- The endpoint returns the stored chunk snapshot for the current version.

Versioning rule:
- Chunk reads stay backward compatible within `/api/v1`.

Future approval relationship:
- Chunk reads are independent of approval state.

#### 4.5.7 `DELETE /api/v1/documents/{document_id}`

Purpose:
Archive a document and preserve version history rather than physically deleting facts.

Request:

- Path parameter: `document_id`

Response `202 Accepted`:

```json
{
  "success": true,
  "request_id": "req-123",
  "data": {
    "document_id": "doc-123",
    "status": "archived"
  },
  "error": null
}
```

Status codes:
`202 Accepted`, `404 Not Found`, `500 Internal Server Error`.

Error codes:
`document_not_found`, `repository_error`, `internal_error`.

Validation rules:
- Delete means archive / soft delete for the frozen contract.
- Physical removal of version history is not part of this contract.
- The operation is idempotent: archiving an already archived document still returns success.

Versioning rule:
- Deletion semantics must not break existing resource reads.

Future approval relationship:
- If approval is added later, active approval states may block archive until the future approval API resolves the document.

#### 4.5.8 `GET /api/v1/documents/{document_id}/upload`

Purpose:
Read the frozen upload session snapshot for retries and progress display.

Request:

- Path parameter: `document_id`

Response `200 OK`:

```json
{
  "upload_id": "upl-123",
  "document_id": "doc-123",
  "status": "completed",
  "progress": 100,
  "created_at": "2026-07-04T12:34:56Z",
  "updated_at": "2026-07-04T12:35:01Z",
  "error_code": null,
  "error_message": null
}
```

Status codes:
`200 OK`, `404 Not Found`, `500 Internal Server Error`.

Error codes:
`document_not_found`, `repository_error`, `internal_error`.

Versioning rule:
- Upload session semantics stay versioned together with `/api/v1/documents`.

#### 4.5.9 `POST /api/v1/documents/{document_id}/import`

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

#### 4.5.10 `GET /api/v1/document-imports/{import_id}`

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

#### 4.5.11 `POST /api/v1/document-retrieval/search`

Purpose:
Run internal document retrieval over the frozen document chunks and return keyword-based ranked results.

Request:

```json
{
  "query": "monthly sales policy",
  "limit": 10,
  "include_archived": false,
  "document_type": "markdown",
  "language": "en",
  "tags": ["sales", "policy"]
}
```

Rules:

- `query`: required, non-empty string.
- `limit`: optional, positive integer within the frozen range.
- `include_archived`: optional boolean, defaults to `false`.
- `document_type`: optional frozen document type filter.
- `language`: optional frozen language filter.
- `tags`: optional list of non-empty strings.

Response `200 OK`:

```json
{
  "results": [
    {
      "document_id": "doc-123",
      "chunk_id": "chk-123",
      "chunk_index": 0,
      "content_excerpt": "Sales policy summary ...",
      "score": 0.87,
      "source": {
        "source_type": "local_file",
        "uri": "upload://upl-123/policy.md",
        "label": "policy.md",
        "external_id": null
      },
      "metadata": {
        "document_id": "doc-123",
        "title": "Sales Policy",
        "description": "Internal policy",
        "owner": "analysis-team",
        "created_at": "2026-07-04T12:34:56Z",
        "updated_at": "2026-07-04T12:34:56Z",
        "version": 1,
        "language": "en",
        "document_type": "markdown",
        "status": "validated",
        "tags": ["sales", "policy"],
        "source": {
          "source_type": "local_file",
          "source_uri": "backend/data/documents/policy.md"
        },
        "checksum": "sha256-..."
      }
    }
  ],
  "total": 1,
  "query": "monthly sales policy",
  "retrieval_mode": "keyword"
}
```

Status codes:
`200 OK`, `400 Bad Request`, `500 Internal Server Error`, `503 Service Unavailable`.

Error codes:
`invalid_query`, `retrieval_unavailable`, `repository_error`, `internal_error`.

Validation rules:
- `query` must not be blank.
- `limit` must stay within the frozen range.
- Filters must use frozen enum values and tag strings when supplied.
- `include_archived=false` excludes archived documents from ranked results.
- Retrieval mode is frozen as `keyword` for this MVP.

Versioning rule:
- Retrieval search semantics are frozen under `/api/v1`.

Future approval relationship:
- Retrieval returns document facts only and does not create approval state or RAG answers.

#### 4.5.12 `POST /api/v1/internal-rag/answer`

Purpose:
Freeze the internal RAG answer contract on top of the existing document retrieval provider boundary.

Request:

```json
{
  "question": "What is the monthly sales policy?",
  "limit": 5,
  "include_archived": false,
  "document_type": "markdown",
  "language": "en",
  "tags": ["sales", "policy"],
  "answer_mode": "extractive",
  "require_citations": true
}
```

Rules:

- `question`: required, non-empty string.
- `limit`: optional, positive integer within the frozen range.
- `include_archived`: optional boolean, defaults to `false`.
- `document_type`: optional frozen document type filter.
- `language`: optional frozen language filter.
- `tags`: optional list of non-empty strings.
- `answer_mode`: required enum `extractive | summary`.
- `require_citations`: required boolean and frozen as `true`.

Response `200 OK`:

```json
{
  "answer": "Extractive answer placeholder",
  "citations": [
    {
      "document_id": "doc-123",
      "chunk_id": "chk-123",
      "chunk_index": 0,
      "excerpt": "Sales policy summary ...",
      "source": {
        "source_type": "local_file",
        "uri": "upload://upl-123/policy.md",
        "label": "policy.md",
        "external_id": null
      },
      "score": 0.87
    }
  ],
  "retrieval_mode": "keyword",
  "answer_mode": "extractive",
  "confidence": 0.72,
  "warnings": []
}
```

Status codes:
`200 OK`, `400 Bad Request`, `422 Unprocessable Entity`, `500 Internal Server Error`, `503 Service Unavailable`.

Error codes:
`invalid_question`, `retrieval_unavailable`, `insufficient_context`, `citation_required`, `provider_timeout`, `repository_error`, `internal_error`.

Validation rules:
- `question` must not be blank.
- `limit` must stay within the frozen range.
- `require_citations` is frozen as `true`; `false` is a contract violation.
- `answer_mode=summary` is frozen as a contract option, but it does not imply that a real LLM provider is currently implemented.
- `retrieval_mode` is frozen as `keyword` for this phase because the contract sits on top of the existing document retrieval provider.

Versioning rule:
- Internal RAG answer semantics are frozen under `/api/v1`.

Future approval relationship:
- Internal RAG returns grounded answers and citations only and does not create approval state.
- Future approval integration must be a separate step and must not be implied by answer generation success.

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
- `document_not_validated`
- `unsupported_document_type`
- `invalid_metadata`
- `invalid_query`
- `invalid_question`
- `retrieval_unavailable`
- `insufficient_context`
- `citation_required`
- `chunk_failed`
- `repository_error`
- `provider_error`
- `workflow_error`
- `internal_error`
- `document_not_found`
- `document_validation_failed`
- `document_duplicate_checksum`
- `document_type_unsupported`
- `document_metadata_invalid`
- `document_delete_conflict`
- `document_version_not_found`

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
