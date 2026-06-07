# Container Demo

这个 demo 演示一个最小可容器化的 Python 服务。

## 你会学到什么

- 如何用 Dockerfile 打包一个简单服务
- 如何用环境变量配置服务行为
- 如何用 docker compose 启动一个最小服务

## 运行方式

本地直接运行：

```bash
python3 app.py
```

容器运行：

```bash
docker build -t agent-advanced-container-demo .
docker run --rm -p 8088:8088 -e APP_NAME="agent-advanced-demo" agent-advanced-container-demo
```

## 目录结构

```text
container_demo/
├── app.py
├── Dockerfile
└── docker-compose.yml
```
