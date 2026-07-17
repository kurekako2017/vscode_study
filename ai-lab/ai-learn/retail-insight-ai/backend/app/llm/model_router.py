"""服务端 Model Router：operation → route_tier → Provider 别名。

文件职责：唯一决定 Provider 实例；客户端不能指定 provider/model/route_tier。
谁调用它：LLMGatewayService。
它调用谁：已注册的 Stub 或 OpenRouter Provider 实例。
输入：operation；输出：匹配的 LLMProvider。
设计理由：low_cost 与 high_quality 物理隔离，测试可分别统计 call_count。
日本现场面试：路由是服务端权威，未知 operation/tier 一律 fail-closed。
"""

from __future__ import annotations

from app.llm.operation_policy import OperationPolicyRegistry
from app.providers.llm_provider import LLMProvider


class ModelRouter:
    """按 operation policy 选择 Provider；禁止跨 tier 串线。"""

    def __init__(
        self,
        *,
        policy_registry: OperationPolicyRegistry,
        providers_by_alias: dict[str, LLMProvider],
    ) -> None:
        self._policy_registry = policy_registry
        self._providers = providers_by_alias

    def resolve(self, operation: str) -> tuple[LLMProvider, str, str]:
        """返回 (provider, provider_alias, model_name)。"""

        try:
            policy = self._policy_registry.get(operation)
        except KeyError as exc:
            raise LookupError(f"unknown operation: {operation}") from exc
        provider = self._providers.get(policy.provider_alias)
        if provider is None:
            raise LookupError(f"unknown provider alias: {policy.provider_alias}")
        if getattr(provider, "provider_name", None) != policy.provider_alias:
            raise RuntimeError("provider alias mismatch; refuse cross-tier routing")
        if getattr(provider, "model_name", None) != policy.model_name:
            raise RuntimeError("provider model mismatch; refuse cross-tier routing")
        return provider, policy.provider_alias, policy.model_name


__all__ = ["ModelRouter"]
