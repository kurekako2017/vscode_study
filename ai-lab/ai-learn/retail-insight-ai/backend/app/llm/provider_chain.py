"""严格串行 Provider Fallback Chain。

文件职责：
- 固定顺序调用 OpenRouter → NVIDIA → Gemini → Local Qwen。
- 成功立即停止；eligible failure 才 fallback；业务错误不进入 Chain。
- 每次 attempt 独立账本字段；Circuit open 跳过不记收费 attempt。

谁调用它：LLMGatewayService（fallback_chain 模式）。
它调用谁：具体 LLMProvider、CircuitBreaker、可选 AttemptWriter。
禁止：并行竞速、客户端选 Provider、无限重试。
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, ROUND_UP
from time import monotonic
from typing import Protocol
from uuid import uuid4

from app.llm.attempt_models import (
    ChainAnalysisOutcome,
    ChainFailure,
    ChainReportOutcome,
    ProviderAttemptRecord,
    ProviderAttemptSummary,
    ProviderChainCancelledError,
    ProviderChainExhaustedError,
    ProviderChainQuotaStopError,
)
from app.llm.circuit_breaker import CircuitBreaker
from app.llm.provider_registry import ProviderEndpointConfig, RouteTier
from app.models.ai_analysis import (
    LLMAnalysisInput,
    LLMProviderAuthenticationError,
    LLMProviderCitationInvalidError,
    LLMProviderModelUnavailableError,
    LLMProviderPartialFailureError,
    LLMProviderRateLimitError,
    LLMProviderResponseInvalidError,
    LLMProviderResult,
    LLMProviderTimeoutError,
    LLMProviderUnavailableError,
    LLMReportInput,
    LLMReportResult,
)
from app.providers.llm_provider import LLMProvider

_MILLION = Decimal(1_000_000)
_COST_QUANTUM = Decimal("0.00000001")

# 允许进入下一个 Provider 的错误类别
_FALLBACK_ELIGIBLE = frozenset(
    {
        "timeout",
        "rate_limited",
        "unavailable",
        "authentication",
        "configuration_error",
        "model_unavailable",
        "connection_failure",
        "partial_failure",
    }
)

# 不允许 fallback（应在调用 Provider 前结束；若误入 Chain 则立即终止）
_NON_FALLBACK = frozenset(
    {
        "citation_invalid",
        "response_invalid",
        "cancelled",
    }
)


class AttemptWriter(Protocol):
    def append_attempt(self, record: ProviderAttemptRecord) -> None: ...

    def complete_attempt(self, record: ProviderAttemptRecord) -> None: ...


class NullAttemptWriter:
    def append_attempt(self, record: ProviderAttemptRecord) -> None:
        return None

    def complete_attempt(self, record: ProviderAttemptRecord) -> None:
        return None


@dataclass(frozen=True)
class BoundProvider:
    """Chain 中已绑定 route_tier 模型的 Provider 实例。"""

    endpoint: ProviderEndpointConfig
    provider: LLMProvider
    configured_model: str
    route_tier: RouteTier


@dataclass(frozen=True)
class ChainContext:
    usage_id: str
    request_id: str
    idempotency_key: str
    operation: str
    route_tier: RouteTier
    currency: str
    total_timeout_seconds: float
    max_provider_attempts: int
    estimated_input_tokens: int
    max_output_tokens: int
    # 已累计实际费用（来自先前 attempt）；进入下一次前检查额度
    spent_cost: Decimal = Decimal("0")
    # 回调：给定 attempt 预估成本，返回是否允许继续
    can_afford: Callable[[Decimal], bool] | None = None
    is_cancelled: Callable[[], bool] | None = None


class ProviderChain:
    """严格串行 fallback；未知 Provider fail-closed。"""

    def __init__(
        self,
        *,
        providers: list[BoundProvider],
        circuit_breaker: CircuitBreaker | None = None,
        attempt_writer: AttemptWriter | None = None,
    ) -> None:
        if not providers:
            raise ValueError("provider chain requires at least one provider")
        # 校验固定顺序：索引必须非递减出现在 FIXED 顺序中
        names = [item.endpoint.name for item in providers]
        order_index = {"openrouter": 0, "nvidia": 1, "gemini": 2, "local_qwen": 3}
        last = -1
        for name in names:
            if name not in order_index:
                raise ValueError(f"unknown provider in chain: {name}")
            idx = order_index[name]
            if idx <= last:
                raise ValueError("provider chain order must remain OpenRouter→NVIDIA→Gemini→Local Qwen")
            last = idx
        self._providers = providers
        self._circuit = circuit_breaker
        self._writer = attempt_writer or NullAttemptWriter()

    def analyze(self, request: LLMAnalysisInput, context: ChainContext) -> ChainAnalysisOutcome:
        def invoke(bound: BoundProvider, timeout: float) -> LLMProviderResult:
            adjusted = LLMAnalysisInput(
                question=request.question,
                evidence=request.evidence,
                max_output_tokens=request.max_output_tokens,
                request_id=request.request_id,
                timeout_seconds=timeout,
            )
            return bound.provider.analyze(adjusted)

        return self._run(context=context, invoke=invoke, kind="analyze")  # type: ignore[return-value]

    def generate_report(self, request: LLMReportInput, context: ChainContext) -> ChainReportOutcome:
        def invoke(bound: BoundProvider, timeout: float) -> LLMReportResult:
            adjusted = LLMReportInput(
                title=request.title,
                analysis_answer=request.analysis_answer,
                evidence=request.evidence,
                max_output_tokens=request.max_output_tokens,
                request_id=request.request_id,
                timeout_seconds=timeout,
            )
            generate = getattr(bound.provider, "generate_report", None)
            if generate is None:
                raise LLMProviderUnavailableError("provider cannot generate reports")
            return generate(adjusted)

        return self._run(context=context, invoke=invoke, kind="report")  # type: ignore[return-value]

    def _run(
        self,
        *,
        context: ChainContext,
        invoke: Callable[[BoundProvider, float], LLMProviderResult | LLMReportResult],
        kind: str,
    ) -> ChainAnalysisOutcome | ChainReportOutcome:
        chain_started = monotonic()
        attempts: list[ProviderAttemptRecord] = []
        summaries: list[ProviderAttemptSummary] = []
        total_input = 0
        total_output = 0
        total_cost = Decimal("0")
        last_error_category = "unavailable"
        last_error_code = "provider_chain_exhausted"
        attempt_number = 0

        for bound in self._providers:
            if context.is_cancelled is not None and context.is_cancelled():
                failure = self._failure(
                    "cancelled",
                    "provider_chain_cancelled",
                    attempts,
                    summaries,
                    total_input,
                    total_output,
                    total_cost,
                    context.currency,
                    charge_possible=total_cost > 0,
                )
                raise ProviderChainCancelledError(failure)

            elapsed = monotonic() - chain_started
            remaining_total = context.total_timeout_seconds - elapsed
            if remaining_total <= 0:
                last_error_category = "timeout"
                last_error_code = "llm_total_timeout"
                break
            if attempt_number >= context.max_provider_attempts:
                last_error_category = "unavailable"
                last_error_code = "llm_max_provider_attempts"
                break

            # Circuit open：跳过，不记收费 attempt
            if self._circuit is not None:
                allowed, reason = self._circuit.allow_request(bound.endpoint.name)
                if not allowed:
                    summaries.append(
                        ProviderAttemptSummary(
                            provider_name=bound.endpoint.name,
                            model_name=bound.configured_model,
                            status="skipped_circuit_open",
                            latency_ms=None,
                        )
                    )
                    continue
                if reason == "half_open_probe":
                    self._circuit.mark_probe_started(bound.endpoint.name)

            estimated_cost = self._estimate_cost(
                bound,
                context.route_tier,
                context.estimated_input_tokens,
                context.max_output_tokens,
            )
            if context.can_afford is not None and not context.can_afford(estimated_cost):
                failure = self._failure(
                    "quota",
                    "llm_quota_insufficient_for_fallback",
                    attempts,
                    summaries,
                    total_input,
                    total_output,
                    total_cost,
                    context.currency,
                    charge_possible=total_cost > 0,
                )
                raise ProviderChainQuotaStopError(failure)

            attempt_number += 1
            timeout = min(bound.endpoint.attempt_timeout_seconds, remaining_total)
            attempt = ProviderAttemptRecord(
                attempt_id=f"att-{uuid4().hex}",
                usage_id=context.usage_id,
                request_id=context.request_id,
                idempotency_key=context.idempotency_key,
                attempt_number=attempt_number,
                operation=context.operation,
                route_tier=context.route_tier,
                provider_name=bound.endpoint.name,
                configured_model=bound.configured_model,
                timeout_seconds=timeout,
                input_unit_price=bound.endpoint.input_price_for(context.route_tier),
                output_unit_price=bound.endpoint.output_price_for(context.route_tier),
                estimated_cost=estimated_cost,
                currency=context.currency,
                started_at=datetime.now(timezone.utc),
                status="started",
            )
            self._writer.append_attempt(attempt)
            started = monotonic()
            try:
                result = invoke(bound, timeout)
            except Exception as exc:
                latency_ms = max(1, int((monotonic() - started) * 1000))
                category, code, status, charge_possible, in_tok, out_tok = self._classify(exc)
                actual_cost = Decimal("0")
                if charge_possible and (in_tok or out_tok):
                    actual_cost = self._cost(bound, context.route_tier, in_tok, out_tok)
                elif category == "timeout":
                    # timeout 无法确定是否收费：charge_possible + 安全估算
                    charge_possible = True
                    actual_cost = estimated_cost
                    in_tok = context.estimated_input_tokens
                    out_tok = 0
                attempt.status = status  # type: ignore[assignment]
                attempt.completed_at = datetime.now(timezone.utc)
                attempt.latency_ms = latency_ms
                attempt.input_tokens = in_tok
                attempt.output_tokens = out_tok
                attempt.total_tokens = in_tok + out_tok
                attempt.actual_cost = actual_cost
                attempt.error_category = category
                attempt.error_code = code
                attempt.fallback_reason = category
                attempt.response_received = category not in {"timeout", "connection_failure", "cancelled"}
                attempt.charge_possible = charge_possible
                if isinstance(exc, LLMProviderPartialFailureError):
                    attempt.usage_source = "provider_reported"
                self._writer.complete_attempt(attempt)
                attempts.append(attempt)
                summaries.append(attempt.safe_summary())
                total_input += in_tok
                total_output += out_tok
                total_cost += actual_cost
                last_error_category = category
                last_error_code = code
                if self._circuit is not None and category in _FALLBACK_ELIGIBLE:
                    self._circuit.record_failure(bound.endpoint.name)
                if category in _NON_FALLBACK:
                    failure = self._failure(
                        category,
                        code,
                        attempts,
                        summaries,
                        total_input,
                        total_output,
                        total_cost,
                        context.currency,
                        charge_possible=total_cost > 0,
                    )
                    raise ProviderChainExhaustedError(failure)
                # eligible → 继续下一个 Provider
                continue

            # 成功
            latency_ms = max(1, int((monotonic() - started) * 1000))
            if isinstance(result, LLMProviderResult):
                in_tok = result.input_tokens
                out_tok = result.output_tokens
                actual_model = result.actual_model or bound.configured_model
                model_mismatch = bool(result.actual_model and result.actual_model != bound.configured_model)
                usage_source = result.usage_source
                provider_request_id = result.provider_request_id
            else:
                in_tok = result.input_tokens
                out_tok = result.output_tokens
                actual_model = result.actual_model or bound.configured_model
                model_mismatch = bool(result.actual_model and result.actual_model != bound.configured_model)
                usage_source = result.usage_source
                provider_request_id = result.provider_request_id

            actual_cost = self._cost(bound, context.route_tier, in_tok, out_tok)
            attempt.status = "succeeded"
            attempt.completed_at = datetime.now(timezone.utc)
            attempt.latency_ms = latency_ms
            attempt.input_tokens = in_tok
            attempt.output_tokens = out_tok
            attempt.total_tokens = in_tok + out_tok
            attempt.actual_cost = actual_cost
            attempt.actual_model = actual_model
            attempt.usage_source = usage_source
            attempt.provider_request_id = provider_request_id
            attempt.response_received = True
            attempt.charge_possible = True
            attempt.model_mismatch = model_mismatch
            self._writer.complete_attempt(attempt)
            attempts.append(attempt)
            summaries.append(attempt.safe_summary())
            total_input += in_tok
            total_output += out_tok
            total_cost += actual_cost
            if self._circuit is not None:
                self._circuit.record_success(bound.endpoint.name)

            fallback_used = attempt_number > 1 or any(
                s.status not in {"succeeded"} for s in summaries[:-1]
            )
            # 若前面有 skipped_circuit_open 也算 fallback 路径
            if any(s.status == "skipped_circuit_open" for s in summaries):
                fallback_used = True

            if kind == "analyze":
                assert isinstance(result, LLMProviderResult)
                return ChainAnalysisOutcome(
                    result=result,
                    provider_name=bound.endpoint.name,
                    configured_model=bound.configured_model,
                    actual_model=actual_model,
                    route_tier=context.route_tier,
                    fallback_used=fallback_used,
                    attempt_count=len(attempts),
                    attempted_providers=tuple(summaries),
                    attempts=tuple(attempts),
                    total_input_tokens=total_input,
                    total_output_tokens=total_output,
                    total_tokens=total_input + total_output,
                    total_actual_cost=total_cost,
                    currency=context.currency,
                )
            assert isinstance(result, LLMReportResult)
            return ChainReportOutcome(
                result=result,
                provider_name=bound.endpoint.name,
                configured_model=bound.configured_model,
                actual_model=actual_model,
                route_tier=context.route_tier,
                fallback_used=fallback_used,
                attempt_count=len(attempts),
                attempted_providers=tuple(summaries),
                attempts=tuple(attempts),
                total_input_tokens=total_input,
                total_output_tokens=total_output,
                total_tokens=total_input + total_output,
                total_actual_cost=total_cost,
                currency=context.currency,
            )

        failure = self._failure(
            last_error_category,
            last_error_code,
            attempts,
            summaries,
            total_input,
            total_output,
            total_cost,
            context.currency,
            charge_possible=total_cost > 0,
        )
        raise ProviderChainExhaustedError(failure)

    def _classify(
        self, exc: Exception
    ) -> tuple[str, str, str, bool, int, int]:
        if isinstance(exc, LLMProviderTimeoutError):
            return "timeout", "provider_timeout", "timed_out", True, 0, 0
        if isinstance(exc, LLMProviderRateLimitError):
            return "rate_limited", "provider_rate_limited", "rate_limited", False, 0, 0
        if isinstance(exc, LLMProviderAuthenticationError):
            return "authentication", "provider_authentication_failed", "configuration_error", False, 0, 0
        if isinstance(exc, LLMProviderModelUnavailableError):
            return "model_unavailable", "provider_model_unavailable", "configuration_error", False, 0, 0
        if isinstance(exc, LLMProviderUnavailableError):
            return "unavailable", "provider_unavailable", "unavailable", False, 0, 0
        if isinstance(exc, LLMProviderPartialFailureError):
            return (
                "partial_failure",
                "provider_partial_failure",
                "failed",
                True,
                exc.input_tokens,
                exc.output_tokens,
            )
        if isinstance(exc, LLMProviderCitationInvalidError):
            return "citation_invalid", "provider_citation_invalid", "failed", False, 0, 0
        if isinstance(exc, LLMProviderResponseInvalidError):
            return "response_invalid", "provider_response_invalid", "failed", False, 0, 0
        # 连接层 / 未知：按不可用处理并允许 fallback
        return "connection_failure", "provider_unavailable", "unavailable", False, 0, 0

    def _estimate_cost(
        self,
        bound: BoundProvider,
        route_tier: RouteTier,
        input_tokens: int,
        output_tokens: int,
    ) -> Decimal:
        return self._cost(bound, route_tier, input_tokens, output_tokens)

    def _cost(
        self,
        bound: BoundProvider,
        route_tier: RouteTier,
        input_tokens: int,
        output_tokens: int,
    ) -> Decimal:
        value = (
            Decimal(input_tokens) * bound.endpoint.input_price_for(route_tier)
            + Decimal(output_tokens) * bound.endpoint.output_price_for(route_tier)
        ) / _MILLION
        return value.quantize(_COST_QUANTUM, rounding=ROUND_UP)

    def _failure(
        self,
        category: str,
        code: str,
        attempts: list[ProviderAttemptRecord],
        summaries: list[ProviderAttemptSummary],
        total_input: int,
        total_output: int,
        total_cost: Decimal,
        currency: str,
        *,
        charge_possible: bool,
    ) -> ChainFailure:
        return ChainFailure(
            error_category=category,
            error_code=code,
            public_message="All providers in the fallback chain failed",
            attempt_count=len(attempts),
            attempted_providers=tuple(summaries),
            attempts=tuple(attempts),
            total_input_tokens=total_input,
            total_output_tokens=total_output,
            total_actual_cost=total_cost,
            currency=currency,
            charge_possible=charge_possible,
        )


__all__ = [
    "BoundProvider",
    "ChainContext",
    "NullAttemptWriter",
    "ProviderChain",
]
