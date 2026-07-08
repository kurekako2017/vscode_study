# FastAPI 从启动到一次 HTTP 请求的完整生命周期

> 适用项目：Retail Insight AI / ERIP\
> 学习目标：理解 **Uvicorn → FastAPI → Router → Service → Repository →
> Response** 的完整生命周期。

------------------------------------------------------------------------

# 一、整体生命周期

``` text
启动命令

uvicorn app.main:app

        │
        ▼
┌────────────────────────────┐
│ Uvicorn Web Server         │
└────────────────────────────┘
        │
        ▼
读取 backend/app/main.py
        │
        ▼
create_app()
        │
        ▼
创建 FastAPI()
        │
        ▼
注册 Middleware
        │
        ▼
注册 Router
(include_router)
        │
        ▼
HTTP Server 开始监听
127.0.0.1:8000
        │
        ▼
等待 HTTP Request
```

------------------------------------------------------------------------

# 二、浏览器发起一次请求

例如：

``` http
GET /health
```

生命周期：

``` text
浏览器
    │
    ▼
HTTP Request
    │
    ▼
Uvicorn
    │
    ▼
FastAPI
    │
    ▼
Middleware
(request_context 等)
    │
    ▼
Router
(@router.get)
    │
    ▼
Controller(API)
health()
    │
    ▼
Schema
HealthResponse
    │
    ▼
JSON
    │
    ▼
HTTP Response
    │
    ▼
浏览器
```

------------------------------------------------------------------------

# 三、POST /api/tasks 生命周期

## Request（同步执行）

``` text
浏览器

↓

POST /api/tasks

↓

Uvicorn

↓

FastAPI

↓

Middleware

↓

Router

↓

create_task()

↓

TaskService.create_task()

↓

Repository.create()

↓

BackgroundTasks.add_task()

↓

HTTP 202 + task_id

↓

浏览器收到响应
```

> 到这里 **HTTP 请求已经结束**。

------------------------------------------------------------------------

## Background（异步执行）

``` text
BackgroundTasks

↓

Repository.save()

↓

AnalysisWorkflow.stream()

↓

Route

↓

KPI

↓

Research

↓

Report

↓

Repository.save()

↓

EventPublisher.publish()

↓

任务完成
```

> 浏览器不会等待这一阶段执行结束。

------------------------------------------------------------------------

# 四、为什么 Request 与 Background 要分开？

  Request（同步）       Background（异步）
  --------------------- --------------------
  浏览器等待响应        浏览器已收到响应
  必须尽快结束          可以耗时执行
  返回 HTTP 200 / 202   不返回 HTTP
  创建任务              真正完成分析

------------------------------------------------------------------------

# 五、源码阅读顺序（推荐）

``` text
1. backend/app/main.py
        │
        ▼
2. create_app()
        │
        ▼
3. include_router()
        │
        ▼
4. backend/app/api/
        │
        ▼
5. backend/app/services/
        │
        ▼
6. backend/app/repositories/
        │
        ▼
7. backend/app/workflow/
        │
        ▼
8. backend/app/schemas/
```

------------------------------------------------------------------------

# 六、Java 对照理解

  Java（Spring Boot）      FastAPI
  ------------------------ ---------------------------------
  Tomcat                   Uvicorn
  @SpringBootApplication   main.py
  DispatcherServlet        FastAPI Router
  Controller               api/\*.py
  Service                  services/\*.py
  Repository               repositories/\*.py
  ResponseEntity           Pydantic Schema + JSON Response

------------------------------------------------------------------------

# 七、学习建议

建议按下面顺序学习源码：

1.  Uvicorn 如何启动应用
2.  main.py 如何创建 FastAPI
3.  create_app() 注册哪些内容
4.  Router 如何接收 HTTP 请求
5.  Service 如何处理业务
6.  Repository 如何保存数据
7.  Workflow 如何执行后台任务
8.  Schema 如何返回 JSON

完成这八步后，就能理解一次 HTTP 请求在 FastAPI 中的完整生命周期。
