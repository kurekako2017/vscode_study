"""`POST /api/v1/executive-reports` 的稳定 HTTP 合同。"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.ai_analysis_api import AIAnalysisCitationResponse, AIAnalysisUsageResponse


class ExecutiveReportRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ai_analysis_id: str = Field(min_length=1, max_length=128)
    title: str = Field(min_length=1, max_length=200)
    confirmed: bool
    task_id: str | None = Field(default=None, max_length=128)

    @field_validator("title")
    @classmethod
    def normalize_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("title must not be blank")
        return value

    @field_validator("ai_analysis_id")
    @classmethod
    def normalize_analysis_id(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("ai_analysis_id must not be blank")
        return value


class ExecutiveReportResponse(BaseModel):
    report_id: str
    report_version_id: str
    task_id: str
    title: str
    executive_summary: str
    kpi_findings: list[str]
    risks: list[str]
    recommendations: list[str]
    citations: list[AIAnalysisCitationResponse]
    provider: str
    model: str
    route_tier: str
    usage: AIAnalysisUsageResponse
    estimated_cost: Decimal
    actual_cost: Decimal
    currency: str
    status: str
    analysis_id: str
    usage_id: str
    created_at: datetime


__all__ = ["ExecutiveReportRequest", "ExecutiveReportResponse"]
