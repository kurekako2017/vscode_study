# Retail Insight AI 学习笔记全集（正式版 V2.0）

**Volume 01：FastAPI 基础篇**

> Chapter 05：main.py 源码解析（Application Entry）

------------------------------------------------------------------------

# 文档信息

  项目       内容
  ---------- -----------------
  文档版本   V2.0
  Volume     01
  Chapter    05
  状态       Draft（审阅中）

------------------------------------------------------------------------

# 本章目标

完成本章后，你将能够：

-   理解 `backend/app/main.py` 在整个项目中的职责。
-   理解 `app` 与 `create_app()` 的关系。
-   理解 Middleware、Router、Lifespan 是如何注册的。
-   建立后续阅读 API 源码的入口。

------------------------------------------------------------------------

# 1. 为什么先阅读 main.py？

在 Retail Insight AI 中，**所有 HTTP 请求都会先经过 FastAPI
Application**。

而创建这个 Application 的地方就是：

``` text
backend/app/main.py
```

因此，阅读源码时建议从这里开始，而不是直接进入 `tasks.py`。

------------------------------------------------------------------------

# 2. main.py 在整个系统中的位置

``` text
Browser
    │
HTTP Request
    │
Uvicorn
    │
backend/app/main.py
    │
create_app()
    │
FastAPI Application
    │
Router
    │
Service
    │
Workflow
```

可以把 `main.py` 理解为整个项目的**总入口**。

------------------------------------------------------------------------

# 3. FastAPI Application 是什么？

`FastAPI()` 创建的是整个 Web 应用实例。

职责包括：

-   接收 HTTP 请求
-   保存全局配置
-   管理 Router
-   管理 Middleware
-   管理生命周期（Lifespan）
-   自动生成 OpenAPI

学习重点：

> **Application 是容器，不是业务逻辑。**

------------------------------------------------------------------------

# 4. create_app() 为什么存在？

企业项目通常不会直接：

``` python
app = FastAPI()
```

而是：

``` text
create_app()
        │
        ├── 创建 Application
        ├── 注册 Middleware
        ├── 注册 Router
        ├── 注册 Exception Handler
        ├── 注册 Lifespan
        └── 返回 app
```

这样做的优点：

-   职责集中
-   初始化流程统一
-   更容易测试
-   更容易扩展

------------------------------------------------------------------------

# 5. include_router()

Router 是真正的 HTTP 入口。

例如：

``` text
include_router()
        │
        ├── health.py
        ├── tasks.py
        ├── documents.py
        ├── approvals.py
        └── security.py
```

没有注册 Router，即使代码存在，也无法通过 HTTP 访问。

------------------------------------------------------------------------

# 6. Middleware

Middleware 位于请求进入 Router 之前。

执行顺序：

``` text
Browser
    │
Middleware
    │
Router
    │
Service
```

在本项目中，Middleware 常用于：

-   request_id
-   Learning Trace
-   日志
-   CORS

------------------------------------------------------------------------

# 7. Lifespan

Lifespan 表示应用生命周期。

典型流程：

``` text
Application Start
        │
        ▼
初始化资源
        │
等待请求
        │
        ▼
Application Stop
        │
释放资源
```

它不是处理 HTTP 请求，而是处理应用本身的启动和关闭。

------------------------------------------------------------------------

# 8. 对应 Learning Trace

Learning Trace 从收到请求开始，因此 Console 中通常会看到：

``` text
backend/app/main.py
create_app()
    ↓
（路由已注册）
    ↓
backend/app/api/tasks.py
```

这里表示：

1.  Application 已经创建完成。
2.  Router 已经注册。
3.  请求正式进入业务层。

------------------------------------------------------------------------

# 9. Java（Spring Boot）对照

  Retail Insight AI   Spring Boot
  ------------------- ------------------------------------------
  main.py             SpringBootApplication
  FastAPI()           Spring ApplicationContext
  create_app()        Spring 容器初始化
  include_router()    Controller 扫描
  Middleware          Filter / Interceptor
  Lifespan            @PostConstruct / @PreDestroy（概念类似）

------------------------------------------------------------------------

# 10. 常见误区

❌ main.py 负责业务分析。

实际上：

业务分析发生在：

``` text
tasks.py
    ↓
TaskService
    ↓
Workflow
```

main.py 只负责**创建并配置 Application**。

------------------------------------------------------------------------

# 11. Learning Tip

★★★★★

阅读 `main.py` 时，请重点关注：

1.  Application 是如何创建的？
2.  Router 在哪里注册？
3.  Middleware 在哪里注册？
4.  Lifespan 在哪里初始化？

不用急于理解每一行代码，先理解整体职责。

------------------------------------------------------------------------

# 本章总结

可以把 `main.py` 记成一句话：

``` text
main.py
    │
创建 FastAPI Application
    │
注册 Middleware
    │
注册 Router
    │
初始化 Lifespan
    │
等待 HTTP Request
```

它是整个项目的**应用入口（Application Entry）**，而不是业务入口。

------------------------------------------------------------------------

# 下一章预告

**Chapter 06：第一次 HTTP 请求**

我们将结合真实的 `GET /health` 和 `POST /api/tasks`，分析：

-   HTTP 请求如何进入 Router
-   Router 如何调用 Service
-   Learning Trace 如何记录程序执行阶段
-   Request 与 Background 为什么分离
