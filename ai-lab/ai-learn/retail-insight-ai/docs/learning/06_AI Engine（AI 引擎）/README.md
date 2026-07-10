# Retail Insight AI 企业源码架构手册

# Volume 06：AI Engine（AI 引擎）

> Understand How Enterprise AI Systems Work

---

# 文档信息

| 项目         | 内容                   |
| ------------ | ---------------------- |
| Volume       | 06                     |
| 名称         | AI Engine              |
| 学习重点     | Enterprise AI Workflow |
| 推荐程度     | ⭐⭐⭐⭐⭐             |
| 建议阅读时间 | 2～3 天                |

---

# 本册定位

从 Volume 06 开始，我们正式进入 **AI Engine（AI 引擎）**。

前五册主要学习：

- FastAPI
- Repository
- BackgroundTasks
- Workflow
- Enterprise Architecture

本册开始，不再介绍 Web 开发基础，而是深入研究企业 AI 系统的核心能力，包括：

- AI Workflow
- LangChain
- LangGraph
- Prompt Engineering
- RAG
- Vector Search
- Streaming
- MCP
- Multi-Agent

本册重点不是学习某个框架的 API，而是理解 **Enterprise AI Engine 的设计思想**，并结合 Retail Insight AI 项目分析其未来演进方向。

---

# 学习目标

完成本册后，你应该能够：

- 理解 Enterprise AI Engine 的整体架构
- 理解 LangChain 与 LangGraph 的职责分工
- 掌握 Prompt Engineering 的设计原则
- 理解 RAG、Embedding 与 Vector Search
- 理解 MCP 与企业 Tool Integration
- 理解 Multi-Agent 的协作模式
- 设计企业级 AI Workflow

---

# 推荐阅读顺序

建议按以下顺序阅读：

```text
36_AI_Architecture

↓

37_LangChain_Architecture

↓

38_LangGraph_Architecture

↓

39_AI_State_Management

↓

40_AI_Node_Execution

↓

41_Prompt_Engineering

↓

42_RAG_Architecture

↓

43_Vector_Search

↓

44_AI_Streaming

↓

45_MCP_Architecture

↓

46_Multi_Agent

↓

47_Enterprise_AI_Best_Practice
```

每一章都建立在上一章的基础之上，建议不要跳读。

---

# 本册目录

| Chapter | 文件                        | 学习重点              |
| ------- | --------------------------- | --------------------- |
| 36      | AI Architecture             | AI Engine 总体架构    |
| 37      | LangChain Architecture      | LLM 调用抽象          |
| 38      | LangGraph Architecture      | AI Workflow           |
| 39      | AI State Management         | State 管理            |
| 40      | AI Node Execution           | Node 生命周期         |
| 41      | Prompt Engineering          | Prompt 设计           |
| 42      | RAG Architecture            | 企业知识检索          |
| 43      | Vector Search               | Embedding 与 pgvector |
| 44      | AI Streaming                | Token Streaming、SSE  |
| 45      | MCP Architecture            | Tool Integration      |
| 46      | Multi-Agent                 | 多 Agent 协作         |
| 47      | Enterprise AI Best Practice | 企业 AI 平台          |

---

# 阅读方式

建议采用以下学习流程：

```text
阅读 Markdown

↓

打开 VS Code

↓

阅读源码

↓

运行程序

↓

Learning Trace

↓

Console Log

↓

验证执行流程
```

理论与源码结合，效果最佳。

---

# 与前五册关系

整个学习路线如下：

```text
Volume 01

Foundation
（认识项目）

↓

Volume 02

Source Code
（认识源码）

↓

Volume 03

Subsystem
（理解模块）

↓

Volume 04

Execution Flow
（理解调用流程）

↓

Volume 05

Enterprise
（理解企业架构）

↓

Volume 06

AI Engine
（理解 AI 引擎）
```

本册是在前五册基础上的进一步提升。

---

# 学习建议

建议阅读每一章时：

1. 阅读本章理论
2. 打开对应源码
3. 跟踪 Learning Trace
4. 观察 Console Log
5. 思考企业扩展方案
6. 完成本章练习

建议不要只阅读 Markdown，而是配合源码一起学习。

---

# 面试准备

完成本册后，建议能够独立回答以下问题：

- 什么是 AI Engine？
- LangChain 与 LangGraph 有什么区别？
- Workflow 为什么需要 State？
- 为什么企业需要 RAG？
- 为什么使用 Vector Search？
- MCP 的作用是什么？
- Multi-Agent 与 Single-Agent 有什么区别？
- 企业 AI Platform 应具备哪些能力？

这些都是日本 AI Agent 岗位的高频问题。

---

# 学习成果

完成 Volume 06 后，你将掌握：

- ✅ AI Architecture
- ✅ LangChain
- ✅ LangGraph
- ✅ Workflow State
- ✅ Node Execution
- ✅ Prompt Engineering
- ✅ RAG
- ✅ Vector Search
- ✅ AI Streaming
- ✅ MCP
- ✅ Multi-Agent
- ✅ Enterprise AI Best Practice

你将能够理解现代 Enterprise AI Platform 的整体设计思路，并具备进一步学习 AI Agent、RAG 系统和企业 AI 平台的基础。

---

# 下一册

**Volume 07：Interview（日本 AI Agent 面试指南）**

主要内容：

- AI Agent 高频面试题
- LangChain 面试题
- LangGraph 面试题
- RAG 面试题
- MCP 面试题
- Multi-Agent 面试题
- 企业 AI 架构设计题
- 日本 SES AI 项目表达技巧

---

# 本册总结

一句话：

```text
Workflow

组织 AI

↓

LangGraph

控制流程

↓

LangChain

调用能力

↓

RAG

提供知识

↓

MCP

连接工具

↓

Multi-Agent

分工协作

↓

Enterprise AI Platform
```

**Volume 06 的目标不是学习某一个 AI 框架，而是建立完整的 Enterprise AI Engine 架构思维。**

完成本册后，你已经能够从源码、架构和企业实践三个角度理解现代 AI 系统，为后续的 AI Agent 面试和企业项目开发打下坚实基础。
