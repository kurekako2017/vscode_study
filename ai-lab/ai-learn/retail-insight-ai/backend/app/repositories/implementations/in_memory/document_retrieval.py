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
                    content_excerpt=self._content_excerpt(chunk.content, query_terms),
                    score=round(score, 4),
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
        limited = [item[4] for item in results[: request.limit]]
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


__all__ = ["InMemoryKeywordRetrieval"]
