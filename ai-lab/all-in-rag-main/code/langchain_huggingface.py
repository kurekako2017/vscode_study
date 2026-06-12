from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, List

from _compat import DEFAULT_EMBED_DIM, hash_embed


@dataclass
class HuggingFaceEmbeddings:
    model_name: str = "offline/hash-embed"
    model_kwargs: dict[str, Any] | None = None
    encode_kwargs: dict[str, Any] | None = None
    dimension: int = DEFAULT_EMBED_DIM

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [hash_embed(text, self.dimension).tolist() for text in texts]

    def embed_query(self, text: str) -> List[float]:
        return hash_embed(text, self.dimension).tolist()

    def __call__(self, texts: Iterable[str]) -> List[List[float]]:
        return self.embed_documents(list(texts))

