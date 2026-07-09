# Retail Insight AI 学习笔记全集（正式版 V2.0）

**Volume 01：FastAPI 基础篇**

> Chapter 02：项目整体认识

------------------------------------------------------------------------

# 文档信息

  项目       内容
  ---------- -----------------
  文档版本   V2.0
  Volume     01
  Chapter    02
  状态       Draft（审阅中）

------------------------------------------------------------------------

# 本章目标

完成本章后，你将能够：

-   理解整个项目的目录结构。
-   知道应该先阅读哪些目录。
-   理解前端、后端、文档之间的关系。
-   建立完整的源码阅读地图。

------------------------------------------------------------------------

# 1. 项目整体架构

``` text
Retail Insight AI
│
├── backend      ← FastAPI 后端
├── frontend     ← React 前端
├── docs         ← 项目文档
├── scripts      ← 启动、测试脚本
└── docker       ← 容器部署
```

这是整个项目最重要的五个目录。

------------------------------------------------------------------------

# 2. backend（重点）

``` text
backend/
└── app/
    ├── api/
    ├── services/
    ├── repositories/
    ├── workflow/
    ├── agents/
    ├── reports/
    ├── schemas/
    ├── events/
    └── core/
```

职责说明：

  目录           作用
  -------------- ----------------------------------------
  api            HTTP 接口入口（Router）
  services       业务逻辑
  repositories   数据访问层
  workflow       AI 工作流（LangGraph）
  agents         AI Agent 能力
  reports        报告生成
  schemas        Request / Response 数据模型
  events         SSE 与事件发布
  core           全局基础能力（Learning Trace、配置等）

------------------------------------------------------------------------

# 3. frontend

``` text
frontend
```

负责：

-   页面展示
-   Swagger 调试辅助
-   SSE 实时更新
-   调用后端 API

学习前期无需深入源码，理解职责即可。

------------------------------------------------------------------------

# 4. docs

项目所有设计文档集中在 docs。

建议优先阅读：

1.  LEARNING_API_WALKTHROUGH.md
2.  CODE_STUDY_GUIDE.md
3.  RUNBOOK_LOCAL.md

之后再阅读：

-   architecture/
-   governance/
-   contracts/

------------------------------------------------------------------------

# 5. scripts

常用脚本：

``` text
scripts/
├── start_backend.sh
├── run_tests.sh
└── ...
```

学习阶段最常用的是：

-   start_backend.sh
-   run_tests.sh

------------------------------------------------------------------------

# 6. 推荐源码阅读顺序

``` text
main.py
    │
    ▼
api/
    │
    ▼
services/
    │
    ▼
repositories/
    │
    ▼
workflow/
    │
    ▼
agents/
    │
    ▼
reports/
```

不要一开始就阅读 workflow。

先理解 HTTP 请求，再理解 AI Workflow。

------------------------------------------------------------------------

# 7. Browser 到 AI 的完整调用关系

``` text
Browser
    │
Swagger
    │
FastAPI
    │
Router
    │
Service
    │
Repository
    │
Workflow
    │
AI Provider
    │
Report
```

这是整个项目最重要的一条主线，后续所有章节都会围绕它展开。

------------------------------------------------------------------------

# 8. Learning Tip

★★★★★ 建议

第一次阅读源码时：

不要急于理解每一行代码。

先回答三个问题：

1.  当前目录负责什么？
2.  谁调用它？
3.  它又调用了谁？

只要能回答这三个问题，就已经掌握了整体架构。

------------------------------------------------------------------------

# 9. Java（Spring Boot）对照

  Retail Insight AI   Spring Boot
  ------------------- --------------------------
  api                 Controller
  services            Service
  repositories        Repository / DAO
  schemas             DTO
  workflow            业务流程引擎（概念类似）

------------------------------------------------------------------------

# 本章总结

本章建立了整个项目的目录地图。

后续学习时，不再是"看到文件再猜作用"，而是能够根据目录快速定位职责。

------------------------------------------------------------------------

# 下一章预告

**Chapter 03：FastAPI 基础**

将学习：

-   Uvicorn
-   FastAPI
-   ASGI
-   OpenAPI
-   Swagger
-   为什么浏览器能够直接调用 API
