# 当前任务

最后更新：2026-07-04

## 当前阶段

Sprint 9.4: LLM Provider Seam Contract Freeze

## 当前最高优先级任务

- [x] `LLMProvider` interface concept frozen
- [x] `RAGAnswerGenerator` concept frozen
- [x] prompt input/output contract frozen for future model-backed answers
- [x] provider error model frozen for unavailable / timeout / invalid output / citation missing / cost limit cases
- [x] deterministic extractive fallback remains the current default
- [x] token / cost / latency tracking placeholders documented
- [x] handbook architecture / prompt / design / error docs updated
- [x] TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS synchronized

### Boundary

- 当前行为仍然是 deterministic internal RAG，不调用 LLM、不调用外部 provider。
- 不修改 backend、frontend 或 scripts。
- 不改变 `POST /api/v1/internal-rag/answer` 的 response 结构。

## Sprint 9.4: LLM Provider Seam Contract Freeze

### Current State

Internal RAG 已完成 deterministic answer assembly，当前只冻结未来 LLM provider 的接入边界。

### Target State

未来可以把 `LLMProvider` 接到 `RAGAnswerGenerator` 后面，而不改变 retrieval contract、citation contract 或 API response。

### Planned

- 继续保持当前 no-LLM 行为作为默认路径。
- 未来若接入模型，只允许替换 answer generation seam，不允许回写 retrieval provider boundary。

## Sprint 9.3: Internal RAG Evaluation + Citation Quality MVP

- [x] citation quality checker validates document_id / chunk_id / grounded excerpt
- [x] internal RAG evaluation service computes coverage_score / citation_score / confidence / warnings
- [x] low_context / missing_citation / weak_match warnings are generated internally
- [x] extractive answer has citation_score=1.0 on grounded paths
- [x] summary mode still returns citations
- [x] archived filtering and retrieval API behavior remain unchanged
- [x] backend tests added for evaluation scores, missing citation warning, weak_match, and low_context
- [x] existing retrieval and internal RAG tests still pass
- [x] TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS / handbook mirror synchronized

## Sprint 9.3: Internal RAG Evaluation + Citation Quality MVP

### Current State

Internal RAG 已具备 deterministic answer assembly 和内部 evaluation / citation quality checking。

### Target State

未来若接入 LLM provider，仍要复用当前 evaluation contract、citation quality checker 和 warning taxonomy。

### Planned

- 继续保持 `/api/v1/internal-rag/answer` 对外 response backward compatible。
- 未来评估规则可扩展，但不能破坏 current warning taxonomy 和 retrieval boundary。

## Sprint 9.2: Internal RAG MVP without LLM

- [x] POST /api/v1/internal-rag/answer implemented
- [x] InternalRagService added on top of DocumentRetrievalProvider
- [x] extractive answer assembly uses top retrieval excerpts
- [x] summary mode is deterministic and does not call an LLM
- [x] citation validation returns grounded citations for each used excerpt
- [x] invalid_question / insufficient_context / citation_required behavior covered
- [x] archived documents are excluded unless include_archived=true
- [x] backend tests added for extractive success, summary determinism, no context, empty question, citations, and archived exclusion
- [x] existing retrieval tests still pass
- [x] TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS / handbook mirror synchronized
- [x] retrieval API behavior remains unchanged

## Sprint 8.2: Document Retrieval API MVP Implementation

### Current State

Document Retrieval API 已实现，且严格遵守 Sprint 8.1 冻结 contract。

### Target State

Internal Document Retrieval 成为 chunk 与 future RAG 之间的稳定只读边界。

### Planned

- 后续可在不破坏 contract 的前提下引入 PostgreSQL full-text / hybrid search。
- 继续保持 Retrieval 仅为只读边界，不接入 LLM answer generation。

## Sprint 9.1: Internal RAG Contract Freeze

### Current State

Internal RAG 只是基于 Document Retrieval Provider 的上层 contract，没有实际回答引擎。

### Target State

未来 Internal RAG 将成为 retrieval 之后、approval 之前的稳定 grounded answer boundary。

### Planned

- 继续保持 `/api/v1/internal-rag/answer` 与 `/api/v1/document-retrieval/search` 分离。
- 未来 summary mode 可接入可替换 LLM provider，但不得破坏 contract。

## Epic 0: Enterprise Platform Architecture Evolution

### Current State

- 当前实现仍停留在 Document Chunk Pipeline MVP，文档读写的后端 MVP 已覆盖上传、读取、归档、导入与切分。
- Document Retrieval 仅完成契约冻结，尚未进入 backend 实现。
- 不实现 frontend、不实现 RAG、不实现 embedding、不实现 pgvector、不实现 hybrid search、不实现 Approval API。
- 继续保持 PostgreSQL Document Repository 仅设计不实现，versions / RAG / embedding / pgvector / Approval API 仍冻结未实现。

### Target State

未来平台目标名称：

`Enterprise Retail Intelligence Platform (ERIP)`

### Planned

- [ ] Architecture Freeze
- [ ] Directory Refactor
- [ ] Repository Abstraction
- [ ] Workflow Abstraction
- [ ] Provider Abstraction
- [ ] Documentation Standard
- [ ] Testing Standard

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

## Definition of Done

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

## Epic 12: Retrieval and RAG Platform

### Current State

当前 handbook 尚未把 Retrieval Layer 作为完整横向平台能力冻结下来。

### Target State

未来 `Epic 12` 覆盖：

- Business Data Retrieval
- Internal Document Retrieval
- Internet Search Retrieval
- Context Merge
- Citation and Source Trace
- Hallucination Risk Control
- Retrieval Evaluation

### Planned

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

## Sprint 1 Follow-up: Phase 3.1 Document Domain Model

### Current State

Document Domain Model 已作为 Phase 3.1 共同基础同步到 handbook。

### Synced Result

- [x] Document / DocumentVersion / DocumentChunk placeholder / DocumentMetadata / DocumentSource
- [x] DocumentStatus / DocumentType / Language / ApprovalStatus reuse
- [x] DocumentRepository Interface
- [x] InMemoryDocumentRepository
- [x] Document creation / metadata validation / status transition / CRUD / checksum duplicate detection
- [x] Handbook Architecture / ROADMAP / PROJECT_BACKLOG / DECISIONS / CHANGELOG / 图册 / 系统设计书 / 生产路线图 同步
- [x] `backend/app/repositories/implementations/in_memory/document_repository.py` 仅存在于正确路径
- [x] 之前提到的重复路径是报告 typo，不是实际误放文件

### Next Step

- 保持 Document Domain Model 作为后续 Upload / RAG / Approval / PostgreSQL 的唯一领域基础。

## Sprint 2 Follow-up: Document Upload API Contract Freeze

### Current State

Document Upload API contract 已冻结，当前仍不表示 Upload API 已实现。

### Synced Result

- [x] Document Upload API contract 已冻结
- [x] Document Upload event contract 已冻结
- [x] Document Upload Validation Flow 已同步
- [x] Future Approval Integration Flow 已同步
- [x] Handbook Architecture / ROADMAP / PROJECT_BACKLOG / DECISIONS / CHANGELOG / 图册 / 系统设计书 / 生产路线图 同步
- [ ] Upload API implementation
- [ ] Upload persistence implementation

## Sprint 2.5 Follow-up: Document Upload Workflow + Error Catalog + Upload Policy Freeze

### Current State

Document Upload Workflow, Error Catalog, and Upload Policy 已同步到 handbook。

### Synced Result

- [x] Document Upload Workflow
- [x] Upload Session contract
- [x] Idempotency contract
- [x] `docs/ERROR_CATALOG.md`
- [x] `docs/UPLOAD_POLICY.md`
- [x] Handbook Architecture / ROADMAP / PROJECT_BACKLOG / DECISIONS / CHANGELOG / 图册 / 系统设计书 / 生产路线图 同步
- [ ] Upload API implementation
- [ ] Upload Session persistence

### Next Step

- 保持 Upload API 仅处于冻结状态，不进入实现。

## Phase 1 Sync: 文件化输入实现

### Current State

handbook 已同步主项目的文件化输入改造结果，但当前不表示 Approval Workflow 已实现。

### Synced Result

- [x] KPI 从 `backend/data/business/*.csv` 读取并计算
- [x] Research 从 `backend/data/research/*.json` 读取 `summary / sources`
- [x] 建立 `backend/data/documents/*.md` 输入边界样例
- [x] Report 当前状态为 `generated`
- [x] 预留后续审批状态：
  `draft / pending_approval / approved / rejected / revised`
- [x] Handbook 文档已同步

## Phase 1.5 Sync: Data Contract Freeze + Approval State Machine Design

### Current State

handbook 尚未把 Data Contract、Import Error Model 和 Approval State Machine 作为独立冻结输出记录完整。

### Synced Result

- [x] Data Contract 冻结已同步
- [x] Import Error Model 冻结已同步
- [x] Approval State Machine 冻结已同步
- [x] Phase 2 PostgreSQL 准备项已同步
- [x] Handbook 文档已同步

## Phase 2 Sync: PostgreSQL Persistence MVP

### Current State

主项目已完成 PostgreSQL 持久化基础代码，但 handbook 需要明确当前仍处于默认 `inmemory` 运行模式。

### Synced Result

- [x] Code implemented
- [x] InMemory path verified
- [x] PostgreSQL schema implemented
- [x] PostgreSQL repository tests prepared
- [ ] PostgreSQL real integration test pending
- [x] Status: In Progress / Partially Verified
- [x] `REPOSITORY_BACKEND` 支持 `inmemory / postgres`
- [x] 默认值仍为 `inmemory`
- [x] PostgreSQL 覆盖 Task / Event / Report 持久化
- [x] `data_imports`、`import_errors` 仅完成 schema 预留
- [x] `approval_requests`、`approval_events` 仅完成 schema 预留
- [x] `reports.approval_status` 已入库，当前值仍为 `generated`
- [x] Handbook 文档已同步
- [x] 当前环境缺少 Docker CLI、未安装 `psycopg` 到实际运行 venv、PostgreSQL 集成测试被 skip

## Sprint 1 Follow-up: Phase 3.1 Document Domain Model

### Current State

Document Domain Model 已作为 Phase 3.1 共同基础同步到 handbook。

### Synced Result

- [x] Document / DocumentVersion / DocumentChunk placeholder / DocumentMetadata / DocumentSource
- [x] DocumentStatus / DocumentType / Language / ApprovalStatus reuse
- [x] DocumentRepository Interface
- [x] InMemoryDocumentRepository
- [x] Document creation / metadata validation / status transition / CRUD / checksum duplicate detection
- [x] Handbook Architecture / ROADMAP / PROJECT_BACKLOG / DECISIONS / CHANGELOG / 图册 / 系统设计书 / 生产路线图 同步
- [x] `backend/app/repositories/implementations/in_memory/document_repository.py` 仅存在于正确路径
- [x] 之前提到的重复路径是报告 typo，不是实际误放文件

### Next Step

- 保持 Document Domain Model 作为后续 Upload / RAG / Approval / PostgreSQL 的唯一领域基础。

## Handbook 同步规则

- 每个 Phase 完成后，必须同步更新 handbook 对应文档。
- handbook 同步最小集合：
  `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/ARCHITECTURE.md`、`docs/CHANGELOG.md`、`docs/DECISIONS.md`。
- 若变更涉及测试、流程、系统设计和生产路线图，还必须同步检查并更新：
  `08_架构图册.md`、`09_系统设计书.md`、`10_Production_Roadmap.md`。
- 未完成 handbook 同步，不得把主项目对应 Phase 标记为完成。
- 所有核心架构图必须三语言维护：
  English、中文（简体）、日本語。

## 文档模板规则

- 每个测试用例必须包含：
  - 用例目标
  - 前端操作流程
  - 后端处理流程
  - 数据输入来源
  - 预期输出
  - 验收标准
  - Mermaid 前端流程图
  - Mermaid 后端流程图
- 架构文档必须覆盖：
  - 前端流程图
  - 后端流程图
  - 数据流图
  - 数据库 ER 图
  - LangGraph workflow 图
  - 文档检索流程图
  - 审批 workflow 图
  - 互联网检索流程图
## Governance V2 升级记录

- [x] 创建 `ROADMAP.md`
- [x] 创建 `docs/ARCHITECTURE.md`
- [x] 创建 `docs/DECISIONS.md`
- [x] 更新项目 `AGENTS.md` 的开发前读取顺序
- [ ] 根据项目实际状态完善 Roadmap 与 Architecture

## 2026-07-02 文档同步器

- [x] 建立 ai-agent-retail-handbook-v3 与 retail-insight-ai 的文档同步映射
- [x] 新增跨项目文档同步脚本 `../scripts/sync_retail_handbook_docs.py`
- [x] 新增同步清单 `../doc-sync.manifest.json`

<!-- DOC-SYNC:START group=governance -->
## 文档同步块

- group: `governance`
- file: `ai-agent-retail-handbook-v3/TASK.md`
- self_sha256: `8375c8be41775af3f492dbc66e69653096db6bcdc4838d411eacf72cd81d5c82`
- peers:
- `retail-insight-ai/ROADMAP.md` | sha256=5bf39c8dbde1e5279088478951af2f3c02a4506bcbf3682403b3e45a02846cae | # retail-insight-ai Roadmap / 最后更新：2026-06-29 / ## 当前阶段 / 待根据项目现状确认。
- `retail-insight-ai/TASK.md` | sha256=83a6ef1d9395a1c0026514c5d8fab074fb8428781ab712ad25764c1c82decc05 | # retail-insight-ai 当前任务 / 最后更新：2026-07-02 / ## 当前阶段 / Phase 2: Internal Knowledge Approval Agent
- `retail-insight-ai/docs/PROJECT_BACKLOG.md` | sha256=b1dd8a6cee6a7fc07965026b8aefe8c9c8f08669871abd5ce2b8eb3dc1d5d477 | # retail-insight-ai Project Backlog / 最后更新：2026-07-02 / ## 项目目标 / 构建企业级 Retail Insight AI 平台，包含：
- `retail-insight-ai/docs/CHANGELOG.md` | sha256=cf9c2939e3369aa13c65a636fb64c44d56b672866b23771cf1dda5f1dbe755b3 | # retail-insight-ai CHANGELOG / ## 2026-07-02 / - 建立 retail-insight-ai 与 ai-agent-retail-handbook-v3 的跨项目文档同步机制。 / - 新增 `../scripts/sync_retail_handbook_docs.py` 与 `../doc-sync.manifest.json`。
- `ai-agent-retail-handbook-v3/ROADMAP.md` | sha256=8bea54fca33668303cb3ebc6a86e9fb359d814605450746eb7575075bc4600cf | # ai-agent-retail-handbook-v3 Roadmap / 最后更新：2026-06-29 / ## 当前阶段 / 待根据项目现状确认。
- `ai-agent-retail-handbook-v3/docs/PROJECT_BACKLOG.md` | sha256=4b25c1fa793fa7ce50f3cc87341c8136603a8fc0eeae44e3b57dfcfd17f4dfc7 | # 项目总待办清单 / 最后更新：2026-07-02 / ## 项目目标 / 待确认
- `ai-agent-retail-handbook-v3/docs/CHANGELOG.md` | sha256=db921303a94dca1268fc38339f4c13606461269c65ca79c1de024cc1d36601c3 | # CHANGELOG / ## 2026-07-02 / - 建立 ai-agent-retail-handbook-v3 与 retail-insight-ai 的跨项目文档同步机制。 / - 新增 `../scripts/sync_retail_handbook_docs.py` 与 `../doc-sync.manifest.json`。
- `ai-agent-retail-handbook-v3/10_Production_Roadmap.md` | sha256=d904e6883e84c4bb5adda4d7adab4499e1e0f6f5e52bf97f46ecd7150271e64e | # 10_Production_Roadmap / # 目录 / - [1. Roadmap 原则](#1-roadmap-原则) / - [2. Level 1 Demo](#2-level-1-demo)

说明：
- 这个块由 `scripts/sync_retail_handbook_docs.py` 自动维护。
- 只同步这个块，不覆盖各自正文。
- 任一组内文档正文变化时，整组文档的同步块都会一起刷新。
<!-- DOC-SYNC:END group=governance -->
