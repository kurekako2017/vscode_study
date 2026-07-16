from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_audit_service
from app.observability.logging import get_logger, get_request_id, log_event
from app.schemas.audit_api import AuditLogListResponse, AuditLogQuery
from app.schemas.common import ApiResponse, success_response
from app.services.audit_service import AuditService
from app.security.dependencies import require_permission
from app.security.rbac_contracts import Permission
from app.api.persistent_audit import persistent_audit_dependency
from app.services.persistent_audit_service import PersistentAuditSpec

# audit_logs 路由只提供只读事实查询，不提供任何写接口。
router = APIRouter(
    prefix="/api/v1/audit-logs",
    tags=["audit"],
    dependencies=[Depends(require_permission(Permission.AUDIT_READ))],
)
logger = get_logger(__name__)


@router.get(
    "",
    response_model=ApiResponse[AuditLogListResponse],
    dependencies=[
        Depends(
            persistent_audit_dependency(
                PersistentAuditSpec(
                    action="audit.read",
                    resource_type="audit_log",
                    resource_id="audit-logs",
                    success_status_code=200,
                    permission=Permission.AUDIT_READ.value,
                )
            )
        )
    ],
)
async def get_audit_logs(
    query: Annotated[AuditLogQuery, Query()],
    service: AuditService = Depends(get_audit_service),
) -> ApiResponse[AuditLogListResponse]:
    """读取 append-only 审计事实列表。"""

    page = service.query_audit_logs(query.to_domain())
    log_event(
        logger,
        "info",
        "audit_log_list_read",
        "Audit log list read",
        status="success",
    )
    return success_response(AuditLogListResponse.from_page(page), get_request_id())
