# Container Demo

这个 demo 演示一个最小可容器化的 Python 服务。

## 业务场景说明

- 适用场景：想把 Python 服务放进统一运行环境，避免本地和线上机器差异带来的问题。
- 如果不用这种方式：不同机器上的依赖和配置很容易不一致，出现“我这边能跑，你那边不行”的情况。
- 解决的问题：用 Dockerfile 和 compose 固化环境，让部署、调试和交付更稳定。

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
