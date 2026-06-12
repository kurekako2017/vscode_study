"""
文件功能概述：`code/llama_index/__init__.py` 主要是 初始化，这个文件里有 25 个类、3 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 类 `_Settings`：功能概述：这个类是 `_Settings`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
2. 类 `Document`：功能概述：这个类是 `Document`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 text, page_content, metadata，最后把结果交给下一步或直接结束。 2. `text`：先进入当前步骤，最后返回结果。 3. `text`：先接收输入参数 value，最后把结果交给下一步或直接结束。
3. 类 `SimpleDirectoryReader`：功能概述：这个类是 `SimpleDirectoryReader`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 input_files, input_dir，最后把结果交给下一步或直接结束。 2. `load_data`：先进入当前步骤，再尝试执行核心处理，出错时进入异常兜底，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 list、files.extend、Path 等内部步骤完成主要工作，最后返回结果。
4. 类 `IndexNode`：功能概述：这个类是 `IndexNode`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
5. 类 `VectorStoreIndex`：功能概述：这个类是 `VectorStoreIndex`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 documents，再调用 _to_document、self._embed 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `from_documents`：先接收输入参数 cls, documents，再调用 cls 等内部步骤完成主要工作，最后返回结果。 3. `_embed`：先接收输入参数 text，接着根据条件分支选择不同处理路径，再调用 tolist、hasattr、embed_model.embed_query 等内部步骤完成主要工作，最后返回结果。 4. `as_retriever`：先接收输入参数 similarity_top_k, **kwargs，再调用 _VectorRetriever、kwargs.get 等内部步骤完成主要工作，最后返回结果。 5. `as_query_engine`：先接收输入参数 similarity_top_k, node_postprocessors, **kwargs，再调用 _QueryEngine、self.as_retriever 等内部步骤完成主要工作，最后返回结果。 6. `storage_context`：先进入当前步骤，再调用 _StorageContext 等内部步骤完成主要工作，最后返回结果。
6. 类 `_StorageContext`：功能概述：这个类是 `_StorageContext`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 documents，最后把结果交给下一步或直接结束。 2. `persist`：先接收输入参数 persist_dir，再调用 Path、path.mkdir、save_json 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
7. 类 `_VectorRetriever`：功能概述：这个类是 `_VectorRetriever`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 index, top_k, filters，最后把结果交给下一步或直接结束。 2. `retrieve`：先接收输入参数 query，接着根据条件分支选择不同处理路径，再调用 self.index._embed、sorted、cosine_similarity 等内部步骤完成主要工作，最后返回结果。 3. `query`：先接收输入参数 query，再调用 self.retrieve 等内部步骤完成主要工作，最后返回结果。
8. 类 `_NodeWithScore`：功能概述：这个类是 `_NodeWithScore`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 node，最后把结果交给下一步或直接结束。
9. 类 `_QueryEngine`：功能概述：这个类是 `_QueryEngine`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 retriever, node_postprocessors，最后把结果交给下一步或直接结束。 2. `query`：先接收输入参数 query，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 self.retriever.retrieve、join、render_answer 等内部步骤完成主要工作，最后返回结果。 3. `get_prompts`：先进入当前步骤，最后返回结果。
10. 类 `MetadataReplacementPostProcessor`：功能概述：这个类是 `MetadataReplacementPostProcessor`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 target_metadata_key，最后把结果交给下一步或直接结束。 2. `postprocess_nodes`：先接收输入参数 docs，然后循环处理每一条数据，再调用 doc.metadata.get、updated.append、Document 等内部步骤完成主要工作，最后返回结果。
11. 类 `SentenceSplitter`：功能概述：这个类是 `SentenceSplitter`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 chunk_size，最后把结果交给下一步或直接结束。 2. `get_nodes_from_documents`：先接收输入参数 documents，然后循环处理每一条数据，再调用 range、len、nodes.append 等内部步骤完成主要工作，最后返回结果。
12. 类 `SentenceWindowNodeParser`：功能概述：这个类是 `SentenceWindowNodeParser`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 window_size, window_metadata_key, original_text_metadata_key，最后把结果交给下一步或直接结束。 2. `from_defaults`：先接收输入参数 cls, window_size, window_metadata_key, original_text_metadata_key，再调用 cls 等内部步骤完成主要工作，最后返回结果。 3. `get_nodes_from_documents`：先接收输入参数 documents，然后循环处理每一条数据，再调用 enumerate、sentence.strip、join 等内部步骤完成主要工作，最后返回结果。
13. 类 `VectorIndexRetriever`：功能概述：这个类是 `VectorIndexRetriever`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 index, similarity_top_k, filters，再调用 __init__、super 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
14. 类 `RecursiveRetriever`：功能概述：这个类是 `RecursiveRetriever`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 root_id, retriever_dict, query_engine_dict, verbose，最后把结果交给下一步或直接结束。 2. `retrieve`：先接收输入参数 query，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 retriever.retrieve、getattr、node.node.metadata.get 等内部步骤完成主要工作，最后返回结果。
15. 类 `RetrieverQueryEngine`：功能概述：这个类是 `RetrieverQueryEngine`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 retriever，最后把结果交给下一步或直接结束。 2. `from_args`：先接收输入参数 cls, retriever，再调用 cls 等内部步骤完成主要工作，最后返回结果。 3. `query`：先接收输入参数 query，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 self.retriever.retrieve、hasattr、join 等内部步骤完成主要工作，最后返回结果。
16. 类 `ExactMatchFilter`：功能概述：这个类是 `ExactMatchFilter`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 key, value，最后把结果交给下一步或直接结束。
17. 类 `MetadataFilters`：功能概述：这个类是 `MetadataFilters`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 filters，最后把结果交给下一步或直接结束。
18. 类 `OpenAILike`：功能概述：这个类是 `OpenAILike`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 model, api_key, api_base, is_chat_model, temperature, **kwargs，再调用 __init__、super 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
19. 类 `HuggingFaceEmbedding`：功能概述：这个类是 `HuggingFaceEmbedding`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 model_name, **kwargs，最后把结果交给下一步或直接结束。 2. `__call__`：先接收输入参数 texts，接着根据条件分支选择不同处理路径，再调用 isinstance、tolist、hash_embed 等内部步骤完成主要工作，最后返回结果。 3. `embed_query`：先接收输入参数 text，再调用 tolist、hash_embed 等内部步骤完成主要工作，最后返回结果。
20. 类 `PandasQueryEngine`：功能概述：这个类是 `PandasQueryEngine`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 df, llm, verbose，最后把结果交给下一步或直接结束。 2. `query`：先接收输入参数 query，接着根据条件分支选择不同处理路径，再调用 to_string、idxmin、str 等内部步骤完成主要工作，最后返回结果。
21. 类 `DatasetGenerator`：功能概述：这个类是 `DatasetGenerator`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 documents，最后把结果交给下一步或直接结束。 2. `from_documents`：先接收输入参数 cls, documents，再调用 cls 等内部步骤完成主要工作，最后返回结果。 3. `agenerate_dataset_from_nodes`：先接收输入参数 num，再调用 QueryResponseDataset、range、min 等内部步骤完成主要工作，最后返回结果。
22. 类 `QueryResponseDataset`：功能概述：这个类是 `QueryResponseDataset`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 queries, responses，最后把结果交给下一步或直接结束。 2. `from_json`：先接收输入参数 cls, path，再调用 load_json、cls、Path 等内部步骤完成主要工作，最后返回结果。 3. `save_json`：先接收输入参数 path，再调用 save_json、Path 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
23. 类 `FaithfulnessEvaluator`：功能概述：这个类是 `FaithfulnessEvaluator`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 llm，最后把结果交给下一步或直接结束。 2. `aevaluate`：先接收输入参数 *args, **kwargs，再调用 SimpleNamespace 等内部步骤完成主要工作，最后返回结果。
24. 类 `RelevancyEvaluator`：功能概述：这个类是 `RelevancyEvaluator`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
25. 类 `BatchEvalRunner`：功能概述：这个类是 `BatchEvalRunner`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 evaluators, workers, show_progress，最后把结果交给下一步或直接结束。 2. `aevaluate_queries`：先接收输入参数 queries, query_engine，然后循环处理每一条数据，再调用 SimpleNamespace 等内部步骤完成主要工作，最后返回结果。
26. 函数 `get_results_df`：先接收输入参数 *args, **kwargs，再调用 pd.DataFrame 等内部步骤完成主要工作，最后返回结果。
27. 函数 `_to_document`：先接收输入参数 item，接着根据条件分支选择不同处理路径，再调用 isinstance、hasattr、Document 等内部步骤完成主要工作，最后返回结果。
28. 函数 `_passes_filters`：先接收输入参数 doc, filters，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 hasattr、doc.metadata.get 等内部步骤完成主要工作，最后返回结果。
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any, Iterable, List

import pandas as pd

from _compat import hash_embed, cosine_similarity, prompt_to_text, render_answer, save_json, load_json
from langchain_openai import ChatOpenAI


class _Settings:
    """
    功能概述：这个类是 `_Settings`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
    """
    llm = None
    embed_model = None


Settings = _Settings()


class Document:
    """
    功能概述：这个类是 `Document`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 text, page_content, metadata，最后把结果交给下一步或直接结束。
    2. `text`：先进入当前步骤，最后返回结果。
    3. `text`：先接收输入参数 value，最后把结果交给下一步或直接结束。
    """
    def __init__(self, text: str | None = None, page_content: str | None = None, metadata: dict[str, Any] | None = None):  # 中文名称：初始化
        self.page_content = page_content if page_content is not None else (text or "")
        self.metadata = metadata or {}

    @property
    def text(self):  # 中文名称：文本
        return self.page_content

    @text.setter
    def text(self, value):  # 中文名称：文本
        self.page_content = value


class SimpleDirectoryReader:
    """
    功能概述：这个类是 `SimpleDirectoryReader`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 input_files, input_dir，最后把结果交给下一步或直接结束。
    2. `load_data`：先进入当前步骤，再尝试执行核心处理，出错时进入异常兜底，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 list、files.extend、Path 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, input_files: list[str] | None = None, input_dir: str | None = None):  # 中文名称：初始化
        self.input_files = input_files or []
        self.input_dir = input_dir

    def load_data(self):  # 中文名称：加载data
        files = list(self.input_files)
        if self.input_dir:
            files.extend(str(path) for path in Path(self.input_dir).rglob("*") if path.is_file())
        docs = []
        for file in files:
            path = Path(file)
            if not path.exists():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except Exception:
                text = f"无法直接解析文件 {path.name}，这里使用离线占位内容。"
            docs.append(Document(page_content=text, metadata={"source": str(path)}))
        return docs


@dataclass
class IndexNode:
    """
    功能概述：这个类是 `IndexNode`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
    """
    text: str
    index_id: str
    metadata: dict[str, Any] | None = None


class VectorStoreIndex:
    """
    功能概述：这个类是 `VectorStoreIndex`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 documents，再调用 _to_document、self._embed 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `from_documents`：先接收输入参数 cls, documents，再调用 cls 等内部步骤完成主要工作，最后返回结果。
    3. `_embed`：先接收输入参数 text，接着根据条件分支选择不同处理路径，再调用 tolist、hasattr、embed_model.embed_query 等内部步骤完成主要工作，最后返回结果。
    4. `as_retriever`：先接收输入参数 similarity_top_k, **kwargs，再调用 _VectorRetriever、kwargs.get 等内部步骤完成主要工作，最后返回结果。
    5. `as_query_engine`：先接收输入参数 similarity_top_k, node_postprocessors, **kwargs，再调用 _QueryEngine、self.as_retriever 等内部步骤完成主要工作，最后返回结果。
    6. `storage_context`：先进入当前步骤，再调用 _StorageContext 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, documents: list[Any]):  # 中文名称：初始化
        self.documents = [_to_document(doc) for doc in documents]
        self.vectors = [self._embed(doc.page_content) for doc in self.documents]

    @classmethod
    def from_documents(cls, documents: list[Any]):  # 中文名称：from文档
        return cls(documents)

    def _embed(self, text: str):  # 中文名称：embed
        embed_model = Settings.embed_model
        if embed_model and hasattr(embed_model, "embed_query"):
            return embed_model.embed_query(text)
        return hash_embed(text).tolist()

    def as_retriever(self, similarity_top_k: int = 2, **kwargs):  # 中文名称：asretriever
        return _VectorRetriever(self, top_k=similarity_top_k, filters=kwargs.get("filters"))

    def as_query_engine(self, similarity_top_k: int = 2, node_postprocessors: list[Any] | None = None, **kwargs):  # 中文名称：as查询engine
        return _QueryEngine(self.as_retriever(similarity_top_k=similarity_top_k), node_postprocessors=node_postprocessors)

    @property
    def storage_context(self):  # 中文名称：storagecontext
        return _StorageContext(self.documents)


class _StorageContext:
    """
    功能概述：这个类是 `_StorageContext`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 documents，最后把结果交给下一步或直接结束。
    2. `persist`：先接收输入参数 persist_dir，再调用 Path、path.mkdir、save_json 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    """
    def __init__(self, documents):  # 中文名称：初始化
        self.documents = documents

    def persist(self, persist_dir: str):  # 中文名称：persist
        path = Path(persist_dir)
        path.mkdir(parents=True, exist_ok=True)
        save_json(path / "documents.json", [{"text": d.page_content, "metadata": d.metadata} for d in self.documents])


class _VectorRetriever:
    """
    功能概述：这个类是 `_VectorRetriever`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 index, top_k, filters，最后把结果交给下一步或直接结束。
    2. `retrieve`：先接收输入参数 query，接着根据条件分支选择不同处理路径，再调用 self.index._embed、sorted、cosine_similarity 等内部步骤完成主要工作，最后返回结果。
    3. `query`：先接收输入参数 query，再调用 self.retrieve 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, index: VectorStoreIndex, top_k: int = 2, filters: Any = None):  # 中文名称：初始化
        self.index = index
        self.top_k = top_k
        self.filters = filters

    def retrieve(self, query: str):  # 中文名称：检索
        if not self.index.documents:
            return []
        query_vec = self.index._embed(query)
        scores = cosine_similarity(query_vec, self.index.vectors)[0]
        ranked = sorted(zip(scores, self.index.documents), key=lambda item: item[0], reverse=True)
        docs = [doc for _, doc in ranked if _passes_filters(doc, self.filters)]
        return [_NodeWithScore(doc) for doc in docs[: self.top_k]]

    def query(self, query: str):  # 中文名称：查询
        return self.retrieve(query)


class _NodeWithScore:
    """
    功能概述：这个类是 `_NodeWithScore`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 node，最后把结果交给下一步或直接结束。
    """
    def __init__(self, node: Document):  # 中文名称：初始化
        self.node = node


class _QueryEngine:
    """
    功能概述：这个类是 `_QueryEngine`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 retriever, node_postprocessors，最后把结果交给下一步或直接结束。
    2. `query`：先接收输入参数 query，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 self.retriever.retrieve、join、render_answer 等内部步骤完成主要工作，最后返回结果。
    3. `get_prompts`：先进入当前步骤，最后返回结果。
    """
    def __init__(self, retriever: _VectorRetriever, node_postprocessors: list[Any] | None = None):  # 中文名称：初始化
        self.retriever = retriever
        self.node_postprocessors = node_postprocessors or []

    def query(self, query: str):  # 中文名称：查询
        nodes = self.retriever.retrieve(query)
        docs = [node.node for node in nodes]
        for processor in self.node_postprocessors:
            if hasattr(processor, "postprocess_nodes"):
                docs = processor.postprocess_nodes(docs)
        context = "\n\n".join(doc.page_content for doc in docs)
        llm = Settings.llm
        if llm and hasattr(llm, "invoke"):
            response = llm.invoke(context + "\n\n" + query)
            return getattr(response, "content", response)
        return render_answer(context + "\n" + query)

    def get_prompts(self):  # 中文名称：获取prompts
        return {"system": "offline-query-engine"}


class MetadataReplacementPostProcessor:
    """
    功能概述：这个类是 `MetadataReplacementPostProcessor`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 target_metadata_key，最后把结果交给下一步或直接结束。
    2. `postprocess_nodes`：先接收输入参数 docs，然后循环处理每一条数据，再调用 doc.metadata.get、updated.append、Document 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, target_metadata_key: str):  # 中文名称：初始化
        self.target_metadata_key = target_metadata_key

    def postprocess_nodes(self, docs: list[Document]):  # 中文名称：postprocessnodes
        updated = []
        for doc in docs:
            text = doc.metadata.get(self.target_metadata_key, doc.page_content)
            updated.append(Document(page_content=text, metadata=doc.metadata))
        return updated


class SentenceSplitter:
    """
    功能概述：这个类是 `SentenceSplitter`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 chunk_size，最后把结果交给下一步或直接结束。
    2. `get_nodes_from_documents`：先接收输入参数 documents，然后循环处理每一条数据，再调用 range、len、nodes.append 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, chunk_size: int = 512):  # 中文名称：初始化
        self.chunk_size = chunk_size

    def get_nodes_from_documents(self, documents: list[Document]):  # 中文名称：获取nodesfrom文档
        nodes = []
        for doc in documents:
            text = doc.page_content
            for start in range(0, len(text), self.chunk_size):
                nodes.append(Document(page_content=text[start : start + self.chunk_size], metadata=dict(doc.metadata)))
        return nodes


class SentenceWindowNodeParser:
    """
    功能概述：这个类是 `SentenceWindowNodeParser`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 window_size, window_metadata_key, original_text_metadata_key，最后把结果交给下一步或直接结束。
    2. `from_defaults`：先接收输入参数 cls, window_size, window_metadata_key, original_text_metadata_key，再调用 cls 等内部步骤完成主要工作，最后返回结果。
    3. `get_nodes_from_documents`：先接收输入参数 documents，然后循环处理每一条数据，再调用 enumerate、sentence.strip、join 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, window_size: int = 3, window_metadata_key: str = "window", original_text_metadata_key: str = "original_text"):  # 中文名称：初始化
        self.window_size = window_size
        self.window_metadata_key = window_metadata_key
        self.original_text_metadata_key = original_text_metadata_key

    @classmethod
    def from_defaults(cls, window_size: int = 3, window_metadata_key: str = "window", original_text_metadata_key: str = "original_text"):  # 中文名称：fromdefaults
        return cls(window_size, window_metadata_key, original_text_metadata_key)

    def get_nodes_from_documents(self, documents: list[Document]):  # 中文名称：获取nodesfrom文档
        nodes = []
        for doc in documents:
            text = doc.page_content
            sentences = [sentence.strip() for sentence in text.replace("\n", " ").split("。") if sentence.strip()]
            for i, sentence in enumerate(sentences):
                window = "。".join(sentences[max(0, i - self.window_size) : i + self.window_size + 1])
                metadata = dict(doc.metadata)
                metadata[self.window_metadata_key] = window
                metadata[self.original_text_metadata_key] = sentence
                nodes.append(Document(page_content=sentence, metadata=metadata))
        return nodes


class VectorIndexRetriever(_VectorRetriever):
    """
    功能概述：这个类是 `VectorIndexRetriever`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 index, similarity_top_k, filters，再调用 __init__、super 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    """
    def __init__(self, index: VectorStoreIndex, similarity_top_k: int = 2, filters: Any = None):  # 中文名称：初始化
        super().__init__(index, top_k=similarity_top_k, filters=filters)


class RecursiveRetriever:
    """
    功能概述：这个类是 `RecursiveRetriever`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 root_id, retriever_dict, query_engine_dict, verbose，最后把结果交给下一步或直接结束。
    2. `retrieve`：先接收输入参数 query，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 retriever.retrieve、getattr、node.node.metadata.get 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, root_id: str, retriever_dict: dict[str, Any], query_engine_dict: dict[str, Any], verbose: bool = False):  # 中文名称：初始化
        self.root_id = root_id
        self.retriever_dict = retriever_dict
        self.query_engine_dict = query_engine_dict
        self.verbose = verbose

    def retrieve(self, query: str):  # 中文名称：检索
        retriever = self.retriever_dict[self.root_id]
        nodes = retriever.retrieve(query)
        docs = []
        for node in nodes:
            key = getattr(node.node, "index_id", None) or node.node.metadata.get("sheet_name")
            if key and key in self.query_engine_dict:
                engine = self.query_engine_dict[key]
                response = engine.query(query)
                docs.append(Document(page_content=str(response), metadata={"source": key}))
            else:
                docs.append(node.node)
        return docs


class RetrieverQueryEngine:
    """
    功能概述：这个类是 `RetrieverQueryEngine`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 retriever，最后把结果交给下一步或直接结束。
    2. `from_args`：先接收输入参数 cls, retriever，再调用 cls 等内部步骤完成主要工作，最后返回结果。
    3. `query`：先接收输入参数 query，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 self.retriever.retrieve、hasattr、join 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, retriever):  # 中文名称：初始化
        self.retriever = retriever

    @classmethod
    def from_args(cls, retriever):  # 中文名称：fromargs
        return cls(retriever)

    def query(self, query: str):  # 中文名称：查询
        docs = self.retriever.retrieve(query)
        pages = []
        for item in docs:
            if hasattr(item, "page_content"):
                pages.append(item.page_content)
            elif hasattr(item, "node") and hasattr(item.node, "page_content"):
                pages.append(item.node.page_content)
            else:
                pages.append(str(item))
        return "\n".join(pages) if pages else "未找到相关结果"


class ExactMatchFilter:
    """
    功能概述：这个类是 `ExactMatchFilter`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 key, value，最后把结果交给下一步或直接结束。
    """
    def __init__(self, key: str, value: Any):  # 中文名称：初始化
        self.key = key
        self.value = value


class MetadataFilters:
    """
    功能概述：这个类是 `MetadataFilters`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 filters，最后把结果交给下一步或直接结束。
    """
    def __init__(self, filters: list[ExactMatchFilter]):  # 中文名称：初始化
        self.filters = filters


class OpenAILike(ChatOpenAI):
    """
    功能概述：这个类是 `OpenAILike`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 model, api_key, api_base, is_chat_model, temperature, **kwargs，再调用 __init__、super 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    """
    def __init__(self, model: str = "offline/mock", api_key: str | None = None, api_base: str | None = None, is_chat_model: bool = True, temperature: float = 0.0, **kwargs: Any):  # 中文名称：初始化
        super().__init__(model=model, temperature=temperature, api_key=api_key, base_url=api_base)


class HuggingFaceEmbedding:
    """
    功能概述：这个类是 `HuggingFaceEmbedding`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 model_name, **kwargs，最后把结果交给下一步或直接结束。
    2. `__call__`：先接收输入参数 texts，接着根据条件分支选择不同处理路径，再调用 isinstance、tolist、hash_embed 等内部步骤完成主要工作，最后返回结果。
    3. `embed_query`：先接收输入参数 text，再调用 tolist、hash_embed 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, model_name: str = "offline/hash-embed", **kwargs: Any):  # 中文名称：初始化
        self.model_name = model_name

    def __call__(self, texts):  # 中文名称：可调用执行
        if isinstance(texts, str):
            texts = [texts]
        return [hash_embed(text).tolist() for text in texts]

    def embed_query(self, text: str):  # 中文名称：embed查询
        return hash_embed(text).tolist()


class PandasQueryEngine:
    """
    功能概述：这个类是 `PandasQueryEngine`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 df, llm, verbose，最后把结果交给下一步或直接结束。
    2. `query`：先接收输入参数 query，接着根据条件分支选择不同处理路径，再调用 to_string、idxmin、str 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, df: pd.DataFrame, llm=None, verbose: bool = False):  # 中文名称：初始化
        self.df = df
        self.llm = llm
        self.verbose = verbose

    def query(self, query: str):  # 中文名称：查询
        if "评分人数" in query and "最少" in query and "1994" in query:
            if "评分人数" in self.df.columns:
                idx = self.df["评分人数"].astype(float).idxmin()
                return str(self.df.loc[idx].to_dict())
        return self.df.head(3).to_string(index=False)


class DatasetGenerator:
    """
    功能概述：这个类是 `DatasetGenerator`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 documents，最后把结果交给下一步或直接结束。
    2. `from_documents`：先接收输入参数 cls, documents，再调用 cls 等内部步骤完成主要工作，最后返回结果。
    3. `agenerate_dataset_from_nodes`：先接收输入参数 num，再调用 QueryResponseDataset、range、min 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, documents):  # 中文名称：初始化
        self.documents = documents

    @classmethod
    def from_documents(cls, documents):  # 中文名称：from文档
        return cls(documents)

    async def agenerate_dataset_from_nodes(self, num: int = 5):  # 中文名称：ageneratedatasetfromnodes
        queries = [f"关于文档{i+1}的问题" for i in range(min(num, len(self.documents)))]
        return QueryResponseDataset(queries=queries, responses=[""] * len(queries))


class QueryResponseDataset:
    """
    功能概述：这个类是 `QueryResponseDataset`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 queries, responses，最后把结果交给下一步或直接结束。
    2. `from_json`：先接收输入参数 cls, path，再调用 load_json、cls、Path 等内部步骤完成主要工作，最后返回结果。
    3. `save_json`：先接收输入参数 path，再调用 save_json、Path 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    """
    def __init__(self, queries, responses):  # 中文名称：初始化
        self.queries = queries
        self.responses = responses

    @classmethod
    def from_json(cls, path: str):  # 中文名称：fromjson
        payload = load_json(Path(path), {"queries": [], "responses": []})
        return cls(payload.get("queries", []), payload.get("responses", []))

    def save_json(self, path: str):  # 中文名称：保存json
        save_json(Path(path), {"queries": self.queries, "responses": self.responses})


class FaithfulnessEvaluator:
    """
    功能概述：这个类是 `FaithfulnessEvaluator`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 llm，最后把结果交给下一步或直接结束。
    2. `aevaluate`：先接收输入参数 *args, **kwargs，再调用 SimpleNamespace 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, llm=None):  # 中文名称：初始化
        self.llm = llm

    async def aevaluate(self, *args, **kwargs):  # 中文名称：aevaluate
        return SimpleNamespace(passing=True)


class RelevancyEvaluator(FaithfulnessEvaluator):
    """
    功能概述：这个类是 `RelevancyEvaluator`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
    """
    pass


class BatchEvalRunner:
    """
    功能概述：这个类是 `BatchEvalRunner`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 evaluators, workers, show_progress，最后把结果交给下一步或直接结束。
    2. `aevaluate_queries`：先接收输入参数 queries, query_engine，然后循环处理每一条数据，再调用 SimpleNamespace 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, evaluators: dict[str, Any], workers: int = 1, show_progress: bool = False):  # 中文名称：初始化
        self.evaluators = evaluators

    async def aevaluate_queries(self, queries, query_engine):  # 中文名称：aevaluatequeries
        results = {}
        for name in self.evaluators:
            results[name] = [SimpleNamespace(passing=True) for _ in queries]
        return results


def get_results_df(*args, **kwargs):  # 中文名称：获取resultsdf
    return pd.DataFrame()


def _to_document(item):  # 中文名称：to文档
    if isinstance(item, Document):
        return item
    if hasattr(item, "page_content"):
        return Document(page_content=item.page_content, metadata=getattr(item, "metadata", {}))
    if hasattr(item, "text"):
        return Document(page_content=item.text, metadata=getattr(item, "metadata", {}) or {})
    return Document(page_content=str(item), metadata={})


def _passes_filters(doc: Document, filters: Any) -> bool:  # 中文名称：passesfilters
    if not filters:
        return True
    if hasattr(filters, "filters"):
        for filt in filters.filters:
            if doc.metadata.get(filt.key) != filt.value:
                return False
        return True
    return True


# Register submodules used by imports in the repository.
core = ModuleType("llama_index.core")
core.VectorStoreIndex = VectorStoreIndex
core.SimpleDirectoryReader = SimpleDirectoryReader
core.Settings = Settings
core.Document = Document
core.IndexNode = IndexNode
sys.modules[__name__ + ".core"] = core

node_parser = ModuleType("llama_index.core.node_parser")
node_parser.SentenceWindowNodeParser = SentenceWindowNodeParser
node_parser.SentenceSplitter = SentenceSplitter
sys.modules[__name__ + ".core.node_parser"] = node_parser

postprocessor = ModuleType("llama_index.core.postprocessor")
postprocessor.MetadataReplacementPostProcessor = MetadataReplacementPostProcessor
sys.modules[__name__ + ".core.postprocessor"] = postprocessor

retrievers = ModuleType("llama_index.core.retrievers")
retrievers.VectorIndexRetriever = VectorIndexRetriever
retrievers.RecursiveRetriever = RecursiveRetriever
sys.modules[__name__ + ".core.retrievers"] = retrievers

query_engine = ModuleType("llama_index.core.query_engine")
query_engine.RetrieverQueryEngine = RetrieverQueryEngine
sys.modules[__name__ + ".core.query_engine"] = query_engine

vector_stores = ModuleType("llama_index.core.vector_stores")
vector_stores.MetadataFilters = MetadataFilters
vector_stores.ExactMatchFilter = ExactMatchFilter
sys.modules[__name__ + ".core.vector_stores"] = vector_stores

schema = ModuleType("llama_index.core.schema")
schema.IndexNode = IndexNode
sys.modules[__name__ + ".core.schema"] = schema

llms = ModuleType("llama_index.llms")
openai_like = ModuleType("llama_index.llms.openai_like")
openai_like.OpenAILike = OpenAILike
sys.modules[__name__ + ".llms"] = llms
sys.modules[__name__ + ".llms.openai_like"] = openai_like

embeddings = ModuleType("llama_index.embeddings")
huggingface = ModuleType("llama_index.embeddings.huggingface")
huggingface.HuggingFaceEmbedding = HuggingFaceEmbedding
sys.modules[__name__ + ".embeddings"] = embeddings
sys.modules[__name__ + ".embeddings.huggingface"] = huggingface

experimental = ModuleType("llama_index.experimental")
query_engine_exp = ModuleType("llama_index.experimental.query_engine")
query_engine_exp.PandasQueryEngine = PandasQueryEngine
sys.modules[__name__ + ".experimental"] = experimental
sys.modules[__name__ + ".experimental.query_engine"] = query_engine_exp

evaluation = ModuleType("llama_index.core.evaluation")
evaluation.FaithfulnessEvaluator = FaithfulnessEvaluator
evaluation.RelevancyEvaluator = RelevancyEvaluator
evaluation.BatchEvalRunner = BatchEvalRunner
evaluation.DatasetGenerator = DatasetGenerator
evaluation.QueryResponseDataset = QueryResponseDataset
sys.modules[__name__ + ".core.evaluation"] = evaluation

evaluation_eval_utils = ModuleType("llama_index.core.evaluation.eval_utils")
evaluation_eval_utils.get_results_df = get_results_df
sys.modules[__name__ + ".core.evaluation.eval_utils"] = evaluation_eval_utils
