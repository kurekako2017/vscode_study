
# Retail Insight AI 企业源码架构手册

# Volume 04：Execution Flow（源码执行流程）

# Chapter 21

# SSE（Server-Sent Events）事件推送全过程

> Real-Time Event Streaming

---

# 文档信息

| 项目     | 内容                            |
| -------- | ------------------------------- |
| Volume   | 04                              |
| Chapter  | 21                              |
| 技术     | Server-Sent Events（SSE）       |
| 入口文件 | backend/app/events/publisher.py |
| Workflow | backend/app/workflow/graph.py   |
| 推荐程度 | ⭐⭐⭐⭐⭐                      |

---

# 学习目标

阅读本章后，你应该能够回答：

- SSE 是什么？
- 为什么 Dashboard 可以实时更新？
- EventPublisher 与 SSE 有什么关系？
- Workflow 如何通知前端？
- Browser 为什么不用不断刷新页面？

---

# 一、SSE 是什么？

SSE（Server-Sent Events）

是一种：

> **服务器主动向浏览器推送数据** 的技术。

与普通 HTTP 不同：

普通 HTTP：

```text
Browser

↓

Request

↓

Response
```

请求结束后：

连接立即关闭。

SSE：

```text
Browser

↓

建立连接

↓

服务器不断发送事件

↓

Browser 实时接收
```

连接会一直保持。

---

# 二、SSE 在 ERIP 中的作用

整个 AI Workflow：

可能执行：

几十秒。

如果：

浏览器：

每秒：

请求：

```http
GET /tasks
```

效率：

非常低。

因此：

项目采用：

SSE。

Workflow：

状态变化后：

立即：

推送：

浏览器。

---

# 三、执行流程 ⭐⭐⭐⭐⭐

```text
Browser

↓

建立 SSE 连接

↓

EventSource

↓

等待服务器事件

======================

Workflow

↓

Repository.save()

↓

EventPublisher.publish()

↓

SSE

↓

Browser

↓

React Dashboard 更新
```

整个过程：

Browser：

不会：

再次：

发送：

HTTP Request。

---

# 四、源码入口 ⭐⭐⭐⭐⭐

打开：

```text
backend/app/events/publisher.py
```

找到：

```python
publish()
```

这里：

就是：

所有事件：

统一出口。

Workflow：

不会：

直接：

操作：

SSE。

---

# 五、源码执行流程 ⭐⭐⭐⭐⭐

AI Workflow：

```text
AnalysisWorkflow.stream()

↓

Repository.save()

↓

EventPublisher.publish()
```

随后：

```text
publish()

↓

SSE

↓

Browser

↓

Dashboard
```

Workflow：

负责：

业务。

Publisher：

负责：

通知。

SSE：

负责：

发送。

Browser：

负责：

显示。

---

# 六、关键源码文件

| 文件            | 职责     |
| --------------- | -------- |
| graph.py        | Workflow |
| publisher.py    | 发布事件 |
| tasks.py        | 创建任务 |
| React Dashboard | 接收事件 |

---

# 七、关键函数

## publish()

作用：

统一：

广播事件。

例如：

```text
running

progress

completed

failed
```

都会：

经过：

publish()

---

## EventSource

浏览器：

建立：

SSE

连接。

等待：

服务器：

发送事件。

---

## Dashboard

收到：

事件。

更新：

页面。

无需：

刷新。

---

# 八、调用关系图 ⭐⭐⭐⭐⭐

```text
AnalysisWorkflow
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
Browser(EventSource)
        │
        ▼
React Dashboard
```

整个通知链：

只有一个方向：

```
Server

↓

Browser
```

Browser：

不能：

通过：

SSE：

发送数据。

---

# 九、Learning Trace 对应

Learning Trace：

例如：

```text
Repository.save()

↓

EventPublisher.publish()
```

说明：

Repository：

更新以后：

立即：

通知：

Publisher。

---

# 十、Console Log 对应

Console：

例如：

```text
Task Running

↓

Event Published

↓

Task Completed
```

Learning Trace：

告诉：

是谁：

调用：

publish()。

Console：

告诉：

发生了什么。

---

# 十一、VS Code 阅读路线 ⭐⭐⭐⭐⭐

建议：

```text
graph.py

↓

Repository.save()

↓

publisher.py

↓

publish()

↓

Frontend EventSource
```

观察：

每一次：

publish()

什么时候：

发生。

---

# 十二、当前源码实现（Current）

ERIP 当前已经实现：

✅ EventPublisher

✅ SSE

✅ Dashboard 实时更新

✅ Workflow 状态通知

已经形成：

完整：

实时事件推送流程。

---

# 十三、企业扩展（Enterprise）

未来：

建议：

升级：

```text
EventPublisher

↓

Redis Pub/Sub

↓

Kafka

↓

RabbitMQ

↓

WebSocket Gateway

↓

Browser
```

支持：

- 多实例
- 分布式
- 高并发

---

# 十四、为什么采用 SSE（Why）

如果：

每秒：

浏览器：

请求：

```http
GET /tasks
```

称为：

Polling。

缺点：

- 请求很多
- 浪费资源
- 延迟高

采用：

```text
Workflow

↓

EventPublisher

↓

SSE

↓

Browser
```

只有：

状态变化：

才：

发送事件。

效率：

更高。

---

# 十五、Java / Spring 对照

| Retail Insight AI | Spring Boot               |
| ----------------- | ------------------------- |
| SSE               | SseEmitter                |
| EventPublisher    | ApplicationEventPublisher |
| publish()         | publishEvent()            |
| EventSource       | EventSource API           |

---

# 十六、面试回答（中文）

面试官：

> 为什么使用 SSE？

回答：

> Retail Insight AI 使用 SSE 实现服务器主动推送。AI Workflow 在后台执行时，每完成一个阶段都会调用 EventPublisher.publish() 发布事件，再通过 SSE 实时推送到浏览器。相比轮询（Polling），SSE 可以减少大量 HTTP 请求，提高实时性和系统效率，非常适合 AI 长任务的状态通知。

---

# 十七、面试回答（日语）

面接官：

> なぜ SSE を採用したのですか。

回答例：

> Retail Insight AI では、AI Workflow の進行状況をリアルタイムにフロントエンドへ通知するために SSE（Server-Sent Events）を採用しています。Workflow が状態を更新するたびに EventPublisher がイベントを発行し、SSE を通じてブラウザへ送信します。Polling のように繰り返しリクエストを送る必要がないため、通信量を削減し、リアルタイム性を向上させています。

---

# 十八、日本SES常见追问

### 为什么不用 WebSocket？

回答：

Retail Insight AI：

主要需求：

只有：

```
Server

↓

Browser
```

单向：

推送。

因此：

SSE：

实现：

更简单。

维护：

成本：

更低。

如果：

以后：

Browser

也需要：

实时：

发送：

数据。

再考虑：

WebSocket。

---

# 十九、本章源码阅读任务 ⭐⭐⭐⭐⭐

完成下面练习：

① 打开：

```text
backend/app/events/publisher.py
```

↓

② 找到：

```text
publish()
```

↓

③ 打开：

```text
graph.py
```

↓

④ 找到：

Repository.save()

↓

⑤ 找到：

publish()

↓

⑥ 打开：

浏览器。

观察：

Dashboard：

什么时候：

自动刷新。

---

# 本章总结

一句话：

```text
AnalysisWorkflow

↓

Repository.save()

↓

EventPublisher.publish()

↓

SSE

↓

Browser

↓

Dashboard
```

SSE 是整个 ERIP 的实时通知机制。

Workflow 不直接操作前端，

而是通过 EventPublisher 与 SSE 解耦，实现企业级实时事件推送。

---

# 下一章

**Chapter 22：AI Workflow 执行全过程**

学习：

- AnalysisWorkflow.stream()
- Route
- KPI
- Research
- Report
- State 生命周期
- LangGraph 如何驱动整个 AI Workflow
