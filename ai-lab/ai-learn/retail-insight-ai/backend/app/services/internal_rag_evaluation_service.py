"""Internal RAG 的内部评估服务。

文件职责：
- 评估 answer / citations / retrieval context 的质量。
- 生成 coverage_score、citation_score、confidence 和 warning 列表。
- 对 citation 做存在性和来源一致性校验。

谁会调用它：
- `backend/app/services/internal_rag_service.py`
- internal RAG 单元测试

它调用谁：
- 不依赖 repository 或 LLM，只处理已组装好的 answer/citations/contexts。

输入是什么：
- query、answer、citations、retrieval results。

输出是什么：
- `InternalRagEvaluationResult`。

为什么需要这一层：
- 这样 internal RAG 的业务编排和质量判断分开，未来替换 answer generation 或增加更复杂的评估规则时不会改 API。

日本现场面试怎么讲：
- 这是 internal RAG 的 quality gate，负责判断引用是否完整、上下文是否足够、以及回答是否是 weak match。
"""

from __future__ import annotations

from dataclasses import dataclass

from app.models.internal_rag import InternalRagEvaluationResult, InternalRagWarning
from app.schemas.document_retrieval_api import DocumentRetrievalResultResponse
from app.schemas.internal_rag_api import InternalRagCitationResponse


@dataclass(frozen=True)
class _CitationLookup:
    document_id: str
    chunk_id: str
    chunk_index: int
    excerpt: str
    score: float


class InternalRagEvaluationService:
    """把 internal RAG 的上下文和引用质量量化成可比较的分数。"""

    def evaluate(
        self,
        *,
        query: str,
        answer: str,
        citations: list[InternalRagCitationResponse],
        retrieval_results: list[DocumentRetrievalResultResponse],
        total_matches: int,
    ) -> InternalRagEvaluationResult:
        """评估回答质量并返回内部 scorecard。"""

        citation_lookup = self._build_lookup(retrieval_results)
        warnings: list[InternalRagWarning] = []
        valid_citation_count = 0
        citation_scores: list[float] = []
        for citation in citations:
            match = citation_lookup.get((citation.document_id, citation.chunk_id))
            if match is None:
                warnings.append(InternalRagWarning.MISSING_CITATION)
                continue
            if not self._citation_excerpt_is_grounded(citation.excerpt, match.excerpt):
                warnings.append(InternalRagWarning.MISSING_CITATION)
                continue
            valid_citation_count += 1
            citation_scores.append(self._citation_quality_score(citation.score, match.score))

        citation_count = len(citations)
        if citation_count == 0:
            citation_score = 0.0
        else:
            citation_score = round(valid_citation_count / citation_count, 2)

        coverage_score = self._coverage_score(valid_citation_count, total_matches)
        if coverage_score < 0.75:
            warnings.append(InternalRagWarning.LOW_CONTEXT)
        if citation_scores and sum(citation_scores) / len(citation_scores) < 0.65:
            warnings.append(InternalRagWarning.WEAK_MATCH)

        confidence = self._confidence_from_scores(coverage_score, citation_score, citation_scores, warnings)
        return InternalRagEvaluationResult(
            query=query,
            answer=answer,
            citations=[self._citation_to_payload(citation) for citation in citations],
            coverage_score=coverage_score,
            citation_score=citation_score,
            confidence=confidence,
            warnings=tuple(dict.fromkeys(warnings)),
        )

    def _build_lookup(
        self,
        retrieval_results: list[DocumentRetrievalResultResponse],
    ) -> dict[tuple[str, str], _CitationLookup]:
        """把 retrieval 结果整理成 citation 校验用索引。"""

        lookup: dict[tuple[str, str], _CitationLookup] = {}
        for result in retrieval_results:
            lookup[(result.document_id, result.chunk_id)] = _CitationLookup(
                document_id=result.document_id,
                chunk_id=result.chunk_id,
                chunk_index=result.chunk_index,
                excerpt=result.content_excerpt,
                score=result.score,
            )
        return lookup

    def _citation_to_payload(self, citation: InternalRagCitationResponse) -> dict[str, object]:
        """把 citation 归一化成便于记录的内部 payload。"""

        return {
            "document_id": citation.document_id,
            "chunk_id": citation.chunk_id,
            "chunk_index": citation.chunk_index,
            "excerpt": citation.excerpt,
            "score": citation.score,
        }

    def _citation_excerpt_is_grounded(self, citation_excerpt: str, retrieved_excerpt: str) -> bool:
        """验证 citation excerpt 是否来自 retrieval chunk 内容。"""

        citation_normalized = " ".join(citation_excerpt.split()).lower()
        retrieved_normalized = " ".join(retrieved_excerpt.split()).lower()
        return citation_normalized in retrieved_normalized or retrieved_normalized in citation_normalized

    def _citation_quality_score(self, citation_score: float, retrieval_score: float) -> float:
        """把 retrieval score 和 citation score 合并为 citation quality。"""

        return round(min(1.0, (citation_score + retrieval_score) / 2.0), 2)

    def _coverage_score(self, valid_citation_count: int, total_matches: int) -> float:
        """衡量当前回答覆盖了多少可用检索结果。"""

        if total_matches <= 0:
            return 0.0
        return round(min(1.0, valid_citation_count / total_matches), 2)

    def _confidence_from_scores(
        self,
        coverage_score: float,
        citation_score: float,
        citation_scores: list[float],
        warnings: list[InternalRagWarning],
    ) -> float:
        """把 coverage / citation / warning 情况折算成确定性的 confidence。"""

        average_citation_score = sum(citation_scores) / len(citation_scores) if citation_scores else 0.0
        warning_penalty = 0.05 * len(tuple(dict.fromkeys(warnings)))
        confidence = (coverage_score * 0.45) + (citation_score * 0.35) + (average_citation_score * 0.2) - warning_penalty
        return round(max(0.0, min(0.99, confidence)), 2)


__all__ = ["InternalRagEvaluationService"]
