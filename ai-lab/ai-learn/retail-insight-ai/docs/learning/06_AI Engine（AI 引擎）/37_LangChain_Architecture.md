# ERIP 企业源码架构手册

# Volume 06：AI Engine（AI 引擎）

# Chapter 37

# LangChain Architecture（LangChain 架构）

> Build LLM Applications with Reusable Components

---

# 文档信息

| 项目     | 内容                            |
| -------- | ------------------------------- |
| Volume   | 06                              |
| Chapter  | 37                              |
| 技术主题 | LangChain Architecture          |
| 难度     | ⭐⭐⭐⭐⭐                      |
| 推荐程度 | ⭐⭐⭐⭐⭐                      |
| 对应源码 | providers / workflow / graph.py |

---

# 学习目标

阅读本章后，你应该能够回答：

- LangChain 在企业 AI 系统中的作用是什么？
- ERIP 如何组织 LLM 调用？
- Prompt、LLM、Tool、Retriever 的关系是什么？
- 为什么企业很少直接调用 OpenAI SDK？

---

# 一、为什么需要 LangChain？

最简单的 LLM 调用方式：

```python
response = client.chat.completions.create(...)
```

对于 Demo 已经足够。

但是企业项目通常需要：

- Prompt 管理
- 多模型切换
- Tool Calling
- Memory
- RAG
- Structured Output
- Retry
- Logging

如果全部写在一个函数中：

代码会越来越复杂。

因此需要一层统一抽象。

---

# 二、LangChain 在 AI Engine 中的位置

ERIP 的 AI Engine 可以抽象为：

```text
Workflow
    │
    ▼
Prompt Builder
    │
    ▼
LLM Provider
    │
    ▼
Structured Result
```

LangChain 主要负责：

- Prompt
- Model
- Tool
- Retriever
- Output Parser

而 Workflow 负责流程控制。

---

# 三、Current（ERIP 当前实现）

目前项目已经具备：

```text
TaskService

↓

AnalysisWorkflow

↓

Provider

↓

LLM
```

虽然没有完全依赖 LangChain，

但整体架构已经符合：

Workflow

↓

LLM Layer

↓

Result

的设计思想。

未来可以逐步替换为：

```text
LangGraph

↓

LangChain

↓

LLM Provider
```

无需修改 Workflow。

---

# 四、Source Binding（源码绑定）

建议阅读：

```text
backend/app/workflow/graph.py

↓

backend/app/services/task_service.py

↓

backend/app/providers/
```

重点观察：

- Prompt 在哪里生成？
- Provider 在哪里调用？
- Result 如何返回？

---

# 五、LangChain 核心组件

企业项目通常包含：

```text
PromptTemplate

↓

ChatModel

↓

Tool

↓

Retriever

↓

OutputParser
```

每个组件职责单一。

避免把所有逻辑写在一个函数里。

---

# 六、Workflow 与 LangChain 的关系

很多人误认为：

LangChain = Workflow。

实际上：

```text
LangGraph

↓

Workflow

↓

Node

↓

LangChain

↓

LLM
```

Workflow 控制流程。

LangChain 完成每个节点的 AI 能力。

两者互补。

---

# 七、Architecture Thinking

为什么企业不直接调用：

```python
client.chat.completions.create()
```

因为：

今天只有 OpenAI。

明天可能切换：

- Azure OpenAI
- Gemini
- Claude
- NVIDIA NIM
- OpenRouter

如果业务层直接依赖 SDK，

所有代码都要修改。

因此：

企业通常增加：

LLM 抽象层。

---

# 八、Java / Spring 对照

| Retail Insight AI | Spring AI      |
| ----------------- | -------------- |
| Provider          | ChatClient     |
| Prompt Builder    | PromptTemplate |
| Workflow          | AI Flow        |
| Tool              | ToolCallback   |

---

# 九、VS Code 阅读路线

建议：

```text
graph.py

↓

Provider

↓

Prompt

↓

LLM

↓

Result
```

不要先研究 SDK。

先理解：

调用关系。

---

# 十、Current vs Enterprise

Current：

```text
Workflow

↓

Provider

↓

LLM
```

Enterprise：

```text
Workflow

↓

LangChain

↓

Model Router

↓

OpenAI

Claude

Gemini

OpenRouter
```

---

# 十一、企业扩展

未来可以增加：

- Prompt Library
- Tool Registry
- Retry Policy
- Model Router
- Cost Control
- Token Statistics

形成完整 LLM Platform。

---

# 十二、面试回答（中文）

为什么企业项目会采用 LangChain？

LangChain 提供了 Prompt、LLM、Tool、Retriever 等统一抽象，使业务代码不直接依赖具体模型 SDK。这样不仅便于切换模型，还可以快速接入 RAG、Tool Calling、Memory 等企业能力。

---

# 十三、面试回答（日文）

なぜ LangChain を利用するのですか。

LangChain は Prompt、LLM、Retriever、Tool を統一的に管理できます。業務ロジックが特定のモデル SDK に依存しないため、保守性・拡張性が向上します。

---

# 十四、日本 SES 常见追问

### Q：LangChain 和 OpenAI SDK 有什么区别？

OpenAI SDK：

负责调用模型。

LangChain：

负责组织模型调用。

它提供统一抽象，支持多模型、多工具、多检索方式。

---

# 十五、本章练习

请完成：

1. 阅读 `backend/app/providers/`
2. 阅读 `graph.py`
3. 思考 Provider 如何演进为 LangChain ChatModel。
4. 设计一个可以切换 OpenAI、Gemini、Claude 的 Provider 抽象。

---

# 十六、本章核心记忆图

```text
Workflow

↓

Prompt

↓

LangChain

↓

LLM

↓

Structured Result
```

---

# 本章总结

一句话：

> **LangChain 不是模型，而是企业 AI 应用的统一抽象层。**

它帮助 Workflow 与具体模型解耦，为企业 AI 平台提供可扩展、可维护的 LLM 调用能力。

---

# 下一章

**Chapter 38：LangGraph Architecture（LangGraph 架构）**

学习：

- Graph
- State
- Node
- Edge
- Conditional Edge
- Retail Insight AI 中的 AnalysisWorkflow
