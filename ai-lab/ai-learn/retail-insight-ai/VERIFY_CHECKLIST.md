# VERIFY CHECKLIST

所有命令默认先进入项目根目录：

```bash
cd ~/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai
```

需要三个终端：终端 A 运行 Backend，终端 B 运行 Frontend，终端 C 执行检查命令。首次启动会安装本地依赖，耗时可能较长。

## 1. Backend 是否启动

- 命令（终端 A）：

  ```bash
  ./scripts/start_backend.sh
  ```

- 预期结果：终端出现 `Uvicorn running on http://127.0.0.1:8000` 和 `Application startup complete`，随后持续运行。
- 失败时看：`scripts/start_backend.sh`、`backend/requirements.txt`、`backend/app/main.py`、Backend 终端异常堆栈。环境问题先运行 `./scripts/check_env.sh`。

## 2. Frontend 是否启动

- 命令（终端 B，保持 Backend 运行）：

  ```bash
  ./scripts/start_frontend.sh
  ```

- 预期结果：终端显示 `Local: http://127.0.0.1:5173/`；浏览器打开该地址能看到 Retail Insight AI 页面。
- 失败时看：`scripts/start_frontend.sh`、`frontend/package.json`、`frontend/vite.config.ts` 和 Frontend 终端错误。

## 3. health 是否 OK

- 命令（终端 C）：

  ```bash
  curl -sS http://127.0.0.1:8000/health
  ```

- 预期结果：HTTP 返回 JSON，包含 `"status":"ok"`、`"service":"retail-insight-ai"`、`"provider":"static"` 和非空 `request_id`。
- 失败时看：`backend/app/api/health.py`、`backend/app/main.py`、Backend 终端；`Connection refused` 通常表示 Backend 未运行或 8000 端口不对。

## 4. 任务是否创建成功

- 命令（终端 C；同时把 task_id 保存到当前 shell）：

  ```bash
  CREATE_RESPONSE=$(curl -sS -X POST http://127.0.0.1:8000/api/tasks -H 'Content-Type: application/json' -H 'X-Request-ID: verify-local-001' -d '{"question":"売上と在庫の状況を分析してください","mode":"hybrid"}')
  printf '%s\n' "$CREATE_RESPONSE"
  TASK_ID=$(printf '%s' "$CREATE_RESPONSE" | python3 -c 'import json,sys; print(json.load(sys.stdin)["data"]["task_id"])')
  printf 'TASK_ID=%s\n' "$TASK_ID"
  ```

- 预期结果：响应包含 `"success":true`、`"status":"queued"`，最后打印一个 UUID 格式的 `TASK_ID`。
- 失败时看：`backend/app/schemas/task_api.py`、`backend/app/api/tasks.py`、`backend/app/services/task_service.py` 和 Backend 日志中的 `request_id=verify-local-001`。

## 5. SSE 是否有 status

- 命令（终端 C；沿用上一步同一终端中的 `TASK_ID`）：

  ```bash
  curl -sS -N "http://127.0.0.1:8000/api/tasks/$TASK_ID/events"
  ```

- 预期结果：至少出现一组 `event: status` 和对应的 `data:`；成功任务最后出现 `event: done`。每组事件有递增的 `id`，data 中有 status、message、request_id 等字段。
- 失败时看：`backend/app/events/sse.py`、`backend/app/events/publisher.py`、`backend/app/api/tasks.py` 和 `repositories/implementations/in_memory/event_repository.py`。404 通常表示 Backend 重启过，内存任务已丢失。

## 6. 是否生成报告

- 命令（终端 C；沿用 `TASK_ID`）：

  ```bash
  curl -sS "http://127.0.0.1:8000/api/tasks/$TASK_ID/report"
  ```

- 预期结果：响应包含 `"success":true`、`"provider":"static"`，`markdown` 中有报告标题、KPI 和 Research 章节。也可在页面提交任务，确认“分析レポート”区域出现同一报告。
- 失败时看：`backend/app/reports/generator.py`、`backend/app/services/task_service.py`、`repositories/implementations/in_memory/report_repository.py` 和 `frontend/src/App.tsx` 的 `loadReport()`。若返回 `REPORT_NOT_FOUND`，先确认 SSE 已收到 done。

## 7. 错误输入是否显示错误

- 命令（自动验证 Error Panel；终端 C）：

  ```bash
  cd frontend && npm test -- --run App.test.tsx -t "shows a task creation error"
  ```

- 预期结果：Vitest 显示该测试通过。测试向页面返回 HTTP 422 `VALIDATION_ERROR`，并断言 `role="alert"` 显示错误码和消息。页面本身会禁用空白问题的提交按钮，所以用测试稳定覆盖服务端拒绝输入后的显示路径。
- 失败时看：`frontend/src/App.test.tsx`、`frontend/src/App.tsx` 的 `submit()`/ErrorPanel、`frontend/src/api.ts` 的 `unwrapResponse()`，以及 `backend/app/errors/handlers.py`。

如需单独确认 Backend 的错误输入合同，在项目根目录执行：

```bash
curl -sS -X POST http://127.0.0.1:8000/api/tasks -H 'Content-Type: application/json' -H 'X-Request-ID: verify-invalid-001' -d '{"question":"","mode":"hybrid"}'
```

预期包含 `"success":false` 和 `"code":"VALIDATION_ERROR"`。

## 8. 日志是否有 request_id / task_id

- 命令（终端 C 发起带固定 request_id 的请求；然后查看终端 A）：

  ```bash
  curl -sS -X POST http://127.0.0.1:8000/api/tasks -H 'Content-Type: application/json' -H 'X-Request-ID: verify-log-001' -d '{"question":"ログ項目を確認してください","mode":"kpi"}'
  ```

- 预期结果：Backend JSON 日志中能找到 `"request_id":"verify-log-001"`；`task_created`、Workflow 节点、`task_completed` 和 SSE 相关日志包含同一个非空 `task_id`。
- 失败时看：`backend/app/main.py` 的 `request_context()`、`backend/app/observability/logging.py`、`backend/app/events/publisher.py` 和 `backend/app/services/task_service.py`。

## 一次性代码验证

- 命令：

  ```bash
  ./scripts/run_tests.sh
  ```

- 预期结果：Backend tests、Frontend tests、Frontend build 和 Python compileall 全部通过。
- 失败时看：输出中第一个失败阶段及对应的 `backend/tests/` 或 `frontend/src/*.test.ts*`；不要跳过第一个错误继续猜后续问题。
