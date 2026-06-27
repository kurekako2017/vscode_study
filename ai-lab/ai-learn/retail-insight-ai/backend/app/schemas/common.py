"""普通 JSON API 共用的成功与失败响应结构。"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel

DataT = TypeVar("DataT")


class ApiError(BaseModel):
    """客户端可依赖的机器错误码、人类说明与安全详情。"""

    code: str
    message: str
    detail: dict[str, Any]


class ApiResponse(BaseModel, Generic[DataT]):
    """统一普通 JSON 端点的 envelope；SSE 不使用该结构。"""

    success: bool
    request_id: str
    data: DataT | None
    error: ApiError | None


def success_response(data: DataT, request_id: str) -> ApiResponse[DataT]:
    """创建成功 envelope，确保 data 与 error 不会同时出现。"""

    return ApiResponse(success=True, request_id=request_id, data=data, error=None)
