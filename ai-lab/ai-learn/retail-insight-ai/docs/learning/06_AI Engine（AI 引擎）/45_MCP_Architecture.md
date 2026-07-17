
# Retail Insight AI 企业源码架构手册

# Volume 06：AI Engine（AI 引擎）

# Chapter 45

# MCP Architecture（Model Context Protocol）

> Connect AI Models with Enterprise Tools

---

# 文档信息

| 项目     | 内容                              |
| -------- | --------------------------------- |
| Volume   | 06                                |
| Chapter  | 45                                |
| 技术主题 | MCP Architecture                  |
| 难度     | ⭐⭐⭐⭐⭐                        |
| 推荐程度 | ⭐⭐⭐⭐⭐                        |
| 对应源码 | backend/app/workflow/（未来扩展） |

---

# 学习目标

阅读本章后，你应该能够回答：

- 什么是 MCP（Model Context Protocol）？
- MCP 与 Function Calling 有什么区别？
- MCP Server 与 MCP Client 分别负责什么？
- ERIP 如何接入 MCP？
- 企业 AI 为什么越来越采用 MCP？

---

# 一、为什么需要 MCP？

LLM：

本身：

只能：

生成文本。

例如：

```text
"请帮我读取销售报表"
```

LLM：

知道：

应该：

读取。

但是：

不会：

真正：

打开：

文件。

因此：

需要：

Tool。

传统：

每个 Tool：

都需要：

自己：

写接口。

越来越复杂。

所以：

OpenAI、Anthropic 等提出：

**Model Context Protocol（MCP）**。

---

# 二、什么是 MCP？

MCP：

Model Context Protocol

模型上下文协议。

它的目标：

不是：

替代：

LLM。

而是：

统一：

LLM

与

外部工具

之间：

通信方式。

可以理解为：

```text
USB

对于电脑

=

MCP

对于 AI
```

统一接口。

统一调用。

统一返回。

---

# 三、MCP 架构

典型结构：

```text
LLM

↓

MCP Client

↓

MCP Server

↓

Tools

Filesystem

Database

GitHub

Slack

Browser

REST API
```

LLM：

不用：

知道：

工具：

如何实现。

只需要：

调用：

MCP。

---

# 四、ERIP 当前实现（Current）

当前：

Workflow：

直接：

调用：

Provider。

未来：

建议：

增加：

```text
Workflow

↓

MCP Client

↓

Tool

↓

Result

↓

Workflow
```

Workflow：

统一：

访问：

所有：

外部能力。

---

# 五、源码目录结构 ⭐

建议：

未来：

增加：

```text
backend/app/mcp/

    client.py

    server.py

    registry.py

    tools/

        filesystem.py

        database.py

        github.py

        web_search.py
```

形成：

完整：

MCP 子系统。

---

# 六、关键源码文件 ⭐

未来：

重点：

```text
client.py

↓

ToolRegistry

↓

ToolExecutor

↓

ToolResult
```

Workflow：

只调用：

MCP Client。

---

# 七、MCP 调用流程 ⭐

```text
Workflow

↓

Need Tool

↓

MCP Client

↓

MCP Server

↓

Tool Execute

↓

Result

↓

Workflow Continue
```

LLM：

并不会：

直接：

访问：

数据库。

---

# 八、Tool Registry ⭐

企业：

不会：

把：

Tool：

写死。

通常：

维护：

统一：

Registry。

例如：

```text
Filesystem

Database

GitHub

Slack

Search

Email
```

Workflow：

按名称：

调用。

---

# 九、Retail Insight AI 实施方案 ⭐

未来：

建议：

Workflow：

增加：

Node：

```text
Need Data

↓

MCP

↓

Database Tool

↓

Workflow
```

或者：

```text
Need Document

↓

Filesystem Tool

↓

Workflow
```

以后：

增加：

任何：

Tool。

Workflow：

无需：

修改。

---

# 十、Approval 与 MCP ⭐

企业：

不会：

允许：

LLM：

直接：

执行：

所有：

Tool。

例如：

```text
Delete Database

↓

Approval

↓

Execute
```

高风险：

Tool：

必须：

审批。

---

# 十一、Audit Log ⭐

所有：

MCP：

调用：

建议：

记录：

```text
Time

↓

Tool Name

↓

User

↓

Arguments

↓

Result

↓

Duration
```

方便：

审计。

---

# 十二、Architecture Thinking ⭐

为什么：

不用：

直接：

调用：

Python？

因为：

Workflow：

越来越复杂。

Tool：

越来越多。

统一：

MCP：

更容易：

扩展。

---

# 十三、Current vs Enterprise

Current：

```text
Workflow

↓

Provider
```

Enterprise：

```text
Workflow

↓

MCP

↓

Tool Registry

↓

Filesystem

↓

Database

↓

GitHub

↓

Slack
```

---

# 十四、Java / Spring 对照 ⭐

| Retail Insight AI | Java           |
| ----------------- | -------------- |
| MCP Client        | Tool Client    |
| Tool Registry     | Bean Registry  |
| Tool              | Service        |
| Workflow          | Process Engine |

---

# 十五、VS Code 阅读路线 ⭐

建议：

未来：

```text
workflow/

↓

mcp/

↓

registry.py

↓

tools/
```

观察：

Workflow：

如何：

调用：

Tool。

---

# 十六、Debug Guide ⭐

建议：

断点：

```text
① Workflow

↓

② MCP Client

↓

③ Tool Execute

↓

④ Result

↓

⑤ Workflow Continue
```

观察：

Tool：

执行：

全过程。

---

# 十七、Performance & Cost ⭐

企业：

建议：

统计：

```text
Tool Count

↓

Average Latency

↓

Error Rate

↓

Retry Count

↓

Timeout
```

MCP：

不仅：

关注：

功能。

更关注：

稳定性。

---

# 十八、企业扩展（Enterprise）

未来：

建议：

增加：

```text
Tool Permission

↓

Approval

↓

Audit Log

↓

Retry

↓

Timeout

↓

Circuit Breaker
```

形成：

企业：

Tool Platform。

---

# 十九、面试回答（中文）

什么是 MCP？

MCP（Model Context Protocol）是一种开放协议，用于统一 AI 模型与外部工具之间的通信。通过 MCP，LLM 可以访问数据库、文件系统、GitHub 等资源，而业务系统无需针对每种模型分别开发工具接口，从而提升系统的扩展性和可维护性。

---

# 二十、面试回答（日文）

MCP とは何ですか。

MCP（Model Context Protocol）は、LLM と外部ツールを接続するための共通プロトコルです。ファイルシステム、データベース、GitHub などを統一的に利用できるため、企業向け AI システムで注目されています。

---

# 二十一、日本 SES 常见追问

### Q：MCP 和 Function Calling 有什么区别？

| Function Calling | MCP                  |
| ---------------- | -------------------- |
| 单模型能力       | 跨模型统一协议       |
| SDK 相关         | 开放标准             |
| 工具数量有限     | 可扩展 Tool Registry |
| 偏单应用         | 偏企业平台           |

---

# 二十二、本章练习 ⭐

完成下面练习：

① 设计：

Retail Insight AI

MCP Tool Registry。

↓

② 设计：

Filesystem Tool。

↓

③ 设计：

Database Tool。

↓

④ 思考：

哪些 Tool

必须：

Approval？

---

# 二十三、本章核心记忆图 ⭐

```text
Workflow

↓

MCP Client

↓

MCP Server

↓

Tool Registry

↓

Filesystem

Database

GitHub

↓

Result

↓

Workflow
```

---

# 二十四、本章总结

一句话：

```text
LLM

负责推理

↓

MCP

负责连接工具

↓

Tool

负责执行
```

MCP 的核心价值在于：

**为 AI 与企业系统之间建立统一的工具调用标准。**

对于 Retail Insight AI 来说，未来引入 MCP 后，可以将数据库、文件系统、GitHub、审批系统等统一纳入 AI Workflow，实现真正的 Enterprise AI Platform。

---

# 下一章

**Chapter 46：Multi-Agent（多 Agent 协作）**

学习：

- Supervisor
- Research Agent
- Planning Agent
- Report Agent
- Agent Communication
- Enterprise AI Team
