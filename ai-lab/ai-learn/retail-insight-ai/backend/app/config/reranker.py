"""Reranker 的集中配置，避免候选数和最终返回数散落在业务代码中。"""

from __future__ import annotations

from dataclasses import dataclass


DEFAULT_RERANKER_CANDIDATE_LIMIT = 20
DEFAULT_RERANKER_TOP_K = 5


@dataclass(frozen=True)
class RerankerConfig:
    """定义 reranker 开关、provider 和 Top-N/Top-K 边界。"""

    enabled: bool = True
    provider: str = "deterministic"
    candidate_limit: int = DEFAULT_RERANKER_CANDIDATE_LIMIT
    top_k: int = DEFAULT_RERANKER_TOP_K

    def __post_init__(self) -> None:
        if self.provider != "deterministic":
            raise ValueError("unsupported reranker provider")
        if not 1 <= self.candidate_limit <= 100:
            raise ValueError("reranker candidate_limit must be within 1 and 100")
        if not 1 <= self.top_k <= 100:
            raise ValueError("reranker top_k must be within 1 and 100")


__all__ = [
    "DEFAULT_RERANKER_CANDIDATE_LIMIT",
    "DEFAULT_RERANKER_TOP_K",
    "RerankerConfig",
]
