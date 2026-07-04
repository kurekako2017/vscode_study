# API Contract / API 契约 / API 契約

## 1. Scope / 范围 / 範囲

This document freezes HTTP API rules for `Retail Insight AI`.
本文件冻结 `Retail Insight AI` 的 HTTP API 规范。
本書は `Retail Insight AI` の HTTP API 規約を凍結します。

Human-readable explanations in this document are trilingual by default.
本文件中的人类可读说明默认采用三语。
本書の人間向け説明は三言語を標準とします。

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
- `POST /api/v1/documents/{document_id}/chunks` and `GET /api/v1/documents/{document_id}/chunks` expose chunk snapshots; chunk payloads are not embedded in upload or list responses.
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

#### 4.5.8 `POST /api/v1/documents/{document_id}/chunks`

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

#### 4.5.9 `GET /api/v1/documents/{document_id}/chunks`

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
Run internal document retrieval over frozen document chunks and return keyword-ranked results.

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
- `warnings[]` may include internal quality signals such as `low_context`, `missing_citation`, and `weak_match`; these are backward-compatible advisory values, not new error codes.
- Future `LLMProvider` / `RAGAnswerGenerator` integration must keep this response shape unchanged and should fall back to deterministic extractive mode before any contract-breaking behavior is considered.

Versioning rule:
- Internal RAG answer semantics are frozen under `/api/v1`.

Future approval relationship:
- Internal RAG returns grounded answers and citations only and does not create approval state.
- Future approval integration must be a separate step and must not be implied by answer generation success.

#### 4.5.13 Approval Workflow APIs

Purpose:
Freeze the approval workflow contract on top of report revisions, audit history, and future RBAC.

中文（简体）：
冻结审批工作流的 HTTP 合同，核心是“审批记录”和“报告版本快照”分离。审批 API 只负责提交、查询、批准、拒绝和修订，不负责 RBAC，也不允许把可变正文当作审批事实。

日本語：
承認ワークフローの HTTP 契約を凍結します。承認記録とレポート版スナップショットを分離し、API は submit / list / detail / approve / reject / revise だけを担当します。RBAC や可変本文の上書きは含めません。

Approval domain model:

- One `task_id` identifies the report business aggregate.
- Each report revision is an immutable snapshot.
- `approval_id` identifies the approval request record for a report version.
- `report_version_id` identifies the frozen report snapshot under review.
- `revised_from_version_id` identifies the prior version that spawned a revision.

State model:

- `draft`
- `pending_approval`
- `approved`
- `rejected`
- `revised`
- `published`
- `archived`

State rules:

- `draft -> pending_approval` when the report is submitted for approval.
- `pending_approval -> approved` when the approval is granted.
- `pending_approval -> rejected` when the approval is denied.
- `rejected -> revised` when a new revision is created.
- `approved -> revised` is allowed only by creating a new immutable revision; the approved snapshot itself must not change.
- `approved -> published` is the business-confirmation step and produces the final business output.
- `published -> archived` keeps the published report readable while removing it from active use.
- Approved reports cannot be overwritten.
- Rejected reports must keep a rejection reason.
- Archived reports remain readable.

Future RBAC relationship:

- Authorization is not implemented in this contract freeze.
- Future RBAC will decide who may submit, approve, reject, revise, or publish.
- The API contract must remain valid even before RBAC is connected.

Audit relationship:

- Approval decisions are append-only facts.
- Revision creation must preserve the prior version and record the new version in the audit trail.
- Approval payloads must stay secret-safe and never include full report text.

##### `POST /api/v1/reports/{task_id}/submit-approval`

Purpose:
Create a pending approval record for the current report version.

Request:

```json
{
  "comment": "Ready for review"
}
```

Response `201 Created`:

```json
{
  "approval_id": "apr-123",
  "task_id": "task-123",
  "report_version_id": "repver-456",
  "status": "pending_approval",
  "requested_at": "2026-07-04T12:34:56Z",
  "requested_by": "reviewer-1",
  "decided_at": null,
  "decided_by": null,
  "decision_reason": null,
  "revision_no": 1,
  "revised_from_version_id": null
}
```

Status codes:
`201 Created`, `404 Not Found`, `409 Conflict`, `422 Unprocessable Entity`, `500 Internal Server Error`.

Error codes:
`approval_not_found`, `approval_already_submitted`, `approval_already_decided`, `invalid_approval_state`, `report_not_found`, `report_revision_conflict`, `internal_error`.

##### `GET /api/v1/approvals`

Purpose:
List approval records for audit, operations, and future workflow monitoring.

Request:

- Query parameters: `status`, `task_id`, `limit`, `cursor`.

Response `200 OK`:

```json
{
  "items": [
    {
      "approval_id": "apr-123",
      "task_id": "task-123",
      "report_version_id": "repver-456",
      "status": "pending_approval",
      "requested_at": "2026-07-04T12:34:56Z",
      "requested_by": "reviewer-1",
      "decided_at": null,
      "decided_by": null,
      "decision_reason": null,
      "revision_no": 1,
      "revised_from_version_id": null
    }
  ],
  "next_cursor": null
}
```

Status codes:
`200 OK`, `400 Bad Request`, `500 Internal Server Error`.

Error codes:
`validation_error`, `repository_error`, `internal_error`.

##### `GET /api/v1/approvals/{approval_id}`

Purpose:
Read one approval record and its frozen report-version binding.

Request:

- Path parameter: `approval_id`.

Response `200 OK`:

```json
{
  "approval_id": "apr-123",
  "task_id": "task-123",
  "report_version_id": "repver-456",
  "status": "pending_approval",
  "requested_at": "2026-07-04T12:34:56Z",
  "requested_by": "reviewer-1",
  "decided_at": null,
  "decided_by": null,
  "decision_reason": null,
  "revision_no": 1,
  "revised_from_version_id": null
}
```

Status codes:
`200 OK`, `404 Not Found`, `500 Internal Server Error`.

Error codes:
`approval_not_found`, `repository_error`, `internal_error`.

##### `POST /api/v1/approvals/{approval_id}/approve`

Purpose:
Approve the pending approval record.

Request:

```json
{
  "comment": "Approved after review"
}
```

Response `200 OK`:

```json
{
  "approval_id": "apr-123",
  "task_id": "task-123",
  "report_version_id": "repver-456",
  "status": "approved",
  "requested_at": "2026-07-04T12:34:56Z",
  "requested_by": "reviewer-1",
  "decided_at": "2026-07-04T12:40:00Z",
  "decided_by": "approver-1",
  "decision_reason": null,
  "revision_no": 1,
  "revised_from_version_id": null
}
```

Status codes:
`200 OK`, `404 Not Found`, `409 Conflict`, `500 Internal Server Error`.

Error codes:
`approval_not_found`, `approval_already_decided`, `approval_already_submitted`, `invalid_approval_state`, `report_revision_conflict`, `internal_error`.

##### `POST /api/v1/approvals/{approval_id}/reject`

Purpose:
Reject the pending approval record.

Request:

```json
{
  "reason": "The report needs a clearer source trace."
}
```

Response `200 OK`:

```json
{
  "approval_id": "apr-123",
  "task_id": "task-123",
  "report_version_id": "repver-456",
  "status": "rejected",
  "requested_at": "2026-07-04T12:34:56Z",
  "requested_by": "reviewer-1",
  "decided_at": "2026-07-04T12:40:00Z",
  "decided_by": "approver-1",
  "decision_reason": "The report needs a clearer source trace.",
  "revision_no": 1,
  "revised_from_version_id": null
}
```

Status codes:
`200 OK`, `404 Not Found`, `409 Conflict`, `422 Unprocessable Entity`, `500 Internal Server Error`.

Error codes:
`approval_not_found`, `approval_already_decided`, `approval_rejected`, `invalid_approval_state`, `missing_rejection_reason`, `internal_error`.

##### `POST /api/v1/reports/{task_id}/revise`

Purpose:
Create a new immutable report revision without overwriting the approved or rejected snapshot.

Request:

```json
{
  "revision_reason": "Clarify the cited policy language."
}
```

Response `201 Created`:

```json
{
  "task_id": "task-123",
  "report_version_id": "repver-457",
  "status": "revised",
  "revision_no": 2,
  "revised_from_version_id": "repver-456"
}
```

Status codes:
`201 Created`, `404 Not Found`, `409 Conflict`, `422 Unprocessable Entity`, `500 Internal Server Error`.

Error codes:
`report_not_found`, `report_revision_conflict`, `invalid_approval_state`, `approval_rejected`, `missing_rejection_reason`, `internal_error`.

Versioning rule:
- Approval workflow semantics are frozen under `/api/v1`.

Future approval relationship:
- Approval APIs manage report-version snapshots and audit events only.
- Publishing is a downstream business confirmation step and must not be confused with revision creation.
- Future RBAC will constrain who may call these endpoints, but the payload contract is frozen independently of authorization.

中文（简体）：
审批 API 只管理报告版本快照和审计事件。发布是下游业务确认步骤，不能和 revision 混淆。未来 RBAC 只限制谁能调用，不改变当前 payload 合同。

日本語：
承認 API はレポート版スナップショットと監査イベントのみを管理します。公開は下流の業務確認であり、revision と混同してはいけません。将来の RBAC は呼び出し主体を制御するだけで、payload 契約は変えません。

#### 4.5.14 Enterprise Security APIs / 企业安全 API / 企業セキュリティ API

Purpose:
Freeze the future identity, RBAC, and audit read contract before implementation.

中文（简体）：
这一组 API 先冻结“谁在执行”和“谁被授权”的读取合同，再冻结审计读取合同。当前阶段只定义契约，不实现 RBAC、认证服务或审计写入逻辑。

日本語：
この API 群は「誰が実行しているか」と「誰が許可されているか」の読み取り契約、および監査読み取り契約を先に凍結します。現段階では契約のみを定義し、RBAC・認証サービス・監査書き込みは実装しません。

Security domain model:

- `user` belongs to one `organization` and one `department`.
- `role` is a reusable authorization label.
- `permission` is a frozen action token such as `document.read` or `approval.approve`.
- `policy` maps roles to permissions and can later gain scope rules.
- `audit log` is append-only and read-only.
- `operation log` is the business-readable projection of audit facts.

##### RBAC Approval-Action Matrix

| API / Action | Required Permission | Default Role Coverage |
|---|---|---|
| `GET /api/v1/users/me` | authenticated identity | all authenticated users |
| `GET /api/v1/security/roles` | `system.admin` | admin |
| `GET /api/v1/security/permissions` | `system.admin` | admin |
| `GET /api/v1/audit-logs` | `audit.read` | auditor, admin |
| `POST /api/v1/reports/{task_id}/submit-approval` | `report.submit_approval` | analyst, manager, admin |
| `GET /api/v1/approvals` | `approval.review` | approver, manager, auditor, admin |
| `GET /api/v1/approvals/{approval_id}` | `approval.review` | approver, manager, auditor, admin |
| `POST /api/v1/approvals/{approval_id}/approve` | `approval.approve` | approver, manager, admin |
| `POST /api/v1/approvals/{approval_id}/reject` | `approval.reject` | approver, manager, admin |
| `POST /api/v1/reports/{task_id}/revise` | `approval.revise` | analyst, manager, approver, admin |

Frozen roles:

- `admin`
- `manager`
- `analyst`
- `viewer`
- `approver`
- `auditor`

Frozen permissions:

- `document.read`
- `document.upload`
- `document.archive`
- `document.import`
- `document.chunk`
- `document.search`
- `rag.answer`
- `report.read`
- `report.submit_approval`
- `approval.review`
- `approval.approve`
- `approval.reject`
- `approval.revise`
- `audit.read`
- `system.admin`

Future authentication relationship:

- `GET /api/v1/users/me` will be populated by a future authentication provider or middleware.
- The current contract does not define login, logout, token issuance, or identity provider wiring.
- RBAC may later consume the authenticated principal, but the API contract remains read-only for now.

##### `GET /api/v1/users/me`

Purpose:
Return the current authenticated principal snapshot.

Response `200 OK`:

```json
{
  "user_id": "user-123",
  "username": "li.chen",
  "display_name": "Li Chen",
  "organization_id": "org-001",
  "department_id": "dept-001",
  "roles": ["analyst", "approver"],
  "permissions": ["document.read", "report.submit_approval", "approval.review"],
  "status": "active"
}
```

Status codes:
`200 OK`, `401 Unauthorized`, `500 Internal Server Error`.

Error codes:
`unauthorized`, `internal_error`.

##### `GET /api/v1/security/roles`

Purpose:
List the frozen role catalog and the permissions granted by each role.

Response `200 OK`:

```json
{
  "items": [
    {
      "role": "analyst",
      "description": "Creates documents, retrieves context, and submits reports for approval.",
      "permissions": ["document.read", "document.upload", "document.import", "document.chunk", "document.search", "rag.answer", "report.read", "report.submit_approval"]
    }
  ]
}
```

Status codes:
`200 OK`, `401 Unauthorized`, `403 Forbidden`, `500 Internal Server Error`.

Error codes:
`unauthorized`, `forbidden`, `internal_error`.

##### `GET /api/v1/security/permissions`

Purpose:
List the frozen permission catalog and its human-readable meanings.

Response `200 OK`:

```json
{
  "items": [
    {
      "permission": "approval.approve",
      "description": "Approve a pending report revision.",
      "category": "approval"
    }
  ]
}
```

Status codes:
`200 OK`, `401 Unauthorized`, `403 Forbidden`, `500 Internal Server Error`.

Error codes:
`unauthorized`, `forbidden`, `internal_error`.

##### `GET /api/v1/audit-logs`

Purpose:
List append-only audit facts and the derived operation log projection.

Response `200 OK`:

```json
{
  "items": [
    {
      "audit_log_id": "aud-123",
      "operation_type": "approval.approved",
      "actor_id": "approver-1",
      "organization_id": "org-001",
      "department_id": "dept-001",
      "resource_type": "approval",
      "resource_id": "apr-123",
      "result": "success",
      "error_code": null,
      "request_id": "req-123",
      "trace_id": "trace-123",
      "timestamp": "2026-07-05T12:34:56Z",
      "metadata": {}
    }
  ],
  "next_cursor": null
}
```

Status codes:
`200 OK`, `401 Unauthorized`, `403 Forbidden`, `500 Internal Server Error`.

Error codes:
`unauthorized`, `forbidden`, `audit_log_failed`, `internal_error`.

Future audit relationship:

- Audit logs are read-only facts.
- Operation logs are a human-readable projection of the same frozen facts.
- Future write paths may append audit facts, but this contract only freezes the read surface.

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
- `unauthorized`
- `forbidden`
- `permission_denied`
- `role_not_found`
- `invalid_role`
- `audit_log_failed`

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
