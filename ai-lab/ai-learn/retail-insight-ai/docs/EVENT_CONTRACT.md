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

Document upload events must keep payloads secret-safe and document-centric.
文档上传事件的 payload 必须安全且以文档为中心。
文書アップロードイベントの payload は安全で文書中心でなければなりません。

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
