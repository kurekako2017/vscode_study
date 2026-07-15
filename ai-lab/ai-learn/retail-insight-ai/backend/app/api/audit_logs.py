from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.dependencies import get_audit_service
from app.observability.logging import get_logger, get_request_id, log_event
from app.schemas.audit_api import AuditLogListResponse
from app.schemas.common import ApiResponse, success_response
from app.services.audit_service import AuditService
from app.security.dependencies import require_permission
from app.security.rbac_contracts import Permission

# audit_logs 路由只提供只读事实查询，不提供任何写接口。
router = APIRouter(
    prefix="/api/v1/audit-logs",
    tags=["audit"],
    dependencies=[Depends(require_permission(Permission.AUDIT_READ))],
)
logger = get_logger(__name__)


@router.get("", response_model=ApiResponse[AuditLogListResponse])
async def get_audit_logs(service: AuditService = Depends(get_audit_service)) -> ApiResponse[AuditLogListResponse]:
    """读取 append-only 审计事实列表。"""

    logs = service.list_audit_logs()
    log_event(
        logger,
        "info",
        "audit_log_list_read",
        "Audit log list read",
        status="success",
    )
    return success_response(AuditLogListResponse.from_domain(logs), get_request_id())
