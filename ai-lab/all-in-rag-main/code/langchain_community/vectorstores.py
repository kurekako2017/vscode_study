"""
文件功能概述：`code/langchain_community/vectorstores.py` 主要是 vectorstores，这个文件里有 5 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 类 `_Retriever`：功能概述：这个类是 `_Retriever`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 store, search_kwargs，最后把结果交给下一步或直接结束。 2. `invoke`：先接收输入参数 query，再调用 self.get_relevant_documents 等内部步骤完成主要工作，最后返回结果。 3. `get_relevant_documents`：先接收输入参数 query，再调用 self.store.similarity_search、self.search_kwargs.get 等内部步骤完成主要工作，最后返回结果。
2. 类 `_BaseVectorStore`：功能概述：这个类是 `_BaseVectorStore`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 docs, embedding，接着根据条件分支选择不同处理路径，再调用 self._rebuild 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `_embed`：先接收输入参数 text，接着根据条件分支选择不同处理路径，再调用 tolist、hasattr、self.embedding.embed_query 等内部步骤完成主要工作，最后返回结果。 3. `_rebuild`：先进入当前步骤，再调用 self._embed 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 4. `from_documents`：先接收输入参数 cls, documents, embedding, **kwargs，再调用 cls、list 等内部步骤完成主要工作，最后返回结果。 5. `add_documents`：先接收输入参数 documents，再调用 self.documents.extend、self._rebuild 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 6. `similarity_search`：先接收输入参数 query, k，接着根据条件分支选择不同处理路径，再调用 self._embed、sorted、cosine_similarity 等内部步骤完成主要工作，最后返回结果。 7. `as_retriever`：先接收输入参数 search_kwargs, **kwargs，再调用 _Retriever 等内部步骤完成主要工作，最后返回结果。 8. `save_local`：先接收输入参数 path，再调用 Path、path_obj.mkdir、save_json 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 9. `load_local`：先接收输入参数 cls, path, embedding, allow_dangerous_deserialization，再调用 load_json、cls、Document 等内部步骤完成主要工作，最后返回结果。
3. 类 `FAISS`：功能概述：这个类是 `FAISS`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
4. 类 `Chroma`：功能概述：这个类是 `Chroma`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
5. 类 `InMemoryVectorStore`：功能概述：这个类是 `InMemoryVectorStore`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 embedding，再调用 __init__、super 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List

import numpy as np
from langchain_core.documents import Document

from _compat import hash_embed, cosine_similarity, save_json, load_json


class _Retriever:
    """
    功能概述：这个类是 `_Retriever`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 store, search_kwargs，最后把结果交给下一步或直接结束。
    2. `invoke`：先接收输入参数 query，再调用 self.get_relevant_documents 等内部步骤完成主要工作，最后返回结果。
    3. `get_relevant_documents`：先接收输入参数 query，再调用 self.store.similarity_search、self.search_kwargs.get 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, store, search_kwargs=None):  # 中文名称：初始化
        self.store = store
        self.search_kwargs = search_kwargs or {"k": 4}

    def invoke(self, query: str):  # 中文名称：invoke
        return self.get_relevant_documents(query)

    def get_relevant_documents(self, query: str):  # 中文名称：获取relevant文档
        return self.store.similarity_search(query, k=self.search_kwargs.get("k", 4))


class _BaseVectorStore:
    """
    功能概述：这个类是 `_BaseVectorStore`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 docs, embedding，接着根据条件分支选择不同处理路径，再调用 self._rebuild 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `_embed`：先接收输入参数 text，接着根据条件分支选择不同处理路径，再调用 tolist、hasattr、self.embedding.embed_query 等内部步骤完成主要工作，最后返回结果。
    3. `_rebuild`：先进入当前步骤，再调用 self._embed 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    4. `from_documents`：先接收输入参数 cls, documents, embedding, **kwargs，再调用 cls、list 等内部步骤完成主要工作，最后返回结果。
    5. `add_documents`：先接收输入参数 documents，再调用 self.documents.extend、self._rebuild 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    6. `similarity_search`：先接收输入参数 query, k，接着根据条件分支选择不同处理路径，再调用 self._embed、sorted、cosine_similarity 等内部步骤完成主要工作，最后返回结果。
    7. `as_retriever`：先接收输入参数 search_kwargs, **kwargs，再调用 _Retriever 等内部步骤完成主要工作，最后返回结果。
    8. `save_local`：先接收输入参数 path，再调用 Path、path_obj.mkdir、save_json 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    9. `load_local`：先接收输入参数 cls, path, embedding, allow_dangerous_deserialization，再调用 load_json、cls、Document 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, docs: List[Document] | None = None, embedding=None):  # 中文名称：初始化
        self.embedding = embedding
        self.documents: List[Document] = docs or []
        self.vectors: List[List[float]] = []
        if docs:
            self._rebuild()

    def _embed(self, text: str):  # 中文名称：embed
        if self.embedding and hasattr(self.embedding, "embed_query"):
            return self.embedding.embed_query(text)
        return hash_embed(text).tolist()

    def _rebuild(self):  # 中文名称：rebuild
        self.vectors = [self._embed(doc.page_content) for doc in self.documents]

    @classmethod
    def from_documents(cls, documents: List[Document], embedding=None, **kwargs):  # 中文名称：from文档
        return cls(list(documents), embedding=embedding)

    def add_documents(self, documents: List[Document]):  # 中文名称：add文档
        self.documents.extend(documents)
        self._rebuild()

    def similarity_search(self, query: str, k: int = 4):  # 中文名称：similarity搜索
        if not self.documents:
            return []
        query_vec = self._embed(query)
        scores = cosine_similarity(query_vec, self.vectors)[0]
        ranked = sorted(zip(scores, self.documents), key=lambda item: item[0], reverse=True)
        return [doc for _, doc in ranked[:k]]

    def as_retriever(self, search_kwargs=None, **kwargs):  # 中文名称：asretriever
        return _Retriever(self, search_kwargs=search_kwargs)

    def save_local(self, path: str):  # 中文名称：保存local
        path_obj = Path(path)
        path_obj.mkdir(parents=True, exist_ok=True)
        payload = [
            {"page_content": doc.page_content, "metadata": doc.metadata}
            for doc in self.documents
        ]
        save_json(path_obj / "store.json", payload)

    @classmethod
    def load_local(cls, path: str, embedding=None, allow_dangerous_deserialization: bool = False):  # 中文名称：加载local
        payload = load_json(Path(path) / "store.json", [])
        docs = [Document(page_content=item["page_content"], metadata=item.get("metadata", {})) for item in payload]
        return cls(docs, embedding=embedding)


class FAISS(_BaseVectorStore):
    """
    功能概述：这个类是 `FAISS`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
    """
    pass


class Chroma(_BaseVectorStore):
    """
    功能概述：这个类是 `Chroma`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
    """
    pass


class InMemoryVectorStore(_BaseVectorStore):
    """
    功能概述：这个类是 `InMemoryVectorStore`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 embedding，再调用 __init__、super 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    """
    def __init__(self, embedding=None):  # 中文名称：初始化
        super().__init__([], embedding=embedding)

