"""
文件功能概述：`code/langchain_community/retrievers.py` 主要是 retrievers，这个文件里有 1 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 类 `BM25Retriever`：功能概述：这个类是 `BM25Retriever`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 docs, k，最后把结果交给下一步或直接结束。 2. `from_documents`：先接收输入参数 cls, documents, k，再调用 cls 等内部步骤完成主要工作，最后返回结果。 3. `invoke`：先接收输入参数 query，再调用 self.get_relevant_documents 等内部步骤完成主要工作，最后返回结果。 4. `get_relevant_documents`：先接收输入参数 query，然后循环处理每一条数据，再调用 set、scored.sort、split 等内部步骤完成主要工作，最后返回结果。
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Iterable, List, Sequence

from langchain_core.documents import Document
from _compat import hash_embed, cosine_similarity


class BM25Retriever:
    """
    功能概述：这个类是 `BM25Retriever`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 docs, k，最后把结果交给下一步或直接结束。
    2. `from_documents`：先接收输入参数 cls, documents, k，再调用 cls 等内部步骤完成主要工作，最后返回结果。
    3. `invoke`：先接收输入参数 query，再调用 self.get_relevant_documents 等内部步骤完成主要工作，最后返回结果。
    4. `get_relevant_documents`：先接收输入参数 query，然后循环处理每一条数据，再调用 set、scored.sort、split 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, docs: List[Document], k: int = 5):  # 中文名称：初始化
        self.docs = docs
        self.k = k

    @classmethod
    def from_documents(cls, documents: List[Document], k: int = 5):  # 中文名称：from文档
        return cls(documents, k=k)

    def invoke(self, query: str):  # 中文名称：invoke
        return self.get_relevant_documents(query)

    def get_relevant_documents(self, query: str):  # 中文名称：获取relevant文档
        query_tokens = set(query.lower().split())
        scored = []
        for doc in self.docs:
            score = len(query_tokens & set(doc.page_content.lower().split()))
            scored.append((score, doc))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [doc for score, doc in scored[: self.k]]

