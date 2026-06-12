# All-in-RAG 快速启动清单

这份清单面向本工作区里的 `ai-lab/all-in-rag-main`，目标是把可运行的代码入口、依赖的全局环境变量、以及需要先启动的本地服务整理到一起。

## 1. 基础准备

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/all-in-rag-main/code
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

如果你平时已经有全局 Python 环境，也可以直接用全局环境安装依赖，但这个仓库的代码默认按 `code/` 目录内的运行方式组织。

## 2. 需要先准备的全局环境变量

这些变量会被不同示例读取，建议先统一导出。

```bash
export OPENROUTER_API_KEY="你的 OpenRouter Key"
export RAGFLOW_BASE_URL="http://127.0.0.1:9380"
export RAGFLOW_API_KEY="你的 RAGFlow Key"
export OPENROUTER_MODEL="~openai/gpt-latest"
```

可选项：

```bash
export HF_ENDPOINT="https://hf-mirror.com"
export POWERRAG_BASE_URL="$RAGFLOW_BASE_URL"
export POWERRAG_API_KEY="$RAGFLOW_API_KEY"
```

## 3. 先启动本地服务

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

## 4. 单文件教程示例

下面这些脚本都可以直接运行，前提是依赖已安装、环境变量已设置好。

### Chapter 1

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/all-in-rag-main/code
python C1/01_langchain_example.py
python C1/02_llamaIndex_example.py
python C1/fix_nltk.py
```

### Chapter 2

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/all-in-rag-main/code
python C2/01_unstructured_example.py
python C2/02_character_splitter.py
python C2/03_recursive_character_splitter.py
python C2/04_semantic_chunker.py
```

### Chapter 3

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/all-in-rag-main/code
python C3/01_bge_visualized.py
python C3/02_langchain_faiss.py
python C3/03_llamaindex_vector.py
python C3/04_multi_milvus.py
python C3/05_sentence_window_retrieval.py
python C3/06_recursive_retrieval.py
python C3/07_recursive_retrieval_v2.py
python C3/download_model.py
python C3/work_multimodal_dragon_search.py
python C3/work_hybrid_multimodal_search.py
```

### Chapter 4

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/all-in-rag-main/code
python C4/01_hybrid_search.py
python C4/01_hybrid_search_v2.py
python C4/02_text_to_metadata_filter.py
python C4/04_text_to_metadata_filter_v2.py
python C4/05_llm_based_routing.py
python C4/06_embedding_based_routing.py
python C4/07_rerank_and_refine.py
python C4/work_rerank_and_refine.py
python C4/03_text2sql_demo.py
python C4/03_text2sql_demo_v2.py
```

### Chapter 5

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/all-in-rag-main/code
python C5/01_pydantic.py
python C5/02_function_calling_example.py
```

### Chapter 6

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/all-in-rag-main/code
python C6/01_llamaindex_evaluation_example.py
```

## 5. 完整项目入口

### 5.1 Chapter 8: 食谱 RAG 系统

主入口：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/all-in-rag-main/code
python C8/main.py
```

注意：

* 默认数据目录是 `data/C8/cook`。
* 如果你的数据放在别处，先改 `code/C8/config.py` 里的 `data_path`，或者把数据放到这个目录下。
* 这个入口要求先有 `OPENROUTER_API_KEY`。

### 5.2 Chapter 9: 图 RAG 系统

主入口：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/all-in-rag-main/code
python C9/main.py
```

注意：

* 先启动 Milvus 和 Neo4j。
* Neo4j 连接默认是 `bolt://localhost:7687`，账号密码默认是 `neo4j / all-in-rag`。
* 需要 `OPENROUTER_API_KEY`。

### 5.3 Chapter 9 的 AI 菜谱图谱生成器

这个目录名里带括号，命令里要加引号。

```bash
cd "/home/victorkure/workspace/vscode_study/ai-lab/all-in-rag-main/code/C9/agent(代码系ai生成)"
export OPENROUTER_API_KEY="你的 OpenRouter Key"
python run_ai_agent.py test
python run_ai_agent.py /path/to/your/recipes
python batch_manager.py status
python batch_manager.py continue /path/to/your/recipes
python batch_manager.py merge
python batch_manager.py details
```

## 6. Extra Chapter

### 6.1 PowerRAG SDK 文本问答

这个示例只做检索，不做最终生成回答。它依赖外部可用的 RAGFlow / PowerRAG 服务。

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/all-in-rag-main/Extra-chapter/PowerRAG-SDK-Text-QA/code
pip install -r requirements.txt
python main.py \
  --file ../data/sample.md \
  --question "退款规则是什么？" \
  --top-k 5
```

如果你已经把服务地址和 token 放进全局环境，也可以直接用环境变量驱动：

```bash
export RAGFLOW_BASE_URL="http://127.0.0.1:9380"
export RAGFLOW_API_KEY="你的 RAGFlow Key"
python main.py --file ../data/sample.md --question "排队规则是什么？"
```

### 6.2 Neo4j 简单应用

这个章节以文档讲解为主，没有单独的 Python 启动脚本。对应的可运行部分主要是 Neo4j 容器和 Cypher 导入流程：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/all-in-rag-main/data/C9
docker compose up -d
```

## 7. 推荐启动顺序

1. 先安装 Python 依赖。
2. 再启动 Milvus。
3. 再启动 Neo4j。
4. 然后跑 `C1` 到 `C6` 的单文件示例。
5. 最后跑 `C8`、`C9` 这种完整项目入口。
6. 如果要跑 `PowerRAG`，先确认你本机或内网已经有可用的 RAGFlow 服务。

## 8. 我帮你标出来的现实限制

* `C8` 默认找 `data/C8/cook`，这份数据目录在仓库里是空的，必须由你本地补齐或改配置。
* `C3`、`C4`、`C6` 里很多脚本会连 DeepSeek / Hugging Face / Milvus，单纯改命令不够，还要把服务和 key 配齐。
* `C9` 的完整图 RAG 方案同时依赖 Milvus 和 Neo4j。
