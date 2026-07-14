"""Reranker 应用服务。

文件职责：
- 在 retrieval 之后执行 Top-N 候选截断和 Final Top-K 选择。
- provider disabled、缺失或异常时保留 retrieval 原顺序，不把可选排序能力升级成 500。

谁会调用它：
- `InternalRagService` 在拿到 Hybrid/Keyword/Vector 候选后调用。

它调用谁：
- `RerankerProvider`；不会调用 Repository，也不会重新执行 Retrieval。

日本现场面试怎么讲：
- Service 管策略与降级，Provider 管评分算法，Repository 只负责候选召回，三者职责可独立替换和测试。
"""

from __future__ import annotations

from time import perf_counter

from app.config.reranker import RerankerConfig
from app.observability.logging import get_logger, get_request_id, log_event
from app.schemas.document_retrieval_api import DocumentRetrievalResultResponse
from app.schemas.reranker import RerankedDocumentChunk, RerankerFallbackReason, RerankerOutcome
from app.services.reranker_provider import RerankerProvider

logger = get_logger(__name__)


class RerankerService:
    """编排候选窗口、provider 与可用性 fallback。"""

    def __init__(
        self,
        provider: RerankerProvider | None,
        config: RerankerConfig | None = None,
    ) -> None:
        self._provider = provider
        self._config = config or RerankerConfig()

    @property
    def config(self) -> RerankerConfig:
        """向上游暴露只读配置，用于一次性请求足够的候选。"""

        return self._config

    def candidate_limit_for(self, top_k: int | None = None) -> int:
        """Top-N 不得小于 Final Top-K，并保持 retrieval contract 的 100 上限。"""

        effective_top_k = top_k if top_k is not None else self._config.top_k
        return min(100, max(self._config.candidate_limit, effective_top_k))

    def rerank(
        self,
        query: str,
        chunks: list[DocumentRetrievalResultResponse],
        *,
        top_k: int | None = None,
    ) -> RerankerOutcome:
        """执行二阶段排序；fallback 时保留候选的原始顺序与字段。"""

        effective_top_k = top_k if top_k is not None else self._config.top_k
        if not 1 <= effective_top_k <= 100:
            raise ValueError("reranker top_k must be within 1 and 100")
        candidate_limit = self.candidate_limit_for(effective_top_k)
        candidates = list(chunks[:candidate_limit])
        if not candidates:
            return RerankerOutcome(
                chunks=(),
                provider_name=self._provider.name if self._provider is not None else None,
                used_provider=False,
            )
        if not self._config.enabled:
            return self._fallback(candidates, effective_top_k, "disabled")
        if self._provider is None:
            return self._fallback(candidates, effective_top_k, "missing_provider")

        started_at = perf_counter()
        try:
            ranked = self._provider.rerank(query, candidates)
        except Exception:  # noqa: BLE001
            duration_ms = (perf_counter() - started_at) * 1000
            log_event(
                logger,
                "warning",
                "reranker.provider_failed",
                "Reranker provider failed; retrieval order preserved",
                request_id=get_request_id(),
                status="fallback",
                node="reranker",
                error_code="reranker_provider_error",
                duration_ms=duration_ms,
            )
            return self._fallback(candidates, effective_top_k, "provider_error")

        return RerankerOutcome(
            chunks=tuple(ranked[:effective_top_k]),
            provider_name=self._provider.name,
            used_provider=True,
        )

    def _fallback(
        self,
        candidates: list[DocumentRetrievalResultResponse],
        top_k: int,
        reason: RerankerFallbackReason,
    ) -> RerankerOutcome:
        """用独立包装保留 retrieval 顺序，明确本次没有产生 rerank score。"""

        wrapped = tuple(
            RerankedDocumentChunk(
                chunk=chunk,
                rerank_score=None,
                reason=f"reranker_{reason};retrieval_order_preserved",
                metadata={"fallback": True, "original_rank": index},
            )
            for index, chunk in enumerate(candidates[:top_k])
        )
        return RerankerOutcome(
            chunks=wrapped,
            provider_name=self._provider.name if self._provider is not None else None,
            used_provider=False,
            fallback_reason=reason,
        )


__all__ = ["RerankerService"]
