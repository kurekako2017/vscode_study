from __future__ import annotations

from typing import Any, Generic, Literal, TypeVar

from pydantic import BaseModel, Field


T = TypeVar("T")


class ApiError(BaseModel):
    code: str
    message: str
    detail: dict[str, Any] = {}


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    request_id: str
    data: T | None
    error: ApiError | None


class QuestionCreateRequest(BaseModel):
    question: str = Field(min_length=2, max_length=1000)


class QuestionResponse(BaseModel):
    question_id: str
    status: str
    risk_level: str | None = None
    approval_id: str | None = None
    error_code: str | None = None
    created_at: str
    updated_at: str


class ApprovalResponse(BaseModel):
    approval_id: str
    question_id: str
    question: str
    risk_level: str | None
    status: Literal["pending", "approved", "rejected"]
    created_at: str
    decided_at: str | None


class ReportResponse(BaseModel):
    question_id: str
    report: str
    risk_level: str
    created_at: str
    updated_at: str


def success(data: T, request_id: str) -> ApiResponse[T]:
    return ApiResponse(success=True, request_id=request_id, data=data, error=None)

