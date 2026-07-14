"""Embedding 执行与验证边界。

文件职责：统一校验文本、批次、维度和数值，并隔离 Provider 异常。
谁调用它：Chunk embedding 与 Vector Retrieval；它调用可替换的 EmbeddingProvider。
输入输出：文本或文本批次进，固定维度有限浮点向量出。
为什么这样设计：业务层不应重复校验厂商响应；日本现场可说明为 Adapter 输出防腐层。
"""

from __future__ import annotations

import math
from collections.abc import Sequence

from app.embeddings.config import EMBEDDING_DIMENSIONS
from app.embeddings.interface import EmbeddingProvider


class EmbeddingValidationError(ValueError):
    """表示输入文本或 Provider 输出不符合固定合同。"""


class EmbeddingProviderError(RuntimeError):
    """表示 Provider 执行失败，调用方不得静默伪造向量。"""


def validate_embedding_vector(
    vector: Sequence[float],
    *,
    dimensions: int = EMBEDDING_DIMENSIONS,
) -> tuple[float, ...]:
    """把向量规范化为不可变 tuple，并拒绝错误维度及 NaN/Infinity。"""

    if len(vector) != dimensions:
        raise EmbeddingValidationError(
            f"embedding vector dimension must be {dimensions}, got {len(vector)}"
        )
    normalized: list[float] = []
    for value in vector:
        try:
            numeric = float(value)
        except (TypeError, ValueError) as exc:
            raise EmbeddingValidationError("embedding vector must contain floats") from exc
        if not math.isfinite(numeric):
            raise EmbeddingValidationError("embedding vector must not contain NaN or Infinity")
        normalized.append(numeric)
    return tuple(normalized)


class EmbeddingService:
    """执行 Provider 并验证其完整输出，避免异常或坏向量进入 Repository。"""

    def __init__(self, provider: EmbeddingProvider, dimensions: int = EMBEDDING_DIMENSIONS) -> None:
        self.provider = provider
        self.dimensions = dimensions
        if provider.dimensions != dimensions:
            raise EmbeddingValidationError(
                f"provider dimension must be {dimensions}, got {provider.dimensions}"
            )

    @property
    def available(self) -> bool:
        """disabled 是明确的未配置状态，不代表 Provider 执行失败。"""

        return self.provider.name != "disabled"

    def embed_text(self, text: str) -> tuple[float, ...]:
        """生成单个向量。"""

        return self.embed_batch([text])[0]

    def embed_batch(self, texts: Sequence[str]) -> list[tuple[float, ...]]:
        """批量生成向量，并验证数量、维度和数值有限性。"""

        if not texts:
            raise EmbeddingValidationError("embedding batch must not be empty")
        normalized_texts: list[str] = []
        for text in texts:
            if not isinstance(text, str) or not text.strip():
                raise EmbeddingValidationError("embedding text must not be blank")
            normalized_texts.append(text.strip())
        try:
            vectors = self.provider.embed_batch(normalized_texts)
        except Exception as exc:  # noqa: BLE001
            raise EmbeddingProviderError(
                f"embedding provider '{self.provider.name}' failed"
            ) from exc
        if len(vectors) != len(normalized_texts):
            raise EmbeddingValidationError(
                "embedding provider result count must match input count"
            )
        return [
            validate_embedding_vector(vector, dimensions=self.dimensions)
            for vector in vectors
        ]


__all__ = [
    "EmbeddingProviderError",
    "EmbeddingService",
    "EmbeddingValidationError",
    "validate_embedding_vector",
]
