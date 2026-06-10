# projects 依赖总表

这份清单把 `agent-advanced/projects/` 下所有 demo 的第三方依赖统一整理到一起，方便一次安装或按需查阅。

## 一键安装

```bash
/usr/bin/python3 -m pip install -r requirements.txt
```

## 依赖总览

| 目录 | 依赖 | 说明 |
| --- | --- | --- |
| `langchain_chain_demo/` | `langchain-core`、`langchain-openai` | LangChain 链式编排，mock 模式可不依赖真实模型，但导入层仍需要 `langchain-core` |
| `langgraph_workflow_demo/` | `langgraph` | LangGraph 状态图 demo |
| `advanced_rag_pipeline_demo/` | `langchain-core`、`langchain-text-splitters` | 文档切分和检索流水线 |
| `internal_hybrid_rag_demo/` | 无第三方依赖 | 仅使用 Python 标准库 |
| `llamaindex_index_demo/` | 无第三方依赖 | 仅使用 Python 标准库 |
| `multi_agent_team_demo/` | 无第三方依赖 | 仅使用 Python 标准库 |
| `vector_db_demo/` | 无第三方依赖 | 仅使用 Python 标准库，教学版向量数据库风格模拟 |
| `deployment/container_demo/` | 无第三方依赖 | 服务本身仅使用标准库；如果你想用 `uvicorn` 启动 ASGI 服务，可以额外安装 `uvicorn` |
| `eval/rag_eval_demo/` | 无第三方依赖 | 仅使用 Python 标准库 |

## 各 demo 说明

### 1. `langchain_chain_demo`

- 主依赖：`langchain-core`、`langchain-openai`
- 作用：
  - `langchain-core` 提供 `ChatPromptTemplate`、`RunnableLambda`、`AIMessage`
  - `langchain-openai` 用于真实模式下的 `ChatOpenAI`

### 2. `langgraph_workflow_demo`

- 主依赖：`langgraph`
- 作用：
  - 提供 `StateGraph`、`START`、`END`
  - 用于演示状态图、条件分支和循环

### 3. `advanced_rag_pipeline_demo`

- 主依赖：`langchain-core`、`langchain-text-splitters`
- 作用：
  - `langchain-core` 提供 `Document`
  - `langchain-text-splitters` 提供 `RecursiveCharacterTextSplitter`

### 4. `internal_hybrid_rag_demo`

- 无第三方依赖
- 说明：
  - 全部逻辑基于标准库
  - 读取本地资产文件并模拟企业知识库检索

### 5. `llamaindex_index_demo`

- 无第三方依赖
- 说明：
  - 用标准库模拟 `Document -> Node -> Index -> QueryEngine` 的概念

### 6. `multi_agent_team_demo`

- 无第三方依赖
- 说明：
  - 用标准库模拟 Planner / Researcher / Writer / Critic / Supervisor 的协作流程

### 7. `deployment/container_demo`

- 默认无第三方依赖
- 可选依赖：`uvicorn`
- 说明：
  - `python main.py` 可直接运行
  - 如果你想用 ASGI 方式启动或集成其他服务，再装 `uvicorn`

### 8. `eval/rag_eval_demo`

- 无第三方依赖
- 说明：
  - 用标准库做最小 RAG 评估

### 9. `vector_db_demo`

- 无第三方依赖
- 说明：
  - 用标准库模拟 Qdrant / Chroma / Memory 风格的 collection、向量写入和相似度检索

## 说明

- 这里的 `requirements.txt` 是“统一安装包”，适合先把演示环境铺齐。
- 如果你只想跑单个 demo，也可以只安装它自己的依赖。
- `langchain_chain_demo` 现在支持缺包时走本地兼容实现，但为了统一环境，仍建议安装 `langchain-core`。
