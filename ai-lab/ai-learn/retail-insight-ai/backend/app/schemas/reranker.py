"""Reranker 内部合同。

文件职责：
- 保存原始 retrieval chunk，以及独立的 rerank_score、reason 和 metadata。
- 明确 reranker 只能附加排序事实，不能覆盖 chunk 内容或 retrieval score。

谁会调用它：
- `RerankerProvider` 产生评分结果。
- `RerankerService` 负责 Top-N、Top-K 与 fallback。

日本现场面试怎么讲：
- Retrieval score 是召回层事实，rerank score 是排序层事实；两个分数并存，便于审计和替换模型。
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.document_retrieval_api import DocumentRetrievalResultResponse


class RerankedDocumentChunk(BaseModel):
    """保存一条不改写原检索结果的 rerank 结果。"""

    model_config = ConfigDict(frozen=True)

    chunk: DocumentRetrievalResultResponse
    rerank_score: float | None = Field(default=None, ge=0.0, le=1.0)
    reason: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class RerankerOutcome(BaseModel):
    """返回最终 chunks，并显式说明 provider 是否执行或发生 fallback。"""

    model_config = ConfigDict(frozen=True)

    chunks: tuple[RerankedDocumentChunk, ...]
    provider_name: str | None
    used_provider: bool
    fallback_reason: Literal["none", "disabled", "missing_provider", "provider_error"] = "none"


__all__ = ["RerankedDocumentChunk", "RerankerOutcome"]
