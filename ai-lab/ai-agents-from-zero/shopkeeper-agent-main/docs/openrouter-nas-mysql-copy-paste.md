# OpenRouter + NAS MySQL 命令块

> 复制即可执行，适合你切回真实模式时直接用。

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
cp .env.nas.example .env
bash scripts/up_local_stack.sh up
python3 -m app.scripts.build_meta_knowledge -c conf/meta_config.yaml
python3 -m uvicorn main:app --host 127.0.0.1 --port 8000
```

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main/frontend
pnpm install
pnpm dev
```

## 预期结果

- NAS MySQL 可连通
- 本机 Qdrant / Elasticsearch / Embedding 已启动
- 元数据知识库已构建完成
- 后端 `/api/query` 可用
- 前端可以展示真实问数流程
