# Retail Insight AI Project Rules

> 放置位置：`ai-learn/retail-insight-ai/AGENTS.md`
>
> 本文件是 Retail Insight AI 项目的项目级规则。它继承 `ai-learn/AGENTS.md`，但只约束当前项目。

---

## 1. 项目定位

Retail Insight AI 是一个用于学习日本现场 AI Agent 项目开发的经营分析 Agent 项目。

项目目标：

```text
React
→ FastAPI
→ Task API
→ TaskService
→ Workflow
→ KPI Engine
→ Research Provider
→ Report Generator
→ SSE
→ React
```

它不是单纯 Demo，而是：

```text
可运行
+
可学习
+
可面试讲解
+
可逐步企业级升级
```

---

## 2. 当前阶段

当前默认阶段：

```text
Local Static Provider
+
InMemory / Local Repository
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
- 不接 PostgreSQL
- 不接 Redis
- 不接 RabbitMQ
- 不接真实外部业务系统

---

## 3. 允许的本地实现

允许存在：

- StaticResearchProvider
- InMemoryRepository
- LocalBusinessDataProvider
- Local / Static Provider

但不要把核心业务流程命名为 Mock / Fake / Dummy。

不允许：

- MockTaskService
- MockWorkflow
- MockKPI
- MockSSE
- MockReportGenerator

---

## 4. 强制中文教学注释

所有新增或修改的核心代码必须包含中文教学注释。

重点文件：

```text
backend/app/main.py
backend/app/api/
backend/app/services/
backend/app/workflow/
backend/app/kpi/
backend/app/agents/
backend/app/reports/
backend/app/repositories/
backend/app/events/
frontend/src/App.tsx
frontend/src/api.ts
```

必须说明：

- 文件职责
- 谁调用它
- 它调用谁
- 输入
- 输出
- 为什么这样设计
- 日本现场面试怎么讲

---

## 5. 企业级日志

新增或修改功能时，必须保持结构化日志。

日志字段至少包含：

- timestamp
- level
- service
- request_id
- task_id
- event
- status
- error_code
- duration_ms

禁止日志输出：

- API Key
- Secret
- 完整 Prompt
- 会员数据
- 内部资料正文

---

## 6. 文档同步

修改代码后，必须同步检查并更新：

```text
README.md
RUNBOOK_LOCAL.md
CODE_STUDY_GUIDE.md
VERIFY_CHECKLIST.md
```

如果新增功能没有更新学习文档，视为未完成。

---

## 7. 测试要求

修改后必须尽量执行：

```bash
./scripts/run_tests.sh
```

至少确认：

- Backend tests
- Frontend tests
- Frontend build
- Python compileall

如果 Docker 不可用，必须明确说明：

```text
当前环境没有 Docker CLI，未执行 Docker Build。
```

不要假装成功。

---

## 8. 新增功能输出要求

每次完成后必须输出：

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

---

## 9. 学习优先级

本项目当前优先事项：

1. 跑通全流程
2. 读懂代码
3. 修改小功能
4. 增加测试
5. 再考虑生产组件

不要过早接入 LLM、PostgreSQL、Redis、RabbitMQ。

## Permanent Backlog Rule

Every work session must start by reading:

1. AGENTS.md
2. docs/PROJECT_BACKLOG.md
3. TASK.md if it exists

Before coding, always check unfinished tasks and technical debt.

After completing work, always update docs/PROJECT_BACKLOG.md:

- mark completed tasks with [x]
- update current status
- add completion log
- add new discovered tasks if needed

Do not start coding directly without checking the backlog first.

# 项目永久任务清单规则

每次开始工作前必须执行：

1. 阅读 AGENTS.md
2. 阅读 docs/PROJECT_BACKLOG.md
3. 阅读 TASK.md（如果存在）

开始编码前必须：

- 查看未完成任务
- 查看当前阶段
- 查看技术债
- 选择最高优先级任务

禁止直接开始编码。

工作完成后必须更新：

`docs/PROJECT_BACKLOG.md`

包括：

- 已完成任务改为 [x]
- 更新任务状态
- 更新最后更新时间
- 增加完成记录
- 增加新发现任务
- 增加发现的问题

如果发现新的需求：

先加入 `PROJECT_BACKLOG.md`，再开始开发。

# retail-insight-ai 项目规则

本项目继承 AI-LAB 全局规则。

每次开发前必须阅读：

1. AGENTS.md
2. docs/PROJECT_BACKLOG.md
3. TASK.md

本项目当前重点：

Phase 2: Internal Knowledge Approval Agent

优先级顺序：

1. 项目结构确认
2. Docker 环境确认
3. .gitignore 敏感文件保护确认
4. Document Upload 流程确认
5. Chunk Pipeline
6. Embedding Pipeline
7. Vector Search
8. Approval Agent

本项目要求：

- 对初级学习者友好
- 重要代码必须添加易懂注释
- 复杂流程必须补充 Mermaid 流程图
- 每次完成任务后必须更新 Backlog
- 发现新任务必须先进入 Backlog

不要破坏已有 AGENTS.md 内容。
