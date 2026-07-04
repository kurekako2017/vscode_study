"""LLMProvider 的稳定接口与输出模型。

文件职责：
- 冻结未来模型 provider 的接口形状。
- 让 RAGAnswerGenerator 可以对接 stub provider 或 future provider。

谁会调用它：
- `backend/app/services/rag_answer_generator.py`

它调用谁：
- 不直接调用其他模块，只定义类型和协议。

输入是什么：
- `RAGPromptContext`

输出是什么：
- `LLMProviderOutput`

为什么需要这一层：
- 先固定 provider seam，再让 answer generator 只依赖一个可替换接口。

日本现场面试怎么讲：
- 这是未来 LLM provider 的契约层，当前只接 stub，不接真实外部模型。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from app.models.internal_rag import LLMUsageMetrics, RAGPromptContext
from app.schemas.internal_rag_api import InternalRagCitationResponse


@dataclass(frozen=True)
class LLMProviderOutput:
    """保存 provider 返回的回答草稿和占位 usage 数据。"""

    answer: str
    citations: list[InternalRagCitationResponse]
    usage: LLMUsageMetrics


@runtime_checkable
class LLMProvider(Protocol):
    """定义 future model provider 的最小可替换接口。"""

    name: str

    def generate(self, context: RAGPromptContext) -> LLMProviderOutput:
        """根据 prompt 上下文生成回答草稿。"""

        ...


__all__ = ["LLMProvider", "LLMProviderOutput", "LLMUsageMetrics", "RAGPromptContext"]
