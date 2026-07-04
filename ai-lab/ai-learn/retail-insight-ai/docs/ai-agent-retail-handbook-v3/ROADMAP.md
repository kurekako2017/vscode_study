# ai-agent-retail-handbook-v3 Roadmap

最后更新：2026-07-04

## 当前阶段

Phase 2: PostgreSQL Persistence MVP Sync

当前状态：

- Code implemented
- InMemory path verified
- PostgreSQL schema implemented
- PostgreSQL repository tests prepared
- PostgreSQL real integration test pending
- Status: In Progress / Partially Verified

## Project Positioning

### Current State

当前项目名称：

`Retail Insight AI`

当前定位：

`Retail Analysis Domain Reference Implementation`

### Target State

未来平台目标：

`Enterprise Retail Intelligence Platform (ERIP)`

### Planned

handbook 后续所有路线图描述都必须显式区分 Current State、Target State 和 Planned。

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

- [ ] Architecture Freeze
- [ ] Directory Refactor
- [ ] Repository Abstraction
- [ ] Workflow Abstraction
- [ ] Provider Abstraction
- [ ] Documentation Standard
- [ ] Testing Standard

## Epic 12: Retrieval and RAG Platform

### Current State

当前 handbook 还未把 Retrieval and RAG Platform 作为独立横向平台能力展开。

### Target State

未来 Epic 12 覆盖结构化业务检索、社内文档检索、互联网检索、上下文合并、引用与风险控制。

### Planned

当前将 Epic 12 作为横向平台能力标记，不表示已经实现完整 RAG 平台。

## Phase 1 Sync: 文件化输入基础

### Current State

主项目已完成本地 CSV / JSON / Markdown 文件输入的第一轮实现。

### Target State

文件输入成为 PostgreSQL、Approval Workflow、Document Upload 之前的稳定输入边界。

### Planned

- 当前 Report 状态为 `generated`
- 后续扩展：
  `draft / pending_approval / approved / rejected / revised`

## Phase 1.5 Sync: Contract Freeze and Approval Design

### Current State

主项目已完成 Phase 1.5 文档冻结。

### Target State

Data Contract、Import Error Model、Approval State Machine 成为 Phase 2 设计输入。

### Planned

- 当前只实现 `generated`
- 后续扩展：
  `draft / pending_approval / approved / rejected / revised / published / archived`

## Phase 2 Sync: PostgreSQL Persistence MVP

### Current State

主项目已完成 PostgreSQL Repository MVP，并保持 `inmemory` 为默认后端。

### Target State

Task、Event、Report 有可选事务持久化能力，同时 Approval / Import 为后续 Phase 预留稳定表结构。

### Planned

- 当前未完成真实 PostgreSQL 联调验收
- 当前未实现 Approval API、Import API、Document Search、RAG、Internet Search
- 当前环境缺少 Docker CLI
- 当前环境未安装 `psycopg` 到实际运行 venv
- PostgreSQL 集成测试当前被 skip

## Definition of Done

任何一个 Phase 只有在以下项目全部满足后，才能标记完成：

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

1. 将 retail-insight-ai 的 Phase 1 到 Phase 8 规划同步映射到 handbook。
2. 为测试文档和架构文档建立固定模板与缺失章节。
3. 将 CHANGELOG 和 DECISIONS 作为每次功能变更的强制同步入口。

## Handbook 同步路线

1. 主项目 Phase 规划更新
2. handbook 任务、Backlog、Roadmap 同步
3. handbook 架构、系统设计、生产路线图同步
4. handbook CHANGELOG 与 DECISIONS 同步
5. 通过同步门禁后才允许关闭主项目 Phase

## 长期规划

- 保持可运行、可验证、可维护。
- 持续偿还高优先级技术债。
- 重要架构变化记录到 `docs/DECISIONS.md`。
- 每个阶段结束后更新本路线图。

<!-- DOC-SYNC:START group=governance -->
## 文档同步块

- group: `governance`
- file: `ai-agent-retail-handbook-v3/ROADMAP.md`
- self_sha256: `8bea54fca33668303cb3ebc6a86e9fb359d814605450746eb7575075bc4600cf`
- peers:
- `retail-insight-ai/ROADMAP.md` | sha256=5bf39c8dbde1e5279088478951af2f3c02a4506bcbf3682403b3e45a02846cae | # retail-insight-ai Roadmap / 最后更新：2026-06-29 / ## 当前阶段 / 待根据项目现状确认。
- `retail-insight-ai/TASK.md` | sha256=83a6ef1d9395a1c0026514c5d8fab074fb8428781ab712ad25764c1c82decc05 | # retail-insight-ai 当前任务 / 最后更新：2026-07-02 / ## 当前阶段 / Phase 2: Internal Knowledge Approval Agent
- `retail-insight-ai/docs/PROJECT_BACKLOG.md` | sha256=b1dd8a6cee6a7fc07965026b8aefe8c9c8f08669871abd5ce2b8eb3dc1d5d477 | # retail-insight-ai Project Backlog / 最后更新：2026-07-02 / ## 项目目标 / 构建企业级 Retail Insight AI 平台，包含：
- `retail-insight-ai/docs/CHANGELOG.md` | sha256=cf9c2939e3369aa13c65a636fb64c44d56b672866b23771cf1dda5f1dbe755b3 | # retail-insight-ai CHANGELOG / ## 2026-07-02 / - 建立 retail-insight-ai 与 ai-agent-retail-handbook-v3 的跨项目文档同步机制。 / - 新增 `../scripts/sync_retail_handbook_docs.py` 与 `../doc-sync.manifest.json`。
- `ai-agent-retail-handbook-v3/TASK.md` | sha256=8375c8be41775af3f492dbc66e69653096db6bcdc4838d411eacf72cd81d5c82 | # 当前任务 / 最后更新：2026-07-02 / ## 当前阶段 / 待确认
- `ai-agent-retail-handbook-v3/docs/PROJECT_BACKLOG.md` | sha256=4b25c1fa793fa7ce50f3cc87341c8136603a8fc0eeae44e3b57dfcfd17f4dfc7 | # 项目总待办清单 / 最后更新：2026-07-02 / ## 项目目标 / 待确认
- `ai-agent-retail-handbook-v3/docs/CHANGELOG.md` | sha256=db921303a94dca1268fc38339f4c13606461269c65ca79c1de024cc1d36601c3 | # CHANGELOG / ## 2026-07-02 / - 建立 ai-agent-retail-handbook-v3 与 retail-insight-ai 的跨项目文档同步机制。 / - 新增 `../scripts/sync_retail_handbook_docs.py` 与 `../doc-sync.manifest.json`。
- `ai-agent-retail-handbook-v3/10_Production_Roadmap.md` | sha256=d904e6883e84c4bb5adda4d7adab4499e1e0f6f5e52bf97f46ecd7150271e64e | # 10_Production_Roadmap / # 目录 / - [1. Roadmap 原则](#1-roadmap-原则) / - [2. Level 1 Demo](#2-level-1-demo)

说明：
- 这个块由 `scripts/sync_retail_handbook_docs.py` 自动维护。
- 只同步这个块，不覆盖各自正文。
- 任一组内文档正文变化时，整组文档的同步块都会一起刷新。
<!-- DOC-SYNC:END group=governance -->
