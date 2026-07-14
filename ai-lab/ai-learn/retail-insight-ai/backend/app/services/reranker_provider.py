"""Reranker provider contract 与本地 deterministic 实现。

文件职责：
- 定义 query + retrieved chunks -> reranked chunks 的独立 provider 接口。
- 使用可解释规则和 SHA-256 tie-break，保证跨进程、跨机器结果一致。

谁会调用它：
- `RerankerService`，Repository 和 Retrieval Service 永远不会调用本文件。

输入与输出：
- 输入是 query 和只读候选 chunk 列表。
- 输出附加 rerank_score、reason、metadata，但保留原 content、score 与 metadata。

日本现场面试怎么讲：
- 这是可替换的二阶段排序接口；当前 provider 无外部模型依赖，未来可换 cross-encoder 而不改检索仓储。
"""

from __future__ import annotations

import hashlib
import re
from abc import ABC, abstractmethod

from app.schemas.document_retrieval_api import DocumentRetrievalResultResponse
from app.schemas.reranker import RerankedDocumentChunk

_TOKEN_RE = re.compile(r"[\w\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff-]+", re.UNICODE)


class RerankerProvider(ABC):
    """定义独立于 retrieval provider 的二阶段排序合同。"""

    name: str

    @abstractmethod
    def rerank(
        self,
        query: str,
        chunks: list[DocumentRetrievalResultResponse],
    ) -> list[RerankedDocumentChunk]:
        """对候选评分并返回稳定排序，不修改输入 chunk。"""


class DeterministicRerankerProvider(RerankerProvider):
    """使用关键词覆盖率、原检索分数、短语命中与原位置进行稳定排序。"""

    name = "deterministic"

    def rerank(
        self,
        query: str,
        chunks: list[DocumentRetrievalResultResponse],
    ) -> list[RerankedDocumentChunk]:
        """按 rerank_score 排序，并对完全相同的 chunk identity 去重。"""

        query_terms = self._unique_terms(query)
        normalized_query = " ".join(query_terms)
        ranked: list[tuple[float, str, RerankedDocumentChunk]] = []
        seen: set[tuple[str, str]] = set()
        for original_rank, chunk in enumerate(chunks):
            identity = (chunk.document_id, chunk.chunk_id)
            if identity in seen:
                continue
            seen.add(identity)

            content_terms = set(self._unique_terms(chunk.content))
            matched_terms = tuple(term for term in query_terms if term in content_terms)
            coverage = len(matched_terms) / len(query_terms) if query_terms else 0.0
            normalized_content = " ".join(self._unique_terms(chunk.content))
            phrase_match = 1.0 if normalized_query and normalized_query in normalized_content else 0.0
            retrieval_score = max(0.0, min(1.0, chunk.score))
            position_score = 1.0 / (original_rank + 1)
            rerank_score = round(
                (coverage * 0.55)
                + (retrieval_score * 0.30)
                + (phrase_match * 0.10)
                + (position_score * 0.05),
                6,
            )
            tie_breaker = self._tie_breaker(chunk)
            reason = (
                f"keyword_coverage={coverage:.4f};retrieval_score={retrieval_score:.4f};"
                f"phrase_match={phrase_match:.1f};original_rank={original_rank}"
            )
            result = RerankedDocumentChunk(
                chunk=chunk,
                rerank_score=rerank_score,
                reason=reason,
                metadata={
                    "provider": self.name,
                    "original_rank": original_rank,
                    "matched_terms": matched_terms,
                    "query_term_count": len(query_terms),
                    "tie_breaker": tie_breaker,
                },
            )
            ranked.append((rerank_score, tie_breaker, result))

        ranked.sort(key=lambda item: (-item[0], item[1]))
        return [item[2] for item in ranked]

    def _unique_terms(self, value: str) -> tuple[str, ...]:
        """稳定分词并按首次出现顺序去重。"""

        return tuple(dict.fromkeys(_TOKEN_RE.findall(value.lower())))

    def _tie_breaker(self, chunk: DocumentRetrievalResultResponse) -> str:
        """使用稳定摘要打破同分，禁止依赖进程随机化的内置 hash。"""

        canonical = "\x1f".join(
            (chunk.document_id, chunk.chunk_id, str(chunk.chunk_index), chunk.content)
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


__all__ = ["DeterministicRerankerProvider", "RerankerProvider"]
