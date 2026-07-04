"""RAGAnswerGenerator 的回答合成边界。

文件职责：
- 把 deterministic extractive mode 和 future LLM provider seam 放到同一个抽象里。
- 当 provider 失败、超时、输出无效或引用缺失时，回退到 deterministic answer。

谁会调用它：
- `backend/app/services/internal_rag_service.py`

它调用谁：
- `LLMProvider` 或 `StubLLMProvider`
- 只在需要时复用 deterministic answer 逻辑

输入是什么：
- internal RAG request、retrieval results、citations、future provider flag

输出是什么：
- `RAGAnswerGenerationResult`

为什么需要这一层：
- 让 internal RAG service 只负责业务编排和事件，回答生成细节单独封装，后续换真模型时只替换这里。

日本现场面试怎么讲：
- 这是 internal RAG 的 answer generation seam，默认 no-LLM，启用时走 stub provider，并在失败时无损回退。
"""

from __future__ import annotations

from time import perf_counter

from app.models.internal_rag import (
    LLMUsageMetrics,
    RAGAnswerGenerationResult,
    RAGFallbackReason,
    RAGPromptContext,
)
from app.providers.llm_provider import LLMProvider, LLMProviderOutput
from app.schemas.document_retrieval_api import DocumentRetrievalResultResponse
from app.schemas.internal_rag_api import InternalRagAnswerMode, InternalRagAnswerRequest, InternalRagCitationResponse


class RAGAnswerGenerator:
    """在 deterministic answer 和未来 provider output 之间做稳定编排。"""

    def __init__(
        self,
        provider: LLMProvider | None = None,
        *,
        use_llm: bool = False,
    ) -> None:
        """注入可替换 provider，并保留默认 deterministic 行为。"""

        self._provider = provider
        self._use_llm = use_llm

    def generate(
        self,
        *,
        request: InternalRagAnswerRequest,
        question: str,
        retrieval_results: list[DocumentRetrievalResultResponse],
        total_matches: int,
    ) -> RAGAnswerGenerationResult:
        """生成 answer、citations 和 usage 占位数据。"""

        citations = self._select_citations(self._build_citations(retrieval_results), request.limit)
        deterministic = self._build_deterministic_result(request.answer_mode, citations)
        if not self._use_llm or self._provider is None:
            return deterministic

        prompt = RAGPromptContext(
            question=question,
            answer_mode=request.answer_mode,
            limit=request.limit,
            citations=list(citations),
            retrieval_excerpts=tuple(result.content_excerpt for result in retrieval_results),
        )

        started_at = perf_counter()
        try:
            provider_output = self._provider.generate(prompt)
        except TimeoutError:
            return self._fallback(deterministic, RAGFallbackReason.TIMEOUT, self._provider.name, started_at)
        except Exception:  # noqa: BLE001
            return self._fallback(deterministic, RAGFallbackReason.UNAVAILABLE, self._provider.name, started_at)

        validated, fallback_reason = self._validate_provider_output(provider_output, retrieval_results)
        if validated is None:
            return self._fallback(
                deterministic,
                fallback_reason or RAGFallbackReason.INVALID_OUTPUT,
                self._provider.name,
                started_at,
            )

        usage = self._ensure_usage(validated, started_at)
        return RAGAnswerGenerationResult(
            answer=validated.answer,
            citations=validated.citations,
            retrieval_mode="keyword",
            answer_mode=request.answer_mode,
            provider_name=self._provider.name,
            usage=usage,
            used_llm_provider=True,
        )

    def _build_citations(self, results: list[DocumentRetrievalResultResponse]) -> list[InternalRagCitationResponse]:
        """把 retrieval 结果转成 citation。"""

        citations: list[InternalRagCitationResponse] = []
        for result in results:
            citations.append(
                InternalRagCitationResponse(
                    document_id=result.document_id,
                    chunk_id=result.chunk_id,
                    chunk_index=result.chunk_index,
                    excerpt=result.content_excerpt,
                    source=result.source,
                    score=result.score,
                )
            )
        return citations

    def _select_citations(
        self,
        citations: list[InternalRagCitationResponse],
        limit: int,
    ) -> list[InternalRagCitationResponse]:
        """只使用 top retrieval excerpts，保持输出长度稳定。"""

        max_citations = min(len(citations), max(1, min(limit, 3)))
        return citations[:max_citations]

    def _build_deterministic_result(
        self,
        answer_mode: InternalRagAnswerMode,
        citations: list[InternalRagCitationResponse],
    ) -> RAGAnswerGenerationResult:
        """默认 no-LLM 路径仍然是可预测的 extractive / summary 组装。"""

        answer = self._assemble_answer(answer_mode, citations)
        usage = LLMUsageMetrics(
            provider_name="deterministic",
            prompt_tokens=0,
            completion_tokens=0,
            estimated_cost=0.0,
            latency_ms=0,
        )
        return RAGAnswerGenerationResult(
            answer=answer,
            citations=citations,
            retrieval_mode="keyword",
            answer_mode=answer_mode,
            provider_name="deterministic",
            usage=usage,
            used_llm_provider=False,
            fallback_reason=RAGFallbackReason.DISABLED,
        )

    def _assemble_answer(
        self,
        answer_mode: InternalRagAnswerMode,
        citations: list[InternalRagCitationResponse],
    ) -> str:
        """根据 answer_mode 生成 deterministic answer。"""

        if answer_mode is InternalRagAnswerMode.EXTRACTIVE:
            lines = [f"{index}. {citation.excerpt}" for index, citation in enumerate(citations, start=1)]
            return "Extractive answer:\n" + "\n".join(lines)

        summary_parts = [self._summarize_excerpt(citation.excerpt) for citation in citations]
        joined = " ".join(part for part in summary_parts if part)
        return "Summary: " + joined if joined else "Summary: no concise summary available."

    def _summarize_excerpt(self, excerpt: str, *, word_limit: int = 20) -> str:
        """用简单截断模拟 summary，保持完全 deterministic。"""

        words = excerpt.split()
        if len(words) <= word_limit:
            return excerpt
        return " ".join(words[:word_limit]).rstrip(",;:") + "..."

    def _validate_provider_output(
        self,
        output: object,
        retrieval_results: list[DocumentRetrievalResultResponse],
    ) -> tuple[LLMProviderOutput | None, RAGFallbackReason | None]:
        """校验 provider output，任何结构异常都回退到 deterministic mode。"""

        try:
            if not isinstance(output, LLMProviderOutput):
                return None, RAGFallbackReason.INVALID_OUTPUT
            if not isinstance(output.answer, str) or not output.answer.strip():
                return None, RAGFallbackReason.INVALID_OUTPUT
            if not output.citations:
                return None, RAGFallbackReason.MISSING_CITATION

            lookup = {
                (result.document_id, result.chunk_id): result.content_excerpt
                for result in retrieval_results
            }
            for citation in output.citations:
                retrieved_excerpt = lookup[(citation.document_id, citation.chunk_id)]
                if not self._citation_is_grounded(citation.excerpt, retrieved_excerpt):
                    return None, RAGFallbackReason.INVALID_OUTPUT
            return output, None
        except Exception:  # noqa: BLE001
            return None, RAGFallbackReason.INVALID_OUTPUT

    def _citation_is_grounded(self, citation_excerpt: str, retrieved_excerpt: str) -> bool:
        """把 provider citation 与 retrieval chunk 做最小 grounding 检查。"""

        citation_normalized = " ".join(citation_excerpt.split()).lower()
        retrieved_normalized = " ".join(retrieved_excerpt.split()).lower()
        return citation_normalized in retrieved_normalized or retrieved_normalized in citation_normalized

    def _ensure_usage(self, output: LLMProviderOutput, started_at: float) -> LLMUsageMetrics:
        """给 provider usage 补齐 latency 占位信息，避免真实 LLM 出现前字段缺失。"""

        elapsed_ms = max(1, int((perf_counter() - started_at) * 1000))
        return LLMUsageMetrics(
            provider_name=output.usage.provider_name,
            prompt_tokens=output.usage.prompt_tokens,
            completion_tokens=output.usage.completion_tokens,
            estimated_cost=output.usage.estimated_cost,
            latency_ms=max(output.usage.latency_ms, elapsed_ms),
        )

    def _fallback(
        self,
        deterministic: RAGAnswerGenerationResult,
        reason: RAGFallbackReason,
        provider_name: str,
        started_at: float,
    ) -> RAGAnswerGenerationResult:
        """在 provider 失败时回退到 deterministic answer。"""

        elapsed_ms = max(1, int((perf_counter() - started_at) * 1000))
        usage = LLMUsageMetrics(
            provider_name=provider_name,
            prompt_tokens=0,
            completion_tokens=0,
            estimated_cost=0.0,
            latency_ms=elapsed_ms,
        )
        return RAGAnswerGenerationResult(
            answer=deterministic.answer,
            citations=deterministic.citations,
            retrieval_mode=deterministic.retrieval_mode,
            answer_mode=deterministic.answer_mode,
            provider_name=provider_name,
            usage=usage,
            used_llm_provider=False,
            fallback_reason=reason,
        )


__all__ = ["RAGAnswerGenerator"]
