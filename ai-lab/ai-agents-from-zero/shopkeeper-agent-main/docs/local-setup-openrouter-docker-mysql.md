# 当前推荐方案：OpenRouter + NAS MySQL

这个项目最适合的本地组合是：

- 大模型：`OpenRouter`
- 结构化业务库：`JtProject` 里使用的 NAS `MySQL`
- 向量库：本机 `Qdrant`
- 全文检索：本机 `Elasticsearch`
- 向量生成：本机 `Embedding`
- 前端：本机 `React + Vite`

## 1. 为什么推荐这个组合

- `OpenRouter` 方便统一接入多个兼容模型，不需要为不同供应商单独改代码。
- 你当前工作区已经有一套可用的 NAS MySQL，可直接复用。
- 这套项目里，MySQL 只是业务数据源，不是核心服务本身，所以复用现成 NAS 数据库最省事。

## 2. 当前前提

你需要先确保：

- 如果要跑本机基础服务，Docker Desktop 已经可用
- 如果暂时不修 Docker，也可以先走 `Mock`
- NAS MySQL 可从当前工作区访问

## 3. `.env` 推荐填写方式

先复制模板：

```bash
cp .env.nas.example .env
```

然后按下面方式填写：

```bash
# OpenRouter
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_API_KEY=你的_openrouter_api_key
LLM_MODEL_NAME=openai/gpt-4o-mini
LLM_BASE_URL=https://openrouter.ai/api/v1

# 运行模式
MOCK_MODE=false

# NAS MySQL
DB_META_HOST=192.168.10.2
DB_META_PORT=3306
DB_META_USER=root
DB_META_PASSWORD=123456
DB_META_DATABASE=meta
DB_DW_HOST=192.168.10.2
DB_DW_PORT=3306
DB_DW_USER=root
DB_DW_PASSWORD=123456
DB_DW_DATABASE=dw

# 向量库
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_EMBEDDING_SIZE=1024

# Embedding
EMBEDDING_HOST=localhost
EMBEDDING_PORT=8081
EMBEDDING_MODEL=BAAI/bge-large-zh-v1.5

# 全文检索
ES_HOST=localhost
ES_PORT=9200
ES_INDEX_NAME=data_agent
```

## 4. MySQL 连接方式

当前直接连接 NAS 上的 MySQL：

- Host: `192.168.10.2`
- Port: `3306`
- Database: `meta` / `dw`
- User: `root`
- Password: `123456`

如果后续你想切回 Docker MySQL，再重新把 `DB_*` 改成本机容器即可。

## 5. 启动顺序

### 5.1 推荐：先 Mock 再真实

如果你只是想先把页面和问数流程跑起来，先看：

- [Mock 优先启动说明](mock-first-quickstart.md)

### 5.2 真实链路

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
bash scripts/up_local_stack.sh up
python3 -m app.scripts.build_meta_knowledge -c conf/meta_config.yaml
python3 -m uvicorn main:app --host 127.0.0.1 --port 8000
```

前端：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main/frontend
pnpm install
pnpm dev
```

## 6. 验证顺序

建议按这个顺序验证：

1. 先看 `.env`
2. 再看后端能不能启动
3. 再看 `meta` / `dw` 能不能连上
4. 再看 `build_meta_knowledge` 能不能跑完
5. 再看前端能不能展示问数结果

## 7. 预期结果

当这一套配置完成后：

- 主问数链路可以用 `OpenRouter` 调用模型
- 数据库查询可以访问 NAS 上的 MySQL
- 前端会在页面里看到问数过程和结果
- 你就可以开始验证“数据库检索 + 智能体回答”的完整链路
