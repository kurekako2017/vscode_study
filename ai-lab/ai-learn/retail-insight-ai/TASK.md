# retail-insight-ai 当前任务

最后更新：2026-07-04

## 当前阶段

Sprint 9.4: LLM Provider Seam Contract Freeze

## 当前最高优先级任务

### Sprint Result

- [x] LLMProvider interface concept frozen as the future model integration seam
- [x] RAGAnswerGenerator concept frozen as the answer assembly boundary
- [x] prompt input/output contract frozen for optional LLM-driven answer generation
- [x] provider error model frozen for unavailable / timeout / invalid output / missing citation / cost limit cases
- [x] deterministic extractive fallback preserved as the current default behavior
- [x] token / cost / latency tracking placeholders documented for future providers
- [x] ARCHITECTURE / PROMPT_STANDARD / AI_AGENT_DESIGN_GUIDE / ERROR_CATALOG updated
- [x] TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS / handbook mirror synchronized

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

### Boundary

- 当前实现已包含 Internal RAG Evaluation MVP，评估层仍是 deterministic，不调用 LLM。
- 不实现 frontend、不实现 embedding、不实现 pgvector、不实现真实 LLM provider、不实现 PostgreSQL retrieval backend。
- 继续保持 `/api/v1/document-retrieval/search` contract、scoring 和 response shape 不变。

## Sprint 9.3: Internal RAG Evaluation + Citation Quality MVP

### Current State

Internal RAG 已具备 deterministic answer assembly 和内部 evaluation / citation quality checking。

### Target State

未来若接入 LLM provider，仍要复用当前 evaluation contract、citation quality checker 和 warning taxonomy。

### Planned

- 继续保持 `/api/v1/internal-rag/answer` 对外 response backward compatible。
- 未来评估规则可扩展，但不能破坏 current warning taxonomy 和 retrieval boundary。

## Sprint 9.2: Internal RAG MVP without LLM

### Sprint Result

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

## Sprint 8.3: Retrieval Repository Abstraction + Worktree Cleanup

### Current State

Document Retrieval service 已改为依赖 `DocumentRetrievalProvider`，不再直接依赖 raw chunk storage。

### Target State

Internal Document Retrieval 继续保持 keyword-only 行为，但检索后端边界已经独立出来，后续可替换成 PostgreSQL full-text 或其他 provider。

### Planned

- 保持 `POST /api/v1/document-retrieval/search` contract 不变。
- 保持 scoring / sorting / response shape 不变。
- 继续不实现 RAG、embedding、pgvector、frontend。

## Sprint 9.1: Internal RAG Contract Freeze

### Sprint Result

- [x] `POST /api/v1/internal-rag/answer` contract frozen
- [x] internal_rag.started / retrieval_completed / answer_generated / failed frozen
- [x] invalid_question / retrieval_unavailable / insufficient_context / citation_required / provider_timeout / repository_error frozen
- [x] Internal RAG Flow / Retrieval to Citation Flow / Future LLM Provider Flow / Future Approval Integration Flow added to Architecture
- [x] Prompt Standard updated with Internal RAG prompt family
- [x] TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS / handbook mirror updated
- [x] retrieval API behavior unchanged

### Boundary

- 只冻结 Internal RAG contract，不实现 RAG。
- 不调用 LLM、不实现 embedding、不实现 pgvector、不实现 frontend。
- 继续保持 retrieval API 行为、评分和返回结构不变。

### Current State

Internal RAG 只是基于 Document Retrieval Provider 的上层 contract，没有实际回答引擎。

### Target State

未来 Internal RAG 将成为 retrieval 之后、approval 之前的稳定 grounded answer boundary。

### Planned

- 继续保持 `/api/v1/internal-rag/answer` 与 `/api/v1/document-retrieval/search` 分离。
- 未来 summary mode 可接入可替换 LLM provider，但不得破坏 contract。

## Sprint 8.2: Document Retrieval API MVP Implementation

### Current State

Document Retrieval API 已实现，且严格遵守 Sprint 8.1 冻结 contract。

### Target State

Internal Document Retrieval 成为 chunk 与 future RAG 之间的稳定只读边界。

### Planned

- 后续可在不破坏 contract 的前提下引入 PostgreSQL full-text / hybrid search。
- 继续保持 Retrieval 仅为只读边界，不接入 LLM answer generation。

## Epic 14: Engineering Standards（Final Freeze）

- [x] 新增 `docs/MASTER_PROMPT.md`
- [x] 新增 `docs/CODING_STANDARD.md`
- [x] 新增 `docs/DEVELOPMENT_GUIDE.md`
- [x] 新增 `docs/AI_AGENT_DESIGN_GUIDE.md`
- [x] 新增 `docs/API_CONTRACT.md`
- [x] 新增 `docs/EVENT_CONTRACT.md`
- [x] 新增 `docs/PROMPT_STANDARD.md`
- [x] 在 `docs/ai-agent-retail-handbook-v3/docs/` 建立 handbook 镜像
- [x] 扩展 `../doc-sync.manifest.json` 以纳入 Engineering Standards 同步组
- [x] 冻结 Architecture / Workflow / Contract / Development Standard 文档入口

当前边界：

- 本次不修改 `backend/`
- 本次不修改 `frontend/`
- 本次不修改 `scripts/`
- 本次不新增业务代码
- 本次不修改数据库 schema

下一任务：

- 在 contract 不变前提下，评估 retrieval ranking 的可解释性、filter coverage 和 future search backend 替换点。

## Epic 0: Enterprise Platform Architecture Evolution

### Current State

当前项目名称保持为 `Retail Insight AI`，当前仓库仍是零售分析 Domain 的参考实现，尚未演进成完整企业平台。

### Target State

未来目标是演进到：

`Enterprise Retail Intelligence Platform (ERIP)`

但当前不得把项目描述为 ERIP 已存在或已实现。

### Planned

- [ ] Architecture Freeze
- [ ] Directory Refactor
- [ ] Repository Abstraction
- [ ] Workflow Abstraction
- [ ] Provider Abstraction
- [ ] Documentation Standard
- [ ] Testing Standard

## Epic 0 Deliverables

- [ ] Architecture Freeze
- [ ] Directory Freeze
- [ ] Repository Freeze
- [ ] Provider Freeze
- [ ] Workflow Freeze
- [ ] Database Freeze
- [ ] Testing Freeze
- [ ] Documentation Freeze

## Epic 12: Retrieval and RAG Platform

### Current State

当前项目尚未实现完整 Retrieval Layer。

当前只存在零售分析主链路中的简化 KPI / Research 路径，不代表已经具备完整 RAG 平台能力。

### Target State

未来 Retrieval and RAG Platform 不只包括社内文档 RAG，还包括：

- 结构化业务数据检索
- 社内文档检索
- 互联网检索
- 多来源上下文合并
- 引用与来源追踪
- 幻觉风险控制
- 检索效果评估

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

当前仓库仍以现有 `backend/`、`frontend/`、`docs/` 为主，不代表平台目标结构已全部落地。

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

上述结构是 ERIP 目标架构视图，当前尚未全部实现。

### P0

- [ ] 确认项目目录结构
- [ ] 确认 Docker 环境
- [ ] 确认 .gitignore 是否保护敏感文件
- [ ] 确认 Document Upload 流程

## Phase 1 到 Phase 8 实施计划

## Definition of Done

以后任何一个 Phase 完成必须同时满足：

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

只要任一项未完成，对应 Phase 不能标记为完成。

## Handbook 同步规则

- 每个 Phase 完成后，必须同步更新 `docs/ai-agent-retail-handbook-v3/` 下对应文档。
- Handbook 同步至少覆盖：
  `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`docs/ARCHITECTURE.md`、`docs/CHANGELOG.md`、`docs/DECISIONS.md`。
- 如果本次变更涉及测试、流程、架构、运行方式，还必须同步检查并更新：
  `08_架构图册.md`、`09_系统设计书.md`、`10_Production_Roadmap.md`。
- 未完成 Handbook 同步，不得将对应 Phase 标记为完成。
- 所有核心架构图必须三语言维护：
  English、中文（简体）、日本語。

## 测试用例文档规则

- 每个测试用例必须包含：
  - 用例目标
  - 前端操作流程
  - 后端处理流程
  - 数据输入来源
  - 预期输出
  - 验收标准
  - Mermaid 前端流程图
  - Mermaid 后端流程图

## 架构文档规则

- 架构文档必须包含：
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

- [x] 是否完成
- [x] Handbook 文档已同步
- 目标：
  建立本地可运行的文件化输入基础，支持 CSV / JSON / Markdown 作为业务数据、Research 数据和文档数据的输入来源。
- 修改范围：
  `backend/app/` 数据加载层、Provider 组合方式、示例数据目录约定、README / RUNBOOK / VERIFY 文档，并为后续 Approval Workflow 预留报告状态边界。
- 验收标准：
  Backend 可以从约定目录读取 CSV / JSON / Markdown；KPI 与 Research 不再依赖写死示例值；本地运行无需真实数据库和外网；Report 当前仍直接生成，但状态模型已预留后续审批流扩展。
- 测试方法：
  运行文件加载单元测试；执行本地 API 创建任务；验证 hybrid 报告内容来自文件输入；验证缺失文件时返回标准错误；记录后续 Approval Workflow 测试预留项。
- 风险：
  文件格式不统一、编码问题、版本命名混乱、示例数据与代码契约不一致。

### Phase 1.5: Data Contract Freeze + Approval State Machine Design

- [x] 是否完成
- [x] Handbook 文档已同步
- 目标：
  固化 Phase 1 文件输入契约、导入错误模型和 Report / Approval 状态机，为 Phase 2 PostgreSQL 持久化与后续承認ワークフロー提供唯一设计依据。
- 修改范围：
  `docs/DATA_CONTRACTS.md`、`docs/APPROVAL_WORKFLOW.md`、`docs/DATABASE.md` 以及治理文档、架构文档、handbook 同步文档。
- 验收标准：
  业务 CSV、Research JSON、Documents Markdown 契约冻结；导入错误模型冻结；审批状态机冻结；Phase 2 表设计准备项冻结。
- 测试方法：
  文档审计；对照 Phase 1 已落地文件输入实现；确认状态机、Mermaid 图和 PostgreSQL 准备项已同步到主项目与 handbook。
- 风险：
  文档与代码未来漂移、审批状态与任务状态语义混淆、导入错误模型与实现不一致。

### Phase 2: PostgreSQL 持久化基础

- [ ] 是否完成
- [x] Handbook 文档已同步
- 当前状态：
  `Code implemented`
  `InMemory path verified`
  `PostgreSQL schema implemented`
  `PostgreSQL repository tests prepared`
  `PostgreSQL verification script added`
  `PostgreSQL real integration test pending`
  `Status: In Progress / Partially Verified`
- 目标：
  为 Task、Event、Report 和后续导入记录建立 PostgreSQL 持久化基础，同时保留本地可切换运行能力。
- 修改范围：
  `backend/app/config/`、`backend/app/db/`、`backend/app/repositories/`、`backend/app/models/`、`backend/tests/`、`backend/db/`、`.env.example`、`docker-compose.yml`、治理文档与 handbook。
- 验收标准：
  `REPOSITORY_BACKEND` 支持 `inmemory / postgres`；默认仍为 `inmemory`；Task / Event / Report 具备 PostgreSQL Repository；`data_imports`、`import_errors`、`approval_requests`、`approval_events` 完成 schema 与基础模型预留；当前 `reports.approval_status` 仍写入 `generated`。
- 测试方法：
  InMemory 全量回归；Repository backend switch 单元测试；PostgreSQL Repository 集成测试覆盖 create task、append event、save report、get report；当前环境缺少 `psycopg` / Docker 时记录跳过原因并提供手动命令。
- 当前未验证原因：
  当前环境缺少 Docker CLI；当前环境未安装 `psycopg` 到实际运行 venv；PostgreSQL 集成测试当前被 skip。已新增 `./scripts/verify_postgres_phase2.sh` 统一输出跳过原因与手动验证命令。外部 handbook 同步脚本因缺少同级 `../ai-agent-retail-handbook-v3/` 工作区而未执行。
- 下一步验证命令：
  `./scripts/verify_postgres_phase2.sh`
  或手工执行：
  `docker compose up -d postgres`
  `cd backend`
  `source .venv/bin/activate`
  `pip install -r requirements.txt`
  `REPOSITORY_BACKEND=postgres python -m unittest tests.test_postgres_repositories -v`
- 风险：
  本地环境数据库依赖增加、Schema 演进成本、连接池与事务边界设计不当、未完成真实 PostgreSQL 联调前不可宣称 Phase 2 全部关闭。

### Phase 3: 社内文档上传与入库

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  支持社内文档上传、元数据登记、原文保存和可追踪的数据版本管理。
- 修改范围：
  上传 API、文件存储路径、文档元数据表、前端上传入口、审计字段、运行手册。
- 验收标准：
  可上传受支持格式文档；系统记录上传者、时间、文件名、版本；上传失败有标准错误与日志。
- 测试方法：
  API 上传测试、非法文件测试、重复上传测试、前端上传流程测试、文档元数据查询测试。
- 风险：
  文件大小限制、编码与格式兼容、权限边界、敏感文档泄露风险。

### Phase 4: 切分与检索基础

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  建立文档切分、索引登记、基础检索和来源引用能力，为知识库问答与审批提供证据链。
- 修改范围：
  Chunk Pipeline、Chunk 配置、Retriever 抽象、引用格式、评估样例、Architecture 文档。
- 验收标准：
  文档可切分并入库；可根据查询返回 Top-K 片段与来源；报告可展示引用来源。
- 测试方法：
  Chunk 单元测试、检索召回测试、固定问答样例测试、来源引用验证。
- 风险：
  Chunk 策略不稳定、召回质量差、索引与原文版本不一致。

### Phase 5: 审批 Workflow

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  建立可审计的审批 Workflow，支持人工确认、状态流转、审批日志和失败恢复。
- 修改范围：
  LangGraph State / Node / Edge、审批表结构、审批 API、前端审批页面、日志与审计文档。
- 验收标准：
  审批任务可进入待审批、已批准、已拒绝状态；状态流转可追踪；不可逆动作有人工确认。
- 测试方法：
  Workflow 状态迁移测试、审批 API 测试、前端审批流程测试、异常恢复测试。
- 风险：
  状态机复杂度上升、幂等性不足、人工操作与自动执行边界不清。

### Phase 6: 互联网检索能力

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  在受控边界内引入互联网检索能力，用于市场趋势、竞品与外部公开信息补充。
- 修改范围：
  Search Provider 抽象、结果清洗、来源可信度规则、超时与重试、开关配置、审计说明。
- 验收标准：
  可按配置启用或禁用互联网检索；结果包含来源；外网失败时系统能降级而非整体崩溃。
- 测试方法：
  Provider 合同测试、失败降级测试、来源格式测试、手工验证检索结果与报告引用。
- 风险：
  外部信息时效与准确性风险、引用不可控、网络超时与成本不可预测。

### Phase 7: LangChain + LangGraph 工作流整合

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  在保持现有 LangGraph 可控状态编排的前提下，引入 LangChain 组件化能力，统一 Tool、Prompt、Retriever 和 Chain 边界。
- 修改范围：
  Workflow 编排层、Tool / Retriever 适配层、Prompt 管理、Chain 组合、架构文档与 ADR。
- 验收标准：
  LangChain 组件与 LangGraph Workflow 边界清晰；核心流程仍由 LangGraph 状态机控制；组件可替换。
- 测试方法：
  Workflow 集成测试、Tool 调用测试、Prompt 回归测试、故障回退测试。
- 风险：
  双框架职责重叠、抽象层过多、调试成本上升。

### Phase 8: 测试体系与流程图文档

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  建立完整测试用例、测试方法、前后台程序流程图和架构文档，使项目达到可交接和可审计水平。
- 修改范围：
  Backend tests、Frontend tests、集成测试、验证清单、`docs/ARCHITECTURE.md`、`README.md`、`VERIFY_CHECKLIST.md`。
- 验收标准：
  核心流程覆盖单元、集成、端到端验证；架构图、数据流图、审批流图、上传与检索流程图齐全且与代码一致。
- 测试方法：
  执行 `./scripts/run_tests.sh`、补充人工验证步骤、按文档逐项验收。
- 风险：
  文档与实现脱节、测试过慢、样例数据不足导致覆盖失真。

## 本次工作完成标准

- [x] PROJECT_BACKLOG.md 已更新
- [x] TASK.md 已更新
- [x] CHANGELOG.md 已更新
- [x] AGENTS.md 规则未被破坏

## 下一步建议

优先进入 Phase 2 设计与最小实现：基于已冻结的 `DATA_CONTRACTS`、`APPROVAL_WORKFLOW`、`DATABASE` 文档，为 Task / Report / Event / Import / Approval 建立 PostgreSQL Repository 边界。
## Governance V2 升级记录

- [x] 创建 `ROADMAP.md`
- [x] 创建 `docs/ARCHITECTURE.md`
- [x] 创建 `docs/DECISIONS.md`
- [x] 更新项目 `AGENTS.md` 的开发前读取顺序
- [ ] 根据项目实际状态完善 Roadmap 与 Architecture

## 2026-07-02 文档同步器

- [x] 建立 retail-insight-ai 与 ai-agent-retail-handbook-v3 的文档同步映射
- [x] 新增跨项目文档同步脚本 `../scripts/sync_retail_handbook_docs.py`
- [x] 新增同步清单 `../doc-sync.manifest.json`

<!-- DOC-SYNC:START group=governance -->
## 文档同步块

- group: `governance`
- file: `retail-insight-ai/TASK.md`
- self_sha256: `83a6ef1d9395a1c0026514c5d8fab074fb8428781ab712ad25764c1c82decc05`
- peers:
- `retail-insight-ai/ROADMAP.md` | sha256=5bf39c8dbde1e5279088478951af2f3c02a4506bcbf3682403b3e45a02846cae | # retail-insight-ai Roadmap / 最后更新：2026-06-29 / ## 当前阶段 / 待根据项目现状确认。
- `retail-insight-ai/docs/PROJECT_BACKLOG.md` | sha256=b1dd8a6cee6a7fc07965026b8aefe8c9c8f08669871abd5ce2b8eb3dc1d5d477 | # retail-insight-ai Project Backlog / 最后更新：2026-07-02 / ## 项目目标 / 构建企业级 Retail Insight AI 平台，包含：
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
