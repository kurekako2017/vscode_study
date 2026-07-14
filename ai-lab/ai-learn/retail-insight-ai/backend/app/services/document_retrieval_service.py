"""文档检索服务。

文件职责：
- 提供 POST /api/v1/document-retrieval/search 的应用服务入口。
- 负责检索事件、错误语义和 HTTP contract 的稳定边界。
- 把 keyword/vector/hybrid 搜索下放给 retrieval provider，避免 service 依赖 raw chunk storage。

谁会调用它：
- `backend/app/api/document_retrieval.py` 路由通过依赖注入调用它。

它调用谁：
- `DocumentRetrievalProvider` 执行检索后端逻辑。
- `EventPublisher` 记录检索事件。

输入是什么：
- query、retrieval mode、top_k/limit 和文档元数据过滤。

输出是什么：
- `DocumentRetrievalSearchResponse`，或者抛出稳定的应用异常。

为什么需要这一层：
- 检索 service 只保留 API 和事件边界，向量 SQL、融合权重和 fallback 都留在 provider/repository。

日本现场面试怎么讲：
- 这是文档检索应用层：HTTP contract 稳定，三种检索策略由组合根注入。
"""

from __future__ import annotations

from threading import RLock

from app.errors.base import AppException
from app.errors.error_codes import ErrorCode
from app.errors.exceptions import InvalidQueryException
from app.events.publisher import EventPublisher
from app.observability.logging import get_logger, get_request_id, log_event
from app.repositories.implementations.in_memory.document_retrieval import InMemoryKeywordRetrieval
from app.repositories.interfaces.document_chunk_repository import DocumentChunkRepository
from app.repositories.interfaces.document_retrieval_provider import DocumentRetrievalProvider
from app.repositories.interfaces.document_repository import DocumentRepository
from app.schemas.document_retrieval_api import DocumentRetrievalSearchRequest, DocumentRetrievalSearchResponse

logger = get_logger(__name__)


class DocumentRetrievalService:
    """封装文档检索 API、事件发布和错误映射逻辑。"""

    def __init__(
        self,
        retrieval_provider: DocumentRetrievalProvider | DocumentRepository,
        event_publisher: EventPublisher | DocumentChunkRepository | None = None,
        chunk_repository: DocumentChunkRepository | None = None,
    ) -> None:
        """保存仓储与事件发布器，并初始化进程内互斥锁。"""

        if isinstance(retrieval_provider, DocumentRetrievalProvider):
            if not isinstance(event_publisher, EventPublisher):
                raise TypeError("event_publisher is required when retrieval_provider is a provider")
            provider = retrieval_provider
            publisher = event_publisher
        else:
            if not isinstance(event_publisher, DocumentChunkRepository) or not isinstance(chunk_repository, EventPublisher):
                raise TypeError("legacy constructor requires document_repository, chunk_repository, event_publisher")
            provider = InMemoryKeywordRetrieval(retrieval_provider, event_publisher)
            publisher = chunk_repository

        self._retrieval_provider = provider
        self._event_publisher = publisher
        self._lock = RLock()

    def search(self, request: DocumentRetrievalSearchRequest) -> DocumentRetrievalSearchResponse:
        """执行请求指定的检索模式，并返回稳定排序与真实 mode。"""

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

                results, total_matches = self._retrieval_provider.search(request)
                response = DocumentRetrievalSearchResponse(
                    results=results,
                    total=total_matches,
                    query=query,
                    retrieval_mode=request.retrieval_mode,
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

    def _normalize_query(self, value: str) -> str:
        """去掉首尾空白，避免空白 query 进入搜索逻辑。"""

        return value.strip()

    def _request_summary(self, request: DocumentRetrievalSearchRequest) -> dict[str, object]:
        """把检索请求摘要写入日志/事件，但不泄露原始 query。"""

        return {
            "query_length": len(request.query.strip()),
            "limit": request.limit,
            "top_k": request.top_k,
            "retrieval_mode": request.retrieval_mode,
            "document_id": request.document_id,
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
