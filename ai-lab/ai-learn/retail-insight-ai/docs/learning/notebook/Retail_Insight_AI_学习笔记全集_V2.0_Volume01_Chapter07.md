# Retail Insight AI 学习笔记全集（正式版 V2.0）
> **历史学习笔记**：项目现名 ERIP V1.0；本文保留教学叙述。现状数字与架构以 handbook 权威材料与源码为准。


**Volume 01：FastAPI 基础篇**

> Chapter 07：Router（API 层）源码解析

------------------------------------------------------------------------

# 文档信息

  项目       内容
  ---------- -----------------
  文档版本   V2.0
  Volume     01
  Chapter    07
  状态       Draft（审阅中）

------------------------------------------------------------------------

# 本章目标

完成本章后，你将能够：

-   理解 Router 在整个项目中的职责。
-   理解 `APIRouter` 与 `include_router()` 的关系。
-   学会阅读 `backend/app/api/` 下的源码。
-   理解 Router 如何把 HTTP 请求交给 Service。

------------------------------------------------------------------------

# 1. Router 在整个系统中的位置

``` text
Browser
    │
HTTP Request
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
```

Router 是 HTTP 请求进入业务层的第一站。

------------------------------------------------------------------------

# 2. 为什么需要 Router？

如果所有 API 都写在 `main.py`：

-   文件会越来越大
-   难以维护
-   无法按功能拆分

因此项目采用按业务拆分 Router：

``` text
backend/app/api/
├── health.py
├── tasks.py
├── documents.py
├── approvals.py
└── security.py
```

每个文件负责一类 API。

------------------------------------------------------------------------

# 3. APIRouter

每个 Router 文件都会创建一个 `APIRouter` 实例。

职责：

-   管理当前模块所有接口
-   定义 URL
-   定义 HTTP Method
-   与 `include_router()` 建立关联

可以理解成：

> **Router = 某一类 HTTP 接口的集合。**

------------------------------------------------------------------------

# 4. include_router()

在 `main.py` 中：

``` text
create_app()
      │
      ▼
include_router()
      │
      ├── health.py
      ├── tasks.py
      ├── documents.py
      ├── approvals.py
      └── security.py
```

如果没有注册：

对应接口即使存在源码，也无法访问。

------------------------------------------------------------------------

# 5. tasks.py

这是项目最重要的 Router。

典型流程：

``` text
POST /api/tasks
      │
      ▼
create_task()
      │
      ▼
TaskService.create_task()
```

Router 不负责分析业务。

它只负责：

-   接收 Request
-   调用 Service
-   返回 Response

------------------------------------------------------------------------

# 6. health.py

`GET /health` 是最简单的同步接口。

执行流程：

``` text
GET /health
      │
      ▼
health()
      │
      ▼
HealthResponse
      │
      ▼
HTTP 200
```

适合作为第一个源码阅读入口。

------------------------------------------------------------------------

# 7. Learning Trace 对照

Router 对应 Learning Trace 中最前面的业务入口。

例如：

``` text
backend/app/main.py
create_app()
    ↓
（路由已注册）
    ↓
backend/app/api/tasks.py
create_task()
```

之后请求继续进入：

``` text
TaskService
    ↓
Repository
    ↓
Workflow
```

------------------------------------------------------------------------

# 8. Java（Spring Boot）对照

  Retail Insight AI   Spring Boot
  ------------------- ---------------------
  APIRouter           @RestController
  @router.get         @GetMapping
  @router.post        @PostMapping
  include_router      Controller 扫描注册

------------------------------------------------------------------------

# 9. 学习建议

建议阅读顺序：

1.  `health.py`
2.  `tasks.py`
3.  `documents.py`
4.  `approvals.py`
5.  `security.py`

不要一开始阅读复杂业务接口。

------------------------------------------------------------------------

# 10. 本章总结

Router 的职责可以概括为：

``` text
HTTP Request
      │
      ▼
Router
      │
      ▼
Service
```

Router 是 HTTP 世界与业务世界之间的桥梁。

------------------------------------------------------------------------

# 下一章预告

**Chapter 08：Schema（数据模型）**

将学习：

-   Request / Response
-   Pydantic
-   HealthResponse
-   TaskResponse
-   为什么企业项目需要 Schema。
