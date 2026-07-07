# Retail Insight AI 日本 Agent 面试攻略 V1.0
## Volume 01 - 项目介绍与系统架构

> 适用对象：AI Agent / Python Backend / LLM Application / RAG 工程师岗位

---

# 1. 面试开场（60秒）

大家好，我最近参与开发的是 **Retail Insight AI** 项目。这是一个面向零售经营分析的 AI Agent 平台，采用 React + FastAPI 构建前后端，后端通过 TaskService 和 LangGraph 组织 AI Workflow，实现 KPI 分析、Research、报告生成以及实时任务状态推送。当前版本采用 Keyword Retrieval，未来规划升级到 LangChain + Embedding + pgvector 的 Semantic RAG 架构。

---

# 2. 项目概要（3分钟）

项目目标：

- 自动生成零售经营分析报告
- 固定 KPI 分析
- AI Research
- Agent Workflow
- 实时任务跟踪（SSE）

核心流程：

```text
React
  ↓
FastAPI
  ↓
Task API
  ↓
TaskService
  ↓
LangGraph Workflow
  ├── Fixed KPI Workflow
  └── Research Agent
        ↓
Context Builder
        ↓
Report Generator
        ↓
Repository
        ↓
SQLite(Current)
```

未来演进：

- LangChain（RAG）
- Embedding
- pgvector
- Hybrid Retrieval

---

# 3. 为什么选择 FastAPI？

回答模板：

FastAPI 在本项目主要承担 HTTP Boundary。

它负责：

- REST API
- OpenAPI
- 参数校验
- SSE

它不负责 Workflow，也不直接处理业务逻辑。

业务全部进入 TaskService，再交给 LangGraph。

这样可以保持 Controller 很薄，符合企业后台架构设计。

---

# 4. 为什么使用 TaskService？

TaskService 是 Application Service。

职责：

- 创建任务
- 调度 Workflow
- 调用 Repository
- 管理生命周期
- 生成报告

它隔离了 API 与 Workflow。

因此以后替换 Workflow 实现时，不影响 API。

---

# 5. 为什么使用 LangGraph？

回答模板：

LangGraph 负责 Workflow Orchestration。

原因：

- Workflow 有状态
- 节点可扩展
- 支持条件分支
- 后续可加入 Checkpoint / Interrupt

它非常适合 AI Agent。

注意：

LangGraph 不负责 RAG。

---

# 6. LangGraph 与 LangChain 的区别

LangGraph：

- Workflow
- State
- Node
- Edge
- Routing

LangChain（规划）：

- Retriever
- Prompt Builder
- Context Builder
- Tool Calling

一句话：

LangGraph 管流程。

LangChain 管知识。

---

# 7. 当前 RAG 设计

Current：

Keyword Retrieval

↓

Chunk

↓

Context Builder

↓

LLM

Target：

Keyword

+

Embedding

+

Vector Database

+

Hybrid Retrieval

+

Rerank

---

# 8. 面试官最可能追问

Q：为什么不用 LangChain 管整个系统？

A：

LangChain 更适合 RAG。

Workflow 更适合 LangGraph。

职责拆分更清晰。

---

Q：为什么不用 AutoGen？

A：

AutoGen 偏多 Agent 对话。

本项目更偏固定 Workflow，因此 LangGraph 更容易维护。

---

Q：为什么未来选择 pgvector？

A：

因为项目未来规划 PostgreSQL。

pgvector 可以直接复用 PostgreSQL，降低企业运维复杂度。

---

# 9. TL 总结版（30秒）

这个项目本质上是企业 AI Backend。

FastAPI 提供 API。

TaskService 编排业务。

LangGraph 管理 Workflow。

未来 LangChain 管理 RAG。

Repository 隔离数据库。

最终形成可持续演进的企业 AI 平台。

---

# 下一册预告

Volume 02：

《LangGraph 深挖》

包括：

- State
- Node
- Edge
- Conditional Edge
- Checkpoint
- Interrupt
- Workflow Design
- 日本 TL 高频追问
