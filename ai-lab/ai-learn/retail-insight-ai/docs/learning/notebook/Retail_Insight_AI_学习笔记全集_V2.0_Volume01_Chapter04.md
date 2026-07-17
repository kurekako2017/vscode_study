# Retail Insight AI 学习笔记全集（正式版 V2.0）
> **历史学习笔记**：项目现名 ERIP V1.0；本文保留教学叙述。现状数字与架构以 handbook 权威材料与源码为准。


**Volume 01：FastAPI 基础篇**

> Chapter 04：项目启动流程（Project Startup Flow）

------------------------------------------------------------------------

# 文档信息

  项目       内容
  ---------- -----------------
  文档版本   V2.0
  Volume     01
  Chapter    04
  状态       Draft（审阅中）

------------------------------------------------------------------------

# 本章目标

完成本章后，你将能够：

-   理解项目是如何启动的。
-   理解 `uvicorn backend.app.main:app` 的含义。
-   理解 `main.py` 在整个项目中的职责。
-   为下一章 `main.py` 源码解析做好准备。

------------------------------------------------------------------------

# 1. 项目真实启动流程

``` text
开发者
    │
    ▼
start_backend.sh
    │
    ▼
uvicorn backend.app.main:app
    │
    ▼
backend/app/main.py
    │
    ▼
create_app()
    │
    ├── 创建 FastAPI Application
    ├── 注册 Middleware
    ├── 注册 Router
    ├── 注册 Exception Handler
    └── 注册 Lifespan
    │
    ▼
Application Ready
    │
    ▼
等待 HTTP Request
```

> 说明：项目启动完成后，并不会立即执行业务逻辑，而是进入等待请求的状态。

------------------------------------------------------------------------

# 2. start_backend.sh

启动脚本负责统一启动方式。

主要职责：

-   设置运行环境
-   启动 Uvicorn
-   指定入口模块

真正启动项目的是：

``` text
uvicorn backend.app.main:app
```

------------------------------------------------------------------------

# 3. uvicorn backend.app.main:app

这一行可以拆成四部分理解。

  部分               含义
  ------------------ --------------------------
  uvicorn            启动 ASGI Server
  backend.app.main   Python 模块路径
  :                  分隔模块与对象
  app                FastAPI Application 实例

因此：

``` text
uvicorn
        │
        ▼
找到 backend/app/main.py
        │
        ▼
读取 app
        │
        ▼
启动 FastAPI
```

------------------------------------------------------------------------

# 4. main.py 的职责

`main.py` 不负责业务分析。

它主要负责：

-   创建 FastAPI Application
-   注册 Middleware
-   注册 Router
-   注册 Lifespan
-   初始化项目

因此可以把它理解成：

> 整个项目的"总装配厂"。

真正的业务会交给：

``` text
Router
    │
Service
    │
Repository
    │
Workflow
```

------------------------------------------------------------------------

# 5. create_app()

项目启动后最重要的方法就是：

``` text
create_app()
```

主要工作：

``` text
create_app()

    │
    ├── FastAPI(...)
    ├── add_middleware(...)
    ├── include_router(...)
    ├── lifespan(...)
    └── 返回 Application
```

> Learning Tip：后续阅读 `main.py` 时，请重点关注 `create_app()`。

------------------------------------------------------------------------

# 6. 为什么先注册 Router？

Router 决定：

当浏览器访问：

``` text
GET /health
POST /api/tasks
```

FastAPI 应该调用哪个 Python 函数。

例如：

``` text
GET /health
      │
      ▼
backend/app/api/health.py

POST /api/tasks
      │
      ▼
backend/app/api/tasks.py
```

------------------------------------------------------------------------

# 7. 项目启动完成后的状态

启动完成后：

``` text
Application Ready
        │
        ▼
Listening...
        │
        ▼
等待 HTTP Request
```

此时：

-   Workflow 尚未执行
-   Repository 尚未访问
-   AI Provider 尚未调用

只有收到请求后，真正的业务流程才开始。

------------------------------------------------------------------------

# 8. 对应 Learning Trace

项目启动属于应用初始化阶段。

目前 Learning Trace 从收到 HTTP Request
开始记录，因此第一次看到的通常是：

``` text
backend/app/main.py
create_app()
    ↓
（路由已注册）
    ↓
backend/app/api/tasks.py
```

这表示应用已经启动完成，请求开始进入 Router。

------------------------------------------------------------------------

# 9. Java（Spring Boot）对照

  Retail Insight AI   Spring Boot
  ------------------- --------------------------------
  start_backend.sh    启动脚本 / mvn spring-boot:run
  Uvicorn             Tomcat
  main.py             SpringBootApplication
  create_app()        Spring 容器初始化
  include_router()    扫描 Controller

------------------------------------------------------------------------

# 10. Learning Tip

★★★★★

不要把 `main.py` 当成业务入口。

它负责的是：

> 创建应用（Application）。

真正的业务入口是：

``` text
Browser
    │
Router
    │
Service
```

------------------------------------------------------------------------

# 本章总结

启动流程可以记成一句话：

``` text
start_backend.sh
    ↓
Uvicorn
    ↓
main.py
    ↓
create_app()
    ↓
FastAPI Application
    ↓
等待 HTTP Request
```

------------------------------------------------------------------------

# 下一章预告

**Chapter 05：main.py 源码解析**

我们将逐行阅读：

-   FastAPI()
-   lifespan()
-   Middleware
-   include_router()
-   为什么 Learning Trace 从这里开始。
