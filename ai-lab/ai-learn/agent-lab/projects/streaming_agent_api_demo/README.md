# Streaming Agent API

FastAPI SSE 最小模板，定义 `status`、`token`、`error`、`done` 四种事件，并通过异步生成器保留客户端断开时的取消点。

```bash
uvicorn main:app --port 8000
curl -N -X POST http://127.0.0.1:8000/runs/stream -H 'Content-Type: application/json' -d '{"message":"解释 Tool Calling"}'
curl -N -X POST http://127.0.0.1:8000/runs/stream -H 'Content-Type: application/json' -d '{"message":"error"}'
```

验收：正常路径以 `done` 结束；异常路径发送结构化 `error` 且不再发送 `done`；反向代理禁用缓冲。依赖：`fastapi`、`uvicorn`。
