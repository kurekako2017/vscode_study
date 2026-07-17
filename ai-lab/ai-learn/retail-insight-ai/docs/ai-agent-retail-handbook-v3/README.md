# Retail Insight AI Handbook V3

本目录是 Retail Insight AI 的长期知识库、长期学习中心、长期面试中心和长期总结区。

项目简介、当前完成情况、完整 Markdown 导航和文档治理规则统一维护在主项目 [README.md](../../README.md)。handbook 不重复维护项目介绍，避免主入口和长期知识库出现两套口径。

## handbook 定位

- 面向学习、面试、项目理解和长期复盘。
- 保留 `01~12` 章节、`INTERVIEW_GUIDE`、`PROJECT_BIBLE`、`README`。
- 每日学习优先看 handbook 根目录。
- 技术规范以主项目 `docs/` 为唯一维护入口；旧镜像已移动到归档候选区。

## 学习路线

```text
README.md
↓
PROJECT_BIBLE.md
↓
01_日本AI项目实战.md
↓
03_AI核心知识.md
↓
04_日本现场开发.md
↓
05_TL代码审查.md
↓
06_学习路线.md
↓
08_架构图册.md
↓
09_系统设计书.md
↓
11_Project_Structure.md
```

配合主项目学习文档：

- [../../docs/learning/LEARNING_API_WALKTHROUGH.md](../../docs/learning/LEARNING_API_WALKTHROUGH.md)
- [../../docs/learning/TEST_CASES.md](../../docs/learning/TEST_CASES.md)
- [../../CODE_STUDY_GUIDE.md](../../CODE_STUDY_GUIDE.md)
- [../../VERIFY_CHECKLIST.md](../../VERIFY_CHECKLIST.md)

## 面试路线

```text
02_日本AI现场面试.md
↓
07_面试口头训练.md
↓
INTERVIEW_GUIDE.md
↓
10_Production_Roadmap.md
↓
12_ADR.md
```

面试准备时，先用主项目 README 确认当前实现边界，再用 handbook 训练日语表达和现场讲解。

## 知识路线

```text
PROJECT_BIBLE.md
↓
03_AI核心知识.md
↓
08_架构图册.md
↓
09_系统设计书.md
↓
10_Production_Roadmap.md
↓
12_ADR.md
```

这条路线用于长期复盘 AI Agent、FastAPI、Workflow、RAG、Approval、RBAC、Audit、Repository、Provider 等概念。

## 根目录文档

- [README.md](README.md)
- [AGENTS.md](AGENTS.md)
- [PROJECT_BIBLE.md](PROJECT_BIBLE.md)
- [01_日本AI项目实战.md](01_日本AI项目实战.md)
- [02_日本AI现场面试.md](02_日本AI现场面试.md)
- [03_AI核心知识.md](03_AI核心知识.md)
- [04_日本现场开发.md](04_日本现场开发.md)
- [05_TL代码审查.md](05_TL代码审查.md)
- [06_学习路线.md](06_学习路线.md)
- [07_面试口头训练.md](07_面试口头训练.md)
- [08_架构图册.md](08_架构图册.md)
- [09_系统设计书.md](09_系统设计书.md)
- [10_Production_Roadmap.md](10_Production_Roadmap.md)
- [11_Project_Structure.md](11_Project_Structure.md)
- [12_ADR.md](12_ADR.md)
- [INTERVIEW_GUIDE.md](INTERVIEW_GUIDE.md)

## 技术规范引用

技术规范统一放在主项目 `docs/`。handbook 不再复制维护一份技术规范正文。

- 查 API 合同看 [../../docs/contracts/API_CONTRACT.md](../../docs/contracts/API_CONTRACT.md)。
- 查架构看 [../../docs/architecture/ARCHITECTURE.md](../../docs/architecture/ARCHITECTURE.md)。
- 查事件合同看 [../../docs/contracts/EVENT_CONTRACT.md](../../docs/contracts/EVENT_CONTRACT.md)。
- 查错误码看 [../../docs/contracts/ERROR_CATALOG.md](../../docs/contracts/ERROR_CATALOG.md)。
- 查数据库看 [../../docs/database/DATABASE.md](../../docs/database/DATABASE.md)。
- 查项目变更看 [../../docs/governance/CHANGELOG.md](../../docs/governance/CHANGELOG.md)。
- 查 backlog 看 [../../docs/governance/PROJECT_BACKLOG.md](../../docs/governance/PROJECT_BACKLOG.md)。

旧技术规范镜像已经移动到：

- [../_archive_candidate/handbook-docs/](../_archive_candidate/handbook-docs/)
- [../_archive_candidate/handbook-root/TASK.md](../_archive_candidate/handbook-root/TASK.md)
- [../_archive_candidate/handbook-root/ROADMAP.md](../_archive_candidate/handbook-root/ROADMAP.md)

## 维护规则

- 不要因为文件看起来重复就删除。
- 如果需要合并，先把有价值内容合并到唯一主文档。
- 已完成内容迁移的旧文档只能移动到 [../_archive_candidate/](../_archive_candidate/)。
- 不能直接删除。
- `handbook/docs` 中与主 `docs/` 重复的内容已经移动到归档候选区，不继续分叉维护。

## 文档同步

同步块只负责附录元数据，不覆盖正文学习内容。

- 同步映射由 `doc-sync.manifest.json` 管理。
- 即使存在镜像文档，也不能因为“内容相似”就直接删除任一文件。

## 更新日志

- V3: 建立 Retail Insight AI 统一世界观和一本书结构。
- Governance V2: handbook README 调整为长期知识库入口，不重复维护主项目介绍。
- Governance V2 Final: handbook 技术规范镜像改为引用主 `docs/`，旧镜像移动到归档候选区。

<!-- DOC-SYNC:START group=overview -->
## 文档同步块

- group: `overview`
- file: `ai-agent-retail-handbook-v3/README.md`
- self_sha256: `572e4166668f669ef002b0a0610c3d745b2b1529531a036afd19453db289a826`
- peers:
- `retail-insight-ai/README.md` | sha256=51340b3878b7fccbd5a7bdcdcbc2ed0f4c0bab07fae94fe85b1ddfd54eeca283 | # Retail Insight AI / ## 明天先做什么 / 1. 运行 `check_env` / 2. 启动 Backend
- `ai-agent-retail-handbook-v3/PROJECT_BIBLE.md` | sha256=e1dc1118cf4a13b542ad81cdd9bfc63a872af5a6fc7ec93430d44ea5cead5860 | # PROJECT_BIBLE / 本文件是 `ai-agent-retail-handbook-v3` 的唯一最高规则，也是 Retail Insight AI 的统一世界观。所有正文文档必须引用并遵守本文件。 / # 项目名称 / Retail Insight AI
- `ai-agent-retail-handbook-v3/02_日本AI现场面试.md` | sha256=713cdb0ae9c24284a5c62cbad95a808bf2bb530f2db5c514aae34e871dea816d | # 02_日本AI现场面试 / ## 目录 / - [第一章 面试表达总则](#第一章-面试表达总则) / - [第二章 自我介绍](#第二章-自我介绍)
- `ai-agent-retail-handbook-v3/07_面试口头训练.md` | sha256=af984812e08556e127ee61023203fc8e85957a971fe9c307a287dae27cd30fbe | # 07_面试口头训练 / 本文件只用于开口训练。练习时先遮住回答，听完问题后立即开口；说完再对照关键词，不逐字追求一致。 / ## 第一章 30秒回答训练 / ### 1. 自己紹介をお願いします。

说明：

- 这个块由 `scripts/sync_retail_handbook_docs.py` 自动维护。
- 只同步这个块，不覆盖各自正文。
- 任一组内文档正文变化时，整组文档的同步块都会一起刷新。
<!-- DOC-SYNC:END group=overview -->

## V1.0 文档批次（增量索引）

| 批次 | 内容 | 位置 |
|---|---|---|
| 第一批 | 启动/测试/验收 | `docs/learning/01_Foundation/RUNBOOK_LOCAL.md`、`TEST_CASES.md`、根 `VERIFY_CHECKLIST.md`（冻结） |
| 第二批 | 面试材料 | `INTERVIEW_GUIDE.md`、`02`、`07`、两份 Volume（冻结） |
| 第三批 | 入口/架构/学习/治理同步 | 根 README、ROADMAP、ARCHITECTURE、学习指南、本 handbook 索引、governance |

业务链：`文書管理→RAG検索→AI分析(low_cost)→董事会报告(high_quality)→承認管理→Persistent Audit`。
