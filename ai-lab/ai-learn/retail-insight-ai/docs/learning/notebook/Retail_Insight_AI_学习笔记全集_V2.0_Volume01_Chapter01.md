# Retail Insight AI 学习笔记全集（正式版 V2.0）

> **历史学习笔记（保留不删除）**  
> 当前正式项目名：**Enterprise Retail Intelligence Platform（ERIP）V1.0**。  
> 面试与现状以 `docs/ai-agent-retail-handbook-v3/` 权威面试材料 + 主 README 为准。  
> 基线：PG 297/6 · IM 286/62 · FE 116 · head `20260717_08_ai_runtime` · 默认 stub。

**Volume 01：FastAPI 基础篇**

> Chapter 01：为什么学习 Retail Insight AI

------------------------------------------------------------------------

# 文档信息

  项目       内容
  ---------- ---------------------------
  文档版本   V2.0
  Volume     01
  Chapter    01
  状态       Draft（审阅中）
  目标读者   FastAPI / AI Agent 初学者

------------------------------------------------------------------------

# 1. 为什么学习这个项目？

很多 FastAPI 教程都会从 Hello World 开始。

例如：

``` python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello World"}
```

虽然容易入门，但无法学习企业项目真正的组织方式。

Retail Insight AI 更接近真实企业开发，能够一次学习：

-   FastAPI 分层架构
-   Repository Pattern
-   BackgroundTasks
-   Learning Trace
-   LangGraph Workflow
-   SSE 实时事件
-   AI Agent 工作流

------------------------------------------------------------------------

# 2. 学习目标

完成本教程后，你应能够：

-   理解一次 HTTP 请求如何进入 FastAPI。
-   理解 Router、Service、Repository 的职责。
-   理解 Background 与 Request 的区别。
-   阅读 Retail Insight AI 的核心源码。
-   为日本 Agent 案件面试做准备。

------------------------------------------------------------------------

# 3. 项目整体架构（概念图）

``` text
Browser
   │
Swagger UI
   │
FastAPI
   │
Router
   │
Service
   │
Repository
   │
Workflow (LangGraph)
   │
AI Provider
   │
Report
```

这是后续所有章节都会反复出现的主线。

------------------------------------------------------------------------

# 4. 为什么不用 Hello World？

Hello World 能学习语法，却学不到：

-   企业项目如何分层
-   为什么需要 Repository
-   为什么要 BackgroundTasks
-   为什么要 Learning Trace
-   为什么要 Workflow

Retail Insight AI 则把这些真实场景全部串联起来。

------------------------------------------------------------------------

# 5. 建议学习顺序

1.  阅读本章。
2.  阅读项目启动流程。
3.  阅读 main.py。
4.  阅读 Router。
5.  阅读 Service。
6.  阅读 Repository。
7.  阅读 Workflow。
8.  阅读 LangGraph。

------------------------------------------------------------------------

# 6. Java（Spring Boot）对照

  Retail Insight AI   Spring Boot
  ------------------- --------------------
  FastAPI             Spring Boot
  Router              Controller
  Service             Service
  Repository          Repository / DAO
  Pydantic Schema     DTO
  BackgroundTasks     @Async（概念类似）

------------------------------------------------------------------------

# 7. 本章总结

本章没有分析具体源码，而是建立整个项目的学习地图。

后续章节都会围绕这一条主线展开：

``` text
Browser
 ↓
FastAPI
 ↓
Router
 ↓
Service
 ↓
Repository
 ↓
Workflow
 ↓
AI
```

------------------------------------------------------------------------

# 下一章预告

**Chapter 02：项目整体认识**

将开始阅读：

-   backend/
-   docs/
-   frontend/
-   scripts/

并理解整个项目的目录结构以及源码阅读入口。
