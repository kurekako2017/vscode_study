"""Schema 的稳定导出入口。

Route 从这里导入公开 API 模型，具体定义仍位于 ``app.api.schemas``。这样未来拆分文件时，
调用方不必同时修改；本模块不做校验或业务处理。
"""

from app.api.schemas import (
    ApiError,
    ApiResponse,
    ApprovalResponse,
    QuestionCreateRequest,
    QuestionResponse,
    ReportResponse,
    success,
)

__all__ = [
    "ApiError",
    "ApiResponse",
    "ApprovalResponse",
    "QuestionCreateRequest",
    "QuestionResponse",
    "ReportResponse",
    "success",
]
