"""`POST /api/v1/ai-analysis` 的稳定 HTTP 合同。"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AIAnalysisEvidenceRefRequest(BaseModel):
    document_id: str = Field(min_length=1, max_length=128)
    chunk_id: str = Field(min_length=1, max_length=128)
    score: Decimal = Field(ge=0)


class AIAnalysisRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    question: str = Field(min_length=1, max_length=2000)
    evidence: list[AIAnalysisEvidenceRefRequest] = Field(min_length=1, max_length=20)
    confirmed: bool
    task_id: str | None = Field(default=None, max_length=128)

    @field_validator("question")
    @classmethod
    def normalize_question(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("question must not be blank")
        return value


class AIAnalysisCitationResponse(BaseModel):
    document_id: str
    chunk_id: str
    score: Decimal
    excerpt: str


class AIAnalysisUsageResponse(BaseModel):
    input_tokens: int
    output_tokens: int
    total_tokens: int


class AIAnalysisResponse(BaseModel):
    analysis_id: str
    answer: str
    citations: list[AIAnalysisCitationResponse]
    provider: str
    model: str
    usage: AIAnalysisUsageResponse
    cost: Decimal
    currency: str
    status: str
    created_at: datetime


__all__ = ["AIAnalysisRequest", "AIAnalysisResponse"]
