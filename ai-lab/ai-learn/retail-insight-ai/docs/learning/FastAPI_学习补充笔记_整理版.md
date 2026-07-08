# FastAPI 学习补充笔记（整理版）

> 根据零散学习笔记重新整理，作为阅读 **LEARNING_API_WALKTHROUGH.md**
> 前的预备知识。

## 1. 推荐学习顺序

1.  `backend/app/main.py` ------ 理解项目启动、Middleware、Router 注册。
2.  `backend/app/api/health.py` ------ 学习最简单的 API。
3.  `backend/app/schemas/health.py` ------ 理解 Response Schema。
4.  回到 `main.py` 理解 `include_router()`。
5.  再学习 `tasks.py`、`services/`、`repositories/`。

------------------------------------------------------------------------

## 2. Router、Service、Repository 三层关系

``` text
tasks.py
    ↓
task_service.py
    ↓
task_repository.py
```

职责：

``` text
Router（接口层）
    ↓
Service（业务层）
    ↓
Repository（数据访问层）
```

-   Router：处理 HTTP 请求
-   Service：处理业务逻辑
-   Repository：访问数据库/文件

------------------------------------------------------------------------

## 3. 一句话理解 FastAPI

``` text
浏览器
    ↓
Router（接收请求）
    ↓
Service（业务处理）
    ↓
Repository（获取数据）
    ↓
Schema（定义返回数据）
    ↓
JSON
    ↓
浏览器
```

> **Schema 不是业务层，而是数据契约（Data Contract）。**

------------------------------------------------------------------------

## 4. api 与 schemas 的职责

``` text
backend/app/

api/
    health.py
    tasks.py

schemas/
    health.py
    task.py
    document.py
```

-   api/：处理 HTTP 请求（Router）
-   schemas/：定义请求与响应的数据结构

记住：

-   Router：处理请求
-   Service：处理业务
-   Repository：访问数据
-   Schema：定义数据结构

------------------------------------------------------------------------

## 5. GET /health 调用过程

``` text
health()
    ↓
HealthResponse
    ↓
return response
```

Learning Trace：

``` text
Swagger / 浏览器
    ↓
main.py（Middleware）
    ↓
health.py
    ↓
health()
    ↓
创建 HealthResponse(...)
    ↓
return response
    ↓
HTTP 200
```

------------------------------------------------------------------------

## 6. 学习建议

每学习一个接口建议：

1.  Swagger 调用接口
2.  阅读 Console Log（Learning Trace）
3.  对照 LEARNING_API_WALKTHROUGH.md
4.  阅读源码（Router → Service → Repository → Schema）

------------------------------------------------------------------------

推荐配合：

-   LEARNING_API_WALKTHROUGH.md
-   FastAPI_项目启动过程_学习笔记.md
-   FastAPI_从启动到一次HTTP请求的完整生命周期.md
-   Retail_Insight_AI_源码阅读路线图_Code_Reading_Roadmap.md
