# AI-Lab 目录覆盖盘点与重规划

> 目的：以 `2026` 目录下 5 份学习路线文档为目标清单，对比 `ai-lab` 当前各学习目录、文档和可运行示例的覆盖情况，找出“已覆盖、部分覆盖、未覆盖、需要整合”的内容，并给出后续目录重规划方案。
>
> 说明：这里的“查缺补漏”不是评价那 5 份文档，而是用它们作为目标能力地图，反查 `ai-lab` 仓库当前内容是否支撑这条路线。

---

# 一、盘点范围

## 目标来源

来自 `2026` 目录 5 份文档的共同目标：

- LangChain 1.x / LCEL
- 结构化输出
- Tool Calling
- RAG 2.0
- LangGraph
- Checkpoint / Memory / Human In The Loop
- MCP Client / Server / Remote / Multi MCP
- Multi-Agent
- Deep Research Agent
- 企业知识库 Agent
- 日本 SES 营业 Agent
- 面试准备 Agent
- MCP Office Agent
- 企业客服 Agent
- GitHub / Coding Agent
- 前端、FastAPI、部署、评估、运维、作品集、面试

## 当前仓库主要目录

| 目录 | 当前定位 |
|---|---|
| `ai-learn/llm-lab/` | LLM 应用基础：模型调用、结构化输出、RAG、FastAPI、评估、日本现场 |
| `ai-learn/agent-lab/` | Agent 基础进阶：Tool Calling、工作流、RAG 工具化、可运行 demo |
| `ai-learn/agent-advanced/` | 高级 Agent：LangChain、LangGraph、高级 RAG、Multi-Agent、前端、评估、部署 |
| `ai-agents-from-zero/` | 系统课程型资料：LangChain、MCP、LangGraph、DeepAgents、实战项目 |
| `all-in-rag-main/` | RAG 专项资料：高级检索、混合检索、GraphRAG、评估 |
| `hello-agents-main/` | Agent 通识、案例项目、技能、WebAgent、GUIAgent 等扩展资料 |
| `2026/` | 新目标路线与规划资料 |

---

# 二、总体结论

`ai-lab` 当前不是缺基础，而是缺“统一主线”和“2026 目标能力的目录归位”。

当前覆盖情况可以概括为：

- 基础 LLM、结构化输出、基础 RAG、FastAPI：覆盖较好，且有可运行 demo。
- Tool Calling、固定 Workflow、基础 Agent：覆盖较好，且有可运行 demo。
- 高级 RAG、混合检索、rerank、引用、权限过滤：已有较强覆盖，但分散在 `agent-advanced` 和 `all-in-rag-main`。
- LangGraph：已有入门 demo 和大量课程源码，但 `agent-advanced` 主线中缺少 checkpoint、HITL、subgraph、streaming 等专题化目录。
- MCP：`ai-agents-from-zero` 有文档和代码，但主学习目录没有独立 `mcp/` 目录和可运行项目入口。
- Multi-Agent：已有基础 demo 和 LangGraph supervisor 示例，但缺少企业级项目化版本。
- Deep Research：`ai-agents-from-zero` 覆盖很强，也有 `deepsearch-agents-main` 项目，但没有整合进 `ai-lab` 主路线。
- 日本 SES 营业 Agent、面试 Agent、MCP Office Agent、企业客服 Agent：多数只是目标方向，缺少主线中的完整项目目录。
- 工程化：FastAPI、React、评估、Docker 都已有，但还需要作为统一“交付模板”贯穿项目。

因此，后续重点不是继续堆资料，而是：

1. 把 `ai-agents-from-zero`、`all-in-rag-main` 中已有强内容映射回 `ai-lab` 主线。
2. 给 2026 目标新增缺失专题目录：`mcp/`、`langgraph-enterprise/`、`deep-research/`、`business-agents/`。
3. 把每个目标能力都配成“文档 + 可运行 demo + 项目任务 + 验收标准”。

---

# 三、覆盖等级说明

| 等级 | 含义 |
|---|---|
| 完整覆盖 | 有学习文档，有可运行 demo，且和 2026 目标直接对应 |
| 部分覆盖 | 有文档或代码，但缺主线整合、缺工程化、缺项目化或缺可运行入口 |
| 资料覆盖 | 有课程资料或外部项目，但未纳入 `ai-lab` 主学习目录 |
| 缺失 | 当前仓库没有明确文档或可运行示例 |

---

# 四、能力清单覆盖矩阵

## 1. 基础 LLM 与结构化输出

| 目标能力 | 覆盖等级 | 当前位置 | 缺口 |
|---|---|---|---|
| Python 面向 LLM 应用基础 | 完整覆盖 | `ai-learn/llm-lab/00-Python学习范围（面向LLM应用开发）.md` | 缺少更系统的练习任务索引 |
| 模型调用 | 完整覆盖 | `ai-learn/llm-lab/02-模型调用基础.md`、`ai-learn/agent-lab/projects/chat_cli/` | 已够用 |
| 结构化输出 | 完整覆盖 | `ai-learn/llm-lab/03-结构化输出.md`、`ai-learn/agent-lab/projects/structured_output_demo/` | 可补“校验失败重试”示例 |
| Prompt / Message Template | 部分覆盖 | `ai-agents-from-zero/13-提示词与消息模板.md`、`ai-learn/agent-advanced/projects/langchain_chain_demo/` | 主线中没有独立 Prompt 工程练习 |
| Pydantic / Schema | 完整覆盖 | `structured_output_demo`、`rag_api_demo` | 可补复杂嵌套 schema 练习 |

结论：基础层已经够支撑 2026 路线，不需要新建大目录，只需要在 `ai-learn/llm-lab/examples/` 增加少量练习。

---

## 2. LangChain 1.x / LCEL

| 目标能力 | 覆盖等级 | 当前位置 | 缺口 |
|---|---|---|---|
| LCEL / Runnable | 完整覆盖 | `ai-agents-from-zero/15-LCEL与链式调用.md`、`ai-learn/agent-advanced/projects/langchain_chain_demo/` | `llm-lab -> agent-advanced` 路线需显式指向 |
| RunnableLambda / Parallel / Branch | 部分覆盖 | `ai-learn/agent-advanced/projects/langchain_chain_demo/` | 缺按 Runnable 类型拆分的小练习 |
| Tool Calling in LangChain | 完整覆盖 | `ai-agents-from-zero/17-Tools工具调用.md`、`ai-learn/agent-lab/projects/tool_agent_demo/` | 可补 LangChain 1.x 风格工具封装对照 |
| AgentExecutor 迁移认知 | 资料覆盖 | `2026` 文档、`ai-agents-from-zero/21-Agent智能体.md` | 缺“旧 AgentExecutor 到 LangGraph”迁移说明 |

结论：LCEL 已覆盖，但建议新增 `ai-learn/agent-advanced/frameworks/langchain/LCEL实战任务清单.md`，把 Runnable 类型和 demo 对齐。

---

## 3. RAG 2.0 / 企业知识库

| 目标能力 | 覆盖等级 | 当前位置 | 缺口 |
|---|---|---|---|
| 基础 RAG | 完整覆盖 | `ai-learn/llm-lab/04-RAG.md`、`ai-learn/agent-lab/projects/doc_qa_agent/` | 已够用 |
| RAG API 化 | 完整覆盖 | `ai-learn/llm-lab/05-FastAPI与企业集成.md`、`ai-learn/agent-lab/projects/rag_api_demo/` | 可补 SSE/流式输出 |
| 向量库基础 | 完整覆盖 | `ai-learn/agent-advanced/projects/vector_db_demo/` | 已够用 |
| Qdrant / Chroma | 完整覆盖 | `vector_db_qdrant_demo/`、`vector_db_chroma_demo/`、`ai-agents-from-zero/18-向量数据库与Embedding实战.md` | 可补统一选择建议 |
| Rerank | 部分覆盖 | `ai-learn/agent-advanced/projects/advanced_rag_pipeline_demo/`、`all-in-rag-main/code/C4` | 缺真实 reranker 接入任务 |
| Hybrid Search | 完整覆盖 | `ai-learn/agent-advanced/projects/internal_hybrid_rag_demo/`、`all-in-rag-main/docs/chapter4` | 需要纳入 2026 主路线 |
| Parent Document Retriever | 资料覆盖 | `all-in-rag-main/docs/chapter9/04_intelligent_query_routing.md` | 缺主线 demo |
| Multi Query Retriever | 部分覆盖 | `all-in-rag-main` 相关资料 | 缺主线 demo |
| Contextual Compression | 部分覆盖 | `all-in-rag-main` 相关资料 | 缺主线 demo |
| Self-RAG | 缺失/弱覆盖 | 未看到主线 demo | 需要新增 |
| GraphRAG | 资料覆盖 | `all-in-rag-main/docs/chapter7`、`all-in-rag-main/docs/chapter9` | 缺简化可运行 demo |
| RAG 评估 | 完整覆盖 | `ai-learn/llm-lab/06-评估与运维.md`、`ai-learn/llm-lab/rag_eval_notes.md`、`ai-learn/agent-advanced/eval/rag_eval_demo/`、`all-in-rag-main/docs/chapter6` | 需要统一成评估模板 |
| 权限过滤与引用 | 完整覆盖 | `ai-learn/agent-advanced/projects/internal_hybrid_rag_demo/` | 可作为企业知识库标准 demo |

结论：RAG 是当前覆盖最强的方向。真正缺的是把高级 RAG 拆成可执行任务链：query rewrite、parent doc、compression、self-rag、graph-rag。

建议新增：

```text
ai-learn/agent-advanced/rag/advanced-patterns/
├── multi_query_retriever_demo/
├── parent_document_retriever_demo/
├── contextual_compression_demo/
├── self_rag_router_demo/
└── graph_rag_minimal_demo/
```

---

## 4. LangGraph

| 目标能力 | 覆盖等级 | 当前位置 | 缺口 |
|---|---|---|---|
| StateGraph / Node / Edge | 完整覆盖 | `ai-learn/agent-advanced/projects/langgraph_workflow_demo/`、`ai-agents-from-zero/22-24 LangGraph章节`、`案例与源码-3-LangGraph框架/` | 已够用 |
| Conditional Edge / Router | 完整覆盖 | `langgraph_workflow_demo`、`案例与源码-3-LangGraph框架/05-edge/` | 可补业务路由案例 |
| State schema / reducer | 资料覆盖 | `案例与源码-3-LangGraph框架/03-state/` | 主线中缺专题说明 |
| ToolNode | 部分覆盖 | `ai-agents-from-zero/25-LangGraph高级特性.md`、源码目录 | 缺主线可运行 demo |
| Checkpoint / Memory | 资料覆盖 | `案例与源码-3-LangGraph框架/07-senior/state_persistence/`、`deepsearch-agents-main/examples/10/11` | 缺主线项目化 demo |
| Human In The Loop | 资料覆盖 | `ai-agents-from-zero/实战项目-深度研搜/5-人机协作与中断恢复.md`、`deepsearch-agents-main/examples/8/9` | 缺纳入 `agent-advanced` |
| Subgraph | 资料覆盖 | `案例与源码-3-LangGraph框架/07-senior/subgraph/` | 缺主线专题 |
| Streaming | 资料覆盖 | `案例与源码-3-LangGraph框架/07-senior/streaming/`、`deepsearch-agents-main/examples/2/4` | 缺前后端联动 demo |
| Time Travel | 资料覆盖 | `案例与源码-3-LangGraph框架/07-senior/time_travel/` | 可选补充 |
| LangGraph + RAG | 部分覆盖 | `ai-learn/agent-advanced/projects/langgraph_workflow_demo/`、`advanced_rag_pipeline_demo/` 分开存在 | 缺组合项目 |
| LangGraph + MCP | 缺失/弱覆盖 | `2026` 文档提到，主线暂无 | 需要新增 |

结论：LangGraph 不是没有资料，而是“课程源码强、主线项目弱”。建议把 `ai-agents-from-zero/案例与源码-3-LangGraph框架` 中的高级能力迁移为 `ai-learn/agent-advanced/langgraph-enterprise` 专题。

建议新增：

```text
ai-learn/agent-advanced/langgraph-enterprise/
├── README.md
├── 01-state-node-edge/
├── 02-router-toolnode/
├── 03-checkpoint-memory/
├── 04-human-in-the-loop/
├── 05-streaming-subgraph/
└── 06-langgraph-rag-agent/
```

---

## 5. MCP

| 目标能力 | 覆盖等级 | 当前位置 | 缺口 |
|---|---|---|---|
| MCP 概念 | 完整覆盖 | `ai-agents-from-zero/20-MCP模型上下文协议.md` | 需要主线入口 |
| MCP Server | 资料覆盖 | `ai-agents-from-zero/案例与源码-2-LangChain框架/11-mcp/McpServer.py`、`McpServerByFastMCP.py` | 缺独立项目目录 |
| FastMCP | 资料覆盖 | `McpServerByFastMCP.py`、`McpServerWeatherByFastMCP.py` | 缺 README 化的运行说明 |
| MCP Client | 资料覆盖 | `McpClient.py`、`McpClientAgent.py` | 缺主线 demo |
| `mcp.json` | 资料覆盖 | `案例与源码-2-LangChain框架/11-mcp/mcp.json` | 缺配置讲解 |
| MCP + LangChain Agent | 资料覆盖 | `McpClientAgent.py` | 缺可验收任务 |
| MCP + LangGraph | 缺失 | 主线暂无组合项目 | 需要新增 |
| Remote MCP | 缺失/弱覆盖 | 未见主线 demo | 需要新增 |
| Multi MCP | 缺失 | 未见多个 MCP server 聚合 demo | 需要新增 |
| MCP 权限 / 日志 / 审计 | 部分覆盖 | MCP 文档有安全说明，工程目录有日志意识 | 缺项目级实现 |

结论：MCP 是 2026 目标里的最大结构性缺口。已有源码在 `ai-agents-from-zero`，但没有变成 `ai-lab` 主线的一等目录。

建议新增：

```text
ai-learn/agent-advanced/mcp/
├── README.md
├── 01-mcp-concepts.md
├── server_fastmcp_demo/
├── client_stdio_demo/
├── client_agent_demo/
├── langgraph_mcp_agent_demo/
├── remote_mcp_demo/
└── multi_mcp_router_demo/
```

优先级最高的是：

1. `server_fastmcp_demo`
2. `client_agent_demo`
3. `langgraph_mcp_agent_demo`

---

## 6. Multi-Agent

| 目标能力 | 覆盖等级 | 当前位置 | 缺口 |
|---|---|---|---|
| Planner / Researcher / Writer / Critic | 完整覆盖 | `ai-learn/agent-advanced/projects/multi_agent_team_demo/` | 已有入门 demo |
| Supervisor | 部分覆盖 | `multi_agent_team_demo`、`案例与源码-3-LangGraph框架/08-multi_agent/` | 缺企业项目版 |
| Reviewer | 完整覆盖 | `multi_agent_team_demo` | 可增强为评审指标 |
| LangGraph Multi-Agent | 资料覆盖 | `案例与源码-3-LangGraph框架/08-multi_agent/` | 缺主线整合 |
| Agent 之间状态传递 | 部分覆盖 | `multi_agent_team_demo` | 缺复杂状态管理 |
| 防无限循环 / 成本控制 | 部分覆盖 | `deepsearch-agents-main/examples/13-model-call-limit-middleware.py` | 缺主线说明 |
| Multi-Agent + RAG | 部分覆盖 | `deepsearch-agents-main`、`multi_agent_team_demo` 分散存在 | 缺统一项目 |

结论：Multi-Agent 入门已覆盖，企业级多 Agent 项目还缺。建议 Deep Research 作为升级项目承接它。

---

## 7. Deep Research Agent

| 目标能力 | 覆盖等级 | 当前位置 | 缺口 |
|---|---|---|---|
| Deep Research 概念 | 完整覆盖 | `ai-agents-from-zero/实战项目-深度研搜/` | 需要接入主线 |
| 搜索子智能体 | 完整覆盖 | `实战项目-深度研搜/10-网络搜索子智能体与Tavily工具.md` | 已有 |
| RAGFlow 子智能体 | 完整覆盖 | `实战项目-深度研搜/12-RAGFlow子智能体与知识库准备.md` | 已有 |
| 数据库查询子智能体 | 完整覆盖 | `实战项目-深度研搜/11-数据库查询子智能体与MySQL工具.md` | 已有 |
| 主智能体 | 完整覆盖 | `实战项目-深度研搜/13-主智能体搭建与异步执行.md` | 已有 |
| FastAPI 闭环 | 完整覆盖 | `实战项目-深度研搜/14-FastAPI接口与项目闭环.md`、`deepsearch-agents-main` | 已有 |
| 流式输出 / 异步 | 完整覆盖 | `deepsearch-agents-main/examples/2/4` | 需要主线索引 |
| HITL / 中断恢复 | 完整覆盖 | `实战项目-深度研搜/5-人机协作与中断恢复.md`、`examples/8/9` | 需要抽成 LangGraph/HITL 专题 |
| 长期记忆 | 完整覆盖 | `实战项目-深度研搜/6-长期记忆与Backend存储.md`、`examples/10/11` | 需要主线索引 |

结论：Deep Research 实际已经覆盖较强，但藏在 `ai-agents-from-zero` 里。建议不要重写，而是把它升级为 `ai-learn/agent-advanced/deep-research/` 主项目入口，链接现有项目。

建议新增：

```text
ai-learn/agent-advanced/deep-research/
├── README.md
├── CODE_READING_ROUTE.md
├── 01-minimal-deep-research-demo/
├── 02-search-rag-db-subagents/
├── 03-hitl-memory-streaming/
└── 04-fastapi-frontend-integration/
```

其中 `deepsearch-agents-main` 可作为完整项目，`ai-learn/agent-advanced/deep-research` 只做学习索引和精简 demo。

---

## 8. 企业业务 Agent 项目

| 2026 目标项目 | 覆盖等级 | 当前位置 | 缺口 |
|---|---|---|---|
| 企业知识库 Agent | 完整覆盖 | `doc_qa_agent`、`rag_api_demo`、`internal_hybrid_rag_demo`、`advanced_rag_pipeline_demo` | 需要合并成标准作品集项目 |
| PDF 智能问答 | 部分覆盖 | `doc_qa_agent`、`rag_api_demo` | PDF 支持需确认和加强 |
| 企业客服 Agent | 部分覆盖 | Coze/Dify 客服案例、RAG demo | 缺 LangGraph 客服项目 |
| 日本 SES 营业 Agent | 缺失 | `llm-lab` 有日本现场关键词，但无完整项目 | 需要新增核心项目 |
| 面试准备 Agent | 缺失/弱覆盖 | `ai-learn/llm-lab/10-作品集与面试准备.md`、面试题库 | 缺可运行 Agent |
| MCP Office Agent | 缺失 | MCP 资料分散，无 Office 集成 demo | 需要新增 |
| GitHub Agent / Code Review Agent | 资料覆盖 | `hello-agents-main/Co-creation-projects/jjyaoao-CodeReviewAgent` 等 | 缺主线 demo |
| 电商问数 Agent | 完整覆盖 | `ai-agents-from-zero/实战项目-电商问数`、`shopkeeper-agent-main` | 可作为“数据库问数 Agent”项目 |
| Deep Research Agent | 完整覆盖但未归位 | `实战项目-深度研搜`、`deepsearch-agents-main` | 需要主线入口 |

结论：企业知识库、问数、Deep Research 已有强项目；日本 SES、面试 Agent、MCP Office 是明显缺口。

建议新增：

```text
ai-learn/agent-advanced/business-agents/
├── README.md
├── enterprise_knowledge_agent/
├── japan_ses_matching_agent/
├── interview_coach_agent/
├── mcp_office_agent/
├── customer_support_agent/
└── github_review_agent/
```

优先级：

1. `japan_ses_matching_agent`
2. `mcp_office_agent`
3. `interview_coach_agent`
4. `customer_support_agent`
5. `github_review_agent`

---

## 9. 工程化、前端、评估、部署

| 目标能力 | 覆盖等级 | 当前位置 | 缺口 |
|---|---|---|---|
| FastAPI | 完整覆盖 | `rag_api_demo`、`deepsearch-agents-main`、`shopkeeper-agent-main` | 可统一模板 |
| React 前端 | 部分覆盖 | `ai-learn/agent-advanced/frontend/chat_ui_demo`、项目 frontend | 缺统一 API 联调模板 |
| Docker | 完整覆盖 | `ai-learn/agent-advanced/deployment/container_demo`、项目 docker | 可补 compose 多服务模板 |
| 环境变量 / 配置 | 完整覆盖 | `ai-learn/agent-lab/API配置与兼容策略.md`、项目配置 | 可补 secrets 管理 |
| 日志 / Tracing | 部分覆盖 | `ai-learn/llm-lab/06-评估与运维.md`、`ai-learn/agent-advanced/开发测试部署流程.md` | 缺可运行 tracing demo |
| RAG eval | 完整覆盖 | `ai-learn/agent-advanced/eval/rag_eval_demo`、`all-in-rag-main` | 需要统一评估报告模板 |
| Agent eval | 部分覆盖 | `multi_agent_team_demo`、评估目录 | 缺 Agent 任务成功率评估 |
| CI/CD | 部分覆盖 | `ai-learn/agent-advanced/开发测试部署流程.md` | 缺可运行 CI 示例 |
| 安全 / 权限 | 部分覆盖 | `internal_hybrid_rag_demo`、`ai-learn/llm-lab/08-云平台与企业环境.md` | 缺 Prompt Injection / PII 专题 |
| 成本控制 | 部分覆盖 | 文档层提到 | 缺 token/cost 统计 demo |

结论：工程化已有骨架，但应该作为所有高级项目的统一底座，而不是单独存在。

建议新增：

```text
ai-learn/agent-advanced/platform-template/
├── README.md
├── backend_fastapi/
├── frontend_react/
├── eval/
├── docker/
├── observability/
└── project_scaffold.md
```

---

# 五、当前目录重规划建议

## 推荐新结构

```text
ai-lab/
├── README.md
├── 2026/
│   ├── README.md
│   ├── AI-Lab-目录覆盖盘点与重规划.md
│   ├── 2026-学习路线总纲.md
│   └── 2026-作品集任务清单.md
├── 00-foundation/
│   └── README.md
├── 01-llm-app/
│   └── README.md
├── 02-rag/
│   └── README.md
├── 03-agent/
│   └── README.md
├── 04-langgraph/
│   └── README.md
├── 05-mcp/
│   └── README.md
├── 06-multi-agent/
│   └── README.md
├── 07-enterprise-projects/
│   └── README.md
├── 08-engineering/
│   └── README.md
├── archive-or-source/
│   ├── ai-agents-from-zero/
│   ├── all-in-rag-main/
│   └── hello-agents-main/
├── ai-learn/llm-lab/
├── ai-learn/agent-lab/
└── ai-learn/agent-advanced/
```

这个方案适合“重构为课程体系”。但如果不想大规模移动目录，可以采用低风险方案。

## 低风险方案：不移动大目录，只新增索引层

推荐先采用这个方案：

```text
ai-lab/
├── 2026/
│   ├── README.md
│   ├── AI-Lab-目录覆盖盘点与重规划.md
│   ├── 2026-能力地图.md
│   ├── 2026-目录索引.md
│   └── 2026-项目任务板.md
├── ai-learn/llm-lab/
├── ai-learn/agent-lab/
├── ai-learn/agent-advanced/
│   ├── mcp/
│   ├── langgraph-enterprise/
│   ├── deep-research/
│   ├── business-agents/
│   └── platform-template/
├── ai-agents-from-zero/
├── all-in-rag-main/
└── hello-agents-main/
```

优点：

- 不破坏现有链接。
- 不移动大量课程资料。
- 先把 2026 路线通过索引串起来。
- 后续新增内容都放到 `agent-advanced` 下，形成高级主线。

建议采用低风险方案。

---

# 六、建议补充目录与优先级

## P0：立刻补

### 1. `ai-learn/agent-advanced/mcp/`

原因：MCP 是 2026 文档里的核心目标，但当前主线缺独立目录。

最小内容：

```text
ai-learn/agent-advanced/mcp/
├── README.md
├── server_fastmcp_demo/
├── client_stdio_demo/
└── langgraph_mcp_agent_demo/
```

可复用来源：

- `ai-agents-from-zero/20-MCP模型上下文协议.md`
- `ai-agents-from-zero/案例与源码-2-LangChain框架/11-mcp/`

### 2. `ai-learn/agent-advanced/langgraph-enterprise/`

原因：LangGraph 已有基础 demo，但 2026 目标强调 checkpoint、memory、HITL、ToolNode、Multi-Agent。

最小内容：

```text
ai-learn/agent-advanced/langgraph-enterprise/
├── README.md
├── checkpoint_memory_demo/
├── human_in_the_loop_demo/
├── toolnode_router_demo/
└── langgraph_rag_agent_demo/
```

可复用来源：

- `ai-agents-from-zero/案例与源码-3-LangGraph框架/07-senior/`
- `ai-agents-from-zero/实战项目-深度研搜/5-人机协作与中断恢复.md`
- `ai-agents-from-zero/deepsearch-agents-main/examples/8-human-approval-interrupt-resume.py`

### 3. `ai-learn/agent-advanced/deep-research/`

原因：Deep Research 已有完整项目，但没有进入主线。

最小内容：

```text
ai-learn/agent-advanced/deep-research/
├── README.md
├── reading_route.md
└── minimal_research_agent_demo/
```

可复用来源：

- `ai-agents-from-zero/实战项目-深度研搜/`
- `ai-agents-from-zero/deepsearch-agents-main/`

### 4. `ai-learn/agent-advanced/business-agents/japan_ses_matching_agent/`

原因：这是 2026 文档反复强调的日本业务方向，但当前无完整项目。

最小功能：

- JD 解析
- 简历解析
- 技能匹配
- 匹配评分
- 推荐理由
- 风险点
- 邮件草稿
- 人工确认

可复用来源：

- `ai-learn/llm-lab/07-日本现场应用与案件关键词.md`
- `ai-learn/llm-lab/日语对照速查表.md`
- `structured_output_demo`
- `workflow_agent`
- `internal_hybrid_rag_demo`

---

## P1：第二批补

### 1. `ai-learn/agent-advanced/rag/advanced-patterns/`

补齐：

- Multi Query Retriever
- Parent Document Retriever
- Contextual Compression
- Self-RAG
- GraphRAG minimal demo

可复用来源：

- `all-in-rag-main/`
- `ai-learn/agent-advanced/projects/advanced_rag_pipeline_demo`

### 2. `ai-learn/agent-advanced/business-agents/mcp_office_agent/`

补齐：

- Gmail-like mock tool
- Calendar-like mock tool
- GitHub-like mock tool
- Notion-like mock tool
- MCP Server + LangGraph Router

### 3. `ai-learn/agent-advanced/business-agents/interview_coach_agent/`

补齐：

- 简历解析
- JD 分析
- 自我介绍生成
- 技术问答生成
- 日文回答草稿

### 4. `ai-learn/agent-advanced/platform-template/`

补齐：

- FastAPI backend template
- React chat UI template
- Docker compose
- eval template
- logs / trace_id / cost tracking

---

## P2：第三批补

- `customer_support_agent`
- `github_review_agent`
- `agent-security`
- `prompt-injection-demo`
- `cost-tracing-demo`
- `agent-eval-demo`
- `remote-mcp-demo`
- `multi-mcp-router-demo`

---

# 七、建议主学习路线

基于当前仓库实际内容，推荐新路线如下：

## 第一层：基础 LLM 应用

入口：

- `ai-learn/llm-lab/README.md`

学习顺序：

1. `00-Python学习范围（面向LLM应用开发）.md`
2. `02-模型调用基础.md`
3. `03-结构化输出.md`
4. `04-RAG.md`
5. `05-FastAPI与企业集成.md`
6. `06-评估与运维.md`

运行项目：

- `ai-learn/agent-lab/projects/chat_cli`
- `ai-learn/agent-lab/projects/structured_output_demo`
- `ai-learn/agent-lab/projects/doc_qa_agent`
- `ai-learn/agent-lab/projects/rag_api_demo`

## 第二层：Agent 基础

入口：

- `ai-learn/agent-lab/README.md`

学习顺序：

1. `Agent系统框架与术语.md`
2. `03-Tool Calling.md`
3. `05-Agent工作流.md`
4. `06-Agent产品化与部署.md`

运行项目：

- `tool_agent_demo`
- `workflow_agent`

## 第三层：高级 RAG 与 LangChain

入口：

- `ai-learn/agent-advanced/README.md`

运行项目：

- `langchain_chain_demo`
- `vector_db_demo`
- `vector_db_qdrant_demo`
- `vector_db_chroma_demo`
- `advanced_rag_pipeline_demo`
- `internal_hybrid_rag_demo`

补充资料：

- `all-in-rag-main/`

## 第四层：LangGraph

当前入口：

- `ai-learn/agent-advanced/projects/langgraph_workflow_demo`
- `ai-agents-from-zero/22-25 LangGraph章节`
- `ai-agents-from-zero/案例与源码-3-LangGraph框架`

待新增主入口：

- `ai-learn/agent-advanced/langgraph-enterprise/`

必须补齐：

- checkpoint
- memory
- human in the loop
- streaming
- subgraph
- toolnode
- langgraph + rag

## 第五层：MCP

当前入口：

- `ai-agents-from-zero/20-MCP模型上下文协议.md`
- `ai-agents-from-zero/案例与源码-2-LangChain框架/11-mcp/`

待新增主入口：

- `ai-learn/agent-advanced/mcp/`

必须补齐：

- FastMCP server demo
- MCP client demo
- Agent + MCP demo
- LangGraph + MCP demo

## 第六层：Multi-Agent / Deep Research

当前入口：

- `ai-learn/agent-advanced/projects/multi_agent_team_demo`
- `ai-agents-from-zero/实战项目-深度研搜`
- `ai-agents-from-zero/deepsearch-agents-main`

待新增主入口：

- `ai-learn/agent-advanced/deep-research/`

必须补齐：

- 统一阅读路线
- minimal deep research demo
- 与 FastAPI / 前端 / eval 的整合

## 第七层：企业项目作品集

当前可用项目：

- 企业知识库：`internal_hybrid_rag_demo`
- 电商问数：`shopkeeper-agent-main`
- Deep Research：`deepsearch-agents-main`

待新增项目：

- 日本 SES 营业 Agent
- MCP Office Agent
- 面试准备 Agent
- 企业客服 Agent
- GitHub Review Agent

---

# 八、现有目录处理建议

## `ai-learn/llm-lab/`

保留。定位明确，不要移动。

建议补：

- `examples/retry_structured_output.py`
- `examples/streaming_chat_example.py`
- `examples/token_cost_tracking.py`

## `ai-learn/agent-lab/`

保留。定位为基础 Agent 和最小 demo。

建议补：

- `projects/tool_agent_demo` 增加 tool call 日志输出。
- `projects/workflow_agent` 增加耗时统计和失败分支。

## `ai-learn/agent-advanced/`

作为 2026 主扩展目录。

建议新增：

```text
ai-learn/agent-advanced/mcp/
ai-learn/agent-advanced/langgraph-enterprise/
ai-learn/agent-advanced/deep-research/
ai-learn/agent-advanced/business-agents/
ai-learn/agent-advanced/platform-template/
```

## `ai-agents-from-zero/`

不要直接混入主线。它是课程资料和完整项目来源库。

建议处理：

- 保留原目录。
- 在 `2026/目录索引.md` 中列为“source material”。
- 把 MCP、LangGraph 高级、Deep Research、Shopkeeper 项目映射到 `agent-advanced`。

## `all-in-rag-main/`

保留为 RAG 专项资料库。

建议处理：

- 不移动。
- 从中抽取高级 RAG 主题到 `ai-learn/agent-advanced/rag/advanced-patterns/`。

## `hello-agents-main/`

保留为 Agent 案例参考库。

建议处理：

- 不作为主线。
- 从 Co-creation projects 中挑选 CodeReview、DatabaseAgent、EmailSmartAssistant 等作为业务 Agent 参考。

---

# 九、最小可执行重规划任务

如果只做一轮整理，建议按下面顺序：

1. 新增 `2026/README.md`，声明 2026 主线入口。
2. 新增 `2026/2026-能力地图.md`，把能力点映射到现有目录。
3. 新增 `ai-learn/agent-advanced/mcp/README.md`，链接现有 MCP 文档和源码。
4. 新增 `ai-learn/agent-advanced/langgraph-enterprise/README.md`，链接现有 LangGraph 高级源码和 DeepAgents HITL。
5. 新增 `ai-learn/agent-advanced/deep-research/README.md`，把深度研搜项目纳入主线。
6. 新增 `ai-learn/agent-advanced/business-agents/README.md`，定义日本 SES、面试、Office、客服、GitHub 项目。
7. 先实现 `japan_ses_matching_agent` 最小版。
8. 再实现 `langgraph_mcp_agent_demo`。

---

# 十、最终目录目标

整理完成后，`ai-lab` 应该变成下面这种关系：

```text
llm-lab
  负责：基础 LLM 应用能力

agent-lab
  负责：基础 Agent 与最小可运行 demo

agent-advanced
  负责：2026 高级能力与企业项目

ai-agents-from-zero / all-in-rag-main / hello-agents-main
  负责：课程资料、外部项目、深度参考

2026
  负责：总路线、能力地图、目录索引、项目任务板
```

最终补齐后，2026 目标清单应该全部能在仓库中找到对应关系：

| 目标 | 应有落点 |
|---|---|
| LCEL / LangChain 1.x | `ai-learn/agent-advanced/projects/langchain_chain_demo` |
| RAG 2.0 | `ai-learn/agent-advanced/rag/advanced-patterns` |
| LangGraph | `ai-learn/agent-advanced/langgraph-enterprise` |
| MCP | `ai-learn/agent-advanced/mcp` |
| Multi-Agent | `ai-learn/agent-advanced/projects/multi_agent_team_demo` + `deep-research` |
| Deep Research | `ai-learn/agent-advanced/deep-research` |
| 企业知识库 | `ai-learn/agent-advanced/business-agents/enterprise_knowledge_agent` |
| 日本 SES | `ai-learn/agent-advanced/business-agents/japan_ses_matching_agent` |
| 面试 Agent | `ai-learn/agent-advanced/business-agents/interview_coach_agent` |
| MCP Office | `ai-learn/agent-advanced/business-agents/mcp_office_agent` |
| 工程化交付 | `ai-learn/agent-advanced/platform-template` |

