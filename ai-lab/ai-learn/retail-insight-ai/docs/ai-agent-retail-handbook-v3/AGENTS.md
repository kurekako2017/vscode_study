# 项目规则

> **文档角色：** 活动 handbook 章节。若与文首 ERIP V1.0 摘要冲突，以源码 + `03_AI核心知识.md` 技术表 + 权威 Volume01 为准。历史阶段表述保留时仅作演进记录。

本 handbook 目录遵守 AI-LAB 全局规则，并服从主项目 `retail-insight-ai` 的文档治理规则。

## 跨项目文档同步

`ai-agent-retail-handbook-v3` 与 `retail-insight-ai` 通过 `ai-learn/scripts/sync_retail_handbook_docs.py` 维护同步块。

- 同步映射由 `doc-sync.manifest.json` 统一管理。
- 同步只维护文档末尾的 `DOC-SYNC` 区块，不覆盖正文。
- retail 侧文档变化后，运行同步器会刷新 handbook 侧对应文档。
- 当前主技术规范以主项目 `docs/` 为唯一维护入口，handbook 不再复制维护技术规范正文。

## 开发前

1. 阅读 `AGENTS.md`。
2. 阅读 `ROADMAP.md`。
3. 阅读 `docs/governance/PROJECT_BACKLOG.md`。
4. 阅读 `TASK.md`。

开发前还必须确认当前阶段、最高优先级任务、技术债和已知问题。

## 开发后

- 更新 `TASK.md`。
- 更新 `docs/governance/PROJECT_BACKLOG.md`。
- 更新 `docs/governance/CHANGELOG.md`。
- 架构变化必须更新 `docs/architecture/ARCHITECTURE.md`。
- 重要决策必须追加到 `docs/governance/DECISIONS.md`。
- 保留全部历史记录，不删除有价值内容。

## 发现新需求

先加入 Backlog，再开始开发。

## 文档治理

- handbook 根目录用于长期学习、面试、项目理解和长期总结。
- 主项目 `README.md` 是项目唯一总入口。
- 主项目 `docs/learning/` 是 API 学习和测试学习入口。
- 主项目 `docs/architecture/`、`docs/contracts/`、`docs/database/`、`docs/development/`、`docs/governance/` 是技术规范和治理记录入口。
- 不要因为文件看起来重复就直接删除。
- 如果需要合并，先迁移有价值内容，再把旧文件移动到 `docs/_archive_candidate/`。
