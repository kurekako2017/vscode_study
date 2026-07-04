"""Internal RAG 的内部评估模型。

文件职责：
- 定义 deterministic internal RAG 的评估结果和 warning 枚举。
- 把 citation quality、coverage、confidence 这些内部指标和对外 API 响应分开。

谁会调用它：
- `backend/app/services/internal_rag_evaluation_service.py`
- `backend/app/services/internal_rag_service.py`
- internal RAG 单元测试

它调用谁：
- 不调用其他模块，只作为内部评估数据结构使用。

输入是什么：
- query、answer、citations 以及检索上下文的质量信息。

输出是什么：
- 评估后的 coverage_score、citation_score、confidence 和 warnings。

为什么需要这一层：
- internal RAG 的 API 只冻结对外 response；评估细节要放在内部模型中，便于后续替换 LLM 或 evaluation 策略。

日本现场面试怎么讲：
- 这是 internal RAG 的 internal scorecard，用来判断 citation 是否完整、上下文是否足够、以及回答是否可靠。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from app.schemas.internal_rag_api import InternalRagAnswerMode, InternalRagCitationResponse


class InternalRagWarning(StrEnum):
    """定义 internal RAG 的非致命质量警告。"""

    LOW_CONTEXT = "low_context"
    MISSING_CITATION = "missing_citation"
    WEAK_MATCH = "weak_match"


@dataclass(frozen=True)
class InternalRagEvaluationResult:
    """保存 internal RAG 的评估结果，不直接作为 HTTP 响应返回。"""

    query: str
    answer: str
    citations: list[dict[str, object]]
    coverage_score: float
    citation_score: float
    confidence: float
    warnings: tuple[InternalRagWarning, ...] = field(default_factory=tuple)


class RAGFallbackReason(StrEnum):
    """定义 RAG answer generation 在何种情况下回退。"""

    NONE = "none"
    DISABLED = "disabled"
    TIMEOUT = "timeout"
    UNAVAILABLE = "unavailable"
    INVALID_OUTPUT = "invalid_output"
    MISSING_CITATION = "missing_citation"


@dataclass(frozen=True)
class LLMUsageMetrics:
    """记录未来 LLM provider 的 token / cost / latency 占位信息。"""

    provider_name: str
    prompt_tokens: int
    completion_tokens: int
    estimated_cost: float
    latency_ms: int


@dataclass(frozen=True)
class RAGAnswerGenerationResult:
    """保存 RAG answer generator 的内部输出，不直接作为 HTTP 响应返回。"""

    answer: str
    citations: list[InternalRagCitationResponse]
    retrieval_mode: str
    answer_mode: InternalRagAnswerMode
    provider_name: str
    usage: LLMUsageMetrics
    used_llm_provider: bool
    fallback_reason: RAGFallbackReason = RAGFallbackReason.NONE


@dataclass(frozen=True)
class RAGPromptContext:
    """把回答生成所需的 prompt 输入显式打包，方便 stub provider 和未来真实 provider 共用。"""

    question: str
    answer_mode: InternalRagAnswerMode
    limit: int
    citations: list[InternalRagCitationResponse]
    retrieval_excerpts: tuple[str, ...]


__all__ = [
    "InternalRagEvaluationResult",
    "InternalRagWarning",
    "LLMUsageMetrics",
    "RAGAnswerGenerationResult",
    "RAGFallbackReason",
    "RAGPromptContext",
]
