# Codex Skill 制作教程（ai-learn 专用版）

## 1. 什么是 Codex Skill

Skill 可以理解为：

```text
一套可复用的专用能力包
```

它不是普通 README，而是给 Codex/AI 编程工具看的专项规则和工作流程。

例如你可以做：

- rag-teacher skill
- langgraph-teacher skill
- mcp-teacher skill
- ai-agent-architect skill
- code-reviewer skill

每个 Skill 都负责一种固定任务。

---

## 2. Skill 和 AGENTS.md 的区别

### AGENTS.md

适合放：

- 全项目长期规则
- 模型优先级
- README 规范
- 测试命令规范
- 目录结构规范

### Skill

适合放：

- 某一种专项任务的流程
- 某一种技术方向的教学方法
- 某一种代码生成模板
- 某一种检查清单

简单理解：

```text
AGENTS.md = 项目宪法
Skill = 专用工具人
```

---

## 3. 推荐 Skill 目录

你现在已经有类似目录：

```text
ai-learn/
└── .codex-skill-build/
    ├── ai-agent-architect/
    ├── langgraph-teacher/
    ├── mcp-teacher/
    └── rag-teacher/
```

推荐继续使用这个结构。

---

## 4. 一个标准 Skill 目录结构

```text
.codex-skill-build/
└── rag-teacher/
    ├── SKILL.md
    ├── templates/
    │   ├── README_TEMPLATE.md
    │   └── PROJECT_STRUCTURE.md
    └── examples/
        └── doc_qa_agent_example.md
```

最核心的是：

```text
SKILL.md
```

---

## 5. SKILL.md 基本模板

```md
# rag-teacher Skill

## 目标

你是一个 RAG 教学助手。

你的任务是帮助用户创建、解释、重构和检查 RAG 示例项目。

## 适用场景

当用户要求：

- 创建 RAG 示例
- 解释 Chunk
- 解释 Embedding
- 解释 Retriever
- 检查 RAG 项目
- 生成 RAG README

时，使用本 Skill。

## 工作原则

- 面向初学者
- 所有解释使用中文
- 代码必须能运行
- README 必须比代码更详细
- 必须同时支持真实模型和 Mock 模式

## 项目结构要求

每个 RAG 项目必须包含：

```text
README.md
main.py
loader.py
splitter.py
retriever.py
generator.py
mock.py
data/
tests/
```

## 必须解释的概念

- Document
- Chunk
- Embedding
- VectorStore
- Retriever
- Generation

## 测试命令要求

所有命令必须从 ai-learn 根目录执行。

OpenRouter：

```bash
python rag-lab/projects/demo/main.py --provider openrouter
```

NVIDIA：

```bash
python rag-lab/projects/demo/main.py --provider nvidia
```

Ollama：

```bash
python rag-lab/projects/demo/main.py --provider ollama
```

Mock：

```bash
python rag-lab/projects/demo/main.py --mock
```

## 输出要求

每次完成任务后，必须说明：

- 修改了哪些文件
- 如何运行
- 学到了什么
- 下一步可以怎么扩展
```

---

## 6. langgraph-teacher Skill 示例

```text
.codex-skill-build/
└── langgraph-teacher/
    └── SKILL.md
```

SKILL.md 内容重点：

```md
# langgraph-teacher Skill

## 目标

帮助用户学习 LangGraph。

## 必须解释

- State
- Node
- Edge
- Conditional Edge
- START
- END
- Graph Compile
- Invoke

## 示例项目必须包含

- README.md
- main.py
- state.py
- nodes.py
- graph.py
- mock.py

## README 必须包含

- 这个例子学什么
- Graph 执行流程
- 每个 Node 的作用
- State 如何变化
- 真实模型命令
- Mock 命令
```

---

## 7. mcp-teacher Skill 示例

```text
.codex-skill-build/
└── mcp-teacher/
    └── SKILL.md
```

重点规则：

```md
# mcp-teacher Skill

## 目标

帮助用户学习 MCP Server 和 MCP Client。

## 必须解释

- MCP Server
- MCP Client
- Tool
- Resource
- Prompt
- JSON Schema
- Tool Call

## 示例项目必须包含

- server.py
- client_demo.py
- tools.py
- README.md
- mock_client.py
```

---

## 8. ai-agent-architect Skill 示例

适合做企业级 Agent 项目设计。

重点规则：

```md
# ai-agent-architect Skill

## 目标

帮助用户设计企业级 Agent 项目。

## 必须关注

- 需求分析
- 角色设计
- Tool 设计
- Workflow 设计
- Memory 设计
- 日志设计
- 错误处理
- 测试设计
- README 文档

## 输出格式

必须输出：

1. 项目目标
2. 目录结构
3. 执行流程
4. 核心模块
5. 测试命令
6. 下一步扩展
```

---

## 9. 如何让 Codex 使用 Skill

在 Codex 里可以这样下指令：

```text
请使用 rag-teacher skill，帮我检查 rag-lab/projects/doc_qa_agent 是否符合教学项目规范。
```

或者：

```text
请使用 langgraph-teacher skill，在 langgraph-lab/projects 下创建一个最小可运行示例。
```

或者：

```text
请使用 ai-agent-architect skill，为我设计一个企业级 Doc QA Agent 项目。
```

---

## 10. Skill 和 AGENTS.md 如何配合

建议：

```text
AGENTS.md 负责全局规则
Skill 负责专项能力
```

例如：

```text
ai-learn/AGENTS.md
```

规定：

- OpenRouter → NVIDIA → Ollama → Mock
- README 结构
- 测试命令
- 所有命令从 ai-learn 根目录执行

```text
rag-teacher/SKILL.md
```

规定：

- RAG 项目怎么讲
- RAG 项目怎么拆文件
- RAG README 必须解释哪些概念

---

## 11. 推荐你的 Skill 清单

### 1. rag-teacher

用途：

- 创建 RAG 示例
- 解释 Chunk / Retriever / Embedding
- 检查 RAG 项目

### 2. langgraph-teacher

用途：

- 创建 LangGraph 示例
- 解释 State / Node / Edge
- 检查 Graph 流程

### 3. mcp-teacher

用途：

- 创建 MCP Server
- 创建 MCP Client
- 解释 Tool / Resource / Prompt

### 4. ai-agent-architect

用途：

- 设计企业级 Agent 项目
- 拆分模块
- 设计工具调用流程

### 5. code-review-teacher

用途：

- 检查代码是否适合初学者
- 检查 README 是否完整
- 检查测试命令是否齐全

---

## 12. Skill 制作步骤

### 第一步：创建目录

```bash
mkdir -p .codex-skill-build/rag-teacher
```

### 第二步：创建 SKILL.md

```bash
touch .codex-skill-build/rag-teacher/SKILL.md
```

### 第三步：写清楚目标

```md
## 目标

你是 RAG 教学助手。
```

### 第四步：写清楚适用场景

```md
## 适用场景

当用户要创建、解释、检查 RAG 项目时使用。
```

### 第五步：写清楚输出规则

```md
## 输出规则

必须输出修改文件、运行命令、学习重点。
```

### 第六步：测试 Skill

对 Codex 说：

```text
请使用 rag-teacher skill 创建一个最小 RAG 示例。
```

---

## 13. Skill 写作原则

好的 Skill 应该：

- 范围小
- 目标明确
- 输出格式固定
- 有检查清单
- 有项目模板
- 有测试命令
- 和 AGENTS.md 不重复太多

不要把所有内容塞进一个 Skill。

推荐：

```text
一个技术方向 = 一个 Skill
```

---

## 14. 最实用的 Skill 命令

### 创建项目

```text
请使用 langgraph-teacher skill 创建一个最小 LangGraph 示例。
```

### 检查项目

```text
请使用 rag-teacher skill 检查当前 RAG 项目是否适合初学者学习。
```

### 生成文档

```text
请使用 mcp-teacher skill 为当前 MCP 项目补全 README。
```

### 重构项目

```text
请使用 ai-agent-architect skill 重构当前 Agent 项目目录。
```

---

## 15. 推荐最终结构

```text
ai-learn/
├── AGENTS.md
├── .codex-skill-build/
│   ├── rag-teacher/
│   │   └── SKILL.md
│   ├── langgraph-teacher/
│   │   └── SKILL.md
│   ├── mcp-teacher/
│   │   └── SKILL.md
│   ├── ai-agent-architect/
│   │   └── SKILL.md
│   └── code-review-teacher/
│       └── SKILL.md
```

---

## 16. 总结

AGENTS.md 解决：

```text
整个项目应该怎么做
```

Skill 解决：

```text
某一类任务应该怎么做
```

你的 ai-learn 最佳组合：

```text
AGENTS.md
+
rag-teacher
+
langgraph-teacher
+
mcp-teacher
+
ai-agent-architect
+
code-review-teacher
```

这样 Codex 不只是“会写代码”，而是会按照你的学习路线持续生成统一风格的教学项目。
