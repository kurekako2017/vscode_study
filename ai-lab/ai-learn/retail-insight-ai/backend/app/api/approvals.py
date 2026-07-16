from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

from fastapi import APIRouter, Depends, Query, Request, status

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
from app.services.persistent_audit_service import PersistentAuditContext
from app.security.contracts import CurrentUser
from app.security.dependencies import get_current_user
from app.security.errors import ForbiddenError

router = APIRouter(prefix="/api/v1", tags=["approvals"])
T = TypeVar("T")


def _approval_response(
    service: ApprovalService,
    approval: Any,
) -> ApprovalResponse:
    """详情与写操作返回 PostgreSQL 业务历史；InMemory 保持空 history。"""

    return ApprovalResponse.from_domain(
        approval,
        history=service.get_approval_history(approval.task_id),
    )


async def require_revision_owner_or_admin(
    task_id: str,
    request: Request,
    current_user: CurrentUser = Depends(get_current_user),
    service: ApprovalService = Depends(get_approval_service),
) -> CurrentUser:
    """把 submitter ownership 集中委托给 ApprovalService。

    该依赖位于 Persistent Audit operation 之前，ownership 拒绝只写一条
    authorization.denied，不会再产生同一动作的 failure 重复记录。
    """

    try:
        service.require_revision_access(task_id, current_user)
    except ForbiddenError:
        request.app.state.container.persistent_audit_service.record_authorization_denied(
            context=PersistentAuditContext(
                request_id=get_request_id(),
                http_method=request.method,
                api_path=request.url.path,
                resource_id=task_id,
                current_user=current_user,
            ),
            permission=Permission.APPROVAL_SUBMIT.value,
        )
        raise
    return current_user


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
    current_user: CurrentUser = Depends(get_current_user),
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
        operation=lambda: _approval_response(
            service,
            service.submit_approval(
                task_id,
                payload.comment,
                current_user=current_user,
            ),
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
        operation=lambda: _approval_response(
            service,
            service.get_approval(approval_id),
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
    current_user: CurrentUser = Depends(get_current_user),
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
        operation=lambda: _approval_response(
            service,
            service.approve(
                approval_id,
                payload.comment,
                current_user=current_user,
            ),
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
    current_user: CurrentUser = Depends(get_current_user),
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
        operation=lambda: _approval_response(
            service,
            service.reject(
                approval_id,
                payload.reason,
                current_user=current_user,
            ),
        ),
        metadata={"approval_id": approval_id},
    )
    return success_response(data, get_request_id())


@router.post(
    "/reports/{task_id}/revise",
    response_model=ApiResponse[ApprovalRevisionResponse],
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(require_permission(Permission.APPROVAL_SUBMIT)),
        Depends(require_revision_owner_or_admin),
        Depends(
            persistent_audit_dependency(
                PersistentAuditSpec(
                    action="approval.revised",
                    resource_type="report",
                    resource_id_param="task_id",
                    success_status_code=status.HTTP_201_CREATED,
                    permission=Permission.APPROVAL_SUBMIT.value,
                )
            )
        ),
    ],
)
async def revise(
    task_id: str,
    payload: ApprovalReviseRequest,
    current_user: CurrentUser = Depends(get_current_user),
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
        operation=lambda: service.revise(
            task_id,
            payload.revision_reason,
            markdown=payload.markdown,
            current_user=current_user,
        ),
        metadata={"task_id": task_id},
    )
    return success_response(data, get_request_id())


@router.post(
    "/reports/{task_id}/resubmit-approval",
    response_model=ApiResponse[ApprovalResponse],
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(require_permission(Permission.APPROVAL_SUBMIT)),
        Depends(require_revision_owner_or_admin),
        Depends(
            persistent_audit_dependency(
                PersistentAuditSpec(
                    action="approval.resubmitted",
                    resource_type="report",
                    resource_id_param="task_id",
                    success_status_code=status.HTTP_201_CREATED,
                    permission=Permission.APPROVAL_SUBMIT.value,
                )
            )
        ),
    ],
)
async def resubmit_approval(
    task_id: str,
    payload: ApprovalSubmitRequest,
    current_user: CurrentUser = Depends(get_current_user),
    audit_middleware: AuditMiddleware = Depends(get_audit_middleware),
    service: ApprovalService = Depends(get_approval_service),
) -> ApiResponse[ApprovalResponse]:
    """将 rejected 后产生的 revised version 重新送审，不复制报告版本。"""

    data = await _run_audited_operation(
        audit_middleware=audit_middleware,
        operation_type="approval.resubmitted",
        resource_type="report",
        resource_id=task_id,
        action="resubmit_approval",
        permission="report.submit_approval",
        operation=lambda: _approval_response(
            service,
            service.resubmit(
                task_id,
                payload.comment,
                current_user=current_user,
            ),
        ),
        metadata={"task_id": task_id},
    )
    return success_response(data, get_request_id())
