# Function Overview

这个文档按“用户能做什么”介绍功能，再对应到代码。

## 1. 创建经营分析任务

用户在前端或 API 输入日文问题，例如：

```text
売上と在庫を確認し、市場トレンドと競合を含めて報告
```

对应代码：

- 前端：`frontend/src/main.tsx`
- API：`interfaces/http/routers/tasks.py`
- 应用服务：`application/task_service.py`

## 2. 选择执行模式

| mode | 功能 |
| --- | --- |
| `auto` | 后端根据问题自动判断 |
| `data` | 只运行固定经营数据查询 |
| `research` | 只运行研究 Agent |
| `hybrid` | 同时运行两者 |

对应代码：

- `orchestration/orchestrator.py`

## 3. 固定经营问数

功能：

- 月次売上・粗利率。
- 地域別売上。
- 在庫・欠品リスク。
- カテゴリ別売上。

特点：

- 只使用白名单 SQL 模板。
- 每个结果指定固定图类型。
- 结果可追踪到 CSV/SQLite 数据来源。

对应代码：

- `data/templates.py`
- `data/sql_guard.py`
- `data/warehouse.py`
- `workflows/business.py`

## 4. 深度研搜式研究 Agent

功能：

- 市場トレンド調査。
- 競合観察。
- 社内確認ルール。

特点：

- 先生成 ResearchPlan。
- 再按问题选择工具。
- 每个工具输出 EvidenceBlock 和 Source。

对应代码：

- `research/agent.py`
- `research/tools.py`

## 5. 实时执行过程展示

后端会发布事件：

```text
started
route
workflow_started
workflow_completed
research_started
research_completed
report_started
completed
```

前端通过 SSE 接收事件，并显示：

- 固定问数工作流面板。
- Research Agent 面板。
- Execution Timeline。
- Markdown Report。

对应代码：

- `events/bus.py`
- `interfaces/http/routers/streams.py`
- `frontend/src/main.tsx`

## 6. 报告输出

最终报告包含：

- 问题。
- 执行模式。
- 固定图/Agent 的使用判断。
- 结构化数据结果。
- 调查结果。
- 风险和确认事项。
- 人工确认记录。
- 监査ログ。

对应代码：

- `reporting/composer.py`

## 7. Checkpoint 和审计

两类持久化：

| 类型 | 文件 | 用途 |
| --- | --- | --- |
| Task store | `runtime/checkpoints.sqlite3` | task、event、report |
| LangGraph checkpoint | `runtime/langgraph.sqlite3` | graph node checkpoint |

对应代码：

- `checkpoint/store.py`
- `orchestration/orchestrator.py`
- `infrastructure/repositories/task_repository.py`

## 8. Metrics

教学版 `/api/metrics` 返回：

- tasks_created
- tasks_completed
- tasks_failed
- events_published
- event_counts

对应代码：

- `infrastructure/observability/metrics.py`
- `interfaces/http/routers/health.py`

