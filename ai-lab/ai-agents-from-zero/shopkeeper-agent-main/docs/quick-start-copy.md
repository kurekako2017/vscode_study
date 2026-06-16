# 复制即启动

> 这是一页最实用的启动命令合集。  
> 默认先跑真实模式；Mock 只作为外部服务不可用时的联调兜底。

## 1. 真实模式启动

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
cp .env.nas.example .env
bash scripts/up_local_stack.sh up
ollama list
.venv/bin/python -m app.scripts.build_meta_knowledge -c conf/meta_config.yaml
.venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

另开一个终端：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main/frontend
VITE_API_BASE_URL= VITE_DEV_PROXY_TARGET=http://127.0.0.1:8000 npm run dev -- --host 0.0.0.0 --port 5173
```

## 2. 真实模式验证

```bash
curl -N -sS -X POST http://127.0.0.1:8000/api/query -H 'Content-Type: application/json' -d '{"query":"统计华北地区销售额"}'
```

## 3. Mock 启动

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
cp .env.mock.example .env
MOCK_MODE=true .venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

另开一个终端：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main/frontend
VITE_API_BASE_URL= VITE_DEV_PROXY_TARGET=http://127.0.0.1:8000 npm run dev -- --host 0.0.0.0 --port 5173
```

## 4. Mock 验证

```bash
curl -N -sS -X POST http://127.0.0.1:8000/api/query -H 'Content-Type: application/json' -d '{"query":"统计华北地区销售额"}'
```

## 5. 最短判断

- 后端有 `Uvicorn running`
- 前端有 `VITE ready`
- `/api/query` 有 `progress` 和 `result`
