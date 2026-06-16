# OpenRouter / NVIDIA / Ollama + NAS MySQL 启动说明

> 这份说明是给“切回真实模式”的版本。
> 目标是把项目重新接到你 NAS 上的 MySQL，并按 `OpenRouter -> NVIDIA -> 本地 Ollama qwen2.5-coder:1.5b` 调用模型。

## 适合什么情况

- 你已经准备好了 OpenRouter API Key
- 你可以选择再补 NVIDIA API Key
- 你本地已经有 Ollama `qwen2.5-coder:1.5b`
- 你希望复用 NAS 上的 MySQL，而不是在本机再起一套 MySQL 容器
- 你想跑真实问数链路，而不是 mock 流程

## 这个模式会做什么

- 后端优先使用 OpenRouter 调用大模型
- OpenRouter 不可用时尝试 NVIDIA
- 远端模型都不可用时尝试本地 Ollama
- `meta` 和 `dw` 连接 NAS MySQL
- Qdrant、Elasticsearch、Embedding 继续由本机 Docker 提供
- 前端仍然通过 SSE 看真实问数过程

## 一次性准备

1. 复制环境文件：

```bash
cp .env.nas.example .env
```

2. 按你的实际情况补齐：

```bash
OPENROUTER_API_KEY=你的_openrouter_api_key
NVIDIA_API_KEY=你的_nvidia_api_key
OLLAMA_BASE_URL=http://127.0.0.1:11434/v1
OLLAMA_MODEL_NAME=qwen2.5-coder:1.5b
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
```

## 启动顺序

### 1. 准备 NAS MySQL

确认 NAS 上已经存在：

- `meta`
- `dw`

并且 `docker/mysql/meta.sql`、`docker/mysql/dw.sql` 已导入。

### 2. 启动本机基础服务

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
bash scripts/up_local_stack.sh up
```

预期结果：

- `Qdrant` 可访问 `http://127.0.0.1:6333`
- `Elasticsearch` 可访问 `http://127.0.0.1:9200`
- `Kibana` 可访问 `http://127.0.0.1:5601`
- `Embedding` 可访问 `http://127.0.0.1:8081`

### 2.1 检查本地 Ollama 回退模型

```bash
ollama list
```

预期结果：

- 能看到 `qwen2.5-coder:1.5b`

如果没有，执行：

```bash
ollama pull qwen2.5-coder:1.5b
```

### 3. 构建元数据知识库

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
python3 -m app.scripts.build_meta_knowledge -c conf/meta_config.yaml
```

预期结果：

- 表信息、字段信息、指标信息写入 NAS MySQL
- 字段和指标向量写入 Qdrant
- 字段取值写入 Elasticsearch

### 4. 启动后端

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main
python3 -m uvicorn main:app --host 127.0.0.1 --port 8000
```

预期结果：

- 终端出现 `Uvicorn running on http://127.0.0.1:8000`
- `/api/query` 可访问

### 5. 启动前端

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/shopkeeper-agent-main/frontend
pnpm install
pnpm dev
```

## 如何测试

### 测试 1：检查 NAS MySQL 是否连通

```bash
mysql -h 192.168.10.2 -P 3306 -u root -p
```

预期结果：

- 能登录
- 能看到 `meta` 和 `dw` 数据库

### 测试 2：检查后端接口

```bash
curl -N -sS -X POST http://127.0.0.1:8000/api/query -H 'Content-Type: application/json' -d '{"query":"统计华北地区销售额"}'
```

预期结果：

- 先返回多段 `progress`
- 再返回 `result`
- `result` 里是模型生成的 SQL 和真实查询结果

### 测试 3：检查前端联动

输入：

```text
统计华北地区销售额
```

预期结果：

- 页面显示问数进度
- 页面展示 SQL
- 页面展示结果表格

## 什么时候说明搭好了

当下面这些都成立，就说明真实链路搭好了：

- NAS MySQL 可连通
- `meta` / `dw` 已导入
- `build_meta_knowledge` 能成功执行
- `Qdrant` / `Elasticsearch` / `Embedding` 都在线
- 后端 `/api/query` 可以返回真实 SSE
- 前端可以正常显示问数结果

## 这条路的价值

- 让你最终从 mock 平滑切到真实业务链路
- 可以复用 NAS 上已有 MySQL
- 可以复用 OpenRouter Key
- 不需要在本机再额外维护一套 MySQL 容器
