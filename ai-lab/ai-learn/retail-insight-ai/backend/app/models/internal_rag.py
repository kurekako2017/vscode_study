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


__all__ = ["InternalRagEvaluationResult", "InternalRagWarning"]
