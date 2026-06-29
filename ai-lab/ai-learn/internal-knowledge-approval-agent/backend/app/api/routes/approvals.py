"""人工审批 HTTP 接口。

文件职责：查询待审批项，并接收 Approve/Reject 操作。
谁调用它：React API Client；它通过 FastAPI Depends 调用 ``ApprovalService``。
输入：question_id 和审批动作；输出：统一包装的 ``ApprovalResponse``。
为什么需要这一层：Route 只做 HTTP 转换，审批有效性与 Workflow 恢复交给 Service。
初学者重点：观察 URL 中使用 question_id，而 Service 再定位 approval_id。
日本现场面试：可说明高风险操作由显式 Endpoint 进入并保留 409 冲突语义。
企业级替换：增加登录用户、RBAC、审批意见和幂等键，不能绕过 Service 直接写表。
"""

from typing import Any

from fastapi import APIRouter, Depends

from app.api.routes.dependencies import get_approval_service
from app.config.logging import get_request_id
from app.schemas import ApiResponse, ApprovalResponse, success
from app.services.approval_service import ApprovalService


router = APIRouter(prefix="/api/approvals")


def approval_response(item: dict[str, Any]) -> ApprovalResponse:
    return ApprovalResponse.model_validate(item)


@router.get("", response_model=ApiResponse[list[ApprovalResponse]])
async def list_approvals(
    service: ApprovalService = Depends(get_approval_service),
) -> ApiResponse[list[ApprovalResponse]]:
    return success([approval_response(item) for item in service.list_pending()], get_request_id())


@router.post("/{question_id}/approve", response_model=ApiResponse[ApprovalResponse])
async def approve(
    question_id: str,
    service: ApprovalService = Depends(get_approval_service),
) -> ApiResponse[ApprovalResponse]:
    request_id = get_request_id()
    return success(approval_response(await service.decide(question_id, "approved", request_id)), request_id)


@router.post("/{question_id}/reject", response_model=ApiResponse[ApprovalResponse])
async def reject(
    question_id: str,
    service: ApprovalService = Depends(get_approval_service),
) -> ApiResponse[ApprovalResponse]:
    request_id = get_request_id()
    return success(approval_response(await service.decide(question_id, "rejected", request_id)), request_id)
