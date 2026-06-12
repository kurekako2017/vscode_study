from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, List

from _compat import DEFAULT_EMBED_DIM, hash_embed


@dataclass
class FakeEmbeddings:
    size: int = DEFAULT_EMBED_DIM

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [hash_embed(text, self.size).tolist() for text in texts]

    def embed_query(self, text: str) -> List[float]:
        return hash_embed(text, self.size).tolist()


class HuggingFaceEmbeddings(FakeEmbeddings):
    def __init__(self, model_name: str = "offline/hash-embed", model_kwargs: dict[str, Any] | None = None, encode_kwargs: dict[str, Any] | None = None, size: int = DEFAULT_EMBED_DIM):
        super().__init__(size=size)
        self.model_name = model_name
        self.model_kwargs = model_kwargs or {}
        self.encode_kwargs = encode_kwargs or {}


class HuggingFaceBgeEmbeddings(HuggingFaceEmbeddings):
    pass

