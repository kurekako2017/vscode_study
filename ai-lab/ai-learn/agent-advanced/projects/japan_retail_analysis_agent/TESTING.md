# Testing

## 测试目标

本项目的测试分三层：

1. 业务单元测试：验证路由、SQL guard、data/research 模式。
2. 应用层测试：验证 task repository、checkpoint、event 记录。
3. Smoke test：验证 FastAPI、SSE、WebSocket、前端 build。

## 测试用例表

这个项目不依赖真实 LLM 或外部搜索服务，所以左列统一写 `不适用（不调用真实模型 / 外部服务）`。
右列给出本地可直接执行的命令，并写明输入、命令和预期输出。

| 真实模型 / 真实服务命令 | 纯 Mock / 本地命令 |
| --- | --- |
| 不适用（不调用真实模型 / 外部服务） | **用例**：hybrid 主链路<br>**输入**：`売上と在庫を確認し、市場トレンドと競合を含めて報告`<br>**命令**：`cd /home/victorkure/workspace/vscode_study/ai-lab && python3 ai-learn/agent-advanced/projects/japan_retail_analysis_agent/main.py`<br>**预期输出**：`mode=hybrid`，报告同时包含 `固定 LangGraph 相当ワークフロー` 和 `自主 Agent`，且有销售、库存、市场、竞品四类信息。 |
| 不适用（不调用真实模型 / 外部服务） | **用例**：data 模式只跑固定经营问数<br>**输入**：`6月の売上と在庫リスクを確認` + `--mode data`<br>**命令**：`cd /home/victorkure/workspace/vscode_study/ai-lab && python3 ai-learn/agent-advanced/projects/japan_retail_analysis_agent/main.py "6月の売上と在庫リスクを確認" --mode data`<br>**预期输出**：`mode=data`，有 `data_blocks`，没有 `research_blocks`，报告里不应出现研究工具调用痕迹。 |
| 不适用（不调用真实模型 / 外部服务） | **用例**：research 模式只跑调查链路<br>**输入**：`市場トレンドと競合を調査して報告` + `--mode research`<br>**命令**：`cd /home/victorkure/workspace/vscode_study/ai-lab && python3 ai-learn/agent-advanced/projects/japan_retail_analysis_agent/main.py "市場トレンドと競合を調査して報告" --mode research`<br>**预期输出**：`mode=research`，有 `research_blocks`，没有 `data_blocks`，报告里不应出现固定 SQL 路径。 |
| 不适用（不调用真实模型 / 外部服务） | **用例**：SQL 白名单只允许 SELECT<br>**输入**：`DELETE FROM sales`<br>**命令**：`cd /home/victorkure/workspace/vscode_study/ai-lab/ai-learn/agent-advanced/projects/japan_retail_analysis_agent && python3 -m unittest tests.test_main.RetailAnalysisAgentTest.test_sql_guard_rejects_non_select`<br>**预期输出**：抛出 `ValueError`，错误信息包含 `SELECT`。 |
| 不适用（不调用真实模型 / 外部服务） | **用例**：`inventory_risk` 模板返回可审计结果<br>**输入**：模板名 `inventory_risk`<br>**命令**：`cd /home/victorkure/workspace/vscode_study/ai-lab/ai-learn/agent-advanced/projects/japan_retail_analysis_agent && python3 -m unittest tests.test_main.RetailAnalysisAgentTest.test_read_only_templates_return_verifiable_rows`<br>**预期输出**：返回 SQL 以 `select` 开头，且至少一行 `risk_level = "要補充"`。 |
| 不适用（不调用真实模型 / 外部服务） | **用例**：API health liveness<br>**输入**：无<br>**命令**：`cd /home/victorkure/workspace/vscode_study/ai-lab/ai-learn/agent-advanced/projects/japan_retail_analysis_agent && python3 -m unittest tests.test_api.RetailAnalysisApiTest.test_health_endpoint`<br>**预期输出**：返回 `{"status": "ok"}`。 |
| 不适用（不调用真实模型 / 外部服务） | **用例**：任务创建后写入 checkpoint 和事件<br>**输入**：`売上と在庫を確認し、市場トレンドと競合を含めて報告`<br>**命令**：`cd /home/victorkure/workspace/vscode_study/ai-lab/ai-learn/agent-advanced/projects/japan_retail_analysis_agent && python3 -m unittest tests.test_api.RetailAnalysisApiTest.test_task_runner_writes_checkpoint_and_events`<br>**预期输出**：task 状态为 `completed`，`report_markdown` 含 `日本小売 経営分析レポート`，事件包含 `workflow_completed`、`research_completed`、`completed`。 |
| 不适用（不调用真实模型 / 外部服务） | **用例**：后端 smoke test<br>**输入**：启动 `server.py` 后发起 `POST /api/tasks`<br>**命令**：`cd /home/victorkure/workspace/vscode_study/ai-lab/ai-learn/agent-advanced/projects/japan_retail_analysis_agent && python3 server.py`，再用 `curl` 创建任务<br>**预期输出**：`/api/health` 返回 200，任务最终 `status=completed`，SSE 事件顺序完整。 |
| 不适用（不调用真实模型 / 外部服务） | **用例**：前端 build<br>**输入**：无<br>**命令**：`cd /home/victorkure/workspace/vscode_study/ai-lab/ai-learn/agent-advanced/projects/japan_retail_analysis_agent/frontend && npm install && npm run build`<br>**预期输出**：TypeScript 和 Vite 构建成功，无编译错误。 |

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

| 用例 | 输入 | 预期输出 |
| --- | --- | --- |
| `test_hybrid_question_uses_data_and_research` | `売上と在庫を確認し、市場トレンドと競合を含めて報告` | `mode=hybrid`，`state.data_blocks` 与 `state.research_blocks` 都非空，报告同时包含固定工作流和自主 Agent 描述。 |
| `test_read_only_templates_return_verifiable_rows` | 模板名 `inventory_risk` | 返回只读 SQL 和至少一行库存风险数据，且存在 `要補充` 风险。 |
| `test_data_mode_does_not_run_research_agent` | `6月の売上と在庫リスクを確認` + `--mode data` | `mode=data`，只有数据块，没有研究块。 |
| `test_research_mode_does_not_run_fixed_sql` | `市場トレンドと競合を調査して報告` + `--mode research` | `mode=research`，只有研究块，没有数据块。 |
| `test_sql_guard_rejects_non_select` | `DELETE FROM sales` | 抛出 `ValueError`。 |
| `test_health_endpoint` | 无 | 返回 `status=ok`。 |
| `test_task_runner_writes_checkpoint_and_events` | `売上と在庫を確認し、市場トレンドと競合を含めて報告` | 任务与事件持久化成功，报告落库，事件序列包含 `workflow_completed`、`research_completed`、`completed`。 |

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

## 测试数据覆盖情况

当前样本数据已经覆盖本项目现有测试所需的主要场景，不需要再补一整套新数据集：

- `data/sales.csv` 覆盖月度销售、地区销售、品类销售。
- `data/inventory.csv` 覆盖库存风险，并且包含至少一条 `要補充` 记录。
- `data/research_notes.md` 覆盖市场趋势、竞品观察、社内确认规则。

如果后续要补异常场景，建议新增以下测试数据，而不是改动现有业务样本：

- 空销售集：验证“无数据”报告分支。
- 缺货加剧集：验证 `risk_level` 和风险提示更明显的分支。
- 旧日期研究笔记：验证报告里的“更新日期过期”提示。

## 未覆盖风险

详见 [Production Gaps](./docs/PRODUCTION_GAPS.md)。测试层还缺：

- NL2SQL golden set。
- 报告引用正确率评估。
- Prompt injection 测试。
- 负载测试。
- 多租户/权限测试。
