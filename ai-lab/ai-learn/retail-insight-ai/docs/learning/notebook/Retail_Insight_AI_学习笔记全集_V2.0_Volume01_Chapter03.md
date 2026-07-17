# Retail Insight AI 学习笔记全集（正式版 V2.0）
> **历史学习笔记**：项目现名 ERIP V1.0；本文保留教学叙述。现状数字与架构以 handbook 权威材料与源码为准。


**Volume 01：FastAPI 基础篇**

> Chapter 03：FastAPI 基础（Uvicorn、ASGI、OpenAPI、Swagger）

------------------------------------------------------------------------

# 文档信息

  项目       内容
  ---------- -----------------
  文档版本   V2.0
  Volume     01
  Chapter    03
  状态       Draft（审阅中）

------------------------------------------------------------------------

# 本章目标

完成本章后，你将理解：

-   什么是 Uvicorn
-   什么是 FastAPI
-   什么是 ASGI
-   OpenAPI 与 Swagger 的关系
-   在 Retail Insight AI 中它们如何协同工作

------------------------------------------------------------------------

# 1. FastAPI 是什么？

FastAPI 是一个基于 Python 的现代 Web 框架，用于构建 HTTP API。

在本项目中，FastAPI 负责：

-   接收 HTTP 请求
-   路由到对应 Router
-   数据校验（Pydantic）
-   返回 JSON 响应
-   自动生成 OpenAPI 文档

------------------------------------------------------------------------

# 2. Uvicorn 是什么？

Uvicorn 是一个 **ASGI Server**。

它的职责不是执行业务，而是负责：

``` text
启动服务
    │
监听 HTTP 请求
    │
把请求交给 FastAPI
```

在本项目中：

``` text
start_backend.sh
        │
        ▼
uvicorn backend.app.main:app
        │
        ▼
main.py
```

> 学习重点：Uvicorn 是入口，不是业务层。

------------------------------------------------------------------------

# 3. 什么是 ASGI？

ASGI（Asynchronous Server Gateway Interface）是 Python Web
应用与服务器之间的通信规范。

关系如下：

``` text
Browser
    │
HTTP
    │
Uvicorn（ASGI Server）
    │
ASGI
    │
FastAPI
```

相比传统同步模式，ASGI 更适合：

-   异步请求
-   BackgroundTasks
-   SSE
-   WebSocket

Retail Insight AI 的后台分析流程正是基于这种异步能力。

------------------------------------------------------------------------

# 4. OpenAPI 与 Swagger

FastAPI 会自动根据 Router 和 Schema 生成 OpenAPI 规范。

Swagger UI 则根据 OpenAPI 文档生成可交互页面。

``` text
Router
    │
Schema
    │
OpenAPI
    │
Swagger UI
```

因此，不需要手写 API 文档。

------------------------------------------------------------------------

# 5. 在 Retail Insight AI 中的对应关系

  技术      项目位置
  --------- -------------------------------
  Uvicorn   scripts/start_backend.sh 启动
  FastAPI   backend/app/main.py
  Router    backend/app/api/
  Schema    backend/app/schemas/
  Swagger   /docs
  OpenAPI   /openapi.json

------------------------------------------------------------------------

# 6. 一次请求如何进入项目？

``` text
Browser
    │
HTTP
    │
Uvicorn
    │
FastAPI
    │
Middleware
    │
Router
    │
Service
    │
Repository
    │
Workflow
```

从下一章开始，我们将逐步分析这条调用链。

------------------------------------------------------------------------

# 7. Java（Spring Boot）对照

  Retail Insight AI   Spring Boot
  ------------------- -------------------
  Uvicorn             Tomcat
  FastAPI             Spring Boot
  Router              Controller
  OpenAPI             springdoc-openapi
  Swagger UI          Swagger UI

------------------------------------------------------------------------

# 8. Learning Tip

★★★★★

第一次学习时，不要纠结 Uvicorn 的内部实现。

重点理解：

-   它负责启动应用。
-   它把 HTTP 请求交给 FastAPI。
-   真正的业务逻辑从 `main.py` 开始。

------------------------------------------------------------------------

# 本章总结

本章建立了 FastAPI 运行环境的整体认识：

``` text
Uvicorn
    │
ASGI
    │
FastAPI
    │
Router
    │
Service
```

这是后续源码分析的基础。

------------------------------------------------------------------------

# 下一章预告

**Chapter 04：项目启动流程**

我们将结合 Retail Insight AI 的真实启动过程，分析：

-   start_backend.sh
-   uvicorn
-   backend/app/main.py
-   create_app()
-   路由注册
-   Middleware 初始化
