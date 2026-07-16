"""双路由 StubLLMProvider：low_cost 与 high_quality 互不串线。

文件职责：
- 提供不访问外部服务的确定性 stub。
- 两个 alias 有不同 provider/model 标识，测试可分别统计 call_count。

谁会调用它：
- 仅 LLMGatewayService（经 ModelRouter）在预占成功后调用。

它调用谁：
- 不调用外部 API。

日本现场面试怎么讲：
- 先把成本治理与双路由跑通，再把 alias 映射到真实模型。
"""

from __future__ import annotations

from uuid import uuid5, NAMESPACE_URL

from app.models.ai_analysis import (
    LLMAnalysisInput,
    LLMProviderPartialFailureError,
    LLMProviderRateLimitError,
    LLMProviderResult,
    LLMProviderTimeoutError,
    LLMReportInput,
    LLMReportResult,
)
from app.models.internal_rag import LLMUsageMetrics, RAGPromptContext
from app.providers.llm_provider import LLMProviderOutput


class StubLLMProvider:
    """本地 stub provider；behavior 只服务无网络合同测试。"""

    def __init__(
        self,
        *,
        provider_name: str,
        model_name: str,
        behavior: str = "success",
        mode: str = "analysis",
    ) -> None:
        self.provider_name = provider_name
        self.model_name = model_name
        self.name = provider_name
        self.behavior = behavior
        self.mode = mode
        self.call_count = 0
        self.analyze_call_count = 0
        self.generate_report_call_count = 0

    def analyze(self, request: LLMAnalysisInput) -> LLMProviderResult:
        """生成确定性低成本分析；故障模式只用于无网络合同测试。"""

        self.call_count += 1
        self.analyze_call_count += 1
        self._maybe_fail()
        excerpts = [f"[{item.document_id}/{item.chunk_id}] {item.excerpt}" for item in request.evidence]
        answer = f"Stub AI analysis ({self.provider_name}):\n" + "\n".join(excerpts)
        input_tokens = max(1, (len(request.question) + sum(len(item.excerpt) for item in request.evidence) + 3) // 4)
        output_tokens = min(request.max_output_tokens, max(1, (len(answer) + 3) // 4))
        return LLMProviderResult(
            answer=answer,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=max(1, len(answer) // 8),
            provider_request_id=str(uuid5(NAMESPACE_URL, f"{self.provider_name}:{request.request_id}")),
            finish_reason="stop",
        )

    def generate_report(self, request: LLMReportInput) -> LLMReportResult:
        """生成确定性高质量董事会报告草稿。"""

        self.call_count += 1
        self.generate_report_call_count += 1
        self._maybe_fail()
        citations = [f"- {item.document_id}/{item.chunk_id}: {item.excerpt[:120]}" for item in request.evidence]
        executive_summary = (
            f"Board summary ({self.provider_name}): {request.title}. "
            f"Analysis basis: {request.analysis_answer[:240]}"
        )
        kpi_findings = (
            "KPI trajectory remains evidence-grounded",
            f"Evidence count under review: {len(request.evidence)}",
        )
        risks = (
            "Residual operational risk if evidence is incomplete",
            "High-quality generation cost must stay inside daily quota",
        )
        recommendations = (
            "Submit the generated report to Approval only after human review",
            "Keep low_cost analysis as the daily default path",
        )
        markdown = "\n".join(
            [
                f"# {request.title}",
                "",
                "## Executive Summary",
                executive_summary,
                "",
                "## KPI Findings",
                *[f"- {item}" for item in kpi_findings],
                "",
                "## Risks",
                *[f"- {item}" for item in risks],
                "",
                "## Recommendations",
                *[f"- {item}" for item in recommendations],
                "",
                "## Citations",
                *citations,
            ]
        )
        input_tokens = max(
            1,
            (
                len(request.title)
                + len(request.analysis_answer)
                + sum(len(item.excerpt) for item in request.evidence)
                + 3
            )
            // 4,
        )
        output_tokens = min(request.max_output_tokens, max(1, (len(markdown) + 3) // 4))
        return LLMReportResult(
            executive_summary=executive_summary,
            kpi_findings=kpi_findings,
            risks=risks,
            recommendations=recommendations,
            markdown=markdown,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=max(1, len(markdown) // 6),
            provider_request_id=str(uuid5(NAMESPACE_URL, f"{self.provider_name}:report:{request.request_id}")),
            finish_reason="stop",
        )

    def generate(self, context: RAGPromptContext) -> LLMProviderOutput:
        """兼容旧 RAG seam；普通 RAG 路径已强制 deterministic，不进入 Gateway。"""

        self.call_count += 1
        if context.answer_mode.value == "extractive":
            lines = [f"{index}. {citation.excerpt}" for index, citation in enumerate(context.citations, start=1)]
            answer = "Stub extractive answer:\n" + "\n".join(lines)
        else:
            summary = " ".join(context.retrieval_excerpts[: context.limit])
            answer = "Stub summary: " + summary if summary else "Stub summary: no concise summary available."
        usage = LLMUsageMetrics(
            provider_name=self.name,
            prompt_tokens=max(1, len(context.question.split()) + sum(len(c.excerpt.split()) for c in context.citations)),
            completion_tokens=max(1, len(answer.split())),
            estimated_cost=round((max(1, len(context.question.split())) + max(1, len(answer.split()))) * 0.00001, 6),
            latency_ms=max(1, len(answer) // 4),
        )
        return LLMProviderOutput(answer=answer, citations=list(context.citations), usage=usage)

    def _maybe_fail(self) -> None:
        if self.behavior == "timeout":
            raise LLMProviderTimeoutError("stub timeout")
        if self.behavior == "rate_limit":
            raise LLMProviderRateLimitError("stub rate limited")
        if self.behavior == "failure":
            raise RuntimeError("stub provider failure")
        if self.behavior == "partial_failure":
            raise LLMProviderPartialFailureError(input_tokens=7, output_tokens=3, latency_ms=4)
