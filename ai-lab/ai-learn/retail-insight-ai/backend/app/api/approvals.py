from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_approval_service, get_audit_middleware
from app.models.report import ReportStatus
from app.observability.logging import get_request_id
from app.schemas.approval_api import (
    ApprovalListResponse,
    ApprovalRejectRequest,
    ApprovalResponse,
    ApprovalReviseRequest,
    ApprovalRevisionResponse,
    ApprovalSubmitRequest,
)
from app.schemas.common import ApiResponse, success_response
from app.services.approval_service import ApprovalService
from app.services.audit_middleware import AuditAction, AuditMiddleware
from app.security.dependencies import require_permission
from app.security.rbac_contracts import Permission
from app.api.persistent_audit import persistent_audit_dependency
from app.services.persistent_audit_service import PersistentAuditSpec

router = APIRouter(prefix="/api/v1", tags=["approvals"])
T = TypeVar("T")


async def _run_audited_operation(
    *,
    audit_middleware: AuditMiddleware,
    operation_type: str,
    resource_type: str,
    resource_id: str,
    action: str,
    permission: str,
    operation: Callable[[], T | Awaitable[T]],
    metadata: dict[str, Any] | None = None,
) -> T:
    """把 approval 的授权和审计统一收敛到一个执行入口。"""

    return await audit_middleware.run(
        action=AuditAction(
            operation_type=operation_type,
            resource_type=resource_type,
            resource_id=resource_id,
            action=action,
            metadata=metadata or {},
            permission=permission,
        ),
        operation=operation,
    )


@router.post(
    "/reports/{task_id}/submit-approval",
    response_model=ApiResponse[ApprovalResponse],
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(require_permission(Permission.APPROVAL_SUBMIT)),
        Depends(
            persistent_audit_dependency(
                PersistentAuditSpec(
                    action="approval.submitted",
                    resource_type="report",
                    resource_id_param="task_id",
                    success_status_code=status.HTTP_201_CREATED,
                    permission=Permission.APPROVAL_SUBMIT.value,
                )
            )
        ),
    ],
)
async def submit_approval(
    task_id: str,
    payload: ApprovalSubmitRequest,
    audit_middleware: AuditMiddleware = Depends(get_audit_middleware),
    service: ApprovalService = Depends(get_approval_service),
) -> ApiResponse[ApprovalResponse]:
    """创建 pending approval 记录，并返回冻结的审批响应。"""

    data = await _run_audited_operation(
        audit_middleware=audit_middleware,
        operation_type="approval.submitted",
        resource_type="report",
        resource_id=task_id,
        action="submit_approval",
        permission="report.submit_approval",
        operation=lambda: ApprovalResponse.from_domain(
            service.submit_approval(task_id, payload.comment)
        ),
        metadata={"task_id": task_id},
    )
    return success_response(data, get_request_id())


@router.get(
    "/approvals",
    response_model=ApiResponse[ApprovalListResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(require_permission(Permission.APPROVAL_REVIEW)),
        Depends(
            persistent_audit_dependency(
                PersistentAuditSpec(
                    action="approval.listed",
                    resource_type="approval_collection",
                    resource_id="all",
                    success_status_code=status.HTTP_200_OK,
                    permission=Permission.APPROVAL_REVIEW.value,
                )
            )
        ),
    ],
)
async def list_approvals(
    task_id: str | None = Query(default=None),
    status_filter: ReportStatus | None = Query(default=None, alias="status"),
    limit: int | None = Query(default=None, ge=1, le=100),
    cursor: str | None = Query(default=None),
    audit_middleware: AuditMiddleware = Depends(get_audit_middleware),
    service: ApprovalService = Depends(get_approval_service),
) -> ApiResponse[ApprovalListResponse]:
    """列出审批记录，支持 task / status 过滤。"""

    resource_id = task_id or "all"
    data = await _run_audited_operation(
        audit_middleware=audit_middleware,
        operation_type="approval.listed",
        resource_type="approval_collection",
        resource_id=resource_id,
        action="list_approvals",
        permission="approval.review",
        operation=lambda: ApprovalListResponse.from_domain(
            service.list_approvals(
                task_id=task_id, status=status_filter, limit=limit, cursor=cursor
            )
        ),
        metadata={
            "task_id": task_id,
            "status": status_filter.value if status_filter is not None else None,
            "limit": limit,
            "cursor": cursor,
        },
    )
    return success_response(data, get_request_id())


@router.get(
    "/approvals/{approval_id}",
    response_model=ApiResponse[ApprovalResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(require_permission(Permission.APPROVAL_REVIEW)),
        Depends(
            persistent_audit_dependency(
                PersistentAuditSpec(
                    action="approval.read",
                    resource_type="approval",
                    resource_id_param="approval_id",
                    success_status_code=status.HTTP_200_OK,
                    permission=Permission.APPROVAL_REVIEW.value,
                )
            )
        ),
    ],
)
async def get_approval(
    approval_id: str,
    audit_middleware: AuditMiddleware = Depends(get_audit_middleware),
    service: ApprovalService = Depends(get_approval_service),
) -> ApiResponse[ApprovalResponse]:
    """读取一条审批记录。"""

    data = await _run_audited_operation(
        audit_middleware=audit_middleware,
        operation_type="approval.read",
        resource_type="approval",
        resource_id=approval_id,
        action="get_approval",
        permission="approval.review",
        operation=lambda: ApprovalResponse.from_domain(
            service.get_approval(approval_id)
        ),
        metadata={"approval_id": approval_id},
    )
    return success_response(data, get_request_id())


@router.post(
    "/approvals/{approval_id}/approve",
    response_model=ApiResponse[ApprovalResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(require_permission(Permission.APPROVAL_ADMIN)),
        Depends(
            persistent_audit_dependency(
                PersistentAuditSpec(
                    action="approval.approved",
                    resource_type="approval",
                    resource_id_param="approval_id",
                    success_status_code=status.HTTP_200_OK,
                    permission=Permission.APPROVAL_ADMIN.value,
                )
            )
        ),
    ],
)
async def approve(
    approval_id: str,
    payload: ApprovalSubmitRequest,
    audit_middleware: AuditMiddleware = Depends(get_audit_middleware),
    service: ApprovalService = Depends(get_approval_service),
) -> ApiResponse[ApprovalResponse]:
    """批准已提交的审批记录。"""

    data = await _run_audited_operation(
        audit_middleware=audit_middleware,
        operation_type="approval.approved",
        resource_type="approval",
        resource_id=approval_id,
        action="approve_approval",
        permission="approval.approve",
        operation=lambda: ApprovalResponse.from_domain(
            service.approve(approval_id, payload.comment)
        ),
        metadata={"approval_id": approval_id},
    )
    return success_response(data, get_request_id())


@router.post(
    "/approvals/{approval_id}/reject",
    response_model=ApiResponse[ApprovalResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(require_permission(Permission.APPROVAL_ADMIN)),
        Depends(
            persistent_audit_dependency(
                PersistentAuditSpec(
                    action="approval.rejected",
                    resource_type="approval",
                    resource_id_param="approval_id",
                    success_status_code=status.HTTP_200_OK,
                    permission=Permission.APPROVAL_ADMIN.value,
                )
            )
        ),
    ],
)
async def reject(
    approval_id: str,
    payload: ApprovalRejectRequest,
    audit_middleware: AuditMiddleware = Depends(get_audit_middleware),
    service: ApprovalService = Depends(get_approval_service),
) -> ApiResponse[ApprovalResponse]:
    """拒绝已提交的审批记录。"""

    data = await _run_audited_operation(
        audit_middleware=audit_middleware,
        operation_type="approval.rejected",
        resource_type="approval",
        resource_id=approval_id,
        action="reject_approval",
        permission="approval.reject",
        operation=lambda: ApprovalResponse.from_domain(
            service.reject(approval_id, payload.reason)
        ),
        metadata={"approval_id": approval_id},
    )
    return success_response(data, get_request_id())


@router.post(
    "/reports/{task_id}/revise",
    response_model=ApiResponse[ApprovalRevisionResponse],
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(require_permission(Permission.APPROVAL_ADMIN)),
        Depends(
            persistent_audit_dependency(
                PersistentAuditSpec(
                    action="approval.revised",
                    resource_type="report",
                    resource_id_param="task_id",
                    success_status_code=status.HTTP_201_CREATED,
                    permission=Permission.APPROVAL_ADMIN.value,
                )
            )
        ),
    ],
)
async def revise(
    task_id: str,
    payload: ApprovalReviseRequest,
    audit_middleware: AuditMiddleware = Depends(get_audit_middleware),
    service: ApprovalService = Depends(get_approval_service),
) -> ApiResponse[ApprovalRevisionResponse]:
    """基于 rejected report 创建新的 immutable revision。"""

    data = await _run_audited_operation(
        audit_middleware=audit_middleware,
        operation_type="approval.revised",
        resource_type="report",
        resource_id=task_id,
        action="revise_approval",
        permission="approval.revise",
        operation=lambda: service.revise(task_id, payload.revision_reason),
        metadata={"task_id": task_id},
    )
    return success_response(data, get_request_id())
