# Retail Insight AI 学习笔记全集（正式版 V2.0）
> **历史学习笔记**：项目现名 ERIP V1.0；本文保留教学叙述。现状数字与架构以 handbook 权威材料与源码为准。


**Volume 01：FastAPI 基础篇**

> Chapter 06：第一次 HTTP 请求（GET /health 与 POST /api/tasks）

------------------------------------------------------------------------

# 文档信息

  项目       内容
  ---------- -----------------
  文档版本   V2.0
  Volume     01
  Chapter    06
  状态       Draft（审阅中）

------------------------------------------------------------------------

# 本章目标

完成本章后，你将能够：

-   理解浏览器发送 HTTP 请求后的完整执行流程。
-   学会阅读 Learning Trace（程序执行阶段）。
-   理解 Request 与 Background 的区别。
-   建立 Router → Service → Repository → Workflow 的整体认识。

------------------------------------------------------------------------

# 1. 第一次 HTTP 请求

浏览器访问：

``` text
GET /health
```

或者：

``` text
POST /api/tasks
```

请求会按照固定流程进入系统。

``` text
Browser
    │
HTTP Request
    │
Uvicorn
    │
FastAPI
    │
Middleware
    │
Router
```

------------------------------------------------------------------------

# 2. GET /health（同步接口）

## Console Log（示意）

``` text
backend/app/main.py
create_app()
    ↓
（路由已注册）
    ↓
backend/app/api/health.py
health()
    ↓
HealthResponse
    ↓
HTTP 200 Response
```

## 程序执行阶段（Execution Flow）

``` text
Request
    │
main.py
    │
health.py
    │
HealthResponse
    │
HTTP 200
```

特点：

-   没有 Background。
-   收到 HTTP 200 表示整个请求已经结束。

------------------------------------------------------------------------

# 3. POST /api/tasks（异步接口）

创建分析任务：

``` text
POST /api/tasks
```

与 GET 不同，它分为两个阶段。

## 第一阶段：Request（同步）

``` text
Browser
    │
Router
    │
TaskService.create_task()
    │
Repository.create()
    │
BackgroundTasks.add_task()
    │
HTTP 202 Response
```

浏览器此时已经收到：

``` json
{
  "task_id": "...",
  "status": "queued"
}
```

------------------------------------------------------------------------

## 第二阶段：Background（异步）

FastAPI 返回 HTTP 202 后：

``` text
TaskService.run_task()
        │
Repository.save()
        │
EventPublisher.publish()
        │
AnalysisWorkflow.stream()
        │
Route
        │
KPI
        │
Research
        │
Report
        │
Repository.save()
```

这一阶段浏览器不会等待。

如果需要查看结果：

``` text
GET /api/tasks/{task_id}

或

GET /api/tasks/{task_id}/events
```

------------------------------------------------------------------------

# 4. 为什么分成 Request / Background？

原因：

AI 分析可能持续数秒甚至数十秒。

如果一直等待：

``` text
Browser
        │
等待...
        │
等待...
        │
等待...
```

用户体验很差。

因此：

``` text
Request
        │
快速返回 task_id
        │
Background
        │
后台完成分析
```

这也是企业项目中常见的异步处理方式。

------------------------------------------------------------------------

# 5. Learning Trace 对照

Learning Trace 不是业务逻辑。

它只是记录程序执行阶段。

例如：

``` text
Request
    │
Router
    │
Service
    │
Repository

Background
    │
Workflow
    │
Report
```

帮助学习源码，而不会影响业务执行。

------------------------------------------------------------------------

# 6. Java（Spring Boot）对照

  Retail Insight AI   Spring Boot
  ------------------- --------------------
  GET /health         @GetMapping
  POST /api/tasks     @PostMapping
  BackgroundTasks     @Async（概念类似）
  Learning Trace      调试日志 + 调用链

------------------------------------------------------------------------

# 7. 常见误区

❌ HTTP 202 表示任务完成。

实际上：

HTTP 202 仅表示：

> **服务器已经接受任务，并开始后台处理。**

真正完成需要等待 Background 执行结束。

------------------------------------------------------------------------

# 8. Learning Tip

★★★★★

以后阅读每个 API，请先判断：

-   它是同步接口（只有 Request）？
-   还是异步接口（Request + Background）？

这是理解整个项目调用链的关键。

------------------------------------------------------------------------

# 本章总结

同步接口：

``` text
Request
    ↓
HTTP 200
```

异步接口：

``` text
Request
    ↓
HTTP 202
    ↓
Background
    ↓
Workflow
```

理解这一点，就能理解为什么项目需要 BackgroundTasks、Learning Trace 和
EventPublisher。

------------------------------------------------------------------------

# 下一章预告

**Chapter 07：Router（API 层）**

我们将开始阅读：

-   APIRouter
-   @router.get()
-   @router.post()
-   include_router()
-   Router 如何把 HTTP 请求交给 Service。
