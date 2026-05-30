# vscode_study 工作区入口

这个目录是当前学习工作区的总入口。

🚀 **新用户？从这里开始**: [QUICK_START_NAVIGATION.md](QUICK_START_NAVIGATION.md) — 30 秒进入开发状态 + 完整项目地图

它的作用是：

- 说明这个工作区里有哪些主学习线
- 给出每条主线最适合先看的入口文档

## 当前主学习线

### 1. LLM 应用开发主线

如果你的目标是贴近日本 IT 现场、企业 PoC 和派遣案件要求，建议优先看：

- [ai-lab/llm-lab/README.md](ai-lab/llm-lab/README.md)

这条线重点是：

- 模型调用
- 结构化输出
- `RAG / 社内検索`
- `FastAPI`
- 企业集成
- 评估与运维

### 2. Agent 进阶主线

如果你已经有了 `LLM 应用开发` 基础，再继续看：

- [ai-lab/agent-lab/README.md](ai-lab/agent-lab/README.md)

这条线重点是：

- Tool Calling
- 单 Agent
- 多 Agent
- 工作流

### 3. 对日 Java 开发主线

如果你的目标是传统对日项目开发、Java、文档、流程和测试，建议看：

- [java-lab/README.md](java-lab/README.md)

这条线重点是：

- Java
- 对日项目常用工具
- SQL 与数据库
- 项目结构
- 日式文档与测试资料

### 4. DevOps / SRE 补充主线

如果你想基于当前工作区已有内容补：

- `Docker`
- `CI/CD`
- 自动化运维
- `Kubernetes` 入门

建议看：

- [devops-lab/README.md](devops-lab/README.md)

## 在 IDEA 里确认是否连的是 WSL

如果你的目标是让 IDEA 通过 Remote Development 连接到 WSL，并且和 VS Code + WSL 保持同一套路径，那么重点不是“Windows 还是 WSL 机器”，而是“当前项目是不是在 WSL 文件系统里打开”。

可以这样确认：

- 在 IDEA 首页进入 `Remote Development`，再选择 `WSL` 的 `New Connection`。这表示 IDE 会把开发环境放到 WSL 里，而不是 Windows 本地环境。
- 打开项目后，看项目根路径。如果路径是 `/home/victorkure/workspace/vscode_study`，说明你和 VS Code + WSL 用的是同一个 Linux 路径；如果是 `D:\...`、`C:\...`，那就是 Windows 本地路径。
- 看 Terminal。若默认 shell 是 Linux shell，并且 `pwd` 输出 `/home/victorkure/workspace/vscode_study`，就说明当前终端确实连在 WSL 上。
- 看解释器和 SDK 配置。Python、JDK、Node 等如果指向 WSL 路径，就说明工具链也在 WSL 中。

如果你是为了和 VS Code 的 WSL 开发保持一致，建议统一使用同一个路径，例如 `/home/victorkure/workspace/vscode_study`，不要一边用 `D:\...`，一边用 `/home/...`。这样代码位置、依赖安装和终端环境都会一致。

### 配置步骤

第一步：打开远程开发入口

1. 启动 IntelliJ IDEA，进入 Welcome 欢迎界面。
2. 在左侧菜单栏中点击 `Remote Development`（远程开发）。
3. 找到 `WSL` 选项，点击 `New Connection`（新建连接）。

第二步：选择 WSL 发行版与项目路径

1. `Linux distribution`：在下拉菜单中选择你正在使用的 WSL 子系统，例如 `Ubuntu`。
2. `Project directory`：点击文件夹图标，选择你存储在 WSL 内的项目路径。
3. 注意：请确保项目路径是在 Linux 内部，例如 `/home/victorkure/...`，而不是 `/mnt/c/...`，否则会拖慢文件读写性能。
4. 点击 `Next`。

第三步：下载并启动 IDE 后端

1. `IDE version`：选择你想要在 WSL 内部运行的 IDEA 版本，建议选择最新推荐的 Stable 版本。
2. 点击 `Start IDE and Connect`。
3. 此时，IDEA 会自动在你的 WSL 子系统内部下载、解压并启动一个无界面的 IDE 后端（JetBrains Client Agent）。
4. 下载完成后，Windows 侧会弹出一个专用的轻量级前端窗口（JetBrains Client），之后你就可以像操作本地 IDEA 一样写代码。

💡 进阶技巧：使用 JetBrains Gateway 管理

如果你每次打开 IDEA 都去找远程连接入口，建议下载官方的 JetBrains Gateway 独立软件（也可以通过 JetBrains Toolbox 安装）。

1. 打开 JetBrains Gateway。
2. 同样选择 WSL，它会自动扫描出当前运行的 Linux 子系统。
3. 这样你可以统一管理所有的 WSL、SSH 远程项目，一键即可连接。

## 推荐查看顺序

如果你现在主要想学生成 AI 并贴日本现场：

1. [ai-lab/llm-lab/README.md](ai-lab/llm-lab/README.md)
2. [ai-lab/agent-lab/README.md](ai-lab/agent-lab/README.md)

如果你现在主要想学对日 Java 开发：

1. [java-lab/README.md](java-lab/README.md)

如果你现在主要想补 `DevOps / SRE`：

1. [devops-lab/README.md](devops-lab/README.md)

## 当前目录概览

```text
vscode_study/
|-- ai-lab/          # 生成 AI 学习总入口
|   |-- llm-lab/     # LLM 应用开发主线
|   `-- agent-lab/   # Agent 进阶专题
|-- java-lab/         # 对日 Java 开发主线
|-- devops-lab/       # DevOps / SRE 补充主线
|-- java-projects/    # Java 项目实战
|-- python-projects/  # Python 项目
|-- web-projects/     # Web 项目
|-- sap-lab/          # SAP 学习资料
`-- scripts/          # 脚本和工具
```

## Agent Demos — 快速学习路线

本工作区在 `ai-lab/agent-lab/projects/` 下包含一组教学用的 Python demo，用于示范 RAG、Tool Calling、结构化输出与工作流分阶段设计。每个 demo 的详细学习要点见各自的 `README_LEARN.md`。下面是汇总与快速运行示例：

- `ai-lab/agent-lab/projects/chat_cli/` — Minimal CLI chat demo
  - 快速运行（mock）:
    ```bash
    python3 ai-lab/agent-lab/projects/chat_cli/main.py --mock "你好，帮我总结"
    ```
  - 快速运行（real）:
    ```bash
    OPENAI_API_KEY=sk-... python3 ai-lab/agent-lab/projects/chat_cli/main.py --real "请总结文档"
    ```

- `ai-lab/agent-lab/projects/doc_qa_agent/` — 本地 RAG（文件切分 + 关键词检索）
  - 快速运行（mock）:
    ```bash
    python3 ai-lab/agent-lab/projects/doc_qa_agent/main.py --mock --docs ai-lab "项目简介是什么"
    ```

- `ai-lab/agent-lab/projects/rag_api_demo/` — FastAPI RAG 微服务示例（/ask, /reload, /health）
  - 启动服务（mock）:
    ```bash
    cd ai-lab/agent-lab/projects/rag_api_demo
    RAG_API_MOCK=1 uvicorn main:app --reload --port 8000
    ```
  - 测试接口:
    ```bash
    curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d '{"question":"请总结文档"}'
    ```

- `ai-lab/agent-lab/projects/structured_output_demo/` — 演示 Pydantic 结构化输出解析
  - 快速运行（mock）:
    ```bash
    python3 ai-lab/agent-lab/projects/structured_output_demo/main.py --mock "请生成计划"
    ```

- `ai-lab/agent-lab/projects/tool_agent_demo/` — Tool-calling agent 示例（本地工具：list/read/search）
  - 快速运行（mock）:
    ```bash
    python3 ai-lab/agent-lab/projects/tool_agent_demo/main.py --mock --workdir ai-lab "查找关键字"
    ```

- `ai-lab/agent-lab/projects/workflow_agent/` — 三阶段工作流示例（analyze → plan → finalize）
  - 快速运行（mock）:
    ```bash
    python3 ai-lab/agent-lab/projects/workflow_agent/main.py --mock "请制定发布计划"
    ```

每个项目目录下的 `README_LEARN.md` 包含更多学习建议与练习题，建议先以 mock 模式熟悉行为，再在有 `OPENAI_API_KEY` 的环境切换到 real 测试。

## 使用建议

- 先选一条主线，不要多个方向同时发散。
- 如果你的目标是日本现场生成 AI 开发，优先顺序是：
  - `llm-lab`
  - `agent-lab`
- 如果你的目标是传统对日系统开发，优先看：
  - `java-lab`

## 非 Java 运行入口

如果你想把这个工作区里的非 Java 代码真正跑起来，先看这 3 个文档：

- [全局环境安装说明](docs/workspace-env-setup.md)
- [非 Java 项目最短启动清单](docs/workspace-run-guide.md)
- [VS Code 插件清单](docs/vscode-plugin-list.md)
