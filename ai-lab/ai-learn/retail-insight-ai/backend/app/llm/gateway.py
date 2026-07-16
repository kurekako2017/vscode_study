"""统一 LLM Gateway：唯一允许调用 Provider 的组件。

文件职责：根据 operation 解析 policy 与 provider，执行 analyze / generate_report。
谁调用它：AIAnalysisService、ExecutiveReportService。
它调用谁：ModelRouter → StubLLMProvider；不接触 HTTP/JWT/Repository。
输入：operation + 领域请求；输出：Provider 结果。
设计理由：业务 Router 与普通 RAG 永远不直接依赖 Provider。
日本现场面试：所有收费 side-effect 都必须经过 Gateway 这一条窄门。
"""

from __future__ import annotations

from app.llm.model_router import ModelRouter
from app.llm.operation_policy import OperationPolicy, OperationPolicyRegistry
from app.models.ai_analysis import LLMAnalysisInput, LLMProviderResult, LLMReportInput, LLMReportResult
from app.providers.llm_provider import LLMProvider


class LLMGatewayService:
    """企业级 LLM 调用窄门；本轮只接 Stub，不访问真实网络。"""

    def __init__(
        self,
        *,
        policy_registry: OperationPolicyRegistry,
        model_router: ModelRouter,
    ) -> None:
        self._policy_registry = policy_registry
        self._router = model_router

    def policy_for(self, operation: str) -> OperationPolicy:
        try:
            return self._policy_registry.get(operation)
        except KeyError as exc:
            raise LookupError(f"unknown operation: {operation}") from exc

    def resolve_provider(self, operation: str) -> LLMProvider:
        provider, _, _ = self._router.resolve(operation)
        return provider

    def analyze(self, *, operation: str, request: LLMAnalysisInput) -> LLMProviderResult:
        """low_cost 分析入口；只允许 ai_analysis 操作。"""

        if operation != "ai_analysis":
            raise LookupError(f"analyze does not accept operation: {operation}")
        provider, _, _ = self._router.resolve(operation)
        return provider.analyze(request)

    def generate_report(self, *, operation: str, request: LLMReportInput) -> LLMReportResult:
        """high_quality 报告入口；只允许 executive_report 操作。"""

        if operation != "executive_report":
            raise LookupError(f"generate_report does not accept operation: {operation}")
        provider, _, _ = self._router.resolve(operation)
        generate = getattr(provider, "generate_report", None)
        if generate is None:
            raise RuntimeError("selected provider cannot generate executive reports")
        return generate(request)


__all__ = ["LLMGatewayService"]
