# 《2026 企业级 AI Agent 开发学习笔记》总体规划

> 配套 **ai-learn** 项目，从基础到企业级实战的完整学习体系。

------------------------------------------------------------------------

# 全书结构

## 📗 第1卷：Python + FastAPI 基础（约100页）

**目标**

掌握 AI Agent 开发所需的 Python 与 FastAPI 基础，为后续 RAG 与 Agent
打下基础。

### 内容

-   Python 现代语法
-   类型注解
-   Pydantic
-   Async / Await
-   FastAPI
-   REST API
-   StreamingResponse
-   SSE
-   WebSocket
-   项目结构设计

------------------------------------------------------------------------

## 📘 第2卷：RAG（Chunk、Embedding、Retriever、Vector DB）（约150页）

**目标**

彻底理解企业级 RAG 的完整流程，而不仅仅会调用框架。

### 内容

-   RAG 原理
-   Loader
-   Text Splitter
-   Chunk
-   Chunk Size
-   Chunk Overlap
-   Token
-   Embedding
-   Similarity Search
-   Top K
-   Prompt 构建
-   FAISS
-   Chroma
-   PGVector
-   Milvus
-   企业级 RAG 架构

------------------------------------------------------------------------

## 📙 第3卷：LangChain 1.x（约150页）

**目标**

掌握 LangChain 1.x 最新开发模式。

### 内容

-   Runnable
-   LCEL
-   PromptTemplate
-   ChatPromptTemplate
-   OutputParser
-   Tool
-   Retriever
-   Memory
-   Agent
-   Callback
-   Streaming
-   LangSmith

------------------------------------------------------------------------

## 📕 第4卷：LangGraph（约200页）

**目标**

掌握企业级 Agent Workflow。

### 内容

-   StateGraph
-   Node
-   Edge
-   Conditional Edge
-   Router
-   ToolNode
-   Memory
-   Checkpointer
-   Human in the Loop
-   Multi-Agent
-   Supervisor
-   企业工作流

------------------------------------------------------------------------

## 📒 第5卷：MCP 与 Agent（约150页）

**目标**

学习现代 AI Agent 的工具调用标准。

### 内容

-   MCP Protocol
-   MCP Server
-   MCP Client
-   Tool
-   Resource
-   Prompt
-   OpenAI Agents SDK
-   Claude Code
-   Codex
-   Continue
-   企业工具调用

------------------------------------------------------------------------

## 📓 第6卷：企业级完整项目（React + FastAPI + LangGraph + RAG）（约200页）

**目标**

完成一个可部署的企业级 AI Agent 系统。

### 内容

-   React 前端
-   FastAPI 后端
-   LangGraph
-   RAG
-   向量数据库
-   用户登录
-   多轮对话
-   Memory
-   Tool Calling
-   文件上传
-   Docker
-   部署
-   企业项目架构

------------------------------------------------------------------------

# 每章统一结构

每个 ai-learn 示例统一采用：

1.  为什么要学习
2.  业务背景
3.  整体架构图
4.  Mermaid 流程图
5.  源码逐函数解析
6.  源码逐流程解析
7.  企业为什么这样设计
8.  LangChain 对照
9.  LangGraph 对照
10. 面试高频问题
11. 扩展练习
12. 企业最佳实践

------------------------------------------------------------------------

# 最终目标

完成一套覆盖：

-   Python
-   FastAPI
-   RAG
-   Embedding
-   Vector Database
-   LangChain 1.x
-   LangGraph
-   MCP
-   AI Agent
-   React
-   企业级项目

的系统化学习教材《2026 企业级 AI Agent 开发学习笔记》。
