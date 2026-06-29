# VERIFY_CHECKLIST

先进入项目目录。表格中的 `<question_id>` 必须替换成实际 POST 响应中的 `data.question_id`；Approve 与 Reject 使用两个不同的 HIGH 问题。

```bash
cd ~/workspace/vscode_study/ai-lab/ai-learn/internal-knowledge-approval-agent
```

## 环境验证

| Checklist | 命令 | 预期结果 | 失败时查看文件 |
| --- | --- | --- | --- |
| [ ] check_env 通过 | `./scripts/check_env.sh` | 所有工具 OK，最后为 `Environment OK` | `scripts/check_env.sh` |
| [ ] Backend 启动 | `./scripts/start_backend.sh` | Uvicorn 监听 `127.0.0.1:8000` | `scripts/start_backend.sh`、`backend/requirements.txt` |
| [ ] Frontend 启动 | 新终端执行 `./scripts/start_frontend.sh` | Vite 显示 `127.0.0.1:5173` | `scripts/start_frontend.sh`、`frontend/package.json` |

## API验证

| Checklist | 命令 | 预期结果 | 失败时查看文件 |
| --- | --- | --- | --- |
| [ ] health OK | `curl -sS -i http://127.0.0.1:8000/health` | HTTP 200、正文 `status: ok`、响应头有 `X-Request-ID` | `backend/app/api/routes/health.py`、`backend/app/main.py` |
| [ ] LOW 问题 created | `curl -sS -X POST http://127.0.0.1:8000/api/questions -H 'Content-Type: application/json' -d '{"question":"休暇申請の手順を確認したい"}'` | HTTP 202 envelope，包含 `data.question_id` | `backend/app/api/routes/questions.py`、`backend/app/api/schemas.py` |
| [ ] LOW 问题 completed | `curl -sS http://127.0.0.1:8000/api/questions/<question_id>` | `risk_level: LOW`、`status: completed` | `backend/app/services/question_service.py`、`backend/app/workflow/graph.py` |
| [ ] HIGH 问题 approval_required | POST `個人情報の取扱手順を確認したい` 后执行 `curl -sS http://127.0.0.1:8000/api/questions/<question_id>` | `risk_level: HIGH`、`status: approval_required` | `backend/app/approval/policy.py`、`backend/app/workflow/nodes.py` |
| [ ] approve 后 completed | `curl -sS -X POST http://127.0.0.1:8000/api/approvals/<question_id>/approve`，再 GET Question | 审批为 approved，问题最终 completed | `backend/app/api/routes/approvals.py`、`backend/app/services/approval_service.py` |
| [ ] reject 后 rejected | 对另一个 HIGH ID 执行 `curl -sS -X POST http://127.0.0.1:8000/api/approvals/<question_id>/reject` | 问题 `status: rejected` | `backend/app/services/approval_service.py`、`backend/app/workflow/graph.py` |
| [ ] report 可读取 | `curl -sS http://127.0.0.1:8000/api/questions/<completed_question_id>/report` | `success: true`，包含 report 和 risk_level | `backend/app/api/routes/questions.py`、`backend/app/agents/answer_generator.py` |
| [ ] question not found 正确返回错误 | `curl -sS -i http://127.0.0.1:8000/api/questions/not-found` | HTTP 404、`RESOURCE_NOT_FOUND` | `backend/app/main.py`、`backend/app/services/question_service.py` |

## Frontend验证

| Checklist | 命令 | 预期结果 | 失败时查看文件 |
| --- | --- | --- | --- |
| [ ] 页面打开 | 浏览器访问 `http://127.0.0.1:5173` | 显示问题输入页 | `frontend/src/main.tsx`、`frontend/src/App.tsx` |
| [ ] 可以提交问题 | 输入问题并点击 `Workflow を開始` | 页面进入状态视图并显示 question ID | `frontend/src/App.tsx`、`frontend/src/api.ts` |
| [ ] 时间线显示 | 提交后打开 `SSE 状態` | 按 sequence 显示 received 等事件 | `frontend/src/App.tsx`、`frontend/src/api.ts` |
| [ ] LOW 自动完成 | 提交 `休暇申請の手順を確認したい` | 无审批步骤，显示最终报告 | `frontend/src/App.tsx`、Backend Workflow 文件 |
| [ ] HIGH 显示审批按钮 | 提交 `個人情報の取扱手順を確認したい` | 审批列表显示 Approve/Reject | `frontend/src/App.tsx` |
| [ ] Approve 成功 | 点击 HIGH 项目的 Approve | 最终显示报告 | `frontend/src/App.tsx`、`frontend/src/api.ts` |
| [ ] Reject 成功 | 新建 HIGH 问题并点击 Reject | 状态为 rejected，不生成报告 | `frontend/src/App.tsx`、`backend/app/workflow/graph.py` |
| [ ] 错误显示正常 | 停止 Backend 后从页面提交 | 页面 `role=alert` 区域显示连接/请求错误 | `frontend/src/App.tsx`、`frontend/src/api.ts` |

## 日志验证

| Checklist | 命令 | 预期结果 | 失败时查看文件 |
| --- | --- | --- | --- |
| [ ] request_id 存在 | 发起任意 curl 后查看 Backend 终端 | 每行 JSON 有非空 request_id 或应用级占位符 | `backend/app/main.py`、`backend/app/config/logging.py` |
| [ ] question_id 存在 | 创建问题后在终端搜索返回的 UUID | 问题相关日志包含同一 question_id | `backend/app/services/question_service.py` |
| [ ] event 存在 | 查看 Backend JSON 日志 | 包含 `question_created`、`question_status_transition` 等 event | `backend/app/config/logging.py`、`backend/app/services/question_service.py` |
| [ ] status 存在 | 完成 LOW/HIGH 流程后看日志 | 状态转换日志含 received/risk_checked/completed 等 status | `backend/app/services/question_service.py` |
| [ ] error_code 存在 | `curl -sS http://127.0.0.1:8000/api/questions/not-found` 后看日志 | 字段存在，错误日志为 `RESOURCE_NOT_FOUND`；正常日志可为 null | `backend/app/main.py`、`backend/app/config/logging.py` |

补充检查 `duration_ms`：完成任意 Workflow 后，`workflow_run_finished` 日志应包含数值；失败时查看 `backend/app/services/question_service.py`。

## 测试验证

| Checklist | 命令 | 预期结果 | 失败时查看文件 |
| --- | --- | --- | --- |
| [ ] Backend tests 通过 | `cd backend && .venv/bin/python -m unittest discover -s tests -v` | 所有 Backend test 为 OK | `backend/tests/test_api.py` |
| [ ] Frontend tests 通过 | `cd frontend && npm test` | Vitest 所有 test passed | `frontend/src/App.test.tsx`、`frontend/src/api.test.ts` |
| [ ] TypeScript build 通过 | `cd frontend && npm run build` | tsc 无错误且 Vite build 完成 | `frontend/tsconfig*.json`、`frontend/src/` |

也可以从项目根目录一次执行：

```bash
./scripts/run_tests.sh
```
