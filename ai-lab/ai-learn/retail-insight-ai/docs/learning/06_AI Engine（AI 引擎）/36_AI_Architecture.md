
> **V1.0 校正：** 正式 Repository = **PostgreSQL + pgvector**。文中 SQLite 仅作历史/对比教学，不是当前主库。InMemory = unittest only。

# Retail Insight AI 企业源码架构手册

# Volume 06：AI Engine（AI 引擎）

# Chapter 36

# AI Architecture（AI 引擎总体架构）

> Understand the Entire AI Engine

---

# 文档信息

| 项目     | 内容                                    |
| -------- | --------------------------------------- |
| Volume   | 06                                      |
| Chapter  | 36                                      |
| 技术主题 | AI Architecture                         |
| 难度     | ⭐⭐⭐⭐⭐                              |
| 推荐程度 | ⭐⭐⭐⭐⭐                              |
| 对应源码 | workflow/ graph.py services/ providers/ |

---

# 学习目标

阅读本章后，你应该能够回答：

- ERIP 的 AI Engine 是什么？
- AI Engine 与 Web API 的关系？
- AI Engine 包含哪些模块？
- AI Engine 如何执行一次完整分析？
- 为什么企业 AI 都采用分层架构？

---

# 一、什么是 AI Engine？

AI Engine 并不是 LLM。

AI Engine 是：

整个 AI 执行系统。

包括：

- Workflow
- Prompt
- LLM
- Retriever
- Repository
- Event
- Streaming

共同组成。

---

# 二、ERIP 当前 AI Engine

整个 AI 调用链：

Browser

↓

POST /api/tasks

↓

TaskService

↓

BackgroundTasks

↓

AnalysisWorkflow

↓

Prompt

↓

LLM

↓

Result

↓

Repository

↓

EventPublisher

↓

SSE

↓

Browser

这就是：

整个 AI Engine。

---

# 三、源码目录结构 ⭐

backend/app/

↓

api/

↓

services/

↓

workflow/

↓

providers/

↓

repositories/

↓

events/

这一层：

就是：

AI Engine。

---

# 四、关键源码文件 ⭐

建议阅读顺序：

main.py

↓

tasks.py

↓

task_service.py

↓

graph.py

↓

provider

↓

repository

↓

publisher

---

# 五、AI Engine 分层 ⭐

第一层：

API Layer

↓

第二层：

Service Layer

↓

第三层：

Workflow Layer

↓

第四层：

AI Provider Layer

↓

第五层：

Persistence Layer

↓

第六层：

Communication Layer

---

# 六、调用关系 ⭐

HTTP Request

↓

TaskService

↓

AnalysisWorkflow

↓

Provider

↓

Repository

↓

Publisher

↓

SSE

---

# 七、AI Workflow 对应 ⭐

Workflow

负责：

组织流程

Provider

负责：

调用模型

Repository

负责：

保存结果

Publisher

负责：

通知前端

---

# 八、Learning Trace 对应 ⭐

Learning Trace：

完整记录：

Task

↓

Workflow

↓

LLM

↓

Repository

↓

Publisher

↓

Completed

---

# 九、Console Log 对应 ⭐

建议观察：

Workflow Start

↓

Research Start

↓

Report Complete

↓

Repository Save

↓

Task Finished

---

# 十、Architecture Thinking ⭐

为什么：

AI Engine

要分层？

如果：

Workflow

直接：

调用：

数据库、

浏览器、

LLM、

日志。

整个系统：

会变得：

无法维护。

因此：

企业：

一定：

分层。

---

# 十一、Current vs Enterprise

Current：

FastAPI

↓

Workflow

↓

LLM

↓

SQLite

Enterprise：

Gateway

↓

Workflow Engine

↓

LangGraph

↓

RAG

↓

Redis

↓

RabbitMQ

↓

pgvector

↓

PostgreSQL

↓

Monitoring

---

# 十二、Java / Spring 对照 ⭐

FastAPI

=

Controller

TaskService

=

Service

Workflow

=

Process Engine

Repository

=

JpaRepository

Provider

=

OpenAI Client

---

# 十三、VS Code 阅读路线 ⭐

建议：

不要：

从 graph.py 开始。

正确：

main.py

↓

tasks.py

↓

task_service.py

↓

graph.py

↓

provider

↓

repository

↓

publisher

---

# 十四、企业扩展（Enterprise）

未来：

增加：

LangGraph

↓

MCP

↓

Multi-Agent

↓

Memory

↓

Vector Search

↓

Knowledge Graph

---

# 十五、面试回答（中文）

什么是 AI Engine？

AI Engine 是 AI 系统真正执行业务逻辑的核心，包括 Workflow、Prompt、模型调用、知识检索、结果持久化和事件通知等多个模块。它不仅负责调用 LLM，还负责组织整个 AI 执行流程，是企业 AI 平台的核心能力。

---

# 十六、面试回答（日文）

AI Engine とは何ですか。

AI Engine は LLM を呼び出すだけではなく、Workflow、Prompt、Retriever、Repository、Event 通知などを統合した AI 実行基盤です。企業システムでは AI の中核として重要な役割を担います。

---

# 十七、日本 SES 常见追问

Q：

AI Engine 和 LLM 有什么区别？

回答：

LLM：

负责：

推理。

AI Engine：

负责：

组织：

整个：

AI 系统。

---

# 十八、本章练习 ⭐

请完成：

① 阅读：

TaskService

↓

② 阅读：

AnalysisWorkflow

↓

③ 阅读：

Provider

↓

④ 画出：

AI Engine

架构图。

---

# 十九、本章核心记忆图 ⭐

Browser

↓

TaskService

↓

Workflow

↓

LLM

↓

Repository

↓

Publisher

↓

Browser

---

# 本章总结

一句话：

AI Engine：

不是模型。

而是：

企业 AI 的执行系统。

---

# 下一章

Chapter37：

LangChain Architecture
