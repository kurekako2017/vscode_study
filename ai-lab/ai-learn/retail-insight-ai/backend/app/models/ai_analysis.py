"""AI Analysis / Executive Report 的领域合同。

文件职责：定义证据引用、Provider 输入输出、Ledger 状态和 API 结果快照。
调用关系：Service 组装输入，Gateway 调 Stub Provider，PostgreSQL Repository 持久化。
设计理由：Provider 不接触 HTTP/JWT/Repository，且只获得截断后的必要证据。
日本现场面试：可以说成“用稳定 Port 把模型调用与成本治理、数据库事实解耦”。
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any


class LLMUsageStatus(StrEnum):
    RESERVED = "reserved"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    REJECTED = "rejected"


@dataclass(frozen=True)
class AIEvidence:
    document_id: str
    chunk_id: str
    score: Decimal
    excerpt: str


@dataclass(frozen=True)
class LLMAnalysisInput:
    question: str
    evidence: tuple[AIEvidence, ...]
    max_output_tokens: int
    request_id: str
    timeout_seconds: float


@dataclass(frozen=True)
class LLMProviderResult:
    answer: str
    input_tokens: int
    output_tokens: int
    latency_ms: int
    provider_request_id: str
    finish_reason: str
    # provider_reported：信任上游 usage；estimated：本地估算并记账，不伪造精确值。
    usage_source: str = "provider_reported"
    actual_model: str | None = None
    warnings: tuple[str, ...] = ()
    insufficient_context: bool = False


@dataclass(frozen=True)
class LLMReportInput:
    """高质量董事会报告的 Provider 输入；只含已成功分析与证据摘要。"""

    title: str
    analysis_answer: str
    evidence: tuple[AIEvidence, ...]
    max_output_tokens: int
    request_id: str
    timeout_seconds: float


@dataclass(frozen=True)
class LLMReportResult:
    """高质量 Provider 的结构化报告输出。"""

    executive_summary: str
    kpi_findings: tuple[str, ...]
    risks: tuple[str, ...]
    recommendations: tuple[str, ...]
    markdown: str
    input_tokens: int
    output_tokens: int
    latency_ms: int
    provider_request_id: str
    finish_reason: str
    usage_source: str = "provider_reported"
    actual_model: str | None = None


@dataclass(frozen=True)
class ProviderAttemptPublic:
    """API 安全摘要：仅 provider/model/status/latency。"""

    provider_name: str
    model_name: str
    status: str
    latency_ms: int | None = None


@dataclass(frozen=True)
class AIAnalysisResult:
    analysis_id: str
    answer: str
    citations: tuple[AIEvidence, ...]
    provider_name: str
    model_name: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    actual_cost: Decimal
    currency: str
    status: str
    created_at: datetime
    route_tier: str = "low_cost"
    estimated_cost: Decimal | None = None
    actor_user_id: str | None = None
    task_id: str | None = None
    usage_id: str | None = None
    fallback_used: bool = False
    attempt_count: int = 1
    attempted_providers: tuple[ProviderAttemptPublic, ...] = ()


@dataclass(frozen=True)
class ExecutiveReportResult:
    report_id: str
    report_version_id: str
    task_id: str
    title: str
    executive_summary: str
    kpi_findings: tuple[str, ...]
    risks: tuple[str, ...]
    recommendations: tuple[str, ...]
    citations: tuple[AIEvidence, ...]
    provider_name: str
    model_name: str
    route_tier: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    estimated_cost: Decimal
    actual_cost: Decimal
    currency: str
    status: str
    created_at: datetime
    analysis_id: str
    usage_id: str
    markdown: str
    fallback_used: bool = False
    attempt_count: int = 1
    attempted_providers: tuple[ProviderAttemptPublic, ...] = ()


@dataclass(frozen=True)
class ReservationOutcome:
    kind: str
    usage_id: str
    existing_result: Any = None
    rejection_code: str | None = None


class LLMProviderTimeoutError(TimeoutError):
    """Stub/Real Provider 共用的稳定超时类别。"""


class LLMProviderRateLimitError(RuntimeError):
    """Provider 端限流，与本地 quota rejected 分开。"""


class LLMProviderPartialFailureError(RuntimeError):
    """Provider 已消耗部分 token 后失败，Ledger 仍必须结算该成本。"""

    def __init__(self, *, input_tokens: int, output_tokens: int, latency_ms: int) -> None:
        super().__init__("provider partial failure")
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.latency_ms = latency_ms


class LLMProviderAuthenticationError(RuntimeError):
    """Provider 401/403：凭据无效，不得重试。"""


class LLMProviderModelUnavailableError(RuntimeError):
    """模型不存在或不可用：不得重试、不得静默换模型。"""


class LLMProviderUnavailableError(RuntimeError):
    """Provider 5xx / 连接层故障：允许有限重试后仍失败。"""


class LLMProviderResponseInvalidError(RuntimeError):
    """结构化 JSON 无效且本地修复失败：不得发起第二次收费调用。"""


class LLMProviderCitationInvalidError(RuntimeError):
    """模型返回了不在 Evidence 集合内的 Citation。"""


__all__ = [
    "AIEvidence", "AIAnalysisResult", "ExecutiveReportResult", "LLMAnalysisInput",
    "LLMProviderResult", "LLMReportInput", "LLMReportResult",
    "LLMProviderPartialFailureError", "LLMProviderRateLimitError", "LLMProviderTimeoutError",
    "LLMProviderAuthenticationError", "LLMProviderModelUnavailableError",
    "LLMProviderUnavailableError", "LLMProviderResponseInvalidError",
    "LLMProviderCitationInvalidError",
    "LLMUsageStatus", "ProviderAttemptPublic", "ReservationOutcome",
]
