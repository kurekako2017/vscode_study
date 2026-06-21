# 2026 LangChain 1.x + LangGraph + MCP 企业级学习路线（完整版）

## 为什么不建议继续深挖 LangChain 0.x

你已经完成：

- DocumentLoader
- TextSplitter
- Embedding
- FAISS
- Chroma
- Retriever
- 基础RAG
- Tool Calling
- AgentExecutor
- Memory

这些内容已经覆盖传统 LangChain 课程 70%~80%。

2026 企业项目主流方向已经转向：

LangGraph → MCP → Multi-Agent → Deep Research Agent

---

# 第一阶段：LCEL（立即开始）

核心知识：

- Runnable
- RunnableLambda
- RunnableBranch
- RunnableParallel
- RunnablePassthrough

目标：

```python
prompt | llm | parser
```

理解现代 LangChain 链式开发模式。

官方教程：

https://docs.langchain.com/oss/python/langchain/overview

重点章节：

- Runtime
- LCEL
- Structured Output
- Tool Calling

---

# 第二阶段：LangChain 1.x

重点学习：

## Prompt

- ChatPromptTemplate
- MessagesPlaceholder

## Output

- Structured Output
- Pydantic

## Runnable

- invoke
- batch
- stream

## Tool Calling

- bind_tools
- Structured Tool

不建议继续投入：

- initialize_agent
- AgentExecutor 深挖
- ConversationBufferMemory

---

# 第三阶段：高级 RAG

必须掌握：

## Multi Query Retriever

一个问题生成多个检索问题。

## Parent Document Retriever

解决 Chunk 丢失上下文。

## Contextual Compression

压缩上下文。

## Rerank

企业项目必备。

## Self-RAG

自动判断是否检索。

官方教程：

https://docs.langchain.com/oss/python/langchain/rag

---

# 第四阶段：LangGraph（最重要）

学习顺序：

1. State
2. Node
3. Edge
4. Conditional Edge
5. Router
6. Checkpoint
7. Memory
8. Human In The Loop

企业项目核心：★★★★★

官方教程：

https://langchain-ai.github.io/langgraph/

---

# 第五阶段：MCP

学习内容：

## MCP Client

调用工具。

## MCP Server

暴露工具。

## Remote MCP

远程工具。

## Multi MCP

多个系统协作。

典型结构：

Agent
├── Gmail
├── GitHub
├── Jira
├── Slack
└── Notion

官方教程：

https://modelcontextprotocol.io/introduction

---

# 第六阶段：Multi-Agent

学习：

- Supervisor
- Planner
- Worker
- Reviewer

典型结构：

Supervisor
├── Research Agent
├── Coding Agent
├── Review Agent
└── Report Agent

---

# GitHub 仓库推荐（按学习顺序）

## 第一梯队（必看）

1. LangGraph
https://github.com/langchain-ai/langgraph

2. LangChain
https://github.com/langchain-ai/langchain

3. MCP Specification
https://github.com/modelcontextprotocol/specification

4. Awesome MCP Servers
https://github.com/punkpeye/awesome-mcp-servers

5. Open Deep Research
https://github.com/langchain-ai/open_deep_research

---

# B站课程推荐

## S级

宋红康 LangChain 系列

优点：

- 中文
- 系统
- 入门最快

缺点：

- 偏 LangChain 0.x

---

## S级

LangGraph 实战课程

搜索：

- LangGraph 教程
- LangGraph 实战
- LangGraph Agent

重点：

- State
- Node
- Edge
- Router
- Memory

---

## A级

MCP 实战课程

搜索：

- MCP协议
- MCP Server
- MCP Client
- MCP实战

---

# 企业级实战项目

## 项目1：企业知识库

PDF
↓
RAG
↓
LangGraph
↓
回答

---

## 项目2：日本SES营业Agent

Gmail
+
Excel
+
案件JD
+
简历

自动匹配案件。

---

## 项目3：面试准备Agent

简历
+
案件
+
面试题

自动生成答案。

---

## 项目4：MCP办公Agent

Notion
+
GitHub
+
Slack
+
Gmail

---

## 项目5：Deep Research Agent

搜索
↓
阅读
↓
总结
↓
报告

---

# 你的最佳学习路线

（已完成）

DocumentLoader
↓
TextSplitter
↓
Embedding
↓
FAISS
↓
Retriever
↓
RAG

━━━━━━━━━━━━━━

（下一步）

LCEL
↓
LangChain 1.x
↓
高级RAG
↓
LangGraph
↓
MCP
↓
Multi-Agent

━━━━━━━━━━━━━━

（项目实战）

企业知识库
↓
日本SES Agent
↓
Deep Research Agent

---

# 2026 日本Agent开发路线

LCEL
↓
RAG
↓
LangGraph
↓
MCP

---

# 最终目标

DocumentLoader
↓
TextSplitter
↓
Embedding
↓
FAISS / Chroma
↓
Retriever
↓
RAG
↓
LCEL
↓
LangGraph
↓
MCP
↓
Multi-Agent

达到：

- 企业知识库开发
- AI客服开发
- 企业Agent开发
- 日本Agent项目面试
- 独立完成企业级Agent项目
