"""InMemoryKeywordRetrieval 的本地实现。

文件职责：
- 提供当前阶段可运行的 keyword-only 文档检索后端。
- 读取文档与 chunk 仓储，完成过滤、评分、排序和结果组装。

谁会调用它：
- `DocumentRetrievalService` 调用它，而不是直接碰 chunk 仓储。

它调用谁：
- `DocumentRepository` 读取文档事实。
- `DocumentChunkRepository` 读取已生成 chunk。

输入是什么：
- `DocumentRetrievalSearchRequest`。

输出是什么：
- 检索结果列表与总命中数。

为什么需要这一层：
- 先把检索算法放进 provider 边界，service 只保留 API/事件语义，后续替换 PostgreSQL full-text 或 hybrid search 时可以维持同一合同。

日本现场面试怎么讲：
- 这是当前阶段的 InMemoryKeywordRetrieval，核心 service 不依赖 raw chunk storage，未来搜索后端可以无痛替换。
"""

from __future__ import annotations

import re

from app.config.retrieval import HybridRetrievalConfig
from app.embeddings.service import EmbeddingProviderError, EmbeddingService
from app.errors.base import AppException
from app.errors.error_codes import ErrorCode
from app.errors.exceptions import InvalidQueryException
from app.models.document import Document, DocumentChunk, DocumentStatus, DocumentType, Language
from app.repositories.interfaces.document_chunk_repository import DocumentChunkRepository
from app.repositories.interfaces.document_retrieval_provider import DocumentRetrievalProvider
from app.repositories.interfaces.document_repository import DocumentRepository
from app.schemas.document_api import DocumentResponse, DocumentSourceResponse
from app.schemas.document_retrieval_api import (
    DocumentRetrievalResultResponse,
    DocumentRetrievalSearchRequest,
)

_TOKEN_RE = re.compile(r"[\w\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff-]+", re.UNICODE)


class InMemoryKeywordRetrieval(DocumentRetrievalProvider):
    """基于现有内存文档与 chunk 仓储的 keyword 检索实现。"""

    name = "inmemory_keyword"

    def __init__(
        self,
        document_repository: DocumentRepository,
        chunk_repository: DocumentChunkRepository,
    ) -> None:
        """注入文档仓储与 chunk 仓储，避免检索 service 直接接触 storage 细节。"""

        self._document_repository = document_repository
        self._chunk_repository = chunk_repository

    def search(self, request: DocumentRetrievalSearchRequest) -> tuple[list[DocumentRetrievalResultResponse], int]:
        """执行 keyword-only 检索，返回稳定排序后的结果。"""

        self._validate_limit(request.limit)
        document_type = self._parse_document_type(request.document_type)
        language = self._parse_language(request.language)

        query = self._normalize_query(request.query)
        if not query:
            raise InvalidQueryException({"field": "query", "reason": "query must not be blank"})

        query_terms = self._unique_terms(query)
        if not query_terms:
            raise InvalidQueryException({"field": "query", "reason": "query must contain searchable terms"})
        normalized_query = " ".join(query_terms)

        results: list[tuple[float, str, int, str, DocumentRetrievalResultResponse]] = []
        for document in self._iter_documents():
            if not self._matches_document(document, request, document_type=document_type, language=language):
                continue
            chunks = self._chunk_repository.list_for_document(document.document_id, document.version)
            for chunk in chunks:
                score = self._score_chunk(chunk, query_terms, normalized_query)
                if score <= 0:
                    continue
                result = DocumentRetrievalResultResponse(
                    document_id=document.document_id,
                    chunk_id=chunk.chunk_id,
                    chunk_index=chunk.chunk_index,
                    content=chunk.content,
                    content_excerpt=self._content_excerpt(chunk.content, query_terms),
                    score=round(score, 4),
                    retrieval_method="keyword",
                    source=DocumentSourceResponse.from_domain(document.metadata.source),
                    metadata=DocumentResponse.from_domain(document),
                )
                results.append(
                    (
                        result.score,
                        result.document_id,
                        result.chunk_index,
                        result.chunk_id,
                        result,
                    )
                )

        results.sort(key=lambda item: (-item[0], item[1], item[2], item[3]))
        limited = [item[4] for item in results[: request.effective_limit]]
        return limited, len(results)

    def _iter_documents(self) -> list[Document]:
        """按 document_id 排序返回文档快照，确保检索顺序稳定。"""

        documents = self._document_repository.list_all()
        return sorted(documents, key=lambda document: document.document_id)

    def _matches_document(
        self,
        document: Document,
        request: DocumentRetrievalSearchRequest,
        *,
        document_type: DocumentType | None,
        language: Language | None,
    ) -> bool:
        """先做元数据过滤，再进入 chunk 级 keyword 排名。"""

        metadata = document.metadata
        if metadata.status is DocumentStatus.ARCHIVED and not request.include_archived:
            return False
        if document_type is not None and metadata.document_type is not document_type:
            return False
        if language is not None and metadata.language is not language:
            return False
        if request.tags:
            tags = set(metadata.tags)
            if not set(request.tags).issubset(tags):
                return False
        if request.document_id is not None and document.document_id != request.document_id:
            return False
        return True

    def _validate_limit(self, limit: int) -> None:
        """冻结 limit 范围，避免越界分页破坏 contract。"""

        if limit < 1 or limit > 100:
            raise InvalidQueryException({"field": "limit", "reason": "limit must be within 1 and 100"})

    def _parse_document_type(self, value: str | None) -> DocumentType | None:
        """把字符串 filter 转成领域枚举，保持 request 轻量。"""

        if value is None:
            return None
        try:
            return DocumentType(value)
        except ValueError as exc:
            raise InvalidQueryException({"field": "document_type", "reason": "unsupported document_type", "value": value}) from exc

    def _parse_language(self, value: str | None) -> Language | None:
        """把字符串 filter 转成领域枚举，保持 request 轻量。"""

        if value is None:
            return None
        try:
            return Language(value)
        except ValueError as exc:
            raise InvalidQueryException({"field": "language", "reason": "unsupported language", "value": value}) from exc

    def _score_chunk(
        self,
        chunk: DocumentChunk,
        query_terms: list[str],
        normalized_query: str,
    ) -> float:
        """只基于 chunk.content 计算 deterministic keyword score。"""

        content = chunk.content.lower()
        matched_terms = [term for term in query_terms if term in content]
        if not matched_terms:
            return 0.0

        score = len(matched_terms) / len(query_terms)
        if normalized_query in content:
            score = min(1.0, score + 0.25)
        return score

    def _unique_terms(self, value: str) -> list[str]:
        """提取稳定的 keyword tokens，保留出现顺序并去重。"""

        tokens = _TOKEN_RE.findall(value.lower())
        unique: list[str] = []
        seen: set[str] = set()
        for token in tokens:
            if token not in seen:
                seen.add(token)
                unique.append(token)
        return unique

    def _normalize_query(self, value: str) -> str:
        """去掉首尾空白，避免空白 query 进入搜索逻辑。"""

        return value.strip()

    def _content_excerpt(self, content: str, query_terms: list[str], window: int = 160) -> str:
        """截取与命中词相关的稳定摘要，优先返回最早命中附近内容。"""

        lowered = content.lower()
        hit_index = len(content)
        for term in query_terms:
            index = lowered.find(term)
            if index != -1 and index < hit_index:
                hit_index = index

        if hit_index == len(content):
            excerpt = content[:window]
        else:
            start = max(0, hit_index - window // 3)
            end = min(len(content), start + window)
            excerpt = content[start:end]
        excerpt = " ".join(excerpt.split())
        if len(excerpt) > window:
            excerpt = excerpt[: window - 3].rstrip() + "..."
        return excerpt


class VectorDocumentRetrieval(DocumentRetrievalProvider):
    """通过 EmbeddingService 与同一 Chunk Repository 执行 cosine 检索。"""

    name = "vector"

    def __init__(
        self,
        document_repository: DocumentRepository,
        chunk_repository: DocumentChunkRepository,
        embedding_service: EmbeddingService,
    ) -> None:
        self._document_repository = document_repository
        self._chunk_repository = chunk_repository
        self._embedding_service = embedding_service
        self._filters = InMemoryKeywordRetrieval(document_repository, chunk_repository)

    @property
    def available(self) -> bool:
        return self._embedding_service.available

    def search(self, request: DocumentRetrievalSearchRequest) -> tuple[list[DocumentRetrievalResultResponse], int]:
        """生成 query vector，并把 cosine 排序下放给当前 Repository backend。"""

        self._filters._validate_limit(request.effective_limit)
        query = self._filters._normalize_query(request.query)
        if not query:
            raise InvalidQueryException({"field": "query", "reason": "query must not be blank"})
        if not self.available:
            raise AppException(
                ErrorCode.RETRIEVAL_UNAVAILABLE,
                "Vector retrieval requires an explicitly configured embedding provider",
                503,
            )
        document_type = self._filters._parse_document_type(request.document_type)
        language = self._filters._parse_language(request.language)
        documents = [
            document
            for document in self._filters._iter_documents()
            if self._filters._matches_document(
                document,
                request,
                document_type=document_type,
                language=language,
            )
        ]
        by_id = {document.document_id: document for document in documents}
        try:
            query_embedding = self._embedding_service.embed_text(query)
        except EmbeddingProviderError as exc:
            raise AppException(
                ErrorCode.RETRIEVAL_UNAVAILABLE,
                "Embedding provider failed during vector retrieval",
                503,
                detail={"provider": self._embedding_service.provider.name},
            ) from exc
        matches = self._chunk_repository.search_by_embedding(
            query_embedding,
            limit=request.effective_limit,
            document_ids=list(by_id),
        )
        results: list[DocumentRetrievalResultResponse] = []
        for match in matches:
            document = by_id.get(match.chunk.document_id)
            if document is None:
                continue
            # cosine 的范围是 [-1, 1]；映射到 [0, 1] 后才能与 keyword score 合并。
            score = max(0.0, min(1.0, (match.cosine_similarity + 1.0) / 2.0))
            results.append(
                DocumentRetrievalResultResponse(
                    document_id=document.document_id,
                    chunk_id=match.chunk.chunk_id,
                    chunk_index=match.chunk.chunk_index,
                    content=match.chunk.content,
                    content_excerpt=self._filters._content_excerpt(match.chunk.content, []),
                    score=round(score, 6),
                    retrieval_method="vector",
                    source=DocumentSourceResponse.from_domain(document.metadata.source),
                    metadata=DocumentResponse.from_domain(document),
                )
            )
        results.sort(key=lambda item: (-item.score, item.document_id, item.chunk_index, item.chunk_id))
        return results, len(results)


class HybridDocumentRetrieval(DocumentRetrievalProvider):
    """路由三种 mode，并在 hybrid 下归一化、加权和按 chunk_id 去重。"""

    name = "hybrid"

    def __init__(
        self,
        keyword: InMemoryKeywordRetrieval,
        vector: VectorDocumentRetrieval,
        config: HybridRetrievalConfig | None = None,
    ) -> None:
        self._keyword = keyword
        self._vector = vector
        self._config = config or HybridRetrievalConfig()

    def search(self, request: DocumentRetrievalSearchRequest) -> tuple[list[DocumentRetrievalResultResponse], int]:
        if request.retrieval_mode == "keyword":
            return self._keyword.search(request)
        if request.retrieval_mode == "vector":
            return self._vector.search(request)

        keyword_results, _ = self._keyword.search(request)
        if not self._vector.available:
            return self._as_hybrid(keyword_results), len(keyword_results)
        vector_results, _ = self._vector.search(request)
        if not vector_results:
            return self._as_hybrid(keyword_results), len(keyword_results)

        keyword_scores = self._normalize(keyword_results)
        vector_scores = self._normalize(vector_results)
        keyword_weight, vector_weight = self._config.normalized_weights
        candidates = {item.chunk_id: item for item in keyword_results}
        for item in vector_results:
            candidates.setdefault(item.chunk_id, item)

        merged: list[DocumentRetrievalResultResponse] = []
        for chunk_id, item in candidates.items():
            score = (
                keyword_weight * keyword_scores.get(chunk_id, 0.0)
                + vector_weight * vector_scores.get(chunk_id, 0.0)
            )
            merged.append(item.model_copy(update={"score": round(score, 6), "retrieval_method": "hybrid"}))
        merged.sort(key=lambda item: (-item.score, item.document_id, item.chunk_index, item.chunk_id))
        return merged[: request.effective_limit], len(merged)

    def _normalize(self, results: list[DocumentRetrievalResultResponse]) -> dict[str, float]:
        """按当前候选最大分归一化；空路或零分保持空/零。"""

        if not results:
            return {}
        maximum = max(item.score for item in results)
        if maximum <= 0:
            return {item.chunk_id: 0.0 for item in results}
        return {item.chunk_id: item.score / maximum for item in results}

    def _as_hybrid(
        self, results: list[DocumentRetrievalResultResponse]
    ) -> list[DocumentRetrievalResultResponse]:
        """无向量数据时保留 keyword score，但如实标记请求走的是 hybrid。"""

        return [item.model_copy(update={"retrieval_method": "hybrid"}) for item in results]


__all__ = ["HybridDocumentRetrieval", "InMemoryKeywordRetrieval", "VectorDocumentRetrieval"]
