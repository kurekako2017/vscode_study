# Agent Advanced

`agent-advanced/` 是 `ai-lab` 里更高阶的一条学习线，目标是把基础 Agent、RAG 和后端集成继续往工程化方向推进。

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

## 推荐入口

1. [学习路线](./学习路线.md)
2. [核心技术栈总览](./核心技术栈总览.md)
3. [projects/](./projects/README.md) 里的可运行案例
4. `frameworks/` 下的框架专题
5. `rag/` 下的高级检索专题
6. `multi-agent/` 下的多 Agent 专题

## 先看什么

如果你是第一次进入这个目录，建议按这个顺序：

1. 先看 [学习路线](./学习路线.md)，知道这条线怎么学
2. 再看 [核心技术栈总览](./核心技术栈总览.md)，知道现在缺什么、补什么
3. 打开 [projects/README.md](./projects/README.md)，直接跑最小可运行 demo
4. 回到 `frameworks/`、`rag/`、`multi-agent/` 里补概念和对比

## 可运行案例

| 目录 | 主题 | 运行方式 |
| --- | --- | --- |
| [projects/langchain_chain_demo](./projects/langchain_chain_demo/README.md) | LangChain 链式编排、Prompt、输出解析 | `python3 main.py "..." --mock` |
| [projects/langgraph_workflow_demo](./projects/langgraph_workflow_demo/README.md) | LangGraph 状态图、分支、循环 | `python3 main.py "..."` |
| [projects/advanced_rag_pipeline_demo](./projects/advanced_rag_pipeline_demo/README.md) | 高级 RAG、切分、检索、rerank、引用 | `python3 main.py "..."` |
| [projects/internal_hybrid_rag_demo](./projects/internal_hybrid_rag_demo/README.md) | 社内文件 + Wiki 混合检索、权限过滤、引用 | `python3 main.py "..." --role employee` |
| [projects/llamaindex_index_demo](./projects/llamaindex_index_demo/README.md) | LlamaIndex 风格的索引和查询引擎概念 | `python3 main.py "..."` |
| [projects/multi_agent_team_demo](./projects/multi_agent_team_demo/README.md) | 多 Agent 协作、监督者、规划者、审校者 | `python3 main.py "..."` |

## 未来会放什么

- 框架对比笔记
- 高级 RAG 管线拆解
- 社内文件 + Wiki 混合检索
- 多 Agent 协调模式
- React 客户端与 API 的联调
- 评估体系、Tracing、日志、成本控制
- Docker、CI/CD、部署说明
