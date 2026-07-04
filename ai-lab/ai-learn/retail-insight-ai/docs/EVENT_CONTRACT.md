# Event Contract / 事件契约 / イベント契約

## 1. Scope / 范围 / 範囲

This document freezes SSE event envelope rules.
本文件冻结 SSE 事件封装规范。
本書は SSE イベントの封筒規約を凍結します。

## 2. Current Event Families / 当前事件族 / 現在イベント種別

- `started`
- `status`
- `done`
- `error`

Current families remain frozen for existing task event streams.
当前任务事件流继续冻结为以上事件族。
既存タスクイベントストリームでは上記イベント種別を維持します。

## 2.1 Document Upload Event Families / 文档上传事件族 / 文書アップロードイベント種別

Document upload events are frozen as a separate family and do not replace task SSE events.
文档上传事件族单独冻结，不替代任务 SSE 事件。
文書アップロードイベントは別系統として凍結し、タスク SSE を置き換えません。

- `document.upload.accepted`
- `document.upload.validating`
- `document.upload.storing`
- `document.upload.completed`
- `document.upload.failed`
- `document.upload.duplicate_detected`
- `document.upload.started`
- `document.upload.validated`
- `document.archive.completed`
- `document.import.started`
- `document.import.validated`
- `document.import.completed`
- `document.import.failed`
- `document.chunk.started`
- `document.chunk.completed`
- `document.chunk.failed`
- `document.retrieval.started`
- `document.retrieval.completed`
- `document.retrieval.failed`
- `internal_rag.started`
- `internal_rag.retrieval_completed`
- `internal_rag.answer_generated`
- `internal_rag.failed`
- `document.version.created`
- `document.validation.failed`

## 3. Event Envelope / 事件封装 / イベント封筒

Every event must include the following logical fields:

```json
{
  "version": "v1",
  "event_type": "status",
  "request_id": "req-123",
  "trace_id": "trace-123",
  "task_id": "task-123",
  "status": "running",
  "node": "research",
  "message": "Research step started",
  "payload": {},
  "timestamp": "2026-07-04T12:34:56Z",
  "source": "workflow",
  "error_code": null
}
```

## 4. Required Fields / 必填字段 / 必須フィールド

- `version`
- `event_type`
- `request_id`
- `trace_id`
- `task_id`
- `status`
- `node`
- `message`
- `payload`
- `timestamp`
- `source`
- `error_code`

## 5. Field Rules / 字段规则 / フィールド規則

- `version`: current standard is `v1`.
- `event_type`: one of the frozen event families or a future versioned family.
- `request_id`: HTTP request correlation id.
- `trace_id`: cross-layer execution trace id.
- `task_id`: task business identifier.
- `status`: task or workflow progress state.
- `node`: workflow node or component name.
- `message`: short operator-facing summary.
- `payload`: structured details only; never raw secrets or full confidential documents.
- `timestamp`: ISO 8601 UTC.
- `source`: `api | service | workflow | repository | provider`.
- `error_code`: nullable; required for `error` events.

## 6. Event Type Semantics / 事件语义 / イベント意味

- `started`: task accepted and execution started.
- `status`: intermediate progress update.
- `done`: terminal successful completion.
- `error`: terminal failure or unrecoverable error.

Rule:
After `error`, do not send `done`.
规则：`error` 之后禁止再发送 `done`。
ルール：`error` の後に `done` を送信してはいけません。

### 6.1 Document Upload Event Semantics / 文档上传事件语义 / 文書アップロードイベント意味

- `document.upload.accepted`: upload request accepted and session created.
- `document.upload.validating`: file and metadata validation is in progress.
- `document.upload.storing`: repository save is in progress.
- `document.upload.duplicate_detected`: a duplicate checksum or duplicate session was detected.
- `document.upload.completed`: upload session completed successfully.
- `document.upload.failed`: upload session failed before completion.
- `document.version.created`: the first frozen version record was created.
- `document.validation.failed`: validation failed before the upload could complete.
- `document.upload.started`: upload request accepted and validation began.
- `document.upload.validated`: metadata, type, language, and checksum validation passed.
- `document.archive.completed`: document was soft deleted and preserved for future reads.

### 6.2 Document Import Event Semantics / 文档导入事件语义 / 文書インポートイベント意味

- `document.import.started`: import request accepted and import session created.
- `document.import.validated`: uploaded document passed import eligibility checks.
- `document.import.completed`: document import completed and the document was marked as validated.
- `document.import.failed`: document import failed before completion.

Document import events must keep payloads secret-safe and document-centric.
文档导入事件的 payload 必须安全且以文档为中心。
文書インポートイベントの payload は安全で文書中心でなければなりません。

Document upload events must keep payloads secret-safe and document-centric.
文档上传事件的 payload 必须安全且以文档为中心。
文書アップロードイベントの payload は安全で文書中心でなければなりません。

### 6.3 Document Chunk Event Semantics / 文档切片事件语义 / 文書チャンクイベント意味

- `document.chunk.started`: chunk request accepted and chunk pipeline began.
- `document.chunk.completed`: chunk set was generated or replaced successfully.
- `document.chunk.failed`: chunk pipeline failed before completion.

Document chunk events must keep payloads secret-safe and document-centric.
文档切片事件的 payload 必须安全且以文档为中心。
文書チャンクイベントの payload は安全で文書中心でなければなりません。

### 6.4 Document Retrieval Event Semantics / 文档检索事件语义 / 文書検索イベント意味

- `document.retrieval.started`: retrieval request accepted and ranked search began.
- `document.retrieval.completed`: retrieval finished successfully and results were returned.
- `document.retrieval.failed`: retrieval failed before completion.

Document retrieval events must keep payloads secret-safe and document-centric.
文档检索事件的 payload 必须安全且以文档为中心。
文書検索イベントの payload は安全で文書中心でなければなりません。

### 6.5 Internal RAG Event Semantics / 内部 RAG 事件语义 / 社内 RAG イベント意味

- `internal_rag.started`: internal RAG request accepted and answer flow began.
- `internal_rag.retrieval_completed`: retrieval phase finished and citation candidates are ready.
- `internal_rag.answer_generated`: answer contract was assembled and returned.
- `internal_rag.failed`: internal RAG failed before completion.

Internal RAG events must keep payloads secret-safe, citation-aware, and document-centric.
内部 RAG 事件的 payload 必须安全、可追溯并以文档为中心。
内部 RAG イベントの payload は安全で、追跡可能で、文書中心でなければなりません。

## 7. Versioning Rules / 版本规则 / バージョン規則

- Existing task SSE stream remains compatible with current clients.
- New event families or breaking field changes require a new version.
- Additive payload keys are allowed only when consumers can ignore them safely.

## 8. Trilingual Key Terms / 三语术语 / 三言語用語

| English | 中文（简体） | 日本語 |
|---|---|---|
| Event Type | 事件类型 | イベント種別 |
| Node | 节点 | ノード |
| Payload | 载荷 | ペイロード |
| Trace ID | 跟踪 ID | トレース ID |
| Source | 来源组件 | 送信元 |
| Error Event | 错误事件 | エラーイベント |
| Completion Event | 完成事件 | 完了イベント |

## 9. Text Flow / 纯文本流程 / テキストフロー

```text
HTTP request accepted
│
▼
started event
│
▼
status event(s) from service / workflow / provider
├── recoverable detail stays inside payload
└── unrecoverable failure
    │
    ▼
    error event

Successful path:
status event(s)
│
▼
done event
```

## 10. Validation Checklist / 校验清单 / 検証チェックリスト

1. Does each event carry `request_id` and `trace_id`?
2. Is `error_code` set for `error`?
3. Is `timestamp` UTC ISO 8601?
4. Is `payload` structured and secret-safe?
5. Does the stream avoid `error` followed by `done`?
