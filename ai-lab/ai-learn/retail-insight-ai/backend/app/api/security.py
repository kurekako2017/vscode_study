from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.dependencies import get_security_service
from app.observability.logging import get_logger, get_request_id, log_event
from app.schemas.common import ApiResponse, success_response
from app.schemas.security_api import CurrentUserResponse, PermissionListResponse, RoleListResponse
from app.services.security_service import SecurityService

# security 路由负责当前用户快照、冻结角色目录和冻结权限目录。
router = APIRouter(prefix="/api/v1", tags=["security"])
logger = get_logger(__name__)


@router.get("/users/me", response_model=ApiResponse[CurrentUserResponse])
async def get_current_user(service: SecurityService = Depends(get_security_service)) -> ApiResponse[CurrentUserResponse]:
    """返回系统占位用户，后续可由真实认证 middleware 替换。"""

    user = service.get_current_user()
    log_event(
        logger,
        "info",
        "security_current_user_read",
        "Current user snapshot read",
        task_id=user.user_id,
        status=user.status.value,
    )
    return success_response(CurrentUserResponse.from_domain(user), get_request_id())


@router.get("/security/roles", response_model=ApiResponse[RoleListResponse])
async def get_roles(service: SecurityService = Depends(get_security_service)) -> ApiResponse[RoleListResponse]:
    """返回冻结角色目录，供未来 RBAC 和审计界面直接读取。"""

    roles = service.list_roles()
    log_event(
        logger,
        "info",
        "security_role_catalog_read",
        "Role catalog read",
        status="success",
    )
    return success_response(RoleListResponse.from_domain(roles), get_request_id())


@router.get("/security/permissions", response_model=ApiResponse[PermissionListResponse])
async def get_permissions(
    service: SecurityService = Depends(get_security_service),
) -> ApiResponse[PermissionListResponse]:
    """返回冻结权限目录，方便前端或未来治理工具展示。"""

    permissions = service.list_permissions()
    log_event(
        logger,
        "info",
        "security_permission_catalog_read",
        "Permission catalog read",
        status="success",
    )
    return success_response(PermissionListResponse.from_domain(permissions), get_request_id())

