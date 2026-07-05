# retail-insight-ai CHANGELOG

# CHANGELOG

## 2026-07-05 Sprint R3 Learning Guide + Test Case + Interview Docs Optimization

- 统一最短学习路径到 `README.md`、`docs/LEARNING_API_WALKTHROUGH.md`、`CODE_STUDY_GUIDE.md`。
- 新增 `docs/TEST_CASES.md` 和 `docs/INTERVIEW_GUIDE.md`，分别用于测试总览和面试讲解。
- 更新 `README.md`、`RUNBOOK_LOCAL.md`、`VERIFY_CHECKLIST.md`、`CODE_STUDY_GUIDE.md`、`TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`。
- 新文档保留 English / 中文（简体） / 日本語 三语摘要，不把未完成能力写成已完成。
- 本次不新增业务功能，不改 frontend，不接 PostgreSQL，不接真实 LLM，不接 JWT/OAuth，不接 pgvector/MCP。

## 2026-07-05 Sprint R2 Runnable Learning MVP Verification

- 验证 `from app.main import app; print(app.title)` 和 `app.openapi()` 可正常运行。
- 通过 ASGI 直接确认最小可运行路径：health、task、document、pipeline、approval、security、audit。
- 新增 `docs/LEARNING_API_WALKTHROUGH.md`，把 runnable learning 路径收敛成最短学习顺序。
- 更新 `README.md`、`RUNBOOK_LOCAL.md`、`VERIFY_CHECKLIST.md`、`CODE_STUDY_GUIDE.md`、`TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`。
- 本次不新增功能，不改 frontend，不接 PostgreSQL，不接真实 LLM，不接 JWT/OAuth，不接 pgvector/MCP。

## 2026-07-05 Final Wrap-up Sprint: Project Consolidation and Verification

- 本次仅做收口整理和验证，不新增功能，不改 frontend，不接 PostgreSQL，不接真实 LLM，不接 JWT / OAuth。
- `python3 -m unittest discover -s tests -v` 通过，`115` 个测试运行，`1` 个 PostgreSQL 相关测试因当前环境缺少 `psycopg` 跳过。
- `python3 -m compileall app tests` 通过。
- 当前已完成能力、未完成能力和项目边界已整理为三语摘要，并同步到 handbook mirror。
- 当前完成能力包括：Document Upload / Read / Archive / Import / Chunk / Retrieval、Internal RAG without LLM、LLM Provider Stub Seam、Approval Workflow、Approval RBAC、Approval Audit Middleware、Security Domain、InMemory Audit Log。
- 当前未完成能力包括：frontend UI、PostgreSQL repository full migration、real authentication、JWT/OAuth、real LLM provider、pgvector、internet search、MCP、production deployment。

## 2026-07-05 Sprint 11.3 RBAC Enforcement for Approval APIs

- 在现有 `SecurityService` current-user seam 上，只对 approval APIs 强制 RBAC，不扩展到 document / retrieval / RAG / task APIs。
- `POST /api/v1/reports/{task_id}/submit-approval` 现在要求 `report.submit_approval`；`GET /api/v1/approvals`、`GET /api/v1/approvals/{approval_id}` 要求 `approval.review`；`approve`、`reject`、`revise` 分别要求 `approval.approve`、`approval.reject`、`approval.revise`。
- default system admin placeholder user 继续通过所有 approval permission checks。
- permission denied 会写入 append-only audit fact，并以 `permission_denied` 返回 403。
- 新增 backend tests 覆盖允许路径、拒绝路径与 denied audit logging。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/DECISIONS.md`、`docs/ARCHITECTURE.md`、`docs/API_CONTRACT.md` 以及 handbook mirror。
- 本次不修改 frontend、scripts 或 approval response shape。

## 2026-07-05 Sprint 11.2 Security Domain + InMemory Audit MVP

- 新增 security domain models：`User`、`Organization`、`Department`、`Role`、`Permission`、`Policy`。
- 实现 `GET /api/v1/users/me`、`GET /api/v1/security/roles`、`GET /api/v1/security/permissions` 和 `GET /api/v1/audit-logs`。
- 新增 `AuditLog`、`AuditRepository`、`InMemoryAuditRepository` 和 `AuditService`，并把审计写入边界做成 append-only seam。
- current user 使用 `user_id="system"` 的 placeholder principal，roles 预置为 `admin`，permissions 预置为 frozen catalog。
- `audit.log.created` / `audit.log.failed` 作为结构化日志事件记录审计追加成功和失败。
- 新增 backend tests，覆盖系统用户、冻结目录、审计追加、审计只读读取和 append-only 语义。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/DECISIONS.md`、`docs/ARCHITECTURE.md` 以及 handbook mirror。
- 本次仍不实现真实认证、JWT、OAuth、RBAC enforcement、PostgreSQL audit repository 或 frontend 变更。

## 2026-07-05 Sprint 11.1 Enterprise Security Foundation Contract Freeze

- 冻结企业安全基础合同，覆盖 user / organization / department / role / permission / policy 概念。
- 冻结 `GET /api/v1/users/me`、`GET /api/v1/security/roles`、`GET /api/v1/security/permissions`、`GET /api/v1/audit-logs` 的未来读接口边界。
- 冻结 RBAC approval-action matrix、audit log contract、operation log contract 和 future authentication relationship。
- 更新 `docs/API_CONTRACT.md`、`docs/EVENT_CONTRACT.md`、`docs/ERROR_CATALOG.md`、`docs/ARCHITECTURE.md`、`docs/DATABASE.md`、`TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/DECISIONS.md` 以及 handbook mirror。
- 本次不修改 backend、frontend 或 scripts。

## 2026-07-05 Sprint 10.2 Approval API MVP Implementation

- 在 frozen approval contract 上实现 backend-only Approval API MVP。
- 新增 `POST /api/v1/reports/{task_id}/submit-approval`、`GET /api/v1/approvals`、`GET /api/v1/approvals/{approval_id}`、`POST /api/v1/approvals/{approval_id}/approve`、`POST /api/v1/approvals/{approval_id}/reject`、`POST /api/v1/reports/{task_id}/revise`。
- 新增 immutable `ReportVersion`、`ApprovalRequest`、`ApprovalEvent`、InMemory approval repository 和 approval service / router / tests。
- approval submitted / approved / rejected / revised / failed events 进入 backend event trail。
- 继续保持 report / retrieval / internal RAG response contract 不变。
- Approval API / Approval Events / Approval Errors / Approval Architecture sections were checked and supplemented with 中文（简体） / 日本語 summaries where they were still English-only.

## 2026-07-04 Sprint 10.1 follow-up Trilingual Documentation Rule Freeze

- 冻结文档语言政策：所有人类可读项目文档默认采用 English / 中文（简体） / 日本語 三语。
- 明确 English-only 仅允许用于 code identifiers、API paths、class names、environment variables、enum values、error codes 和 event names。
- 更新 `docs/MASTER_PROMPT.md`、`docs/CODING_STANDARD.md`、`docs/DEVELOPMENT_GUIDE.md`、`docs/API_CONTRACT.md`、`docs/EVENT_CONTRACT.md`、`docs/ERROR_CATALOG.md`、`docs/ARCHITECTURE.md`、`TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/DECISIONS.md` 以及 handbook mirror。
- 本次仅冻结规则，不重写旧文档正文。

## 2026-07-04 Sprint 10.1 Approval Workflow Contract Freeze

- 冻结 Approval Workflow contract，覆盖 `submit-approval`、`approvals list/detail`、`approve`、`reject`、`revise` 的 API 边界。
- 冻结 approval state machine：`draft`、`pending_approval`、`approved`、`rejected`、`revised`、`published`、`archived`。
- 冻结 approval events：`approval.submitted`、`approval.approved`、`approval.rejected`、`approval.revised`、`approval.published`、`approval.failed`。
- 冻结 approval error catalog，并明确 report revision relationship、audit relationship、future RBAC relationship。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/API_CONTRACT.md`、`docs/EVENT_CONTRACT.md`、`docs/ERROR_CATALOG.md`、`docs/DATABASE.md`、`docs/ARCHITECTURE.md`、`docs/DECISIONS.md` 以及 handbook mirror。
- 本次不修改 backend、frontend 或 scripts。

## 2026-07-04 Sprint 9.5 LLM Provider Seam Stub MVP

- 新增 `StubLLMProvider` 作为本地 provider stub，不访问 OpenAI、Azure 或任何外部 API。
- 新增 `RAGAnswerGenerator`，并通过 `LLM_PROVIDER=stub` / `INTERNAL_RAG_USE_LLM=false` 控制是否启用 model seam。
- provider failure、timeout、invalid output、missing citation 都回退到 deterministic extractive answer。
- 记录 `provider_name`、`prompt_tokens`、`completion_tokens`、`estimated_cost`、`latency_ms` 占位信息，仅用于内部事件/日志，不暴露到 API response。
- 新增 `backend/tests/test_rag_answer_generator.py`，并确认 backend full suite 与 compileall 已通过。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/DECISIONS.md`、`docs/ARCHITECTURE.md` 以及 handbook mirror。
- 本次不修改 `/api/v1/internal-rag/answer` response contract，不修改 frontend。

## 2026-07-04 Sprint 9.4 LLM Provider Seam Contract Freeze

- 冻结未来 `LLMProvider` interface concept、`RAGAnswerGenerator` concept 以及 prompt input/output contract。
- 冻结 provider error model：`llm_provider_unavailable`、`llm_provider_timeout`、`llm_output_invalid`、`llm_citation_missing`、`llm_cost_limit_exceeded`。
- 明确当前默认仍是 deterministic extractive fallback，不调用 LLM、不调用外部 provider。
- 记录 token / cost / latency tracking placeholders，供未来模型接入时使用。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/DECISIONS.md`、`docs/PROMPT_STANDARD.md`、`docs/AI_AGENT_DESIGN_GUIDE.md`、`docs/ARCHITECTURE.md`、`docs/ERROR_CATALOG.md` 以及 handbook mirror。
- 本次不修改 backend、frontend 或 scripts，且不改变 `/api/v1/internal-rag/answer` response。

## 2026-07-04 Sprint 9.3 Internal RAG Evaluation + Citation Quality MVP

- 新增 internal RAG evaluation service，用于计算 `coverage_score`、`citation_score`、`confidence` 和 warnings。
- 新增 citation quality checker，验证 `document_id` / `chunk_id` / excerpt grounding 关系，并生成 `low_context`、`missing_citation`、`weak_match` warnings。
- `POST /api/v1/internal-rag/answer` 仍保持 backward compatible，对外 response 未增加新字段。
- `extractive` / `summary` 两种 answer mode 继续不调用 LLM、embedding 或 pgvector。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/DECISIONS.md`、`docs/ARCHITECTURE.md` 以及 handbook mirror。
- `python3 -m unittest discover -s tests -v` 与 `python3 -m compileall app tests` 已通过。

## 2026-07-04 Sprint 9.2 Internal RAG MVP without LLM

- 实现 `POST /api/v1/internal-rag/answer`，基于现有 `DocumentRetrievalProvider` 进行 deterministic answer assembly。
- `answer_mode=extractive` 直接组装 top retrieval excerpts，并为使用的每个 excerpt 返回 citation。
- `answer_mode=summary` 采用稳定的本地摘要规则，不调用 LLM、embedding 或 pgvector。
- `invalid_question`、`insufficient_context`、`citation_required`、`archived exclusion` 行为已由 backend tests 覆盖。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/DECISIONS.md`、`docs/ARCHITECTURE.md` 以及 handbook mirror。
- `python3 -m unittest discover -s tests -v` 与 `python3 -m compileall app tests` 已通过。

## 2026-07-04 Sprint 9.1 Internal RAG Contract Freeze

- 冻结 `POST /api/v1/internal-rag/answer`，定义 question / limit / include_archived / document_type / language / tags / answer_mode / require_citations 请求合同。
- 冻结 internal RAG response contract，包含 `answer`、`citations[]`、`retrieval_mode`、`answer_mode`、`confidence`、`warnings[]`。
- 冻结 `internal_rag.started`、`internal_rag.retrieval_completed`、`internal_rag.answer_generated`、`internal_rag.failed` 事件语义。
- 在 `docs/ARCHITECTURE.md` 增加 Internal RAG Flow、Retrieval to Citation Flow、Future LLM Provider Flow、Future Approval Integration Flow。
- 在 `docs/PROMPT_STANDARD.md` 增加 Internal RAG prompt family，在 `docs/ERROR_CATALOG.md` 增加内部 RAG 错误码分组。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/DECISIONS.md` 以及 handbook mirror。
- 本次不实现 RAG、LLM、embedding、pgvector、frontend，且不修改 retrieval API 行为。

## 2026-07-04 Sprint 8.3 Retrieval Repository Abstraction + Worktree Cleanup

- 将 `POST /api/v1/document-retrieval/search` 的实现边界从 raw chunk storage 下沉到 `DocumentRetrievalProvider`。
- 新增 `backend/app/repositories/interfaces/document_retrieval_provider.py` 与 `backend/app/repositories/implementations/in_memory/document_retrieval.py`，并保留当前 `InMemoryKeywordRetrieval` 作为唯一实现。
- `backend/app/services/document_retrieval_service.py` 现在只负责 API、事件和错误边界，不再直接依赖 chunk repository。
- 更新 `backend/app/config/container.py` 以在组合根中装配 retrieval provider。
- 更新 `docs/ARCHITECTURE.md`、`docs/DECISIONS.md`、`TASK.md`、`docs/PROJECT_BACKLOG.md`。
- 检查工作区后未发现额外 untracked chunk 文件，因此无需删除重复产物。
- 本次不改变 API response、不改变 scoring 行为、不引入 RAG、embedding、pgvector、frontend 或 PostgreSQL 搜索后端。

## 2026-07-04 Sprint 8.2 Document Retrieval API MVP Implementation

- 实现 `POST /api/v1/document-retrieval/search`，以 keyword-only 方式在现有 in-memory document chunks 上执行检索。
- 支持 `query`、`limit`、`include_archived`、`document_type`、`language`、`tags`，并返回 `document_id`、`chunk_id`、`chunk_index`、`content_excerpt`、`score`、`source`、`metadata`。
- 新增 `backend/app/api/document_retrieval.py`、`backend/app/services/document_retrieval_service.py`、`backend/app/schemas/document_retrieval_api.py` 与 `backend/tests/test_document_retrieval_api.py`。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/ARCHITECTURE.md`、`docs/DECISIONS.md` 以及 handbook mirror。
- 本次仍不实现 LLM、RAG、embedding、pgvector、hybrid search、frontend 或 PostgreSQL document repository。

## 2026-07-04 Sprint 8.1 Document Retrieval Contract Freeze

- 冻结 `POST /api/v1/document-retrieval/search` 的请求、响应、状态码、错误码、检索事件与错误目录。
- 在 `docs/ARCHITECTURE.md` 增加 Document Retrieval Flow、Source Trace Flow 与 Future RAG Integration Flow。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/DECISIONS.md` 以及 handbook mirror。
- 本次仍不实现 Retrieval API、RAG、embedding、pgvector、hybrid search 或 future approval flow。

## 2026-07-04 Sprint 7 Document Chunk Pipeline MVP

- 实现 `POST /api/v1/documents/{document_id}/chunks` 与 `GET /api/v1/documents/{document_id}/chunks`。
- Chunk pipeline 只接受 validated 文档，只支持 Markdown / Text，并采用 deterministic replace 规则。
- 新增 `backend/app/repositories/interfaces/document_chunk_repository.py`、`backend/app/repositories/implementations/in_memory/document_chunk_repository.py`、`backend/app/services/document_chunk_service.py`、`backend/app/api/document_chunks.py`、`backend/app/schemas/document_chunk_api.py` 与 `backend/tests/test_document_chunk_api.py`。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/API_CONTRACT.md`、`docs/EVENT_CONTRACT.md`、`docs/ERROR_CATALOG.md`、`docs/ARCHITECTURE.md`、`docs/DECISIONS.md` 以及 handbook mirror。
- 本次仍不实现 frontend、RAG、embedding、pgvector、Approval API、PostgreSQL Document Repository、versions、search。

## 2026-07-04 Sprint 6 Document Import Pipeline MVP

- 实现 `POST /api/v1/documents/{document_id}/import` 与 `GET /api/v1/document-imports/{import_id}`。
- 导入流水线支持 pending / running / completed / failed 状态，成功导入会把文档状态推进到 `validated`。
- 对 Markdown / Text / CSV / JSON 允许导入，对 PDF / Word / Excel / Image 作为计划能力返回 `unsupported_document_type`。
- 新增 `backend/app/models/document_import.py`、`backend/app/services/document_import_service.py`、`backend/app/api/document_imports.py`、`backend/app/schemas/document_import_api.py` 与 `backend/tests/test_document_import_api.py`。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/API_CONTRACT.md`、`docs/EVENT_CONTRACT.md`、`docs/ERROR_CATALOG.md`、`docs/DATABASE.md`、`docs/ARCHITECTURE.md`、`docs/DECISIONS.md` 以及 handbook mirror。
- 本次仍不实现 frontend、RAG、embedding、pgvector、Internet Search、Approval API、versions、chunks、PostgreSQL Document Repository。

## 2026-07-04 Sprint 5 Document Archive API MVP

- 实现 `DELETE /api/v1/documents/{document_id}` 的软删除归档语义，不做物理删除。
- archived 文档继续可由 `GET /api/v1/documents/{document_id}` 读取；列表默认排除 archived，并支持 `include_archived=true` 或 `status=archived`。
- 新增 `backend/app/services/document_archive_service.py` 与 `backend/tests/test_document_archive_api.py`，并调整文档领域删除行为为 archive / soft delete。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/API_CONTRACT.md`、`docs/EVENT_CONTRACT.md`、`docs/ARCHITECTURE.md`、`docs/DECISIONS.md` 以及 handbook mirror。
- 本次仍不实现 frontend、RAG、chunking、pgvector、Approval API、versions、chunks、PostgreSQL Document Repository。

## 2026-07-04 Sprint 4 Document Read API MVP

- 实现 `GET /api/v1/documents` 与 `GET /api/v1/documents/{document_id}`。
- 支持 status / document_type / language / tag / owner 基础过滤，并在缺失文档时返回 `document_not_found`。
- 新增 `backend/app/services/document_read_service.py`、`backend/tests/test_document_read_api.py`，并复用现有 `InMemoryDocumentRepository`。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/ARCHITECTURE.md`、`docs/CHANGELOG.md`、`docs/DECISIONS.md` 以及 handbook mirror。
- 本次仍不实现 frontend、RAG、chunking、pgvector、Approval API、DELETE、versions、chunks、PostgreSQL Document Repository。

## 2026-07-04 Sprint 3 Document Upload API MVP Implementation

- 实现 `POST /api/v1/documents` 的同步 MVP。
- 支持 multipart/form-data、metadata JSON、title / description / owner / tags / language 校验、SHA-256 checksum、duplicate checksum detection 和 `Idempotency-Key`。
- 新增 `backend/app/api/documents.py`、`backend/app/services/document_upload_service.py`、`backend/app/schemas/document_api.py` 与 `backend/tests/test_document_upload_api.py`。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/API_CONTRACT.md`、`docs/EVENT_CONTRACT.md`、`docs/CHANGELOG.md`、`docs/DECISIONS.md` 以及 handbook mirror。
- 本次仍不实现 frontend、不实现 RAG、不实现 chunking、不实现 pgvector、不实现 Approval API。

## 2026-07-04 Sprint 2.5 Document Upload Workflow + Error Catalog + Upload Policy Freeze

- 冻结 Document Upload Workflow、Upload Session contract、Idempotency contract、Error Catalog 和 Upload Policy。
- 新增 `docs/ERROR_CATALOG.md` 与 `docs/UPLOAD_POLICY.md`。
- 更新 `docs/API_CONTRACT.md`、`docs/EVENT_CONTRACT.md`、`docs/ARCHITECTURE.md`、`docs/DATABASE.md`、`docs/PROJECT_BACKLOG.md`、`TASK.md`、`ROADMAP.md`、`docs/DECISIONS.md` 以及 handbook mirror。
- 本次仍不实现 Upload API，不修改 backend 业务代码，不修改 frontend。

## 2026-07-04 Sprint 2 Document Upload API Contract Freeze

- 冻结 Document Upload API contract，覆盖 `POST /api/v1/documents`、`GET /api/v1/documents`、`GET /api/v1/documents/{document_id}`、`GET /api/v1/documents/{document_id}/versions`、`GET /api/v1/documents/{document_id}/chunks`、`DELETE /api/v1/documents/{document_id}`。
- 冻结 Document Upload event contract，覆盖 `document.upload.started`、`document.upload.validated`、`document.upload.completed`、`document.upload.failed`、`document.version.created`、`document.validation.failed`。
- 更新 `docs/API_CONTRACT.md`、`docs/EVENT_CONTRACT.md`、`docs/ARCHITECTURE.md`、`docs/DATABASE.md`、`docs/PROJECT_BACKLOG.md`、`TASK.md`、`ROADMAP.md`、`docs/DECISIONS.md` 以及 handbook mirror。
- 本次仍只停留在 Document Domain Model，未实现 Upload API、未修改 backend 业务代码、未修改 frontend。

## 2026-07-04

- 完成 `Sprint 1: Phase 3.1 Document Domain Model`。
- 新增 `backend/app/models/document.py`，定义 Document、DocumentVersion、DocumentChunk placeholder、DocumentMetadata、DocumentSource、DocumentStatus、DocumentType、Language，并复用现有 ApprovalStatus 与 ImportBatch。
- 新增 `backend/app/repositories/interfaces/document_repository.py` 与 `backend/app/repositories/implementations/in_memory/document_repository.py`。
- 新增文档域单元测试，覆盖 Document creation、metadata validation、status transition、Repository CRUD、checksum duplicate detection。
- 更新 `docs/ARCHITECTURE.md`、`docs/PROJECT_BACKLOG.md`、`docs/ROADMAP.md`、`docs/TASK.md`、`docs/DECISIONS.md` 以及 handbook mirror。
- 本次未实现 Upload API、RAG、Chunk、pgvector、Internet Search 或 PostgreSQL Document Repository。

- 完成 `Epic 14: Engineering Standards (Final Freeze)` 文档冻结。
- Master Prompt Summary was added after Epic 14 final freeze.
- 新增 `docs/MASTER_PROMPT.md`，作为唯一 Master Prompt。
- 新增 `docs/CODING_STANDARD.md`、`docs/DEVELOPMENT_GUIDE.md`、`docs/AI_AGENT_DESIGN_GUIDE.md`。
- 新增 `docs/API_CONTRACT.md`、`docs/EVENT_CONTRACT.md`、`docs/PROMPT_STANDARD.md`。
- 在 `docs/ai-agent-retail-handbook-v3/docs/` 新增上述 7 份镜像文档。
- 更新 `ROADMAP.md`、`TASK.md`、`docs/PROJECT_BACKLOG.md`、`docs/ARCHITECTURE.md`、`docs/DECISIONS.md` 记录本次冻结。
- 扩展 `../doc-sync.manifest.json`，新增 `engineering-standards` 同步组。
- 本次未修改 `backend/`、`frontend/`、`scripts/`，未新增业务代码，未修改数据库 schema。

- 新增 `scripts/verify_postgres_phase2.sh`，统一 Phase 2 PostgreSQL 验证入口。
- 该脚本会先检查 `psycopg` 与 Docker，再决定自动启动 `postgres` 容器并执行 `tests.test_postgres_repositories`，或明确输出跳过原因与手动命令。
- 修正 `RUNBOOK_LOCAL.md` 中 PostgreSQL 示例账号口径，统一为 `retail_user / retail_password`。
- README、RUNBOOK、VERIFY_CHECKLIST、CODE_STUDY_GUIDE 补充 PostgreSQL 验证脚本说明。
- 尝试执行 `python3 ../scripts/sync_retail_handbook_docs.py` 刷新外部 handbook，同步因缺少同级 `ai-agent-retail-handbook-v3/README.md` 工作区文件而阻塞。
- 实现 Phase 2：PostgreSQL Persistence MVP 的代码基础。
- 新增 `backend/app/db/connection.py` 与 `backend/app/repositories/postgres/`。
- 新增 `backend/db/schema.sql`、`backend/db/init.sql`。
- 新增 `REPOSITORY_BACKEND=inmemory|postgres`，默认保持 `inmemory`。
- 新增 PostgreSQL 连接配置：
  `POSTGRES_HOST`、`POSTGRES_PORT`、`POSTGRES_DB`、`POSTGRES_USER`、`POSTGRES_PASSWORD`。
- 为 `tasks`、`task_events`、`reports`、`report_versions` 实现 PostgreSQL Repository。
- 为 `data_imports`、`import_errors`、`approval_requests`、`approval_events` 新增 schema 与基础模型预留。
- `reports` 表新增 `approval_status` 字段，当前值仍为 `generated`。
- `docker-compose.yml` 新增 PostgreSQL service。
- 新增 backend switch 测试与 PostgreSQL Repository 集成测试骨架。
- 同步更新 `docs/DATABASE.md`、`docs/ARCHITECTURE.md`、`docs/DECISIONS.md` 以及 handbook 对应文档。
- 修正 Phase 2 状态口径为：
  `Code implemented`
  `InMemory path verified`
  `PostgreSQL schema implemented`
  `PostgreSQL repository tests prepared`
  `PostgreSQL real integration test pending`
  `Status: In Progress / Partially Verified`
- 明确当前环境缺少 Docker CLI、未安装 `psycopg` 到实际运行 venv，因此 PostgreSQL 集成测试被 skip。

- 新增 Phase 1.5：Data Contract Freeze + Approval State Machine Design。
- 新增 `docs/DATA_CONTRACTS.md`，冻结业务 CSV、Research JSON、Documents Markdown 契约。
- 新增 `docs/APPROVAL_WORKFLOW.md`，冻结 `generated / draft / pending_approval / approved / rejected / revised / published / archived` 状态机。
- 新增 `docs/DATABASE.md`，冻结 Phase 2 PostgreSQL 准备项：
  `data_imports`、`import_errors`、`reports`、`report_versions`、`approval_requests`、`approval_events`。
- 新增导入错误模型：
  `missing_file`、`invalid_header`、`invalid_type`、`empty_dataset`、`invalid_json`、`invalid_source`、`unsupported_encoding`。
- 完成 Phase 1 文件化输入实现。
- 新增 `backend/app/data_loaders/` 本地文件加载层。
- KPI 从 `backend/data/business/sales.csv`、`inventory.csv`、`members.csv`、`promotions.csv` 读取并计算。
- Research 从 `backend/data/research/market_trend_2026_06.json` 与 `competitor_summary_2026_06.json` 读取 summary / sources。
- 新增 `backend/data/documents/company_policy_sample.md`，作为后续文档上传与检索输入边界样例。
- Report API 新增 `status` 字段，当前值为 `generated`，并为后续 Approval Workflow 预留 `draft / pending_approval / approved / rejected / revised`。
- 新增文件输入测试、Research JSON 测试、hybrid 报告测试。
- 新增企业架构定位（Architecture Positioning）。
- 明确 `Retail Insight AI` 仍为当前项目名称和仓库名称。
- 明确 `Enterprise Retail Intelligence Platform (ERIP)` 为未来平台化目标，而非当前已实现平台。
- 新增 `Epic 0: Enterprise Platform Architecture Evolution`。
- 新增平台化架构原则：
  Platform First、Domain Driven、Provider Pattern、Repository Pattern、Workflow Driven、Configuration First、Test First、Documentation First、Backward Compatibility。
- 新增目标架构逻辑分层：
  Platform、Domain、Provider、Workflow、Repository、Approval、Documents、Search、Import、Audit、Database、Frontend。
- 新增 Phase 完成的 Definition of Done。
- 新增 `Epic 0` 的 Enterprise Architecture Freeze 设计内容：
  Architecture Freeze、Directory Refactor Design、Repository Abstraction Design、Provider Abstraction Design、Workflow Architecture、Document Pipeline、Business Data Pipeline、Approval Workflow、Database Target Design、Testing Matrix、Documentation Matrix、Epic 0 Deliverables。
- 新增 `Epic 12: Retrieval and RAG Platform`。
- 明确 RAG 包含结构化业务数据检索、社内文档检索、互联网检索，而不只限于社内文档。
- 新增检索层相关架构章节：
  Retrieval Layer Architecture、Business Retrieval Flow、Internal RAG Flow、Internet Search Flow、Context Merge Flow、Citation and Source Trace Flow、Future Hybrid Search Architecture。

## 2026-07-02

- 建立 retail-insight-ai 与 ai-agent-retail-handbook-v3 的跨项目文档同步机制。
- 新增 `../scripts/sync_retail_handbook_docs.py` 与 `../doc-sync.manifest.json`。
- 为 README、TASK、PROJECT_BACKLOG、CHANGELOG、RUNBOOK、CODE_STUDY_GUIDE、VERIFY_CHECKLIST、STUDY_PLAN、ARCHITECTURE 和 DECISIONS 建立同步块维护入口。

## 2026-06-29

- 创建项目永久任务清单机制。
- 更新项目 AGENTS.md。
- 建立开发前检查、开发后更新规则。
- 执行项目状态检查。
- 检查结果概要：五份治理文档完整，项目处于 Phase 2 开发准备阶段；当前仍是 Level 1 本地可运行实现，Document Upload、Chunk Pipeline、Embedding、Vector Search 与 Approval Agent 尚未实现。
- 风险概要：README 与 Backlog 的阶段描述尚未统一，CHANGELOG 尚未完整回溯既有功能，当前 WSL 环境无法使用 Docker CLI；`.env`、虚拟环境、依赖目录和构建产物已被 `.gitignore` 保护且未被 Git 跟踪。
- 升级到 AI-LAB Project Governance V2。
- 新增 `ROADMAP.md`、`docs/ARCHITECTURE.md` 和 `docs/DECISIONS.md`。
- 更新 `AGENTS.md`，开发前增加 Roadmap、Backlog 和 TASK 强制读取顺序。
- 影响文件：AGENTS.md、TASK.md、ROADMAP.md、docs/PROJECT_BACKLOG.md、docs/CHANGELOG.md、docs/ARCHITECTURE.md、docs/DECISIONS.md。

<!-- DOC-SYNC:START group=governance -->
## 文档同步块

- group: `governance`
- file: `retail-insight-ai/docs/CHANGELOG.md`
- self_sha256: `cf9c2939e3369aa13c65a636fb64c44d56b672866b23771cf1dda5f1dbe755b3`
- peers:
- `retail-insight-ai/ROADMAP.md` | sha256=5bf39c8dbde1e5279088478951af2f3c02a4506bcbf3682403b3e45a02846cae | # retail-insight-ai Roadmap / 最后更新：2026-06-29 / ## 当前阶段 / 待根据项目现状确认。
- `retail-insight-ai/TASK.md` | sha256=83a6ef1d9395a1c0026514c5d8fab074fb8428781ab712ad25764c1c82decc05 | # retail-insight-ai 当前任务 / 最后更新：2026-07-02 / ## 当前阶段 / Phase 2: Internal Knowledge Approval Agent
- `retail-insight-ai/docs/PROJECT_BACKLOG.md` | sha256=b1dd8a6cee6a7fc07965026b8aefe8c9c8f08669871abd5ce2b8eb3dc1d5d477 | # retail-insight-ai Project Backlog / 最后更新：2026-07-02 / ## 项目目标 / 构建企业级 Retail Insight AI 平台，包含：
- `ai-agent-retail-handbook-v3/ROADMAP.md` | sha256=8bea54fca33668303cb3ebc6a86e9fb359d814605450746eb7575075bc4600cf | # ai-agent-retail-handbook-v3 Roadmap / 最后更新：2026-06-29 / ## 当前阶段 / 待根据项目现状确认。
- `ai-agent-retail-handbook-v3/TASK.md` | sha256=8375c8be41775af3f492dbc66e69653096db6bcdc4838d411eacf72cd81d5c82 | # 当前任务 / 最后更新：2026-07-02 / ## 当前阶段 / 待确认
- `ai-agent-retail-handbook-v3/docs/PROJECT_BACKLOG.md` | sha256=4b25c1fa793fa7ce50f3cc87341c8136603a8fc0eeae44e3b57dfcfd17f4dfc7 | # 项目总待办清单 / 最后更新：2026-07-02 / ## 项目目标 / 待确认
- `ai-agent-retail-handbook-v3/docs/CHANGELOG.md` | sha256=db921303a94dca1268fc38339f4c13606461269c65ca79c1de024cc1d36601c3 | # CHANGELOG / ## 2026-07-02 / - 建立 ai-agent-retail-handbook-v3 与 retail-insight-ai 的跨项目文档同步机制。 / - 新增 `../scripts/sync_retail_handbook_docs.py` 与 `../doc-sync.manifest.json`。
- `ai-agent-retail-handbook-v3/10_Production_Roadmap.md` | sha256=d904e6883e84c4bb5adda4d7adab4499e1e0f6f5e52bf97f46ecd7150271e64e | # 10_Production_Roadmap / # 目录 / - [1. Roadmap 原则](#1-roadmap-原则) / - [2. Level 1 Demo](#2-level-1-demo)

说明：
- 这个块由 `scripts/sync_retail_handbook_docs.py` 自动维护。
- 只同步这个块，不覆盖各自正文。
- 任一组内文档正文变化时，整组文档的同步块都会一起刷新。
<!-- DOC-SYNC:END group=governance -->
