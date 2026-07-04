from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_approval_service
from app.observability.logging import get_request_id
from app.schemas.approval_api import (
    ApprovalListResponse,
    ApprovalRejectRequest,
    ApprovalResponse,
    ApprovalRevisionResponse,
    ApprovalReviseRequest,
    ApprovalSubmitRequest,
)
from app.schemas.common import ApiResponse, success_response
from app.models.report import ReportStatus
from app.services.approval_service import ApprovalService

router = APIRouter(prefix="/api/v1", tags=["approvals"])


@router.post(
    "/reports/{task_id}/submit-approval",
    response_model=ApiResponse[ApprovalResponse],
    status_code=status.HTTP_201_CREATED,
)
async def submit_approval(
    task_id: str,
    payload: ApprovalSubmitRequest,
    service: ApprovalService = Depends(get_approval_service),
) -> ApiResponse[ApprovalResponse]:
    """创建 pending approval 记录，并返回冻结的审批响应。"""

    data = ApprovalResponse.from_domain(service.submit_approval(task_id, payload.comment))
    return success_response(data, get_request_id())


@router.get(
    "/approvals",
    response_model=ApiResponse[ApprovalListResponse],
    status_code=status.HTTP_200_OK,
)
async def list_approvals(
    task_id: str | None = Query(default=None),
    status_filter: ReportStatus | None = Query(default=None, alias="status"),
    limit: int | None = Query(default=None, ge=1, le=100),
    cursor: str | None = Query(default=None),
    service: ApprovalService = Depends(get_approval_service),
) -> ApiResponse[ApprovalListResponse]:
    """列出审批记录，支持 task / status 过滤。"""

    data = ApprovalListResponse.from_domain(
        service.list_approvals(task_id=task_id, status=status_filter, limit=limit, cursor=cursor)
    )
    return success_response(data, get_request_id())


@router.get(
    "/approvals/{approval_id}",
    response_model=ApiResponse[ApprovalResponse],
    status_code=status.HTTP_200_OK,
)
async def get_approval(
    approval_id: str,
    service: ApprovalService = Depends(get_approval_service),
) -> ApiResponse[ApprovalResponse]:
    """读取一条审批记录。"""

    data = ApprovalResponse.from_domain(service.get_approval(approval_id))
    return success_response(data, get_request_id())


@router.post(
    "/approvals/{approval_id}/approve",
    response_model=ApiResponse[ApprovalResponse],
    status_code=status.HTTP_200_OK,
)
async def approve(
    approval_id: str,
    payload: ApprovalSubmitRequest,
    service: ApprovalService = Depends(get_approval_service),
) -> ApiResponse[ApprovalResponse]:
    """批准已提交的审批记录。"""

    data = ApprovalResponse.from_domain(service.approve(approval_id, payload.comment))
    return success_response(data, get_request_id())


@router.post(
    "/approvals/{approval_id}/reject",
    response_model=ApiResponse[ApprovalResponse],
    status_code=status.HTTP_200_OK,
)
async def reject(
    approval_id: str,
    payload: ApprovalRejectRequest,
    service: ApprovalService = Depends(get_approval_service),
) -> ApiResponse[ApprovalResponse]:
    """拒绝已提交的审批记录。"""

    data = ApprovalResponse.from_domain(service.reject(approval_id, payload.reason))
    return success_response(data, get_request_id())


@router.post(
    "/reports/{task_id}/revise",
    response_model=ApiResponse[ApprovalRevisionResponse],
    status_code=status.HTTP_201_CREATED,
)
async def revise(
    task_id: str,
    payload: ApprovalReviseRequest,
    service: ApprovalService = Depends(get_approval_service),
) -> ApiResponse[ApprovalRevisionResponse]:
    """基于 rejected report 创建新的 immutable revision。"""

    data = service.revise(task_id, payload.revision_reason)
    return success_response(data, get_request_id())
