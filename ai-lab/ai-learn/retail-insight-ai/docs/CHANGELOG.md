# retail-insight-ai CHANGELOG

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
