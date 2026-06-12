from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List

import numpy as np
from langchain_core.documents import Document

from _compat import hash_embed, cosine_similarity, save_json, load_json


class _Retriever:
    def __init__(self, store, search_kwargs=None):
        self.store = store
        self.search_kwargs = search_kwargs or {"k": 4}

    def invoke(self, query: str):
        return self.get_relevant_documents(query)

    def get_relevant_documents(self, query: str):
        return self.store.similarity_search(query, k=self.search_kwargs.get("k", 4))


class _BaseVectorStore:
    def __init__(self, docs: List[Document] | None = None, embedding=None):
        self.embedding = embedding
        self.documents: List[Document] = docs or []
        self.vectors: List[List[float]] = []
        if docs:
            self._rebuild()

    def _embed(self, text: str):
        if self.embedding and hasattr(self.embedding, "embed_query"):
            return self.embedding.embed_query(text)
        return hash_embed(text).tolist()

    def _rebuild(self):
        self.vectors = [self._embed(doc.page_content) for doc in self.documents]

    @classmethod
    def from_documents(cls, documents: List[Document], embedding=None, **kwargs):
        return cls(list(documents), embedding=embedding)

    def add_documents(self, documents: List[Document]):
        self.documents.extend(documents)
        self._rebuild()

    def similarity_search(self, query: str, k: int = 4):
        if not self.documents:
            return []
        query_vec = self._embed(query)
        scores = cosine_similarity(query_vec, self.vectors)[0]
        ranked = sorted(zip(scores, self.documents), key=lambda item: item[0], reverse=True)
        return [doc for _, doc in ranked[:k]]

    def as_retriever(self, search_kwargs=None, **kwargs):
        return _Retriever(self, search_kwargs=search_kwargs)

    def save_local(self, path: str):
        path_obj = Path(path)
        path_obj.mkdir(parents=True, exist_ok=True)
        payload = [
            {"page_content": doc.page_content, "metadata": doc.metadata}
            for doc in self.documents
        ]
        save_json(path_obj / "store.json", payload)

    @classmethod
    def load_local(cls, path: str, embedding=None, allow_dangerous_deserialization: bool = False):
        payload = load_json(Path(path) / "store.json", [])
        docs = [Document(page_content=item["page_content"], metadata=item.get("metadata", {})) for item in payload]
        return cls(docs, embedding=embedding)


class FAISS(_BaseVectorStore):
    pass


class Chroma(_BaseVectorStore):
    pass


class InMemoryVectorStore(_BaseVectorStore):
    def __init__(self, embedding=None):
        super().__init__([], embedding=embedding)

