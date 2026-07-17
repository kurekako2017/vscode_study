# ERIP 企业源码架构手册
> **V1.0 校正：** 正式 Repository = **PostgreSQL + pgvector**。文中 SQLite 仅作历史/对比教学，不是当前主库。InMemory = unittest only。


# Volume 05：Enterprise（企业架构）

# 第31章（Chapter 31）

# Security Architecture（企业安全架构）

> Secure AI Systems by Design

---

# 文档信息

| 项目     | 内容                      |
| -------- | ------------------------- |
| Volume   | 05                        |
| Chapter  | 31                        |
| 技术主题 | Security Architecture     |
| 难度     | ⭐⭐⭐⭐⭐                |
| 推荐程度 | ⭐⭐⭐⭐⭐                |
| 对应模块 | API / Workflow / Approval |

---

# 学习目标

阅读本章后，你应该能够回答：

- 企业系统为什么需要安全架构？
- Authentication 与 Authorization 有什么区别？
- 什么是 RBAC？
- AI Workflow 为什么需要 Approval？
- Audit Log 在 AI 系统中的作用是什么？

---

# 一、为什么安全架构如此重要？

传统 Web 系统主要保护：

- 用户信息
- 数据库
- 订单

AI 系统除了这些，还需要保护：

- Prompt
- LLM API Key
- AI Workflow
- 企业知识库
- AI 输出结果

因此：

AI 系统的安全要求通常高于普通 Web 系统。

---

# 二、安全架构总览

一个典型企业 AI 平台：

```text
                User
                  │
                  ▼
         Authentication
                  │
                  ▼
         Authorization
                  │
                  ▼
             RBAC
                  │
                  ▼
          AI Workflow
                  │
                  ▼
           Approval
                  │
                  ▼
           Audit Log
```

安全不是一个功能。

而是一整套体系。

---

# 三、Authentication（身份认证）

Authentication 用于回答：

> **你是谁？**

常见方式：

- 用户名密码
- OAuth2
- JWT
- SSO
- 企业 AD

例如：

```text
User

↓

Login

↓

JWT Token

↓

Access API
```

没有认证：

系统无法确认请求者身份。

---

# 四、Authorization（权限授权）

Authorization 回答：

> **你能做什么？**

例如：

普通员工：

```text
查看报告
```

经理：

```text
批准报告
```

管理员：

```text
删除任务
```

即使已经登录，

没有权限，

仍然不能执行对应操作。

---

# 五、RBAC（Role Based Access Control）

企业项目几乎都会使用 RBAC。

例如：

```text
Admin

Manager

Analyst

Viewer
```

不同角色拥有不同权限。

例如：

| Role    | 权限     |
| ------- | -------- |
| Admin   | 全部     |
| Manager | Approval |
| Analyst | 创建任务 |
| Viewer  | 查看报告 |

Retail Insight AI 企业版建议采用 RBAC。

---

# 六、Approval Workflow

AI 不应该直接决定最终结果。

例如：

```text
AI

↓

Generate Report

↓

Manager Approval

↓

Publish
```

增加人工审批后：

可以降低 AI 输出错误带来的风险。

因此：

Approval 是企业 AI 系统的重要组成部分。

---

# 七、Audit Log（审计日志）

Audit Log 用于记录：

- 谁执行了任务？
- 谁修改了 Prompt？
- 谁批准了报告？
- 谁删除了数据？

例如：

```text
2026-07-10

Victor

Approve Task

Task-001
```

Audit Log 不允许随意删除。

它是企业安全审计的重要依据。

---

# 八、ERIP 当前实现（Current）

当前项目已经具备：

```text
Approval 模块

↓

Approval API

↓

Approval Workflow（文档规划）
```

未来可以进一步加入：

- JWT
- RBAC
- Audit Log
- API Key 管理

形成完整安全体系。

---

# 九、Source Binding（源码绑定）

建议阅读：

```text
backend/app/api/

backend/app/services/

backend/app/workflow/

docs/APPROVAL_WORKFLOW.md
```

观察：

Approval 与 Workflow 如何协作。

---

# 十、Architecture Thinking（架构思考）

为什么企业 AI 不直接返回结果？

因为：

AI：

可能：

产生错误。

企业：

需要：

```text
AI

↓

Human Review

↓

Approval

↓

Publish
```

这样才能真正投入生产环境。

---

# 十一、AI 安全（AI Security）

相比传统系统，

AI 系统还需要考虑：

- Prompt Injection
- Prompt 泄露
- API Key 泄露
- 模型越权调用
- 数据污染
- 幻觉（Hallucination）

因此：

AI 安全不仅是系统安全，

也是模型安全。

---

# 十二、Java / Spring 对照

| Retail Insight AI | Spring Boot          |
| ----------------- | -------------------- |
| JWT               | Spring Security JWT  |
| RBAC              | Spring Security Role |
| Approval          | BPM Approval         |
| Audit Log         | Audit Trail          |

设计思想完全一致。

---

# 十三、VS Code 阅读路线

建议：

```text
Approval API

↓

Approval Service

↓

Workflow

↓

Repository
```

观察：

审批流程如何影响 Workflow。

---

# 十四、Learning Trace 对应

未来：

Approval：

可以增加：

```text
Workflow

↓

Waiting Approval

↓

Approved

↓

Continue
```

Learning Trace：

完整记录：

审批过程。

---

# 十五、企业扩展（Enterprise）

未来企业版建议加入：

```text
JWT

↓

RBAC

↓

Approval

↓

Audit Log

↓

OpenTelemetry

↓

Security Monitoring
```

形成完整 AI 安全体系。

---

# 十六、面试回答（中文）

为什么 AI 系统需要 Approval？

AI 模型可能产生错误或不符合企业规范的内容，因此很多企业会在 AI Workflow 中增加 Approval 节点，由人工确认后再发布结果。这样既能发挥 AI 的效率，也能保证业务安全。

---

# 十七、面试回答（日语）

AI システムで Approval が必要な理由は何ですか。

AI は誤った回答や不適切な内容を生成する可能性があります。そのため企業では AI の結果をそのまま利用せず、人による Approval を挟むことで品質と安全性を確保しています。

---

# 十八、日本 SES 常见追问

### Q：为什么 AI 系统需要 Audit Log？

回答：

AI 的决策过程需要可追溯。

企业必须知道：

- 谁发起任务
- 谁审批
- 谁修改 Prompt
- 谁查看结果

这样才能满足安全审计和合规要求。

---

# 十九、本章练习

请完成：

① 阅读：

```text
docs/APPROVAL_WORKFLOW.md
```

↓

② 思考：

Approval 应该插入 Workflow 哪个位置？

↓

③ 设计：

Admin、Manager、Viewer 三种角色的权限。

---

# 二十、本章核心记忆图

```text
User

↓

Authentication

↓

Authorization

↓

RBAC

↓

Workflow

↓

Approval

↓

Audit Log
```

---

# 本章总结

一句话：

```text
Authentication

确认身份

↓

Authorization

确认权限

↓

Approval

确认结果

↓

Audit Log

记录全过程
```

企业 AI 系统不仅要关注功能实现，更要保证安全、合规和可追溯性。通过认证、授权、审批和审计，可以建立一套完整的企业级 AI 安全架构。

---

# 下一章

**Chapter 32：Persistence Architecture（持久化架构）**

学习：

- Repository 与数据库
- SQLite、PostgreSQL、Redis 的职责
- Transaction
- Unit of Work
- 企业数据持久化设计
