# retail-insight-ai Roadmap

最后更新：2026-07-04

## 当前阶段

Phase 2: PostgreSQL Persistence MVP

当前企业化主线：

1. 文件化输入（CSV / JSON / Markdown）
2. PostgreSQL 持久化基础
3. 社内文档上传、入库、切分、检索
4. 审批 Workflow
5. 互联网检索
6. LangChain + LangGraph 工作流整合
7. 完整测试体系
8. 架构图与流程图文档

## Epic 12 Positioning

### Current State

当前尚未形成完整 Retrieval and RAG Platform。

### Target State

`Epic 12: Retrieval and RAG Platform` 作为横向平台能力，服务于业务检索、社内文档检索、互联网检索、上下文组装、引用追踪与风险控制。

### Planned

当前将 Epic 12 作为横向平台能力标记。未来若出现 Epic 9~11，Epic 12 仍保持横向能力，不依赖编号顺序表达优先级。

## Project Positioning

### Current State

项目名称保持为 `Retail Insight AI`。

当前项目定位：

`Retail Analysis Domain Reference Implementation`

### Target State

未来平台目标名称：

`Enterprise Retail Intelligence Platform (ERIP)`

ERIP 表示企业平台目标架构，不表示当前仓库、当前部署或当前产品名称。

### Planned

后续所有平台化规划都必须写成“演进目标”或“Target State”，不得写成已落地现状。

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

## Epic 0: Enterprise Platform Architecture Evolution

### Current State

当前仓库仍以单项目、教学型、可运行 Demo 为主，尚未完成平台级目录冻结和抽象边界治理。

### Target State

以 `Retail Insight AI` 为零售分析领域参考实现，逐步沉淀面向 `ERIP` 的平台架构边界。

### Planned Tasks

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

当前 Retrieval 能力尚未形成统一抽象层。

### Target State

未来 RAG 平台覆盖：

- Business Data Retrieval
- Internal Document Retrieval
- Internet Search Retrieval
- Context Merge
- Citation and Source Trace
- Retrieval Evaluation

### Planned Tasks

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

## Target Architecture

### Current State

当前目录尚未完全按平台化目标分层。

### Target State

未来目标架构逻辑分层：

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

这是 ERIP 目标架构分层，不表示当前这些目录或模块已经全部实现。

## Definition of Done

任何一个 Phase 只有在以下项目全部满足后，才允许标记完成：

- Code
- Unit Test
- Integration Test
- Frontend Test
- Handbook
- Changelog
- Decision Record
- Architecture Update
- Mermaid Diagram Update
- Task Update

## 下一阶段

1. 完成 PostgreSQL 本地联调与手动验收，保持 `inmemory` 默认不变。
2. 以 `tasks / task_events / reports / report_versions / data_imports / import_errors / approval_requests / approval_events` 为事实表基础，推进 Phase 3 文档入库与 Phase 5 审批流。
3. 为 Upload、Chunk、Retriever、Approval Workflow 继续保留稳定接口。

## Handbook 同步门禁

- 每个 Phase 完成后，必须同步更新 `docs/ai-agent-retail-handbook-v3/` 对应文档。
- handbook 同步是 Phase 完成门禁的一部分，不允许后补为“已完成”。
- 功能、测试、流程、架构变更至少同步到：
  `docs/ARCHITECTURE.md`、`docs/CHANGELOG.md`、`docs/DECISIONS.md`。
- 若本次变更涉及任务治理、生产路线图或系统流程，还必须同步检查：
  `TASK.md`、`ROADMAP.md`、`docs/PROJECT_BACKLOG.md`、`08_架构图册.md`、`09_系统设计书.md`、`10_Production_Roadmap.md`。

## 测试与架构文档门禁

- 每个测试用例必须具备目标、前端操作流程、后端处理流程、数据输入来源、预期输出、验收标准、Mermaid 前端流程图、Mermaid 后端流程图。
- 架构文档必须持续覆盖前端流程图、后端流程图、数据流图、数据库 ER 图、LangGraph workflow 图、文档检索流程图、审批 workflow 图、互联网检索流程图。

## Phase 1 到 Phase 8 路线图

### Phase 1: 文件化输入基础

- 目标：建立 CSV / JSON / Markdown 输入边界，替代关键运行路径中的硬编码数据。
- 交付重点：数据目录、加载契约、样例数据、文档说明、Approval Workflow 预留状态边界。
- 当前结果：已完成本地 CSV / JSON / Markdown 输入落地。KPI 改为从 `backend/data/business/*.csv` 计算，Research 改为从 `backend/data/research/*.json` 读取，`backend/data/documents/` 已建立 Markdown 样例目录。
- 当前边界：Report 仍为直接生成，当前状态为 `generated`。后续 Approval Workflow 将在此基础上扩展 `draft / pending_approval / approved / rejected / revised`。

### Phase 1.5: Data Contract Freeze + Approval State Machine Design

- 目标：冻结文件输入契约、导入错误分类与报告审批状态机，避免 CSV / JSON 字段漂移，并为 Phase 2 PostgreSQL 提供表设计依据。
- 交付重点：`docs/DATA_CONTRACTS.md`、`docs/APPROVAL_WORKFLOW.md`、`docs/DATABASE.md`、Mermaid 图、ADR。
- 当前结果：已冻结业务 CSV、Research JSON、Documents Markdown 边界；已冻结 `missing_file / invalid_header / invalid_type / empty_dataset / invalid_json / invalid_source / unsupported_encoding`；已冻结 `generated / draft / pending_approval / approved / rejected / revised / published / archived`。
- 当前边界：当前仍只实现 `generated`；当前未实现 PostgreSQL、审批 API、审批事件、审批前端。

### Phase 2: PostgreSQL 持久化基础

- 目标：为 Task、Event、Report 与导入记录建立数据库持久化能力。
- 交付重点：`REPOSITORY_BACKEND` 切换、PostgreSQL 连接管理、`schema.sql` / `init.sql`、Task / Event / Report Repository、导入与审批 schema 预留。
- 当前结果：已完成 PostgreSQL Repository MVP，默认后端仍为 `inmemory`；`reports.approval_status` 已入库但当前值仍为 `generated`；`data_imports`、`import_errors`、`approval_requests`、`approval_events` 已建表但未接入 API。
- 当前边界：当前环境未执行真实 PostgreSQL 集成测试，原因是本地未安装 `psycopg` 且没有 Docker CLI；因此本阶段保持进行中，待环境具备后完成联调验收。

### Phase 3: 社内文档上传与入库

- 目标：支持社内文档上传、版本管理与元数据追踪。
- 交付重点：上传 API、元数据表、存储策略、前端入口。

### Phase 4: 切分与检索基础

- 目标：实现文档切分、片段存储、Top-K 检索与引用输出。
- 交付重点：Chunk Pipeline、Retriever、来源引用。

### Phase 5: 审批 Workflow

- 目标：建立人工审批与自动分析结合的状态机。
- 交付重点：审批状态流转、日志、恢复与重试。

### Phase 6: 互联网检索能力

- 目标：受控接入互联网公开信息，补充市场与竞品证据。
- 交付重点：Search Provider、降级策略、来源可信度规则。

### Phase 7: LangChain + LangGraph 工作流整合

- 目标：形成可替换的 Tool / Retriever / Prompt / Workflow 分层。
- 交付重点：Chain 适配层、Workflow 组合层、ADR 与边界说明。

### Phase 8: 测试体系与流程图文档

- 目标：补齐自动化测试、人工验收、前后台流程图与架构文档。
- 交付重点：测试矩阵、架构图、数据流图、运行与排障文档。

## 长期规划

- 保持可运行、可验证、可维护。
- 持续偿还高优先级技术债。
- 重要架构变化记录到 `docs/DECISIONS.md`。
- 每个阶段结束后更新本路线图。

<!-- DOC-SYNC:START group=governance -->
## 文档同步块

- group: `governance`
- file: `retail-insight-ai/ROADMAP.md`
- self_sha256: `5bf39c8dbde1e5279088478951af2f3c02a4506bcbf3682403b3e45a02846cae`
- peers:
- `retail-insight-ai/TASK.md` | sha256=83a6ef1d9395a1c0026514c5d8fab074fb8428781ab712ad25764c1c82decc05 | # retail-insight-ai 当前任务 / 最后更新：2026-07-02 / ## 当前阶段 / Phase 2: Internal Knowledge Approval Agent
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
