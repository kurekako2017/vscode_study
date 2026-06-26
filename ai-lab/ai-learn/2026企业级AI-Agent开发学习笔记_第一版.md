# 2026 企业级 AI Agent 开发学习笔记（第一版）

> 配套 ai-learn 学习资料。

## 学习路线

Python -\> FastAPI -\> RAG -\> Embedding -\> Vector DB -\> LangChain -\>
LangGraph -\> MCP -\> Enterprise Agent

------------------------------------------------------------------------

## 第一章 RAG 基础

-   RAG = Retrieval + Generation
-   Loader
-   Chunk
-   Retriever
-   Prompt
-   LLM

### Chunk

将大文档切分为多个小片段，方便检索。

### Top K

从所有 Chunk 中检索最相关的 K 个片段提供给 LLM。

------------------------------------------------------------------------

## 第二章 doc_qa_agent

流程：

Question ↓ 读取 docs ↓ Chunk ↓ Retrieve ↓ TopK ↓ Context ↓ LLM ↓ Answer

### 文档路径

    python main.py "问题" --docs ./docs

企业项目一般通过 `.env` 或 `config.yaml` 指定固定资料目录。

------------------------------------------------------------------------

## 第三章 rag_api_demo

新增：

-   FastAPI
-   JSON API
-   PDF Loader
-   /ask
-   /reload
-   /health
-   内存缓存

------------------------------------------------------------------------

## 第四章 Streaming Agent

普通 API：

等待 -\> 返回

Streaming：

status -\> token -\> token -\> done

核心：

-   SSE
-   yield
-   StreamingResponse

------------------------------------------------------------------------

## 后续章节

-   Embedding
-   FAISS
-   Chroma
-   PGVector
-   LangChain 1.x
-   LangGraph
-   MCP
-   企业级 Agent

------------------------------------------------------------------------

## 建议

以后每个 ai-learn 示例统一整理：

1.  原理
2.  流程图
3.  源码解析
4.  企业实现
5.  LangChain 对照
6.  LangGraph 对照
7.  面试知识点
