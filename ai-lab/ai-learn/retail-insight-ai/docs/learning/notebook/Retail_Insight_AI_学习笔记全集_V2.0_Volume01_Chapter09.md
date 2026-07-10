# Retail Insight AI 学习笔记全集（正式版 V2.0）

**Volume 01：FastAPI 基础篇**

> Chapter 09：Router / Service / Repository（三层架构源码解析）

------------------------------------------------------------------------

# 文档信息

  项目       内容
  ---------- -----------------
  文档版本   V2.0
  Volume     01
  Chapter    09
  状态       Draft（审阅中）

------------------------------------------------------------------------

# 本章目标

完成本章后，你将能够：

-   理解为什么企业项目采用三层架构。
-   理解 Router、Service、Repository 的职责。
-   理解一次 HTTP 请求如何在三层之间流转。
-   阅读 `create_task()` 的完整调用链。

------------------------------------------------------------------------

# 1. 三层架构总览

``` text
Browser
    │
HTTP Request
    │
Router
    │
Service
    │
Repository
    │
Database / Memory
```

三层分工明确，每层只负责自己的职责。

------------------------------------------------------------------------

# 2. Router（API 层）

源码位置：

``` text
backend/app/api/tasks.py
```

职责：

-   接收 HTTP 请求
-   读取 Request Schema
-   调用 Service
-   返回 Response

典型流程：

``` text
POST /api/tasks
      │
      ▼
create_task()
```

> Router 不负责业务判断，也不直接访问数据库。

------------------------------------------------------------------------

# 3. Service（业务层）

源码位置：

``` text
backend/app/services/task_service.py
```

典型函数：

``` text
TaskService.create_task()
```

职责：

-   编排业务流程
-   调用 Repository
-   发布 Event
-   启动 BackgroundTasks

调用关系：

``` text
Router
   │
   ▼
TaskService.create_task()
```

------------------------------------------------------------------------

# 4. Repository（数据访问层）

源码位置：

``` text
backend/app/repositories/
```

典型函数：

``` text
TaskRepository.create()
TaskRepository.save()
```

职责：

-   保存数据
-   查询数据
-   更新数据

Repository 不关心 HTTP，也不关心 AI Workflow。

------------------------------------------------------------------------

# 5. 一次真实调用链

创建任务时：

``` text
Browser
    │
POST /api/tasks
    │
Router
(create_task)
    │
Service
(TaskService.create_task)
    │
Repository
(create)
    │
EventPublisher.publish()
    │
BackgroundTasks.add_task()
    │
HTTP 202
```

后台继续：

``` text
TaskService.run_task()
      │
AnalysisWorkflow.stream()
      │
Repository.save()
```

------------------------------------------------------------------------

# 6. Learning Trace 对照

对应 Console Log：

``` text
Request
    │
tasks.py
    │
TaskService.create_task()
    │
TaskRepository.create()
    │
EventPublisher.publish()
    │
BackgroundTasks.add_task()
```

随后进入：

``` text
Background
    │
TaskService.run_task()
    │
AnalysisWorkflow.stream()
    │
Repository.save()
```

------------------------------------------------------------------------

# 7. 为什么企业项目这样设计（Why）

## 为什么 Router 不写业务？

如果 Router 写业务：

``` text
Router
 ├── HTTP
 ├── SQL
 ├── AI
 └── Report
```

文件会越来越大。

采用三层后：

``` text
Router
    │
Service
    │
Repository
```

优点：

-   易维护
-   易测试
-   易扩展
-   职责单一

------------------------------------------------------------------------

# 8. Java（Spring Boot）对照

  Retail Insight AI           Spring Boot
  --------------------------- ----------------------
  Router                      Controller
  Service                     Service
  Repository                  Repository / DAO
  TaskService.create_task()   Service#createTask()
  TaskRepository.create()     save()

------------------------------------------------------------------------

# 9. 学习建议

建议阅读顺序：

1.  api/tasks.py
2.  TaskService.create_task()
3.  TaskRepository.create()
4.  EventPublisher.publish()
5.  BackgroundTasks.add_task()
6.  TaskService.run_task()
7.  AnalysisWorkflow.stream()

不要跳着读，这样最容易理解调用链。

------------------------------------------------------------------------

# 10. 本章总结

一句话记忆：

``` text
Router
    │
负责 HTTP

Service
    │
负责业务

Repository
    │
负责数据
```

三层共同组成企业项目最基础的后端架构。

------------------------------------------------------------------------

# 下一章预告

**Chapter 10：源码阅读路线（Code Reading Roadmap）**

我们将结合整个项目，建立从 `main.py` 到 `Workflow`
的完整源码阅读顺序，并给出第一轮、第二轮、第三轮学习建议。
