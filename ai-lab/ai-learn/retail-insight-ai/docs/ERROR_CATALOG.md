# Error Catalog / 错误目录 / エラーカタログ

## 1. Scope / 范围 / 範囲

This file freezes document upload related error codes and their operator-facing behavior.
本文件冻结文档上传相关错误码与面向用户的处理方式。
本書は文書アップロード関連のエラーコードと利用者向け挙動を凍結します。

## 2. Key Terms / 关键术语 / 主要用語

| English | 中文（简体） | 日本語 |
|---|---|---|
| Error Code | 错误码 | エラーコード |
| HTTP Status | HTTP 状态码 | HTTP ステータス |
| Retryable | 可重试 | 再試行可否 |
| Source | 来源层 | 発生元 |
| UI Behavior | 界面行为 | UI 挙動 |

## 3. Common Errors / 通用错误 / 共通エラー

| Code | HTTP Status | User Message | Developer Message | Retryable | Source | Future UI Behavior |
|---|---:|---|---|---|---|---|
| `repository_error` | 500 | Temporary storage error. | Repository write or read failed. | Yes | repository | Show retry and support hint |
| `database_unavailable` | 503 | Service temporarily unavailable. | Database or connection layer unavailable. | Yes | database | Show retry later |
| `provider_timeout` | 503 | Processing timed out. | Provider or external dependency timed out. | Yes | provider | Show retry with spinner fallback |
| `event_publish_failed` | 500 | Upload completed, but progress updates failed. | Event publish failed after a state transition. | Yes | event | Show partial completion warning |
| `internal_error` | 500 | Unexpected error occurred. | Unhandled server failure. | No | common | Show generic error screen |

## 4. Validation Errors / 校验错误 / 検証エラー

| Code | HTTP Status | User Message | Developer Message | Retryable | Source | Future UI Behavior |
|---|---:|---|---|---|---|---|
| `missing_title` | 422 | Title is required. | Document title is blank or missing. | No | validation | Highlight title field |
| `empty_file` | 422 | File cannot be empty. | Uploaded file content is empty. | No | validation | Highlight file selector |
| `unsupported_document_type` | 415 | This document type is not supported. | Document type is outside frozen allowlist. | No | validation | Show supported types |
| `invalid_metadata` | 422 | Metadata is invalid. | Metadata payload failed schema or semantic checks. | No | validation | Highlight metadata section |
| `unsupported_encoding` | 422 | File encoding is not supported. | Encoding could not be decoded safely. | No | validation | Show encoding hint |
| `upload_too_large` | 413 | File exceeds the allowed size. | Upload size is above the frozen limit. | No | validation | Show size limit hint |

## 5. Document Upload Errors / 文档上传错误 / 文書アップロードエラー

| Code | HTTP Status | User Message | Developer Message | Retryable | Source | Future UI Behavior |
|---|---:|---|---|---|---|---|
| `duplicate_checksum` | 409 | The same file was already uploaded. | Checksum matched an existing document. | Maybe | upload | Offer open existing document |
| `idempotency_conflict` | 409 | This retry does not match the original upload. | Same idempotency key with different checksum. | No | upload | Ask user to retry with new key |
| `document_not_found` | 404 | Document not found. | Requested document_id does not exist. | No | upload | Show not found screen |
| `document_archived` | 409 | Document is archived. | Operation is blocked by archived state. | No | upload | Show archived badge |
| `document_version_conflict` | 409 | Document version changed. | Version decision conflicts with current state. | Maybe | upload | Show refresh warning |
| `approval_required` | 409 | Approval is required before publish. | Future approval gate blocks the operation. | No | approval | Show approval required state |
| `approval_rejected` | 409 | The document was rejected. | Future approval workflow rejected the document. | No | approval | Show rejected state |

## 6. Document Import Errors / 文档导入错误 / 文書インポートエラー

| Code | HTTP Status | User Message | Developer Message | Retryable | Source | Future UI Behavior |
|---|---:|---|---|---|---|---|
| `document_import_not_found` | 404 | Import record not found. | Requested import_id does not exist. | No | import | Show not found screen |
| `import_already_running` | 409 | Another import is already running. | Same document_id already has a running import session. | Maybe | import | Show running state badge |
| `document_archived` | 409 | Document is archived. | Archived documents cannot be imported again. | No | import | Show archived badge |
| `unsupported_document_type` | 415 | This document type is not supported for import. | Planned-only document type cannot enter import pipeline. | No | import | Show supported types |
| `invalid_metadata` | 422 | Document metadata is invalid. | Import eligibility checks failed. | No | import | Highlight metadata issue |

## 7. Document Chunk Errors / 文档切片错误 / 文書チャンクエラー

| Code | HTTP Status | User Message | Developer Message | Retryable | Source | Future UI Behavior |
|---|---:|---|---|---|---|---|
| `document_not_validated` | 409 | Document is not validated yet. | Chunk pipeline requires validated document status. | No | chunk | Show import required state |
| `chunk_failed` | 500 | Document chunking failed. | Chunk generation or persistence failed. | Yes | chunk | Show retry and support hint |

## 8. Document Retrieval Errors / 文档检索错误 / 文書検索エラー

| Code | HTTP Status | User Message | Developer Message | Retryable | Source | Future UI Behavior |
|---|---:|---|---|---|---|---|
| `invalid_query` | 422 | Query is invalid. | Query text or filters failed validation. | No | retrieval | Highlight query input |
| `retrieval_unavailable` | 503 | Retrieval is temporarily unavailable. | Retrieval layer is down or disabled. | Yes | retrieval | Show retry notice |
| `repository_error` | 500 | Retrieval storage error. | Repository operation failed during search. | Yes | retrieval | Show retry and support hint |

## 9. Retrieval / Database / Event / Provider Errors / 检索 / 数据库 / 事件 / 提供器错误 / 検索 / DB / イベント / プロバイダーエラー

| Code | HTTP Status | User Message | Developer Message | Retryable | Source | Future UI Behavior |
|---|---:|---|---|---|---|---|
| `retrieval_unavailable` | 503 | Retrieval is temporarily unavailable. | Retrieval layer is down or disabled. | Yes | retrieval | Show retry notice |
| `document_not_found` | 404 | Document not found. | Document does not exist in repository. | No | repository | Show empty state |
| `database_unavailable` | 503 | Database is temporarily unavailable. | Database service or connection pool failed. | Yes | database | Show retry later |
| `provider_timeout` | 503 | External processing timed out. | Provider timed out while handling upload. | Yes | provider | Show retry button |
| `event_publish_failed` | 500 | Upload finished with notification issues. | Event publish failed after persistence. | Yes | event | Show partial success warning |

## 10. Internal RAG Errors / 内部 RAG 错误 / 社内 RAG エラー

| Code | HTTP Status | User Message | Developer Message | Retryable | Source | Future UI Behavior |
|---|---:|---|---|---|---|---|
| `invalid_question` | 422 | Question is invalid. | Question text failed validation or was blank. | No | internal_rag | Highlight question input |
| `retrieval_unavailable` | 503 | Retrieval is temporarily unavailable. | Retrieval provider could not produce contexts. | Yes | internal_rag | Show retry notice |
| `insufficient_context` | 422 | Not enough context was found. | Retrieved evidence is insufficient for a grounded answer. | No | internal_rag | Show refine query hint |
| `citation_required` | 400 | Citations are required. | Request disabled the frozen citation requirement. | No | internal_rag | Force citations enabled |
| `provider_timeout` | 503 | Answer generation timed out. | Provider timed out while assembling the answer. | Yes | internal_rag | Show retry button |
| `repository_error` | 500 | Answer storage error. | Repository operation failed during RAG flow. | Yes | internal_rag | Show retry and support hint |

## 11. Retry Guidance / 重试建议 / 再試行ガイド

- Retryable errors should keep the current session state and allow safe retry.
- Non-retryable validation errors should be fixed in the current form before retry.
- Idempotency conflicts should use a new idempotency key only after the payload changes.
