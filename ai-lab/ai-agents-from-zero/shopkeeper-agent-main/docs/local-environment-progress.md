# 本地环境推进记录

> 说明：这份文档记录 `shopkeeper-agent-main` 在本地环境搭建上的推进情况，适合边做边更新。

## 已完成

- 后端配置已改成可通过 `.env` 覆盖
- 已增加 `MOCK_MODE`，可在没有 Docker 的情况下先跑 mock SSE 链路
- 已补充 `.env.example`
- 已确认后端会在启动时加载项目根目录 `.env`
- 已确认前端支持 `VITE_DEV_PROXY_TARGET` / `VITE_API_BASE_URL`
- 已确认 Docker Compose 可以分别支持本机整套环境和 NAS MySQL 方案
- 已把 Embedding 客户端改成兼容本机 TEI 的适配器，不再把 URL 误传给 Hugging Face Hub 包装器
- 已验证 `main.py` 能生成 OpenAPI，且 `/api/query` 已挂载到 FastAPI 应用上
- 已验证 `uvicorn main:app` 可以完成启动
- 当前这个 WSL 里常规 `docker` CLI / Windows 互通命令不可用，但 Docker 守护进程本身是可达的，现有 `Qdrant` / `Elasticsearch` / `Kibana` / `Embedding` 容器仍在运行
- 已确认 NAS 友好版 `docker/docker-compose.nas.yaml` 能成功创建并启动 `Qdrant`、`Elasticsearch`、`Kibana` 和 `Embedding`
- 已确认 NAS MySQL 中的 `meta` 和 `dw` 库已创建并导入初始化表结构与样例数据
- 已确认 `build_meta_knowledge` 可以跑通并成功写入元数据、向量索引和全文索引

## 进行中

- 选择数据库来源
  - 已倾向采用 `OpenRouter + NAS MySQL`
  - 当前实际连通测试优先使用 NAS `root / 123456`
  - 参考文档：[OpenRouter + NAS MySQL 本地方案](openrouter-nas-mysql-setup.md)
- 如果暂时不修 Docker，可以先走 mock 版本启动
  - 参考文档：[Mock 优先启动说明](mock-first-quickstart.md)
  - 最短命令版：[Mock 启动命令块](mock-first-copy-paste.md)
  - 5 行极简版：[Mock 最短 5 行命令](mock-first-5lines.md)
- 如果要切回真实模式，可以走 OpenRouter + NAS MySQL
  - 参考文档：[OpenRouter + NAS MySQL 启动说明](openrouter-nas-mysql-quickstart.md)
  - 最短命令版：[OpenRouter + NAS MySQL 命令块](openrouter-nas-mysql-copy-paste.md)
  - 5 行极简版：[OpenRouter + NAS MySQL 最短 5 行命令](openrouter-nas-mysql-5lines.md)
- 如果想先看功能和测试方法
  - 参考文档：[功能一览与测试指南](feature-overview-and-test-guide.md)
  - 清单版：[功能检查清单](feature-checklist.md)
- 如果想先看最终版总入口
  - 参考文档：[启动 / 验证 / 排错最终说明](start-verify-troubleshoot-final.md)
- 准备 `.env`
- 准备 Embedding 模型文件
  - 现在 NAS 友好 compose 已改成首次启动自动拉取 `BAAI/bge-large-zh-v1.5`
- 启动 Docker 基础服务
  - NAS 方案建议只起 `docker/docker-compose.nas.yaml`，避免和 NAS MySQL 的 `3306` 冲突
- 打通 NAS MySQL、Qdrant、Elasticsearch 和 TEI 的真实联调
- 等待 `embedding` 首次下载 `BAAI/bge-large-zh-v1.5` 完成后，再做向量召回验证
- 后续可以继续验证后端问数接口和前端页面联动
- 当前这个 WSL 里 `docker` 命令不可用，需要先在 Docker Desktop 里打开当前发行版的 WSL Integration 才能继续容器层验证
- 已验证 mock 模式下 `main.openapi()` 仍然有 `/api/query`
- 已验证 mock 模式下 SSE 事件流能输出 progress 事件
- 已调整 mock 模式为轻启动链路，避免因为真实路由和外部客户端导入而被 `omegaconf` / `qdrant_client` / `elasticsearch` / `asyncmy` 等缺失依赖卡住

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
6. 启动 `docker/docker-compose.nas.yaml`
7. 再启动后端与前端
8. 继续验证 `/api/query` 的问数效果

## 验证点

- `uv run fastapi dev main.py` 可启动
- `main.app.openapi()` 可以看到 `/api/query`
- `http://127.0.0.1:8000/docs` 可访问
- `pnpm dev` 可启动前端
- `/api/query` 可返回 SSE
- `meta.table_info` / `meta.column_info` / `meta.metric_info` / `dw.fact_order` 都有数据
