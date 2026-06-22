# 2026 企业级 Agent 开发资源导航（终极版）

> 适合已经完成 LangChain 基础（Loader、RAG、Retriever、Tool、Agent）的开发者。
>
> 目标：进入 LangGraph、MCP、Multi-Agent、Deep Research Agent 企业实战。
>
> 说明：本文是资源索引，不是完成度清单。当前可运行实现与阶段验收，请以 [2026补齐实施状态.md](./2026补齐实施状态.md) 为准。

---

# 第一部分：哪些内容已经过时

## 不建议投入大量时间

### LangChain 0.x

- initialize_agent
- AgentExecutor 深度研究
- ConversationBufferMemory
- LLMChain
- ConversationChain

原因：

2026 企业项目已全面转向 LangGraph。

这里的“过时”指学习重心迁移，不等于相关概念或历史资料失效。

---

# 第二部分：2026 主流技术栈

```text
LLM
↓
Tool Calling
↓
RAG 2.0
↓
LangGraph
↓
MCP
↓
Multi-Agent
↓
Deep Research
```

---

# 第三部分：官方文档学习顺序

## 第一阶段

LangChain

https://docs.langchain.com/oss/python/langchain/overview

重点：

- Runtime
- Runnable
- Structured Output
- Tool Calling

预计：

1~2周

---

## 第二阶段

LangGraph

https://langchain-ai.github.io/langgraph/

重点：

- State
- Node
- Edge
- Router
- Memory
- Checkpoint

预计：

2~4周

---

## 第三阶段

MCP

https://modelcontextprotocol.io/introduction

重点：

- MCP Client
- MCP Server
- Tool Discovery

预计：

1~2周

---

# 第四部分：GitHub 仓库推荐

## S级（必学）

### LangGraph

https://github.com/langchain-ai/langgraph

重点：

- examples
- tutorials

---

### LangChain

https://github.com/langchain-ai/langchain

重点：

- LCEL
- Runnable

---

### MCP Specification

https://github.com/modelcontextprotocol/specification

重点：

- protocol
- architecture

---

## A级

### Awesome MCP Servers

https://github.com/punkpeye/awesome-mcp-servers

学习各种 MCP Server。

---

### Open Deep Research

https://github.com/langchain-ai/open_deep_research

学习 Deep Research Agent。

---

# 第五部分：B站课程推荐

## S级

宋红康 LangChain

适合基础。

---

## S级

LangGraph 教程

搜索关键词：

- LangGraph
- LangGraph Agent
- LangGraph 实战

---

## A级

MCP 实战

搜索关键词：

- MCP协议
- MCP Server
- MCP Agent

---

# 第六部分：RAG 2.0 必学

## Multi Query Retriever

一个问题生成多个查询。

---

## Parent Document Retriever

解决上下文丢失。

---

## Contextual Compression

压缩上下文。

---

## Rerank

推荐：

- BGE Reranker
- Jina Reranker

---

## Self-RAG

Agent自动决定是否继续检索。

---

# 第七部分：LangGraph 学习路线

## Level 1

单节点Agent

```text
START
↓
Agent
↓
END
```

---

## Level 2

Agent + Tool

```text
START
↓
Agent
↓
Tool
↓
END
```

---

## Level 3

Router

```text
START
↓
Router
├─ FAQ
├─ RAG
└─ Search
```

---

## Level 4

Memory

短期记忆

长期记忆

---

## Level 5

Human In The Loop

人工审批流程。

---

# 第八部分：MCP 学习路线

## Client

调用工具

---

## Server

暴露工具

---

## Remote MCP

远程服务

---

## Multi MCP

多个系统集成

示例：

- Gmail
- GitHub
- Jira
- Slack
- Notion

---

# 第九部分：Multi-Agent

## Supervisor

总控Agent

---

## Planner

任务规划

---

## Worker

执行任务

---

## Reviewer

结果审核

---

# 第十部分：企业项目路线

## 项目1

企业知识库

技术：

LangGraph
+
RAG

---

## 项目2

PDF 智能问答

技术：

LangGraph
+
RAG
+
Rerank

---

## 项目3

日本SES营业Agent

技术：

Gmail
+
Excel
+
LangGraph

---

## 项目4

面试Agent

技术：

简历
+
案件
+
RAG

---

## 项目5

MCP办公Agent

技术：

Notion
+
GitHub
+
Slack
+
Gmail

---

## 项目6

Deep Research Agent

技术：

Search
+
RAG
+
LangGraph
+
Multi-Agent

---

# 第十一部分：3个月计划

## 第1个月

LCEL
↓
LangChain 1.x
↓
高级RAG

---

## 第2个月

LangGraph

---

## 第3个月

MCP
↓
Multi-Agent
↓
企业项目

---

# 第十二部分：最终能力目标

掌握：

- LangChain 1.x
- LCEL
- RAG 2.0
- LangGraph
- MCP
- Multi-Agent

能够完成：

- 企业知识库
- 企业Agent
- AI客服
- 日本Agent项目
- Deep Research Agent

达到企业级 Agent 开发能力。
