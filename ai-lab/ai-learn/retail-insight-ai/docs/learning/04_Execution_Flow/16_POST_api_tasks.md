
# Retail Insight AI 企业源码架构手册

# Volume 04：Execution Flow（源码执行流程）

# Chapter 16

# POST /api/tasks 执行全过程

> Everything starts here.

---

# 文档信息

| 项目     | 内容                                 |
| -------- | ------------------------------------ |
| Volume   | 04                                   |
| Chapter  | 16                                   |
| 接口     | POST /api/tasks                      |
| 入口文件 | backend/app/api/tasks.py             |
| Service  | backend/app/services/task_service.py |
| Workflow | backend/app/workflow/graph.py        |
| Event    | backend/app/events/publisher.py      |
| 推荐程度 | ⭐⭐⭐⭐⭐                           |

---

# 学习目标

阅读本章后，你应该能够回答：

- POST /api/tasks 为什么返回 202？
- BackgroundTasks 为什么存在？
- create_task() 和 run_task() 有什么区别？
- Workflow 是什么时候开始执行的？
- Learning Trace 为什么分成 Request 与 Background？
- EventPublisher 为什么最后才执行？
- SSE 为什么能够实时更新页面？

---

# 一、接口说明（API）

接口：

```http
POST /api/tasks
```

作用：

创建一个新的 AI 分析任务。

浏览器发送请求后：

系统不会等待 AI 分析完成，

而是：

立即返回：

```http
202 Accepted
```

后台继续执行 AI Workflow。

---

# 二、HTTP Request 生命周期

整个请求生命周期如下：

```text
Browser

↓

POST /api/tasks

↓

FastAPI

↓

tasks.py

↓

TaskService.create_task()

↓

Repository.create()

↓

Repository.save()

↓

BackgroundTasks.add_task()

↓

HTTP 202
```

至此：

HTTP Request

结束。

随后：

后台开始真正执行 AI Workflow。

---

# 三、后台执行生命周期

Background Task：

开始运行：

```text
TaskService.run_task()

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

Completed
```

注意：

真正耗时的是：

```
AnalysisWorkflow.stream()
```

而不是：

HTTP Request。

---

# 四、源码入口 ⭐⭐⭐⭐⭐

打开：

```text
backend/app/api/tasks.py
```

找到：

```python
@router.post("/tasks")
```

这是：

整个 Retail Insight AI

真正的入口。

随后：

调用：

```python
TaskService.create_task()
```

---

继续进入：

```text
backend/app/services/task_service.py
```

找到：

```python
create_task()
```

这里负责：

- 创建 Task
- 初始化状态
- 保存 Repository
- 启动 BackgroundTasks

---

随后：

调用：

```python
BackgroundTasks.add_task()
```

启动：

```python
run_task()
```

HTTP 返回：

```http
202 Accepted
```

---

# 五、源码执行流程 ⭐⭐⭐⭐⭐

```text
Browser

↓

POST /api/tasks

↓

tasks.py

↓

TaskService.create_task()

↓

TaskRepository.create()

↓

TaskRepository.save()

↓

BackgroundTasks.add_task()

↓

HTTP 202

========================

TaskService.run_task()

↓

TaskRepository.save()

↓

AnalysisWorkflow.stream()

↓

Route

↓

KPI Workflow

↓

Research Agent

↓

Report Generator

↓

TaskRepository.save()

↓

EventPublisher.publish()

↓

Completed
```

这张图建议以后熟记。

---

# 六、关键源码文件

| 文件              | 职责                   |
| ----------------- | ---------------------- |
| main.py           | FastAPI 应用入口       |
| tasks.py          | Router，接收 HTTP 请求 |
| task_service.py   | 任务创建与后台执行     |
| graph.py          | AI Workflow            |
| publisher.py      | 发布事件               |
| learning_trace.py | 输出 Learning Trace    |

---

# 七、关键函数

## tasks.py

```python
@router.post("/tasks")
```

作用：

HTTP 接口入口。

---

## TaskService.create_task()

作用：

创建任务。

负责：

- 创建 Task
- 保存 Repository
- 返回 HTTP 202

不会：

执行 AI。

---

## TaskService.run_task()

作用：

真正执行 AI Workflow。

这是整个项目：

最重要的方法之一。

---

## AnalysisWorkflow.stream()

作用：

驱动：

整个 Workflow。

包括：

- Route
- KPI
- Research
- Report

---

## EventPublisher.publish()

作用：

通知：

前端。

例如：

```
Running

Completed

Failed
```

---

# 八、调用关系图 ⭐⭐⭐⭐⭐

```text
Browser
    │
    ▼
POST /api/tasks
    │
    ▼
tasks.py
    │
    ▼
TaskService.create_task()
    │
    ├───────────────┐
    ▼               ▼
Repository     BackgroundTasks
                    │
                    ▼
             TaskService.run_task()
                    │
                    ▼
       AnalysisWorkflow.stream()
                    │
      ┌─────────────┼────────────┐
      ▼             ▼            ▼
    Route         KPI       Research
                                  │
                                  ▼
                           Report Generator
                                  │
                                  ▼
                         Repository.save()
                                  │
                                  ▼
                     EventPublisher.publish()
                                  │
                                  ▼
                                SSE
                                  │
                                  ▼
                         React Dashboard
```

---

# 九、Learning Trace 对应 ⭐⭐⭐⭐⭐

Request：

```text
============= Request =============

POST /api/tasks

↓

TaskService.create_task()
```

随后：

Background：

```text
============= Background =============

TaskService.run_task()

↓

AnalysisWorkflow.stream()

↓

Repository.save()

↓

EventPublisher.publish()
```

Learning Trace：

最大的价值：

就是帮助理解：

Request

什么时候结束。

Background

什么时候开始。

---

# 十、Console Log 对应

Console：

例如：

```text
Task Created

↓

Task Running

↓

Task Completed
```

Learning Trace：

记录：

调用链。

Console：

记录：

执行状态。

两者作用不同。

---

# 十一、VS Code 调试路线 ⭐⭐⭐⭐⭐

建议：

```text
main.py

↓

tasks.py

↓

TaskService.create_task()

↓

TaskService.run_task()

↓

graph.py

↓

AnalysisWorkflow.stream()

↓

publisher.py
```

不要：

跳着阅读。

---

# 十二、为什么采用 BackgroundTasks（Why）

如果：

HTTP：

等待：

AI 分析完成。

浏览器：

可能等待：

几十秒。

体验很差。

因此：

采用：

```text
HTTP

↓

202 Accepted

↓

BackgroundTasks

↓

Workflow
```

这是企业项目常见设计。

---

# 十三、Java / Spring 对照

| Retail Insight AI | Spring Boot    |
| ----------------- | -------------- |
| Router            | Controller     |
| TaskService       | Service        |
| Repository        | Repository     |
| BackgroundTasks   | @Async         |
| Workflow          | Process Engine |

整体设计思想非常接近。

---

# 十四、常见问题（FAQ）

### Q1：为什么返回 202？

因为任务已经创建成功，

但后台仍在执行 AI Workflow。

---

### Q2：为什么 create_task() 不直接调用 Workflow？

为了让 HTTP 快速返回。

Workflow 放到后台执行。

---

### Q3：为什么需要 Repository.save() 多次？

因为每个阶段：

都会更新：

Task Status。

---

### Q4：为什么 EventPublisher 最后才执行？

Workflow：

完成一个阶段后，

需要通知：

前端。

---

# 十五、面试回答（中文）

面试官：

> POST /api/tasks 的执行流程是什么？

回答：

> 浏览器发送 POST /api/tasks 请求后，FastAPI Router 首先进入 tasks.py，然后调用 TaskService.create_task() 创建任务并保存 Repository。随后通过 BackgroundTasks 启动 run_task()，HTTP 接口立即返回 202 Accepted。后台再调用 AnalysisWorkflow.stream() 执行 Route、KPI、Research 和 Report 等 AI Workflow，每完成一个阶段都会更新 Repository，并通过 EventPublisher 发布事件，最终由 SSE 将任务状态实时推送到前端。

---

# 十六、面试回答（日语）

面接官：

> POST /api/tasks の実行フローを説明してください。

回答例：

> ブラウザから POST /api/tasks が送信されると、FastAPI の Router が tasks.py にリクエストを振り分けます。その後、TaskService.create_task() がタスクを作成し、Repository に保存します。HTTP は 202 Accepted を返し、BackgroundTasks により run_task() が非同期で開始されます。run_task() は AnalysisWorkflow.stream() を呼び出し、Route、KPI、Research、Report の各ステップを順番に実行します。各ステップの状態は Repository に保存され、EventPublisher を通じて SSE でフロントエンドへリアルタイムに通知されます。

---

# 十七、日本SES常见追问

### 为什么不用同步执行？

回答：

AI 分析耗时较长，

同步执行会阻塞 HTTP 请求。

因此采用：

```
202 Accepted

↓

BackgroundTasks

↓

Workflow
```

既保证响应速度，

又提升用户体验。

---

# 本章总结

一句话记住：

```text
POST /api/tasks

↓

TaskService.create_task()

↓

HTTP 202

↓

BackgroundTasks

↓

AnalysisWorkflow

↓

Repository

↓

EventPublisher

↓

SSE
```

这就是整个 Retail Insight AI 最重要的一条执行链。

掌握这一章，

就掌握了整个项目最核心的运行流程。

---

# 下一章

**Chapter 17：GET /api/tasks**

学习：

- GET 请求执行流程
- Repository 查询
- Response 返回
- Dashboard 数据刷新
