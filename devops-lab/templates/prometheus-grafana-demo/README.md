# prometheus-grafana-demo

最小可运行的 `Prometheus + Grafana + demo-app` 练习模板。

这个模板解决的问题是：

- 用一个最小应用暴露 `/metrics`
- 用 `Prometheus` 抓取这个应用的指标
- 用 `Grafana` 连接 `Prometheus`

## 文件结构

```text
prometheus-grafana-demo/
|-- docker-compose.yml
|-- README.md
|-- app/
|   |-- app.py
|   |-- Dockerfile
|   `-- requirements.txt
`-- prometheus/
    `-- prometheus.yml
```

## 启动

在当前目录运行：

```bash
docker compose up --build
```

## 访问地址

- `demo-app`：`http://127.0.0.1:8000`
- `demo-app metrics`：`http://127.0.0.1:8000/metrics`
- `Prometheus`：`http://127.0.0.1:9090`
- `Grafana`：`http://127.0.0.1:3000`

## Grafana 默认登录

- 用户名：`admin`
- 密码：`admin`

## 最小验证

建议按这个顺序检查：

1. 打开 `http://127.0.0.1:8000`
2. 打开 `http://127.0.0.1:8000/metrics`
3. 打开 `Prometheus`，确认 target 是 `UP`
4. 打开 `Grafana`，手动添加 `Prometheus` 数据源

## 停止

```bash
docker compose down
```

如果连卷一起清掉：

```bash
docker compose down -v
```

## 你可以先改什么

- 改 `app.py` 里的欢迎消息
- 改指标名字
- 给应用多加一个路由
- 给 `Prometheus` 多加一个 job

## 对应教程

- [11-监控与可观测性入口.md](D:/dev/source_code/vscode_study/devops-lab/11-%E7%9B%91%E6%8E%A7%E4%B8%8E%E5%8F%AF%E8%A7%82%E6%B5%8B%E6%80%A7%E5%85%A5%E5%8F%A3.md)
- [12-Prometheus_Grafana最小入门.md](D:/dev/source_code/vscode_study/devops-lab/12-Prometheus_Grafana%E6%9C%80%E5%B0%8F%E5%85%A5%E9%97%A8.md)
- [13-docker-compose_最小监控栈演练页.md](D:/dev/source_code/vscode_study/devops-lab/13-docker-compose_%E6%9C%80%E5%B0%8F%E7%9B%91%E6%8E%A7%E6%A0%88%E6%BC%94%E7%BB%83%E9%A1%B5.md)
