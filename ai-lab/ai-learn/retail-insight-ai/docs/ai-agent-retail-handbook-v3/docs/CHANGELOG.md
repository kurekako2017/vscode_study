# CHANGELOG

## 2026-07-05 Sprint 11.3 RBAC Enforcement for Approval APIs

- 在现有 `SecurityService` current-user seam 上，只对 approval APIs 强制 RBAC，不扩展到 document / retrieval / RAG / task APIs。
- `POST /api/v1/reports/{task_id}/submit-approval` 现在要求 `report.submit_approval`；`GET /api/v1/approvals`、`GET /api/v1/approvals/{approval_id}` 要求 `approval.review`；`approve`、`reject`、`revise` 分别要求 `approval.approve`、`approval.reject`、`approval.revise`。
- default system admin placeholder user 继续通过所有 approval permission checks。
- permission denied 会写入 append-only audit fact，并以 `permission_denied` 返回 403。
- 新增 backend tests 覆盖允许路径、拒绝路径与 denied audit logging。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/DECISIONS.md`、`docs/ARCHITECTURE.md`、`docs/API_CONTRACT.md` 以及 handbook mirror。
- 本次不修改 frontend、scripts 或 approval response shape。

## 2026-07-05 Sprint 11.1 Enterprise Security Foundation Contract Freeze

- 冻结企业安全基础合同，覆盖 user / organization / department / role / permission / policy 概念。
- 冻结 `GET /api/v1/users/me`、`GET /api/v1/security/roles`、`GET /api/v1/security/permissions`、`GET /api/v1/audit-logs` 的未来读接口边界。
- 冻结 RBAC approval-action matrix、audit log contract、operation log contract 和 future authentication relationship。
- 更新 `docs/API_CONTRACT.md`、`docs/EVENT_CONTRACT.md`、`docs/ERROR_CATALOG.md`、`docs/ARCHITECTURE.md`、`TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/DECISIONS.md` 以及 handbook mirror。
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
- 更新 `docs/MASTER_PROMPT.md`、`docs/CODING_STANDARD.md`、`docs/DEVELOPMENT_GUIDE.md`、`docs/API_CONTRACT.md`、`docs/EVENT_CONTRACT.md`、`docs/ERROR_CATALOG.md`、`docs/ARCHITECTURE.md`、`TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/DECISIONS.md`。
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
- 更新 `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/DECISIONS.md`、`docs/ARCHITECTURE.md`。
- 本次不修改 `/api/v1/internal-rag/answer` response contract，不修改 frontend。

## 2026-07-04 Sprint 9.4 LLM Provider Seam Contract Freeze

- 冻结未来 `LLMProvider` interface concept、`RAGAnswerGenerator` concept 以及 prompt input/output contract。
- 冻结 provider error model：`llm_provider_unavailable`、`llm_provider_timeout`、`llm_output_invalid`、`llm_citation_missing`、`llm_cost_limit_exceeded`。
- 明确当前默认仍是 deterministic extractive fallback，不调用 LLM、不调用外部 provider。
- 记录 token / cost / latency tracking placeholders，供未来模型接入时使用。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/DECISIONS.md`、`docs/PROMPT_STANDARD.md`、`docs/AI_AGENT_DESIGN_GUIDE.md`、`docs/ARCHITECTURE.md`、`docs/ERROR_CATALOG.md`。
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
- 更新 handbook 镜像的 `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/ARCHITECTURE.md`、`docs/CHANGELOG.md`、`docs/DECISIONS.md`。
- 本次仍不实现 frontend、RAG、embedding、pgvector、Internet Search、Approval API、versions、chunks、PostgreSQL Document Repository。

## 2026-07-04 Sprint 5 Document Archive API MVP

- 实现 `DELETE /api/v1/documents/{document_id}` 的软删除归档语义，不做物理删除。
- archived 文档继续可由 `GET /api/v1/documents/{document_id}` 读取；列表默认排除 archived，并支持 `include_archived=true` 或 `status=archived`。
- 新增 `backend/app/services/document_archive_service.py` 与 `backend/tests/test_document_archive_api.py`，并调整文档领域删除行为为 archive / soft delete。
- 更新 handbook 镜像的 `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/ARCHITECTURE.md`、`docs/CHANGELOG.md`、`docs/DECISIONS.md`。
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
- 更新 handbook mirror 的 `ARCHITECTURE`、`ROADMAP`、`TASK`、`PROJECT_BACKLOG`、`DECISIONS` 及图册。
- 本次仍不实现 Upload API，不修改 backend 业务代码，不修改 frontend。

## 2026-07-04 Sprint 2 Document Upload API Contract Freeze

- 冻结 Document Upload API contract，覆盖 `POST /api/v1/documents`、`GET /api/v1/documents`、`GET /api/v1/documents/{document_id}`、`GET /api/v1/documents/{document_id}/versions`、`GET /api/v1/documents/{document_id}/chunks`、`DELETE /api/v1/documents/{document_id}`。
- 冻结 Document Upload event contract，覆盖 `document.upload.started`、`document.upload.validated`、`document.upload.completed`、`document.upload.failed`、`document.version.created`、`document.validation.failed`。
- 更新 handbook mirror 的 `ARCHITECTURE`、`ROADMAP`、`TASK`、`PROJECT_BACKLOG`、`DECISIONS` 及图册。
- 本次仍只停留在 Document Domain Model，未实现 Upload API、未修改 backend 业务代码、未修改 frontend。

## 2026-07-04 Epic 14 Engineering Standards Final Freeze

- 同步主项目的 Engineering Standards（Final Freeze）。
- Master Prompt Summary was added after Epic 14 final freeze.
- 新增 handbook 镜像文档：
  `docs/MASTER_PROMPT.md`
  `docs/CODING_STANDARD.md`
  `docs/DEVELOPMENT_GUIDE.md`
  `docs/AI_AGENT_DESIGN_GUIDE.md`
  `docs/API_CONTRACT.md`
  `docs/EVENT_CONTRACT.md`
  `docs/PROMPT_STANDARD.md`
- 同步唯一 Master Prompt、API Contract、SSE Event Contract、Prompt Standard、Coding Standard、Development Guide、AI Agent Design Guide 的冻结结论。
- 同步本次未修改 `backend/`、`frontend/`、`scripts/`，未新增业务代码、未修改数据库 schema 的边界。

## 2026-07-04 Sprint 1 Phase 3.1 Document Domain Model

- 同步主项目的 Document Domain Model。
- 新增 Document、DocumentVersion、DocumentChunk placeholder、DocumentMetadata、DocumentSource、DocumentStatus、DocumentType、Language，并复用现有 ApprovalStatus 与 ImportBatch。
- 新增 DocumentRepository Interface 与 InMemoryDocumentRepository。
- 新增文档域单元测试，覆盖 creation、metadata validation、status transition、Repository CRUD、checksum duplicate detection。
- 同步 `docs/ARCHITECTURE.md`、`ROADMAP.md`、`TASK.md`、`docs/PROJECT_BACKLOG.md`、`docs/DECISIONS.md` 以及 handbook mirror。
- 本次未实现 Upload API、RAG、Chunk、pgvector、Internet Search 或 PostgreSQL Document Repository。

## 2026-07-04 Phase 2 PostgreSQL Persistence MVP

- 同步主项目 PostgreSQL Persistence MVP。
- 同步 Phase 2 状态修正为 `In Progress / Partially Verified`。
- 新增 `REPOSITORY_BACKEND=inmemory|postgres` 说明，默认值仍为 `inmemory`。
- 同步 PostgreSQL Task / Event / Report Repository 边界。
- 同步 `tasks`、`task_events`、`reports`、`report_versions` 表。
- 同步 `data_imports`、`import_errors`、`approval_requests`、`approval_events` 的 schema-only 预留说明。
- 同步 Approval / Import 尚未接入业务 API 的边界。
- 同步当前环境缺少 Docker CLI、未安装 `psycopg` 到实际运行 venv、测试被 skip 的说明。
- 同步 `08_架构图册.md` 三语言化要求与核心图集。

## 2026-07-04 Architecture Positioning

- 新增企业架构定位（Architecture Positioning）。
- 明确 `Retail Insight AI` 保持为当前项目名称。
- 明确 `Enterprise Retail Intelligence Platform (ERIP)` 是未来平台架构目标，不是当前已存在平台。
- 新增 `Epic 0: Enterprise Platform Architecture Evolution`。
- 新增 Architecture Principles。
- 新增 Target Architecture 逻辑分层。
- 新增 Phase 完成的 Definition of Done。
- 同步更新 handbook README、ROADMAP、TASK、PROJECT_BACKLOG、ARCHITECTURE、架构图册、系统设计书、Production Roadmap、Project Structure。

## 2026-07-04 Epic 0 Architecture Freeze

- 新增 Enterprise Architecture Freeze 设计。
- 新增 Directory Refactor Design。
- 新增 Repository Abstraction Design。
- 新增 Provider Abstraction Design。
- 新增 Workflow Architecture、Document Pipeline、Business Data Pipeline、Approval Workflow。
- 新增 Database Target ER Diagram。
- 新增 Testing Matrix 与 Documentation Matrix。
- 新增 Epic 0 Deliverables 清单。

## 2026-07-04 Epic 12 Retrieval and RAG Platform

- 新增 `Epic 12: Retrieval and RAG Platform`。
- 明确 RAG 不只包括社内文档，还包括结构化业务数据检索与互联网检索。
- 新增检索层相关架构章节：
  Retrieval Layer Architecture、Business Retrieval Flow、Internal RAG Flow、Internet Search Flow、Context Merge Flow、Citation and Source Trace Flow、Future Hybrid Search Architecture。

## 2026-07-04 Phase 1 文件化输入实现

- 同步主项目的文件化输入改造。
- KPI 改为从 `backend/data/business/*.csv` 读取并计算。
- Research 改为从 `backend/data/research/*.json` 读取 `summary / sources`。
- 新增 `backend/data/documents/*.md` 输入边界说明。
- 报告当前状态为 `generated`，并预留后续审批状态：
  `draft / pending_approval / approved / rejected / revised`。

## 2026-07-04 Phase 1.5 Contract Freeze and Approval Design

- 同步 Data Contract Freeze。
- 同步 Import Error Model：
  `missing_file`、`invalid_header`、`invalid_type`、`empty_dataset`、`invalid_json`、`invalid_source`、`unsupported_encoding`。
- 同步 Approval State Machine：
  `generated / draft / pending_approval / approved / rejected / revised / published / archived`。
- 同步 Phase 2 PostgreSQL 准备项。

## 2026-07-04

- 新增企业化阶段 handbook 同步治理规则。
- 规定每个 Phase 完成后必须同步更新 handbook 文档。
- 新增测试用例固定模板要求：
  用例目标、前端操作流程、后端处理流程、数据输入来源、预期输出、验收标准、Mermaid 前端流程图、Mermaid 后端流程图。
- 新增架构文档必备图示要求：
  前端流程图、后端流程图、数据流图、数据库 ER 图、LangGraph workflow 图、文档检索流程图、审批 workflow 图、互联网检索流程图。
- 影响文件：
  `TASK.md`
  `ROADMAP.md`
  `docs/PROJECT_BACKLOG.md`
  `docs/ARCHITECTURE.md`
  `docs/DECISIONS.md`
  `08_架构图册.md`
  `09_系统设计书.md`
  `10_Production_Roadmap.md`

## 2026-07-02

- 建立 ai-agent-retail-handbook-v3 与 retail-insight-ai 的跨项目文档同步机制。
- 新增 `../scripts/sync_retail_handbook_docs.py` 与 `../doc-sync.manifest.json`。
- 为 README、PROJECT_BIBLE、01-12 全部章节、ROADMAP、TASK、PROJECT_BACKLOG、CHANGELOG、ARCHITECTURE 和 DECISIONS 建立同步块维护入口。

## 2026-06-29

- 初始化项目治理体系
- 创建 AGENTS.md
- 创建 TASK.md
- 创建 PROJECT_BACKLOG.md
- 升级到 AI-LAB Project Governance V2。
- 新增 `ROADMAP.md`、`docs/ARCHITECTURE.md` 和 `docs/DECISIONS.md`。
- 更新 `AGENTS.md`，开发前增加 Roadmap、Backlog 和 TASK 强制读取顺序。
- 影响文件：AGENTS.md、TASK.md、ROADMAP.md、docs/PROJECT_BACKLOG.md、docs/CHANGELOG.md、docs/ARCHITECTURE.md、docs/DECISIONS.md。

<!-- DOC-SYNC:START group=governance -->
## 文档同步块

- group: `governance`
- file: `ai-agent-retail-handbook-v3/docs/CHANGELOG.md`
- self_sha256: `db921303a94dca1268fc38339f4c13606461269c65ca79c1de024cc1d36601c3`
- peers:
- `retail-insight-ai/ROADMAP.md` | sha256=5bf39c8dbde1e5279088478951af2f3c02a4506bcbf3682403b3e45a02846cae | # retail-insight-ai Roadmap / 最后更新：2026-06-29 / ## 当前阶段 / 待根据项目现状确认。
- `retail-insight-ai/TASK.md` | sha256=83a6ef1d9395a1c0026514c5d8fab074fb8428781ab712ad25764c1c82decc05 | # retail-insight-ai 当前任务 / 最后更新：2026-07-02 / ## 当前阶段 / Phase 2: Internal Knowledge Approval Agent
- `retail-insight-ai/docs/PROJECT_BACKLOG.md` | sha256=b1dd8a6cee6a7fc07965026b8aefe8c9c8f08669871abd5ce2b8eb3dc1d5d477 | # retail-insight-ai Project Backlog / 最后更新：2026-07-02 / ## 项目目标 / 构建企业级 Retail Insight AI 平台，包含：
- `retail-insight-ai/docs/CHANGELOG.md` | sha256=cf9c2939e3369aa13c65a636fb64c44d56b672866b23771cf1dda5f1dbe755b3 | # retail-insight-ai CHANGELOG / ## 2026-07-02 / - 建立 retail-insight-ai 与 ai-agent-retail-handbook-v3 的跨项目文档同步机制。 / - 新增 `../scripts/sync_retail_handbook_docs.py` 与 `../doc-sync.manifest.json`。
- `ai-agent-retail-handbook-v3/ROADMAP.md` | sha256=8bea54fca33668303cb3ebc6a86e9fb359d814605450746eb7575075bc4600cf | # ai-agent-retail-handbook-v3 Roadmap / 最后更新：2026-06-29 / ## 当前阶段 / 待根据项目现状确认。
- `ai-agent-retail-handbook-v3/TASK.md` | sha256=8375c8be41775af3f492dbc66e69653096db6bcdc4838d411eacf72cd81d5c82 | # 当前任务 / 最后更新：2026-07-02 / ## 当前阶段 / 待确认
- `ai-agent-retail-handbook-v3/docs/PROJECT_BACKLOG.md` | sha256=4b25c1fa793fa7ce50f3cc87341c8136603a8fc0eeae44e3b57dfcfd17f4dfc7 | # 项目总待办清单 / 最后更新：2026-07-02 / ## 项目目标 / 待确认
- `ai-agent-retail-handbook-v3/10_Production_Roadmap.md` | sha256=d904e6883e84c4bb5adda4d7adab4499e1e0f6f5e52bf97f46ecd7150271e64e | # 10_Production_Roadmap / # 目录 / - [1. Roadmap 原则](#1-roadmap-原则) / - [2. Level 1 Demo](#2-level-1-demo)

说明：
- 这个块由 `scripts/sync_retail_handbook_docs.py` 自动维护。
- 只同步这个块，不覆盖各自正文。
- 任一组内文档正文变化时，整组文档的同步块都会一起刷新。
<!-- DOC-SYNC:END group=governance -->
