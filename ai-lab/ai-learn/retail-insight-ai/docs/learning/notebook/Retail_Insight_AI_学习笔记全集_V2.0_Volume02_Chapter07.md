> **历史学习笔记**：项目现名 ERIP V1.0；本文保留教学叙述。现状数字与架构以 handbook 权威材料与源码为准。


# Retail Insight AI 学习笔记全集（正式版 V2.0）

# Volume 02：Workflow、Learning Trace 与 LangGraph

> Chapter 07：BackgroundTasks 深度解析

---

# 文档信息

| 项目     | 内容            |
| -------- | --------------- |
| 文档版本 | V2.0            |
| Volume   | 02              |
| Chapter  | 07              |
| 状态     | Draft（审阅中） |

---

# 本章目标

完成本章后，你将能够：

- 理解 FastAPI BackgroundTasks 的工作机制
- 理解为什么 POST /api/tasks 返回 HTTP 202
- 理解 Request 与 Background 的生命周期
- 理解 TaskService.run_task() 为什么放到后台执行

---

# 1. BackgroundTasks 是什么？

BackgroundTasks 是 FastAPI 提供的后台任务机制。

它允许：

> **HTTP Response 已经返回，但后台任务继续执行。**

因此：

```text
Request
    │
HTTP 202
    │
──────────── 浏览器请求结束 ────────────
    │
Background Task
    │
继续运行
```

---

# 2. 在 Retail Insight AI 中的位置

真实调用流程：

```text
POST /api/tasks
        │
        ▼
create_task()
        │
        ▼
TaskService.create_task()
        │
        ▼
BackgroundTasks.add_task(
        run_task
)
        │
        ▼
HTTP 202 Response
```

这里：

真正加入后台的是：

```
TaskService.run_task()
```

---

# 3. 为什么返回 HTTP 202？

HTTP 202：

表示：

> **服务器已经接受任务。**

并不是：

> **任务已经完成。**

因此：

```text
POST /api/tasks

↓

HTTP 202

↓

Task ID

↓

Background

↓

Workflow

↓

Completed
```

---

# 4. Request 生命周期

Request 阶段：

```text
Browser

↓

POST /api/tasks

↓

Router

↓

TaskService.create_task()

↓

Repository.create()

↓

BackgroundTasks.add_task()

↓

HTTP 202
```

这里：

浏览器工作已经结束。

---

# 5. Background 生命周期

HTTP Response 返回以后：

```text
TaskService.run_task()

↓

Learning Trace

↓

Workflow

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

Completed
```

这一部分：

浏览器不会等待。

---

# 6. 为什么企业项目采用 Background？

假设 AI 分析：

需要：

20 秒。

如果不用 Background：

```text
Browser

等待...

等待...

等待...

等待...

20 秒
```

用户体验很差。

采用：

```text
HTTP 202

↓

立即返回

↓

后台分析

↓

SSE 推送
```

体验更好。

---

# 7. Background 与 Learning Trace

Learning Trace：

真正开始的位置：

```text
============= Background =============

TaskRepository.save()

↓

EventPublisher.publish()

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
```

因此：

Learning Trace 可以完整记录后台流程。

---

# 8. Background 与 EventPublisher

后台运行时：

每完成一步：

```text
Workflow

↓

EventPublisher.publish()

↓

SSE

↓

Frontend
```

前端：

立即看到：

```
Running

↓

KPI Completed

↓

Research Completed

↓

Report Completed
```

---

# 9. Background 与 LangGraph

LangGraph：

本身：

不知道：

HTTP。

它只是：

执行 Workflow。

真正把：

HTTP

↓

Background

↓

LangGraph

连接起来的是：

```text
TaskService.run_task()
```

因此：

TaskService：

既属于：

FastAPI。

又属于：

LangGraph。

它是：

二者之间的桥梁。

---

# 10. Java 对照

| Retail Insight AI | Spring Boot   |
| ----------------- | ------------- |
| BackgroundTasks   | @Async        |
| HTTP 202          | Accepted      |
| run_task()        | Async Service |
| SSE               | SseEmitter    |

---

# 企业为什么这样设计（Why）

真正的职责：

```text
Router

负责 HTTP

↓

TaskService

负责启动后台

↓

Background

负责长时间运行

↓

Workflow

负责 AI

↓

EventPublisher

负责通知

↓

Frontend
```

每层：

只有一种职责。

---

# Learning Tip

★★★★★

以后：

看到：

```
BackgroundTasks.add_task()
```

立即想到：

```
HTTP Response

已经结束。

后台：

才刚刚开始。
```

这是：

理解：

Learning Trace

Workflow

EventPublisher

SSE

的关键。

---

# 本章总结

一句话：

```text
Request

↓

HTTP 202

↓

Background

↓

Workflow

↓

EventPublisher

↓

SSE

↓

Frontend
```

整个 Retail Insight AI：

都是围绕这一条链路设计的。

---

# 下一章预告

**Volume 02 · Chapter 08：TaskService.run_task() 源码精读**

下一章将逐行分析：

- TaskService.run_task()
- 为什么它是 FastAPI 与 LangGraph 的桥梁
- 谁调用它？
- 它调用谁？
- 每一行代码负责什么？
- 与 Learning Trace 的对应关系
