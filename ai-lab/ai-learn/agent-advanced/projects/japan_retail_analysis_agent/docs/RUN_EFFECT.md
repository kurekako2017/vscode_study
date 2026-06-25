# Run Effect

## Hybrid 模式

```bash
python3 ai-learn/agent-advanced/projects/japan_retail_analysis_agent/main.py \
  "売上と在庫を確認し、市場トレンドと競合を含めて報告"
```

会看到：

- `mode=hybrid`
- 月次売上・粗利率：`fixed_line`
- 地域別売上：`fixed_bar`
- 在庫・欠品リスク：`fixed_table`
- 市場トレンド調査：`agent_report_section`
- 競合観察：`agent_report_section`
- 社内確認ルール：`agent_report_section`
- 監査ログ中包含固定 SQL 和 research tool 调用。

## Data 模式

```bash
python3 ai-learn/agent-advanced/projects/japan_retail_analysis_agent/main.py \
  "6月の売上と在庫リスクを確認" \
  --mode data
```

这个模式只展示电商问数类能力：

- 白名单 SQL 模板。
- 可验证 CSV/SQLite 数据结果。
- 固定图建议。
- 如果报告缺少市场/竞品信息，会给出风险提示。

## Research 模式

```bash
python3 ai-learn/agent-advanced/projects/japan_retail_analysis_agent/main.py \
  "市場トレンドと競合を調査して報告" \
  --mode research
```

这个模式只展示深度研搜类能力：

- Agent 先生成 `ResearchPlan`。
- 再调用市场、竞品、社内资料工具。
- 输出来源和 retrieved_at。
- 不生成经营数据库结果。

## 只看审计日志

```bash
python3 ai-learn/agent-advanced/projects/japan_retail_analysis_agent/main.py \
  "売上と在庫を確認し、市場トレンドと競合を含めて報告" \
  --show-audit-only
```

重点观察：

- `orchestrator.route`
- `fixed_workflow.sql`
- `research_agent.plan`
- `research_agent.tool`
- `report.compose`

这能说明运行路径是可追踪的，不是一个黑盒聊天机器人。

## 后端服务

```bash
cd ai-learn/agent-advanced/projects/japan_retail_analysis_agent
python3 server.py
```

核心接口：

- `GET /api/health`
- `POST /api/tasks`
- `GET /api/tasks`
- `GET /api/tasks/{task_id}`
- `GET /api/tasks/{task_id}/events`
- `WS /ws/tasks/{task_id}`

真实 smoke 期望：

```text
health=200
status=completed
events=8
report=True
```

运行后会生成两个 SQLite 文件：

- `runtime/checkpoints.sqlite3`：任务、事件、最终报告。
- `runtime/langgraph.sqlite3`：LangGraph `SqliteSaver` checkpoint。

SSE 会输出类似：

```text
event: started
event: route
event: workflow_started
event: workflow_completed
event: research_started
event: research_completed
event: report_started
event: completed
```

WebSocket 会收到同样的事件序列。

## 前端页面

```bash
cd ai-learn/agent-advanced/projects/japan_retail_analysis_agent/frontend
npm install
npm run dev
```

页面能力：

- 输入日文经营问题。
- 选择 `auto`、`data`、`research`、`hybrid`。
- 创建后端任务。
- 通过 SSE 显示执行时间线。
- 分区展示固定问数工作流和研究 Agent 事件。
- 展示最终 Markdown 报告。
