# All-in-RAG 启动速查

这份短文档保留最常用的启动命令，并在每组命令上方标明“在练什么”。
如果你要看完整学习导航、章节索引和模块说明，请打开 [QUICKSTART.md](./QUICKSTART.md)。

原则：先把命令跑通，再逐步补真实依赖和完整实现。

## 1. 基础准备

练习内容：把本地 Python 环境和依赖装起来，确认仓库能进入可运行状态。

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/all-in-rag-main
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r code/requirements.txt
```

## 2. 环境变量

练习内容：准备最少可运行环境，尤其是模型和服务地址。

```bash
cp .env.example .env
```

至少补这两个：

```bash
OPENROUTER_API_KEY=your_key
OPENROUTER_MODEL=openai/gpt-4o-mini
```

## 3. Chapter 1 到 Chapter 6

练习内容：按章节学习 RAG 的基础组件、切分、检索、路由、结构化输出和评估。

### Chapter 1

LangChain 和 LlamaIndex 入门，练最小链式调用和索引查询。

```bash
python3 run.py c1-1
python3 run.py c1-2
python3 run.py c1-fix
```

- `c1-1` -> `C1/01_langchain_example.py`：LangChain 最小示例，练基础链式调用。
- `c1-2` -> `C1/02_llamaIndex_example.py`：LlamaIndex 最小示例，练索引和检索查询。
- `c1-fix` -> `C1/fix_nltk.py`：修复或下载 NLTK 资源，避免分词相关报错。

### Chapter 2

文本切分练习，理解字符切分、递归切分和语义切分。

```bash
python3 run.py c2-1
python3 run.py c2-2
python3 run.py c2-3
python3 run.py c2-4
```

- `c2-1` -> `C2/01_unstructured_example.py`：处理不同格式文本，练 `unstructured` 的基础用法。
- `c2-2` -> `C2/02_character_splitter.py`：按固定字符长度切分文本。
- `c2-3` -> `C2/03_recursive_character_splitter.py`：递归切分，尽量保留段落和语义边界。
- `c2-4` -> `C2/04_semantic_chunker.py`：按语义相似度切块，更贴近检索场景。

### Chapter 3

向量检索和多模态检索练习，包含 FAISS、Milvus、句窗检索和递归检索。

```bash
python3 run.py c3-1
python3 run.py c3-2
python3 run.py c3-3
python3 run.py c3-4
python3 run.py c3-5
python3 run.py c3-6
python3 run.py c3-7
python3 run.py c3-download
python3 run.py c3-dragon
python3 run.py c3-hybrid
```

- `c3-1` -> `C3/01_bge_visualized.py`：可视化 BGE 向量空间，理解嵌入分布。
- `c3-2` -> `C3/02_langchain_faiss.py`：用 LangChain + FAISS 做本地向量检索。
- `c3-3` -> `C3/03_llamaindex_vector.py`：用 LlamaIndex 构建和查询向量索引。
- `c3-4` -> `C3/04_multi_milvus.py`：演示 Milvus 多集合或多向量检索。
- `c3-5` -> `C3/05_sentence_window_retrieval.py`：句窗检索，保留上下文回答。
- `c3-6` -> `C3/06_recursive_retrieval.py`：递归检索，按层次追踪相关内容。
- `c3-7` -> `C3/07_recursive_retrieval_v2.py`：递归检索的增强版。
- `c3-download` -> `C3/download_model.py`：下载嵌入或多模态模型权重。
- `c3-dragon` -> `C3/work_multimodal_dragon_search.py`：多模态 Dragon Search 练习。
- `c3-hybrid` -> `C3/work_hybrid_multimodal_search.py`：多模态混合检索练习。

### Chapter 4

混合检索、路由和 Text2SQL 练习。

```bash
python3 run.py c4-1
python3 run.py c4-1v2
python3 run.py c4-2
python3 run.py c4-3
python3 run.py c4-3v2
python3 run.py c4-4
python3 run.py c4-5
python3 run.py c4-6
python3 run.py c4-7
python3 run.py c4-work
```

- `c4-1` -> `C4/01_hybrid_search.py`：关键词检索和向量检索结合。
- `c4-1v2` -> `C4/01_hybrid_search_v2.py`：混合检索的改进版。
- `c4-2` -> `C4/02_text_to_metadata_filter.py`：把自然语言转成元数据过滤条件。
- `c4-3` -> `C4/03_text2sql_demo.py`：Text2SQL 基础演示，把问题转成 SQL。
- `c4-3v2` -> `C4/03_text2sql_demo_v2.py`：Text2SQL 改进版。
- `c4-4` -> `C4/04_text_to_metadata_filter_v2.py`：元数据过滤的增强版。
- `c4-5` -> `C4/05_llm_based_routing.py`：用大模型判断走哪条检索路径。
- `c4-6` -> `C4/06_embedding_based_routing.py`：用向量相似度做路由。
- `c4-7` -> `C4/07_rerank_and_refine.py`：先重排，再精炼答案。
- `c4-work` -> `C4/work_rerank_and_refine.py`：重排与精炼的工作版入口。

### Chapter 5

结构化输出和函数调用练习。

```bash
python3 run.py c5-1
python3 run.py c5-2
```

- `c5-1` -> `C5/01_pydantic.py`：用 Pydantic 约束模型输出格式。
- `c5-2` -> `C5/02_function_calling_example.py`：函数调用示例，练工具调用范式。

### Chapter 6

评估练习，理解怎么给 RAG 或问答系统做验证。

```bash
python3 run.py c6-1
```

- `c6-1` -> `C6/01_llamaindex_evaluation_example.py`：LlamaIndex 评估示例，练回答质量验证。

## 4. 完整项目入口

练习内容：把单文件实验串成完整项目，感受端到端流程。

### Chapter 8: 食谱 RAG 系统

练习点：食谱数据处理、向量索引、检索和生成整合。

```bash
python3 run.py c8
```

- `c8` -> `C8/main.py`：食谱 RAG 项目总入口，串起预处理、索引、检索和生成。

### Chapter 9: 图 RAG 系统

练习点：图数据、Milvus、Neo4j 和混合检索整合。

```bash
python3 run.py c9
```

- `c9` -> `C9/main.py`：图 RAG 项目总入口，练图数据和向量检索联动。

## 5. C9 Agent

练习内容：菜谱知识抽取、批次管理和图谱生成。

```bash
python3 run.py c9-agent-test
python3 run.py c9-agent-run /path/to/recipes
python3 run.py c9-agent-status
python3 run.py c9-agent-continue /path/to/recipes
python3 run.py c9-agent-merge
python3 run.py c9-agent-details
```

- `c9-agent-test` -> `C9/agent(代码系ai生成)/run_ai_agent.py`：跑一个测试批次，验证抽取流程。
- `c9-agent-run` -> `C9/agent(代码系ai生成)/run_ai_agent.py`：对指定菜谱目录执行批处理抽取。
- `c9-agent-status` -> `C9/agent(代码系ai生成)/batch_manager.py`：查看批次状态。
- `c9-agent-continue` -> `C9/agent(代码系ai生成)/batch_manager.py`：从中断处继续处理。
- `c9-agent-merge` -> `C9/agent(代码系ai生成)/batch_manager.py`：合并批次结果。
- `c9-agent-details` -> `C9/agent(代码系ai生成)/batch_manager.py`：查看批次详情。

## 6. PowerRAG

练习内容：连接外部 RAGFlow / PowerRAG 服务做文本问答检索。

```bash
python3 run.py powerrag --file ../data/sample.md --question "退款规则是什么？"
```

- `powerrag` -> `Extra-chapter/PowerRAG-SDK-Text-QA/code/main.py`：把文档送进 PowerRAG 服务做检索问答。

## 7. 分组运行

练习内容：按章节一次跑一整组，快速验证依赖是否完整。

```bash
python3 run.py c1
python3 run.py c2
python3 run.py c3
python3 run.py c4
python3 run.py c5
python3 run.py c6
python3 run.py c8
python3 run.py c9
```

- `c1`：Chapter 1 整组，练基础库入门。
- `c2`：Chapter 2 整组，练文本切分。
- `c3`：Chapter 3 整组，练向量检索和多模态检索。
- `c4`：Chapter 4 整组，练混合检索、路由和 Text2SQL。
- `c5`：Chapter 5 整组，练结构化输出和函数调用。
- `c6`：Chapter 6 整组，练评估。
- `c8`：Chapter 8 整组，练食谱 RAG 项目。
- `c9`：Chapter 9 整组，练图 RAG 项目。

如果你要看更完整的章节说明、每个脚本的具体作用，去 [QUICKSTART.md](./QUICKSTART.md)。
