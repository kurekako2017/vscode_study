"""Internal RAG API 的请求/响应 schema。

文件职责：
- 定义 `POST /api/v1/internal-rag/answer` 的冻结请求与响应合同。
- 把 answer assembly、citation 输出和 confidence 字段固定在一个独立层。

谁会调用它：
- `backend/app/api/internal_rag.py` 路由。
- `backend/app/services/internal_rag_service.py` 服务层。
- internal RAG 相关测试。

它调用谁：
- 只依赖 Pydantic 和文档检索相关的公开 schema，不依赖 repository 或 LLM。

输入是什么：
- question、limit、include_archived、document_type、language、tags、answer_mode、require_citations。

输出是什么：
- 结构化 answer、citations、retrieval_mode、answer_mode、confidence、warnings。

为什么需要这一层：
- internal RAG 是 retrieval 之后、approval 之前的稳定边界，必须把对外字段先冻结。

日本现场面试怎么讲：
- 这是 grounded answer 的 HTTP 合同层，未来即使接入真正的 LLM provider，外部字段也不需要改。
"""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.schemas.document_api import DocumentSourceResponse
from app.models.document import DocumentType, Language


class InternalRagAnswerMode(StrEnum):
    """定义 internal RAG 冻结的回答模式。"""

    EXTRACTIVE = "extractive"
    SUMMARY = "summary"


class InternalRagAnswerRequest(BaseModel):
    """冻结 `POST /api/v1/internal-rag/answer` 的请求结构。"""

    question: str
    limit: int = Field(default=5, ge=1, le=100)
    include_archived: bool = False
    document_type: DocumentType | None = None
    language: Language | None = None
    tags: list[str] | None = None
    answer_mode: InternalRagAnswerMode
    require_citations: bool = True
    retrieval_mode: Literal["keyword", "vector", "hybrid"] = "keyword"

    @field_validator("question")
    @classmethod
    def _normalize_question(cls, value: str) -> str:
        """保留原始 question 文本，但去掉首尾空白，方便 service 层做语义判断。"""

        return value.strip()

    @field_validator("tags")
    @classmethod
    def _normalize_tags(cls, value: list[str] | None) -> list[str] | None:
        """只允许非空标签，避免把无意义字符串送进检索边界。"""

        if value is None:
            return None
        normalized: list[str] = []
        for tag in value:
            if not isinstance(tag, str) or not tag.strip():
                raise ValueError("tags must contain non-empty strings")
            normalized.append(tag.strip())
        return normalized


class InternalRagCitationResponse(BaseModel):
    """单条 grounded citation，必须与回答片段一一对应。"""

    document_id: str
    chunk_id: str
    chunk_index: int
    excerpt: str
    source: DocumentSourceResponse
    score: float


class InternalRagAnswerResponse(BaseModel):
    """冻结 internal RAG 成功响应。"""

    answer: str
    citations: list[InternalRagCitationResponse]
    retrieval_mode: Literal["keyword", "vector", "hybrid"] = "keyword"
    answer_mode: InternalRagAnswerMode
    confidence: float
    warnings: list[str] = Field(default_factory=list)


__all__ = [
    "InternalRagAnswerMode",
    "InternalRagAnswerRequest",
    "InternalRagAnswerResponse",
    "InternalRagCitationResponse",
]
