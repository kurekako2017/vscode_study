# TEST CASES

English summary: this file maps the existing backend tests to the features they protect and explains which ones are core, which ones are PostgreSQL-related, and which capabilities still lack dedicated tests.
中文（简体）摘要：这份文档把现有 backend tests 对应到功能和风险边界，说明哪些是核心路径、哪些与 PostgreSQL 有关、哪些能力还没有专门测试。
日本語要約：この文書は既存の backend tests を機能とリスク境界に対応付け、どれが核心か、どれが PostgreSQL 関連か、どの能力がまだ専用テストを持たないかを説明します。

## How to Run / 如何运行 / 実行方法

```bash
cd backend
python3 -m unittest discover -s tests -v
python3 -m compileall app tests
```

English: `unittest discover` is the authoritative backend test command for this project.
中文（简体）：`unittest discover` 是本项目后端测试的主命令。
日本語：このプロジェクトの backend テストの主コマンドは `unittest discover` です。

## Test File Inventory

| Test file | What it covers | Core path? | PostgreSQL-related? |
| --- | --- | --- | --- |
| `backend/tests/test_api.py` | task create/status/report/SSE/error envelopes | Yes | No |
| `backend/tests/test_approval_api.py` | approval submit/list/detail/approve/reject/revise and RBAC seams | Yes | No |
| `backend/tests/test_audit_middleware.py` | approval audit middleware success, deny, and failure paths | Yes | No |
| `backend/tests/test_document_upload_api.py` | document upload contract and validation | Yes | No |
| `backend/tests/test_document_read_api.py` | document list/detail and filters | Yes | No |
| `backend/tests/test_document_archive_api.py` | document archive / soft delete behavior | Yes | No |
| `backend/tests/test_document_import_api.py` | document import pipeline and status transitions | Yes | No |
| `backend/tests/test_document_chunk_api.py` | chunk pipeline and stored chunk reads | Yes | No |
| `backend/tests/test_document_retrieval_api.py` | keyword retrieval search and archived filtering | Yes | No |
| `backend/tests/test_internal_rag_api.py` | internal RAG deterministic answer path | Yes | No |
| `backend/tests/test_internal_rag_evaluation.py` | citation quality and evaluation warnings | Yes | No |
| `backend/tests/test_security_audit_api.py` | current user, roles, permissions, audit logs | Yes | No |
| `backend/tests/test_rbac_guard.py` | service-level RBAC allow/deny behavior | Yes | No |
| `backend/tests/test_logging.py` | structured logging fields and safe placeholders | Yes | No |
| `backend/tests/test_file_inputs.py` | local file-backed KPI / research inputs | Yes | No |
| `backend/tests/test_document_domain.py` | document domain model and in-memory repository rules | Yes | No |
| `backend/tests/test_repositories.py` | repository interface boundaries | Yes | No |
| `backend/tests/test_repository_backend_switch.py` | in-memory default vs PostgreSQL backend wiring | Partial | Yes |
| `backend/tests/test_postgres_repositories.py` | PostgreSQL persistence smoke test | Partial | Yes |
| `backend/tests/test_rag_answer_generator.py` | stub LLM provider seam and deterministic fallback | Yes | No |
| `backend/tests/test_settings.py` | environment and settings parsing | Yes | No |

## Core Paths

- Task API chain
- Document upload/read/archive/import/chunk/retrieval chain
- Internal RAG deterministic chain
- Approval submit/review/approve/reject chain
- Security read model and audit read model
- RBAC and audit middleware seams

## PostgreSQL / Environment Related

- `backend/tests/test_repository_backend_switch.py`
- `backend/tests/test_postgres_repositories.py`

These tests are important because they prove the repository abstraction exists, but the real PostgreSQL path is still environment-dependent.

## What `unittest discover` Tells You

- If it passes, the backend API contracts and the core local learning path are stable.
- If exactly one test is skipped for `psycopg`, that is expected in environments without PostgreSQL dependencies.
- If `compileall` passes, the Python modules are syntactically valid.

## What Still Lacks Dedicated Tests

- frontend UI behavior
- browser end-to-end flows
- live uvicorn network smoke in every environment
- real authentication
- JWT/OAuth
- real LLM provider integration
- pgvector
- internet search
- MCP
- production deployment

English: these gaps are intentional for the current phase.
中文（简体）：这些缺口是当前阶段有意保留的边界。
日本語：これらの未実装は現在フェーズで意図的に残している境界です。

