# Retail Insight AI 源码阅读路线图（Code Reading Roadmap）

> **项目：Retail Insight AI / ERIP**
>
> **目标：**
> 从"项目如何启动"到"一次请求如何完成"，建立完整源码阅读路线。

------------------------------------------------------------------------

# 总体阅读路线

``` text
环境准备
    │
    ▼
backend/
    │
    ▼
Uvicorn
    │
    ▼
backend/app/main.py
    │
    ▼
create_app()
    │
    ▼
FastAPI()
    │
    ▼
Middleware
    │
    ▼
Router
    │
    ▼
API
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
KPI
    │
    ▼
Research
    │
    ▼
Report
    │
    ▼
Repository.save()
    │
    ▼
SSE / Events
    │
    ▼
Swagger / Frontend
```

------------------------------------------------------------------------

# 第一阶段：项目启动

阅读顺序：

``` text
backend/
    │
    ▼
app/main.py
    │
    ▼
create_app()
```

重点：

-   FastAPI 如何创建
-   Router 如何注册
-   Middleware 如何注册
-   生命周期事件（Startup / Shutdown）

------------------------------------------------------------------------

# 第二阶段：HTTP 请求入口

建议阅读：

``` text
backend/app/api/
```

阅读顺序：

``` text
health.py
    │
    ▼
tasks.py
    │
    ▼
upload.py
```

重点：

-   APIRouter
-   @router.get()
-   @router.post()
-   Request 如何进入 API

------------------------------------------------------------------------

# 第三阶段：业务层（Service）

目录：

``` text
backend/app/services/
```

学习：

``` text
API

↓

TaskService

↓

业务逻辑
```

重点：

-   Service 不处理 HTTP
-   Service 专注业务规则

------------------------------------------------------------------------

# 第四阶段：Repository

目录：

``` text
backend/app/repositories/
```

学习：

``` text
Service

↓

Repository.create()

↓

Repository.save()

↓

Repository.find()
```

重点：

-   数据存取
-   Repository Pattern

------------------------------------------------------------------------

# 第五阶段：BackgroundTasks

重点：

``` text
Request

↓

BackgroundTasks.add_task()

↓

HTTP 202

↓

Background 开始
```

理解：

-   为什么 HTTP 很快返回
-   为什么 Workflow 在后台运行

------------------------------------------------------------------------

# 第六阶段：Workflow

目录：

``` text
backend/app/workflow/
```

建议阅读：

``` text
graph.py

↓

AnalysisWorkflow.stream()

↓

Route()

↓

各节点
```

重点：

-   LangGraph
-   Workflow
-   Route

------------------------------------------------------------------------

# 第七阶段：AI Agent

学习顺序：

``` text
Route

↓

KPI

↓

Research

↓

Report
```

理解：

-   KPI 如何生成
-   Research 如何检索
-   Report 如何组合最终结果

------------------------------------------------------------------------

# 第八阶段：Repository 回写

Workflow 完成：

``` text
Report

↓

Repository.save()

↓

EventPublisher.publish()
```

重点：

-   状态更新
-   数据持久化
-   事件通知

------------------------------------------------------------------------

# 第九阶段：SSE

学习：

``` text
GET /api/tasks/{task_id}/events

↓

Repository

↓

Event

↓

Stream

↓

Browser
```

理解：

-   为什么页面能实时刷新
-   Event 如何推送

------------------------------------------------------------------------

# 第十阶段：Swagger 验证

建议验证顺序：

1.  GET /health
2.  POST /api/tasks
3.  GET /api/tasks/{task_id}
4.  GET /api/tasks/{task_id}/events

每完成一个接口：

-   阅读 Console Log
-   对照 Learning Walkthrough
-   阅读对应源码
-   理解执行阶段（Execution Flow）

------------------------------------------------------------------------

# 推荐源码阅读顺序

``` text
01 main.py
        │
        ▼
02 api/
        │
        ▼
03 services/
        │
        ▼
04 repositories/
        │
        ▼
05 workflow/
        │
        ▼
06 agents/
        │
        ▼
07 reports/
        │
        ▼
08 events/
        │
        ▼
09 schemas/
```

------------------------------------------------------------------------

# 学习建议

建议采用固定四步法：

``` text
① Swagger 测试接口
        │
        ▼
② 阅读 Console Log（Learning Trace）
        │
        ▼
③ 对照 LEARNING_API_WALKTHROUGH.md
        │
        ▼
④ 阅读对应源码
```

完成上述流程后，再进入下一个接口。

------------------------------------------------------------------------

# 最终目标

完成本路线图后，应能够回答：

-   Uvicorn 如何启动 FastAPI？
-   main.py 为什么是项目入口？
-   Router 如何找到 API？
-   Service 与 Repository 如何分工？
-   为什么 POST /api/tasks 分为 Request 与 Background？
-   Workflow 如何驱动 KPI、Research、Report？
-   SSE 如何实时返回执行进度？
-   一次 HTTP 请求如何完成整个生命周期？
