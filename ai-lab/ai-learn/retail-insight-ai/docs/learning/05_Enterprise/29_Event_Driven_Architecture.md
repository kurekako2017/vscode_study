
# Retail Insight AI 企业源码架构手册

# Volume 05：Enterprise（企业架构）

# Chapter 29

# Event Driven Architecture（事件驱动架构）

> Decouple Systems with Events

---

# 文档信息

| 项目     | 内容                             |
| -------- | -------------------------------- |
| Volume   | 05                               |
| Chapter  | 29                               |
| 技术主题 | Event Driven Architecture（EDA） |
| 难度     | ⭐⭐⭐⭐☆                       |
| 推荐程度 | ⭐⭐⭐⭐⭐                       |
| 对应源码 | backend/app/events/publisher.py  |

---

# 学习目标

阅读本章后，你应该能够回答：

- 什么是 Event Driven Architecture（EDA）？
- Retail Insight AI 为什么需要 EventPublisher？
- Publish / Subscribe 如何工作？
- Event Driven 与直接调用有什么区别？
- 企业项目为什么大量采用事件驱动架构？

---

# 一、什么是 Event Driven Architecture？

事件驱动架构（Event Driven Architecture，EDA）是一种以**事件（Event）**为核心的系统设计方式。

传统调用方式：

```text
Service

↓

Frontend
```

Service 必须知道 Frontend。

而事件驱动：

```text
Service

↓

Publish Event

↓

Subscriber
```

两者之间没有直接依赖。

---

# 二、为什么需要事件？

假设：

TaskService：

完成：

Workflow。

然后：

直接：

```python
frontend.update()
```

以后：

如果：

增加：

邮件通知、

Slack、

Teams、

Webhook、

Audit Log。

TaskService：

必须：

全部修改。

采用：

Event：

以后：

TaskService：

只负责：

```text
Publish Event
```

谁需要：

谁订阅。

---

# 三、Retail Insight AI 当前实现（Current）

当前项目：

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
```

Workflow：

不知道：

浏览器。

浏览器：

也不知道：

Workflow。

中间：

就是：

EventPublisher。

---

# 四、Source Binding（源码绑定）

建议阅读：

```text
backend/app/events/
```

重点：

```text
publisher.py
```

然后：

查看：

```text
backend/app/services/task_service.py
```

找到：

Workflow 完成后：

调用：

```text
EventPublisher.publish()
```

继续：

Frontend：

观察：

SSE：

如何接收事件。

---

# 五、Publish / Subscribe 模型

整个流程：

```text
Workflow

↓

Publish Event

↓

EventPublisher

↓

Subscriber

↓

Browser
```

以后：

增加：

```text
Mail

Slack

Webhook
```

Workflow：

完全不用修改。

---

# 六、Current vs Enterprise

当前：

```text
Workflow

↓

Publisher

↓

SSE
```

企业版：

```text
Workflow

↓

Event Bus

↓

RabbitMQ

↓

Kafka

↓

Redis Stream

↓

Subscribers
```

事件：

真正：

广播。

---

# 七、Architecture Thinking（架构思考）

为什么：

不用：

```python
frontend.update()
```

因为：

Workflow：

不应该：

知道：

谁使用数据。

它：

只负责：

产生事件。

这就是：

低耦合。

---

# 八、为什么企业喜欢 Event Driven？

原因：

① 解耦

Workflow：

不用：

知道：

调用者。

---

② 易扩展

以后：

新增：

消费者。

无需：

修改：

Workflow。

---

③ 高并发

多个：

Subscriber：

同时：

处理：

同一个：

Event。

---

④ 可维护

每个：

Subscriber：

职责：

单一。

---

# 九、Java / Spring 对照

| Retail Insight AI | Spring Boot               |
| ----------------- | ------------------------- |
| EventPublisher    | ApplicationEventPublisher |
| publish()         | publishEvent()            |
| Subscriber        | @EventListener            |
| SSE               | WebSocket / SSE           |

设计思想一致。

---

# 十、VS Code 阅读路线

建议：

```text
publisher.py

↓

TaskService

↓

AnalysisWorkflow

↓

Frontend SSE
```

观察：

Event：

在哪里：

产生。

在哪里：

消费。

---

# 十一、Learning Trace 对应

Learning Trace：

看到：

```text
Workflow

↓

Repository

↓

Publisher

↓

Completed
```

Publisher：

表示：

Workflow：

已经：

通知：

其它模块。

---

# 十二、企业扩展（Enterprise）

未来：

建议：

```text
RabbitMQ

Kafka

Redis Stream

Google Pub/Sub

AWS SNS

Azure Event Grid
```

Retail Insight AI：

可以：

无缝升级。

---

# 十三、面试回答（中文）

为什么采用 Event Driven Architecture？

事件驱动架构能够降低模块之间的耦合度。Workflow 不需要知道前端、通知系统或日志系统的实现，只需要发布事件。其它模块根据需要订阅事件即可，这种设计更容易扩展，也更符合企业级系统架构。

---

# 十四、面试回答（日语）

なぜ Event Driven Architecture を採用するのですか。

イベント駆動アーキテクチャでは、Workflow はイベントを発行するだけで、受信側を意識する必要がありません。これにより各モジュールの結合度が低くなり、拡張性・保守性が向上します。

---

# 十五、日本 SES 常见追问

Q：

为什么不用：

```python
service.call()
```

回答：

直接调用：

耦合。

Event：

解耦。

以后：

增加：

新的：

Subscriber。

无需：

修改：

Workflow。

---

# 十六、本章练习

请完成：

① 打开：

```text
backend/app/events/publisher.py
```

↓

② 阅读：

publish()

↓

③ 找到：

Workflow：

调用：

Publisher。

↓

④ 找到：

Frontend：

SSE：

接收：

Event。

---

# 十七、本章核心记忆图

```text
Workflow

↓

Publish Event

↓

EventPublisher

↓

SSE

↓

Browser
```

---

# 本章总结

一句话：

```text
Don't call.

Publish.
```

Event Driven Architecture 的核心思想是：

**模块之间不直接调用，而是通过事件进行通信。**

这种设计降低了系统耦合度，提高了扩展能力，也是现代企业系统、微服务和 AI 平台广泛采用的架构模式。

---

# 下一章

**Chapter 30：Workflow Pattern（工作流模式）**

学习：

- Workflow Engine
- State Machine
- LangGraph
- Node
- Edge
- AI Workflow Design
