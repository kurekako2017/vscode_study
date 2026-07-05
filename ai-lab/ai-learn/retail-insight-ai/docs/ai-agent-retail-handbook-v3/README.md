# Retail Insight AI Handbook V3

# 项目介绍

Retail Insight AI 是《日本 AI Agent 企业开发与面试宝典》V3 的统一项目。

日文名称：小売業向け AI 経営分析システム。

本目录所有内容都围绕 Retail Insight AI 展开。

## Project Positioning

### Current State

当前项目名称保持为：

`Retail Insight AI`

当前项目定位为：

`Retail Analysis Domain Reference Implementation`

### Target State

未来平台目标名称为：

`Enterprise Retail Intelligence Platform (ERIP)`

ERIP 是未来企业平台架构目标，不表示当前手册描述的是一个已存在的平台。

### Planned

本 handbook 需要持续记录：

- 当前 Retail Insight AI 的实现边界
- 面向 ERIP 的目标架构
- 从当前到目标的演进路径

不得把 ERIP 写成当前已实现现状。

如果你想先按“先启动、再看 Swagger、再学接口、再看测试、再看源码、最后准备面试”的顺序学习，先看 [README.md](../../README.md) 和 [RUNBOOK_LOCAL.md](../../RUNBOOK_LOCAL.md)。
再继续看 [docs/LEARNING_API_WALKTHROUGH.md](../../docs/LEARNING_API_WALKTHROUGH.md)、[docs/TEST_CASES.md](../../docs/TEST_CASES.md) 和 [INTERVIEW_GUIDE.md](./INTERVIEW_GUIDE.md)。

## handbook 根目录说明

handbook 根目录面向学习、面试和项目理解，是每天最先进入的地方。

根目录重点内容包括：

- `README.md`
- `PROJECT_BIBLE.md`
- `TASK.md`
- `ROADMAP.md`
- `01_日本AI项目实战.md`
- `02_日本AI现场面试.md`
- `03_AI核心知识.md`
- `04_日本现场开发.md`
- `05_TL代码审查.md`
- `06_学习路线.md`
- `07_面试口头训练.md`
- `08_架构图册.md`
- `09_系统设计书.md`
- `10_Production_Roadmap.md`
- `11_Project_Structure.md`
- `12_ADR.md`
- `INTERVIEW_GUIDE.md`

建议学习顺序：

```text
handbook/README.md
↓
handbook/PROJECT_BIBLE.md
↓
handbook/01_日本AI项目实战.md
↓
handbook/02_日本AI现场面试.md
↓
handbook/03_AI核心知识.md
↓
handbook/04_日本现场开发.md
↓
handbook/05_TL代码审查.md
↓
handbook/06_学习路线.md
↓
handbook/07_面试口头训练.md
↓
handbook/08_架构图册.md
↓
handbook/09_系统设计书.md
↓
handbook/10_Production_Roadmap.md
↓
handbook/11_Project_Structure.md
↓
handbook/12_ADR.md
↓
handbook/INTERVIEW_GUIDE.md
```

## handbook/docs 目录说明

`handbook/docs` 面向技术规范镜像和治理文档，不是每天学习主入口。

这里主要放：

- `ARCHITECTURE.md`
- `API_CONTRACT.md`
- `DATABASE.md`
- `ERROR_CATALOG.md`
- `EVENT_CONTRACT.md`
- `CHANGELOG.md`
- `PROJECT_BACKLOG.md`
- `MASTER_PROMPT.md`
- 其他与工程标准、历史记录、治理同步相关的文档

查技术细节时，先回到根目录确认学习入口，再进入 `handbook/docs` 看规范和镜像。

## 维护说明

- 每天学习先看 handbook 根目录。
- 查技术细节再进 `handbook/docs`。
- 不要随意移动文件。
- 不要因为“看起来重复”就删除文件。
- 如果需要合并，先在 README 中说明主入口，再逐步迁移，不能直接删除内容。

## 目录说明

- `PROJECT_BIBLE.md`: 全工程唯一世界观和最高规则
- `01_日本AI项目实战.md`: 项目、架构、职责、源码解析入口
- `02_日本AI现场面试.md`: 自我介绍、项目介绍、现场问答
- `03_AI核心知识.md`: FastAPI、LangGraph、Workflow、RAG、Streaming 等核心知识
- `04_日本现场开发.md`: 日本现场流程、设计、测试、部署、保守
- `05_TL代码审查.md`: TL Review、风险、改修建议
- `06_学习路线.md`: 学习路线、能力成长、复习顺序

## 文档同步

本手册与 [retail-insight-ai](../retail-insight-ai/README.md) 保持同步块联动，脚本位于 [ai-learn/scripts/sync_retail_handbook_docs.py](../scripts/sync_retail_handbook_docs.py)。

- 同步块只维护附录，不覆盖手册正文。
- 同步映射由 [doc-sync.manifest.json](../doc-sync.manifest.json) 管理。
- retail 侧文档更新后，刷新脚本即可让手册侧对应章节同步变化。

# 目录说明

- `PROJECT_BIBLE.md`: 全工程唯一世界观和最高规则
- `01_日本AI项目实战.md`: 项目、架构、职责、源码解析入口
- `02_日本AI现场面试.md`: 自我介绍、项目介绍、现场问答
- `03_AI核心知识.md`: FastAPI、LangGraph、Workflow、RAG、Streaming 等核心知识
- `04_日本现场开发.md`: 日本现场流程、设计、测试、部署、保守
- `05_TL代码审查.md`: TL Review、风险、改修建议
- `06_学习路线.md`: 学习路线、能力成长、复习顺序

# 推荐阅读顺序

1. `PROJECT_BIBLE.md`
2. `01_日本AI项目实战.md`
3. `02_日本AI现场面试.md`
4. `03_AI核心知识.md`
5. `04_日本现场开发.md`
6. `05_TL代码审查.md`
7. `06_学习路线.md`

# 如何维护

- 先维护 `PROJECT_BIBLE.md`
- 再维护对应正文 Markdown
- 不新增目录
- 不新增正文 Markdown
- 不拆分知识点
- 优先增加章节，不增加文件

# 更新日志

- V3: 建立 Retail Insight AI 统一世界观和一本书结构

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
