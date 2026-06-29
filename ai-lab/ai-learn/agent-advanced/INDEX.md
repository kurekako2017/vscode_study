# Agent Advanced 总索引

本索引帮助学习者从“技术主题、学习阶段、项目类型”三个角度进入 `agent-advanced/`。详细运行命令仍以各项目 README 为准。

> 当前导航策略：文档与代码保持物理分离，通过相对链接建立关系。不要从索引中移动、删除或重命名项目。

## 快速开始

1. 先读 [学习路线](./学习路线.md) 和 [核心技术栈总览](./核心技术栈总览.md)。
2. 想学概念，进入 [frameworks](./frameworks/README.md)。
3. 想直接运行，进入 [projects](./projects/README.md)。
4. 想补工程能力，再进入 RAG、MCP、评估、观测和部署专题。
5. 想看完整作品集，进入 [日本小売经营分析 Agent](./projects/japan_retail_analysis_agent/README.md) 或 [业务 Agent 作品集](./business-agents/README.md)。

## 按技术主题

### LangChain

- 文档入口：[frameworks/langchain](./frameworks/langchain/README.md)
- 学习笔记：[LangChain 学习笔记](./frameworks/langchain/LangChain学习笔记.md)
- 项目导航：[LangChain 相关项目](./frameworks/langchain/相关项目链接.md)
- 基础 demo：[langchain_chain_demo](./projects/langchain_chain_demo/README.md)
- RAG 延伸：[advanced_rag_pipeline_demo](./projects/advanced_rag_pipeline_demo/README.md)

### LangGraph

- 文档入口：[frameworks/langgraph](./frameworks/langgraph/README.md)
- 项目导航：[LangGraph 相关项目](./frameworks/langgraph/相关项目链接.md)
- 基础工作流：[langgraph_workflow_demo](./projects/langgraph_workflow_demo/README.md)
- 企业能力：[langgraph-enterprise](./langgraph-enterprise/README.md)
- 图编排 Multi-Agent：[graph_team_demo](./multi-agent/graph_team_demo/README.md)
- Deep Research：[deep-research](./deep-research/README.md)

### LlamaIndex

- 文档入口：[frameworks/llamaindex](./frameworks/llamaindex/README.md)
- 项目导航：[LlamaIndex 相关项目](./frameworks/llamaindex/相关项目链接.md)
- 概念教学 demo：[llamaindex_index_demo](./projects/llamaindex_index_demo/README.md)

### RAG

- 专题入口：[rag](./rag/README.md)
- 高级模式：[advanced-patterns](./rag/advanced-patterns/README.md)
- 完整管线：[advanced_rag_pipeline_demo](./projects/advanced_rag_pipeline_demo/README.md)
- 企业混合检索：[internal_hybrid_rag_demo](./projects/internal_hybrid_rag_demo/README.md)
- 向量库原理：[vector_db_demo](./projects/vector_db_demo/README.md)
- Qdrant：[vector_db_qdrant_demo](./projects/vector_db_qdrant_demo/README.md)
- Chroma：[vector_db_chroma_demo](./projects/vector_db_chroma_demo/README.md)
- RAG 评估：[rag_eval_demo](./eval/rag_eval_demo/README.md)

### MCP

- 协议与代码入口：[mcp](./mcp/README.md)
- Client：[mcp/client.py](./mcp/client.py)
- Server：[mcp/server.py](./mcp/server.py)
- Multi-MCP Router：[mcp/multi_router.py](./mcp/multi_router.py)
- 业务 Agent 示例：[mcp_office_agent](./business-agents/mcp_office_agent/README.md)

### Multi-Agent

- 专题入口：[multi-agent](./multi-agent/README.md)
- 轻量角色协作：[multi_agent_team_demo](./projects/multi_agent_team_demo/README.md)
- 真实 LangGraph 图编排：[graph_team_demo](./multi-agent/graph_team_demo/README.md)
- 业务 Agent 作品集：[business-agents](./business-agents/README.md)

### Observability

- 专题入口：[observability](./observability/README.md)
- Tracing 示例：[tracing_demo/main.py](./observability/tracing_demo/main.py)
- 完整项目观测设计：[日本小売 Agent 架构](./projects/japan_retail_analysis_agent/docs/ARCHITECTURE.md)

### Deployment

- 专题入口：[deployment](./deployment/README.md)
- 容器示例：[container_demo](./deployment/container_demo/README.md)
- 项目级 Docker 示例：[日本小売 Agent](./projects/japan_retail_analysis_agent/README.md)
- 开发测试部署流程：[开发测试部署流程](./开发测试部署流程.md)

### Evaluation

- 专题入口：[eval](./eval/README.md)
- RAG 评估：[rag_eval_demo](./eval/rag_eval_demo/README.md)
- Deep Research 评估要求：[需求与评估标准](./deep-research/需求与评估标准.md)
- 完整项目测试：[日本小売 Agent 测试](./projects/japan_retail_analysis_agent/TESTING.md)

### Frontend

- 专题入口：[frontend](./frontend/README.md)
- React 聊天 UI：[chat_ui_demo](./frontend/chat_ui_demo/README.md)
- 完整项目前端：[日本小売 Agent](./projects/japan_retail_analysis_agent/README.md)

### Deep Research

- 主入口：[deep-research](./deep-research/README.md)
- 入口代码：[deep_research_demo/main.py](./deep-research/deep_research_demo/main.py)
- 评估标准：[需求与评估标准](./deep-research/需求与评估标准.md)

## 按学习阶段

### 初级

目标：理解框架概念和最小调用链。

1. [LangChain 文档](./frameworks/langchain/README.md) → [基础 Chain demo](./projects/langchain_chain_demo/README.md)
2. [LangGraph 文档](./frameworks/langgraph/README.md) → [基础 Workflow demo](./projects/langgraph_workflow_demo/README.md)
3. [LlamaIndex 文档](./frameworks/llamaindex/README.md) → [概念索引 demo](./projects/llamaindex_index_demo/README.md)
4. [向量数据库最小教学版](./projects/vector_db_demo/README.md)

### 中级

目标：把框架能力组合成完整检索、协作和 UI 流程。

1. [高级 RAG 管线](./projects/advanced_rag_pipeline_demo/README.md)
2. [企业混合检索](./projects/internal_hybrid_rag_demo/README.md)
3. [轻量多 Agent](./projects/multi_agent_team_demo/README.md)
4. [React 聊天 UI](./frontend/chat_ui_demo/README.md)
5. [RAG 评估](./eval/rag_eval_demo/README.md)

### 高级

目标：掌握真实框架编排、协议集成、持久化后端与可观测性。

1. [LangGraph Multi-Agent](./multi-agent/graph_team_demo/README.md)
2. [MCP](./mcp/README.md)
3. [Deep Research](./deep-research/README.md)
4. [Qdrant](./projects/vector_db_qdrant_demo/README.md) 或 [Chroma](./projects/vector_db_chroma_demo/README.md)
5. [Tracing 与成本观测](./observability/README.md)

### 企业级

目标：理解审批、恢复、评估、部署、审计与业务闭环。

1. [LangGraph 企业能力](./langgraph-enterprise/README.md)
2. [业务 Agent 作品集](./business-agents/README.md)
3. [日本小売经营分析 Agent](./projects/japan_retail_analysis_agent/README.md)
4. [部署专题](./deployment/README.md)
5. [交付前检查清单](./交付前检查清单.md)

## 按项目类型

### 学习文档

- [学习路线](./学习路线.md)
- [核心技术栈总览](./核心技术栈总览.md)
- [框架专题](./frameworks/README.md)
- [RAG 专题](./rag/README.md)
- [MCP 专题](./mcp/README.md)
- [Multi-Agent 专题](./multi-agent/README.md)

### Demo 代码

- [projects demo 总入口](./projects/README.md)
- [LangChain demo](./projects/langchain_chain_demo/README.md)
- [LangGraph demo](./projects/langgraph_workflow_demo/README.md)
- [LlamaIndex 概念 demo](./projects/llamaindex_index_demo/README.md)
- [向量数据库 demo](./projects/vector_db_demo/README.md)

### 实战项目

- [日本小売经营分析 Agent](./projects/japan_retail_analysis_agent/README.md)
- [业务 Agent 作品集](./business-agents/README.md)
- [企业混合检索 RAG](./projects/internal_hybrid_rag_demo/README.md)

### 部署示例

- [容器化 demo](./deployment/container_demo/README.md)
- [部署专题](./deployment/README.md)
- [开发测试部署流程](./开发测试部署流程.md)

### 评估示例

- [RAG 评估 demo](./eval/rag_eval_demo/README.md)
- [Deep Research 评估标准](./deep-research/需求与评估标准.md)
- [完整项目测试说明](./projects/japan_retail_analysis_agent/TESTING.md)

## 维护规则

- 新增框架文档时，更新 `frameworks/README.md`。
- 新增 demo 时，更新 `projects/README.md` 和对应框架/专题关联页。
- 新增企业级能力时，标明前置知识和对应基础 demo。
- 不链接 `node_modules`、`__pycache__`、`dist`、runtime 数据库等生成物。
- 不为整理目录而移动可运行项目；需要移动时先生成逐文件方案并验证命令、导入、测试和部署路径。
