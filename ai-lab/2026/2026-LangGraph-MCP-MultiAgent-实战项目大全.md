# 2026 LangGraph + MCP + Multi-Agent 实战项目大全

> 面向企业级 Agent 开发者
>
> 目标：达到日本企业 Agent 项目实战水平

---

# 第一章 Agent 技术演进

## 第一代

Prompt Engineering

```text
User
↓
LLM
↓
Answer
```

---

## 第二代

RAG

```text
User
↓
Retriever
↓
Context
↓
LLM
```

---

## 第三代

Tool Calling

```text
User
↓
LLM
↓
Tool
↓
Answer
```

---

## 第四代

Agent

```text
User
↓
Agent
↓
Tool
↓
Memory
↓
Answer
```

---

## 第五代

LangGraph

```text
State
↓
Node
↓
Router
↓
Checkpoint
```

---

## 第六代

Multi-Agent

```text
Supervisor
├─ Researcher
├─ Coder
└─ Reviewer
```

---

# 第二章 LangGraph 学习路线

## Level 1

单节点 Agent

学习：

- StateGraph
- START
- END

---

## Level 2

Tool Agent

学习：

- ToolNode
- Tool Calling

---

## Level 3

Router

学习：

- Conditional Edge
- Route Logic

---

## Level 4

Memory

学习：

- Checkpointer
- Short-term Memory
- Long-term Memory

---

## Level 5

Human In The Loop

企业审批流。

---

# 第三章 MCP 学习路线

## MCP Client

调用工具。

---

## MCP Server

暴露工具。

---

## Remote MCP

远程工具服务。

---

## Multi MCP

多个 MCP 集成。

示例：

- GitHub
- Gmail
- Slack
- Jira
- Notion

---

# 第四章 Multi-Agent

## Supervisor 模式

```text
Supervisor
↓
Worker
```

---

## Planner 模式

```text
Planner
↓
Workers
```

---

## Review 模式

```text
Coder
↓
Reviewer
```

---

# 第五章 Deep Research Agent

实现流程：

搜索
↓
网页抓取
↓
阅读
↓
总结
↓
生成报告

学习项目：

Open Deep Research

---

# 第六章 企业项目

## 项目1

企业知识库

技术：

LangGraph
+
RAG

---

## 项目2

客服 Agent

技术：

LangGraph
+
Memory
+
Knowledge Base

---

## 项目3

PDF 问答 Agent

技术：

RAG
+
Rerank

---

## 项目4

日本 SES 营业 Agent

功能：

- Gmail
- JD分析
- 简历匹配
- 自动推荐

---

## 项目5

面试 Agent

功能：

- 简历分析
- 案件分析
- 面试题生成

---

## 项目6

GitHub Agent

功能：

- Issue分析
- PR分析
- 自动Review

---

## 项目7

MCP Office Agent

功能：

- Gmail
- Calendar
- Notion
- Slack

---

## 项目8

Deep Research Agent

功能：

- 搜索
- 阅读
- 总结
- 报告

---

# 第七章 GitHub Top 项目

## LangGraph

https://github.com/langchain-ai/langgraph

---

## LangChain

https://github.com/langchain-ai/langchain

---

## Open Deep Research

https://github.com/langchain-ai/open_deep_research

---

## MCP Specification

https://github.com/modelcontextprotocol/specification

---

## Awesome MCP Servers

https://github.com/punkpeye/awesome-mcp-servers

---

# 第八章 日本 Agent 面试准备

重点：

- RAG 原理
- LangGraph
- MCP
- Multi-Agent
- Tool Calling
- Structured Output

常见问题：

1. 什么是 LangGraph？
2. 为什么 LangGraph 替代 AgentExecutor？
3. MCP 与 Tool 的区别？
4. Multi-Agent 如何设计？
5. 如何设计企业知识库？

---

# 第九章 6个月成长路线

第1个月

LCEL + LangChain 1.x

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

企业项目实战

---

# 最终能力

能够独立开发：

- 企业知识库
- 客服 Agent
- Deep Research Agent
- MCP Agent
- Multi-Agent 系统

达到 2026 企业级 Agent 开发水平。
