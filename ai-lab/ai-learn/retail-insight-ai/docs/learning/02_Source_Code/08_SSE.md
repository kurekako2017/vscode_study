# ERIP 源码精读系列

# 08_SSE.md

> Source Code Deep Dive

------------------------------------------------------------------------

# 文档信息

  项目       内容
  ---------- -----------------------------------------------------------
  系列       Source Code Deep Dive
  文档       08
  主题       Server-Sent Events (SSE)
  对应源码   backend/app/events/、backend/app/api/tasks.py（事件相关）
  难度       ★★★★☆

------------------------------------------------------------------------

# 学习目标

阅读完本文后，你应该能够回答：

-   什么是 SSE？
-   为什么项目选择 SSE？
-   SSE 与 EventPublisher 如何配合？
-   浏览器如何实时收到 AI Workflow 的执行状态？

------------------------------------------------------------------------

# 一、什么是 SSE？

SSE（Server-Sent Events）是一种 **服务器主动向浏览器推送消息** 的 HTTP
技术。

与普通 HTTP 不同：

``` text
普通 HTTP

Browser
    │ Request
    ▼
Server
    │ Response
    ▼
结束
```

SSE：

``` text
Browser
    │ 建立连接
    ▼
Server
    │
    ├── Running
    ├── KPI Completed
    ├── Research Completed
    └── Report Completed
```

连接保持开启，服务器可以持续发送事件。

------------------------------------------------------------------------

# 二、为什么使用 SSE？

ERIP 的 AI Workflow 可能持续数秒甚至数十秒。

如果没有 SSE：

``` text
Browser

↓

不停刷新

↓

GET /status
```

采用 SSE：

``` text
Workflow

↓

EventPublisher.publish()

↓

SSE

↓

Browser 自动更新
```

浏览器无需轮询。

------------------------------------------------------------------------

# 三、项目中的整体位置

``` text
TaskService.run_task()
        │
AnalysisWorkflow.stream()
        │
EventPublisher.publish()
        │
SSE
        │
Frontend Dashboard
```

SSE 位于 **EventPublisher 与前端之间**。

------------------------------------------------------------------------

# 四、SSE 与 EventPublisher

EventPublisher：

负责：

``` text
发布事件
```

SSE：

负责：

``` text
传输事件
```

关系：

``` text
Workflow
    │
EventPublisher
    │
SSE
    │
Browser
```

职责清晰分离。

------------------------------------------------------------------------

# 五、Workflow 执行过程

后台执行：

``` text
Route
    │
publish(progress)
    │
KPI
    │
publish(progress)
    │
Research
    │
publish(progress)
    │
Report
    │
publish(completed)
```

浏览器看到：

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

# 六、SSE 与 Learning Trace

Learning Trace：

``` text
============= Background =============

AnalysisWorkflow.stream()

↓

Route

↓

Research
```

SSE：

``` text
Running

↓

Progress

↓

Completed
```

Learning Trace 给开发者。

SSE 给用户界面。

------------------------------------------------------------------------

# 七、SSE 与 WebSocket

  SSE                WebSocket
  ------------------ ----------------------
  服务端→客户端      双向通信
  基于 HTTP          独立协议
  实现简单           功能更丰富
  非常适合状态推送   适合聊天室、协同编辑

Retail Insight AI 主要需求是：

> **服务器持续推送分析状态。**

因此 SSE 足够且实现简单。

------------------------------------------------------------------------

# 八、企业为什么这样设计（Why）

拆分职责：

``` text
Workflow
    │
EventPublisher
    │
SSE
    │
Frontend
```

Workflow 不依赖前端框架。

未来即使改成：

-   WebSocket
-   Kafka
-   RabbitMQ

Workflow 基本无需修改。

------------------------------------------------------------------------

# 九、Java / Spring 对照

  Retail Insight AI   Spring Boot
  ------------------- ---------------------------
  SSE                 SseEmitter
  EventPublisher      ApplicationEventPublisher
  publish()           publishEvent()

------------------------------------------------------------------------

# 十、面试回答

如果面试官问：

> 为什么选择 SSE？

可以回答：

> 项目主要需求是服务器持续向前端推送 AI Workflow
> 的执行状态，不需要客户端主动发送大量实时消息，因此采用实现简单、基于
> HTTP 的 SSE。EventPublisher 负责发布事件，SSE
> 负责将事件实时推送到浏览器，两者职责分离，便于维护和扩展。

------------------------------------------------------------------------

# 十一、源码阅读建议

建议阅读：

``` text
EventPublisher.publish()

↓

SSE 推送逻辑

↓

Frontend EventSource

↓

Dashboard 更新
```

结合浏览器开发者工具观察事件流。

------------------------------------------------------------------------

# 本章总结

一句话记住：

``` text
SSE

=

AI Workflow 的实时状态传输通道
```

它负责把后台分析过程持续推送给浏览器，而不参与任何业务逻辑。

------------------------------------------------------------------------

# 下一章

**09_任务持久化子系统.md**

将深入解析：

-   Repository Pattern
-   TaskRepository
-   create()
-   save()
-   update()
-   InMemory Repository
-   PostgreSQL 扩展设计
