# projects

这里放可运行 demo。

建议每个 demo 都具备：

- `README.md`
- `requirements.txt` 或 `package.json`
- `main.py` / `src/`
- 运行脚本
- 最小测试或 smoke check

## 现有示例

| 目录 | 主题 | 你会学到什么 | 运行命令 |
| --- | --- | --- | --- |
| [langchain_chain_demo](./langchain_chain_demo/README.md) | LangChain 链式编排 | Prompt 模板、Runnable 组合、输出解析 | `python3 main.py "你想问的问题" --mock` |
| [langgraph_workflow_demo](./langgraph_workflow_demo/README.md) | LangGraph 工作流 | State、Node、Edge、条件分支、循环 | `python3 main.py "LangGraph 适合什么场景"` |
| [advanced_rag_pipeline_demo](./advanced_rag_pipeline_demo/README.md) | 高级 RAG | 切分、检索、重排、引用、答案合成 | `python3 main.py "LangGraph 适合什么场景？"` |
| [internal_hybrid_rag_demo](./internal_hybrid_rag_demo/README.md) | 社内文件 + Wiki 混合检索 | 接入层、检索层、权限层、引用层 | `python3 main.py "远程办公和发布流程有什么要求？" --role employee` |
| [llamaindex_index_demo](./llamaindex_index_demo/README.md) | LlamaIndex 概念版索引 | Document、Node、Index、QueryEngine | `python3 main.py "LlamaIndex 和 LangChain 有什么区别？"` |
| [multi_agent_team_demo](./multi_agent_team_demo/README.md) | 多 Agent 协作 | Planner、Researcher、Writer、Critic、Supervisor | `python3 main.py "如何学习 LangGraph 和高级 RAG"` |

## 目录阅读建议

先跑代码，再回来看文档：

1. `langchain_chain_demo/`
2. `langgraph_workflow_demo/`
3. `advanced_rag_pipeline_demo/`
4. `internal_hybrid_rag_demo/`
5. `llamaindex_index_demo/`
6. `multi_agent_team_demo/`

每个目录里的 `README.md` 都只讲这一小段代码，不会把所有概念混在一起。
