from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Iterable, List, Sequence

from langchain_core.documents import Document
from _compat import hash_embed, cosine_similarity


class BM25Retriever:
    def __init__(self, docs: List[Document], k: int = 5):
        self.docs = docs
        self.k = k

    @classmethod
    def from_documents(cls, documents: List[Document], k: int = 5):
        return cls(documents, k=k)

    def invoke(self, query: str):
        return self.get_relevant_documents(query)

    def get_relevant_documents(self, query: str):
        query_tokens = set(query.lower().split())
        scored = []
        for doc in self.docs:
            score = len(query_tokens & set(doc.page_content.lower().split()))
            scored.append((score, doc))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [doc for score, doc in scored[: self.k]]

