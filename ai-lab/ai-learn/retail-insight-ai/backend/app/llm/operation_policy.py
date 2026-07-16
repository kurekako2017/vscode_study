"""集中式 Operation Policy：定义 low_cost / high_quality 调用边界。

文件职责：从 Settings 构建不可变 policy snapshot，供 Gateway、Ledger 与测试使用。
谁调用它：LLMGatewayService、AIAnalysisService、ExecutiveReportService。
它调用谁：Settings；不调用 Provider 或 Repository。
输入：operation 名称；输出：冻结的 OperationPolicy。
设计理由：限额、价格与路由不得散落 magic number，也不得由客户端传入。
日本现场面试：政策快照写入 Ledger 后，后续配置变更不能改写历史账单。
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal
from typing import Any, Literal

from app.config.settings import Settings

OperationName = Literal["ai_analysis", "executive_report"]
RouteTier = Literal["low_cost", "high_quality"]


@dataclass(frozen=True)
class OperationPolicy:
    """单次调用的服务端权威政策；写入 Ledger 时序列化为 snapshot。"""

    operation: OperationName
    route_tier: RouteTier
    provider_alias: str
    model_name: str
    max_input_tokens: int
    max_output_tokens: int
    request_max_cost: Decimal
    user_daily_request_limit: int
    user_daily_token_limit: int
    user_daily_cost_limit: Decimal
    global_daily_request_limit: int
    global_daily_token_limit: int
    global_daily_cost_limit: Decimal
    input_price_per_million: Decimal
    output_price_per_million: Decimal
    currency: str
    timeout_seconds: float
    evidence_max_count: int
    evidence_max_chars: int
    requires_confirmation: bool
    requires_evidence: bool
    requires_succeeded_analysis: bool
    creates_report_version: bool

    def snapshot(self) -> dict[str, Any]:
        """返回可 JSON 化的 policy 快照；金额以字符串保留精度。"""

        payload = asdict(self)
        for key, value in list(payload.items()):
            if isinstance(value, Decimal):
                payload[key] = str(value)
        return payload

    def price_snapshot(self) -> dict[str, str]:
        return {
            "input_price_per_million": str(self.input_price_per_million),
            "output_price_per_million": str(self.output_price_per_million),
            "currency": self.currency,
        }

    def token_limit_snapshot(self) -> dict[str, int]:
        return {
            "max_input_tokens": self.max_input_tokens,
            "max_output_tokens": self.max_output_tokens,
        }


class OperationPolicyRegistry:
    """按 operation 解析服务端政策；未知 operation fail-closed。"""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._policies = {
            "ai_analysis": OperationPolicy(
                operation="ai_analysis",
                route_tier="low_cost",
                provider_alias=settings.llm_low_cost_provider_alias,
                model_name=settings.llm_low_cost_model_name,
                max_input_tokens=settings.llm_max_input_tokens,
                max_output_tokens=settings.llm_max_output_tokens,
                request_max_cost=settings.llm_request_max_cost,
                user_daily_request_limit=settings.llm_user_daily_request_limit,
                user_daily_token_limit=settings.llm_user_daily_token_limit,
                user_daily_cost_limit=settings.llm_user_daily_cost_limit,
                global_daily_request_limit=settings.llm_global_daily_request_limit,
                global_daily_token_limit=settings.llm_global_daily_token_limit,
                global_daily_cost_limit=settings.llm_global_daily_cost_limit,
                input_price_per_million=settings.llm_input_price_per_million,
                output_price_per_million=settings.llm_output_price_per_million,
                currency=settings.llm_currency,
                timeout_seconds=settings.llm_timeout_seconds,
                evidence_max_count=settings.llm_evidence_max_count,
                evidence_max_chars=settings.llm_evidence_max_chars,
                requires_confirmation=True,
                requires_evidence=True,
                requires_succeeded_analysis=False,
                creates_report_version=False,
            ),
            "executive_report": OperationPolicy(
                operation="executive_report",
                route_tier="high_quality",
                provider_alias=settings.llm_high_quality_provider_alias,
                model_name=settings.llm_high_quality_model_name,
                max_input_tokens=settings.llm_hq_max_input_tokens,
                max_output_tokens=settings.llm_hq_max_output_tokens,
                request_max_cost=settings.llm_hq_request_max_cost,
                user_daily_request_limit=settings.llm_hq_user_daily_request_limit,
                user_daily_token_limit=settings.llm_hq_user_daily_token_limit,
                user_daily_cost_limit=settings.llm_hq_user_daily_cost_limit,
                global_daily_request_limit=settings.llm_hq_global_daily_request_limit,
                global_daily_token_limit=settings.llm_hq_global_daily_token_limit,
                global_daily_cost_limit=settings.llm_hq_global_daily_cost_limit,
                input_price_per_million=settings.llm_hq_input_price_per_million,
                output_price_per_million=settings.llm_hq_output_price_per_million,
                currency=settings.llm_currency,
                timeout_seconds=settings.llm_timeout_seconds,
                evidence_max_count=settings.llm_evidence_max_count,
                evidence_max_chars=settings.llm_hq_evidence_max_chars,
                requires_confirmation=True,
                requires_evidence=True,
                requires_succeeded_analysis=True,
                creates_report_version=True,
            ),
        }

    def get(self, operation: str) -> OperationPolicy:
        policy = self._policies.get(operation)
        if policy is None:
            raise KeyError(f"unknown operation: {operation}")
        return policy


__all__ = ["OperationName", "OperationPolicy", "OperationPolicyRegistry", "RouteTier"]
