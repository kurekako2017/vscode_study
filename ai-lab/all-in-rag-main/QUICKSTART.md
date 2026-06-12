# All-in-RAG 学习与启动总览

这是一份合并版文档，整合了原来的 `QUICKSTART.md` 和 `RUNBOOK_SHORT.md`。
如果你想先跑起来，再补真实依赖、真实数据和完整版效果，就按这份文档走。

原则很简单：先保证命令跑通，再逐步补全实现。文档里出现的离线兼容、默认值和示例数据，都是为了“先可运行”。

## 章节导航

- [1. 基础准备](#base)
- [2. 环境变量](#env)
- [3. 本地服务](#services)
- [4. Chapter 1 到 Chapter 6](#core-chapters)
- [5. 完整项目入口](#full-apps)
- [6. C9 Agent 工具链](#agent)
- [7. Extra Chapter](#extra)
- [8. 推荐启动顺序](#order)
- [9. 现实限制](#limits)

## 文档关系

- `RUNBOOK_SHORT.md` 现在只保留为快捷入口，主内容以这份文档为准。
- 如果你从仓库根目录启动，优先看 [`run.py`](./run.py)。
- 如果你已经在 `code/` 目录里，`code/run.py` 也会接住同样的命令。

<a id="base"></a>
## 1. 基础准备

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/all-in-rag-main/code
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

如果你平时已经有全局 Python 环境，也可以直接用全局环境安装依赖，但这个仓库默认按 `code/` 目录内的运行方式组织。

仓库根目录和 `code/` 目录都放了 `sitecustomize.py`，只要你在任一目录下启动 Python，就会自动读取附近的 `.env`，并把 `OPENROUTER_*` 映射成兼容库可识别的变量。

如果你想偷懒，直接把 [.env.example](./.env.example) 复制成 `.env`，再填上真实 key 就行。

<a id="env"></a>
## 2. 环境变量

这些变量会被不同示例读取，建议先统一导出。

```bash
export OPENROUTER_API_KEY="你的 OpenRouter Key"
export RAGFLOW_BASE_URL="http://127.0.0.1:9380"
export RAGFLOW_API_KEY="你的 RAGFlow Key"
export OPENROUTER_MODEL="openai/gpt-4o-mini"
```

可选项：

```bash
export HF_ENDPOINT="https://hf-mirror.com"
export POWERRAG_BASE_URL="$RAGFLOW_BASE_URL"
export POWERRAG_API_KEY="$RAGFLOW_API_KEY"
```

<a id="services"></a>
## 3. 本地服务

### 3.1 Milvus

`code/docker-compose.yml` 提供了 Milvus 单机环境，`C3`、`C4`、`C9` 里很多示例会用到。

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/all-in-rag-main/code
docker compose -f docker-compose.yml up -d
```

常用访问地址：

```bash
curl -s http://localhost:8086/api/health
```

### 3.2 Neo4j

`data/C9/docker-compose.yml` 提供了 `C9` 图 RAG 示例使用的 Neo4j 环境。

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/all-in-rag-main/data/C9
docker compose up -d
```

默认账号密码：

```text
neo4j / all-in-rag
```

浏览器地址：

```text
http://127.0.0.1:7474
```

<a id="core-chapters"></a>
## 4. Chapter 1 到 Chapter 6

下面这些脚本是最适合拿来学习和验证的单文件示例。每个条目都写了文件名和它的作用，方便你按章节顺着看。

### Chapter 1: LangChain / LlamaIndex 入门

学习重点是“最小 RAG 组件长什么样”。

| 文件 | 作用 |
| --- | --- |
| `C1/01_langchain_example.py` | LangChain 最小示例，演示基础链式调用。 |
| `C1/02_llamaIndex_example.py` | LlamaIndex 最小示例，演示索引、检索和查询。 |
| `C1/fix_nltk.py` | 修复或下载 NLTK 资源，避免分词/停用词报错。 |

### Chapter 2: 文本切分

学习重点是“怎么把长文拆成可检索的块”。

| 文件 | 作用 |
| --- | --- |
| `C2/01_unstructured_example.py` | 使用 `unstructured` 处理不同格式文本。 |
| `C2/02_character_splitter.py` | 按固定字符长度切分文本。 |
| `C2/03_recursive_character_splitter.py` | 递归式字符切分，尽量保留语义边界。 |
| `C2/04_semantic_chunker.py` | 按语义相似度切块，更适合检索。 |

### Chapter 3: 向量检索与多模态检索

学习重点是“向量化、检索、以及图文混合场景”。

| 文件 | 作用 |
| --- | --- |
| `C3/01_bge_visualized.py` | 可视化 BGE 向量效果，帮助理解嵌入空间。 |
| `C3/02_langchain_faiss.py` | 用 LangChain + FAISS 做本地向量检索。 |
| `C3/03_llamaindex_vector.py` | 用 LlamaIndex 做向量索引和检索。 |
| `C3/04_multi_milvus.py` | 演示 Milvus 多向量/多集合检索。 |
| `C3/05_sentence_window_retrieval.py` | 句窗检索，让回答保留上下文。 |
| `C3/06_recursive_retrieval.py` | 递归检索，按层次追踪相关内容。 |
| `C3/07_recursive_retrieval_v2.py` | 递归检索的改进版。 |
| `C3/download_model.py` | 下载多模态或嵌入模型所需权重。 |
| `C3/work_multimodal_dragon_search.py` | 多模态 Dragon Search 示例。 |
| `C3/work_hybrid_multimodal_search.py` | 多模态混合检索示例。 |
| `C3/visual_bge/` | 视觉 BGE 的支持实现和模型封装，属于配套依赖目录。 |

### Chapter 4: 混合检索、路由和 Text2SQL

学习重点是“检索策略怎么组合成完整问答流程”。

| 文件 | 作用 |
| --- | --- |
| `C4/01_hybrid_search.py` | 混合检索示例，结合关键词和向量检索。 |
| `C4/01_hybrid_search_v2.py` | 混合检索的改进版。 |
| `C4/02_text_to_metadata_filter.py` | 把自然语言映射成元数据过滤条件。 |
| `C4/04_text_to_metadata_filter_v2.py` | 元数据过滤的增强版。 |
| `C4/03_text2sql_demo.py` | Text2SQL 演示，把问题转成 SQL。 |
| `C4/03_text2sql_demo_v2.py` | Text2SQL 的改进版。 |
| `C4/05_llm_based_routing.py` | 用大模型决定走哪条检索路径。 |
| `C4/06_embedding_based_routing.py` | 用向量相似度做路由。 |
| `C4/07_rerank_and_refine.py` | 先重排，再精炼答案。 |
| `C4/work_rerank_and_refine.py` | 重排与精炼的工作版入口。 |
| `C4/text2sql/knowledge_base.py` | Text2SQL 的数据库描述和样例知识库。 |
| `C4/text2sql/sql_generator.py` | 把自然语言转换为 SQL。 |
| `C4/text2sql/text2sql_agent.py` | Text2SQL 流程编排入口。 |

### Chapter 5: 结构化输出与函数调用

学习重点是“让模型输出可验证、可调用的结构化结果”。

| 文件 | 作用 |
| --- | --- |
| `C5/01_pydantic.py` | 用 Pydantic 约束和校验模型输出。 |
| `C5/02_function_calling_example.py` | 函数调用示例，演示工具调用范式。 |

### Chapter 6: 评估

学习重点是“怎么给 RAG 或问答系统做评估”。

| 文件 | 作用 |
| --- | --- |
| `C6/01_llamaindex_evaluation_example.py` | LlamaIndex 评估示例。 |
| `C6/c6_response_eval_dataset.json` | 评估数据集样例。 |

<a id="full-apps"></a>
## 5. 完整项目入口

这部分是“可以当成项目跑起来”的入口，不只是单文件实验。

### 5.1 Chapter 8: 食谱 RAG 系统

主入口：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/all-in-rag-main/code
python3 C8/main.py
```

核心文件：

| 文件 | 作用 |
| --- | --- |
| `C8/main.py` | 食谱 RAG 项目总入口。 |
| `C8/config.py` | 数据路径和运行配置。 |
| `C8/rag_modules/data_preparation.py` | 数据清洗、切分和预处理。 |
| `C8/rag_modules/index_construction.py` | 构建向量索引。 |
| `C8/rag_modules/retrieval_optimization.py` | 检索优化逻辑。 |
| `C8/rag_modules/generation_integration.py` | 检索结果与生成模型的集成。 |

注意：

- 默认数据目录是 `data/C8/cook`。
- 如果你的数据放在别处，先改 `code/C8/config.py` 里的 `data_path`，或者把数据放到这个目录下。
- 仓库已经补了可直接跑通的示例数据，不需要你先手工造空目录。
- 这个入口要求先有 `OPENROUTER_API_KEY`。

### 5.2 Chapter 9: 图 RAG 系统

主入口：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/all-in-rag-main/code
python3 C9/main.py
```

核心文件：

| 文件 | 作用 |
| --- | --- |
| `C9/main.py` | 图 RAG 项目总入口。 |
| `C9/config.py` | 图数据库、向量库和模型配置。 |
| `C9/rag_modules/graph_data_preparation.py` | 图数据准备。 |
| `C9/rag_modules/graph_indexing.py` | 图索引构建。 |
| `C9/rag_modules/milvus_index_construction.py` | Milvus 向量索引构建。 |
| `C9/rag_modules/graph_rag_retrieval.py` | 图检索流程。 |
| `C9/rag_modules/hybrid_retrieval.py` | 图检索和向量检索的混合策略。 |
| `C9/rag_modules/intelligent_query_router.py` | 智能路由器，决定查询走哪条链路。 |
| `C9/rag_modules/generation_integration.py` | 生成阶段整合。 |

注意：

- 先启动 Milvus 和 Neo4j。
- Neo4j 连接默认是 `bolt://localhost:7687`，账号密码默认是 `neo4j / all-in-rag`。
- 需要 `OPENROUTER_API_KEY`。

<a id="agent"></a>
## 6. C9 Agent 工具链

这个目录名里带括号，命令里要加引号。

```bash
cd "/home/victorkure/workspace/vscode_study/ai-lab/all-in-rag-main/code/C9/agent(代码系ai生成)"
export OPENROUTER_API_KEY="你的 OpenRouter Key"
python3 run_ai_agent.py test
python3 run_ai_agent.py /path/to/your/recipes
python3 batch_manager.py status
python3 batch_manager.py continue /path/to/your/recipes
python3 batch_manager.py merge
python3 batch_manager.py details
```

核心文件：

| 文件 | 作用 |
| --- | --- |
| `run_ai_agent.py` | 批量启动 AI 菜谱图谱抽取流程。 |
| `batch_manager.py` | 管理批次状态、继续处理、合并结果和查看详情。 |
| `recipe_ai_agent.py` | 菜谱知识抽取代理的核心逻辑。 |
| `amount_normalizer.py` | 食材数量和单位归一化。 |
| `config.json` | 运行配置。 |
| `AI_AGENT_README.md` | 这个子项目的说明文档。 |
| `recipe_ontology_design.md` | 菜谱本体设计说明。 |

<a id="extra"></a>
## 7. Extra Chapter

### 7.1 PowerRAG SDK 文本问答

这个示例只做检索，不做最终生成回答。它依赖外部可用的 RAGFlow / PowerRAG 服务。

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/all-in-rag-main/Extra-chapter/PowerRAG-SDK-Text-QA/code
pip install -r requirements.txt
python3 main.py \
  --file ../data/sample.md \
  --question "退款规则是什么？" \
  --top-k 5
```

核心文件：

| 文件 | 作用 |
| --- | --- |
| `main.py` | PowerRAG 文本问答入口。 |
| `config.py` | 服务地址和调用配置。 |
| `requirements.txt` | 该示例的依赖列表。 |

如果你已经把服务地址和 token 放进全局环境，也可以直接用环境变量驱动：

```bash
export RAGFLOW_BASE_URL="http://127.0.0.1:9380"
export RAGFLOW_API_KEY="你的 RAGFlow Key"
python3 main.py --file ../data/sample.md --question "排队规则是什么？"
```

### 7.2 Neo4j Simple Application

这个章节以文档讲解为主，没有单独的 Python 启动脚本。对应的可运行部分主要是 Neo4j 容器和 Cypher 导入流程。

| 文件 | 作用 |
| --- | --- |
| `Extra-chapter/Neo4J-Simple-Application/readme.md` | Neo4j 基础应用说明。 |

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/all-in-rag-main/data/C9
docker compose up -d
```

### 7.3 多模态 Embedding 练习

这个子目录是多模态向量实验，偏练习和扩展阅读。

| 文件 | 作用 |
| --- | --- |
| `Extra-chapter/multimodal-embedding-omni-practice/code/08_jina_embedding_omni.py` | Jina multimodal embedding 练习脚本。 |
| `Extra-chapter/multimodal-embedding-omni-practice/readme.md` | 该练习的说明。 |

<a id="order"></a>
## 8. 推荐启动顺序

1. 先让最小命令跑通，再补齐真实依赖和数据。
2. 先安装 Python 依赖。
3. 再启动 Milvus。
4. 再启动 Neo4j。
5. 然后跑 `C1` 到 `C6` 的单文件示例。
6. 最后跑 `C8`、`C9` 这种完整项目入口。
7. 如果要跑 `PowerRAG`，先确认你本机或内网已经有可用的 RAGFlow 服务。

<a id="limits"></a>
## 9. 现实限制

- `C3`、`C4`、`C6` 里很多脚本会连 Hugging Face / Milvus / 本地向量库，除了 `OPENROUTER_API_KEY` 之外，还要把相关服务启动好。
- `C9` 的完整图 RAG 方案同时依赖 Milvus 和 Neo4j。
- 如果你只是先看学习路径，可以先按本地兼容模式跑通，再逐步切回真实服务。
