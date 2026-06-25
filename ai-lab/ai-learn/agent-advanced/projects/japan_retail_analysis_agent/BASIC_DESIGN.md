# Basic Design

## 1. 背景

日本小売现场常见需求不是单纯聊天，而是把经营数据、市场调查、竞争情报和社内报告合成一个可审计的经营分析流程。

本项目把两个方向组合：

- 电商问数：结构化经营数据、固定 KPI、白名单 SQL、固定图。
- 深度研搜：市场/竞品/社内资料调查、工具选择、来源引用、报告交付。

## 2. 系统目标

| 目标 | 说明 |
| --- | --- |
| 可运行 | 后端、前端、CLI 都能运行 |
| 可学习 | 代码分层清楚，关键路径有注释 |
| 可解释 | 报告保留来源、风险、人工确认和审计 |
| 可扩展 | 可以替换真实 DWH、企业搜索、认证授权 |
| 可面试 | 能讲清固定图和自主 Agent 的边界 |

## 3. 功能范围

### 已实现

- 创建分析任务。
- 查询任务详情。
- SSE/WebSocket 实时事件。
- data/research/hybrid 三种执行模式。
- LangGraph StateGraph 编排。
- LangGraph SqliteSaver checkpoint。
- SQLite task/event/report 持久化。
- React 前端运行控制台。

### 未实现

详见 [Production Gaps](./docs/PRODUCTION_GAPS.md)。

## 4. 业务流程

```text
问题输入
  |
  v
模式判断：data / research / hybrid
  |
  +--> data: 売上・粗利・在庫 KPI 查询
  |
  +--> research: 市場・競合・社内資料调查
  |
  v
EvidenceBlock 标准化
  |
  v
ReportComposer 生成日文报告
  |
  v
TaskRepository 保存结果
```

## 5. LangGraph 设计

| Node | 输入 State | 输出 State | 为什么需要 |
| --- | --- | --- | --- |
| `route` | `AnalysisState.question/mode` | 原样返回并发事件 | 明确任务路径，方便审计 |
| `data_workflow` | `AnalysisState` | 追加 `data_blocks` | 可验证经营数据必须受控 |
| `research_agent` | `AnalysisState` | 追加 `research_blocks` | 调查来源随问题变化 |
| `report` | `AnalysisState` | 写入 `report_markdown` | 统一交付经营报告 |

## 6. API 设计

| API | 方法 | 用途 |
| --- | --- | --- |
| `/api/health` | GET | 健康检查 |
| `/api/metrics` | GET | 教学用内存指标 |
| `/api/tasks` | POST | 创建分析任务 |
| `/api/tasks` | GET | 查询最近任务 |
| `/api/tasks/{task_id}` | GET | 查询任务详情和报告 |
| `/api/tasks/{task_id}/events` | GET | SSE 事件流 |
| `/ws/tasks/{task_id}` | WS | WebSocket 事件流 |

## 7. 数据设计

| 数据 | 文件/表 | 说明 |
| --- | --- | --- |
| 销售数据 | `data/sales.csv` | 売上、粗利、客数、商品 |
| 库存数据 | `data/inventory.csv` | stock、daily sales、reorder point |
| 调查资料 | `data/research_notes.md` | 市场、竞品、社内规则 |
| task store | `runtime/checkpoints.sqlite3` | task、event、report |
| graph checkpoint | `runtime/langgraph.sqlite3` | LangGraph checkpoint |

## 8. 前端设计

前端不是聊天 UI，而是任务控制台：

- 输入问题。
- 选择 mode。
- 创建任务。
- 订阅 SSE。
- 分区展示固定问数事件和 research Agent 事件。
- 展示最终 Markdown 报告。

## 9. 生产扩展设计

| 当前实现 | 生产替换 |
| --- | --- |
| CSV + SQLite | DWH / Data Mart / BI semantic layer |
| Markdown research notes | 企业搜索、SharePoint、Confluence |
| 规则 planner | LLM tool calling + permission policy |
| In-process EventBus | Redis Pub/Sub / Kafka / NATS |
| asyncio background task | Durable queue |
| in-memory metrics | Prometheus/OpenTelemetry |

