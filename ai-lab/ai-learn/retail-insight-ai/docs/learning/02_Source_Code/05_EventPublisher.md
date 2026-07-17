# ERIP 源码精读系列

# 05_EventPublisher.md

> Source Code Deep Dive

------------------------------------------------------------------------

# 文档信息

  ---------------------------------------------------------------------------------------------------------------------------------------------
  项目                                内容
  ----------------------------------- ---------------------------------------------------------------------------------------------------------
  系列                                Source Code Deep Dive

  文档                                05

  主题                                EventPublisher.publish()

  对应源码                            backend/app/events/publisher.py

  关联源码                            backend/app/services/task_service.py、backend/app/workflow/graph.py、backend/app/core/learning_trace.py

  难度                                ★★★★☆
  ---------------------------------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# 学习目标

阅读完本文后，你应该能够回答：

-   EventPublisher 是什么？
-   为什么项目要单独设计 EventPublisher？
-   `publish()` 是谁调用的？
-   它为什么和 SSE 有关系？
-   它和 `trace_step()`、`log_event()` 有什么区别？

------------------------------------------------------------------------

# 一、源码位置

``` text
backend/app/events/publisher.py
```

重点关注：

``` python
class EventPublisher
```

以及：

``` python
publish(...)
```

------------------------------------------------------------------------

# 二、EventPublisher 是什么？

一句话：

> **EventPublisher 是整个项目的事件发布中心（Event Bus）。**

它负责：

-   发布任务状态
-   发布 Workflow 进度
-   发布完成事件
-   通知订阅者（如 SSE）

它**不负责业务处理**。

------------------------------------------------------------------------

# 三、谁调用 publish()？

真实调用链：

``` text
POST /api/tasks
      │
TaskService.create_task()
      │
publish(running)
      │
Background
      │
AnalysisWorkflow.stream()
      │
publish(progress)
      │
Workflow 完成
      │
publish(completed)
```

因此：

> `publish()` 被 Service、Workflow
> 等业务层调用，用于通知外部"发生了什么"。

------------------------------------------------------------------------

# 四、为什么需要 EventPublisher？

如果没有 EventPublisher：

``` text
TaskService
    │
直接通知 Frontend
```

那么：

-   Service 依赖前端
-   Workflow 依赖前端
-   更换通信方式困难

采用 EventPublisher 后：

``` text
TaskService
      │
EventPublisher
      │
SSE / WebSocket / MQ
      │
Frontend
```

业务层只负责发布事件，不关心谁接收。

------------------------------------------------------------------------

# 五、publish() 的职责

可以理解为：

``` text
收到业务事件
      │
创建 Event
      │
广播 Event
      │
通知所有订阅者
```

例如：

``` text
Task Running

↓

publish()

↓

running Event

↓

Frontend 更新
```

------------------------------------------------------------------------

# 六、publish() 常见事件

典型事件：

``` text
queued
running
progress
completed
failed
```

这些事件通常对应任务生命周期。

例如：

``` text
Queued

↓

Running

↓

Progress

↓

Completed
```

------------------------------------------------------------------------

# 七、publish() 与 Workflow

Workflow 每完成一个节点：

``` text
Route

↓

publish(progress)

↓

KPI

↓

publish(progress)

↓

Research

↓

publish(progress)

↓

Report

↓

publish(completed)
```

因此前端能够看到：

``` text
Running...

↓

KPI Completed

↓

Research Completed

↓

Report Completed
```

------------------------------------------------------------------------

# 八、publish() 与 SSE

EventPublisher：

本身：

不知道浏览器。

它只负责：

``` text
Publish Event
```

真正发送：

``` text
Event

↓

SSE

↓

Browser
```

因此：

EventPublisher 和 SSE 是：

> **发布者（Publisher）+ 传输层（Transport）**

关系。

------------------------------------------------------------------------

# 九、publish() 与 trace_step()

很多初学者容易混淆：

``` python
trace_step(...)
publish(...)
```

区别：

  trace_step()   publish()
  -------------- ---------------
  学习调用链     发布业务事件
  Console Log    Event Stream
  给开发者       给系统 / 前端
  不改变业务     推动系统通信

------------------------------------------------------------------------

# 十、publish() 与 log_event()

区别：

  log_event()   publish()
  ------------- --------------
  写日志        发布事件
  面向调试      面向消息通知
  Console       Event Bus

有时会一起出现：

``` python
log_event(...)
publish(...)
```

但：

一个是记录。

一个是通知。

------------------------------------------------------------------------

# 十一、为什么企业项目喜欢 Event Bus？

原因：

``` text
Workflow
      │
publish()
      │
──────────────
│      │      │
SSE   MQ   Audit
```

未来：

增加：

-   Kafka
-   RabbitMQ
-   Redis Pub/Sub

Workflow 完全不用修改。

因此：

EventPublisher 提供了很好的扩展能力。

------------------------------------------------------------------------

# 十二、对应 Console Log

Learning Trace 中：

``` text
TaskRepository.save()

↓

EventPublisher.publish()

↓

AnalysisWorkflow.stream()
```

这里看到的是：

Workflow 发布了一个运行事件。

真正的事件内容：

例如：

``` text
status=running
```

则由 EventPublisher 负责发送。

------------------------------------------------------------------------

# 十三、企业为什么这样设计（Why）

如果没有 EventPublisher：

``` text
Workflow

↓

Frontend
```

耦合严重。

现在：

``` text
Workflow

↓

EventPublisher

↓

SSE

↓

Frontend
```

Workflow 不需要知道：

-   React
-   Vue
-   WebSocket
-   SSE

职责更加单一。

------------------------------------------------------------------------

# 十四、Java / Spring 对照

  Retail Insight AI   Spring Boot
  ------------------- ---------------------------
  EventPublisher      ApplicationEventPublisher
  publish()           publishEvent()
  Subscriber          @EventListener
  SSE                 SseEmitter

------------------------------------------------------------------------

# 十五、面试回答

如果面试官问：

> 为什么项目使用 EventPublisher？

可以回答：

> EventPublisher 将业务处理与消息通知解耦。Workflow 和 Service
> 只负责发布事件，不需要关心事件最终由 SSE、WebSocket
> 或消息队列消费，从而提高系统的可扩展性和可维护性。

------------------------------------------------------------------------

# 十六、源码阅读建议

建议顺序：

``` text
publisher.py
      │
publish()
      │
TaskService.run_task()
      │
AnalysisWorkflow.stream()
      │
SSE
```

边看源码，边观察：

``` python
publish(...)
```

在什么时候调用。

------------------------------------------------------------------------

# 本章总结

一句话记住：

``` text
EventPublisher.publish()

=

整个项目的事件广播中心
```

它负责：

-   发布状态
-   通知外部
-   解耦 Workflow
-   支持 SSE
-   为未来 MQ 留出扩展空间

------------------------------------------------------------------------

# 下一章

**06_BackgroundTasks.md**

将继续精读：

-   FastAPI BackgroundTasks
-   为什么 HTTP 202 后任务仍继续运行
-   Request 与 Background 的生命周期
-   BackgroundTasks 如何连接 TaskService.run_task()
