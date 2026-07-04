"""文档检索服务。

文件职责：
- 提供 POST /api/v1/document-retrieval/search 的 keyword-only 检索逻辑。
- 在现有文档域与 chunk 域之上做只读排名，不引入 LLM、RAG 或向量检索。
- 记录检索事件，便于未来 SSE、审计和监控扩展。

谁会调用它：
- `backend/app/api/document_retrieval.py` 路由通过依赖注入调用它。

它调用谁：
- `DocumentRepository` 读取文档事实和过滤条件。
- `DocumentChunkRepository` 读取已生成的 chunk。
- `EventPublisher` 记录检索事件。

输入是什么：
- keyword 查询、limit、归档过滤、文档类型、语言和标签过滤。

输出是什么：
- `DocumentRetrievalSearchResponse`，或者抛出稳定的应用异常。

为什么需要这一层：
- 检索是 chunk 与 future RAG 之间的只读边界，不能把搜索逻辑塞进路由或模型层。

日本现场面试怎么讲：
- 这是文档检索的应用服务层，先做 deterministic keyword search，后续可以无痛替换成 PostgreSQL full-text 或 hybrid search。
"""

from __future__ import annotations

import re
from threading import RLock

from app.errors.base import AppException
from app.errors.error_codes import ErrorCode
from app.errors.exceptions import InvalidQueryException
from app.events.publisher import EventPublisher
from app.models.document import Document, DocumentChunk, DocumentStatus, DocumentType, Language
from app.observability.logging import get_logger, get_request_id, log_event
from app.repositories.interfaces.document_chunk_repository import DocumentChunkRepository
from app.repositories.interfaces.document_repository import DocumentRepository
from app.schemas.document_api import DocumentResponse, DocumentSourceResponse
from app.schemas.document_retrieval_api import (
    DocumentRetrievalResultResponse,
    DocumentRetrievalSearchRequest,
    DocumentRetrievalSearchResponse,
)

logger = get_logger(__name__)

_TOKEN_RE = re.compile(r"[\w\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff-]+", re.UNICODE)


class DocumentRetrievalService:
    """封装文档检索、过滤、排名和事件发布逻辑。"""

    def __init__(
        self,
        document_repository: DocumentRepository,
        chunk_repository: DocumentChunkRepository,
        event_publisher: EventPublisher,
    ) -> None:
        """保存仓储与事件发布器，并初始化进程内互斥锁。"""

        self._document_repository = document_repository
        self._chunk_repository = chunk_repository
        self._event_publisher = event_publisher
        self._lock = RLock()

    def search(self, request: DocumentRetrievalSearchRequest) -> DocumentRetrievalSearchResponse:
        """执行 keyword-only 检索，并返回稳定的结果排序。"""

        scope_id = self._scope_id()
        with self._lock:
            self._publish(
                scope_id,
                "document.retrieval.started",
                "Document retrieval started",
                status="running",
                extra=self._request_summary(request),
            )

            try:
                query = self._normalize_query(request.query)
                if not query:
                    raise InvalidQueryException(
                        {
                            "field": "query",
                            "reason": "query must not be blank",
                        }
                    )

                results, total_matches = self._search_documents(request, query)
                response = DocumentRetrievalSearchResponse(
                    results=results,
                    total=total_matches,
                    query=query,
                )
                self._publish(
                    scope_id,
                    "document.retrieval.completed",
                    "Document retrieval completed",
                    status="completed",
                    extra={
                        "result_count": len(results),
                        "total_matches": total_matches,
                        "query_length": len(query),
                        **self._request_summary(request),
                    },
                )
                return response
            except AppException as exc:
                self._publish(
                    scope_id,
                    "document.retrieval.failed",
                    "Document retrieval failed",
                    status="failed",
                    error_code=exc.error_code.value,
                    extra={
                        "error_code": exc.error_code.value,
                        **self._request_summary(request),
                    },
                )
                raise
            except Exception as exc:  # noqa: BLE001
                self._publish(
                    scope_id,
                    "document.retrieval.failed",
                    "Document retrieval failed",
                    status="failed",
                    error_code=ErrorCode.REPOSITORY_ERROR.value,
                    extra={
                        "error_code": ErrorCode.REPOSITORY_ERROR.value,
                        **self._request_summary(request),
                    },
                )
                raise AppException(
                    ErrorCode.REPOSITORY_ERROR,
                    "Retrieval storage error",
                    500,
                    detail={"query_length": len(self._normalize_query(request.query))},
                ) from exc

    def _search_documents(
        self,
        request: DocumentRetrievalSearchRequest,
        query: str,
    ) -> tuple[list[DocumentRetrievalResultResponse], int]:
        """读取文档与 chunk 快照，按 deterministic keyword score 排序。"""

        self._validate_limit(request.limit)
        document_type = self._parse_document_type(request.document_type)
        language = self._parse_language(request.language)
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

    def _request_summary(self, request: DocumentRetrievalSearchRequest) -> dict[str, object]:
        """把检索请求摘要写入日志/事件，但不泄露原始 query。"""

        return {
            "query_length": len(request.query.strip()),
            "limit": request.limit,
            "include_archived": request.include_archived,
            "document_type": request.document_type,
            "language": request.language,
            "tags_count": len(request.tags or []),
        }

    def _scope_id(self) -> str:
        """为检索请求生成可追踪的事件分组 ID。"""

        request_id = get_request_id()
        return f"document_retrieval:{request_id}"

    def _publish(
        self,
        scope_id: str,
        event_type: str,
        message: str,
        *,
        status: str,
        extra: dict[str, object] | None = None,
        error_code: str | None = None,
    ) -> None:
        """把检索状态变化写入统一事件仓库。"""

        payload = {
            "request_id": get_request_id(),
            "trace_id": get_request_id(),
            "status": status,
            "scope": scope_id,
        }
        if extra:
            payload.update(extra)
        event = self._event_publisher.publish(scope_id, event_type, message, payload)
        log_event(
            logger,
            "info",
            event_type,
            message,
            request_id=get_request_id(),
            task_id=scope_id,
            status=status,
            node="document_retrieval",
            error_code=error_code,
            sequence=event.sequence,
        )


__all__ = ["DocumentRetrievalService"]
