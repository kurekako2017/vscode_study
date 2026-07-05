# 项目总待办清单

最后更新：2026-07-05

## 项目目标

作为 retail-insight-ai 企业化改造的 handbook 镜像与讲解文档集合，持续同步任务、架构、测试方法、决策和变更历史。

## 当前阶段

Documentation Consolidation Sprint 2

状态：已完成

### Documentation Restore + Safe Merge Sprint

- [x] 补充 handbook 根目录与 `docs` 目录职责说明
- [x] 同步 handbook 镜像侧 `MASTER_PROMPT` 文档规则
- [x] 保留既有内容，仅做补充和合并

### 文档重构 V1

- [x] `README.md` 已重写为项目门户，补齐项目概览、架构、目录、文档导航和验证系统
- [x] `RUNBOOK_LOCAL.md` 已重写为启动与排错指南，补齐每条命令的原因、结果、失败和验证
- [x] `docs/LEARNING_API_WALKTHROUGH.md` 已重写为初学者学习文档，补齐 Swagger、当前学习阶段和时序模板
- [x] `docs/TEST_CASES.md` 已重写为学习导向测试文档，补齐 Swagger / unittest 区别、测试保护的 bug 和能力
- [x] `CODE_STUDY_GUIDE.md` 已重写为固定阅读顺序，明确 `Swagger -> API -> Service -> Repository -> Domain -> Tests`
- [x] `INTERVIEW_GUIDE.md` 继续作为唯一面试文档入口
- [x] 本次仅修改文档，不修改 backend、frontend、scripts、业务逻辑或测试实现

### Documentation Consolidation Sprint 2

- [x] README 增加文档导航中心、初学者/面试/开发维护阅读分组和文档数量控制规则
- [x] `docs/LEARNING_API_WALKTHROUGH.md` 改为主链路接口学习表，补齐下一步和常见失败
- [x] `docs/TEST_CASES.md` 改为测试文件学习表，补齐后端流程和 Swagger/前端流程
- [x] `INTERVIEW_GUIDE.md` 改为中文主导、日语辅助的日本项目面试稿
- [x] `RUNBOOK_LOCAL.md` 补齐项目根目录脚本与 backend 目录 uvicorn 的区分，以及 Swagger / ReDoc / OpenAPI JSON 用法
- [x] `VERIFY_CHECKLIST.md` 增加失败时先看哪个文档
- [x] `CODE_STUDY_GUIDE.md` 补齐推荐阅读文件和下一步看哪里
- [x] `docs/MASTER_PROMPT.md` 增加文档数量控制规则
- [x] 本次仅修改文档，不修改 backend/app、backend/tests、frontend、scripts

### Sprint R3: Learning Guide + Test Case + Interview Docs Optimization

- [x] 最短学习路径已收敛到 `README.md` / `docs/LEARNING_API_WALKTHROUGH.md` / `CODE_STUDY_GUIDE.md`
- [x] `README.md` / `RUNBOOK_LOCAL.md` / `VERIFY_CHECKLIST.md` 已补齐启动命令、Swagger 地址、最小验证命令和常见失败原因
- [x] 新增 `docs/TEST_CASES.md`，整理 backend tests 现状、核心路径和 PostgreSQL 相关测试
- [x] 新增 `INTERVIEW_GUIDE.md`，整理项目背景、架构、职责和面试回答要点
- [x] `docs/LEARNING_API_WALKTHROUGH.md` 已补充最短路径、文档职责与三语言摘要
- [x] backend tests 与 compileall 继续作为收口检查

### Sprint R2: Runnable Learning MVP Verification

- [x] backend import 验证通过
- [x] OpenAPI / Swagger 验证通过
- [x] 最小可运行路径通过 ASGI 验证
- [x] 新增 `docs/LEARNING_API_WALKTHROUGH.md`
- [x] 更新 README / RUNBOOK / VERIFY / CODE_STUDY / TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG
- [x] 不新增功能，不改 frontend，不接 PostgreSQL，不接真实 LLM，不接 JWT/OAuth，不接 pgvector/MCP

### Final Wrap-up Sprint: Project Consolidation and Verification

- [x] 完成收口整理，不新增功能，不改 frontend，不接 PostgreSQL，不接真实 LLM，不接 JWT / OAuth
- [x] 后端单测与编译检查已通过
- [x] 当前已完成能力、未完成能力和项目边界已用三语摘要记录
- [x] handbook mirror 已同步

### Capability Envelope

- English: Document Upload, Document Read, Document Archive, Document Import, Document Chunk, Document Retrieval, Internal RAG without LLM, LLM Provider Stub Seam, Approval Workflow, RBAC for Approval APIs, Approval Audit Middleware, Security Domain, InMemory Audit Log
- 中文（简体）：文档上传、文档读取、文档归档、文档导入、文档切分、文档检索、无 LLM 的内部 RAG、LLM Provider Stub 接缝、审批工作流、审批 API 的 RBAC、审批审计中间件、安全域、InMemory 审计日志
- 日本語：ドキュメントアップロード、ドキュメント読取、ドキュメントアーカイブ、ドキュメントインポート、ドキュメントチャンク、ドキュメント検索、LLM なしの内部 RAG、LLM Provider Stub の接続点、承認ワークフロー、承認 API の RBAC、承認監査ミドルウェア、セキュリティドメイン、InMemory 監査ログ

### Remaining Capabilities

- English: frontend UI, PostgreSQL repository full migration, real authentication, JWT/OAuth, real LLM provider, pgvector, internet search, MCP, production deployment
- 中文（简体）：前端 UI、PostgreSQL 仓库全面迁移、真实认证、JWT/OAuth、真实 LLM 提供方、pgvector、互联网搜索、MCP、生产部署
- 日本語：frontend UI、PostgreSQL リポジトリの完全移行、実認証、JWT/OAuth、実 LLM provider、pgvector、インターネット検索、MCP、本番デプロイ

### Sprint 11.3: RBAC Enforcement for Approval APIs

- [x] submit-approval / approvals list-detail / approve / reject / revise enforce RBAC via current user seam
- [x] default system admin placeholder user passes all approval checks
- [x] denied approval access writes append-only audit facts
- [x] backend tests added for allow / deny paths and denied audit logging
- [x] docs / roadmap / task / changelog / decisions / architecture / handbook mirror synchronized
- [x] backend / frontend / scripts boundary unchanged
- [x] Human-readable documentation is trilingual: English / 中文（简体） / 日本語

### Sprint 11.1: Enterprise Security Foundation Contract Freeze

- [x] user / organization / department / role / permission / policy concepts frozen
- [x] GET /api/v1/users/me contract frozen
- [x] GET /api/v1/security/roles contract frozen
- [x] GET /api/v1/security/permissions contract frozen
- [x] GET /api/v1/audit-logs contract frozen
- [x] RBAC approval-action matrix frozen
- [x] audit log contract and operation log contract frozen
- [x] future authentication relationship documented
- [x] docs and handbook mirror synchronized
- [x] backend / frontend / scripts boundary unchanged
- [x] Human-readable documentation is trilingual: English / 中文（简体） / 日本語

### Sprint 10.2: Approval API MVP Implementation

- [x] POST /api/v1/reports/{task_id}/submit-approval implemented
- [x] GET /api/v1/approvals implemented
- [x] GET /api/v1/approvals/{approval_id} implemented
- [x] POST /api/v1/approvals/{approval_id}/approve implemented
- [x] POST /api/v1/approvals/{approval_id}/reject implemented
- [x] POST /api/v1/reports/{task_id}/revise implemented
- [x] immutable report version snapshot model added
- [x] ApprovalRequest / ApprovalEvent domain models added
- [x] InMemory approval repository added
- [x] approval events emitted and backend tests added
- [x] docs and handbook mirror synchronized
- [x] backend / frontend / scripts boundary unchanged
- [x] Human-readable documentation is trilingual: English / 中文（简体） / 日本語

### Sprint 10.1: Approval Workflow Contract Freeze

- [x] approval domain model frozen
- [x] approval API contract frozen
- [x] approval event contract frozen
- [x] approval error catalog frozen
- [x] approval state transition rules frozen
- [x] report revision relationship / audit relationship / future RBAC relationship documented
- [x] docs and handbook mirror synchronized
- [x] backend / frontend / scripts boundary unchanged
- [x] Human-readable documentation is trilingual: English / 中文（简体） / 日本語

### Sprint 9.5: LLM Provider Seam Stub MVP

- [x] `StubLLMProvider` added as the local no-external-API provider implementation
- [x] `RAGAnswerGenerator` now routes through an optional provider seam
- [x] `LLM_PROVIDER=stub` and `INTERNAL_RAG_USE_LLM=false` defaults added
- [x] provider failure / timeout / invalid output fallback to deterministic answer
- [x] usage / cost / latency placeholder model recorded internally
- [x] default deterministic path remains unchanged
- [x] backend tests added for default path, stub path, fallback, invalid output, and usage placeholders
- [x] backend full suite and compileall pass
- [x] TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS / handbook mirror synchronized
- [x] handbook / backend / frontend / scripts boundary unchanged

## Epic 0: Enterprise Platform Architecture Evolution

### Current State

当前 handbook 仍主要服务于 `Retail Insight AI` 这一零售分析领域参考实现。

### Target State

未来平台目标为：

`Enterprise Retail Intelligence Platform (ERIP)`

### Planned Tasks

- [x] Sprint 10.2 Approval API MVP Implementation
- [x] Sprint 10.1 Approval Workflow Contract Freeze
- [ ] Human-readable documentation is trilingual: English / 中文（简体） / 日本語
- [x] Sprint 9.5 LLM Provider Seam Stub MVP
- [x] Sprint 9.4 LLM Provider Seam Contract Freeze
- [ ] Human-readable documentation is trilingual: English / 中文（简体） / 日本語
- [ ] Architecture Freeze
- [ ] Directory Refactor
- [ ] Repository Abstraction
- [ ] Workflow Abstraction
- [ ] Provider Abstraction
- [ ] Documentation Standard
- [ ] Testing Standard

### Sprint 4: Document Read API MVP

- [x] GET /api/v1/documents implemented
- [x] GET /api/v1/documents/{document_id} implemented
- [x] basic list filters implemented for status / document_type / language / tag / owner
- [x] document_not_found 404 behavior implemented for missing documents
- [x] backend tests added for empty list, upload then list, upload then get, missing document, and filters
- [x] existing upload tests still pass
- [x] Architecture / Task / Roadmap / Backlog / Changelog / Decisions / handbook mirror sync
- [ ] PostgreSQL Document Repository remains design-only
- [ ] DELETE / versions / chunks remain frozen for later phases

### Sprint 5: Document Archive API MVP

- [x] DELETE /api/v1/documents/{document_id} implemented as archive / soft delete
- [x] archived documents remain readable by GET /api/v1/documents/{document_id}
- [x] list default excludes archived unless include_archived=true or status=archived
- [x] backend tests added for archive success, archive missing, archive idempotency, and archived list visibility
- [x] existing upload/read tests still pass
- [x] Architecture / Task / Roadmap / Backlog / Changelog / Decisions / handbook mirror sync
- [ ] PostgreSQL Document Repository remains design-only
- [ ] versions / chunks remain frozen for later phases

### Sprint 6: Document Import Pipeline MVP

- [x] POST /api/v1/documents/{document_id}/import implemented
- [x] GET /api/v1/document-imports/{import_id} implemented
- [x] import status transitions pending / running / completed / failed implemented
- [x] successful import marks document as validated
- [x] backend tests added for markdown/text success, unsupported PDF failure, missing document, archived document, deterministic repeat, status read, and event recording
- [x] existing upload/read/archive tests still pass
- [x] Architecture / Task / Roadmap / Backlog / Changelog / Decisions / handbook mirror sync
- [ ] PostgreSQL Document Repository remains design-only
- [ ] versions / chunks / RAG / embedding / pgvector remain frozen for later phases

### Sprint 7: Document Chunk Pipeline MVP

- [x] POST /api/v1/documents/{document_id}/chunks implemented
- [x] GET /api/v1/documents/{document_id}/chunks implemented
- [x] chunk pipeline requires validated documents and rejects archived / unvalidated / unsupported types
- [x] deterministic replace rule implemented for repeated chunking
- [x] backend tests added for markdown/text success, pre-import rejection, archived rejection, unsupported PDF rejection, stored chunk reads, deterministic repeat, and event recording
- [x] existing upload/read/archive/import tests still pass
- [x] Architecture / Task / Roadmap / Backlog / Changelog / Decisions / handbook mirror sync
- [ ] PostgreSQL Document Repository remains design-only
- [ ] versions / RAG / embedding / pgvector / Approval API remain frozen for later phases

### Sprint 8.1: Document Retrieval Contract Freeze

- [x] POST /api/v1/document-retrieval/search contract frozen
- [x] document.retrieval.started / completed / failed contract frozen
- [x] invalid_query / retrieval_unavailable / repository_error frozen in Error Catalog
- [x] Document Retrieval Flow / Source Trace Flow / Future RAG Integration Flow added to Architecture
- [x] TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS / handbook mirror sync
- [ ] Retrieval implementation remains pending
- [ ] RAG / embedding / pgvector / hybrid search remain frozen for later phases

### Sprint 8.2: Document Retrieval API MVP Implementation

- [x] POST /api/v1/document-retrieval/search implemented
- [x] keyword-only search over existing in-memory document chunks implemented
- [x] empty query returns invalid_query
- [x] archived documents are excluded unless include_archived=true
- [x] deterministic score ordering implemented
- [x] retrieval events started / completed / failed emitted
- [x] backend tests added for success, no match, empty query, archived exclusion, include_archived, and deterministic ordering
- [x] existing upload/read/archive/import/chunk tests still pass
- [x] Architecture / Task / Roadmap / Backlog / Changelog / Decisions / handbook mirror sync
- [x] frozen contract remains unchanged

### Sprint 9.1: Internal RAG Contract Freeze

- [x] `POST /api/v1/internal-rag/answer` contract frozen
- [x] `internal_rag.started` / `internal_rag.retrieval_completed` / `internal_rag.answer_generated` / `internal_rag.failed` frozen
- [x] `invalid_question` / `retrieval_unavailable` / `insufficient_context` / `citation_required` / `provider_timeout` / `repository_error` frozen
- [x] Internal RAG Flow / Retrieval to Citation Flow / Future LLM Provider Flow / Future Approval Integration Flow added to Architecture
- [x] Prompt Standard updated with Internal RAG prompt family
- [x] TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS / handbook mirror updated
- [x] retrieval API behavior unchanged

### Sprint 9.2: Internal RAG MVP without LLM

- [x] `POST /api/v1/internal-rag/answer` implemented on top of `DocumentRetrievalProvider`
- [x] extractive answer assembly uses top retrieval excerpts
- [x] summary mode stays deterministic and does not call an LLM
- [x] citations are returned for every excerpt used in the answer
- [x] `invalid_question` / `insufficient_context` / `citation_required` behavior covered by backend tests
- [x] archived documents are excluded unless `include_archived=true`
- [x] existing retrieval tests still pass
- [x] backend full test suite and compileall pass
- [x] TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS / handbook mirror synchronized
- [x] retrieval API behavior remains unchanged

### Sprint 9.3: Internal RAG Evaluation + Citation Quality MVP

- [x] citation quality checker validates document_id / chunk_id / grounded excerpt
- [x] internal RAG evaluation service computes coverage_score / citation_score / confidence / warnings
- [x] low_context / missing_citation / weak_match warnings are generated internally
- [x] extractive answer has citation_score=1.0 on grounded paths
- [x] summary mode still returns citations
- [x] archived filtering and retrieval API behavior remain unchanged
- [x] backend tests added for evaluation scores, missing citation warning, weak_match, and low_context
- [x] existing retrieval and internal RAG tests still pass
- [x] backend full test suite and compileall pass
- [x] TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS / handbook mirror synchronized
- [x] retrieval API behavior remains unchanged

## Backlog

### Epic 1

- [ ] 项目结构检查

### Epic 2

- [ ] 建立 Phase 完成后的 handbook 同步关闭条件
- [ ] 补齐架构文档必备图示章节
- [ ] 补齐测试用例固定模板
- [ ] 建立 CHANGELOG / DECISIONS 强制同步规则
- [ ] 检查 08_架构图册、09_系统设计书、10_Production_Roadmap 的企业化待完善章节

### Epic 3

- [ ] 明确 Retail Insight AI 与 ERIP 的 Current / Target / Planned 定位
- [ ] 在 handbook 中冻结 Architecture Principles
- [ ] 在 handbook 中写入 Definition of Done

### Epic 12: Retrieval and RAG Platform

- [ ] Business Data Retrieval
- [ ] SQL-based structured retrieval
- [ ] Internal Document Retrieval
- [ ] Internal RAG MVP
- [ ] Document chunk retrieval
- [ ] PostgreSQL keyword search
- [ ] PostgreSQL full-text search planning
- [ ] pgvector planning
- [ ] Hybrid search planning
- [ ] Internet Search Retrieval
- [ ] Retrieval provider interface
- [ ] Context merge strategy
- [ ] Source citation model
- [ ] Reference tracking
- [ ] Hallucination risk control
- [ ] Retrieval evaluation
- [ ] Handbook 文档已同步

### Phase 1: 文件化输入基础

- [x] KPI CSV 输入已同步到 handbook
- [x] Research JSON 输入已同步到 handbook
- [x] Documents Markdown 输入目录已同步到 handbook
- [x] Approval Workflow 状态预留说明已同步到 handbook
- [ ] PostgreSQL 持久化基础

### Phase 1.5: Data Contract Freeze + Approval State Machine Design

- [x] Data Contract 已同步到 handbook
- [x] Import Error Model 已同步到 handbook
- [x] Approval State Machine 已同步到 handbook
- [x] Phase 2 PostgreSQL 准备项已同步到 handbook

### Sprint 1: Phase 3.1 Document Domain Model

- [x] Document Domain Model 已同步到 handbook
- [x] Document Repository Interface 已同步到 handbook
- [x] InMemory Document Repository 已同步到 handbook
- [x] 仅保留正确路径 `backend/app/repositories/implementations/in_memory/document_repository.py`
- [x] 先前出现的重复路径是报告 typo，不是实际误放文件

### Sprint 2: Document Upload API Contract Freeze

- [x] Document Upload API contract 已冻结
- [x] Document Upload event contract 已冻结
- [x] Document Upload Mermaid diagrams 已同步
- [x] DATABASE / ARCHITECTURE / CHANGELOG / DECISIONS / TASK / ROADMAP / handbook mirror 已同步
- [ ] Document Upload API implementation
- [ ] Document Upload persistence implementation
- [ ] Document Upload integration tests

### Sprint 2.5: Document Upload Workflow + Error Catalog + Upload Policy Freeze

- [x] Document Upload Workflow 已冻结
- [x] Upload Session contract 已冻结
- [x] Idempotency contract 已冻结
- [x] 新增 `docs/ERROR_CATALOG.md`
- [x] 新增 `docs/UPLOAD_POLICY.md`
- [x] 更新 handbook mirror 对应文档
- [ ] Document Upload API implementation
- [ ] Upload Session persistence
- [ ] Upload API integration tests

### Sprint 3: Document Upload API MVP

- [x] `POST /api/v1/documents` 已实现
- [x] multipart/form-data 请求、metadata 校验、checksum、重复检测、幂等与事件发布已实现
- [x] backend 单元测试已新增并通过后续验证
- [x] docs / TASK / ROADMAP / CHANGELOG / DECISIONS / handbook mirror 已同步
- [ ] `GET /api/v1/documents` 等后续只读接口仍保持冻结未实现
- [ ] PostgreSQL Document Repository 仍保持设计不实现
- [ ] Upload API 后续扩展（versions / chunks / delete）仍保持冻结

### Sprint 4: Document Read API MVP

- 状态：已实现并待验证。
- 本次完成：
  - [x] 实现 `GET /api/v1/documents`
  - [x] 实现 `GET /api/v1/documents/{document_id}`
  - [x] 实现 status / document_type / language / tag / owner 过滤
  - [x] 实现 `document_not_found` 404 行为
  - [x] 新增 backend 单元测试覆盖空列表、上传后列表、上传后读取、缺失文档和过滤条件
  - [x] existing upload tests still pass
  - [x] 同步 `TASK.md`、`ROADMAP.md`、`docs/ARCHITECTURE.md`、`docs/CHANGELOG.md`、`docs/DECISIONS.md` 以及 handbook mirror
- 后续待办：
  - [ ] `DELETE`、`versions`、`chunks` 接口仍冻结未实现
  - [ ] PostgreSQL Document Repository 仍保持设计不实现

## 技术债

### High

- [ ] handbook 同步门禁尚未形成闭环
- [ ] 测试模板和架构模板仍不完整

## 已知问题

- [ ] 当前 handbook 架构文档仍有治理占位章节
- [ ] 当前 handbook 决策文档尚未覆盖同步治理规则

## 完成记录

### 2026-06-29

- 初始化 Backlog
### 2026-06-29 Governance V2

- [x] 升级到 AI-LAB Project Governance V2
- [x] 建立 Roadmap、Architecture 和 ADR 文档
- [ ] 根据真实代码和项目状态细化 Roadmap 与 Architecture

### 2026-07-02 文档同步器

- [x] 建立 ai-agent-retail-handbook-v3 与 retail-insight-ai 的文档同步映射
- [x] 新增跨项目文档同步脚本 `../../scripts/sync_retail_handbook_docs.py`
- [x] 新增同步清单 `../../doc-sync.manifest.json`

### 2026-07-04 Handbook Sync Governance

- [x] 将主项目 Phase 级 handbook 同步规则映射到 handbook 侧治理文件
- [x] 新增测试用例模板要求
- [x] 新增架构文档必备图示要求
- [x] 新增 CHANGELOG / DECISIONS 强制同步要求

### 2026-07-04 Phase 1 文件化输入实现

- [x] 同步 KPI CSV 输入边界
- [x] 同步 Research JSON 输入边界
- [x] 同步 Document Markdown 输入边界
- [x] 同步 Approval Workflow 状态预留说明

### 2026-07-04 Phase 1.5 Contract Freeze and Approval Design

- [x] 同步 Data Contract Freeze
- [x] 同步 Import Error Model
- [x] 同步 Approval State Machine
- [x] 同步 Phase 2 PostgreSQL 准备项

### 2026-07-04 Phase 2 PostgreSQL Persistence MVP

- [x] 同步 `Code implemented`
- [x] 同步 `InMemory path verified`
- [x] 同步 `PostgreSQL schema implemented`
- [x] 同步 `PostgreSQL repository tests prepared`
- [ ] `PostgreSQL real integration test pending`
- [x] 同步 `Status: In Progress / Partially Verified`
- [x] 同步 `REPOSITORY_BACKEND=inmemory|postgres`
- [x] 同步 PostgreSQL Task / Event / Report Repository 边界
- [x] 同步 `data_imports` / `import_errors` schema 预留
- [x] 同步 `approval_requests` / `approval_events` schema 预留
- [x] 同步默认仍为 `inmemory` 的运行边界

### 2026-07-04 Sprint 8.1 Document Retrieval Contract Freeze

- [x] 同步 `POST /api/v1/document-retrieval/search`
- [x] 同步 `document.retrieval.started`、`document.retrieval.completed`、`document.retrieval.failed`
- [x] 同步 `invalid_query`、`retrieval_unavailable`、`repository_error`
- [x] 同步 Document Retrieval Flow、Source Trace Flow、Future RAG Integration Flow
- [x] 同步主项目与 handbook 的任务、路线图、Backlog、Changelog、决策
- [ ] Retrieval implementation / RAG / embedding / pgvector / hybrid search 留待后续 Sprint

### 2026-07-04 Sprint 8.2 Document Retrieval API MVP Implementation

- [x] 同步 `POST /api/v1/document-retrieval/search` 实现结果
- [x] 同步 keyword-only in-memory chunk search
- [x] 同步 empty query / no match / archived exclusion / include_archived / deterministic ordering 测试
- [x] 保持 frozen contract 不变
- [x] 同步主项目与 handbook 的任务、路线图、Backlog、Changelog、决策

### 2026-07-04 Sprint 9.1 Internal RAG Contract Freeze

- [x] 冻结 `POST /api/v1/internal-rag/answer`
- [x] 冻结 `internal_rag.started`、`internal_rag.retrieval_completed`、`internal_rag.answer_generated`、`internal_rag.failed`
- [x] 冻结 `invalid_question`、`retrieval_unavailable`、`insufficient_context`、`citation_required`、`provider_timeout`、`repository_error`
- [x] 新增 Internal RAG Flow、Retrieval to Citation Flow、Future LLM Provider Flow、Future Approval Integration Flow
- [x] 完成主项目与 handbook 的任务、路线图、Backlog、Changelog、决策同步
- [x] 仅冻结 contract，不实现 RAG、embedding、pgvector、frontend

<!-- DOC-SYNC:START group=governance -->
## 文档同步块

- group: `governance`
- file: `ai-agent-retail-handbook-v3/docs/PROJECT_BACKLOG.md`
- self_sha256: `4b25c1fa793fa7ce50f3cc87341c8136603a8fc0eeae44e3b57dfcfd17f4dfc7`
- peers:
- `retail-insight-ai/ROADMAP.md` | sha256=5bf39c8dbde1e5279088478951af2f3c02a4506bcbf3682403b3e45a02846cae | # retail-insight-ai Roadmap / 最后更新：2026-06-29 / ## 当前阶段 / 待根据项目现状确认。
- `retail-insight-ai/TASK.md` | sha256=83a6ef1d9395a1c0026514c5d8fab074fb8428781ab712ad25764c1c82decc05 | # retail-insight-ai 当前任务 / 最后更新：2026-07-02 / ## 当前阶段 / Phase 2: Internal Knowledge Approval Agent
- `retail-insight-ai/docs/PROJECT_BACKLOG.md` | sha256=b1dd8a6cee6a7fc07965026b8aefe8c9c8f08669871abd5ce2b8eb3dc1d5d477 | # retail-insight-ai Project Backlog / 最后更新：2026-07-02 / ## 项目目标 / 构建企业级 Retail Insight AI 平台，包含：
- `retail-insight-ai/docs/CHANGELOG.md` | sha256=cf9c2939e3369aa13c65a636fb64c44d56b672866b23771cf1dda5f1dbe755b3 | # retail-insight-ai CHANGELOG / ## 2026-07-02 / - 建立 retail-insight-ai 与 ai-agent-retail-handbook-v3 的跨项目文档同步机制。 / - 新增 `../scripts/sync_retail_handbook_docs.py` 与 `../doc-sync.manifest.json`。
- `ai-agent-retail-handbook-v3/ROADMAP.md` | sha256=8bea54fca33668303cb3ebc6a86e9fb359d814605450746eb7575075bc4600cf | # ai-agent-retail-handbook-v3 Roadmap / 最后更新：2026-06-29 / ## 当前阶段 / 待根据项目现状确认。
- `ai-agent-retail-handbook-v3/TASK.md` | sha256=8375c8be41775af3f492dbc66e69653096db6bcdc4838d411eacf72cd81d5c82 | # 当前任务 / 最后更新：2026-07-02 / ## 当前阶段 / 待确认
- `ai-agent-retail-handbook-v3/docs/CHANGELOG.md` | sha256=db921303a94dca1268fc38339f4c13606461269c65ca79c1de024cc1d36601c3 | # CHANGELOG / ## 2026-07-02 / - 建立 ai-agent-retail-handbook-v3 与 retail-insight-ai 的跨项目文档同步机制。 / - 新增 `../scripts/sync_retail_handbook_docs.py` 与 `../doc-sync.manifest.json`。
- `ai-agent-retail-handbook-v3/10_Production_Roadmap.md` | sha256=d904e6883e84c4bb5adda4d7adab4499e1e0f6f5e52bf97f46ecd7150271e64e | # 10_Production_Roadmap / # 目录 / - [1. Roadmap 原则](#1-roadmap-原则) / - [2. Level 1 Demo](#2-level-1-demo)

说明：
- 这个块由 `scripts/sync_retail_handbook_docs.py` 自动维护。
- 只同步这个块，不覆盖各自正文。
- 任一组内文档正文变化时，整组文档的同步块都会一起刷新。
<!-- DOC-SYNC:END group=governance -->
