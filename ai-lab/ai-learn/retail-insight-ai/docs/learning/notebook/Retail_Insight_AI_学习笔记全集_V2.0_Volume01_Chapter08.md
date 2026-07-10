# Retail Insight AI 学习笔记全集（正式版 V2.0）

**Volume 01：FastAPI 基础篇**

> Chapter 08：Schema（数据模型）源码解析

------------------------------------------------------------------------

# 文档信息

  项目       内容
  ---------- -----------------
  文档版本   V2.0
  Volume     01
  Chapter    08
  状态       Draft（审阅中）

------------------------------------------------------------------------

# 本章目标

完成本章后，你将理解：

-   什么是 Schema（数据模型）
-   为什么企业项目要使用 Pydantic
-   Request / Response 的区别
-   Schema 在 Retail Insight AI 中的作用
-   为什么 Schema 是 API Contract 的基础

------------------------------------------------------------------------

# 1. 什么是 Schema？

Schema 是**数据模型**。

它规定：

-   有哪些字段
-   每个字段的数据类型
-   哪些字段必填
-   返回数据长什么样

可以理解为：

> **Schema = 数据的说明书（Data Contract）。**

------------------------------------------------------------------------

# 2. Schema 在项目中的位置

``` text
Browser
    │
HTTP Request
    │
Router
    │
Request Schema
    │
Service
    │
Repository
    │
Response Schema
    │
Browser
```

Schema 不负责业务逻辑，只负责**数据结构**。

------------------------------------------------------------------------

# 3. backend/app/schemas/

项目中的 Schema 统一放在：

``` text
backend/app/schemas/
```

常见类型：

``` text
health.py
tasks.py
documents.py
approvals.py
security.py
```

每个模块对应自己的 Request / Response。

------------------------------------------------------------------------

# 4. Request Schema

例如：

``` text
POST /api/tasks
        │
        ▼
TaskCreateRequest
```

作用：

-   校验浏览器提交的数据
-   自动检查类型
-   自动检查必填字段
-   自动生成 Swagger 文档

------------------------------------------------------------------------

# 5. Response Schema

例如：

``` text
health()
      │
      ▼
HealthResponse
      │
      ▼
JSON
```

作用：

-   统一返回格式
-   保证字段一致
-   自动生成 OpenAPI

------------------------------------------------------------------------

# 6. 为什么不用 dict？

很多初学者会问：

> 为什么不用 Python dict？

原因：

``` text
dict
    │
容易缺字段
容易拼写错误
没有类型检查

Schema
    │
自动校验
自动提示
自动文档
自动序列化
```

企业项目几乎都会选择 Schema。

------------------------------------------------------------------------

# 7. Schema 与 Learning Trace

Schema 一般出现在 Router 返回结果之前。

例如：

``` text
backend/app/api/health.py
health()
    ↓
HealthResponse
    ↓
HTTP 200
```

Learning Trace 中出现的 `HealthResponse`，正是 Response Schema。

------------------------------------------------------------------------

# 8. Java（Spring Boot）对照

  Retail Insight AI   Spring Boot
  ------------------- -----------------
  Pydantic Model      DTO
  Request Schema      Request DTO
  Response Schema     Response DTO
  Field 校验          Bean Validation

------------------------------------------------------------------------

# 9. 为什么企业项目这样设计（Why）

没有 Schema：

``` text
Browser
    │
dict
    │
Service
```

容易：

-   字段遗漏
-   类型错误
-   文档不同步

使用 Schema：

``` text
Browser
    │
Schema
    │
Service
```

优势：

-   数据统一
-   API 更稳定
-   Swagger 自动同步
-   IDE 自动补全
-   更容易维护

------------------------------------------------------------------------

# 10. Learning Tip

★★★★★

阅读 API 时，请先看：

1.  Request Schema
2.  Response Schema

然后再阅读 Router。

这样会更容易理解整个接口。

------------------------------------------------------------------------

# 本章总结

Schema 是整个 API 的数据标准。

一句话记忆：

``` text
Request
    │
Schema
    │
Service
    │
Schema
    │
Response
```

业务逻辑属于 Service；

数据结构属于 Schema。

------------------------------------------------------------------------

# 下一章预告

**Chapter 09：Router / Service / Repository**

将深入分析企业项目为什么采用三层架构，以及一次请求如何在三层之间流转。
