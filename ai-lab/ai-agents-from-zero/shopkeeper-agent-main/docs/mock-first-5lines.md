# Mock 最短 5 行命令

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
cp .env.mock.example .env
MOCK_MODE=true python3 -m uvicorn main:app --host 127.0.0.1 --port 8000
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main/frontend
pnpm install && pnpm dev
```

## 先测接口

```bash
curl -N -sS -X POST http://127.0.0.1:8000/api/query -H 'Content-Type: application/json' -d '{"query":"统计华北地区销售额"}'
```

## 预期结果

- 后端先起来
- 前端再起来
- 问数请求返回 SSE 流
- 页面显示进度和结果
