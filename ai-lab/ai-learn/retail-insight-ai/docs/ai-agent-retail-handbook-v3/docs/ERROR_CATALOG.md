# 错误目录 / Error Catalog / エラーカタログ

## 范围 / Scope / 範囲

文档上传相关错误码与 UI 行为冻结入口。

Human-readable explanations in this catalog are trilingual by default.
本目录中的人类可读说明默认采用三语。
本カタログの人間向け説明は三言語を標準とします。

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

## 审批工作流错误 / Approval Workflow Errors / 承認ワークフローエラー

These error codes are frozen for the approval workflow contract and the report revision relationship.

中文（简体）：
这组错误码固定给审批工作流与报告修订关系使用。它们区分“未找到”“状态冲突”“缺少拒绝原因”和“修订冲突”，便于前端与运维按稳定语义处理。

日本語：
このエラーコード群は承認ワークフローとレポート修正版の関係専用です。未検出、状態競合、拒否理由不足、修正版競合を区別し、UI と運用が安定した意味で扱えるようにします。

| Code | HTTP | User | Developer | Retryable | Source |
|---|---:|---|---|---|---|
| `approval_not_found` | 404 | Approval record not found. | Requested approval_id does not exist. | No | approval |
| `approval_required` | 409 | Approval is required before publishing. | The report cannot be published until approval completes. | No | approval |
| `approval_already_submitted` | 409 | Approval was already submitted. | The current report version already has a pending approval. | No | approval |
| `approval_already_decided` | 409 | Approval was already decided. | The approval record already has a final decision. | No | approval |
| `approval_rejected` | 409 | The report was rejected. | The report version is blocked by a rejection decision. | No | approval |
| `invalid_approval_state` | 409 | Approval state is invalid. | The requested transition is not allowed by the frozen state machine. | No | approval |
| `missing_rejection_reason` | 422 | Rejection reason is required. | Reject request omitted the frozen reason field. | No | approval |
| `report_not_found` | 404 | Report not found. | Requested task_id or report record does not exist. | No | approval |
| `report_revision_conflict` | 409 | Report revision conflict. | The report cannot be revised from the current frozen state. | Maybe | approval |

## 企业安全错误 / Enterprise Security Errors / 企業セキュリティエラー

These error codes are frozen for the future security foundation contract.

中文（简体）：
这一组错误码固定给未来的身份、权限和审计读取合同使用。它们分别覆盖未认证、无权限、角色无效、角色不存在和审计写入失败的边界。

日本語：
このエラーコード群は、将来の認証・認可・監査読み取り契約専用です。未認証、権限不足、ロール無効、ロール未検出、監査書き込み失敗を区別します。

| Code | HTTP | User | Developer | Retryable | Source |
|---|---:|---|---|---|---|
| `unauthorized` | 401 | You must sign in first. | Request lacks a valid authenticated principal. | No | security |
| `forbidden` | 403 | You do not have access. | Authenticated principal lacks access to the resource. | No | security |
| `permission_denied` | 403 | This action is not permitted. | RBAC policy denied the requested action. | No | security |
| `role_not_found` | 404 | Role not found. | Requested role does not exist in the frozen catalog. | No | security |
| `invalid_role` | 422 | Role is invalid. | Role value is not part of the frozen role model. | No | security |
| `audit_log_failed` | 500 | Audit record could not be saved. | Audit log append failed. | Yes | security |

## 内部 RAG 错误 / Internal RAG Errors / 社内 RAG エラー

| Code | HTTP | User | Developer | Retryable | Source |
|---|---:|---|---|---|---|
| `invalid_question` | 422 | Question is invalid. | Question text failed validation or was blank. | No | internal_rag |
| `retrieval_unavailable` | 503 | Retrieval is temporarily unavailable. | Retrieval provider could not produce contexts. | Yes | internal_rag |
| `insufficient_context` | 422 | Not enough context was found. | Retrieved evidence is insufficient for a grounded answer. | No | internal_rag |
| `citation_required` | 400 | Citations are required. | Request disabled the frozen citation requirement. | No | internal_rag |
| `provider_timeout` | 503 | Answer generation timed out. | Provider timed out while assembling the answer. | Yes | internal_rag |
| `repository_error` | 500 | Answer storage error. | Repository operation failed during RAG flow. | Yes | internal_rag |

## Future LLM Provider Errors / 未来 LLM 提供器错误 / 将来の LLM プロバイダーエラー

These error codes are frozen for the future LLM provider seam. The current deterministic path does not emit them yet.

| Code | HTTP | User | Developer | Retryable | Source |
|---|---:|---|---|---|---|
| `llm_provider_unavailable` | 503 | Answer provider is temporarily unavailable. | LLM provider could not be reached or is disabled. | Yes | llm_provider |
| `llm_provider_timeout` | 503 | Answer provider timed out. | LLM provider request exceeded the frozen timeout. | Yes | llm_provider |
| `llm_output_invalid` | 502 | Answer output is invalid. | Provider returned malformed or schema-invalid output. | Yes | llm_provider |
| `llm_citation_missing` | 422 | Citations are required. | LLM answer omitted required grounded citations. | Maybe | llm_provider |
| `llm_cost_limit_exceeded` | 429 | Answer generation budget exceeded. | Token or cost ceiling was reached before completion. | Maybe | llm_provider |

## Internal RAG Warnings / 内部 RAG 警告 / 社内 RAG 警告

The following values are warning signals for internal RAG quality and do not represent new HTTP error codes:

- `low_context`: retrieval coverage is partial or thin.
- `missing_citation`: at least one answer excerpt could not be grounded to a valid citation.
- `weak_match`: citation grounding exists, but the match quality is weak.
