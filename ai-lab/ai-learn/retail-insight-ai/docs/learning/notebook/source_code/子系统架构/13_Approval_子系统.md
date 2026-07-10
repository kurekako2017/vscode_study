![1783641074661](image/13_Approval_子系统/1783641074661.png)

# Retail Insight AI 企业源码架构手册

# Part 02：子系统架构

# 13_Approval_子系统

> Enterprise Subsystem Deep Dive

---

## 文档信息

---

  项目                                内容

---

  系列                                企业源码架构手册

  Part                                02 子系统架构

  文档                                13

  主题                                Approval 子系统（Approval Workflow）

对应源码                            backend/app/api/approvals.py、backend/app/services/、backend/app/workflow/
--------------------------------------------------------------------------------------------------------------

---

# 学习目标

阅读完本章后，你应该能够回答：

- Approval 子系统负责什么？
- 为什么企业 AI 系统需要审批？
- Approval Workflow 如何与 AI Workflow 协同？
- Human-in-the-Loop 是什么？
- 为什么审批功能独立成子系统？

---

# 一、Approval 子系统定位

Approval（审批）子系统负责管理**需要人工确认的业务流程**。

它的职责包括：

- 发起审批
- 查询审批状态
- 执行批准（Approve）
- 执行拒绝（Reject）
- 将审批结果反馈给 Workflow

一句话：

> **AI 可以提出建议，但最终决策可以交由人工完成。**

---

# 二、源码位置

```text
backend/
└── app/
    ├── api/
    │   └── approvals.py
    ├── services/
    ├── workflow/
    └── repositories/
```

- `approvals.py`：HTTP 接口入口
- Service：审批业务逻辑
- Repository：审批数据存储
- Workflow：根据审批结果继续执行

---

# 三、整体架构

```text
Browser
    │
Approval API
    │
Approval Service
    │
Repository
    │
Workflow
    │
Approved / Rejected
```

---

# 四、Approval 生命周期

```text
Create Approval
        │
Pending
        │
Approve / Reject
        │
Workflow Continue
        │
Completed
```

审批本身也是一个状态机。

---

# 五、Approval 与 AI Workflow

AI Workflow：

```text
Route
    │
Research
    │
Approval
    │
Report
```

如果需要人工确认：

Workflow 可以暂停等待审批结果。

审批完成后：

```text
Approval Result
        │
Workflow Resume
```

---

# 六、Human-in-the-Loop

Human-in-the-Loop（HITL）表示：

```text
AI
   │
生成建议
   │
Human Approval
   │
继续执行
```

优点：

- 降低 AI 风险
- 满足企业合规要求
- 保留人工最终决策权

---

# 七、Approval 与 Repository

Repository 保存：

- approval_id
- task_id
- status
- approver
- comment
- timestamp

Service 不直接操作数据库，而通过 Repository 完成数据访问。

---

# 八、Approval 与 EventPublisher

审批状态变化：

```text
Approve
    │
publish(approved)

Reject
    │
publish(rejected)
```

事件可以通过 SSE 实时推送给前端。

---

# 九、Approval 与 Learning Trace

Learning Trace 可以记录：

```text
Approval API
    │
Approval Service
    │
Repository
    │
Workflow Resume
```

帮助开发者定位审批流程。

---

# 十、企业为什么这样设计

如果 Workflow 直接完成所有操作：

```text
AI
   │
Final Result
```

企业无法审核关键决策。

增加 Approval 后：

```text
AI
   │
Pending
   │
Human Review
   │
Continue
```

更符合企业治理要求。

---

# 十一、未来扩展

Approval 子系统可以扩展：

- 多级审批
- 并行审批
- RBAC 权限控制
- Audit Log
- 邮件通知
- Slack / Teams 通知

---

# 十二、Java / Spring 对照

  Retail Insight AI   Spring Boot

---

  Approval API        REST Controller
  Approval Service    Service
  Repository          Repository / DAO
  Approval Workflow   BPM / Workflow Engine
  Human Approval      Human Task

---

# 十三、VS Code 阅读路线

```text
backend/app/api/approvals.py
        │
Approval Service
        │
Repository
        │
Workflow
```

建议结合 `workflow/graph.py` 阅读审批节点与业务流程。

---

# 十四、面试回答

> Approval 子系统负责企业级人工审批流程。AI Workflow
> 在需要人工确认时进入 Pending 状态，审批结果通过 Repository 保存，并由
> Workflow 根据 Approved 或 Rejected 继续执行，实现
> Human-in-the-Loop，满足企业对风险控制、审计和合规的要求。

---

# 本章总结

```text
Approval

=

企业 AI 的人工决策入口
```

它负责：

- 管理审批流程
- 暂停/恢复 Workflow
- 保存审批状态
- 推送审批事件
- 支持企业治理

---

# 下一章

**14_安全认证子系统.md**

将解析：

- Security API
- Authentication
- Authorization
- RBAC
- Audit Log
- 企业安全架构
