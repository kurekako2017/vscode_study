# 错误目录 / Error Catalog / エラーカタログ

## 范围 / Scope / 範囲

文档上传相关错误码与 UI 行为冻结入口。

## 主要术语 / Key Terms / 主要用語

| English | 中文（简体） | 日本語 |
|---|---|---|
| Error Code | 错误码 | エラーコード |
| Retryable | 可重试 | 再試行可否 |
| Source | 来源 | 発生元 |

## 错误分类 / Categories / 分類

| Code | HTTP | User | Developer | Retryable | Source |
|---|---:|---|---|---|---|
| `missing_title` | 422 | Title is required. | Title missing. | No | validation |
| `empty_file` | 422 | File cannot be empty. | Empty file payload. | No | validation |
| `unsupported_document_type` | 415 | Unsupported document type. | Type outside allowlist. | No | validation |
| `invalid_metadata` | 422 | Metadata is invalid. | Metadata schema failed. | No | validation |
| `duplicate_checksum` | 409 | Same file already uploaded. | Duplicate checksum. | Maybe | upload |
| `idempotency_conflict` | 409 | Retry payload conflicts. | Same key, different checksum. | No | upload |
| `upload_too_large` | 413 | File exceeds allowed size. | Size limit exceeded. | No | validation |
| `unsupported_encoding` | 422 | Encoding not supported. | Safe decode failed. | No | validation |
| `document_not_found` | 404 | Document not found. | Missing document_id. | No | repository |
| `document_archived` | 409 | Document is archived. | Archived state blocks write. | No | approval |
| `repository_error` | 500 | Storage error. | Repository operation failed. | Yes | repository |
| `database_unavailable` | 503 | Database unavailable. | DB layer down. | Yes | database |
| `approval_required` | 409 | Approval required. | Future gate blocked. | No | approval |
| `retrieval_unavailable` | 503 | Retrieval unavailable. | Retrieval layer down. | Yes | retrieval |
| `provider_timeout` | 503 | Processing timed out. | Provider timeout. | Yes | provider |
| `event_publish_failed` | 500 | Progress update failed. | Event publish failed. | Yes | event |

## 导入错误 / Import Errors / インポートエラー

| Code | HTTP | User | Developer | Retryable | Source |
|---|---:|---|---|---|---|
| `document_import_not_found` | 404 | Import record not found. | Requested import_id does not exist. | No | import |
| `import_already_running` | 409 | Another import is already running. | Same document_id already has a running import session. | Maybe | import |
| `document_archived` | 409 | Document is archived. | Archived documents cannot be imported again. | No | import |
| `unsupported_document_type` | 415 | This document type is not supported for import. | Planned-only document type cannot enter import pipeline. | No | import |
| `invalid_metadata` | 422 | Document metadata is invalid. | Import eligibility checks failed. | No | import |

## 切片错误 / Chunk Errors / チャンクエラー

| Code | HTTP | User | Developer | Retryable | Source |
|---|---:|---|---|---|---|
| `document_not_validated` | 409 | Document is not validated yet. | Chunk pipeline requires validated document status. | No | chunk |
| `chunk_failed` | 500 | Document chunking failed. | Chunk generation or persistence failed. | Yes | chunk |

## 检索错误 / Retrieval Errors / 検索エラー

| Code | HTTP | User | Developer | Retryable | Source |
|---|---:|---|---|---|---|
| `invalid_query` | 422 | Query is invalid. | Query text or filters failed validation. | No | retrieval |
| `retrieval_unavailable` | 503 | Retrieval is temporarily unavailable. | Retrieval layer is down or disabled. | Yes | retrieval |
| `repository_error` | 500 | Retrieval storage error. | Repository operation failed during search. | Yes | retrieval |
