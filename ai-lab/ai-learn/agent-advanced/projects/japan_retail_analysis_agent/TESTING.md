# Testing

## 测试目标

本项目的测试分三层：

1. 业务单元测试：验证路由、SQL guard、data/research 模式。
2. 应用层测试：验证 task repository、checkpoint、event 记录。
3. Smoke test：验证 FastAPI、SSE、WebSocket、前端 build。

## 单元测试

运行：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab
python3 -m unittest discover ai-learn/agent-advanced/projects/japan_retail_analysis_agent/tests
```

当前测试文件：

| 文件 | 覆盖内容 |
| --- | --- |
| `tests/test_main.py` | hybrid/data/research 模式、SQL 模板、SQL guard |
| `tests/test_api.py` | health、task checkpoint、event 记录 |

## 重点测试用例

| 用例 | 目的 |
| --- | --- |
| `test_hybrid_question_uses_data_and_research` | hybrid 同时运行固定问数和研究 Agent |
| `test_data_mode_does_not_run_research_agent` | data 模式不应调用 research |
| `test_research_mode_does_not_run_fixed_sql` | research 模式不应调用固定 SQL |
| `test_sql_guard_rejects_non_select` | 非 SELECT SQL 必须拒绝 |
| `test_task_runner_writes_checkpoint_and_events` | 任务结果和事件必须可追踪 |

## 后端 Smoke Test

启动：

```bash
cd ai-learn/agent-advanced/projects/japan_retail_analysis_agent
python3 server.py
```

健康检查：

```bash
curl http://127.0.0.1:8020/api/health
```

创建任务：

```bash
curl -X POST http://127.0.0.1:8020/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"question":"売上と在庫を確認し、市場トレンドと競合を含めて報告","mode":"hybrid"}'
```

期望：

```text
status=completed
events=8
report contains 日本小売
```

## SSE 测试

```bash
curl -N http://127.0.0.1:8020/api/tasks/{task_id}/events
```

期望事件：

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

## WebSocket 测试

可以用 Python `websockets` 连接：

```text
ws://127.0.0.1:8020/ws/tasks/{task_id}
```

期望收到和 SSE 相同的事件序列。

## 前端测试

```bash
cd ai-learn/agent-advanced/projects/japan_retail_analysis_agent/frontend
npm install
npm run build
```

当前前端没有 E2E 自动化测试。生产化时建议补：

- Playwright：创建任务、等待 completed、检查报告展示。
- API mock：模拟 failed 事件和网络中断。
- Accessibility check：表单、按钮、事件区域可访问性。

## 未覆盖风险

详见 [Production Gaps](./docs/PRODUCTION_GAPS.md)。测试层还缺：

- NL2SQL golden set。
- 报告引用正确率评估。
- Prompt injection 测试。
- 负载测试。
- 多租户/权限测试。
