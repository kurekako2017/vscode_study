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
| [langchain_chain_demo](./langchain_chain_demo/README.md) | LangChain 链式编排 | Prompt 模板、Runnable 组合、输出解析 | `/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/langchain_chain_demo/main.py "你想问的问题" --mock` |
| [langgraph_workflow_demo](./langgraph_workflow_demo/README.md) | LangGraph 工作流 | State、Node、Edge、条件分支、循环 | `/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/langgraph_workflow_demo/main.py "LangGraph 适合什么场景"` |
| [advanced_rag_pipeline_demo](./advanced_rag_pipeline_demo/README.md) | 高级 RAG | 切分、检索、重排、引用、答案合成 | `/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/advanced_rag_pipeline_demo/main.py "LangGraph 适合什么场景？"` |
| [internal_hybrid_rag_demo](./internal_hybrid_rag_demo/README.md) | 社内文件 + Wiki 混合检索 | 接入层、检索层、权限层、引用层 | `/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/internal_hybrid_rag_demo/main.py "远程办公和发布流程有什么要求？" --role employee` |
| [llamaindex_index_demo](./llamaindex_index_demo/README.md) | LlamaIndex 概念版索引 | Document、Node、Index、QueryEngine | `/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/llamaindex_index_demo/main.py "LlamaIndex 和 LangChain 有什么区别？"` |
| [multi_agent_team_demo](./multi_agent_team_demo/README.md) | 多 Agent 协作 | Planner、Researcher、Writer、Critic、Supervisor | `/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/multi_agent_team_demo/main.py "如何学习 LangGraph 和高级 RAG"` |
| [vector_db_demo](./vector_db_demo/README.md) | 向量数据库最小教学版 | 文本向量化、collection、相似度检索、top-k 召回 | `/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/vector_db_demo/main.py "怎么申请出差报销？"` |

## 专题代码区

| 目录 | 主题 | 你会学到什么 |
| --- | --- | --- |
| [../frontend](../frontend/README.md) | 前端专题 | React UI 壳、消息流、来源展示 |
| [../eval](../eval/README.md) | 评估专题 | RAG 命中率、引用覆盖率、本地评估报告 |
| [../deployment](../deployment/README.md) | 部署专题 | Docker、环境变量、最小可容器化服务 |

## 目录阅读建议

先跑代码，再回来看文档：

1. `langchain_chain_demo/`
2. `langgraph_workflow_demo/`
3. `advanced_rag_pipeline_demo/`
4. `internal_hybrid_rag_demo/`
5. `llamaindex_index_demo/`
6. `multi_agent_team_demo/`
7. `vector_db_demo/`
8. `../frontend/chat_ui_demo/`
9. `../eval/rag_eval_demo/`
10. `../deployment/container_demo/`

每个目录里的 `README.md` 都只讲这一小段代码，不会把所有概念混在一起。

## 函数调用总览

- [项目函数调用流程说明](./FUNCTION_FLOW.md) - 按文件梳理每个 demo 的入口、调用链和关键名词

## 依赖总表

- [项目依赖总表](./DEPENDENCIES.md) - 按 demo 统一整理第三方依赖和安装方式
