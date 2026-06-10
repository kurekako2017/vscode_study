# OpenRouter + NAS MySQL 最短 5 行命令

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
cp .env.nas.example .env
bash scripts/up_local_stack.sh up && python3 -m app.scripts.build_meta_knowledge -c conf/meta_config.yaml && python3 -m uvicorn main:app --host 127.0.0.1 --port 8000
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main/frontend
pnpm install && pnpm dev
```

## 先测接口

```bash
curl -N -sS -X POST http://127.0.0.1:8000/api/query -H 'Content-Type: application/json' -d '{"query":"统计华北地区销售额"}'
```

## 预期结果

- 基础服务先起来
- 元数据知识库构建成功
- 后端启动成功
- 前端启动成功
- 问数接口返回真实 SSE
