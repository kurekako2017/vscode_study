"""固定 Provider Chain 注册表与端点配置。

文件职责：
- 冻结 OpenRouter → NVIDIA → Gemini → Local Qwen 的严格串行顺序。
- 从 Settings 构建可加入 Chain 的 Provider 端点配置。
- 客户端不能改顺序、不能选 Provider/Model。

谁调用它：container、ProviderChain、Settings 校验。
它调用谁：Settings。
日本现场面试：路由优先级是运维配置，不是业务侧动态策略。
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Literal

from pydantic import SecretStr

from app.config.settings import Settings

ProviderName = Literal["openrouter", "nvidia", "gemini", "local_qwen"]
RouteTier = Literal["low_cost", "high_quality"]

# 客户端不可修改；enabled=false 时从 Chain 跳过，但顺序永不重排。
FIXED_PROVIDER_ORDER: tuple[ProviderName, ...] = (
    "openrouter",
    "nvidia",
    "gemini",
    "local_qwen",
)

DISPLAY_NAMES: dict[str, str] = {
    "openrouter": "OpenRouter",
    "nvidia": "NVIDIA",
    "gemini": "Gemini",
    "local_qwen": "Local Qwen",
    "stub-low-cost": "Development Stub",
    "stub-high-quality": "Development Stub",
}


@dataclass(frozen=True)
class ProviderEndpointConfig:
    """单个 Provider 的服务端权威配置；价格单位：USD / 百万 tokens。"""

    name: ProviderName
    enabled: bool
    base_url: str
    api_key: SecretStr | None
    low_cost_model: str
    high_quality_model: str
    low_input_price_per_million: Decimal
    low_output_price_per_million: Decimal
    high_input_price_per_million: Decimal
    high_output_price_per_million: Decimal
    attempt_timeout_seconds: float
    requires_api_key: bool = True
    max_retries: int = 0

    def model_for(self, route_tier: RouteTier) -> str:
        if route_tier == "low_cost":
            return self.low_cost_model
        return self.high_quality_model

    def input_price_for(self, route_tier: RouteTier) -> Decimal:
        if route_tier == "low_cost":
            return self.low_input_price_per_million
        return self.high_input_price_per_million

    def output_price_for(self, route_tier: RouteTier) -> Decimal:
        if route_tier == "low_cost":
            return self.low_output_price_per_million
        return self.high_output_price_per_million

    def display_name(self) -> str:
        return DISPLAY_NAMES.get(self.name, self.name)


def _secret_present(value: SecretStr | None) -> bool:
    if value is None:
        return False
    return bool(value.get_secret_value().strip())


def build_provider_endpoints(settings: Settings) -> list[ProviderEndpointConfig]:
    """按固定顺序返回全部端点配置（含 disabled）；Chain 构建时再过滤。"""

    return [
        ProviderEndpointConfig(
            name="openrouter",
            enabled=settings.openrouter_enabled,
            base_url=settings.openrouter_base_url,
            api_key=settings.openrouter_api_key,
            low_cost_model=(settings.openrouter_low_cost_model or "").strip(),
            high_quality_model=(settings.openrouter_high_quality_model or "").strip(),
            low_input_price_per_million=settings.openrouter_low_input_price,
            low_output_price_per_million=settings.openrouter_low_output_price,
            high_input_price_per_million=settings.openrouter_high_input_price,
            high_output_price_per_million=settings.openrouter_high_output_price,
            attempt_timeout_seconds=settings.openrouter_attempt_timeout_seconds,
            requires_api_key=True,
            max_retries=0 if settings.llm_provider_mode == "fallback_chain" else settings.real_llm_max_retries,
        ),
        ProviderEndpointConfig(
            name="nvidia",
            enabled=settings.nvidia_enabled,
            base_url=settings.nvidia_base_url,
            api_key=settings.nvidia_api_key,
            low_cost_model=(settings.nvidia_low_cost_model or "").strip(),
            high_quality_model=(settings.nvidia_high_quality_model or "").strip(),
            low_input_price_per_million=settings.nvidia_low_input_price,
            low_output_price_per_million=settings.nvidia_low_output_price,
            high_input_price_per_million=settings.nvidia_high_input_price,
            high_output_price_per_million=settings.nvidia_high_output_price,
            attempt_timeout_seconds=settings.nvidia_attempt_timeout_seconds,
            requires_api_key=True,
            max_retries=0,
        ),
        ProviderEndpointConfig(
            name="gemini",
            enabled=settings.gemini_enabled,
            base_url=settings.gemini_base_url,
            api_key=settings.gemini_api_key,
            low_cost_model=(settings.gemini_low_cost_model or "").strip(),
            high_quality_model=(settings.gemini_high_quality_model or "").strip(),
            low_input_price_per_million=settings.gemini_low_input_price,
            low_output_price_per_million=settings.gemini_low_output_price,
            high_input_price_per_million=settings.gemini_high_input_price,
            high_output_price_per_million=settings.gemini_high_output_price,
            attempt_timeout_seconds=settings.gemini_attempt_timeout_seconds,
            requires_api_key=True,
            max_retries=0,
        ),
        ProviderEndpointConfig(
            name="local_qwen",
            enabled=settings.local_qwen_enabled,
            base_url=settings.local_qwen_base_url,
            api_key=settings.local_qwen_api_key,
            low_cost_model=(settings.local_qwen_low_cost_model or "").strip(),
            high_quality_model=(settings.local_qwen_high_quality_model or "").strip(),
            low_input_price_per_million=settings.local_qwen_low_input_price,
            low_output_price_per_million=settings.local_qwen_low_output_price,
            high_input_price_per_million=settings.local_qwen_high_input_price,
            high_output_price_per_million=settings.local_qwen_high_output_price,
            attempt_timeout_seconds=settings.local_qwen_attempt_timeout_seconds,
            requires_api_key=settings.local_qwen_require_api_key,
            max_retries=0,
        ),
    ]


def enabled_chain_endpoints(settings: Settings) -> list[ProviderEndpointConfig]:
    """仅返回 enabled 且配置完整的 Provider；顺序与 FIXED_PROVIDER_ORDER 一致。"""

    return [item for item in build_provider_endpoints(settings) if item.enabled]


def validate_endpoint_or_raise(endpoint: ProviderEndpointConfig) -> None:
    """enabled=true 时缺 Key/模型/URL 则 fail-closed。"""

    if not endpoint.enabled:
        return
    if not endpoint.base_url.strip():
        raise ValueError(f"{endpoint.name}: base_url is required when enabled")
    if not endpoint.low_cost_model or not endpoint.high_quality_model:
        raise ValueError(f"{endpoint.name}: low_cost and high_quality models are required when enabled")
    if endpoint.low_cost_model == endpoint.high_quality_model:
        raise ValueError(f"{endpoint.name}: low_cost and high_quality models must be distinct")
    if endpoint.requires_api_key and not _secret_present(endpoint.api_key):
        raise ValueError(f"{endpoint.name}: API key is required when enabled")


def display_provider_name(provider: str) -> str:
    if provider in DISPLAY_NAMES:
        return DISPLAY_NAMES[provider]
    if provider.startswith("stub"):
        return "Development Stub"
    if provider.startswith("openrouter"):
        return "OpenRouter"
    if provider.startswith("nvidia"):
        return "NVIDIA"
    if provider.startswith("gemini"):
        return "Gemini"
    if provider.startswith("local_qwen") or provider.startswith("qwen"):
        return "Local Qwen"
    return provider


__all__ = [
    "DISPLAY_NAMES",
    "FIXED_PROVIDER_ORDER",
    "ProviderEndpointConfig",
    "ProviderName",
    "RouteTier",
    "build_provider_endpoints",
    "display_provider_name",
    "enabled_chain_endpoints",
    "validate_endpoint_or_raise",
]
