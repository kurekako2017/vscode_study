# 启动完成检查清单

按下面顺序逐项验证。每一项都要能明确说出“怎么确认成功”。

## 失败时先看哪个文档

| 问题 | 先看哪个文档 |
| --- | --- |
| 后端启动失败 | `RUNBOOK_LOCAL.md`、`backend/app/main.py` |
| 前端启动失败 | `RUNBOOK_LOCAL.md`、`frontend/src/App.tsx` |
| Swagger 打不开 | `RUNBOOK_LOCAL.md`、`docs/LEARNING_API_WALKTHROUGH.md` |
| 主链路 API 失败 | `docs/LEARNING_API_WALKTHROUGH.md`、`docs/ARCHITECTURE.md` |
| 测试失败 | `docs/TEST_CASES.md`、`README.md` |
| 日志/审计异常 | `docs/ERROR_CATALOG.md`、`docs/MASTER_PROMPT.md` |

## 1. 后端是否启动成功

- 命令：

```bash
./scripts/start_backend.sh
```

- 如何验证成功：终端出现 `Uvicorn running on http://127.0.0.1:8000` 和 `Application startup complete`，并且进程持续运行。
- 常见失败现象：`ModuleNotFoundError`、`Address already in use`、`ImportError`、`SyntaxError`。
- 处理方式：先看后端终端日志，再检查 `RUNBOOK_LOCAL.md` 和 `backend/app/main.py`。

## 2. 前端是否启动成功

- 命令：

```bash
./scripts/start_frontend.sh
```

- 如何验证成功：终端出现 `Local: http://127.0.0.1:5173/`，浏览器能打开前端页面。
- 常见失败现象：5173 被占用、npm 依赖未安装、Vite 报错。
- 处理方式：先检查 `RUNBOOK_LOCAL.md` 和前端终端日志。

## 3. health 是否可访问

- 命令：

```bash
curl -sS http://127.0.0.1:8000/health
```

- 如何验证成功：返回 JSON，包含 `status=ok`、`service=retail-insight-ai`、`provider=static` 和非空 `request_id`。
- 常见失败现象：`Connection refused`、404、空响应。
- 处理方式：回头确认后端是否真的在 8000 端口运行，并对照 `docs/LEARNING_API_WALKTHROUGH.md`。

## 4. 任务是否创建成功

- 命令：

```bash
CREATE_RESPONSE=$(curl -sS -X POST http://127.0.0.1:8000/api/tasks -H 'Content-Type: application/json' -H 'X-Request-ID: verify-local-001' -d '{"question":"売上と在庫の状況を分析してください","mode":"hybrid"}')
printf '%s\n' "$CREATE_RESPONSE"
TASK_ID=$(printf '%s' "$CREATE_RESPONSE" | python3 -c 'import json,sys; print(json.load(sys.stdin)["data"]["task_id"])')
printf 'TASK_ID=%s\n' "$TASK_ID"
```

- 如何验证成功：响应包含 `success=true`、`status=queued`，并打印出一个 UUID 格式的 `TASK_ID`。
- 常见失败现象：HTTP 422、`VALIDATION_ERROR`、JSON 解析失败。
- 处理方式：检查 `docs/LEARNING_API_WALKTHROUGH.md` 和 `backend/app/api/tasks.py`。

## 5. SSE 是否能收到状态事件

- 命令：

```bash
curl -sS -N "http://127.0.0.1:8000/api/tasks/$TASK_ID/events"
```

- 如何验证成功：至少能看到一条 `event: status`，任务结束时能看到 `event: done` 或 `event: error`。
- 常见失败现象：连接立即断开、没有事件、`404`。
- 处理方式：确认任务 ID 没写错，后端没有重启，查看 `docs/LEARNING_API_WALKTHROUGH.md`。

## 6. 报告是否能读取

- 命令：

```bash
curl -sS "http://127.0.0.1:8000/api/tasks/$TASK_ID/report"
```

- 如何验证成功：返回 `success=true`、`status=generated`，`markdown` 中有报告标题和正文。
- 常见失败现象：`REPORT_NOT_FOUND`。
- 处理方式：先确认 SSE 已经出现 `done`，再对照 `docs/LEARNING_API_WALKTHROUGH.md` 取报告。

## 7. 错误输入是否能正确返回

- 命令：

```bash
curl -sS -X POST http://127.0.0.1:8000/api/tasks -H 'Content-Type: application/json' -d '{"question":"","mode":"hybrid"}'
```

- 如何验证成功：返回 `success=false`，并带有 `code=VALIDATION_ERROR`。
- 常见失败现象：请求被错误接受，或者返回格式不符合统一 envelope。
- 处理方式：检查 `docs/ERROR_CATALOG.md` 和 `backend/app/api/tasks.py`。

## 8. 日志是否包含 request_id / task_id

- 命令：

```bash
curl -sS -X POST http://127.0.0.1:8000/api/tasks -H 'Content-Type: application/json' -H 'X-Request-ID: verify-log-001' -d '{"question":"ログ項目を確認してください","mode":"kpi"}'
```

- 如何验证成功：后端 JSON 日志能找到 `request_id=verify-log-001`，并且任务相关日志带有同一个 `task_id`。
- 常见失败现象：日志没有结构化字段，或者字段值为空。
- 处理方式：检查 `docs/MASTER_PROMPT.md` 和 `backend/app/main.py`。

## 9. Security read model 是否正常

- 命令：

```bash
curl -sS http://127.0.0.1:8000/api/v1/users/me
curl -sS http://127.0.0.1:8000/api/v1/security/roles
curl -sS http://127.0.0.1:8000/api/v1/security/permissions
curl -sS http://127.0.0.1:8000/api/v1/audit-logs
```

- 如何验证成功：`users/me` 返回 `user_id=system`，`roles` 和 `permissions` 返回冻结目录，`audit-logs` 返回列表。
- 常见失败现象：返回 404、500 或空结构。
- 处理方式：检查 `docs/LEARNING_API_WALKTHROUGH.md` 和对应 service。

## 10. 一次性代码验证是否通过

- 命令：

```bash
./scripts/run_tests.sh
```

- 如何验证成功：Backend tests、Frontend tests、Frontend build 和 Python compileall 全部通过。
- 常见失败现象：脚本停在第一个失败阶段。
- 处理方式：优先修复最早失败的测试或构建阶段，再看 `docs/TEST_CASES.md`。

## 11. PostgreSQL 可选验证是否符合当前环境

- 命令：

```bash
./scripts/verify_postgres_phase2.sh
```

- 如何验证成功：如果环境具备 `psycopg` 和 Docker，脚本会自动跑 PostgreSQL 验证；如果不具备，脚本会明确说明跳过原因。
- 常见失败现象：`docker: command not found`、`psycopg is not installed`。
- 处理方式：确认当前环境边界，允许跳过，但不要把跳过写成成功；必要时回看 `docs/DATABASE.md`。
