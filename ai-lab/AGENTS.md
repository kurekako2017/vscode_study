# ai-lab Codex Root Rules

> 放置位置：`ai-lab/AGENTS.md`
>
> 作用：作为整个 `ai-lab` 仓库的最上层规则。这里不要写太多技术细节，只负责规则继承、目录判断和输出要求。

---

## 1. 规则优先级

Codex 执行任务时，必须按以下顺序读取规则：

```text
当前项目目录 AGENTS.md
>
技术方向目录 AGENTS.md
>
ai-learn/AGENTS.md
>
ai-lab/AGENTS.md
```

如果多个规则冲突，以更靠近当前工作目录的 `AGENTS.md` 为准。

---

## 2. ai-learn 任务识别

只要任务涉及以下内容，默认属于 `ai-learn/` 范围：

- AI Agent
- RAG
- LangChain
- LangGraph
- MCP
- Tool Calling
- Retriever
- Chunk
- Embedding
- Vector Store / VectorDB
- Ollama
- OpenAI / Azure OpenAI
- FastAPI + React AI 项目
- retail-insight-ai
- internal-knowledge-approval-agent
- ai-agent-retail-handbook-v3

涉及这些任务时，Codex 必须继续读取并遵守：

```text
ai-learn/AGENTS.md
```

---

## 3. 默认工作目录

AI 学习、Agent 项目、RAG 项目、LangGraph 项目，默认应在：

```text
ai-lab/ai-learn/
```

下执行。

不要在 `ai-lab` 根目录直接生成学习项目代码，除非用户明确要求。

---

## 4. 修改前必须检查

开始修改前，Codex 必须优先检查：

```text
README.md
PROJECT_BIBLE.md
当前项目 AGENTS.md
ai-learn/AGENTS.md
```

如果用户明确禁止修改某些目录，必须严格遵守。

---

## 5. 禁止行为

- 不要忽略 `ai-learn/AGENTS.md`
- 不要把所有规则都复制到根目录
- 不要修改用户明确禁止的目录
- 不要为了“整理”而删除已有学习资料
- 不要自动接入真实 API Key、真实 LLM、真实外部服务

---

## 6. 输出要求

每次完成任务后，必须说明：

1. 修改了哪些文件
2. 新增了哪些文件
3. 没有修改哪些被保护目录
4. 如何启动
5. 如何测试
6. 当前实现边界
7. 下一步建议

# AI-LAB 全局项目管理规则

本工作区下的所有项目都必须采用统一项目管理结构。

每个项目必须包含：

- AGENTS.md
- README.md
- TASK.md
- docs/PROJECT_BACKLOG.md
- docs/CHANGELOG.md

统一定义：

- `docs/PROJECT_BACKLOG.md`：永久任务清单，保存全部已完成与未完成任务。
- `TASK.md`：当前任务，描述当前阶段和本次最高优先级工作。
- `docs/CHANGELOG.md`：修改历史，按日期记录项目变更。

每次开始开发前，必须按顺序阅读：

1. 当前项目的 AGENTS.md
2. 当前项目的 docs/PROJECT_BACKLOG.md
3. 当前项目的 TASK.md

开始编码前必须确认：

- 当前阶段
- 未完成任务
- 技术债
- 已知问题
- 本次最高优先级任务

禁止不检查 Backlog 就直接开始编码。

每次完成工作后，必须更新：

- docs/PROJECT_BACKLOG.md
- TASK.md
- docs/CHANGELOG.md

必须记录：

- 已完成任务
- 未完成任务
- 新发现任务
- 新发现问题
- 下一步建议

如果项目没有 docs/PROJECT_BACKLOG.md：

必须先创建，再继续开发。

如果项目没有 TASK.md：

必须根据当前最高优先级任务创建。

如果项目没有 docs/CHANGELOG.md：

必须创建基础 CHANGELOG.md，用于记录完成历史。

## 任务状态与历史保护

- 禁止删除未完成任务。
- 完成任务时，将状态从 `[ ]` 改为 `[x]`。
- 已完成任务必须保留，不得为了缩短清单而删除。
- Backlog、TASK 和 CHANGELOG 中的历史记录必须持续保留。
- 发现新任务或新问题时，先登记到 `docs/PROJECT_BACKLOG.md`，再开始开发。

## 新项目初始化规则

在 `ai-lab` 下初始化新项目时，必须自动创建并填写：

1. `AGENTS.md`
2. `README.md`
3. `TASK.md`
4. `docs/PROJECT_BACKLOG.md`
5. `docs/CHANGELOG.md`

上述治理文件创建完成并检查 Backlog 后，才允许开始项目编码。

本规则适用于 ai-lab 下所有项目，除非用户明确说明某个项目不适用。

# Universal Project Governance

本规则适用于 `ai-lab` 下所有项目。

---

## 项目标准结构

每个项目必须包含：

```text
AGENTS.md
README.md
TASK.md
docs/
├── PROJECT_BACKLOG.md
└── CHANGELOG.md
```

---

## 工作开始规则

开始任何任务前必须读取：

1. `AGENTS.md`
2. `README.md`
3. `docs/PROJECT_BACKLOG.md`
4. `TASK.md`

如果文件不存在，必须报告缺失文件。

禁止直接开始编码。

---

## 工作结束规则

完成任务后必须更新：

1. `TASK.md`
2. `docs/PROJECT_BACKLOG.md`
3. `docs/CHANGELOG.md`

任务状态：

- 已完成：`[x]`
- 未完成：`[ ]`

不得删除历史记录。

---

## 项目状态检查

当用户输入“项目状态检查”时，必须读取：

1. `AGENTS.md`
2. `README.md`
3. `docs/PROJECT_BACKLOG.md`
4. `TASK.md`
5. `docs/CHANGELOG.md`

输出：

```text
# 项目状态检查报告

1. 项目名称
2. 当前阶段
3. 已完成项目
4. 进行中项目
5. 未完成项目
6. 下一步推荐
7. 风险检查
8. 文档覆盖率
9. 数据完整性检查
10. 总结
```

---

## Backlog 管理规则

`docs/PROJECT_BACKLOG.md` 是永久任务清单。

- 禁止删除任务。
- 完成任务时将 `[ ]` 改为 `[x]`。
- 必须保留全部历史。

---

## Task 管理规则

`TASK.md` 记录当前 Sprint，包括：

- 当前任务
- 下一任务
- 阻塞事项

---

## ChangeLog 管理规则

`docs/CHANGELOG.md` 必须记录：

- 日期
- 修改内容
- 影响文件

---

## 项目恢复规则

如果用户说：

- 继续开发
- 继续项目
- 恢复上下文
- 继续上次任务

则自动执行：

1. 项目状态检查
2. 读取 `docs/PROJECT_BACKLOG.md`
3. 读取 `TASK.md`
4. 给出下一步建议

---

## 新项目初始化规则

创建新项目时自动创建：

```text
AGENTS.md
README.md
TASK.md
docs/
├── PROJECT_BACKLOG.md
└── CHANGELOG.md
```

---

## 禁止事项

禁止：

- 删除 Backlog
- 删除 CHANGELOG
- 删除历史任务
- 直接覆盖 README

必须采用追加或保留历史的更新方式。

保留项目历史。

# AI-LAB Project Governance V2

AI-LAB 下所有正式项目统一采用 V2 结构：

```text
project/
├── AGENTS.md
├── README.md
├── TASK.md
├── ROADMAP.md
└── docs/
    ├── PROJECT_BACKLOG.md
    ├── CHANGELOG.md
    ├── ARCHITECTURE.md
    └── DECISIONS.md
```

其中：

- `ROADMAP.md` 记录当前阶段、下一阶段和长期规划。
- `docs/ARCHITECTURE.md` 记录技术架构、系统架构、Agent、RAG 和 MCP 流程。
- `docs/DECISIONS.md` 保存 ADR，记录决策、原因、备选方案和影响。

开发前必须依次读取：

1. 当前项目的 `AGENTS.md`
2. 当前项目的 `ROADMAP.md`
3. 当前项目的 `docs/PROJECT_BACKLOG.md`
4. 当前项目的 `TASK.md`

开发结束后必须同步更新 TASK、Backlog 和 CHANGELOG；发生架构变化或重要技术决策时，还必须更新 ARCHITECTURE 和 DECISIONS。
