# Mock 启动命令块

> 复制即可执行，先把项目跑起来，不依赖 Docker。

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
cp .env.mock.example .env
MOCK_MODE=true python3 -m uvicorn main:app --host 127.0.0.1 --port 8000
```

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main/frontend
pnpm install
pnpm dev
```

```bash
curl -N -sS -X POST http://127.0.0.1:8000/api/query -H 'Content-Type: application/json' -d '{"query":"统计华北地区销售额"}'
```

## 预期结果

- 后端启动后，`/api/query` 可用
- 前端启动后，可在页面中直接输入问题
- `curl` 会先看到多段 `progress`，最后看到 `result`

## 最短判断

- 能看到 `Uvicorn running`，说明后端起来了
- 页面能打开并发起请求，说明前后端联调通了
- `curl` 返回 SSE，说明 mock 问数链路通了
