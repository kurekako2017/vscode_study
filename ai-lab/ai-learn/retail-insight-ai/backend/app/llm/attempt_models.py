"""Provider Attempt 领域模型与 Chain 执行结果。

文件职责：表达每次 Provider 尝试与最终 Gateway 汇总结果。
谁调用它：ProviderChain、Gateway、Usage Repository、API 层。
设计理由：业务 Usage Ledger 一行对应整次请求；Attempt 独立 append-only。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any, Literal

from app.models.ai_analysis import LLMProviderResult, LLMReportResult

AttemptStatus = Literal[
    "started",
    "succeeded",
    "failed",
    "timed_out",
    "rate_limited",
    "unavailable",
    "configuration_error",
    "cancelled",
    "skipped_circuit_open",
]


@dataclass(frozen=True)
class ProviderAttemptSummary:
    """前端与 API 可见的安全摘要；禁止 Base URL / Key / 原始错误。"""

    provider_name: str
    model_name: str
    status: str
    latency_ms: int | None = None


@dataclass
class ProviderAttemptRecord:
    """单次 attempt 的完整账本字段（不含 Prompt/正文/Key）。"""

    attempt_id: str
    usage_id: str
    request_id: str
    idempotency_key: str
    attempt_number: int
    operation: str
    route_tier: str
    provider_name: str
    configured_model: str
    actual_model: str | None = None
    status: AttemptStatus = "started"
    started_at: datetime | None = None
    completed_at: datetime | None = None
    timeout_seconds: float = 0.0
    latency_ms: int | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    usage_source: str | None = None
    input_unit_price: Decimal = Decimal("0")
    output_unit_price: Decimal = Decimal("0")
    estimated_cost: Decimal = Decimal("0")
    actual_cost: Decimal = Decimal("0")
    currency: str = "USD"
    provider_request_id: str | None = None
    error_category: str | None = None
    error_code: str | None = None
    fallback_reason: str | None = None
    response_received: bool = False
    charge_possible: bool = False
    model_mismatch: bool = False

    def safe_summary(self) -> ProviderAttemptSummary:
        return ProviderAttemptSummary(
            provider_name=self.provider_name,
            model_name=self.actual_model or self.configured_model,
            status=self.status,
            latency_ms=self.latency_ms,
        )


@dataclass(frozen=True)
class ChainAnalysisOutcome:
    """Gateway analyze 的最终结果：成功答案 + 多 attempt 汇总。"""

    result: LLMProviderResult
    provider_name: str
    configured_model: str
    actual_model: str
    route_tier: str
    fallback_used: bool
    attempt_count: int
    attempted_providers: tuple[ProviderAttemptSummary, ...]
    attempts: tuple[ProviderAttemptRecord, ...] = field(default_factory=tuple)
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_tokens: int = 0
    total_actual_cost: Decimal = Decimal("0")
    currency: str = "USD"


@dataclass(frozen=True)
class ChainReportOutcome:
    """Gateway generate_report 的最终结果。"""

    result: LLMReportResult
    provider_name: str
    configured_model: str
    actual_model: str
    route_tier: str
    fallback_used: bool
    attempt_count: int
    attempted_providers: tuple[ProviderAttemptSummary, ...]
    attempts: tuple[ProviderAttemptRecord, ...] = field(default_factory=tuple)
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_tokens: int = 0
    total_actual_cost: Decimal = Decimal("0")
    currency: str = "USD"


@dataclass(frozen=True)
class ChainFailure:
    """整条 Chain 失败时抛出的结构化信息载体（由异常携带）。"""

    error_category: str
    error_code: str
    public_message: str
    attempt_count: int
    attempted_providers: tuple[ProviderAttemptSummary, ...]
    attempts: tuple[ProviderAttemptRecord, ...]
    total_input_tokens: int
    total_output_tokens: int
    total_actual_cost: Decimal
    currency: str
    charge_possible: bool


class ProviderChainExhaustedError(RuntimeError):
    """所有 Provider 失败或无可执行 Provider。"""

    def __init__(self, failure: ChainFailure) -> None:
        super().__init__(failure.public_message)
        self.failure = failure


class ProviderChainQuotaStopError(RuntimeError):
    """剩余额度不足，停止 fallback。"""

    def __init__(self, failure: ChainFailure) -> None:
        super().__init__("remaining quota insufficient for next provider attempt")
        self.failure = failure


class ProviderChainCancelledError(RuntimeError):
    """用户取消后停止后续 Provider。"""

    def __init__(self, failure: ChainFailure) -> None:
        super().__init__("provider chain cancelled")
        self.failure = failure


def outcome_to_safe_dict(outcome: ChainAnalysisOutcome | ChainReportOutcome | ChainFailure) -> dict[str, Any]:
    """写入 Audit metadata 的安全摘要。"""

    if isinstance(outcome, ChainFailure):
        return {
            "fallback_used": outcome.attempt_count > 1,
            "attempt_count": outcome.attempt_count,
            "attempted_provider_names": [item.provider_name for item in outcome.attempted_providers],
            "total_tokens": outcome.total_input_tokens + outcome.total_output_tokens,
            "total_cost": str(outcome.total_actual_cost),
            "final_status": "failure",
        }
    return {
        "selected_provider": outcome.provider_name,
        "selected_model": outcome.actual_model,
        "route_tier": outcome.route_tier,
        "fallback_used": outcome.fallback_used,
        "attempt_count": outcome.attempt_count,
        "attempted_provider_names": [item.provider_name for item in outcome.attempted_providers],
        "total_tokens": outcome.total_tokens,
        "total_cost": str(outcome.total_actual_cost),
        "final_status": "success",
    }


__all__ = [
    "AttemptStatus",
    "ChainAnalysisOutcome",
    "ChainFailure",
    "ChainReportOutcome",
    "ProviderAttemptRecord",
    "ProviderAttemptSummary",
    "ProviderChainCancelledError",
    "ProviderChainExhaustedError",
    "ProviderChainQuotaStopError",
    "outcome_to_safe_dict",
]
