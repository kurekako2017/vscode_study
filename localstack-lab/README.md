# LocalStack Lab（本地 AWS 模拟环境练习）

这个目录用于本地隔离地练习基于 LocalStack 的开发，不影响仓库里的其他项目。

包含内容：
- `projects/hello-localstack`：Python 最小示例
- `projects/hello-localstack-java`：Java 最小示例
- `scripts/bootstrap.sh`：创建 `.venv` 并安装 Python 依赖
- `docs/`：记录笔记/踩坑

文档入口：
- [AWS知识点总览（中日对照）](./docs/AWS_Knowledge_Map.md)
- [AWS 系统学习路线（LocalStack 版）](./docs/aws/AWS系统学习路线.md)
- [AWS 单页笔记索引](./docs/aws/README.md)
- [高频架构组合索引](./docs/aws/combos/README.md)

建议学习顺序：
1. 先看系统路线，理解 AWS 的访问入口、计算、网络、数据、消息、权限、监控、IaC 分层。
2. 再按场景学习：Web 部署、异步处理、容器交付、数据分析。
3. 最后用 LocalStack 做 CLI / SDK 实操，重点观察 endpoint、资源名、日志和执行结果。

快速开始（Python 示例）：
1) 在本目录执行 `./scripts/bootstrap.sh`，创建虚拟环境并装依赖。
2) 确保 LocalStack 已启动（如 `localstack start` 或 docker-compose`）。
3) 运行示例：`source .venv/bin/activate && python projects/hello-localstack/main.py`（默认端点 `http://s3.localhost.localstack.cloud:4566`，可用 `LOCALSTACK_ENDPOINT_URL` 覆盖）。

Java 示例：
1) `cd projects/hello-localstack-java`
2) `mvn -q package` 
3) `LOCALSTACK_ENDPOINT_URL=http://s3.localhost.localstack.cloud:4566 mvn -q exec:java`

请将 LocalStack 相关依赖都放在本目录内，避免影响其他项目。
