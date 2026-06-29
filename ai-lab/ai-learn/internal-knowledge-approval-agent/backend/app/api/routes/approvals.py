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
