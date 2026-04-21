# vscode_study 工作区入口

这个目录是当前学习工作区的总入口。

🚀 **新用户？从这里开始**: [QUICK_START_NAVIGATION.md](QUICK_START_NAVIGATION.md) — 30 秒进入开发状态 + 完整项目地图

它的作用是：

- 说明这个工作区里有哪些主学习线
- 给出每条主线最适合先看的入口文档

## 当前主学习线

### 1. LLM 应用开发主线

如果你的目标是贴近日本 IT 现场、企业 PoC 和派遣案件要求，建议优先看：

- [llm-lab/README.md](D:/dev/source_code/vscode_study/llm-lab/README.md)

这条线重点是：

- 模型调用
- 结构化输出
- `RAG / 社内検索`
- `FastAPI`
- 企业集成
- 评估与运维

### 2. Agent 进阶主线

如果你已经有了 `LLM 应用开发` 基础，再继续看：

- [agent-lab/README.md](D:/dev/source_code/vscode_study/agent-lab/README.md)

这条线重点是：

- Tool Calling
- 单 Agent
- 多 Agent
- 工作流

### 3. 对日 Java 开发主线

如果你的目标是传统对日项目开发、Java、文档、流程和测试，建议看：

- [java-lab/README.md](D:/dev/source_code/vscode_study/java-lab/README.md)

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

- [devops-lab/README.md](D:/dev/source_code/vscode_study/devops-lab/README.md)

## 推荐查看顺序

如果你现在主要想学生成 AI 并贴日本现场：

1. [llm-lab/README.md](D:/dev/source_code/vscode_study/llm-lab/README.md)
2. [llm-lab/projects/README.md](D:/dev/source_code/vscode_study/llm-lab/projects/README.md)
3. [agent-lab/README.md](D:/dev/source_code/vscode_study/agent-lab/README.md)

如果你现在主要想学对日 Java 开发：

1. [java-lab/README.md](D:/dev/source_code/vscode_study/java-lab/README.md)

如果你现在主要想补 `DevOps / SRE`：

1. [devops-lab/README.md](D:/dev/source_code/vscode_study/devops-lab/README.md)

## 当前目录概览

```text
vscode_study/
|-- llm-lab/          # LLM 应用开发主线
|-- agent-lab/        # Agent 进阶专题
|-- java-lab/         # 对日 Java 开发主线
|-- devops-lab/       # DevOps / SRE 补充主线
|-- java-projects/    # Java 项目实战
|-- python-projects/  # Python 项目
|-- web-projects/     # Web 项目
|-- sap-lab/          # SAP 学习资料
`-- scripts/          # 脚本和工具
```

## 使用建议

- 先选一条主线，不要多个方向同时发散。
- 如果你的目标是日本现场生成 AI 开发，优先顺序是：
  - `llm-lab`
  - `agent-lab`
- 如果你的目标是传统对日系统开发，优先看：
  - `java-lab`
