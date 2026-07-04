# 项目总待办清单

最后更新：2026-07-04

## 项目目标

作为 retail-insight-ai 企业化改造的 handbook 镜像与讲解文档集合，持续同步任务、架构、测试方法、决策和变更历史。

## 当前阶段

Phase 4: Document Read API MVP

## Epic 0: Enterprise Platform Architecture Evolution

### Current State

当前 handbook 仍主要服务于 `Retail Insight AI` 这一零售分析领域参考实现。

### Target State

未来平台目标为：

`Enterprise Retail Intelligence Platform (ERIP)`

### Planned Tasks

- [ ] Architecture Freeze
- [ ] Directory Refactor
- [ ] Repository Abstraction
- [ ] Workflow Abstraction
- [ ] Provider Abstraction
- [ ] Documentation Standard
- [ ] Testing Standard

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
