# Agent Advanced

`agent-advanced/` 是 `ai-lab` 里更高阶的一条学习线，目标是把基础 Agent、RAG 和后端集成继续往工程化方向推进。

## 章节链接

- [学习定位](#agent-advanced)
- [目录分工](#和现有目录的分工)
- [目录约定](#目录约定)
- [学习路线 + 选择建议](#学习路线--入口建议)
- [先看什么](#先看什么)
- [可运行案例](#可运行案例)
- [专题代码](#专题代码)
- [未来会放什么](#未来会放什么)

这里已经不是“只有笔记”的目录了，而是分成两层：

- `frameworks/`、`rag/`、`multi-agent/`、`frontend/`、`eval/`、`deployment/`：学习文档和路线图
- `projects/`：可运行的代码案例，每个案例都配了自己的 `README.md` 和 `main.py`

这个目录主要面向这些主题：

- LangChain
- LlamaIndex
- LangGraph
- 高级 RAG
- 多 Agent 设计
- React 前端客户端
- FastAPI / Python 服务层
- 评估、日志、Tracing、部署

## 和现有目录的分工

| 目录 | 重点 |
| --- | --- |
| [../llm-lab](../llm-lab/README.md) | 模型调用、结构化输出、基础 RAG、FastAPI、评估 |
| [../agent-lab](../agent-lab/README.md) | Tool Calling、Agent 工作流、最小可运行 demo |
| [./](./README.md) | LangChain / LlamaIndex / LangGraph / 高级 RAG / 多 Agent / React 客户端 |

## 目录约定

- 每个技术栈单独一个章节
- 每个章节先有说明文档，再有一个或多个可运行 demo
- React 客户端、Python 服务、测试和部署示例分开维护
- 尽量保留“学习笔记”和“可运行项目”两条线

## 学习路线 + 入口建议

### 适用对象

- 第一次进入 `agent-advanced/` 的人
- 想先看清“学习路线、工程流程、可运行 demo”三层关系的人
- 需要在文档和代码之间快速切换的人

### 推荐顺序

如果你是第一次进入 `agent-advanced/`，建议按这个顺序看：

1. 先看 [学习路线](./学习路线.md)，知道这条线怎么学
2. 再看 [核心技术栈总览](./核心技术栈总览.md)，知道现在缺什么、补什么
3. 接着看 [开发测试部署流程](./开发测试部署流程.md)，把测试和上线顺序先记住
4. 再看 [交付前检查清单](./交付前检查清单.md)，知道交付前要检查什么
5. 打开 [projects/README.md](./projects/README.md)，先从最短路径跑 demo
6. 回到 `frameworks/`、`rag/`、`multi-agent/` 里补概念和对比

如果你是按“目标”来选入口，可以直接参考下面这个表：

| 你的目标 | 优先看哪个入口 | 原因 |
| --- | --- | --- |
| 先把整体学习路线看懂 | [学习路线](./学习路线.md) | 最适合先建立目录级别的学习顺序 |
| 想知道当前缺什么、补什么 | [核心技术栈总览](./核心技术栈总览.md) | 适合先做能力盘点 |
| 想先把测试和上线顺序搞清楚 | [开发测试部署流程](./开发测试部署流程.md) | 适合先建立工程化意识 |
| 想先确认交付前要查什么 | [交付前检查清单](./交付前检查清单.md) | 适合把容易漏的项先固定住 |
| 想先跑一个 demo | [projects/](./projects/README.md) | 最适合直接上手 |
| 想先补框架知识 | `frameworks/` | 适合先看 LangChain / LlamaIndex / LangGraph 对比 |
| 想先补 RAG 知识 | `rag/` | 适合看高级检索和混合检索专题 |
| 想先补多 Agent 知识 | `multi-agent/` | 适合看协作模式和调度方式 |

### 快速判断

- 想“先看懂全局结构”，先看学习路线和技术栈总览
- 想“先看工程流程”，先看开发测试部署流程和交付前检查清单
- 想“先上手代码”，直接进 [projects/](./projects/README.md)

如果你只想先跑一个 demo，不想做选择，默认从 [projects/README.md](./projects/README.md) 里推荐的最短路径开始：

1. `langchain_chain_demo/`
2. `vector_db_demo/`
3. `langgraph_workflow_demo/`

## 可运行案例

| 目录 | 主题 | 运行方式 |
| --- | --- | --- |
| [projects/langchain_chain_demo](./projects/langchain_chain_demo/README.md) | LangChain 链式编排、Prompt、输出解析 | `python3 main.py "..." --mock` |
| [projects/langgraph_workflow_demo](./projects/langgraph_workflow_demo/README.md) | LangGraph 状态图、分支、循环 | `python3 main.py "..."` |
| [projects/advanced_rag_pipeline_demo](./projects/advanced_rag_pipeline_demo/README.md) | 高级 RAG、切分、检索、rerank、引用 | `python3 main.py "..."` |
| [projects/internal_hybrid_rag_demo](./projects/internal_hybrid_rag_demo/README.md) | 社内文件 + Wiki 混合检索、权限过滤、引用 | `python3 main.py "..." --role employee` |
| [projects/llamaindex_index_demo](./projects/llamaindex_index_demo/README.md) | LlamaIndex 风格的索引和查询引擎概念 | `python3 main.py "..."` |
| [projects/multi_agent_team_demo](./projects/multi_agent_team_demo/README.md) | 多 Agent 协作、监督者、规划者、审校者 | `python3 main.py "..."` |
| [projects/vector_db_demo](./projects/vector_db_demo/README.md) | 向量数据库最小教学版、collection、相似度检索 | `python3 main.py "..." --backend qdrant` |
| [projects/vector_db_qdrant_demo](./projects/vector_db_qdrant_demo/README.md) | 真实 Qdrant 版骨架、collection、payload、search | `python3 main.py "..."` |
| [projects/vector_db_chroma_demo](./projects/vector_db_chroma_demo/README.md) | 真实 Chroma 版骨架、collection、metadata、query | `python3 main.py "..."` |

## 专题代码

| 目录 | 角色 | 说明 |
| --- | --- | --- |
| [frontend/](./frontend/README.md) | 前端专题区 | 这里放 Agent / RAG 前端接入说明和 React UI demo |
| [eval/](./eval/README.md) | 评估专题区 | 这里放 RAG / Agent 评估说明和本地评估脚本 |
| [deployment/](./deployment/README.md) | 部署专题区 | 这里放 Docker / 环境变量 / 发布方式示例 |

## 未来会放什么

- 框架对比笔记
- 高级 RAG 管线拆解
- 社内文件 + Wiki 混合检索
- 多 Agent 协调模式
- React 客户端与 API 的联调
- 评估体系、Tracing、日志、成本控制
- Docker、CI/CD、部署说明

## 2026 新增主线

- [LangGraph 企业能力](./langgraph-enterprise/README.md)：Checkpoint、Memory、HITL、Subgraph、Streaming
- [高级 RAG 标准模式](./rag/advanced-patterns/README.md)：Parent Document、Compression、HyDE、Corrective RAG
- [MCP](./mcp/README.md)：Client、Server、Remote、Multi-MCP
- [真实 Multi-Agent 图编排](./multi-agent/graph_team_demo/README.md)
- [Deep Research](./deep-research/README.md)
- [Tracing](./observability/README.md)
- [业务 Agent 作品集](./business-agents/README.md)

完成等级统一记录在 [../../2026/2026补齐实施状态.md](../../2026/2026补齐实施状态.md)。统一测试和 CI/CD 暂未实施。
