# 非 Java 项目最短启动清单

这个清单只列工作区里最常跑的非 Java 项目，以及最短启动方式。

## 1. Python AI 学习项目

目录：`python-projects/ai-lab`

最短启动：

```bash
cd python-projects/ai-lab
./setup.sh
source .venv/bin/activate
python 01_python_basics.py
```

如果要跑 Jupyter：

```bash
source .venv/bin/activate
jupyter notebook
```

前置条件：Python、pip、Jupyter 相关扩展。

## 2. Agent Lab

目录：`agent-lab/projects/<demo>`

最短启动：

```bash
cd agent-lab/projects/chat_cli
bash run_demo.sh
```

其它 demo 也同样使用 `bash run_demo.sh`。

前置条件：Python 3.10+、`OPENAI_API_KEY`。

## 3. LLM Lab

目录：`llm-lab`

这个目录本身主要是学习文档，真正可运行的 demo 现在集中在 `agent-lab/projects`。

## 4. Web Projects

目录：`web-projects/examples/*`

最短启动：

```bash
cd web-projects/examples/vue_hello
npm install
npm run dev
```

同类项目还包括：

- `react_hello`
- `next_hello`
- `angular_hello`

前置条件：Node.js、npm、ESLint、Prettier、Vue 或 Angular 扩展。

## 5. Web Project Samples

目录：`web-projects/sample/*`

典型启动方式：先进入前端或后端子目录，再分别运行 `npm install` 和 `npm run dev`。

例如 React + Node 结构通常是：

```bash
cd web-projects/sample/react-node-demo/client
npm install
npm run dev
```

服务端通常在另一个终端里启动。

## 6. DevOps Lab

目录：`devops-lab`

最短启动通常依赖 Docker、kubectl、kind/k3d 或 GitHub Actions 本地流程。

常见命令：

```bash
docker compose up --build
```

或者 Kubernetes 练习：

```bash
kind create cluster --name devops-lab
kubectl apply -f <yaml-file>
```

前置条件：Docker、kubectl、YAML 支持。

如果当前 WSL 里还没有 `docker`，先看：[docs/docker-wsl-quickstart.md](docs/docker-wsl-quickstart.md)

## 7. LocalStack Lab

目录：`localstack-lab`

最短启动：

```bash
cd localstack-lab
./scripts/bootstrap.sh
source .venv/bin/activate
python projects/hello-localstack/main.py
```

前置条件：Docker、LocalStack CLI、AWS CLI 或 boto3 相关依赖。

当前状态：LocalStack CLI 已安装；剩下的关键阻塞仍是 WSL 里的 Docker 可用性。

如果 `docker` 还不可用，先看：[docs/docker-wsl-quickstart.md](docs/docker-wsl-quickstart.md)

## 8. SAP Lab

目录：`sap-lab`

最短启动：

```bash
cd sap-lab
./scripts/bootstrap.sh
```

`hello-sap` 是最小练习入口，但 ABAP/CDS/RAP/CAP 大多还是学习资料和 SAP 工具链验证内容，不是纯本地单机 runtime。

## 建议顺序

如果你想先跑最容易成功的项目，建议按下面顺序：

1. `python-projects/ai-lab`
2. `web-projects/examples/vue_hello`
3. `agent-lab/projects/chat_cli`
4. `localstack-lab`
5. `devops-lab`

## 备注

- 这个清单不包含 Java 项目。
- 需要 OpenAI API Key 的 demo，不设置环境变量就不会跑通。
- 依赖 Docker 的项目，在 WSL 里必须先让 Docker Desktop 的 WSL integration 生效。