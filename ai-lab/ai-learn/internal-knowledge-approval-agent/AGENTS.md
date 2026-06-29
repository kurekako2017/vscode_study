# Internal Knowledge Approval Agent Rules

> 放置位置：`ai-learn/internal-knowledge-approval-agent/AGENTS.md`
>
> 本文件是 Internal Knowledge Approval Agent 项目的项目级规则。它继承 `ai-learn/AGENTS.md`。

---

## 1. 项目定位

项目名称：

```text
Internal Knowledge Approval Agent
社内文書検索・承認ワークフローAIエージェント
```

项目目标：

```text
社内文書 RAG
+
リスク判定
+
承認 Workflow
+
SSE
+
React UI
+
FastAPI Backend
```

这是面向日本现场 AI Agent 案件的学习项目，不是普通聊天机器人。

---

## 2. 核心业务流程

```text
员工提交社内问题
│
▼
FastAPI 接收请求
│
▼
QuestionService 创建问题
│
▼
Workflow 执行
│
├── Retriever 检索社内文档
│
├── RiskClassifier 判断风险
│
├── LOW  -> AnswerGenerator -> completed
│
└── HIGH -> approval_required
              │
              ├── approve -> AnswerGenerator -> completed
              └── reject  -> rejected
│
▼
SSE 推送状态
│
▼
React 显示时间线和结果
```

---

## 3. 当前阶段

当前阶段：

```text
V1 Local Static Document Provider
+
SQLite / Local Repository
+
FastAPI
+
React
+
SSE
```

当前禁止：

- 不接真实 OpenAI
- 不接真实 LLM
- 不接 LangSmith
- 不接 PostgreSQL
- 不接 Redis
- 不接 RabbitMQ
- 不扩写架构文档
- 不修改其它项目

---

## 4. 开发路线

```text
V1 Static Documents
↓
V2 SQLite 稳定化
↓
V3 Embedding
↓
V4 Rerank
↓
V5 LLM Provider
↓
V6 PostgreSQL
↓
V7 Redis / Queue
↓
V8 OpenTelemetry / Audit / RBAC
```

每次升级必须先保证当前版本能运行、能测试、能学习。

---

## 5. 强制中文教学注释

所有 Backend 核心代码必须有中文教学注释。

重点文件：

```text
backend/app/main.py
backend/app/api/routes.py
backend/app/services/question_service.py
backend/app/services/approval_service.py
backend/app/workflow/graph.py
backend/app/workflow/state.py
backend/app/workflow/nodes.py
backend/app/rag/retriever.py
backend/app/rag/documents.py
backend/app/approval/policy.py
backend/app/agents/answer_generator.py
backend/app/repositories/
backend/app/events/
backend/app/observability/
```

每个文件必须说明：

- 文件职责
- 谁调用它
- 它调用谁
- 输入
- 输出
- 初学者重点看哪里
- 日本现场面试怎么讲
- 企业级版本怎么替换

---

## 6. Workflow Node 注释规则

每个 Workflow Node 必须说明：

- Node 名称
- 输入 State
- 输出 State
- 状态变化
- 为什么需要
- 失败时怎么办
- 企业级替换方案

示例：

```text
RiskClassifier

输入：
question, retrieved_documents

输出：
risk_level

状态变化：
retrieving -> risk_checked

企业级替换：
规则表 / Policy Engine / LLM Classifier
```

---

## 7. Frontend 注释规则

Frontend 必须包含中文教学注释。

重点文件：

```text
frontend/src/App.tsx
frontend/src/api.ts
frontend/src/main.tsx
```

必须说明：

- 页面职责
- API 调用流程
- SSE 订阅流程
- Approve / Reject 按钮逻辑
- 状态如何展示
- 错误如何展示

---

## 8. 日志规则

结构化日志必须包含：

- timestamp
- level
- service
- request_id
- question_id
- event
- status
- error_code
- duration_ms

禁止记录：

- API Key
- Secret
- 文档全文
- 个人敏感信息

日志必须能回答：

```text
这个问题什么时候进入审批？
谁审批了？
什么时候完成？
哪里失败了？
```

---

## 9. 文档同步规则

修改代码后必须同步检查：

```text
README.md
RUNBOOK_LOCAL.md
CODE_STUDY_GUIDE.md
VERIFY_CHECKLIST.md
STUDY_PLAN_DAY1_DAY5.md
```

如果新增 API、状态、事件、字段，却没有更新文档，视为未完成。

---

## 10. 测试要求

修改后必须执行或说明无法执行的原因：

```bash
./scripts/check_env.sh
./scripts/run_tests.sh
```

至少覆盖：

- health
- LOW completed
- HIGH approval_required
- approve completed
- reject rejected
- report
- not found
- Frontend render
- API client
- error display

---

## 11. 输出要求

完成后必须输出：

```text
修改文件:
新增文件:
未修改目录:
启动命令:
测试结果:
当前实现边界:
学习顺序:
下一步建议:
```

如果是代码修改，还必须输出：

```text
中文注释覆盖情况:
日志覆盖情况:
文档同步情况:
```

---

## 12. 当前最优先事项

当前阶段优先级：

1. 本地运行验证
2. 读懂代码
3. 完善中文教学注释
4. 小功能练习
5. 测试补充
6. 再考虑 Embedding / LLM / PostgreSQL

不要在还没读懂项目之前继续堆功能。
