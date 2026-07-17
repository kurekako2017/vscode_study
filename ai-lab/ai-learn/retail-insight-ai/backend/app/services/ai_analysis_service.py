"""PostgreSQL-only 显式 AI Analysis 编排服务。

文件职责：严格执行 confirmation、Evidence Gate、成本上限、quota 预占、Gateway 和结算。
调用关系：Router 传入 JWT CurrentUser；本服务只通过 LLMGatewayService 调用 Provider。
输入输出：输入问题与稳定证据 ID，输出持久化分析结果和 Decimal 成本。
设计理由：预占和结算是两个短事务，Provider 调用不持有数据库锁。
日本现场面试：“贵的 side effect 必须在证据、授权、幂等和预算都通过后才发生”。
"""

from __future__ import annotations

from decimal import Decimal, ROUND_UP
from time import monotonic
from uuid import uuid4

from app.errors.error_codes import ErrorCode
from app.errors.exceptions import AIAnalysisException
from app.llm.attempt_models import (
    ProviderChainCancelledError,
    ProviderChainExhaustedError,
    ProviderChainQuotaStopError,
    outcome_to_safe_dict,
)
from app.llm.gateway import LLMGatewayService
from app.models.ai_analysis import (
    AIEvidence,
    AIAnalysisResult,
    LLMAnalysisInput,
    LLMProviderAuthenticationError,
    LLMProviderCitationInvalidError,
    LLMProviderModelUnavailableError,
    LLMProviderPartialFailureError,
    LLMProviderRateLimitError,
    LLMProviderResponseInvalidError,
    LLMProviderTimeoutError,
    LLMProviderUnavailableError,
    ProviderAttemptPublic,
)
from app.models.document import DocumentStatus
from app.repositories.interfaces.document_chunk_repository import DocumentChunkRepository
from app.repositories.interfaces.document_repository import DocumentRepository
from app.repositories.postgres.llm_usage_repository import PostgresLLMUsageRepository
from app.repositories.interfaces.unit_of_work import UnitOfWork
from app.schemas.ai_analysis_api import AIAnalysisRequest
from app.security.contracts import CurrentUser
from app.services.persistent_audit_service import PersistentAuditContext, PersistentAuditService

_MILLION = Decimal(1_000_000)
_COST_QUANTUM = Decimal("0.00000001")
_OPERATION = "ai_analysis"


class AIAnalysisService:
    def __init__(
        self, *, gateway: LLMGatewayService,
        usage_repository: PostgresLLMUsageRepository | None,
        document_repository: DocumentRepository,
        chunk_repository: DocumentChunkRepository,
        persistent_audit_service: PersistentAuditService,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._gateway = gateway
        self._usage = usage_repository
        self._documents = document_repository
        self._chunks = chunk_repository
        self._audit = persistent_audit_service
        self._uow = unit_of_work

    def execute(
        self, request: AIAnalysisRequest, *, actor: CurrentUser,
        idempotency_key: str, context: PersistentAuditContext,
    ) -> AIAnalysisResult:
        if self._usage is None:
            raise AIAnalysisException(
                ErrorCode.AI_ANALYSIS_REQUIRES_POSTGRES, "AI analysis requires PostgreSQL", 503,
            )
        try:
            policy = self._gateway.policy_for(_OPERATION)
        except LookupError as exc:
            raise AIAnalysisException(ErrorCode.VALIDATION_ERROR, "Unknown LLM operation", 422) from exc
        if not request.confirmed:
            raise AIAnalysisException(
                ErrorCode.AI_ANALYSIS_CONFIRMATION_REQUIRED, "Explicit confirmation is required", 422,
            )
        evidence = self._load_evidence(request, policy.evidence_max_count, policy.evidence_max_chars, policy.max_input_tokens)
        estimated_input = self._estimate_tokens(request.question, evidence)
        if estimated_input > policy.max_input_tokens:
            raise AIAnalysisException(
                ErrorCode.LLM_REQUEST_COST_EXCEEDED, "AI analysis input exceeds the per-request token cap", 422,
                {"max_input_tokens": policy.max_input_tokens},
            )
        estimated_cost = self._cost(estimated_input, policy.max_output_tokens, policy)
        if estimated_cost > policy.request_max_cost:
            raise AIAnalysisException(
                ErrorCode.LLM_REQUEST_COST_EXCEEDED, "AI analysis exceeds the per-request cost cap", 422,
                {"max_cost": str(policy.request_max_cost), "currency": policy.currency},
            )

        with self._uow.transaction():
            outcome = self._usage.reserve(
                request_id=context.request_id, idempotency_key=idempotency_key, actor=actor,
                policy=policy, input_tokens=estimated_input, output_tokens=policy.max_output_tokens,
                estimated_cost=estimated_cost, evidence=evidence, task_id=request.task_id,
            )
            if outcome.kind == "rejected":
                self._audit.record_ai_analysis_event(
                    context=context, actor=actor, action="analysis.execute.quota_rejected",
                    result="failure", status_code=429, error_code="llm_quota_exceeded",
                    usage_id=outcome.usage_id, operation=_OPERATION, route_tier=policy.route_tier,
                )
        if outcome.kind == "succeeded" and isinstance(outcome.existing_result, AIAnalysisResult):
            return outcome.existing_result
        if outcome.kind == "reserved":
            return self._invoke_and_settle(
                outcome.usage_id, request, evidence, actor, context, policy,
                idempotency_key, estimated_input, estimated_cost,
            )
        if outcome.kind == "rejected":
            raise AIAnalysisException(
                ErrorCode.LLM_QUOTA_EXCEEDED, "Daily LLM quota exceeded", 429,
                {"scope": outcome.rejection_code},
            )
        raise AIAnalysisException(
            ErrorCode.AI_ANALYSIS_IN_PROGRESS,
            "This AI analysis idempotency key is already final or in progress", 409,
            {"status": outcome.kind},
        )

    def _invoke_and_settle(
        self, usage_id: str, request: AIAnalysisRequest, evidence: tuple[AIEvidence, ...],
        actor: CurrentUser, context: PersistentAuditContext, policy,
        idempotency_key: str, estimated_input: int, estimated_cost: Decimal,
    ) -> AIAnalysisResult:
        started = monotonic()
        spent_holder = {"cost": Decimal("0")}

        def can_afford(attempt_cost: Decimal) -> bool:
            # 进入下一个 Provider 前：累计 attempt 费用 + 本 attempt 预估不得超过 request_max 与剩余预占。
            projected = spent_holder["cost"] + attempt_cost
            if projected > policy.request_max_cost:
                return False
            if self._usage is None:
                return True
            return self._usage.can_afford_additional(
                actor_user_id=actor.user_id,
                route_tier=policy.route_tier,
                additional_cost=attempt_cost,
                additional_tokens=estimated_input + policy.max_output_tokens,
                policy=policy,
            )

        try:
            chain_outcome = self._gateway.analyze(
                operation=_OPERATION,
                request=LLMAnalysisInput(
                    question=request.question, evidence=evidence,
                    max_output_tokens=policy.max_output_tokens,
                    request_id=context.request_id,
                    timeout_seconds=policy.timeout_seconds,
                ),
                usage_id=usage_id,
                idempotency_key=idempotency_key,
                estimated_input_tokens=estimated_input,
                can_afford=can_afford,
            )
        except ProviderChainQuotaStopError as exc:
            return self._fail_chain(
                usage_id, actor, context, "llm_quota_exceeded", 429,
                ErrorCode.LLM_QUOTA_EXCEEDED, started, policy, exc.failure,
            )
        except ProviderChainCancelledError as exc:
            return self._fail_chain(
                usage_id, actor, context, "provider_chain_cancelled", 499,
                ErrorCode.PROVIDER_FAILED, started, policy, exc.failure,
            )
        except ProviderChainExhaustedError as exc:
            status_code, public = self._map_chain_error(exc.failure.error_category)
            return self._fail_chain(
                usage_id, actor, context, exc.failure.error_code, status_code,
                public, started, policy, exc.failure,
            )
        except LLMProviderPartialFailureError as exc:
            return self._fail(
                usage_id, actor, context, "provider_partial_failure", 502,
                ErrorCode.PROVIDER_FAILED, started, policy,
                input_tokens=exc.input_tokens, output_tokens=exc.output_tokens, latency_ms=exc.latency_ms,
            )
        except LLMProviderTimeoutError:
            return self._fail(usage_id, actor, context, "provider_timeout", 504, ErrorCode.PROVIDER_TIMEOUT, started, policy)
        except LLMProviderRateLimitError:
            return self._fail(usage_id, actor, context, "provider_rate_limited", 429, ErrorCode.PROVIDER_RATE_LIMITED, started, policy)
        except LLMProviderAuthenticationError:
            return self._fail(
                usage_id, actor, context, "provider_authentication_failed", 502,
                ErrorCode.PROVIDER_AUTHENTICATION_FAILED, started, policy,
            )
        except LLMProviderModelUnavailableError:
            return self._fail(
                usage_id, actor, context, "provider_model_unavailable", 502,
                ErrorCode.PROVIDER_MODEL_UNAVAILABLE, started, policy,
            )
        except LLMProviderUnavailableError:
            return self._fail(
                usage_id, actor, context, "provider_unavailable", 502,
                ErrorCode.PROVIDER_UNAVAILABLE, started, policy,
            )
        except LLMProviderResponseInvalidError:
            return self._fail(
                usage_id, actor, context, "provider_response_invalid", 502,
                ErrorCode.PROVIDER_RESPONSE_INVALID, started, policy,
            )
        except LLMProviderCitationInvalidError:
            return self._fail(
                usage_id, actor, context, "provider_citation_invalid", 502,
                ErrorCode.PROVIDER_CITATION_INVALID, started, policy,
            )
        except Exception:
            return self._fail(
                usage_id, actor, context, "provider_failed", 502, ErrorCode.PROVIDER_FAILED,
                started, policy,
            )

        provider_result = chain_outcome.result
        # stub/openrouter：按 policy 价格；fallback_chain：使用 chain 汇总的 actual_cost（含失败 attempt）
        if chain_outcome.attempts:
            actual_cost = chain_outcome.total_actual_cost
            input_tokens = chain_outcome.total_input_tokens
            output_tokens = chain_outcome.total_output_tokens
        else:
            input_tokens = provider_result.input_tokens
            output_tokens = provider_result.output_tokens
            actual_cost = self._cost(input_tokens, output_tokens, policy)

        public_attempts = tuple(
            ProviderAttemptPublic(
                provider_name=item.provider_name,
                model_name=item.model_name,
                status=item.status,
                latency_ms=item.latency_ms,
            )
            for item in chain_outcome.attempted_providers
        )
        analysis_id = f"ana-{uuid4().hex}"
        with self._uow.transaction():
            result = self._usage.settle_analysis_success(
                usage_id=usage_id, analysis_id=analysis_id, answer=provider_result.answer,
                evidence=evidence, input_tokens=input_tokens,
                output_tokens=output_tokens, actual_cost=actual_cost,
                latency_ms=provider_result.latency_ms, provider_request_id=provider_result.provider_request_id,
                finish_reason=provider_result.finish_reason,
                usage_source=provider_result.usage_source,
                actual_model=chain_outcome.actual_model,
                selected_provider=chain_outcome.provider_name,
                fallback_used=chain_outcome.fallback_used,
                attempt_count=chain_outcome.attempt_count,
                attempted_providers=[
                    {
                        "provider_name": a.provider_name,
                        "model_name": a.model_name,
                        "status": a.status,
                        "latency_ms": a.latency_ms,
                    }
                    for a in public_attempts
                ],
            )
            # 附加 fallback 元数据到返回对象
            result = AIAnalysisResult(
                analysis_id=result.analysis_id,
                answer=result.answer,
                citations=result.citations,
                provider_name=chain_outcome.provider_name,
                model_name=chain_outcome.actual_model,
                input_tokens=result.input_tokens,
                output_tokens=result.output_tokens,
                total_tokens=result.total_tokens,
                actual_cost=result.actual_cost,
                currency=result.currency,
                status=result.status,
                created_at=result.created_at,
                route_tier=result.route_tier,
                estimated_cost=result.estimated_cost,
                actor_user_id=result.actor_user_id,
                task_id=result.task_id,
                usage_id=usage_id,
                fallback_used=chain_outcome.fallback_used,
                attempt_count=chain_outcome.attempt_count,
                attempted_providers=public_attempts,
            )
            audit_meta = outcome_to_safe_dict(chain_outcome)
            # audit_meta 已含 route_tier/selected_*，避免与显式 kwargs 重复传参。
            self._audit.record_ai_analysis_event(
                context=context, actor=actor, action="analysis.execute.succeeded",
                result="success", status_code=200, usage_id=usage_id,
                analysis_id=analysis_id, token_count=result.total_tokens,
                cost=str(result.actual_cost), currency=result.currency,
                operation=_OPERATION,
                provider=result.provider_name, model=result.model_name,
                **audit_meta,
            )
        return result

    def _fail_chain(
        self, usage_id: str, actor: CurrentUser, context: PersistentAuditContext,
        error_code: str, status_code: int, public_code: ErrorCode, started: float, policy,
        failure,
    ):
        assert self._usage is not None
        latency = max(0, int((monotonic() - started) * 1000))
        with self._uow.transaction():
            self._usage.settle_failure(
                usage_id=usage_id, error_code=error_code, latency_ms=latency,
                input_tokens=failure.total_input_tokens,
                output_tokens=failure.total_output_tokens,
                actual_cost=failure.total_actual_cost,
                fallback_used=failure.attempt_count > 1,
                attempt_count=failure.attempt_count,
                attempted_providers=[
                    {
                        "provider_name": a.provider_name,
                        "model_name": a.model_name,
                        "status": a.status,
                        "latency_ms": a.latency_ms,
                    }
                    for a in failure.attempted_providers
                ],
            )
            self._audit.record_ai_analysis_event(
                context=context, actor=actor, action="analysis.execute.failed",
                result="failure", status_code=status_code, error_code=error_code,
                usage_id=usage_id, operation=_OPERATION, route_tier=policy.route_tier,
                **{
                    key: value
                    for key, value in outcome_to_safe_dict(failure).items()
                    if key not in {"route_tier", "operation"}
                },
            )
        raise AIAnalysisException(public_code, "AI analysis provider failed", status_code)

    def _fail(
        self, usage_id: str, actor: CurrentUser, context: PersistentAuditContext,
        error_code: str, status_code: int, public_code: ErrorCode, started: float, policy,
        input_tokens: int = 0, output_tokens: int = 0, latency_ms: int | None = None,
    ):
        assert self._usage is not None
        latency = latency_ms if latency_ms is not None else max(0, int((monotonic() - started) * 1000))
        actual_cost = self._cost(input_tokens, output_tokens, policy) if input_tokens or output_tokens else Decimal("0")
        with self._uow.transaction():
            self._usage.settle_failure(
                usage_id=usage_id, error_code=error_code, latency_ms=latency,
                input_tokens=input_tokens, output_tokens=output_tokens, actual_cost=actual_cost,
            )
            self._audit.record_ai_analysis_event(
                context=context, actor=actor, action="analysis.execute.failed",
                result="failure", status_code=status_code, error_code=error_code,
                usage_id=usage_id, operation=_OPERATION, route_tier=policy.route_tier,
            )
        raise AIAnalysisException(public_code, "AI analysis provider failed", status_code)

    def _map_chain_error(self, category: str) -> tuple[int, ErrorCode]:
        mapping = {
            "timeout": (504, ErrorCode.PROVIDER_TIMEOUT),
            "rate_limited": (429, ErrorCode.PROVIDER_RATE_LIMITED),
            "authentication": (502, ErrorCode.PROVIDER_AUTHENTICATION_FAILED),
            "configuration_error": (502, ErrorCode.PROVIDER_AUTHENTICATION_FAILED),
            "model_unavailable": (502, ErrorCode.PROVIDER_MODEL_UNAVAILABLE),
            "unavailable": (502, ErrorCode.PROVIDER_UNAVAILABLE),
            "connection_failure": (502, ErrorCode.PROVIDER_UNAVAILABLE),
            "citation_invalid": (502, ErrorCode.PROVIDER_CITATION_INVALID),
            "response_invalid": (502, ErrorCode.PROVIDER_RESPONSE_INVALID),
            "partial_failure": (502, ErrorCode.PROVIDER_FAILED),
        }
        return mapping.get(category, (502, ErrorCode.PROVIDER_FAILED))

    def _load_evidence(
        self, request: AIAnalysisRequest, max_count: int, max_chars: int, max_input_tokens: int,
    ) -> tuple[AIEvidence, ...]:
        unique = {(item.document_id, item.chunk_id): item for item in request.evidence}
        ordered = sorted(unique.values(), key=lambda item: (-item.score, item.document_id, item.chunk_id))[:max_count]
        remaining = min(max_chars, max_input_tokens * 4 - len(request.question))
        selected: list[AIEvidence] = []
        chunks_by_document: dict[str, dict[str, object]] = {}
        for ref in ordered:
            document = self._documents.get(ref.document_id)
            if document is None or document.metadata.status is DocumentStatus.ARCHIVED:
                raise AIAnalysisException(
                    ErrorCode.EVIDENCE_INVALID, "Evidence is unavailable", 422,
                    {"document_id": ref.document_id},
                )
            if ref.document_id not in chunks_by_document:
                chunks_by_document[ref.document_id] = {
                    chunk.chunk_id: chunk
                    for chunk in self._chunks.list_for_document(ref.document_id, document.metadata.version)
                }
            chunk = chunks_by_document[ref.document_id].get(ref.chunk_id)
            if chunk is None:
                raise AIAnalysisException(
                    ErrorCode.EVIDENCE_INVALID, "Evidence chunk is unavailable", 422,
                    {"document_id": ref.document_id, "chunk_id": ref.chunk_id},
                )
            excerpt = str(getattr(chunk, "content"))[:remaining]
            if not excerpt:
                break
            selected.append(AIEvidence(ref.document_id, ref.chunk_id, ref.score, excerpt))
            remaining -= len(excerpt)
            if remaining <= 0:
                break
        if not selected:
            raise AIAnalysisException(
                ErrorCode.INSUFFICIENT_CONTEXT, "At least one accessible evidence chunk is required", 422,
            )
        return tuple(selected)

    def _estimate_tokens(self, question: str, evidence: tuple[AIEvidence, ...]) -> int:
        return max(1, (len(question) + sum(len(item.excerpt) for item in evidence) + 3) // 4)

    def _cost(self, input_tokens: int, output_tokens: int, policy) -> Decimal:
        value = (
            Decimal(input_tokens) * policy.input_price_per_million
            + Decimal(output_tokens) * policy.output_price_per_million
        ) / _MILLION
        return value.quantize(_COST_QUANTUM, rounding=ROUND_UP)


__all__ = ["AIAnalysisService"]
