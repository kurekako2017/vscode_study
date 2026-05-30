# vscode_study 工作区入口

这是当前学习工作区的总入口。它把生成 AI、Agent、Java、Web、DevOps、SAP、LocalStack、WSL/VS Code 环境教程放在同一个目录里，方便按学习方向逐步推进。

快速启动请先看：

[QUICK_START_NAVIGATION.md](QUICK_START_NAVIGATION.md)

## 主学习线

| 学习线 | 入口 | 适合目标 |
| --- | --- | --- |
| LLM 应用开发 | [ai-lab/llm-lab/README.md](ai-lab/llm-lab/README.md) | 模型调用、结构化输出、RAG、FastAPI、企业集成 |
| Agent 进阶 | [ai-lab/agent-lab/README.md](ai-lab/agent-lab/README.md) | Tool Calling、单 Agent、多 Agent、工作流 |
| 对日 Java | [java-lab/README.md](java-lab/README.md) | Java、SQL、项目结构、日式文档、测试 |
| Java 项目实战 | [java-projects/README.md](java-projects/README.md) | Spring Boot、前后端项目、部署练习 |
| Web / 企业站 | [web-projects/README.md](web-projects/README.md) | React、Vue、Angular、Next.js、WordPress、企业官网 |
| DevOps / SRE | [devops-lab/README.md](devops-lab/README.md) | Docker、CI/CD、Kubernetes、自动化运维 |
| SAP | [sap-lab/README.md](sap-lab/README.md) | ABAP、CDS、RAP、CAP |
| AWS 本地模拟 | [localstack-lab/README.md](localstack-lab/README.md) | LocalStack、S3、DynamoDB、本地云服务测试 |
| 环境与工具教程 | [softbs/README.md](softbs/README.md) | WSL、VS Code、GitHub、Aider、OpenClaw、本地模型 |
| 脚本工具 | [scripts/README.md](scripts/README.md) | WSL、Docker、LocalStack、部署脚本 |

## 当前目录概览

```text
vscode_study/
  QUICK_START_NAVIGATION.md   # 快速导航
  README.md                   # 本文件
  ai-lab/                     # 生成 AI 学习总入口
    llm-lab/                  # LLM 应用开发
    agent-lab/                # AI Agent 工作流
  java-lab/                   # 对日 Java 学习资料
  java-projects/              # Java 项目实战
  web-projects/               # Web 示例、企业站、WordPress、插件
  devops-lab/                 # Docker / CI/CD / Kubernetes
  sap-lab/                    # SAP 学习资料和项目
  localstack-lab/             # AWS 本地模拟学习
  python-projects/            # Python 历史/补充项目
  scripts/                    # 自动化脚本
  softbs/                     # 软件、环境、AI 编程工具教程
  docs/                       # 工作区环境和运行说明
```

## 推荐查看顺序

### 如果你现在主要想学生成 AI 并贴近日本现场

1. [ai-lab/llm-lab/README.md](ai-lab/llm-lab/README.md)
2. [ai-lab/llm-lab/examples/README.md](ai-lab/llm-lab/examples/README.md)
3. [ai-lab/agent-lab/README.md](ai-lab/agent-lab/README.md)
4. [ai-lab/agent-lab/projects/chat_cli/README.md](ai-lab/agent-lab/projects/chat_cli/README.md)

没有 API Key 时，优先使用 mock 模式：

```bash
python3 ai-lab/agent-lab/projects/chat_cli/main.py --mock "你好，帮我总结"
```

### 如果你现在主要想学 Web / 前端 / 企业站

1. [web-projects/README.md](web-projects/README.md)
2. [web-projects/examples/README.md](web-projects/examples/README.md)
3. [web-projects/sample/README.md](web-projects/sample/README.md)

先从最小示例开始：

```bash
cd web-projects/examples/typescript_hello
npm install
npm run dev
```

### 如果你现在主要想学对日 Java 开发

1. [java-lab/README.md](java-lab/README.md)
2. [java-projects/README.md](java-projects/README.md)
3. [devops-lab/README.md](devops-lab/README.md)

示例启动：

```bash
cd java-projects/JtProject
./mvnw spring-boot:run
```

### 如果你现在主要想补 DevOps / SRE

1. [devops-lab/README.md](devops-lab/README.md)
2. [devops-lab/QUICK_REFERENCE.md](devops-lab/QUICK_REFERENCE.md)
3. [localstack-lab/README.md](localstack-lab/README.md)

## WSL / VS Code / IDEA 建议

建议统一使用 WSL 文件系统中的工作区路径，例如：

```text
/home/victorkure/workspace/vscode_study
```

不要一边用 Windows 路径 `D:\...`，一边用 WSL 路径 `/home/...`。统一路径可以减少依赖安装、终端环境、文件权限和构建缓存问题。

### VS Code

推荐使用 Remote - WSL 打开本工作区：

```bash
cd /home/victorkure/workspace/vscode_study
code .
```

### IntelliJ IDEA / JetBrains Gateway

如果使用 IDEA Remote Development：

1. 打开 `Remote Development`。
2. 选择 `WSL`。
3. 选择 Ubuntu 发行版。
4. 项目路径选择 `/home/victorkure/workspace/vscode_study`。
5. 打开后检查 Terminal 的 `pwd` 是否仍是这个路径。

如果看到的是 `D:\...` 或 `C:\...`，说明当前不是 WSL 内部项目路径。

更详细的环境教程见：

- [softbs/vscode/UM890Pro_Win11_WSL2_Docker_Java_Python_本地模型辅助开发教程.md](softbs/vscode/UM890Pro_Win11_WSL2_Docker_Java_Python_本地模型辅助开发教程.md)
- [softbs/vscode/Win11_WSL_VSCode_Java_Python_快速开发指南.md](softbs/vscode/Win11_WSL_VSCode_Java_Python_快速开发指南.md)
- [docs/workspace-env-setup.md](docs/workspace-env-setup.md)
- [docs/workspace-run-guide.md](docs/workspace-run-guide.md)

## 非 Java 运行入口

如果你想把这个工作区里的非 Java 代码真正跑起来，先看这 3 个文档：

- [全局环境安装说明](docs/workspace-env-setup.md)
- [非 Java 项目最短启动清单](docs/workspace-run-guide.md)
- [VS Code 插件清单](docs/vscode-plugin-list.md)

## 一句话速记

```text
不知道看哪里：先看 QUICK_START_NAVIGATION.md。
AI 看 ai-lab，Web 看 web-projects，Java 看 java-lab/java-projects，环境看 softbs/vscode。
```
