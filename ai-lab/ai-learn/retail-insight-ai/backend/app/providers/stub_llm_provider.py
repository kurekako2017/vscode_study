"""StubLLMProvider 的本地实现。

文件职责：
- 提供不访问外部服务的模型 provider stub。
- 作为未来 LLMProvider 的可运行占位实现，方便测试 seam 和 fallback。

谁会调用它：
- `backend/app/config/container.py` 在组合根中创建。
- `backend/app/services/rag_answer_generator.py` 在启用 LLM path 时调用。

它调用谁：
- 不调用外部 API，只基于传入的 prompt context 组装确定性结果。

输入是什么：
- `RAGPromptContext`

输出是什么：
- `LLMProviderOutput`

为什么需要这一层：
- 先把 provider 接口跑通，但不引入真实 OpenAI / Azure / 外部依赖。

日本现场面试怎么讲：
- 这是最小可运行的 model seam，先验证编排与 fallback，不碰真实模型成本。
"""

from __future__ import annotations

from uuid import uuid5, NAMESPACE_URL

from app.models.ai_analysis import (
    LLMAnalysisInput,
    LLMProviderRateLimitError,
    LLMProviderResult,
    LLMProviderTimeoutError,
)
from app.models.internal_rag import LLMUsageMetrics, RAGPromptContext
from app.providers.llm_provider import LLMProviderOutput


class StubLLMProvider:
    """本地 stub provider，返回 deterministic 的草稿回答。"""

    name = "stub"
    provider_name = "stub"
    model_name = "stub-enterprise-v1"

    def __init__(self, behavior: str = "success") -> None:
        self.behavior = behavior
        self.call_count = 0

    def analyze(self, request: LLMAnalysisInput) -> LLMProviderResult:
        """生成确定性分析；故障模式只用于无网络合同测试。"""

        self.call_count += 1
        if self.behavior == "timeout":
            raise LLMProviderTimeoutError("stub timeout")
        if self.behavior == "rate_limit":
            raise LLMProviderRateLimitError("stub rate limited")
        if self.behavior == "failure":
            raise RuntimeError("stub provider failure")
        excerpts = [f"[{item.document_id}/{item.chunk_id}] {item.excerpt}" for item in request.evidence]
        answer = "Stub AI analysis:\n" + "\n".join(excerpts)
        input_tokens = max(1, (len(request.question) + sum(len(item.excerpt) for item in request.evidence) + 3) // 4)
        output_tokens = min(request.max_output_tokens, max(1, (len(answer) + 3) // 4))
        return LLMProviderResult(
            answer=answer,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=max(1, len(answer) // 8),
            provider_request_id=str(uuid5(NAMESPACE_URL, request.request_id)),
            finish_reason="stop",
        )

    def generate(self, context: RAGPromptContext) -> LLMProviderOutput:
        """基于 citations 和 answer mode 组装稳定输出，不访问外部服务。"""

        answer = self._build_answer(context)
        usage = self._build_usage(context, answer)
        return LLMProviderOutput(answer=answer, citations=list(context.citations), usage=usage)

    def _build_answer(self, context: RAGPromptContext) -> str:
        """用 prompt 输入拼出一个稳定、可测试的 stub answer。"""

        if context.answer_mode.value == "extractive":
            lines = [f"{index}. {citation.excerpt}" for index, citation in enumerate(context.citations, start=1)]
            return "Stub extractive answer:\n" + "\n".join(lines)

        summary_bits = [self._summarize(text) for text in context.retrieval_excerpts[: context.limit]]
        summary = " ".join(bit for bit in summary_bits if bit)
        return "Stub summary: " + summary if summary else "Stub summary: no concise summary available."

    def _build_usage(self, context: RAGPromptContext, answer: str) -> LLMUsageMetrics:
        """生成 token / cost / latency 的占位信息，便于后续接真实计费。"""

        prompt_tokens = max(1, len(context.question.split()) + sum(len(c.excerpt.split()) for c in context.citations))
        completion_tokens = max(1, len(answer.split()))
        estimated_cost = round((prompt_tokens + completion_tokens) * 0.00001, 6)
        latency_ms = max(1, len(answer) // 4)
        return LLMUsageMetrics(
            provider_name=self.name,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            estimated_cost=estimated_cost,
            latency_ms=latency_ms,
        )

    def _summarize(self, value: str, *, word_limit: int = 18) -> str:
        """简单截断，保证 stub summary 的输出完全确定。"""

        words = value.split()
        if len(words) <= word_limit:
            return value
        return " ".join(words[:word_limit]).rstrip(",;:") + "..."
