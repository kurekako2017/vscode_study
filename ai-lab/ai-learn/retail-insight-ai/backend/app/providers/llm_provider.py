"""LLMProvider 的稳定接口与输出模型。

文件职责：
- 冻结 Provider 接口形状，供 Gateway 与 Stub 使用。
- analyze / generate_report 只允许经 LLMGatewayService 调用。

谁会调用它：
- LLMGatewayService（唯一生产调用方）

设计理由：
- 先固定 provider seam，再让业务服务只依赖 Gateway。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from app.models.ai_analysis import (
    LLMAnalysisInput,
    LLMProviderResult,
    LLMReportInput,
    LLMReportResult,
)
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
    """定义 model provider 的最小可替换接口。"""

    provider_name: str
    model_name: str

    def analyze(self, request: LLMAnalysisInput) -> LLMProviderResult:
        """只由 LLMGatewayService 在预占成功后显式调用。"""

        ...

    def generate_report(self, request: LLMReportInput) -> LLMReportResult:
        """只由 LLMGatewayService 在 high_quality 路由上调用。"""

        ...

    def generate(self, context: RAGPromptContext) -> LLMProviderOutput:
        """旧 RAG seam；普通 Internal RAG 不得进入此路径。"""

        ...


__all__ = ["LLMProvider", "LLMProviderOutput", "LLMUsageMetrics", "RAGPromptContext"]
