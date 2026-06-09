# 本地推荐方案：OpenRouter + Docker MySQL

这个项目最适合的本地组合是：

- 大模型：`OpenRouter`
- 结构化业务库：本机 `Docker MySQL`
- 互联网搜索：`Tavily`
- 私有知识库：`RAGFlow`

## 1. 为什么推荐这个组合

- `OpenRouter` 方便统一接入多个兼容模型，不需要为不同供应商单独改代码。
- `Docker MySQL` 可以在本机快速拉起一套干净的教学业务库，适合调试数据库查询子智能体。
- 这套项目里，MySQL 只是业务数据源，不是核心服务本身，所以用容器最省事。

## 2. 当前前提

你需要先确保：

- Docker Desktop 已安装
- Docker Desktop 的 WSL Integration 已开启
- 当前 WSL 发行版已经被 Docker Desktop 勾选

如果这一步没开通，当前工作区里的 WSL 还是不能直接运行 `docker compose`。

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

# Docker MySQL
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3307
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DATABASE=deepsearch_db
MYSQL_CHARSET=utf8mb4
MYSQL_COLLATION=utf8mb4_unicode_ci
MYSQL_SQL_MODE=TRADITIONAL
```

## 4. MySQL 启动方式

在 Docker Desktop 的 WSL Integration 已启用后，进入项目的 `docker` 目录执行：

```bash
docker compose up -d
```

如果想看状态：

```bash
docker compose ps
```

如果想看初始化日志：

```bash
docker compose logs -f mysql
```

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
- 数据库查询助手可以访问本机 Docker MySQL
- 前端会在健康面板里看到后端、模型和 MySQL 状态
- 你就可以开始验证“数据库检索 + 智能体回答”的完整链路

