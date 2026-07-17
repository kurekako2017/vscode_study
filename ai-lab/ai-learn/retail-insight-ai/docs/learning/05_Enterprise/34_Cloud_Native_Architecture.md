# ERIP 企业源码架构手册

# Volume 05：Enterprise（企业架构）

# 第34章（Chapter 34）

# Cloud Native Architecture（云原生架构）

> Deploy AI Systems for Production

---

# 文档信息

| 项目     | 内容                                |
| -------- | ----------------------------------- |
| Volume   | 05                                  |
| Chapter  | 34                                  |
| 技术主题 | Cloud Native Architecture           |
| 难度     | ⭐⭐⭐⭐⭐                          |
| 推荐程度 | ⭐⭐⭐⭐⭐                          |
| 对应模块 | Docker / Kubernetes / Observability |

---

# 学习目标

阅读本章后，你应该能够回答：

- 什么是 Cloud Native（云原生）？
- 为什么企业 AI 平台都会容器化？
- Docker 与 Kubernetes 分别负责什么？
- 什么是 ConfigMap、Secret？
- 为什么企业需要 OpenTelemetry？

---

# 一、什么是 Cloud Native？

Cloud Native（云原生）不是某一种技术。

它是一种软件开发与部署理念。

目标是：

> **让应用能够快速部署、快速扩展、快速恢复。**

现代企业 AI 平台通常采用：

```text
Docker

↓

Kubernetes

↓

Cloud Platform
```

而不是直接部署到一台服务器。

---

# 二、为什么需要容器化？

传统部署：

```text
Python

↓

pip install

↓

运行
```

容易出现：

- 环境不同
- Python 版本不同
- 依赖冲突
- 部署失败

容器化以后：

```text
Application

↓

Docker Image

↓

Docker Container
```

开发环境与生产环境保持一致。

---

# 三、ERIP 当前实现（Current）

目前项目已经提供：

```text
Docker

↓

docker-compose

↓

Backend

↓

Frontend
```

开发者可以快速启动：

```bash
docker compose up
```

适合：

- 本地开发
- 功能验证
- MVP

---

# 四、Source Binding（源码绑定）

建议阅读：

```text
docker-compose.yml
```

继续：

```text
Dockerfile
```

观察：

Backend

如何打包。

Frontend

如何部署。

---

# 五、Docker 的职责

Docker 负责：

```text
Build

↓

Image

↓

Container
```

例如：

```text
Retail Insight AI

↓

Docker Image

↓

Container
```

同一个 Image：

可以运行：

多个 Container。

---

# 六、为什么需要 Kubernetes？

Docker：

负责：

运行一个容器。

Kubernetes：

负责：

管理大量容器。

例如：

```text
Frontend

Backend

Worker

Redis

RabbitMQ

PostgreSQL
```

全部：

由 Kubernetes：

统一管理。

---

# 七、Kubernetes 核心组件

企业最常见：

```text
Deployment

↓

Pod

↓

Service

↓

Ingress
```

Deployment：

管理版本。

Pod：

运行程序。

Service：

提供访问。

Ingress：

统一入口。

---

# 八、ConfigMap 与 Secret

企业项目：

不会：

把配置写死。

例如：

```text
API URL

↓

ConfigMap
```

而：

```text
API KEY

↓

Secret
```

这样：

可以：

安全管理配置。

---

# 九、Health Check

企业平台：

必须知道：

服务是否正常。

例如：

```text
Health Check

↓

/health

↓

200 OK
```

如果：

失败：

Kubernetes：

自动：

重启。

---

# 十、Rolling Update

升级系统：

不能：

全部停止。

企业：

通常：

采用：

```text
Version1

↓

Version2

↓

逐步替换
```

用户：

几乎：

无感知。

---

# 十一、OpenTelemetry

OpenTelemetry：

负责：

观察：

整个系统。

例如：

```text
Request

↓

Workflow

↓

Database

↓

LLM

↓

Response
```

全部：

记录。

方便：

排查问题。

---

# 十二、Architecture Thinking（架构思考）

为什么：

企业：

不用：

一台服务器？

因为：

服务器：

总会故障。

Cloud Native：

追求：

```text
Fail

↓

Recover

↓

Continue
```

不是：

永远：

不出错。

而是：

快速恢复。

---

# 十三、Current vs Enterprise

当前：

```text
Docker Compose

↓

Backend

↓

Frontend
```

企业版：

```text
Kubernetes

↓

Ingress

↓

API Gateway

↓

Backend

↓

Worker

↓

Redis

↓

RabbitMQ

↓

PostgreSQL
```

形成：

完整：

AI Platform。

---

# 十四、Java / Spring 对照

| Retail Insight AI | Spring Boot       |
| ----------------- | ----------------- |
| Docker            | Docker            |
| docker-compose    | Docker Compose    |
| Kubernetes        | Kubernetes        |
| ConfigMap         | Config Server     |
| OpenTelemetry     | Micrometer + OTel |

---

# 十五、VS Code 阅读路线

建议：

```text
Dockerfile

↓

docker-compose.yml

↓

Backend

↓

Frontend
```

思考：

如果：

迁移：

Kubernetes。

哪些配置需要调整？

---

# 十六、Learning Trace 对应

Cloud Native：

不会：

改变：

Learning Trace。

但：

未来：

可以增加：

```text
Pod-01

↓

Workflow

↓

Completed
```

帮助：

定位：

具体：

Pod。

---

# 十七、企业扩展（Enterprise）

未来建议：

```text
Docker

↓

Kubernetes

↓

Helm

↓

GitHub Actions

↓

ArgoCD

↓

OpenTelemetry

↓

Prometheus

↓

Grafana
```

形成：

完整：

CI/CD

+ Observability。

---

# 十八、面试回答（中文）

为什么企业 AI 平台需要 Kubernetes？

Kubernetes 可以统一管理大量容器，实现自动扩容、自动恢复、滚动更新和服务发现。当 AI Workflow 数量不断增加时，可以通过增加 Pod 和 Worker 快速扩展系统，而无需修改业务代码。

---

# 十九、面试回答（日语）

なぜ Kubernetes を利用するのですか。

Kubernetes はコンテナを自動管理し、スケールアウトや障害復旧を実現できます。AI Workflow が増加しても Pod を追加するだけで処理能力を拡張できるため、多くの企業で採用されています。

---

# 二十、日本 SES 常见追问

### Q：Docker 和 Kubernetes 有什么区别？

Docker：

负责：

运行：

一个容器。

Kubernetes：

负责：

管理：

很多容器。

Docker：

解决：

"怎么运行"

Kubernetes：

解决：

"怎么管理"

---

# 二十一、本章练习

请完成：

① 阅读：

```text
Dockerfile
```

↓

② 阅读：

```text
docker-compose.yml
```

↓

③ 思考：

如果：

增加：

Worker。

Docker Compose：

应该：

如何修改？

↓

④ 思考：

迁移：

Kubernetes：

需要：

增加：

哪些资源？

---

# 二十二、本章核心记忆图

```text
                 User
                   │
                   ▼
               Ingress
                   │
                   ▼
             Kubernetes
         ┌──────┼────────┐
         ▼      ▼        ▼
    Frontend Backend Worker
                     │
         ┌───────────┼──────────┐
         ▼           ▼          ▼
     PostgreSQL    Redis    RabbitMQ
```

---

# 本章总结

一句话：

```text
Docker

负责打包

↓

Kubernetes

负责管理

↓

OpenTelemetry

负责观察
```

Cloud Native Architecture 的核心目标不是简单部署应用，而是**让企业 AI 平台具备持续交付、自动恢复、弹性扩展和可观测能力**，从而满足生产环境对稳定性和可维护性的要求。

---

# 下一章

**Chapter 35：Enterprise AI Architecture（企业 AI 架构）**

学习：

- LangChain
- LangGraph
- RAG
- pgvector
- MCP
- Multi-Agent
- Enterprise AI Platform 总体架构
