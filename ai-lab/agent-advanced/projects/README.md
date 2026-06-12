# projects

这里放可运行 demo。

建议每个 demo 都具备：

- `README.md`
- `requirements.txt` 或 `package.json`
- `main.py` / `src/`
- 运行脚本
- 最小测试或 smoke check

## 章节链接

- [学习路线 + 选择建议](#学习路线--demo-选择建议)
- [现有示例](#现有示例)
- [专题代码区](#专题代码区)
- [目录阅读建议](#目录阅读建议)
- [函数调用总览](#函数调用总览)
- [依赖总表](#依赖总表)

## 学习路线 + Demo 选择建议

### 适用对象

- 第一次进入 `projects/` 的人
- 想先按目标挑 demo 的人
- 想先跑代码，再回头看文档的人

### 推荐顺序

如果你是第一次进入 `projects/`，建议按下面的顺序学：

1. 先看 `langchain_chain_demo/`
2. 再看 `langgraph_workflow_demo/`
3. 接着看 `advanced_rag_pipeline_demo/`
4. 然后看 `internal_hybrid_rag_demo/`
5. 再看 `llamaindex_index_demo/`
6. 最后看 `multi_agent_team_demo/`
7. 向量库相关先看 `vector_db_demo/`
8. 想接真实服务，再看 `vector_db_qdrant_demo/` 和 `vector_db_chroma_demo/`

### 按目标选择

如果你是按“目标”来选 demo，可以直接参考下面这个表：

| 你的目标 | 优先看哪个 demo | 原因 |
| --- | --- | --- |
| 先把链式调用看懂 | `langchain_chain_demo/` | 最容易理解 prompt -> model -> parser 的最短路径 |
| 想理解工作流、分支、循环 | `langgraph_workflow_demo/` | 能直接看到 state / node / edge 的组织方式 |
| 想学 RAG 的完整过程 | `advanced_rag_pipeline_demo/` | 适合看切分、召回、重排、引用怎么串起来 |
| 想做企业内部知识库 | `internal_hybrid_rag_demo/` | 适合看多来源资料、权限过滤、引用输出 |
| 想理解 LlamaIndex 的概念 | `llamaindex_index_demo/` | 适合先建立 Document / Node / Index 的心智模型 |
| 想做多 Agent 协作 | `multi_agent_team_demo/` | 适合看 Planner / Researcher / Writer / Critic 的协作 |
| 想先理解向量检索 | `vector_db_demo/` | 适合先看最小向量库原理，不依赖外部服务 |
| 想接真实 Qdrant | `vector_db_qdrant_demo/` | 适合本机 Docker 或远端 Qdrant 接入 |
| 想接真实 Chroma | `vector_db_chroma_demo/` | 适合本地持久化原型和快速实验 |

### 快速判断

- 想“先看懂原理”，先跑 `vector_db_demo/` 和 `langchain_chain_demo/`
- 想“先看流程”，先跑 `langgraph_workflow_demo/` 和 `advanced_rag_pipeline_demo/`
- 想“先看真实接入”，直接看 `vector_db_qdrant_demo/` 或 `vector_db_chroma_demo/`

如果你想更快一点选路，可以直接按下面三条来：

### 最快上手

先跑这两个：

1. `langchain_chain_demo/`
2. `vector_db_demo/`

它们最适合用来先建立“链式调用”和“向量检索”的基本感觉。

### 想做项目

先跑这三个：

1. `advanced_rag_pipeline_demo/`
2. `internal_hybrid_rag_demo/`
3. `multi_agent_team_demo/`

它们更接近完整业务流程，适合做成可演示、可扩展的项目。

### 想接真实服务

先跑这两个：

1. `vector_db_qdrant_demo/`
2. `vector_db_chroma_demo/`

它们更像正式工程接入模板，适合后面接 Docker、远端服务、真实知识库。

如果你现在还不知道从哪里开始，默认就按这个顺序走：

1. `langchain_chain_demo/`
2. `vector_db_demo/`
3. `langgraph_workflow_demo/`
4. `advanced_rag_pipeline_demo/`
5. `vector_db_qdrant_demo/`
6. `vector_db_chroma_demo/`

## 现有示例

| 目录 | 主题 | 你会学到什么 | 运行命令 |
| --- | --- | --- | --- |
| [langchain_chain_demo](./langchain_chain_demo/README.md) | LangChain 链式编排 | Prompt 模板、Runnable 组合、输出解析、Tool / Memory / RAG 入门 | `/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/langchain_chain_demo/main.py "你想问的问题" --mock` |
| [langgraph_workflow_demo](./langgraph_workflow_demo/README.md) | LangGraph 工作流 | State、Node、Edge、条件分支、循环 | `/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/langgraph_workflow_demo/main.py "LangGraph 适合什么场景"` |
| [advanced_rag_pipeline_demo](./advanced_rag_pipeline_demo/README.md) | 高级 RAG | 切分、检索、重排、引用、答案合成 | `/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/advanced_rag_pipeline_demo/main.py "LangGraph 适合什么场景？"` |
| [internal_hybrid_rag_demo](./internal_hybrid_rag_demo/README.md) | 社内文件 + Wiki 混合检索 | 接入层、检索层、权限层、引用层 | `/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/internal_hybrid_rag_demo/main.py "远程办公和发布流程有什么要求？" --role employee` |
| [llamaindex_index_demo](./llamaindex_index_demo/README.md) | LlamaIndex 概念版索引 | Document、Node、Index、QueryEngine | `/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/llamaindex_index_demo/main.py "LlamaIndex 和 LangChain 有什么区别？"` |
| [multi_agent_team_demo](./multi_agent_team_demo/README.md) | 多 Agent 协作 | Planner、Researcher、Writer、Critic、Supervisor | `/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/multi_agent_team_demo/main.py "如何学习 LangGraph 和高级 RAG"` |
| [vector_db_demo](./vector_db_demo/README.md) | 向量数据库最小教学版 | 文本向量化、collection、相似度检索、top-k 召回 | `/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/vector_db_demo/main.py "怎么申请出差报销？"` |
| [vector_db_qdrant_demo](./vector_db_qdrant_demo/README.md) | 真实 Qdrant 版骨架 | Qdrant Client、collection、payload、upsert、search | `/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/vector_db_qdrant_demo/main.py "怎么申请出差报销？"` |
| [vector_db_chroma_demo](./vector_db_chroma_demo/README.md) | 真实 Chroma 版骨架 | Chroma Client、collection、metadata、upsert、query | `/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/vector_db_chroma_demo/main.py "怎么申请出差报销？"` |

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
8. `vector_db_qdrant_demo/`
9. `vector_db_chroma_demo/`
10. `../frontend/chat_ui_demo/`
11. `../eval/rag_eval_demo/`
12. `../deployment/container_demo/`

每个目录里的 `README.md` 都只讲这一小段代码，不会把所有概念混在一起。

## 函数调用总览

- [项目函数调用流程说明](./FUNCTION_FLOW.md) - 按文件梳理每个 demo 的入口、调用链和关键名词

## 依赖总表

- [项目依赖总表](./DEPENDENCIES.md) - 按 demo 统一整理第三方依赖和安装方式
