# retail-insight-ai CHANGELOG

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
