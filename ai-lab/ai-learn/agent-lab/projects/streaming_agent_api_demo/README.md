# Streaming Agent API

FastAPI SSE 最小模板，定义 `status`、`token`、`error`、`done` 四种事件，并通过异步生成器保留客户端断开时的取消点。

```bash
uvicorn main:app --port 8000
curl -N -X POST http://127.0.0.1:8000/runs/stream -H 'Content-Type: application/json' -d '{"message":"解释 Tool Calling"}'
curl -N -X POST http://127.0.0.1:8000/runs/stream -H 'Content-Type: application/json' -d '{"message":"error"}'
```

验收：正常路径以 `done` 结束；异常路径发送结构化 `error` 且不再发送 `done`；反向代理禁用缓冲。依赖：`fastapi`、`uvicorn`。

## 业务场景（完整说明）

- **使用者**：聊天 UI、长任务控制台和 Agent API 开发者。
- **要解决的问题**：模型或工具执行时间较长时，持续向客户端发送阶段、文本、错误和结束事件，避免页面长时间无响应。
- **输入与输出**：输入 HTTP JSON 消息；输出 SSE 的 status、token、error、done 事件流。
- **生产环境差距**：需要真实模型流、断线重连、Last-Event-ID、任务取消、心跳、鉴权和代理超时配置。

## 整体流程图

```mermaid
flowchart TD
    A[客户端 POST 消息] --> B[FastAPI 接收请求]
    B --> C[创建异步事件生成器]
    C --> D[发送 status]
    D --> E{是否模拟错误}
    E -- 是 --> F[发送 error 并结束]
    E -- 否 --> G[逐块发送 token]
    G --> H[发送 done]
    F --> I[客户端关闭流]
    H --> I
```
