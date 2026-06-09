# 当前推荐方案：OpenRouter + NAS MySQL

这个项目最适合的本地组合是：

- 大模型：`OpenRouter`
- 结构化业务库：`JtProject` 里使用的 NAS `MySQL`
- 互联网搜索：`Tavily`
- 私有知识库：`RAGFlow`

## 1. 为什么推荐这个组合

- `OpenRouter` 方便统一接入多个兼容模型，不需要为不同供应商单独改代码。
- 你当前工作区已经有一套可用的 NAS MySQL，可直接复用 `JtProject` 的远端数据库配置。
- 这套项目里，MySQL 只是业务数据源，不是核心服务本身，所以复用现成 NAS 数据库最省事。

## 2. 当前前提

你需要先确保：

- Docker Desktop 已安装
- Docker Desktop 的 WSL Integration 已开启
- 当前 WSL 发行版已经被 Docker Desktop 勾选

如果这一步没开通，当前工作区里的 WSL 还是不能直接运行 `docker compose`。
不过在当前方案里，MySQL 已经切到 NAS，不再依赖本机容器启动。

## 3. `.env` 推荐填写方式

先复制模板：

```bash
cp .env.template .env
```

然后按下面方式填写：

```bash
# OpenRouter
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_API_KEY=你的_openrouter_api_key
LLM_QWEN_MAX=你的_openrouter_model_name

# Tavily
TAVILY_API_KEY=你的_tavily_api_key

# RAGFlow
RAGFLOW_API_URL=http://你的-ragflow-host
RAGFLOW_API_KEY=你的_ragflow_api_key

# NAS MySQL
MYSQL_HOST=192.168.10.2
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=123456
MYSQL_DATABASE=ecommjava
MYSQL_CHARSET=utf8mb4
MYSQL_COLLATION=utf8mb4_unicode_ci
MYSQL_SQL_MODE=TRADITIONAL
```

## 4. MySQL 连接方式

当前直接连接 NAS 上的 MySQL：

- Host: `192.168.10.2`
- Port: `3306`
- Database: `ecommjava`
- User: `root`
- Password: `123456`

如果后续你想切回 Docker MySQL，再重新把 `MYSQL_*` 改成本机容器即可。

## 5. 验证顺序

建议按这个顺序验证：

1. `python3 ai-lab/ai-agents-from-zero/deepsearch-agents-main/scripts/check_environment.py`
2. 确认后端能启动
3. 确认前端能启动
4. 确认 `/api/health` 显示 `OpenRouter` 和 `MySQL` 已配置
5. 再测试数据库查询类任务

## 6. 预期结果

当这一套配置完成后：

- 主智能体可以用 `OpenRouter` 调用模型
- 数据库查询助手可以访问 NAS 上的 MySQL
- 前端会在健康面板里看到后端、模型和 MySQL 状态
- 你就可以开始验证“数据库检索 + 智能体回答”的完整链路
