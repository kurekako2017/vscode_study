# docker-compose 最小监控栈演练页

## 1. 这篇是干什么的

[12-Prometheus_Grafana最小入门.md](D:/dev/source_code/vscode_study/devops-lab/12-Prometheus_Grafana%E6%9C%80%E5%B0%8F%E5%85%A5%E9%97%A8.md) 讲的是最小监控栈怎么理解。

这一篇继续往前走一步：

- 不只是看概念
- 不只是读配置
- 而是直接跑一个最小 `docker-compose` 监控栈

这个演练页对应的模板目录在这里：

- [prometheus-grafana-demo/README.md](D:/dev/source_code/vscode_study/devops-lab/templates/prometheus-grafana-demo/README.md)

## 2. 这个最小栈包含什么

这套模板里有 3 个容器：

- 一个 `demo-app`
- 一个 `Prometheus`
- 一个 `Grafana`

职责分别是：

- `demo-app`：暴露一个简单 HTTP 接口和 `/metrics`
- `Prometheus`：定时抓取 `demo-app` 指标
- `Grafana`：连接 `Prometheus`，用于查看指标

也就是说，这次不是空讲：

- 指标是谁暴露的
- 谁来抓
- 谁来展示

而是把这 3 步真正连起来。

## 3. 对应模板文件

模板目录：

- [templates/prometheus-grafana-demo/README.md](D:/dev/source_code/vscode_study/devops-lab/templates/prometheus-grafana-demo/README.md)
- [templates/prometheus-grafana-demo/docker-compose.yml](D:/dev/source_code/vscode_study/devops-lab/templates/prometheus-grafana-demo/docker-compose.yml)
- [templates/prometheus-grafana-demo/prometheus/prometheus.yml](D:/dev/source_code/vscode_study/devops-lab/templates/prometheus-grafana-demo/prometheus/prometheus.yml)
- [templates/prometheus-grafana-demo/app/app.py](D:/dev/source_code/vscode_study/devops-lab/templates/prometheus-grafana-demo/app/app.py)
- [templates/prometheus-grafana-demo/app/requirements.txt](D:/dev/source_code/vscode_study/devops-lab/templates/prometheus-grafana-demo/app/requirements.txt)
- [templates/prometheus-grafana-demo/app/Dockerfile](D:/dev/source_code/vscode_study/devops-lab/templates/prometheus-grafana-demo/app/Dockerfile)

## 4. 你会练到什么

跑完这套模板，至少能建立这些直觉：

- 一个应用怎么暴露指标
- `Prometheus` 是怎么找到抓取目标的
- `Grafana` 虽然还没预置 dashboard，但已经是可连接的数据可视化入口
- 监控平台不是替代日志，而是给你更持续的观察能力

## 5. 最小运行步骤

进入模板目录后运行：

```bash
docker compose up --build
```

启动后可以看这几个地址：

- `demo-app`：`http://127.0.0.1:8000`
- `demo-app metrics`：`http://127.0.0.1:8000/metrics`
- `Prometheus`：`http://127.0.0.1:9090`
- `Grafana`：`http://127.0.0.1:3000`

默认 `Grafana` 登录：

- 用户名：`admin`
- 密码：`admin`

## 6. 最小验证动作

建议按这个顺序验证：

1. 先访问 `http://127.0.0.1:8000`
2. 再访问 `http://127.0.0.1:8000/metrics`
3. 打开 `Prometheus` 看 target 是否为 `UP`
4. 打开 `Grafana`，手动添加 `Prometheus` 数据源

如果你只做到了前 3 步，也已经算跑通了最小链路。

## 7. 你应该重点看哪里

第一次练，不要试图一下子理解所有文件。

优先看这 3 个点：

### 看 `docker-compose.yml`

重点理解：

- 一共起了几个服务
- 端口怎么映射
- `Prometheus` 配置是怎么挂进去的

### 看 `prometheus.yml`

重点理解：

- `scrape_interval`
- `job_name`
- `targets`

### 看 `app.py`

重点理解：

- 应用为什么会有 `/metrics`
- 指标是怎么被定义的
- 请求次数为什么能被统计

## 8. 最小排障思路

如果没跑起来，先按这个顺序查：

1. `docker compose ps`
2. `docker compose logs demo-app`
3. `docker compose logs prometheus`
4. `docker compose logs grafana`

最常见的问题通常是：

- 本地端口冲突
- Docker 没启动
- 镜像拉取失败
- `Prometheus` target 地址写错

## 9. 练习题

### 练习 1：确认链路

用自己的话写清楚：

- 指标从哪里来
- 被谁抓
- 被谁展示

### 练习 2：改一个指标名字

在 `app.py` 里改一个指标名字，再重新构建运行。

### 练习 3：加一个业务计数

例如给 `/hello` 路由加一个单独计数器。

### 练习 4：给 Grafana 手动接 Prometheus 数据源

哪怕先不做 dashboard，也要知道数据源是怎么接上的。

## 10. 过关标准

学完这一页，至少要达到：

- 你能本地启动这套 `docker-compose` 最小监控栈
- 你能打开 `/metrics`
- 你能在 `Prometheus` 里看到 target 为 `UP`
- 你能解释这 3 个容器分别做什么

## 11. 下一步学什么

这一步之后，最自然的后续有两个方向：

- 方向 1：给 `Grafana` 再补一个最小 dashboard 模板
- 方向 2：给 `Prometheus` 再补一个 `node_exporter` 或 `cadvisor` 示例

如果你继续沿当前主线走，建议下一步优先补方向 1。
