"""Hybrid Retrieval 的集中权重配置。"""

from __future__ import annotations

from dataclasses import dataclass


DEFAULT_HYBRID_KEYWORD_WEIGHT = 0.5
DEFAULT_HYBRID_VECTOR_WEIGHT = 0.5


@dataclass(frozen=True)
class HybridRetrievalConfig:
    """保存两路权重，并拒绝无法计算的全零配置。"""

    keyword_weight: float = DEFAULT_HYBRID_KEYWORD_WEIGHT
    vector_weight: float = DEFAULT_HYBRID_VECTOR_WEIGHT

    def __post_init__(self) -> None:
        if self.keyword_weight < 0 or self.vector_weight < 0:
            raise ValueError("hybrid retrieval weights must not be negative")
        if self.keyword_weight + self.vector_weight <= 0:
            raise ValueError("at least one hybrid retrieval weight must be positive")

    @property
    def normalized_weights(self) -> tuple[float, float]:
        total = self.keyword_weight + self.vector_weight
        return self.keyword_weight / total, self.vector_weight / total


__all__ = [
    "DEFAULT_HYBRID_KEYWORD_WEIGHT",
    "DEFAULT_HYBRID_VECTOR_WEIGHT",
    "HybridRetrievalConfig",
]
