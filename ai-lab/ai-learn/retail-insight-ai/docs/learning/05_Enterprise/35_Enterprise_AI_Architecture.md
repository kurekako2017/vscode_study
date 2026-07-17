# ERIP 企业源码架构手册
> **V1.0 校正：** 正式 Repository = **PostgreSQL + pgvector**。文中 SQLite 仅作历史/对比教学，不是当前主库。InMemory = unittest only。


# Volume 05：Enterprise（企业架构）

# Chapter 35

# Enterprise AI Architecture（企业 AI 架构）

> Build an Enterprise AI Platform

---

# 文档信息

| 项目     | 内容                                   |
| -------- | -------------------------------------- |
| Volume   | 05                                     |
| Chapter  | 35                                     |
| 技术主题 | Enterprise AI Architecture             |
| 难度     | ⭐⭐⭐⭐⭐                             |
| 推荐程度 | ⭐⭐⭐⭐⭐                             |
| 对应模块 | Workflow / LangChain / LangGraph / RAG |

---

# 学习目标

阅读本章后，你应该能够回答：

- 什么是 Enterprise AI Platform？
- ERIP 如何演进为企业 AI 平台？
- LangChain 与 LangGraph 分别负责什么？
- 为什么需要 RAG？
- pgvector、MCP、Multi-Agent 在企业中的定位是什么？

---

# 一、什么是 Enterprise AI？

很多初学者认为：

AI 系统就是：

```text
Prompt

↓

LLM

↓

Answer
```

实际上：

企业 AI 平台远不止如此。

真正的企业 AI 系统需要：

- 权限控制
- 工作流
- 企业知识库
- 审批流程
- 日志审计
- 数据持久化
- 多模型管理
- 多 Agent 协作

因此：

AI 只是其中一个能力。

真正的核心是：

> **AI Platform（AI 平台）**

---

# 二、ERIP 当前架构（Current）

当前项目：

```text
Browser

↓

FastAPI

↓

Workflow

↓

Repository

↓

SQLite

↓

LLM

↓

Report
```

已经具备：

- API
- Workflow
- Repository
- Learning Trace
- EventPublisher
- SSE

这是一个完整的 AI 应用。

---

# 三、Enterprise AI Platform（Target）

未来企业版建议：

```text
                 Browser
                     │
                     ▼
               API Gateway
                     │
                     ▼
                 FastAPI API
                     │
                     ▼
              Authentication
                     │
                     ▼
                  Workflow
                     │
         ┌───────────┼────────────┐
         ▼           ▼            ▼
     LangChain   Approval      Event Bus
         │           │            │
         ▼           ▼            ▼
       LangGraph   Audit Log   RabbitMQ
         │
         ▼
    RAG Retrieval
         │
 ┌───────┼─────────────┐
 ▼       ▼             ▼
PostgreSQL  pgvector  Redis
         │
         ▼
       LLM Provider
         │
         ▼
     AI Response
```

---

# 四、LangChain 的定位

LangChain：

负责：

连接：

AI 与外部资源。

例如：

```text
Prompt

↓

LLM

↓

Tools

↓

Retriever

↓

Memory
```

主要解决：

AI 如何使用：

外部能力。

---

# 五、LangGraph 的定位

LangGraph：

负责：

Workflow。

例如：

```text
State

↓

Node

↓

Edge

↓

Next Node
```

它负责：

组织：

整个 AI 流程。

而不是：

调用模型。

---

# 六、LangChain 与 LangGraph 的关系

很多新人容易混淆。

其实：

关系如下：

```text
LangGraph

负责：

Workflow

↓

Node

↓

LangChain

↓

LLM
```

LangGraph：

管理流程。

LangChain：

负责每个节点的 AI 能力。

两者互补。

---

# 七、RAG（Retrieval-Augmented Generation）

企业 AI：

不能只依赖模型训练数据。

还需要：

企业知识。

例如：

```text
Question

↓

Retriever

↓

Company Documents

↓

Prompt

↓

LLM
```

这样：

回答：

更加准确。

---

# 八、pgvector 的作用

Embedding：

不能：

直接：

保存：

普通数据库。

需要：

向量数据库。

当前建议：

```text
PostgreSQL

+

pgvector
```

优点：

- 部署简单
- 成本低
- 与业务数据统一管理

---

# 九、MCP（Model Context Protocol）

MCP 的目标：

统一：

AI 与外部工具通信。

例如：

```text
LLM

↓

MCP

↓

GitHub

↓

Slack

↓

Database

↓

Filesystem
```

未来：

Retail Insight AI：

也可以：

逐步支持：

MCP。

---

# 十、Multi-Agent

未来：

一个 Agent：

负责：

一个任务。

例如：

```text
Research Agent

↓

Planning Agent

↓

Analysis Agent

↓

Report Agent
```

多个 Agent：

共同完成：

企业任务。

---

# 十一、Architecture Thinking

为什么：

不用：

一个：

巨大 Prompt？

因为：

企业：

业务：

越来越复杂。

应该：

拆分：

多个：

Agent。

每个：

Agent：

职责单一。

---

# 十二、Current vs Enterprise

当前：

```text
Workflow

↓

LLM
```

企业版：

```text
Workflow

↓

LangGraph

↓

LangChain

↓

RAG

↓

LLM

↓

Approval

↓

Audit
```

整个：

AI：

真正：

企业化。

---

# 十三、Java / Spring 对照

| Enterprise AI | Java 对应            |
| ------------- | -------------------- |
| Workflow      | BPM Engine           |
| LangGraph     | Process Engine       |
| LangChain     | Service Layer        |
| RAG           | Search Service       |
| pgvector      | PostgreSQL Extension |
| MCP           | Integration Layer    |

---

# 十四、VS Code 阅读路线

建议：

```text
workflow/

↓

graph.py

↓

services/

↓

repositories/

↓

events/

↓

Learning Trace
```

理解：

整个：

AI 平台。

---

# 十五、企业扩展（Enterprise）

未来建议增加：

- PostgreSQL
- pgvector
- Redis
- RabbitMQ
- Kubernetes
- LangChain
- LangGraph
- MCP
- Multi-Agent
- OpenTelemetry

形成真正的：

Enterprise AI Platform。

---

# 十六、面试回答（中文）

什么是 Enterprise AI Platform？

Enterprise AI Platform 不只是调用大模型，而是围绕 AI 建立完整的平台能力，包括 Workflow、RAG、权限管理、审批、知识库、向量检索、事件驱动和可观测性。ERIP 当前已经具备 Workflow、Repository、EventPublisher 等基础能力，未来可以逐步引入 LangChain、LangGraph、pgvector、MCP 和 Multi-Agent，演进为完整的企业 AI 平台。

---

# 十七、面试回答（日语）

Enterprise AI Platform とは何ですか。

Enterprise AI Platform は LLM を呼び出すだけではありません。Workflow、RAG、Knowledge Base、Approval、Audit Log、Vector Database、Multi-Agent などを統合した企業向け AI システムです。Retail Insight AI もこの方向へ段階的に拡張できます。

---

# 十八、日本 SES 常见追问

### Q：LangChain 和 LangGraph 哪个更重要？

回答：

不是替代关系。

LangChain：

负责：

AI 能力。

LangGraph：

负责：

AI Workflow。

企业项目：

通常：

一起使用。

---

# 十九、本章练习

完成下面练习：

① 回顾：

Volume 01～04

↓

② 思考：

哪些模块可以升级为 LangGraph Node？

↓

③ 设计：

Research Agent

Planning Agent

Report Agent

三个 Agent 的职责。

↓

④ 思考：

哪些数据应该保存到 pgvector？

---

# 二十、本章核心记忆图

```text
                Browser
                    │
                    ▼
               FastAPI API
                    │
                    ▼
              AnalysisWorkflow
                    │
            ┌───────┼────────┐
            ▼       ▼        ▼
      LangGraph  Approval  Event Bus
            │
            ▼
        LangChain
            │
     ┌──────┼─────────┐
     ▼      ▼         ▼
   RAG   Tools      Memory
     │
     ▼
 PostgreSQL + pgvector
     │
     ▼
   LLM Provider
     │
     ▼
 AI Response
```

---

# 本章总结

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

补充知识

↓

LLM

完成推理
```

Enterprise AI Architecture 的核心思想是：

**AI 不只是模型，而是一个完整的平台。**

Workflow、LangChain、LangGraph、RAG、向量数据库、审批、安全、事件驱动和云原生共同构成现代企业 AI 平台。

---

# Volume 05 总结

完成 Volume 05 后，你已经掌握：

✅ Repository Pattern

✅ Dependency Injection

✅ Background Task Pattern

✅ Event Driven Architecture

✅ Workflow Pattern

✅ Security Architecture

✅ Persistence Architecture

✅ Scalability Architecture

✅ Cloud Native Architecture

✅ Enterprise AI Architecture

下一册：

**Volume 06：AI Architecture（AI 架构）**

将深入学习：

- LangChain 源码
- LangGraph Workflow
- RAG 检索系统
- Prompt Engineering
- MCP
- Multi-Agent
- AI Agent 企业实践

从"企业架构"正式进入"AI 架构"。
