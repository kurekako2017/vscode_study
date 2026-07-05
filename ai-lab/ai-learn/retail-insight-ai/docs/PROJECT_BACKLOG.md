# retail-insight-ai Project Backlog

最后更新：2026-07-05

## 项目目标

构建企业级 Retail Insight AI 平台，包含：

- RAG 知识库检索
- Internal Knowledge Approval Agent
- 多 Agent 协作
- MCP 集成
- 企业权限控制
- AI 分析报告生成

## 每次工作开始前必须检查

- [ ] 阅读 AGENTS.md
- [ ] 阅读 docs/PROJECT_BACKLOG.md
- [ ] 阅读 TASK.md（如果存在）
- [ ] 检查未完成任务
- [ ] 检查技术债
- [ ] 确认本次要继续的最高优先级任务

## 每次工作完成后必须更新

- [ ] 更新任务状态
- [ ] 将完成项从 [ ] 改为 [x]
- [ ] 更新最后更新时间
- [ ] 追加完成记录
- [ ] 如果发现新任务，追加到 Backlog

## 当前阶段

Sprint R3: Learning Guide + Test Case + Interview Docs Optimization

状态：已完成

### Sprint R3: Learning Guide + Test Case + Interview Docs Optimization

- [x] 最短学习路径已收敛到 `README.md` / `docs/LEARNING_API_WALKTHROUGH.md` / `CODE_STUDY_GUIDE.md`
- [x] `README.md` / `RUNBOOK_LOCAL.md` / `VERIFY_CHECKLIST.md` 已补齐启动命令、Swagger 地址、最小验证命令和常见失败原因
- [x] 新增 `docs/TEST_CASES.md`，整理 backend tests 现状、核心路径和 PostgreSQL 相关测试
- [x] 新增 `docs/INTERVIEW_GUIDE.md`，整理项目背景、架构、职责和面试回答要点
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

### Sprint 11.2: Security Domain + InMemory Audit MVP

- [x] user / organization / department / role / permission / policy domain models added
- [x] GET /api/v1/users/me implemented with system placeholder principal
- [x] GET /api/v1/security/roles implemented with frozen static role catalog
- [x] GET /api/v1/security/permissions implemented with frozen static permission catalog
- [x] append-only AuditLog model added
- [x] InMemoryAuditRepository added
- [x] GET /api/v1/audit-logs implemented
- [x] audit.log.created / audit.log.failed structured logging recorded on append success/failure
- [x] backend tests added for security read APIs and audit append-only behavior
- [x] backend compileall and unittest discover passed
- [x] docs / roadmap / task / changelog / decisions / architecture updated
- [x] handbook mirror synchronized
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
- [x] backend / frontend / scripts boundary unchanged

### Sprint 9.4: LLM Provider Seam Contract Freeze

- [x] `LLMProvider` interface concept frozen
- [x] `RAGAnswerGenerator` concept frozen
- [x] prompt input/output contract frozen for future model-backed answers
- [x] provider error model frozen for unavailable / timeout / invalid output / citation missing / cost limit cases
- [x] deterministic extractive fallback remains the current default
- [x] token / cost / latency tracking placeholders documented
- [x] `docs/PROMPT_STANDARD.md` / `docs/AI_AGENT_DESIGN_GUIDE.md` / `docs/ARCHITECTURE.md` / `docs/ERROR_CATALOG.md` updated
- [x] TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS / handbook mirror synchronized
- [x] backend / frontend / scripts left untouched

## Epic 0: Enterprise Platform Architecture Evolution

### Current State

当前项目名称保持为 `Retail Insight AI`，项目仍是零售分析领域参考实现，平台级抽象尚未冻结。

### Target State

未来目标平台名称：

`Enterprise Retail Intelligence Platform (ERIP)`

ERIP 仅表示目标平台架构，不表示当前项目、当前部署或当前目录已经完成平台化。

### Planned Tasks

- [x] Sprint 10.2 Approval API MVP Implementation
- [x] Sprint 10.1 Approval Workflow Contract Freeze
- [ ] Human-readable documentation is trilingual: English / 中文（简体） / 日本語
- [ ] Architecture Freeze
- [ ] Directory Refactor
- [ ] Repository Abstraction
- [ ] Workflow Abstraction
- [ ] Provider Abstraction
- [ ] Documentation Standard
- [ ] Testing Standard

### Epic 14: Engineering Standards (Final Freeze)

- [x] 冻结唯一 Master Prompt
- [x] 冻结 API Contract
- [x] 冻结 SSE Event Contract
- [x] 冻结 Prompt Standard
- [x] 冻结 Coding Standard
- [x] 冻结 Development Guide
- [x] 冻结 AI Agent Design Guide
- [x] 建立 handbook 镜像文档
- [x] 扩展文档同步清单
- [ ] 后续 Phase 在新增能力时按冻结文档执行一致性审查
- [ ] Human-readable documentation is trilingual: English / 中文（简体） / 日本語

### Epic 0 Deliverables

- [ ] Architecture Freeze
- [ ] Directory Freeze
- [ ] Repository Freeze
- [ ] Provider Freeze
- [ ] Workflow Freeze
- [ ] Database Freeze
- [ ] Testing Freeze
- [ ] Documentation Freeze

### Sprint 1: Phase 3.1 Document Domain Model

- [x] Document / DocumentVersion / DocumentChunk placeholder / DocumentMetadata / DocumentSource
- [x] DocumentStatus / DocumentType / Language / ApprovalStatus reuse
- [x] DocumentRepository Interface
- [x] InMemoryDocumentRepository
- [x] Document creation / metadata validation / status transition / CRUD / checksum duplicate tests
- [x] Architecture / Roadmap / TASK / CHANGELOG / DECISIONS / handbook mirror sync
- [ ] Document Upload API design only, no implementation yet
- [ ] PostgreSQL Document Repository design only, no implementation yet
- [ ] RAG pipeline design based on the frozen document domain model

## 工作区规则继承

本项目继承 ai-lab 全局项目管理规则。

每次开发前必须检查：

- AGENTS.md
- docs/PROJECT_BACKLOG.md
- TASK.md

每次开发后必须更新：

- docs/PROJECT_BACKLOG.md
- TASK.md
- docs/CHANGELOG.md

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

### Sprint 8.3: Retrieval Repository Abstraction + Worktree Cleanup

- [x] `DocumentRetrievalService` depends on `DocumentRetrievalProvider`
- [x] `InMemoryKeywordRetrieval` keeps current keyword scoring and ordering behavior
- [x] POST /api/v1/document-retrieval/search response shape unchanged
- [x] `git status` confirmed no untracked chunk files
- [x] current retrieval boundary documented in Architecture / Decisions / Changelog / Task
- [x] existing retrieval tests remain expected to pass after abstraction change
- [ ] future PostgreSQL full-text / hybrid search backend remains to be planned

### Sprint 9.1: Internal RAG Contract Freeze

- [x] `POST /api/v1/internal-rag/answer` contract frozen
- [x] `internal_rag.started` / `internal_rag.retrieval_completed` / `internal_rag.answer_generated` / `internal_rag.failed` frozen
- [x] `invalid_question` / `retrieval_unavailable` / `insufficient_context` / `citation_required` / `provider_timeout` / `repository_error` frozen
- [x] Internal RAG Flow / Retrieval to Citation Flow / Future LLM Provider Flow / Future Approval Integration Flow added to Architecture
- [x] Prompt Standard updated with Internal RAG prompt family
- [x] TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS / handbook mirror updated
- [x] retrieval API behavior unchanged

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

## 当前近期优先级

### Enterprise Priority

- [x] Sprint 9.5 LLM Provider Seam Stub MVP
- [x] Sprint 9.4 LLM Provider Seam Contract Freeze
- [x] Sprint 9.3 Internal RAG Evaluation + Citation Quality MVP
- [x] Sprint 9.2 Internal RAG MVP without LLM
- [x] Sprint 9.1 Internal RAG Contract Freeze
- [x] Sprint 8.3 Retrieval Repository Abstraction + Worktree Cleanup
- [x] Sprint 8.2 Document Retrieval API MVP Implementation
- [x] Sprint 8.1 Document Retrieval Contract Freeze
- [ ] 第一优先级：文件化输入（CSV / JSON / Markdown）+ PostgreSQL 持久化基础
- [ ] 明确文件输入目录结构、样例数据规范、版本字段与加载边界
- [ ] 明确 PostgreSQL 持久化表结构、迁移方案与 Repository 替换策略
- [ ] 明确本地最小可行运行方案，不依赖真实外部服务
- [ ] 明确 Phase 完成后的 handbook 文档同步清单与验收标准
- [ ] 明确 Retail Insight AI 与 ERIP 的 Current / Target / Planned 定位边界
- [ ] 明确 Retrieval and RAG Platform 的横向能力边界

### P0

- [ ] 确认项目目录结构
- [ ] 确认 Docker 环境
- [ ] 确认 .gitignore 敏感文件保护
- [ ] 确认 Document Upload 流程

### P1

- [ ] Chunk Strategy 设计
- [ ] Chunk Size 配置化
- [ ] Overlap 配置化
- [ ] Chunk 可视化调试页面

### P2

- [ ] Embedding Pipeline
- [ ] Vector Search
- [ ] Approval Agent

## Backlog

### Epic 1: 项目基础架构

- [ ] 确认 monorepo 结构
- [ ] 确认 frontend/backend 目录
- [ ] 确认 Docker 环境
- [ ] 确认 .gitignore 是否保护敏感文件

### Epic 2: Internal Knowledge Approval Agent

- [ ] Document Upload 流程确认
- [ ] Chunk Strategy 设计
- [ ] Chunk Size 配置化
- [ ] Overlap 配置化
- [ ] Chunk 可视化调试页面
- [ ] Chunk 单元测试
- [ ] Embedding Service 设计
- [ ] Vector Search 设计
- [ ] Approval Agent 设计
- [ ] 审批日志设计

### Epic 3: RAG Platform

- [ ] Query Rewrite
- [ ] Hybrid Search
- [ ] Rerank
- [ ] Context Builder
- [ ] Citation 支持

### Epic 4: Multi-Agent

- [ ] Research Agent
- [ ] Knowledge Agent
- [ ] Approval Agent
- [ ] Report Agent
- [ ] Supervisor Agent

### Epic 5: MCP Integration

- [ ] MCP Server
- [ ] MCP Client
- [ ] Tool Registry
- [ ] Permission Layer

### Epic 6: Enterprise Security

- [x] Enterprise Security Foundation Contract Freeze
- [ ] RBAC
- [ ] JWT
- [ ] Audit Log
- [ ] Tenant Isolation

### Epic 7: Observability

- [ ] LangSmith / Langfuse 调研
- [ ] OpenTelemetry
- [ ] Metrics Dashboard
- [ ] Cost Tracking

### Epic 8: Enterprise Delivery Plan

- [x] Phase 1 文件化输入基础
- [x] Phase 1.5 Data Contract Freeze + Approval State Machine Design
- [x] Phase 1.6 Enterprise Security Foundation Contract Freeze
- [ ] Phase 2 PostgreSQL 持久化基础
- [ ] Phase 3 社内文档上传与入库
- [ ] Phase 4 切分与检索基础
- [ ] Phase 5 审批 Workflow
- [ ] Phase 6 互联网检索能力
- [ ] Phase 7 LangChain + LangGraph 工作流整合
- [ ] Phase 8 测试体系与流程图文档

### Epic 12: Retrieval and RAG Platform

说明：

当前将 Epic 12 作为横向平台能力，不表示当前已经实现完整 RAG 平台。

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

## Phase 1 到 Phase 8 详细计划

### Phase 1.5: Data Contract Freeze + Approval State Machine Design

- 状态：已完成文档冻结。
- 本次完成：
  - [x] 冻结业务 CSV 字段契约
  - [x] 冻结 Research JSON 字段契约
  - [x] 冻结 Documents Markdown 当前边界与未来导入规则
  - [x] 冻结导入错误模型
  - [x] 冻结 Approval State Machine
  - [x] 冻结 Phase 2 PostgreSQL 准备项
- 后续待办：
  - [ ] 将导入错误模型映射到真实 Repository
  - [ ] 将审批状态机映射到真实 API / Repository / Event
  - [ ] 将数据契约映射到 PostgreSQL schema version 策略

### Sprint 2: Document Upload API Contract Freeze

- 状态：已完成文档冻结。
- 本次完成：
  - [x] 冻结 `POST /api/v1/documents`、`GET /api/v1/documents`、`GET /api/v1/documents/{document_id}`、`GET /api/v1/documents/{document_id}/versions`、`GET /api/v1/documents/{document_id}/chunks`、`DELETE /api/v1/documents/{document_id}`
  - [x] 冻结 `document.upload.started`、`document.upload.validated`、`document.upload.completed`、`document.upload.failed`、`document.version.created`、`document.validation.failed`
  - [x] 冻结 Document Upload Validation Flow 与 Future Approval Integration Flow
  - [x] 同步 `TASK.md`、`ROADMAP.md`、`docs/ARCHITECTURE.md`、`docs/DATABASE.md`、`docs/CHANGELOG.md`、`docs/DECISIONS.md` 以及 handbook mirror
- 后续待办：
  - [ ] 实现 Upload API
  - [ ] 实现 Document Upload persistence
  - [ ] 补齐 Upload API integration tests

### Sprint 2.5: Document Upload Workflow + Error Catalog + Upload Policy Freeze

- 状态：已完成文档冻结。
- 本次完成：
  - [x] 冻结 Document Upload Workflow
  - [x] 冻结 Upload Session contract
  - [x] 冻结 Idempotency contract
  - [x] 新增 `docs/ERROR_CATALOG.md`
  - [x] 新增 `docs/UPLOAD_POLICY.md`
  - [x] 同步 `TASK.md`、`ROADMAP.md`、`docs/ARCHITECTURE.md`、`docs/DATABASE.md`、`docs/CHANGELOG.md`、`docs/DECISIONS.md` 以及 handbook mirror
- 后续待办：
  - [ ] 实现 Upload API
  - [ ] 实现 Upload Session persistence
  - [ ] 实现 Upload API integration tests

### Sprint 3: Document Upload API MVP

- 状态：已实现并待验证。
- 本次完成：
  - [x] 实现 `POST /api/v1/documents`
  - [x] 实现 multipart/form-data 请求处理
  - [x] 实现 title / description / owner / tags / language 校验
  - [x] 实现 SHA-256 checksum、duplicate checksum detection、Idempotency-Key 处理
  - [x] 实现 `DocumentUploadSession` 成功响应
  - [x] 实现 upload 事件发布到现有 event repository
  - [x] 新增 backend 单元测试覆盖成功、空文件、类型不支持、缺少标题、重复 checksum、幂等重放与幂等冲突
  - [x] 同步 `TASK.md`、`ROADMAP.md`、`docs/ARCHITECTURE.md`、`docs/API_CONTRACT.md`、`docs/EVENT_CONTRACT.md`、`docs/CHANGELOG.md`、`docs/DECISIONS.md` 以及 handbook mirror
- 后续待办：
  - [ ] 实现 GET / DELETE / versions / chunks 只读接口
  - [ ] 保持 PostgreSQL Document Repository 仅设计不实现
  - [ ] 补齐 Upload API integration tests 的真实联调验证

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

### Phase 2: PostgreSQL Persistence MVP

- 状态：In Progress / Partially Verified。
- 本次完成：
  - [x] Code implemented
  - [x] InMemory path verified
  - [x] PostgreSQL schema implemented
  - [x] PostgreSQL repository tests prepared
  - [x] PostgreSQL verification script added
  - [x] 新增 `REPOSITORY_BACKEND=inmemory|postgres` 配置开关，默认仍为 `inmemory`
  - [x] 新增 PostgreSQL 连接工厂与 UTC 会话设置
  - [x] 新增 `tasks`、`task_events`、`reports`、`report_versions` 表
  - [x] 新增 `data_imports`、`import_errors` schema 预留
  - [x] 新增 `approval_requests`、`approval_events` schema 预留
  - [x] 新增 PostgreSQL Repository 与 backend switch 测试
  - [x] 新增 `scripts/verify_postgres_phase2.sh`，统一输出依赖检查、跳过原因与手动验证命令
  - [x] 同步主项目与 handbook 文档
- 后续待办：
  - [ ] PostgreSQL real integration test pending
  - [ ] 在具备 PostgreSQL 环境后执行真实集成测试
  - [x] 记录当前环境缺少 Docker CLI、未安装 `psycopg` 到实际运行 venv、测试被 skip 的验证边界
  - [ ] 在具备同级 `ai-agent-retail-handbook-v3/` 工作区后执行 `python3 ../scripts/sync_retail_handbook_docs.py`
  - [ ] 实现 data imports / import errors Repository
  - [ ] 将 reports approval status 接入真实审批状态流转
  - [ ] 为 Phase 3 文档入库与 Phase 5 审批 API 复用当前 schema

## Handbook 同步治理规则

- 每个 Phase 完成后，必须同步更新 `docs/ai-agent-retail-handbook-v3/` 对应文档。
- handbook 同步最小集合：
  `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/ARCHITECTURE.md`、`docs/CHANGELOG.md`、`docs/DECISIONS.md`。
- 若变更涉及测试、流程、系统设计、生产路线图，还必须同步检查并更新：
  `08_架构图册.md`、`09_系统设计书.md`、`10_Production_Roadmap.md`。
- 未同步 handbook 文档的 Phase 不得从 `[ ]` 改为 `[x]`。
- 所有功能变更必须追加到 handbook 侧：
  `docs/ai-agent-retail-handbook-v3/docs/CHANGELOG.md`
  `docs/ai-agent-retail-handbook-v3/docs/DECISIONS.md`

## 本次完成记录

### 2026-07-04

- 完成 Epic 14：Engineering Standards（Final Freeze）文档冻结。
- 新增 Master Prompt、API / Event Contract、Prompt Standard、Coding Standard、Development Guide、AI Agent Design Guide。
- 在 `docs/ai-agent-retail-handbook-v3/docs/` 建立对应镜像。
- 将 `../doc-sync.manifest.json` 扩展为包含 `engineering-standards` 同步组。
- 未修改 `backend/`、`frontend/`、`scripts/`。

### 2026-07-04 Sprint 1 Phase 3.1 Document Domain Model

- [x] 完成文档域模型、仓储接口、InMemory 仓储、验证与单元测试
- [x] 完成主项目与 handbook 的架构、路线图、任务、Backlog、Changelog、决策同步
- [ ] Upload API / RAG / pgvector / PostgreSQL Repository 留待后续 Sprint

### 2026-07-04 Sprint 8.1 Document Retrieval Contract Freeze

- [x] 冻结 `POST /api/v1/document-retrieval/search`
- [x] 冻结 `document.retrieval.started`、`document.retrieval.completed`、`document.retrieval.failed`
- [x] 冻结 `invalid_query`、`retrieval_unavailable`、`repository_error`
- [x] 新增 Document Retrieval Flow、Source Trace Flow、Future RAG Integration Flow
- [x] 完成主项目与 handbook 的任务、路线图、Backlog、Changelog、决策同步
- [ ] Retrieval implementation / RAG / embedding / pgvector / hybrid search 留待后续 Sprint

### 2026-07-04 Sprint 8.2 Document Retrieval API MVP Implementation

- [x] 实现 `POST /api/v1/document-retrieval/search`
- [x] 仅对现有 in-memory document chunks 做 keyword search
- [x] 实现 empty query / no match / archived exclusion / include_archived / deterministic ordering 测试
- [x] 保持 frozen contract 不变
- [x] 完成主项目与 handbook 的任务、路线图、Backlog、Changelog、决策同步

### 2026-07-04 Sprint 8.3 Retrieval Repository Abstraction + Worktree Cleanup

- [x] 将 `DocumentRetrievalService` 从 raw chunk storage 解耦到 `DocumentRetrievalProvider`
- [x] 保持 `InMemoryKeywordRetrieval` 的 keyword-only scoring / sorting 行为不变
- [x] 确认工作区没有额外 untracked chunk 文件
- [x] 更新主项目的 Architecture、DECISIONS、CHANGELOG、TASK、Backlog
- [ ] handbook mirror 自动同步被阻塞：`../scripts/sync_retail_handbook_docs.py` 需要缺失的 `ai-agent-retail-handbook-v3/README.md`

### 2026-07-04 Sprint 9.1 Internal RAG Contract Freeze

- [x] 冻结 `POST /api/v1/internal-rag/answer`
- [x] 冻结 `internal_rag.started`、`internal_rag.retrieval_completed`、`internal_rag.answer_generated`、`internal_rag.failed`
- [x] 冻结 `invalid_question`、`retrieval_unavailable`、`insufficient_context`、`citation_required`、`provider_timeout`、`repository_error`
- [x] 新增 Internal RAG Flow、Retrieval to Citation Flow、Future LLM Provider Flow、Future Approval Integration Flow
- [x] 完成主项目与 handbook 的任务、路线图、Backlog、Changelog、决策同步
- [x] 仅冻结 contract，不实现 RAG、embedding、pgvector、frontend

## Architecture Principles

- Platform First
- Domain Driven
- Provider Pattern
- Repository Pattern
- Workflow Driven
- Configuration First
- Test First
- Documentation First
- Backward Compatibility

## Target Architecture

### Current State

当前仓库未完全按平台化逻辑分层。

### Target State

未来目标逻辑分层：

```text
Platform
Domain
Provider
Workflow
Repository
Approval
Documents
Search
Import
Audit
Database
Frontend
```

### Planned

该结构用于 ERIP 目标架构规划，当前尚未全部实现。

## Epic 12 Positioning

### Current State

当前 RAG 尚未形成统一 Retrieval Layer。

### Target State

未来 RAG 范围明确包括：

- 结构化业务数据检索
- 社内文档检索
- 互联网检索
- 上下文合并
- 引用与来源追踪
- 幻觉风险控制
- 检索评估

### Planned

Epic 12 作为横向平台能力推进，而不是单一文档 RAG 能力。

## Definition of Done

任何一个 Phase 完成，必须同时满足：

- [ ] Code
- [ ] Unit Test
- [ ] Integration Test
- [ ] Frontend Test
- [ ] Handbook
- [ ] Changelog
- [ ] Decision Record
- [ ] Architecture Update
- [ ] Mermaid Diagram Update
- [ ] Task Update

## 测试文档规则

- 每个测试用例必须包含：
  - 用例目标
  - 前端操作流程
  - 后端处理流程
  - 数据输入来源
  - 预期输出
  - 验收标准
  - Mermaid 前端流程图
  - Mermaid 后端流程图

## 架构文档最小章节

- 前端流程图
- 后端流程图
- 数据流图
- 数据库 ER 图
- LangGraph workflow 图
- Retrieval Layer Architecture
- Business Retrieval Flow
- Internal RAG Flow
- Internet Search Flow
- Context Merge Flow
- Citation and Source Trace Flow
- Future Hybrid Search Architecture
- 文档检索流程图
- 审批 workflow 图
- 互联网检索流程图

### Phase 1: 文件化输入基础

- 状态：已完成第一轮实现，保持本地可运行。
- 本次完成：
  - [x] KPI 从 `backend/data/business/*.csv` 读取并计算
  - [x] Research 从 `backend/data/research/*.json` 读取 summary / sources
  - [x] 新增 `backend/data/documents/` Markdown 输入目录
  - [x] Report 增加 `generated` 状态，预留后续 Approval Workflow
  - [x] 新增文件输入测试与 hybrid 报告测试
- 后续待办：
  - [ ] 将 CSV / JSON 文件版本规则固化到导入规范
  - [ ] 将 `generated` 向 `draft / pending_approval / approved / rejected / revised` 扩展
  - [ ] 为 PostgreSQL 导入和持久化设计映射表结构

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  建立 CSV / JSON / Markdown 输入通路，替代 KPI、Research 和知识文档中的写死数据。
- 修改范围：
  数据目录规范、文件加载层、Provider 输入边界、示例数据、README / RUNBOOK / VERIFY 文档。
- 验收标准：
  任务执行可读取文件数据；移除关键运行路径中的硬编码示例值；本地仍可直接启动。
- 测试方法：
  文件加载单元测试、任务 API 集成测试、缺失文件与非法格式测试、手工验证报告来源。
- 风险：
  数据文件格式不一致、编码问题、样例数据与业务模型字段不匹配。

### Phase 2: PostgreSQL 持久化基础

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  为任务、事件、报告与导入记录提供可持久化数据库基础，并支持后续审批与检索扩展。
- 修改范围：
  PostgreSQL Repository、连接配置、迁移文件、表结构、运行脚本、部署文档。
- 验收标准：
  任务、事件、报告写入 PostgreSQL；进程重启后数据保留；接口合同保持稳定。
- 测试方法：
  Repository 测试、数据库集成测试、迁移测试、任务执行后持久化验证。
- 风险：
  本地数据库准备复杂、Schema 调整频繁、事务边界设计不足。

### Phase 3: 社内文档上传与入库

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  支持上传社内文档，并为每份文档建立版本、来源和审计信息。
- 修改范围：
  Upload API、文档元数据、文件存储策略、前端上传页面、错误处理与日志。
- 验收标准：
  支持上传受控格式文档；文档可登记并查询元数据；失败路径可追踪。
- 测试方法：
  上传接口测试、前端交互测试、重复文件测试、非法格式测试。
- 风险：
  敏感文档处理、文件大小限制、存储策略和权限设计不充分。

### Phase 4: 切分与检索基础

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  实现文档切分、片段入库、基础检索与引用输出，为 Approval Agent 和知识问答提供上下文。
- 修改范围：
  Chunk Pipeline、Retriever 抽象、片段存储、引用格式、Architecture 文档。
- 验收标准：
  上传文档可切分；查询时可返回 Top-K 片段和来源；检索结果可进入报告或审批上下文。
- 测试方法：
  Chunk 单元测试、检索回归测试、来源引用测试、端到端手工验证。
- 风险：
  Chunk 策略不稳定、检索质量不够、文档版本与索引版本失配。

### Phase 5: 审批 Workflow

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  建立可追踪的人工审批流程，支持提交、待审批、批准、拒绝和审计留痕。
- 修改范围：
  LangGraph 状态机、审批 API、审批日志表、前端审批界面、异常恢复逻辑。
- 验收标准：
  审批任务可稳定流转；日志完整；拒绝与重试路径可验证。
- 测试方法：
  状态迁移测试、审批接口测试、前端流程测试、失败恢复测试。
- 风险：
  状态管理复杂、幂等处理不足、人工操作与自动化边界不清。

### Phase 6: 互联网检索能力

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  在可控策略下引入互联网检索，为外部市场与竞品信息提供补充证据。
- 修改范围：
  Search Provider 抽象、可信来源规则、审计字段、降级策略、配置开关。
- 验收标准：
  可按配置启停互联网检索；结果保留来源；网络失败时主流程可降级。
- 测试方法：
  Provider 合同测试、失败降级测试、来源校验测试、人工抽样验证。
- 风险：
  外部数据质量、网络波动、成本与时效不可控。

### Phase 7: LangChain + LangGraph 工作流整合

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  把 LangChain 组件能力与 LangGraph 状态编排整合，形成清晰的 Tool / Retriever / Prompt / Workflow 分层。
- 修改范围：
  Workflow 组装层、Tool 适配层、Prompt 管理、Retriever 接口、架构文档和 ADR。
- 验收标准：
  组件职责清晰；核心状态流仍由 LangGraph 控制；新增组件不破坏现有 API。
- 测试方法：
  集成测试、Tool 调用测试、Prompt 回归测试、异常回退测试。
- 风险：
  框架职责重叠、抽象过度、调试成本上升。

### Phase 8: 测试体系与流程图文档

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  建立完整测试用例、测试方法、前后台流程图、系统架构图和学习文档同步机制。
- 修改范围：
  Backend / Frontend 测试、验证清单、流程图、`docs/ARCHITECTURE.md`、README、RUNBOOK。
- 验收标准：
  核心链路具备单元、集成、端到端验证；文档图示完整且与实现一致。
- 测试方法：
  执行自动化测试脚本、人工验收清单、文档对照审计。
- 风险：
  文档和实现不同步、测试成本过高、覆盖率高但有效性不足。

## Technical Debt

### High

- [ ] Chunk Strategy 统一
- [ ] Embedding 抽象层
- [ ] Prompt 版本管理
- [ ] 文件化输入契约未定义
- [ ] PostgreSQL Schema 与 Repository 边界未定义
- [ ] handbook 同步治理未形成关闭条件

### Medium

- [ ] API 统一返回格式
- [ ] 前端错误处理统一
- [ ] 初级学者友好注释补充
- [ ] Upload / Chunk / Retriever 流程图缺失
- [ ] 测试分层与测试数据策略未成体系
- [ ] handbook 测试模板与架构模板仍需补齐

### Low

- [ ] 文档补充
- [ ] 示例数据补充

## Known Issues

### BUG-001

描述：
Chunk 切分后显示效果需要确认。

状态：
Open

## Completion Log

### 2026-06-29

- 创建 PROJECT_BACKLOG.md
- 建立永久任务清单机制
- 在 AGENTS.md 追加中文“项目永久任务清单规则”，统一所有 AI 开发工具的开工与完工流程
- 建立 AI-LAB 全局规则、项目规则、Backlog、TASK 和 CHANGELOG 两层治理链路
### 2026-06-29 Governance V2

- [x] 升级到 AI-LAB Project Governance V2
- [x] 建立 Roadmap、Architecture 和 ADR 文档
- [ ] 根据真实代码和项目状态细化 Roadmap 与 Architecture

### 2026-07-02 文档同步器

- [x] 建立 retail-insight-ai 与 ai-agent-retail-handbook-v3 的文档同步映射
- [x] 新增跨项目文档同步脚本 `../../scripts/sync_retail_handbook_docs.py`
- [x] 新增同步清单 `../../doc-sync.manifest.json`

### 2026-07-04 Enterprise Planning

- [x] 将企业化改造需求纳入 TASK / Backlog / Roadmap
- [x] 新增 Phase 1 到 Phase 8 实施计划
- [x] 明确第一优先级为“文件化输入 + PostgreSQL 持久化基础”
- [x] 补充 Upload、检索、审批、互联网检索、LangChain + LangGraph、测试与架构文档任务

### 2026-07-04 Handbook Sync Governance

- [x] 新增 Phase 完成后的 handbook 同步规则
- [x] 新增测试用例强制模板规则
- [x] 新增架构文档必备图示清单
- [x] 新增 handbook CHANGELOG 与 DECISIONS 强制同步规则

### 2026-07-04 Epic 12 Retrieval and RAG Platform

- [x] 新增 Epic 12: Retrieval and RAG Platform

### 2026-07-04 Phase 1 文件化输入实现

- [x] KPI 硬编码数值迁移到 `backend/data/business/*.csv`
- [x] Research 硬编码摘要和来源迁移到 `backend/data/research/*.json`
- [x] 新增 `backend/data/documents/company_policy_sample.md`
- [x] 新增文件输入测试、Research JSON 测试、hybrid 报告测试
- [x] 报告模型预留 `generated / draft / pending_approval / approved / rejected / revised`

### 2026-07-04 Phase 1.5 Contract Freeze and Approval Design

- [x] 新增 `docs/DATA_CONTRACTS.md`
- [x] 新增 `docs/APPROVAL_WORKFLOW.md`
- [x] 新增 `docs/DATABASE.md`
- [x] 冻结导入错误模型
- [x] 冻结 Approval State Machine
- [x] 冻结 Phase 2 PostgreSQL 准备项
- [x] 明确 RAG 不只包括社内文档，还包括结构化业务数据检索和互联网检索
- [x] 新增 Retrieval Layer 相关架构章节与图示要求

<!-- DOC-SYNC:START group=governance -->
## 文档同步块

- group: `governance`
- file: `retail-insight-ai/docs/PROJECT_BACKLOG.md`
- self_sha256: `b1dd8a6cee6a7fc07965026b8aefe8c9c8f08669871abd5ce2b8eb3dc1d5d477`
- peers:
- `retail-insight-ai/ROADMAP.md` | sha256=5bf39c8dbde1e5279088478951af2f3c02a4506bcbf3682403b3e45a02846cae | # retail-insight-ai Roadmap / 最后更新：2026-06-29 / ## 当前阶段 / 待根据项目现状确认。
- `retail-insight-ai/TASK.md` | sha256=83a6ef1d9395a1c0026514c5d8fab074fb8428781ab712ad25764c1c82decc05 | # retail-insight-ai 当前任务 / 最后更新：2026-07-02 / ## 当前阶段 / Phase 2: Internal Knowledge Approval Agent
- `retail-insight-ai/docs/CHANGELOG.md` | sha256=cf9c2939e3369aa13c65a636fb64c44d56b672866b23771cf1dda5f1dbe755b3 | # retail-insight-ai CHANGELOG / ## 2026-07-02 / - 建立 retail-insight-ai 与 ai-agent-retail-handbook-v3 的跨项目文档同步机制。 / - 新增 `../scripts/sync_retail_handbook_docs.py` 与 `../doc-sync.manifest.json`。
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
