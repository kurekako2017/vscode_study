# README Learn

这个文档按学习顺序解释项目，不从代码文件开始，而从“你要掌握什么能力”开始。

## 学习目标

学完这个项目后，你应该能说明：

- 为什么经营 KPI 查询要用固定工作流，而不是完全自主 Agent。
- 为什么市场、竞品、社内资料调查适合 Agent 工具选择。
- FastAPI 后端如何把 REST、SSE、WebSocket 和后台任务组织起来。
- LangGraph 的 State、Node、Edge、Conditional Edge、Checkpoint 在代码里分别在哪里。
- 前端如何订阅后端事件流，并把 Agent 执行过程展示给业务用户。

## 推荐阅读顺序

1. [BASIC_DESIGN.md](./BASIC_DESIGN.md)
2. [BACKEND_FRAMEWORK.md](./docs/BACKEND_FRAMEWORK.md)
3. [RUN_EFFECT.md](./docs/RUN_EFFECT.md)
4. [TESTING.md](./TESTING.md)
5. [PRODUCTION_GAPS.md](./docs/PRODUCTION_GAPS.md)

## 代码阅读顺序

先看入口：

1. `server.py`
2. `retail_agent/api/app.py`
3. `retail_agent/interfaces/http/routers/tasks.py`
4. `retail_agent/application/task_service.py`

再看 Agent 编排：

1. `retail_agent/orchestration/orchestrator.py`
2. `retail_agent/workflows/business.py`
3. `retail_agent/research/agent.py`
4. `retail_agent/reporting/composer.py`

最后看基础设施：

1. `retail_agent/data/templates.py`
2. `retail_agent/data/warehouse.py`
3. `retail_agent/checkpoint/store.py`
4. `retail_agent/events/bus.py`
5. `frontend/src/main.tsx`

## 主流程图

```text
用户问题
  |
  v
React 前端 / CLI
  |
  v
FastAPI POST /api/tasks
  |
  v
TaskService 创建任务并启动后台执行
  |
  v
LangGraph StateGraph
  |
  +--> route node
  +--> data_workflow node
  +--> research_agent node
  +--> report node
  |
  v
SQLite task store + LangGraph SqliteSaver
  |
  v
SSE / WebSocket 推送事件
  |
  v
前端展示时间线和 Markdown 报告
```

## 节点和代码对照

| 流程节点 | 对应代码 | 学习重点 |
| --- | --- | --- |
| 创建任务 | `interfaces/http/routers/tasks.py` | Router 只做 HTTP 输入输出 |
| 后台执行 | `application/task_service.py` | UseCase 层负责状态、事件、异常 |
| 图编排 | `orchestration/orchestrator.py` | StateGraph、Node、Edge、Checkpoint |
| 固定问数 | `workflows/business.py` | 白名单 SQL、固定图、可审计数据 |
| 研究 Agent | `research/agent.py` | plan -> tools -> evidence |
| 报告生成 | `reporting/composer.py` | 数据证据 + 调查证据 + 风险 |
| 事件流 | `events/bus.py` | SSE/WebSocket 共享事件总线 |
| 前端展示 | `frontend/src/main.tsx` | EventSource、状态分区、报告展示 |

## 小练习

1. 新增一个 KPI：`客単価推移`。
2. 新增一个 research tool：`supplier_news_search`。
3. 在前端加一个“只看 failed/completed 事件”的过滤器。
4. 在 `PRODUCTION_GAPS.md` 中选择一个 `TODO`，写出你的实现计划。

