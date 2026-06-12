from __future__ import annotations

from typing import Iterable, List

from _compat import DEFAULT_EMBED_DIM, hash_embed


class SentenceTransformer:
    def __init__(self, model_name: str, device: str | None = None):
        self.model_name = model_name
        self.device = device or "cpu"
        self._dimension = DEFAULT_EMBED_DIM

    def get_sentence_embedding_dimension(self) -> int:
        return self._dimension

    def encode(
        self,
        texts: str | Iterable[str],
        normalize_embeddings: bool = True,
        batch_size: int = 32,
        convert_to_numpy: bool = True,
    ):
        if isinstance(texts, str):
            texts = [texts]
        embeddings = [hash_embed(text, self._dimension) for text in texts]
        if convert_to_numpy:
            return embeddings
        return [embedding.tolist() for embedding in embeddings]

