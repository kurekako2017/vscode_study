# 本地环境推进记录

> 说明：这份文档记录 `shopkeeper-agent-main` 在本地环境搭建上的推进情况，适合边做边更新。

## 已完成

- 后端配置已改成可通过 `.env` 覆盖
- 已补充 `.env.example`
- 已确认后端会在启动时加载项目根目录 `.env`
- 已确认前端支持 `VITE_DEV_PROXY_TARGET` / `VITE_API_BASE_URL`
- 已确认 Docker Compose 会启动 `MySQL`、`Qdrant`、`Elasticsearch`、`Kibana`、`Embedding`
- 已把 Embedding 客户端改成兼容本机 TEI 的适配器，不再把 URL 误传给 Hugging Face Hub 包装器
- 已验证 `main.py` 能生成 OpenAPI，且 `/api/query` 已挂载到 FastAPI 应用上
- 已验证 `uvicorn main:app` 可以完成启动

## 进行中

- 选择数据库来源
  - 已倾向采用 `OpenRouter + NAS MySQL`
  - 参考文档：[OpenRouter + NAS MySQL 本地方案](openrouter-nas-mysql-setup.md)
- 准备 `.env`
- 准备 Embedding 模型文件
- 启动 Docker 基础服务
- 打通 NAS MySQL、Qdrant、Elasticsearch 和 TEI 的真实联调

## 待执行

- 执行元数据知识库构建脚本
- 启动前端页面
- 完成一次自然语言问数验证

## 当前推荐的最小推进路径

1. 复制 `.env.nas.example` 为 `.env`
2. 先填 `OPENROUTER_API_KEY`
3. 在 NAS MySQL 上准备 `meta` / `dw`
4. 执行 `scripts/bootstrap_local_env.sh`
5. 下载 Embedding 模型
6. 启动 Qdrant / Elasticsearch / Embedding
7. 再启动后端与前端

## 验证点

- `uv run fastapi dev main.py` 可启动
- `main.app.openapi()` 可以看到 `/api/query`
- `http://127.0.0.1:8000/docs` 可访问
- `pnpm dev` 可启动前端
- `/api/query` 可返回 SSE
