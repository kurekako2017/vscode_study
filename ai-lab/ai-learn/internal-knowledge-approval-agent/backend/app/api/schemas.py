"""HTTP API 的 Pydantic 请求/响应合同。

文件职责：集中定义参数校验、成功响应、错误响应和对外字段。
谁调用它：API Route 用这些模型接收请求并生成 OpenAPI Schema；Frontend 按相同字段消费。
它调用谁：只依赖 Pydantic，不访问 Service、Workflow 或数据库。
输入：HTTP JSON 数据或业务字典；输出：经过校验、可序列化的 API 模型。
为什么需要这一层：把外部合同与数据库字典隔离，避免内部字段无意暴露。
初学者重点：区分 ``QuestionCreateRequest``（输入）和各 ``*Response``（输出）。
日本现场面试：可说明 typed contract 能提前发现字段错误并统一 OpenAPI 文档。
企业级替换：可增加版本化 Schema、分页和字段级权限，但不应直接返回 ORM 实体。
"""

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
