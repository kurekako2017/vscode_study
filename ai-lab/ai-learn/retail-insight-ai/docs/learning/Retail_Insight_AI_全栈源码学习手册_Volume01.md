# Retail Insight AI 全栈源码学习手册（Volume 01）

> **Project:** Retail Insight AI / ERIP\
> **Audience:** FastAPI 初学者、Python 开发者、日本 Agent 项目面试准备

------------------------------------------------------------------------

# 目录

1.  项目整体架构
2.  开发环境
3.  项目启动流程
4.  FastAPI 生命周期
5.  第一次 HTTP 请求
6.  Learning Trace 与 Execution Flow
7.  源码阅读路线图
8.  核心目录说明
9.  BackgroundTasks 与 Workflow
10. Agent 执行流程
11. SSE 实时事件
12. 学习顺序建议

------------------------------------------------------------------------

# 第1章 项目整体架构

``` text
Browser / Swagger
        │
        ▼
Uvicorn
        │
        ▼
FastAPI
        │
        ▼
Middleware
        │
        ▼
Router(API)
        │
        ▼
Service
        │
        ▼
Repository
        │
        ▼
BackgroundTasks
        │
        ▼
Workflow
        │
        ▼
KPI → Research → Report
        │
        ▼
Repository.save()
        │
        ▼
SSE / Events
```

------------------------------------------------------------------------

# 第2章 开发环境

启动：

``` bash
cd backend
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Swagger：

``` text
http://127.0.0.1:8000/docs
```

------------------------------------------------------------------------

# 第3章 项目启动流程

``` text
uvicorn
    ↓
backend/app/main.py
    ↓
create_app()
    ↓
FastAPI()
    ↓
注册 Middleware
    ↓
注册 Router
    ↓
监听 127.0.0.1:8000
```

重点学习：

-   create_app()
-   include_router()
-   Middleware 注册

------------------------------------------------------------------------

# 第4章 FastAPI 生命周期

``` text
Application Startup
        ↓
等待 HTTP 请求
        ↓
处理 Request
        ↓
返回 Response
        ↓
Application Shutdown
```

理解：

-   Startup
-   Request
-   Background
-   Shutdown

------------------------------------------------------------------------

# 第5章 一次 HTTP 请求

GET /health：

``` text
Browser
    ↓
Uvicorn
    ↓
Router
    ↓
health()
    ↓
HealthResponse
    ↓
JSON
    ↓
HTTP 200
```

POST /api/tasks：

``` text
Request
    ↓
BackgroundTasks.add_task()
    ↓
HTTP 202
──────────────
Background
    ↓
Workflow
    ↓
Report
```

------------------------------------------------------------------------

# 第6章 Learning Trace 与 Execution Flow

学习步骤：

1.  Swagger Execute
2.  Console Log（Learning Trace）
3.  Execution Flow
4.  阅读源码

理解：

-   Request（同步）
-   Background（异步）

------------------------------------------------------------------------

# 第7章 源码阅读路线图

推荐顺序：

``` text
main.py
    ↓
api/
    ↓
services/
    ↓
repositories/
    ↓
workflow/
    ↓
agents/
    ↓
reports/
    ↓
events/
    ↓
schemas/
```

------------------------------------------------------------------------

# 第8章 核心目录说明

  目录               作用
  ------------------ -------------------------------
  app/api            HTTP 接口
  app/services       业务逻辑
  app/repositories   数据访问
  app/workflow       工作流
  app/events         事件发布
  app/schemas        请求/响应模型
  app/core           公共能力（Learning Trace 等）

------------------------------------------------------------------------

# 第9章 BackgroundTasks 与 Workflow

同步阶段：

``` text
Router
 ↓
Service
 ↓
Repository.create()
 ↓
BackgroundTasks.add_task()
 ↓
HTTP 202
```

异步阶段：

``` text
Workflow
 ↓
KPI
 ↓
Research
 ↓
Report
 ↓
Repository.save()
```

------------------------------------------------------------------------

# 第10章 Agent 执行流程

``` text
Route
 ↓
KPI Agent
 ↓
Research Agent
 ↓
Report Generator
```

学习重点：

-   路由决策
-   数据分析
-   报告生成

------------------------------------------------------------------------

# 第11章 SSE 实时事件

``` text
Browser
 ↓
GET /api/tasks/{task_id}/events
 ↓
Repository
 ↓
EventPublisher
 ↓
Server Sent Events
 ↓
实时更新页面
```

------------------------------------------------------------------------

# 第12章 推荐学习顺序

## 第一轮

1.  项目启动
2.  GET /health
3.  POST /api/tasks

## 第二轮

1.  Service
2.  Repository
3.  Workflow

## 第三轮

1.  KPI
2.  Research
3.  Report
4.  SSE

------------------------------------------------------------------------

# 面试复习清单

完成本手册后，应能够解释：

-   Uvicorn 如何启动 FastAPI
-   main.py 为什么是入口
-   Router 如何找到 API
-   Service 与 Repository 如何协作
-   为什么要区分 Request 与 Background
-   Workflow 如何驱动 Agent
-   SSE 如何实时返回任务状态

------------------------------------------------------------------------

**Volume 01 建议配合阅读：**

-   LEARNING_API_WALKTHROUGH.md
-   FastAPI_项目启动过程_学习笔记.md
-   FastAPI_从启动到一次HTTP请求的完整生命周期.md
-   Retail_Insight_AI_源码阅读路线图_Code_Reading_Roadmap.md
