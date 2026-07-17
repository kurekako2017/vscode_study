# ERIP 企业源码架构手册

# Volume 04：Execution Flow（源码执行流程）

# 第19章（Chapter 19）

# Approval API 执行全过程

> Human-in-the-Loop Execution Flow

---

# 文档信息

| 项目       | 内容                                            |
| ---------- | ----------------------------------------------- |
| Volume     | 04                                              |
| Chapter    | 19                                              |
| API        | Approval API                                    |
| HTTP       | POST                                            |
| 入口文件   | backend/app/api/approvals.py                    |
| Service    | backend/app/services/approval_service.py        |
| Repository | backend/app/repositories/approval_repository.py |
| 推荐程度   | ⭐⭐⭐⭐⭐                                      |

---

# 学习目标

阅读本章后，你应该能够回答：

- Approval API 的执行流程是什么？
- Approve 与 Reject 的执行路径有什么区别？
- ApprovalService 做了什么？
- Repository 如何更新审批状态？
- Workflow 如何继续执行？
- EventPublisher 为什么会再次发送事件？

---

# 一、接口说明（API）

Approval API 用于处理人工审批。

典型流程：

```http
POST /api/approvals/{approval_id}/approve
```

或：

```http
POST /api/approvals/{approval_id}/reject
```

与 POST /api/tasks 不同，

这里：

不会创建 Task，

而是：

改变：

Approval Status。

---

# 二、HTTP Request 生命周期

Approve：

```text
Browser

↓

POST /api/approvals/{id}/approve

↓

FastAPI

↓

approvals.py

↓

ApprovalService

↓

ApprovalRepository

↓

Workflow Resume

↓

EventPublisher

↓

HTTP Response
```

Reject：

```text
Browser

↓

POST /reject

↓

ApprovalService

↓

ApprovalRepository

↓

Workflow Stop

↓

HTTP Response
```

---

# 三、源码入口 ⭐⭐⭐⭐⭐

打开：

```text
backend/app/api/approvals.py
```

找到：

```python
@router.post(...)
```

这里：

就是：

Approval API

入口。

随后：

进入：

```text
ApprovalService
```

处理：

Approve

Reject。

---

# 四、源码执行流程 ⭐⭐⭐⭐⭐

Approve：

```text
Browser

↓

Approval API

↓

ApprovalService.approve()

↓

ApprovalRepository.save()

↓

TaskRepository.save()

↓

Workflow Resume

↓

EventPublisher.publish()

↓

SSE

↓

Browser
```

Reject：

```text
Browser

↓

Approval API

↓

ApprovalService.reject()

↓

ApprovalRepository.save()

↓

TaskRepository.save()

↓

Workflow Stop

↓

EventPublisher.publish()

↓

SSE

↓

Browser
```

Approve

与

Reject

最大的区别：

是否恢复 Workflow。

---

# 五、关键源码文件

| 文件                   | 职责         |
| ---------------------- | ------------ |
| approvals.py           | HTTP Router  |
| approval_service.py    | 审批业务     |
| approval_repository.py | 保存审批状态 |
| task_repository.py     | 更新 Task    |
| publisher.py           | 发布事件     |

---

# 六、关键函数

## 方法：approve()

作用：

审批通过。

更新：

Approval Status。

恢复：

Workflow。

---

## 方法：reject()

作用：

审批拒绝。

停止：

Workflow。

更新：

Task Status。

---

## 方法：Repository.save()

作用：

保存：

Approval。

以及：

Task。

---

## 方法：publish()

作用：

通知：

前端。

审批状态：

发生变化。

---

# 七、调用关系图 ⭐⭐⭐⭐⭐

```text
Browser
    │
    ▼
Approval API
    │
    ▼
ApprovalService
    │
    ▼
ApprovalRepository
    │
    ▼
TaskRepository
    │
    ▼
Workflow Resume
    │
    ▼
EventPublisher
    │
    ▼
SSE
    │
    ▼
Browser
```

---

# 八、Learning Trace 对应

Request：

```text
============= Request =============

Approval API

↓

ApprovalService
```

如果：

Approve：

继续：

```text
Workflow Resume
```

Learning Trace：

继续：

Background。

---

# 九、Console Log 对应

Console：

例如：

```text
Approval Approved

↓

Workflow Resume

↓

Task Completed
```

Reject：

则：

```text
Approval Rejected

↓

Task Failed
```

---

# 十、VS Code 阅读路线 ⭐⭐⭐⭐⭐

建议：

```text
approvals.py

↓

ApprovalService

↓

ApprovalRepository

↓

TaskRepository

↓

publisher.py
```

观察：

Workflow：

什么时候：

恢复。

---

# 十一、当前源码实现（Current）

ERIP 当前：

已经实现：

- Approval API
- Approval Service
- Approval Repository
- Approval Status 更新
- Workflow Resume
- EventPublisher 通知

形成：

完整：

Approval Flow。

---

# 十二、企业扩展（Enterprise）

企业：

通常：

增加：

```text
Email

↓

Slack

↓

Teams

↓

Reminder

↓

Escalation

↓

Multi Approval
```

Approval

可以：

支持：

多人审批。

---

# 十三、为什么这样设计（Why）

Approval：

负责：

人工决定。

Workflow：

负责：

AI。

Repository：

负责：

保存状态。

EventPublisher：

负责：

通知。

每个模块：

职责：

完全独立。

---

# 十四、Java / Spring 对照

| Retail Insight AI | Spring Boot     |
| ----------------- | --------------- |
| Approval API      | Controller      |
| ApprovalService   | Service         |
| Repository        | JpaRepository   |
| Workflow Resume   | Workflow Engine |

---

# 十五、面试回答（中文）

面试官：

> Approval API 的执行流程是什么？

回答：

> 浏览器调用 Approval API 后，请求首先进入 approvals.py，再由 ApprovalService 处理审批逻辑。审批状态保存到 ApprovalRepository，同时更新关联 Task。当审批通过时恢复 Workflow 执行，并通过 EventPublisher 发布事件，由 SSE 实时通知前端；如果审批拒绝，则终止 Workflow，并更新任务状态。

---

# 十六、面试回答（日语）

面接官：

> Approval API の実行フローを説明してください。

回答例：

> Approval API は approvals.py を入口として、ApprovalService が承認・却下の処理を実行します。承認状態は ApprovalRepository に保存され、関連する Task も更新されます。Approve の場合は Workflow を再開し、EventPublisher を通じて SSE によりフロントエンドへ通知します。Reject の場合は Workflow を終了し、タスク状態を更新します。

---

# 十七、日本SES常见追问

### 为什么 Approval 不直接操作前端？

回答：

Approval：

只负责：

业务。

通知：

统一：

交给：

EventPublisher。

保持：

模块解耦。

---

# 十八、本章源码阅读任务 ⭐⭐⭐⭐⭐

完成下面练习：

① 打开：

```text
backend/app/api/approvals.py
```

↓

② 阅读：

```text
ApprovalService
```

↓

③ 阅读：

```text
ApprovalRepository
```

↓

④ 找到：

```text
Workflow Resume
```

↓

⑤ 找到：

```text
EventPublisher.publish()
```

理解：

审批完成以后，

程序：

如何继续运行。

---

# 本章总结

一句话：

```text
Approval API

↓

ApprovalService

↓

ApprovalRepository

↓

TaskRepository

↓

Workflow Resume

↓

EventPublisher

↓

SSE
```

Approval API 是 AI Workflow 与人工审批之间的桥梁，也是企业级 Human-in-the-Loop 架构的重要组成部分。

---

# 下一章

**Chapter 20：Security API**

学习：

- Authentication
- Authorization
- RBAC
- JWT
- Audit Log
- Security Flow
