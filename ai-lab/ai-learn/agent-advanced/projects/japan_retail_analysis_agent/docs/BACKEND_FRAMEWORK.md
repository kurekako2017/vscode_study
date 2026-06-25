# Backend Framework

这个后端按日本现场常见的 FastAPI 企业项目分层组织，不把路由、业务执行、持久化和 Agent 编排混在一个文件里。

## 分层结构

```text
retail_agent/
  core/
    config.py            # 环境变量、运行目录、端口、CORS
    logging.py           # 日志初始化
    errors.py            # 应用错误模型
  interfaces/http/
    routers/
      health.py          # health / metrics
      tasks.py           # task REST API
      streams.py         # SSE / WebSocket
    dependencies.py      # FastAPI Depends
    schemas.py           # HTTP schema re-export
  application/
    task_service.py      # task use case、后台执行、事件发布
  orchestration/
    orchestrator.py      # LangGraph StateGraph + SqliteSaver
  workflows/
    business.py          # 固定问数工作流
  research/
    agent.py             # research planner
    tools.py             # research tools
  data/
    templates.py         # KPI SQL templates
    sql_guard.py         # SELECT-only guard
    warehouse.py         # SQLite data warehouse
  infrastructure/
    repositories/
      task_repository.py # task/event/report repository
    observability/
      metrics.py         # in-memory metrics
  checkpoint/
    store.py             # SQLite task checkpoint store
  events/
    bus.py               # SSE/WebSocket event bus
  reporting/
    composer.py          # report composition
```

## 对应现场角色

| 层 | 日本现场常见叫法 | 责任 |
| --- | --- | --- |
| `interfaces/http` | API 層 / Controller 層 | HTTP 输入输出、状态码、SSE/WebSocket |
| `application` | Application Service / UseCase | 任务生命周期、事务边界、后台执行 |
| `orchestration` | Agent Orchestration | LangGraph 图、checkpoint、路由 |
| `workflows` | 業務ワークフロー | 固定经营指标和 SQL 模板 |
| `research` | Agent Tooling | 调查计划、工具选择、引用 |
| `infrastructure` | Repository / Adapter | SQLite、metrics、外部系统适配 |
| `core` | 共通基盤 | 配置、日志、错误 |

## 已实现的生产骨架能力

- REST API: `POST /api/tasks`、`GET /api/tasks/{task_id}`。
- Streaming: `GET /api/tasks/{task_id}/events`。
- WebSocket: `WS /ws/tasks/{task_id}`。
- Checkpoint: LangGraph `SqliteSaver` + task/report SQLite store。
- DI: FastAPI app state + dependency functions。
- Config: `.env.example` 对应 `core/config.py`。
- Observability: `/api/metrics` 和结构化事件。
- Deployment: `Dockerfile`、`docker-compose.yml`。

## 仍未生产化的部分

完整清单见 [Production Gaps](./PRODUCTION_GAPS.md)。摘要如下：

| 领域 | 状态 | 说明 |
| --- | --- | --- |
| 认证授权、RBAC、多租户 | `TODO` | 当前无用户、角色和 tenant 隔离 |
| OpenTelemetry / Prometheus / centralized logging | `TODO` | 当前只有基础日志和 in-memory metrics |
| SQL AST parser、PII masking、行列级权限 | `PARTIAL/TODO` | 当前只有 SELECT-only guard |
| 真实 DWH、企业搜索、SharePoint/Confluence 接入 | `PARTIAL` | 当前用 CSV/SQLite/Markdown 模拟 |
| LangGraph interrupt/resume 的人工审批 UI | `PARTIAL` | 当前只在报告中记录人工确认事项 |
| CI/CD、migration、正式 load test | `TODO` | 当前无流水线、迁移和压测 |
