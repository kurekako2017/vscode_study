# 2026 AI Agent 开发学习路线（LangChain 1.x / LangGraph / MCP）

## 当前阶段

已完成：

- Loader
- TextSplitter
- Embedding
- FAISS
- Chroma
- Retriever
- 基础RAG
- Tool Calling
- AgentExecutor
- Memory

---

# 推荐学习路线

## 第一阶段：LangChain 1.x

- ChatPromptTemplate
- MessagesPlaceholder
- Structured Output
- Pydantic OutputParser
- Tool Calling
- Runnable

重点：

```python
prompt | llm | parser
```

---

## 第二阶段：LCEL

学习：

- Runnable
- RunnableLambda
- RunnableParallel
- RunnableBranch
- RunnablePassthrough

目标：理解现代 LangChain 链式开发。

---

## 第三阶段：高级 RAG

学习：

- Parent Document Retriever
- Multi Query Retriever
- HyDE
- Contextual Compression
- Rerank
- Self-RAG

---

## 第四阶段：LangGraph

学习：

- State
- Node
- Edge
- Conditional Edge
- Router
- Checkpoint
- Memory
- Human-in-the-loop

重点程度：★★★★★

---

## 第五阶段：MCP

学习：

- MCP Client
- MCP Server
- Tool Discovery
- Remote MCP
- Multi MCP

---

## 第六阶段：Multi-Agent

学习：

- Supervisor
- Planner
- Worker
- Reviewer

---

## 第七阶段：企业实战项目

### 项目1

企业知识库

技术栈：

LangGraph + RAG + FAISS

### 项目2

PDF智能问答

技术栈：

LangGraph + RAG + Rerank

### 项目3

MCP Agent

技术栈：

LangGraph + MCP + Multi-Agent

---

# 最佳学习顺序

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
↓
企业项目

---

# 日本Agent开发路线

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
