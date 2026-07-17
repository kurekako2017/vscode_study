# ERIP 企业源码架构手册

# Volume 05：Enterprise（企业架构）

# 第28章（Chapter 28）

# Background Task Pattern（后台任务模式）

> Build Responsive AI Systems

---

# 文档信息

| 项目     | 内容                    |
| -------- | ----------------------- |
| Volume   | 05                      |
| Chapter  | 28                      |
| 技术主题 | Background Task Pattern |
| 难度     | ⭐⭐⭐⭐☆              |
| 推荐程度 | ⭐⭐⭐⭐⭐              |
| 对应框架 | FastAPI BackgroundTasks |

---

# 学习目标

阅读本章后，你应该能够回答：

- 为什么需要 Background Task？
- 为什么 AI Workflow 必须异步执行？
- ERIP 如何使用 BackgroundTasks？
- BackgroundTasks 与 Thread 有什么区别？
- Java Spring 如何实现相同功能？

---

# 一、为什么需要 Background Task？

假设：

AI Workflow

需要：

30 秒。

如果：

```text
POST /api/tasks

↓

Workflow

↓

30 秒

↓

HTTP Response
```

浏览器：

一直等待。

用户体验：

非常差。

所以：

企业系统：

都会：

把长时间任务放到后台执行。

---

# 二、ERIP 当前实现（Current）

执行流程：

```text
Browser

↓

POST /api/tasks

↓

TaskService.create_task()

↓

BackgroundTasks.add_task()

↓

HTTP 202 Accepted

====================

TaskService.run_task()

↓

AnalysisWorkflow.stream()
```

HTTP：

立即返回。

AI：

后台继续执行。

---

# 三、Source Binding（源码绑定）

建议打开：

```text
backend/app/api/tasks.py
```

找到：

```python
BackgroundTasks
```

继续：

```text
TaskService.create_task()
```

观察：

```python
background_tasks.add_task(...)
```

随后：

打开：

```text
backend/app/services/task_service.py
```

阅读：

```python
run_task()
```

最后：

打开：

```text
backend/app/workflow/graph.py
```

找到：

```python
AnalysisWorkflow.stream()
```

整个后台流程：

就是：

```text
BackgroundTasks

↓

run_task()

↓

AnalysisWorkflow
```

---

# 四、Background Task 生命周期

```text
HTTP Request

↓

Router

↓

TaskService

↓

BackgroundTasks.add_task()

↓

HTTP 202

====================

Background

↓

run_task()

↓

Workflow

↓

Completed
```

整个 Workflow：

已经：

不属于：

HTTP 生命周期。

---

# 五、为什么不用 Thread？

很多新人：

第一反应：

就是：

Thread。

例如：

```python
Thread(...)
```

企业：

一般：

不会：

直接：

使用：

Thread。

原因：

- 生命周期难管理
- 异常难处理
- 难扩展
- 难监控

BackgroundTasks：

由：

FastAPI：

统一管理。

更加简单。

---

# 六、企业扩展（Enterprise）

随着系统规模扩大，

BackgroundTasks：

通常会升级：

```text
BackgroundTasks

↓

Celery

↓

RabbitMQ

↓

Redis

↓

Worker Cluster
```

AI Workflow：

交给：

多个 Worker。

真正：

支持：

高并发。

---

# 七、Architecture Thinking（架构思考）

为什么：

Retail Insight AI：

没有：

一开始：

就使用：

RabbitMQ？

因为：

当前：

项目：

属于：

MVP。

BackgroundTasks：

已经满足：

学习、

验证、

Demo。

未来：

企业版：

再升级：

消息队列。

这也是：

企业项目：

逐步演进：

而不是：

一步到位。

---

# 八、Java / Spring 对照

| Retail Insight AI | Spring Boot    |
| ----------------- | -------------- |
| BackgroundTasks   | @Async         |
| run_task()        | Async Service  |
| Workflow          | Async Workflow |
| HTTP 202          | Accepted       |

设计思想：

一致。

---

# 九、VS Code 阅读路线

建议：

```text
tasks.py

↓

BackgroundTasks

↓

TaskService.run_task()

↓

AnalysisWorkflow
```

不要：

直接：

阅读：

Workflow。

---

# 十、Learning Trace 对应

Learning Trace：

会看到：

```text
============= Request =============

↓

202 Accepted

============= Background =============

↓

run_task()

↓

Workflow
```

这是：

整个项目：

最重要的：

调用链。

---

# 十一、面试回答（中文）

为什么使用 BackgroundTasks？

BackgroundTasks 可以将长时间运行的 AI Workflow 与 HTTP 请求解耦，使接口快速返回，提升用户体验。同时后台任务可以独立执行，不阻塞 Web 请求，是现代 AI 系统中非常常见的设计方式。

---

# 十二、面试回答（日语）

BackgroundTasks を利用する理由は何ですか。

BackgroundTasks を利用することで、HTTP リクエストをすぐに返しながら、AI Workflow をバックグラウンドで実行できます。レスポンス性能を維持しつつ、長時間処理を実現できるため、多くの Web システムで利用されています。

---

# 十三、日本 SES 常见追问

Q：

为什么不用同步执行？

回答：

AI：

几十秒。

HTTP：

几百毫秒。

应该：

分离。

否则：

用户：

一直等待。

---

# 十四、本章核心记忆图

```text
Browser

↓

POST /api/tasks

↓

BackgroundTasks

↓

HTTP 202

=================

run_task()

↓

AnalysisWorkflow

↓

Repository

↓

Completed
```

---

# 本章总结

一句话：

```text
HTTP

负责响应。

Background

负责工作。
```

Background Task Pattern 的核心价值在于：

**将 Web 请求与长时间运行任务彻底解耦。**

它保证了 Retail Insight AI 在执行 AI Workflow 时，仍然能够快速响应用户请求，也是企业 AI 系统中最常见的异步架构模式之一。

---

# 下一章

**Chapter 29：Event Driven Architecture（事件驱动架构）**

学习：

- EventPublisher
- Publish / Subscribe
- Event Bus
- 企业事件驱动设计
