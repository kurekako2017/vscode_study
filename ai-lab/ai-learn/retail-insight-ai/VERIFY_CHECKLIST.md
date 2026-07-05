# 启动完成检查清单

按下面顺序逐项验证。每一项都要能明确说出“怎么确认成功、失败长什么样、失败后先看哪个文档”。

## 失败时先看哪个文档

| 问题 | 先看哪个文档 | 为什么先看它 |
| --- | --- | --- |
| 后端启动失败 | `RUNBOOK_LOCAL.md`、`backend/app/main.py` | 先看启动入口和终端日志，最快定位导入和端口问题 |
| 前端启动失败 | `RUNBOOK_LOCAL.md`、`frontend/src/App.tsx` | 先看前端启动命令和页面入口 |
| Swagger 打不开 | `RUNBOOK_LOCAL.md`、`docs/LEARNING_API_WALKTHROUGH.md` | 先确认后端是否真的跑起来，再确认接口是否注册 |
| 主链路 API 失败 | `docs/LEARNING_API_WALKTHROUGH.md`、`docs/ARCHITECTURE.md` | 先看接口学习顺序和分层边界 |
| 测试失败 | `docs/TEST_CASES.md`、`README.md` | 先看测试对应什么程序流，再回到入口文档 |
| 日志/审计异常 | `docs/ERROR_CATALOG.md`、`docs/MASTER_PROMPT.md` | 先看错误码和日志规则，避免把现象当原因 |

## 1. 后端是否启动成功

- 执行命令：

```bash
./scripts/start_backend.sh
```

- 预想结果：终端出现 `Uvicorn running on http://127.0.0.1:8000`，并且进程持续运行。
- 失败现象：`ModuleNotFoundError`、`Address already in use`、`ImportError`、`SyntaxError`。
- 应该查看：`RUNBOOK_LOCAL.md`、`backend/app/main.py`。

## 2. 前端是否启动成功

- 执行命令：

```bash
./scripts/start_frontend.sh
```

- 预想结果：终端出现 `Local: http://127.0.0.1:5173/`，浏览器能打开前端页面。
- 失败现象：5173 被占用、npm 依赖未安装、Vite 报错。
- 应该查看：`RUNBOOK_LOCAL.md`、`frontend/src/App.tsx`。

## 3. health 是否可访问

- 执行命令：

```bash
curl -sS http://127.0.0.1:8000/health
```

- 预想结果：返回 JSON，包含 `status=ok`、`service=retail-insight-ai`、`provider=static` 和非空 `request_id`。
- 失败现象：`Connection refused`、404、空响应。
- 应该查看：`RUNBOOK_LOCAL.md`、`docs/LEARNING_API_WALKTHROUGH.md`。

## 4. 任务是否创建成功

- 执行命令：

```bash
CREATE_RESPONSE=$(curl -sS -X POST http://127.0.0.1:8000/api/tasks -H 'Content-Type: application/json' -H 'X-Request-ID: verify-local-001' -d '{"question":"売上と在庫の状況を分析してください","mode":"hybrid"}')
printf '%s\n' "$CREATE_RESPONSE"
TASK_ID=$(printf '%s' "$CREATE_RESPONSE" | python3 -c 'import json,sys; print(json.load(sys.stdin)["data"]["task_id"])')
printf 'TASK_ID=%s\n' "$TASK_ID"
```

- 预想结果：响应包含 `success=true`、`status=queued`，并打印出一个 UUID 格式的 `TASK_ID`。
- 失败现象：HTTP 422、`VALIDATION_ERROR`、JSON 解析失败。
- 应该查看：`docs/LEARNING_API_WALKTHROUGH.md`、`backend/app/api/tasks.py`。

## 5. SSE 是否能收到状态事件

- 执行命令：

```bash
curl -sS -N "http://127.0.0.1:8000/api/tasks/$TASK_ID/events"
```

- 预想结果：至少能看到一条 `event: status`，任务结束时能看到 `event: done` 或 `event: error`。
- 失败现象：连接立即断开、没有事件、`404`。
- 应该查看：`docs/LEARNING_API_WALKTHROUGH.md`、`backend/app/events/sse.py`。

## 6. 报告是否能读取

- 执行命令：

```bash
curl -sS "http://127.0.0.1:8000/api/tasks/$TASK_ID/report"
```

- 预想结果：返回 `success=true`、`status=generated`，`markdown` 中有报告标题和正文。
- 失败现象：`REPORT_NOT_FOUND`。
- 应该查看：`docs/LEARNING_API_WALKTHROUGH.md`、`backend/app/services/task_service.py`。

## 7. 错误输入是否能正确返回

- 执行命令：

```bash
curl -sS -X POST http://127.0.0.1:8000/api/tasks -H 'Content-Type: application/json' -d '{"question":"","mode":"hybrid"}'
```

- 预想结果：返回 `success=false`，并带有 `code=VALIDATION_ERROR`。
- 失败现象：请求被错误接受，或者返回格式不符合统一 envelope。
- 应该查看：`docs/ERROR_CATALOG.md`、`backend/app/api/tasks.py`。

## 8. 日志是否包含 request_id / task_id

- 执行命令：

```bash
curl -sS -X POST http://127.0.0.1:8000/api/tasks -H 'Content-Type: application/json' -H 'X-Request-ID: verify-log-001' -d '{"question":"ログ項目を確認してください","mode":"kpi"}'
```

- 预想结果：后端 JSON 日志能找到 `request_id=verify-log-001`，并且任务相关日志带有同一个 `task_id`。
- 失败现象：日志没有结构化字段，或者字段值为空。
- 应该查看：`docs/MASTER_PROMPT.md`、`backend/app/main.py`、`docs/ARCHITECTURE.md`。

## 9. Security read model 是否正常

- 执行命令：

```bash
curl -sS http://127.0.0.1:8000/api/v1/users/me
curl -sS http://127.0.0.1:8000/api/v1/security/roles
curl -sS http://127.0.0.1:8000/api/v1/security/permissions
curl -sS http://127.0.0.1:8000/api/v1/audit-logs
```

- 预想结果：`users/me` 返回 `user_id=system`，`roles` 和 `permissions` 返回冻结目录，`audit-logs` 返回列表。
- 失败现象：返回 404、500 或空结构。
- 应该查看：`docs/LEARNING_API_WALKTHROUGH.md`、`backend/app/services/security_service.py`、`backend/app/services/audit_service.py`。

## 10. 一次性代码验证是否通过

- 执行命令：

```bash
./scripts/run_tests.sh
```

- 预想结果：Backend tests、Frontend tests、Frontend build 和 Python compileall 全部通过。
- 失败现象：脚本停在第一个失败阶段。
- 应该查看：`docs/TEST_CASES.md`、`README.md`。

## 11. PostgreSQL 可选验证是否符合当前环境

- 执行命令：

```bash
./scripts/verify_postgres_phase2.sh
```

- 预想结果：如果环境具备 `psycopg` 和 Docker，脚本会自动跑 PostgreSQL 验证；如果不具备，脚本会明确说明跳过原因。
- 失败现象：`docker: command not found`、`psycopg is not installed`。
- 应该查看：`docs/DATABASE.md`、`RUNBOOK_LOCAL.md`。

## 12. Swagger / ReDoc / OpenAPI JSON 是否都能打开

- 执行命令：

```bash
curl -I http://127.0.0.1:8000/docs
curl -I http://127.0.0.1:8000/redoc
curl -sS http://127.0.0.1:8000/openapi.json | head
```

- 预想结果：三个入口都能访问，`openapi.json` 返回 JSON。
- 失败现象：404、Connection refused、JSON 解析失败。
- 应该查看：`RUNBOOK_LOCAL.md`、`docs/LEARNING_API_WALKTHROUGH.md`。

## 13. unittest 是否在 backend 目录执行

- 执行命令：

```bash
cd backend
python3 -m unittest tests.test_api -v
```

- 预想结果：测试能被正确发现并执行。
- 失败现象：`ModuleNotFoundError: No module named tests`。
- 应该查看：`docs/TEST_CASES.md`、`RUNBOOK_LOCAL.md`。

## 14. 不要在项目根目录直接执行 unittest

- 执行命令：

```bash
python3 -m unittest tests.test_api -v
```

- 预想结果：这条命令**不应作为标准做法**，因为通常会找不到 `tests` 包。
- 失败现象：`ModuleNotFoundError: No module named tests`。
- 应该查看：`docs/TEST_CASES.md`、`RUNBOOK_LOCAL.md`。
