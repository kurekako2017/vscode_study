
# Retail Insight AI 企业源码架构手册

# Volume 03：Subsystem（子系统架构）

> Think like a Software Architect.

---

# 文档信息

| 项目     | 内容                   |
| -------- | ---------------------- |
| Volume   | 03                     |
| 名称     | Subsystem              |
| 学习重点 | 企业级系统架构         |
| 阅读方式 | 结合源码与架构一起学习 |
| 推荐程度 | ⭐⭐⭐⭐⭐             |

---

# 本册定位

Volume 03 不再关注某一个源码文件。

而是开始站在软件架构师（Software Architect）的角度思考：

> **为什么系统要拆成多个子系统？**

在企业项目中，一个系统通常不会只有一个 Service 或一个 Workflow，而是会被拆分成多个职责明确、相互协作的子系统。

Retail Insight AI 也是如此。

---

# 学习目标

完成本册后，你应该能够回答：

- Repository 为什么独立？
- Workflow 为什么独立？
- EventPublisher 为什么独立？
- Approval 为什么单独设计？
- Security 为什么不能写进每个 API？
- 整个系统如何由多个子系统协同工作？

---

# Retail Insight AI 子系统总览

```text
                    Browser
                        │
                        ▼
                 FastAPI Router
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
   Task Service     Documents API    Security API
        │
        ▼
  Task Repository
        │
        ▼
 Analysis Workflow
        │
        ▼
 Event Publisher
        │
        ▼
      SSE 推送
        │
        ▼
 React Dashboard
```

每一个方框，都对应一个独立的子系统。

---

# 本册目录

## Chapter 09：任务持久化子系统

学习内容：

- Repository Pattern
- Task Repository
- Task 生命周期
- Repository.save()

对应源码：

```text
backend/app/repositories/
```

推荐指数：

⭐⭐⭐⭐⭐

---

## Chapter 10：AI Workflow 子系统

学习内容：

- AnalysisWorkflow
- stream()
- Route
- KPI
- Research
- Report

对应源码：

```text
backend/app/workflow/
```

推荐指数：

⭐⭐⭐⭐⭐

---

## Chapter 11：事件通信子系统

学习内容：

- EventPublisher
- publish()
- Event Driven
- SSE

对应源码：

```text
backend/app/events/
```

推荐指数：

⭐⭐⭐⭐⭐

---

## Chapter 12：文档检索子系统

学习内容：

- Documents API
- Document Service
- Repository
- Internal Document Retrieval
- 企业级 RAG 扩展

对应源码：

```text
backend/app/api/documents.py
```

推荐指数：

⭐⭐⭐⭐⭐

---

## Chapter 13：Approval 子系统

学习内容：

- Approval Workflow
- Human-in-the-Loop
- Workflow Resume
- Pending

对应源码：

```text
backend/app/api/approvals.py
```

推荐指数：

⭐⭐⭐⭐☆

---

## Chapter 14：安全认证子系统

学习内容：

- Authentication
- Authorization
- RBAC
- Audit Log

对应源码：

```text
backend/app/api/security.py
```

推荐指数：

⭐⭐⭐⭐☆

---

## Chapter 15：系统启动子系统

学习内容：

- main.py
- FastAPI
- Uvicorn
- include_router()
- BackgroundTasks
- Application Lifecycle

对应源码：

```text
backend/app/main.py
```

推荐指数：

⭐⭐⭐⭐⭐

---

# 推荐阅读顺序

建议严格按照下面顺序阅读：

```text
09 Repository

↓

10 Workflow

↓

11 EventPublisher

↓

12 Documents

↓

13 Approval

↓

14 Security

↓

15 Application Startup
```

这样可以循序渐进地理解整个系统。

---

# 学习建议

阅读每一章时，建议同时打开：

- 对应 Markdown
- VS Code
- 对应源码文件
- Learning Trace 输出

四者结合学习。

不要只阅读 Markdown。

---

# 本册完成后

完成 Volume 03 后，你应该已经能够理解：

- 每个子系统负责什么
- 子系统之间如何协作
- 企业为什么采用这种分层架构

此时已经具备进入源码执行流程分析的基础。

---

# 下一册

继续阅读：

```text
Volume 04

Execution Flow（源码执行流程）
```

下一册将回答一个更重要的问题：

> **程序到底是怎么跑起来的？**

我们将从浏览器发送 HTTP 请求开始，一直到 AI Workflow 执行完成，再到 SSE 实时推送，全程跟踪整个程序的执行过程。

---

# 本册总结

Volume 03 的核心思想：

```text
一个源码文件

↓

组成一个子系统

↓

多个子系统

↓

组成整个企业系统
```

从这一册开始，我们学习的不再只是代码，而是企业级软件架构的设计思想。
