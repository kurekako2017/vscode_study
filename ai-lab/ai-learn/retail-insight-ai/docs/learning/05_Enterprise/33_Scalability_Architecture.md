# ERIP 企业源码架构手册

# Volume 05：Enterprise（企业架构）

# 第33章（Chapter 33）

# Scalability Architecture（可扩展架构）

> Design AI Systems That Can Grow

---

# 文档信息

| 项目     | 内容                               |
| -------- | ---------------------------------- |
| Volume   | 05                                 |
| Chapter  | 33                                 |
| 技术主题 | Scalability Architecture           |
| 难度     | ⭐⭐⭐⭐⭐                         |
| 推荐程度 | ⭐⭐⭐⭐⭐                         |
| 对应模块 | BackgroundTasks / Workflow / Queue |

---

# 学习目标

阅读本章后，你应该能够回答：

- 什么是 Scalability（可扩展性）？
- 为什么 AI Workflow 不能只依赖一台服务器？
- Redis、RabbitMQ、Worker 分别负责什么？
- ERIP 如何演进为企业 AI 平台？
- 什么是 Horizontal Scaling？

---

# 一、什么是 Scalability？

Scalability（可扩展性）表示：

> **当业务量增长时，系统仍然能够稳定运行，并且可以方便地扩展资源。**

例如：

最初每天只有：

```text
100 个 Task
```

后来增长到：

```text
10000 个 Task
```

如果系统几乎不用修改就能支持新的负载，

说明它具有良好的可扩展性。

---

# 二、为什么 AI Workflow 需要扩展？

AI Workflow 与普通 CRUD 最大的区别在于：

- 调用 LLM 耗时
- 生成报告耗时
- 检索知识库耗时
- 推理成本较高

如果：

```text
1000 个用户

↓

同时执行 AI Workflow
```

一台服务器很快就会成为瓶颈。

---

# 三、ERIP 当前架构（Current）

目前：

```text
Browser

↓

FastAPI

↓

BackgroundTasks

↓

AnalysisWorkflow

↓

Repository
```

对于：

学习、

PoC、

MVP。

已经足够。

但是：

不能支撑：

大规模企业。

---

# 四、Source Binding（源码绑定）

建议阅读：

```text
backend/app/services/task_service.py
```

重点：

```python
run_task()
```

继续：

```text
backend/app/workflow/graph.py
```

观察：

Workflow：

如何执行。

思考：

如果：

1000 个：

Workflow：

同时运行。

系统会怎样？

---

# 五、为什么不能一直使用 BackgroundTasks？

BackgroundTasks：

属于：

单进程。

例如：

```text
FastAPI

↓

BackgroundTasks

↓

Workflow
```

所有任务：

仍然：

运行在：

同一个：

应用进程。

因此：

适合：

轻量任务。

---

# 六、Worker 架构

企业通常采用：

```text
FastAPI

↓

Queue

↓

Worker

↓

Workflow
```

FastAPI：

负责：

接收请求。

Worker：

负责：

执行任务。

两者：

完全分离。

---

# 七、RabbitMQ 的作用

RabbitMQ：

负责：

保存任务。

例如：

```text
Create Task

↓

RabbitMQ

↓

Worker A

Worker B

Worker C
```

Worker：

谁空闲：

谁执行。

实现：

任务分发。

---

# 八、Redis 的作用

Redis：

主要负责：

```text
Cache

Session

Distributed Lock

Rate Limit
```

例如：

同一个 Prompt：

重复执行。

可以：

直接：

读取：

Redis。

减少：

LLM：

调用次数。

---

# 九、Horizontal Scaling（水平扩展）

假设：

一台服务器：

```text
Worker
```

性能不足。

企业不会：

升级：

CPU。

而是：

增加：

服务器。

例如：

```text
Worker1

Worker2

Worker3

Worker4
```

多个 Worker：

共同：

处理：

Workflow。

这就是：

Horizontal Scaling。

---

# 十、Load Balancer

多个 FastAPI：

需要：

统一入口。

例如：

```text
User

↓

Load Balancer

↓

FastAPI1

FastAPI2

FastAPI3
```

常见：

- Nginx
- HAProxy
- Cloud Load Balancer

---

# 十一、Architecture Thinking（架构思考）

为什么：

企业：

不用：

一台超级服务器？

因为：

硬件：

总有上限。

而：

增加：

Worker。

几乎：

无限扩展。

因此：

现代企业：

优先：

水平扩展。

---

# 十二、Retail Insight AI 企业演进路线

当前：

```text
FastAPI

↓

BackgroundTasks

↓

Workflow
```

企业版：

```text
API Gateway

↓

FastAPI

↓

RabbitMQ

↓

Worker Cluster

↓

Workflow

↓

Redis

↓

PostgreSQL
```

进一步：

支持：

高并发。

---

# 十三、Java / Spring 对照

| Retail Insight AI | Spring Boot          |
| ----------------- | -------------------- |
| BackgroundTasks   | @Async               |
| RabbitMQ          | Spring AMQP          |
| Redis             | Spring Data Redis    |
| Worker            | Worker Service       |
| Load Balancer     | Spring Cloud Gateway |

---

# 十四、VS Code 阅读路线

建议：

```text
TaskService

↓

BackgroundTasks

↓

Workflow

↓

Repository
```

思考：

哪些部分：

未来：

可以：

独立：

Worker。

---

# 十五、Learning Trace 对应

未来：

Learning Trace：

可能：

增加：

```text
Worker-01

↓

Workflow

↓

Completed
```

方便：

观察：

多个 Worker：

执行情况。

---

# 十六、企业扩展（Enterprise）

建议：

未来：

增加：

```text
RabbitMQ

↓

Redis

↓

Worker

↓

Auto Scaling

↓

Kubernetes
```

形成：

真正：

Enterprise AI Platform。

---

# 十七、面试回答（中文）

为什么企业 AI 平台需要 Worker？

AI Workflow 通常耗时较长，如果所有任务都运行在 Web 服务进程中，会影响接口响应速度。通过消息队列和 Worker，可以将任务异步分发到多个节点执行，实现高并发、高可用和水平扩展。

---

# 十八、面试回答（日语）

なぜ Worker が必要なのですか。

AI Workflow は時間がかかるため、Web サーバーで直接処理するとレスポンス性能が低下します。RabbitMQ と Worker を利用することで、タスクを非同期に処理し、高い拡張性と可用性を実現できます。

---

# 十九、日本 SES 常见追问

### Q：Redis 和 RabbitMQ 有什么区别？

Redis：

负责：

缓存、

Session、

Lock。

RabbitMQ：

负责：

消息、

任务分发。

两者：

职责不同。

通常：

一起使用。

---

# 二十、本章练习

完成下面练习：

① 思考：

BackgroundTasks：

有哪些限制？

↓

② 如果：

每天：

100 万个 Task。

应该：

如何改造？

↓

③ 画出：

FastAPI

↓

RabbitMQ

↓

Worker

↓

Workflow

↓

PostgreSQL

架构图。

---

# 二十一、本章核心记忆图

```text
                User
                  │
                  ▼
             Load Balancer
                  │
                  ▼
              FastAPI API
                  │
                  ▼
              RabbitMQ
          ┌──────┼──────┐
          ▼      ▼      ▼
      Worker1 Worker2 Worker3
          │      │      │
          └──────┼──────┘
                 ▼
          AnalysisWorkflow
                 │
                 ▼
        PostgreSQL / Redis
```

---

# 本章总结

一句话：

```text
Web Server

负责接收请求

↓

Queue

负责分发任务

↓

Worker

负责执行 AI

↓

Database

负责保存结果
```

Scalability Architecture 的核心思想是：

**通过消息队列、Worker、缓存和水平扩展，将 AI Workflow 从单机架构演进为企业级 AI 平台，满足高并发、高可用和持续扩展的业务需求。**

---

# 下一章

**Chapter 34：Cloud Native Architecture（云原生架构）**

学习：

- Docker
- Kubernetes
- ConfigMap
- Health Check
- OpenTelemetry
- 企业 AI 平台部署架构
