# LangGraph 企业级实战手册（2026版）

> 从 LangChain 基础开发者成长为企业级 Agent 开发工程师
>
> 说明：本文是 LangGraph 专题手册，侧重概念、结构和学习路径。当前 `ai-lab` 中 LangGraph 的实际落地与可运行示例，以 [2026补齐实施状态.md](./2026补齐实施状态.md) 为准。

适合：

- Java开发者
- Python开发者
- AI Agent开发者
- 日本SES工程师
- 企业知识库开发者

---

# 第一章 LangGraph 为什么重要

## LangChain 时代

```text
User
↓
AgentExecutor
↓
Tool
↓
Answer
```

问题：

- 流程不可视化
- 状态管理困难
- 多Agent困难

---

## LangGraph 时代

```text
State
↓
Node
↓
Router
↓
Checkpoint
↓
Memory
```

优势：

- 工作流可视化
- 支持复杂流程
- 支持多Agent
- 支持审批流

---

# 第二章 StateGraph

核心：

```python
StateGraph(State)
```

State保存：

- 用户问题
- 检索结果
- Tool结果
- Agent状态

---

# 第三章 Node

Node 本质：

```python
def node(state):
    return state
```

常见节点：

- AgentNode
- ToolNode
- SearchNode
- RAGNode
- ReviewNode

---

# 第四章 Edge

普通流程：

```text
START
↓
Agent
↓
END
```

---

# 第五章 Conditional Edge

根据条件选择路线：

```text
Router
├─ Search
├─ Tool
└─ RAG
```

适用于：

- 企业知识库
- Deep Research
- Multi-Agent

---

# 第六章 Checkpoint

作用：

断点恢复。

企业场景：

- 长任务执行
- 审批流程
- Agent中断恢复

推荐：

SQLite Checkpoint

PostgreSQL Checkpoint

---

# 第七章 Memory

## 短期记忆

会话级别。

---

## 长期记忆

用户偏好。

企业资料。

知识库。

---

# 第八章 Human In The Loop

企业必备。

示例：

```text
Agent
↓
生成邮件
↓
人工确认
↓
发送
```

---

# 第九章 ToolNode

统一工具调用。

示例：

- Search
- GitHub
- Gmail
- Database

---

# 第十章 Multi-Agent

## Supervisor

统一调度。

---

## Planner

制定计划。

---

## Worker

执行任务。

---

## Reviewer

检查结果。

---

# 第十一章 企业知识库 Agent

架构：

PDF
↓
Loader
↓
Chunk
↓
Embedding
↓
VectorStore
↓
Retriever
↓
LangGraph

---

# 第十二章 Deep Research Agent

流程：

问题
↓
搜索
↓
网页抓取
↓
总结
↓
报告

推荐项目：

Open Deep Research

---

# 第十三章 MCP Server 开发

实现：

- Tool注册
- Tool发现
- Tool调用

支持：

- GitHub
- Gmail
- Slack
- Notion

---

# 第十四章 MCP + LangGraph

企业标准架构：

```text
LangGraph
↓
MCP Client
↓
MCP Servers
```

---

# 第十五章 日本SES营业Agent

功能：

- JD分析
- 简历分析
- 技能匹配
- 自动推荐

技术栈：

LangGraph
+
MCP
+
RAG

---

# 第十六章 面试Agent

输入：

- 简历
- 案件

输出：

- 自我介绍
- 面试题
- 模拟面试

---

# 第十七章 企业办公Agent

功能：

- Gmail
- Calendar
- Notion
- Slack

---

# 第十八章 企业客服Agent

功能：

- FAQ
- 知识库
- 工单系统

---

# 第十九章 项目包装建议

简历可写：

1. 企业知识库Agent
2. Deep Research Agent
3. MCP办公Agent
4. 日本SES营业Agent

---

# 第二十章 2026面试重点

必须掌握：

- LangGraph
- MCP
- RAG 2.0
- Multi-Agent
- Tool Calling
- Structured Output

---

# 推荐成长路线

第1个月

LangChain 1.x

---

第2个月

高级RAG

---

第3个月

LangGraph

---

第4个月

MCP

---

第5个月

Multi-Agent

---

第6个月

企业项目

---

# 最终目标

独立开发：

- 企业知识库
- Deep Research Agent
- MCP Agent
- Multi-Agent系统

达到企业级 Agent 开发水平。
