"""统一 LLM Gateway：唯一允许调用 Provider 的组件。

文件职责：根据 operation 解析 policy，在 stub/openrouter/fallback_chain 下调用 Provider。
谁调用它：AIAnalysisService、ExecutiveReportService。
它调用谁：ModelRouter（单 Provider）或 ProviderChain（严格串行 fallback）。
设计理由：业务 Router 与普通 RAG 永远不直接依赖 Provider。
日本现场面试：所有收费 side-effect 都必须经过 Gateway 这一条窄门。
"""

from __future__ import annotations

from collections.abc import Callable
from decimal import Decimal
from typing import Any
from uuid import uuid4

from app.llm.attempt_models import (
    ChainAnalysisOutcome,
    ChainReportOutcome,
    ProviderAttemptSummary,
)
from app.llm.model_router import ModelRouter
from app.llm.operation_policy import OperationPolicy, OperationPolicyRegistry
from app.llm.provider_chain import ChainContext, ProviderChain
from app.models.ai_analysis import (
    LLMAnalysisInput,
    LLMReportInput,
)
from app.providers.llm_provider import LLMProvider


class LLMGatewayService:
    """企业级 LLM 调用窄门；stub / openrouter 兼容 / fallback_chain 统一入口。"""

    def __init__(
        self,
        *,
        policy_registry: OperationPolicyRegistry,
        model_router: ModelRouter | None = None,
        analysis_chain: ProviderChain | None = None,
        report_chain: ProviderChain | None = None,
        mode: str = "stub",
        total_timeout_seconds: float = 120.0,
        max_provider_attempts: int = 4,
        currency: str = "USD",
    ) -> None:
        self._policy_registry = policy_registry
        self._router = model_router
        self._analysis_chain = analysis_chain
        self._report_chain = report_chain
        self._mode = mode
        self._total_timeout_seconds = total_timeout_seconds
        self._max_provider_attempts = max_provider_attempts
        self._currency = currency

    def policy_for(self, operation: str) -> OperationPolicy:
        try:
            return self._policy_registry.get(operation)
        except KeyError as exc:
            raise LookupError(f"unknown operation: {operation}") from exc

    def resolve_provider(self, operation: str) -> LLMProvider:
        """兼容旧调用；fallback_chain 模式返回 Chain 首个 Provider。"""

        if self._mode == "fallback_chain":
            chain = self._analysis_chain if operation == "ai_analysis" else self._report_chain
            if chain is None or not chain._providers:
                raise LookupError("fallback chain is empty")
            return chain._providers[0].provider
        if self._router is None:
            raise LookupError("model router is not configured")
        provider, _, _ = self._router.resolve(operation)
        return provider

    def analyze(
        self,
        *,
        operation: str,
        request: LLMAnalysisInput,
        usage_id: str | None = None,
        idempotency_key: str | None = None,
        estimated_input_tokens: int | None = None,
        can_afford: Callable[[Decimal], bool] | None = None,
        is_cancelled: Callable[[], bool] | None = None,
    ) -> ChainAnalysisOutcome:
        """low_cost 分析入口；返回含 fallback 元数据的可信结果。"""

        if operation != "ai_analysis":
            raise LookupError(f"analyze does not accept operation: {operation}")
        policy = self.policy_for(operation)

        if self._mode == "fallback_chain":
            if self._analysis_chain is None:
                raise RuntimeError("analysis provider chain is not configured")
            context = ChainContext(
                usage_id=usage_id or f"llm-{uuid4().hex}",
                request_id=request.request_id,
                idempotency_key=idempotency_key or request.request_id,
                operation=operation,
                route_tier="low_cost",
                currency=policy.currency,
                total_timeout_seconds=self._total_timeout_seconds,
                max_provider_attempts=self._max_provider_attempts,
                estimated_input_tokens=estimated_input_tokens or max(1, request.max_output_tokens),
                max_output_tokens=policy.max_output_tokens,
                can_afford=can_afford,
                is_cancelled=is_cancelled,
            )
            return self._analysis_chain.analyze(request, context)

        if self._router is None:
            raise RuntimeError("model router is not configured")
        provider, alias, model_name = self._router.resolve(operation)
        result = provider.analyze(request)
        actual_model = result.actual_model or model_name
        summary = ProviderAttemptSummary(
            provider_name=alias,
            model_name=actual_model,
            status="succeeded",
            latency_ms=result.latency_ms,
        )
        return ChainAnalysisOutcome(
            result=result,
            provider_name=alias,
            configured_model=model_name,
            actual_model=actual_model,
            route_tier=policy.route_tier,
            fallback_used=False,
            attempt_count=1,
            attempted_providers=(summary,),
            attempts=(),
            total_input_tokens=result.input_tokens,
            total_output_tokens=result.output_tokens,
            total_tokens=result.input_tokens + result.output_tokens,
            total_actual_cost=Decimal("0"),  # 由 Service 按 policy 价格结算
            currency=policy.currency,
        )

    def generate_report(
        self,
        *,
        operation: str,
        request: LLMReportInput,
        usage_id: str | None = None,
        idempotency_key: str | None = None,
        estimated_input_tokens: int | None = None,
        can_afford: Callable[[Decimal], bool] | None = None,
        is_cancelled: Callable[[], bool] | None = None,
    ) -> ChainReportOutcome:
        """high_quality 报告入口。"""

        if operation != "executive_report":
            raise LookupError(f"generate_report does not accept operation: {operation}")
        policy = self.policy_for(operation)

        if self._mode == "fallback_chain":
            if self._report_chain is None:
                raise RuntimeError("report provider chain is not configured")
            context = ChainContext(
                usage_id=usage_id or f"llm-{uuid4().hex}",
                request_id=request.request_id,
                idempotency_key=idempotency_key or request.request_id,
                operation=operation,
                route_tier="high_quality",
                currency=policy.currency,
                total_timeout_seconds=self._total_timeout_seconds,
                max_provider_attempts=self._max_provider_attempts,
                estimated_input_tokens=estimated_input_tokens or max(1, request.max_output_tokens),
                max_output_tokens=policy.max_output_tokens,
                can_afford=can_afford,
                is_cancelled=is_cancelled,
            )
            return self._report_chain.generate_report(request, context)

        if self._router is None:
            raise RuntimeError("model router is not configured")
        provider, alias, model_name = self._router.resolve(operation)
        generate = getattr(provider, "generate_report", None)
        if generate is None:
            raise RuntimeError("selected provider cannot generate executive reports")
        result = generate(request)
        actual_model = result.actual_model or model_name
        summary = ProviderAttemptSummary(
            provider_name=alias,
            model_name=actual_model,
            status="succeeded",
            latency_ms=result.latency_ms,
        )
        return ChainReportOutcome(
            result=result,
            provider_name=alias,
            configured_model=model_name,
            actual_model=actual_model,
            route_tier=policy.route_tier,
            fallback_used=False,
            attempt_count=1,
            attempted_providers=(summary,),
            attempts=(),
            total_input_tokens=result.input_tokens,
            total_output_tokens=result.output_tokens,
            total_tokens=result.input_tokens + result.output_tokens,
            total_actual_cost=Decimal("0"),
            currency=policy.currency,
        )


__all__ = ["LLMGatewayService"]
