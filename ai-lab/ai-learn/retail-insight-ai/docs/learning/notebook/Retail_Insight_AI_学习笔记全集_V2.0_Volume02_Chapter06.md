# Retail Insight AI 学习笔记全集（正式版 V2.0）
> **历史学习笔记**：项目现名 ERIP V1.0；本文保留教学叙述。现状数字与架构以 handbook 权威材料与源码为准。


# Volume 02：Workflow、Learning Trace 与 LangGraph

> Chapter 06：Learning Trace、EventPublisher 与 SSE

------------------------------------------------------------------------

# 文档信息

  项目       内容
  ---------- -----------------
  文档版本   V2.0
  Volume     02
  Chapter    06
  状态       Draft（审阅中）

------------------------------------------------------------------------

# 本章目标

完成本章后，你将理解：

-   Learning Trace 为什么存在
-   `trace_step()` 与 `log_event()` 的区别
-   EventPublisher 的职责
-   SSE 如何把后台状态实时推送到前端

------------------------------------------------------------------------

# 1. 三者之间的关系

``` text
TaskService.run_task()
        │
        ▼
trace_step()
        │
        ▼
EventPublisher.publish()
        │
        ▼
SSE
        │
        ▼
Frontend
```

它们共同工作，但职责完全不同。

------------------------------------------------------------------------

# 2. trace_step()

源码位置：

``` text
backend/app/core/learning_trace.py
```

职责：

-   记录程序执行阶段（Execution Flow）
-   输出 Learning Trace
-   帮助阅读源码
-   不影响业务逻辑

例如：

``` text
TaskService.create_task()
      │
trace_step()
      │
Console Log
```

> **trace_step() 负责"记录"，不负责"执行"。**

------------------------------------------------------------------------

# 3. log_event()

`log_event()` 负责记录事件日志。

典型内容：

-   running
-   completed
-   failed

与 `trace_step()` 的区别：

  trace_step()   log_event()
  -------------- --------------
  程序执行阶段   业务事件
  面向开发学习   面向运行状态
  输出调用链     输出事件信息

两者经常一起出现，但目的不同。

------------------------------------------------------------------------

# 4. EventPublisher.publish()

源码位置：

``` text
backend/app/events/publisher.py
```

职责：

-   发布任务事件
-   推送运行状态
-   通知 SSE
-   解耦 Workflow 与前端

调用关系：

``` text
Workflow
    │
EventPublisher.publish()
    │
Event Queue
    │
SSE
```

------------------------------------------------------------------------

# 5. 为什么 EventPublisher 独立？

如果 Workflow 直接更新前端：

``` text
Workflow
   │
Frontend
```

会导致强耦合。

采用发布者模式：

``` text
Workflow
   │
EventPublisher
   │
SSE
   │
Frontend
```

Workflow 不需要知道前端是谁。

------------------------------------------------------------------------

# 6. 什么是 SSE？

SSE（Server-Sent Events）允许服务器主动向浏览器发送事件。

在本项目中：

``` text
Browser
    │
建立 SSE 连接
    │
等待事件
    │
EventPublisher.publish()
    │
Running
KPI Completed
Research Completed
Report Completed
```

因此用户无需不断刷新页面。

------------------------------------------------------------------------

# 7. 一次完整流程

``` text
POST /api/tasks
        │
HTTP 202
        │
Background
        │
trace_step()
        │
EventPublisher.publish()
        │
SSE
        │
Frontend 更新状态
```

Learning Trace 与 EventPublisher 同时工作：

-   Learning Trace：给开发者看
-   EventPublisher：给前端看

------------------------------------------------------------------------

# 8. 企业为什么这样设计（Why）

把三个职责拆开：

``` text
Learning Trace
    │
程序学习

EventPublisher
    │
事件发布

SSE
    │
实时通信
```

优点：

-   单一职责
-   易维护
-   易扩展
-   可替换通信方式（SSE/WebSocket）

------------------------------------------------------------------------

# 9. Java 对照

  Retail Insight AI   Java / Spring
  ------------------- ---------------------------
  trace_step()        调试调用链日志
  EventPublisher      ApplicationEventPublisher
  SSE                 SseEmitter
  Learning Trace      开发辅助日志

------------------------------------------------------------------------

# Learning Tip

★★★★★

看到下面两个调用时：

``` python
trace_step(...)
EventPublisher.publish(...)
```

先问自己：

-   一个是在记录程序流程？
-   一个是在通知外部事件？

分清职责，就不会混淆。

------------------------------------------------------------------------

# 本章总结

``` text
Workflow
   │
trace_step()
   │
Learning Trace

Workflow
   │
EventPublisher
   │
SSE
   │
Frontend
```

两条链路同时存在，但面向不同对象。

------------------------------------------------------------------------

# 下一章预告

**Volume 02 · Chapter 07：BackgroundTasks 深度解析**

将讲解：

-   FastAPI BackgroundTasks
-   为什么 POST /api/tasks 返回 HTTP 202
-   Request 与 Background 如何衔接
-   TaskService.run_task() 为什么在后台执行
