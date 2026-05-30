# 快速启动导航

> 目标：30 秒内知道该打开哪个目录、看哪份文档、运行哪个示例。

## 先看这里

| 你现在想做什么 | 入口 |
| --- | --- |
| 学 LLM 应用、模型调用、RAG、FastAPI | [ai-lab/llm-lab/README.md](ai-lab/llm-lab/README.md) |
| 学 Agent、Tool Calling、工作流、多 Agent | [ai-lab/agent-lab/README.md](ai-lab/agent-lab/README.md) |
| 学对日 Java、SQL、文档、测试、Spring Boot | [java-lab/README.md](java-lab/README.md) |
| 跑 Java 实战项目 | [java-projects/README.md](java-projects/README.md) |
| 学 Web 前端、企业站、WordPress、报价、SEO | [web-projects/README.md](web-projects/README.md) |
| 学 Docker、CI/CD、Kubernetes、运维自动化 | [devops-lab/README.md](devops-lab/README.md) |
| 学 SAP ABAP / CDS / RAP / CAP | [sap-lab/README.md](sap-lab/README.md) |
| 学 AWS 本地模拟 | [localstack-lab/README.md](localstack-lab/README.md) |
| 查 WSL、VS Code、GitHub、Aider、OpenClaw 教程 | [softbs/README.md](softbs/README.md) |
| 查脚本工具 | [scripts/README.md](scripts/README.md) |

## 工作区地图

```text
vscode_study/
  README.md                       # 工作区总入口
  QUICK_START_NAVIGATION.md       # 快速启动导航
  ai-lab/                         # 生成 AI 学习总入口
    llm-lab/                      # LLM 应用工程
    agent-lab/                    # AI Agent 工作流
  java-lab/                       # 对日 Java 学习线
  java-projects/                  # Java 项目实战
  web-projects/                   # Web、前端、企业站、WordPress
  devops-lab/                     # Docker / CI/CD / K8s
  sap-lab/                        # SAP 学习空间
  localstack-lab/                 # AWS 本地模拟实验
  python-projects/                # Python 历史/补充项目
  scripts/                        # WSL、Docker、LocalStack、部署脚本
  softbs/                         # 软件、环境、AI 编程工具教程库
  docs/                           # 工作区环境和运行说明
```

## 最短启动命令

### LLM / Agent

无 API Key 也能先用 mock 模式跑：

```bash
python3 ai-lab/agent-lab/projects/chat_cli/main.py --mock "你好，帮我总结这个项目"
```

有 `OPENAI_API_KEY` 时再切到真实调用：

```bash
OPENAI_API_KEY=sk-... python3 ai-lab/agent-lab/projects/chat_cli/main.py --real "请总结这个项目"
```

### LLM Lab 示例

```bash
cd ai-lab/llm-lab/examples
python3 model_call_example.py --mock "请用一句话解释 RAG"
python3 text_split_example.py
python3 pydantic_example.py
```

### Java 项目

```bash
cd java-projects/JtProject
./mvnw spring-boot:run
```

### Web 示例

```bash
cd web-projects/examples/react_hello
npm install
npm run dev
```

更多 Web 示例见：

- [web-projects/examples/README.md](web-projects/examples/README.md)
- [web-projects/sample/README.md](web-projects/sample/README.md)

### DevOps / LocalStack

```bash
# DevOps 命令速查
cat devops-lab/QUICK_REFERENCE.md

# LocalStack 命令速查
cat localstack-lab/QUICK_REFERENCE.md
```

## 关键文档

### 环境与运行

- [docs/workspace-env-setup.md](docs/workspace-env-setup.md)
- [docs/workspace-run-guide.md](docs/workspace-run-guide.md)
- [docs/vscode-plugin-list.md](docs/vscode-plugin-list.md)
- [softbs/vscode/UM890Pro_Win11_WSL2_Docker_Java_Python_本地模型辅助开发教程.md](softbs/vscode/UM890Pro_Win11_WSL2_Docker_Java_Python_本地模型辅助开发教程.md)
- [softbs/vscode/Win11_WSL_VSCode_Java_Python_快速开发指南.md](softbs/vscode/Win11_WSL_VSCode_Java_Python_快速开发指南.md)

### 生成 AI

- [ai-lab/README.md](ai-lab/README.md)
- [ai-lab/llm-lab/README.md](ai-lab/llm-lab/README.md)
- [ai-lab/agent-lab/README.md](ai-lab/agent-lab/README.md)
- [ai-lab/agent-lab/LLM-Agent学习路径与计划.md](ai-lab/agent-lab/LLM-Agent学习路径与计划.md)

### Web / 前端 / 企业站

- [web-projects/README.md](web-projects/README.md)
- [web-projects/examples/README.md](web-projects/examples/README.md)
- [web-projects/sample/README.md](web-projects/sample/README.md)

### Java / DevOps / SAP

- [java-lab/README.md](java-lab/README.md)
- [java-projects/README.md](java-projects/README.md)
- [devops-lab/README.md](devops-lab/README.md)
- [devops-lab/QUICK_REFERENCE.md](devops-lab/QUICK_REFERENCE.md)
- [sap-lab/README.md](sap-lab/README.md)
- [sap-lab/LEARNING_GUIDE.md](sap-lab/LEARNING_GUIDE.md)

## 推荐学习顺序

### 生成 AI / 日本现场 PoC

1. [ai-lab/llm-lab/README.md](ai-lab/llm-lab/README.md)
2. [ai-lab/llm-lab/examples/README.md](ai-lab/llm-lab/examples/README.md)
3. [ai-lab/agent-lab/README.md](ai-lab/agent-lab/README.md)
4. `ai-lab/agent-lab/projects/chat_cli`
5. `ai-lab/agent-lab/projects/rag_api_demo`

### Web / 前端

1. [web-projects/README.md](web-projects/README.md)
2. [web-projects/examples/README.md](web-projects/examples/README.md)
3. `web-projects/examples/typescript_hello`
4. `web-projects/examples/react_hello` / `vue_hello` / `angular_hello` / `next_hello`
5. [web-projects/sample/README.md](web-projects/sample/README.md)

### 对日 Java

1. [java-lab/README.md](java-lab/README.md)
2. [java-projects/README.md](java-projects/README.md)
3. `java-projects/JtProject`
4. [devops-lab/README.md](devops-lab/README.md)

## 常见问题

| 问题 | 看哪里 |
| --- | --- |
| 不知道先学哪个方向 | 本文件的“先看这里” |
| 没有 OpenAI API Key | `model_call_example.py --mock` 或 `chat_cli --mock` |
| IDEA / VS Code 到底是否连 WSL | [README.md](README.md) 的 WSL / IDEA 说明 |
| Web 项目太多不知道哪个是哪个 | [web-projects/README.md](web-projects/README.md) |
| sample 和 examples 区别不清楚 | [web-projects/sample/README.md](web-projects/sample/README.md) |
| 本地环境要装什么 | [docs/workspace-env-setup.md](docs/workspace-env-setup.md) |

## 一句话速记

```text
AI 看 ai-lab，Web 看 web-projects，Java 看 java-lab/java-projects，环境看 softbs/vscode，脚本看 scripts。
```
