# Codex Skills 使用教程（2026版）

## 一、你当前已安装的 Skills

```text
~/.codex/skills/

├── langgraph-teacher/
├── mcp-teacher/
├── rag-teacher/
└── ai-agent-architect/
```

每个 Skill 包含：

```text
SKILL.md
agents/openai.yaml
```

---

# 二、Skill 是什么

Skill 可以理解为：

- 专属专家提示词（Prompt）
- 工作流程（Workflow）
- 输出规范（Output Rules）
- 最佳实践约束（Best Practices）

作用：

```text
普通 Codex
↓
每次重新解释需求

Skill + Codex
↓
直接按预设规范工作
```

---

# 三、查看 Skills 是否加载成功

重启 VS Code 或 Codex。

在 Codex 中输入：

```text
请使用 langgraph-teacher 解释 StateGraph
```

如果自动：

- 使用 LangGraph
- 输出 Mermaid 图
- 输出 Python 示例

说明 Skill 已加载。

---

# 四、langgraph-teacher 使用教程

## 适用场景

- LangGraph 学习
- StateGraph
- Multi-Agent
- Workflow Agent

### 示例1

```text
使用 langgraph-teacher 教我 StateGraph
```

### 示例2

```text
使用 langgraph-teacher 实现天气 Agent
```

### 示例3

```text
使用 langgraph-teacher 解释 Node、Edge、State
```

### 示例4

```text
按照 langgraph-teacher 规范重构当前项目
```

---

# 五、mcp-teacher 使用教程

## 适用场景

- MCP 学习
- MCP Server
- MCP Client
- MCP Tool

### 示例1

```text
使用 mcp-teacher 创建 Python MCP Server
```

### 示例2

```text
使用 mcp-teacher 解释 MCP 架构
```

### 示例3

```text
使用 mcp-teacher 实现文件系统 MCP Server
```

### 示例4

```text
使用 mcp-teacher 实现数据库 MCP Tool
```

---

# 六、rag-teacher 使用教程

## 适用场景

- RAG
- Hybrid Search
- Rerank
- GraphRAG

### 示例1

```text
使用 rag-teacher 解释现代 RAG
```

### 示例2

```text
使用 rag-teacher 实现 Hybrid Search
```

### 示例3

```text
使用 rag-teacher 实现 Parent Document Retriever
```

### 示例4

```text
使用 rag-teacher 讲解 GraphRAG
```

---

# 七、ai-agent-architect 使用教程

## 适用场景

企业级 Agent 系统设计

### 示例1

```text
使用 ai-agent-architect 设计客服 Agent
```

### 示例2

```text
使用 ai-agent-architect 设计 Multi-Agent 系统
```

### 示例3

```text
使用 ai-agent-architect 设计 MCP + LangGraph 平台
```

### 示例4

```text
使用 ai-agent-architect 输出企业级项目结构
```

---

# 八、自动触发

很多时候不用手动写 Skill 名称。

例如：

```text
帮我实现一个 LangGraph 天气 Agent
```

Codex 可能自动触发：

```text
langgraph-teacher
```

例如：

```text
帮我实现 Hybrid Search
```

可能自动触发：

```text
rag-teacher
```

---

# 九、推荐工作流

## LangGraph 学习

```text
langgraph-teacher
↓
实现 Demo
↓
重构
↓
Mermaid 图
```

## MCP 学习

```text
mcp-teacher
↓
MCP Server
↓
MCP Client
↓
Tool
```

## RAG 学习

```text
rag-teacher
↓
Retriever
↓
Hybrid Search
↓
Rerank
↓
GraphRAG
```

---

# 十、最适合你的使用方式

你当前路线：

```text
LangChain 1.x
LangGraph
MCP
RAG
FastAPI
Multi-Agent
```

推荐优先级：

```text
★★★★★ langgraph-teacher
★★★★★ rag-teacher
★★★★☆ mcp-teacher
★★★★☆ ai-agent-architect
```

日常开发建议：

```text
写代码
→ langgraph-teacher

做RAG
→ rag-teacher

学MCP
→ mcp-teacher

做项目架构
→ ai-agent-architect
```

这样能最大化发挥你目前 ai-learn 项目的学习效率。
