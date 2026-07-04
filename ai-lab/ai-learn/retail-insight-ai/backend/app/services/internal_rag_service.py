"""Internal RAG 应用服务。

文件职责：
- 在 existing DocumentRetrievalProvider 之上组装 grounded answer。
- 负责 internal_rag.started / retrieval_completed / answer_generated / failed 事件。
- 维持 answer_mode、citation 和 confidence 的确定性输出。

谁会调用它：
- `backend/app/api/internal_rag.py` 路由通过依赖注入调用它。

它调用谁：
- `DocumentRetrievalProvider` 获取检索结果。
- `EventPublisher` 记录 internal RAG 事件。

输入是什么：
- `InternalRagAnswerRequest`，包含 question、limit、filters 和 answer_mode。

输出是什么：
- `InternalRagAnswerResponse`，或者抛出稳定的应用异常。

为什么需要这一层：
- 把“检索”和“回答合成”分成两个稳定边界，未来接 LLM provider 时只替换合成策略，不动 retrieval contract。

日本现场面试怎么讲：
- 这是 retrieval 之后的 grounded answer service，当前先用 deterministic 规则实现，后续再平滑替换成真实 LLM。
"""

from __future__ import annotations

from threading import RLock

from app.errors.base import AppException
from app.errors.error_codes import ErrorCode
from app.errors.exceptions import (
    CitationRequiredException,
    InsufficientContextException,
    InvalidQuestionException,
    InvalidQueryException,
)
from app.events.publisher import EventPublisher
from app.models.document import DocumentType, Language
from app.models.internal_rag import InternalRagWarning
from app.observability.logging import get_logger, get_request_id, log_event
from app.repositories.interfaces.document_retrieval_provider import DocumentRetrievalProvider
from app.schemas.document_retrieval_api import DocumentRetrievalSearchRequest
from app.schemas.internal_rag_api import (
    InternalRagAnswerRequest,
    InternalRagAnswerResponse,
)
from app.services.internal_rag_evaluation_service import InternalRagEvaluationService
from app.services.rag_answer_generator import RAGAnswerGenerator

logger = get_logger(__name__)


class InternalRagService:
    """把检索结果转换成可审计、可引用的 answer payload。"""

    def __init__(
        self,
        retrieval_provider: DocumentRetrievalProvider,
        event_publisher: EventPublisher,
        answer_generator: RAGAnswerGenerator | None = None,
        evaluation_service: InternalRagEvaluationService | None = None,
    ) -> None:
        """注入 retrieval provider 和事件发布器，保持 service 不直连 chunk storage。"""

        self._retrieval_provider = retrieval_provider
        self._event_publisher = event_publisher
        self._answer_generator = answer_generator or RAGAnswerGenerator()
        self._evaluation_service = evaluation_service or InternalRagEvaluationService()
        # internal RAG 的输出必须稳定，所以这里沿用与 retrieval service 一样的进程内互斥锁。
        self._lock = RLock()

    def answer(self, request: InternalRagAnswerRequest) -> InternalRagAnswerResponse:
        """执行检索、引用校验和 deterministic answer assembly。"""

        scope_id = self._scope_id()
        with self._lock:
            self._publish(
                scope_id,
                "internal_rag.started",
                "Internal RAG started",
                status="running",
                extra=self._request_summary(request),
            )

            try:
                question = self._normalize_question(request.question)
                if not question:
                    raise InvalidQuestionException({"field": "question", "reason": "question must not be blank"})
                if not request.require_citations:
                    raise CitationRequiredException({"field": "require_citations", "reason": "citations are mandatory"})

                retrieval_request = DocumentRetrievalSearchRequest(
                    query=question,
                    limit=request.limit,
                    include_archived=request.include_archived,
                    document_type=self._document_type_filter(request.document_type),
                    language=self._language_filter(request.language),
                    tags=request.tags,
                )
                results, total_matches = self._retrieval_provider.search(retrieval_request)
                if not results:
                    raise InsufficientContextException(
                        {
                            "field": "question",
                            "reason": "retrieval returned no usable evidence",
                            "total_matches": total_matches,
                        }
                    )

                generation = self._answer_generator.generate(
                    request=request,
                    question=question,
                    retrieval_results=results,
                    total_matches=total_matches,
                )
                selected_citations = generation.citations
                answer = generation.answer
                evaluation = self._evaluation_service.evaluate(
                    query=question,
                    answer=answer,
                    citations=selected_citations,
                    retrieval_results=results,
                    total_matches=total_matches,
                )
                if request.require_citations and InternalRagWarning.MISSING_CITATION in evaluation.warnings:
                    raise CitationRequiredException(
                        {
                            "field": "citations",
                            "reason": "retrieved evidence did not yield citations",
                        }
                    )
                warnings = list(dict.fromkeys(warning.value for warning in evaluation.warnings))
                confidence = evaluation.confidence
                if not warnings and evaluation.coverage_score < 1.0:
                    warnings.append(InternalRagWarning.LOW_CONTEXT.value)
                response = InternalRagAnswerResponse(
                    answer=answer,
                    citations=selected_citations,
                    retrieval_mode="keyword",
                    answer_mode=request.answer_mode,
                    confidence=confidence,
                    warnings=warnings,
                )
                self._publish(
                    scope_id,
                    "internal_rag.retrieval_completed",
                    "Internal RAG retrieval completed",
                    status="completed",
                    extra={
                        **self._request_summary(request),
                        "total_matches": total_matches,
                        "citation_count": len(selected_citations),
                        "coverage_score": evaluation.coverage_score,
                        "citation_score": evaluation.citation_score,
                        "warnings": warnings,
                        "provider_name": generation.provider_name,
                        "used_llm_provider": generation.used_llm_provider,
                        "fallback_reason": generation.fallback_reason.value,
                        "prompt_tokens": generation.usage.prompt_tokens,
                        "completion_tokens": generation.usage.completion_tokens,
                        "estimated_cost": generation.usage.estimated_cost,
                        "latency_ms": generation.usage.latency_ms,
                    },
                )
                self._publish(
                    scope_id,
                    "internal_rag.answer_generated",
                    "Internal RAG answer generated",
                    status="completed",
                    extra={
                        **self._request_summary(request),
                        "citation_count": len(selected_citations),
                        "confidence": confidence,
                        "coverage_score": evaluation.coverage_score,
                        "citation_score": evaluation.citation_score,
                        "warnings": warnings,
                        "provider_name": generation.provider_name,
                        "used_llm_provider": generation.used_llm_provider,
                        "fallback_reason": generation.fallback_reason.value,
                        "prompt_tokens": generation.usage.prompt_tokens,
                        "completion_tokens": generation.usage.completion_tokens,
                        "estimated_cost": generation.usage.estimated_cost,
                        "latency_ms": generation.usage.latency_ms,
                    },
                )
                return response
            except InvalidQueryException as exc:
                self._publish(
                    scope_id,
                    "internal_rag.failed",
                    "Internal RAG failed",
                    status="failed",
                    error_code=ErrorCode.INVALID_QUESTION.value,
                    extra={
                        "error_code": ErrorCode.INVALID_QUESTION.value,
                        **self._request_summary(request),
                    },
                )
                raise InvalidQuestionException(
                    {
                        "field": "question",
                        "reason": "question must contain searchable terms",
                    }
                ) from exc
            except AppException as exc:
                self._publish(
                    scope_id,
                    "internal_rag.failed",
                    "Internal RAG failed",
                    status="failed",
                    error_code=exc.error_code.value,
                    extra={
                        "error_code": exc.error_code.value,
                        **self._request_summary(request),
                    },
                )
                raise
            except TimeoutError as exc:
                self._publish(
                    scope_id,
                    "internal_rag.failed",
                    "Internal RAG failed",
                    status="failed",
                    error_code=ErrorCode.PROVIDER_TIMEOUT.value,
                    extra={
                        "error_code": ErrorCode.PROVIDER_TIMEOUT.value,
                        **self._request_summary(request),
                    },
                )
                raise AppException(
                    ErrorCode.PROVIDER_TIMEOUT,
                    "Retrieval provider timed out",
                    503,
                    detail=self._request_summary(request),
                ) from exc
            except Exception as exc:  # noqa: BLE001
                self._publish(
                    scope_id,
                    "internal_rag.failed",
                    "Internal RAG failed",
                    status="failed",
                    error_code=ErrorCode.REPOSITORY_ERROR.value,
                    extra={
                        "error_code": ErrorCode.REPOSITORY_ERROR.value,
                        **self._request_summary(request),
                    },
                )
                raise AppException(
                    ErrorCode.REPOSITORY_ERROR,
                    "Internal RAG repository error",
                    500,
                    detail={"request_summary": self._request_summary(request)},
                ) from exc

    def _normalize_question(self, value: str) -> str:
        """把 question 统一成去首尾空白的稳定文本。"""

        return value.strip()

    def _document_type_filter(self, value: DocumentType | None) -> str | None:
        """保留明确信息边界：service 只传字符串给 retrieval request。"""

        return value.value if value is not None else None

    def _language_filter(self, value: Language | None) -> str | None:
        """把领域枚举显式转成检索 request 需要的字符串。"""

        return value.value if value is not None else None

    def _request_summary(self, request: InternalRagAnswerRequest) -> dict[str, object]:
        """把安全的请求摘要写入事件，不暴露 question 原文。"""

        return {
            "question_length": len(request.question.strip()),
            "limit": request.limit,
            "include_archived": request.include_archived,
            "document_type": request.document_type.value if request.document_type else None,
            "language": request.language.value if request.language else None,
            "tags_count": len(request.tags or []),
            "answer_mode": request.answer_mode.value,
            "require_citations": request.require_citations,
            "retrieval_mode": "keyword",
        }

    def _scope_id(self) -> str:
        """用 request_id 形成 internal RAG 事件流的稳定分组键。"""

        request_id = get_request_id()
        return f"internal_rag:{request_id}"

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
        """把 internal RAG 进度写入统一事件仓库和结构化日志。"""

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
            node="internal_rag",
            error_code=error_code,
            sequence=event.sequence,
        )


__all__ = ["InternalRagService"]
