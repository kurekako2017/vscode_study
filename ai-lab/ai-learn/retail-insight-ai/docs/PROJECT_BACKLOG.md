# retail-insight-ai Project Backlog

最后更新：2026-07-02

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

Phase 2: Internal Knowledge Approval Agent

状态：进行中

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

## 当前近期优先级

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

- [ ] RBAC
- [ ] JWT
- [ ] Audit Log
- [ ] Tenant Isolation

### Epic 7: Observability

- [ ] LangSmith / Langfuse 调研
- [ ] OpenTelemetry
- [ ] Metrics Dashboard
- [ ] Cost Tracking

## Technical Debt

### High

- [ ] Chunk Strategy 统一
- [ ] Embedding 抽象层
- [ ] Prompt 版本管理

### Medium

- [ ] API 统一返回格式
- [ ] 前端错误处理统一
- [ ] 初级学者友好注释补充

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
