"""Current User 与 Enterprise RBAC Catalog API。

文件职责：返回 JWT 认证后的 Current User，并保留既有角色/权限目录读接口。
谁调用它：Swagger 或其他 HTTP 客户端。
它调用谁：CurrentUser Dependency、Permission Dependency 与 AuthorizationService。
输入：Bearer JWT；目录接口无额外业务输入。
输出：统一 CurrentUser / Role / Permission response envelope。
设计理由：身份来自 Authentication，角色/权限目录来自服务端 Registry，不写进 JWT。
日本现场面试：安全目录本身也受 security.manage 保护，users/me 只要求认证。
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.observability.logging import get_logger, get_request_id, log_event
from app.schemas.common import ApiResponse, success_response
from app.schemas.security_api import CurrentUserResponse, PermissionListResponse, RoleListResponse
from app.security.authorization_service import AuthorizationService
from app.security.contracts import CurrentUser
from app.security.dependencies import (
    get_authorization_service,
    get_current_user as get_authenticated_user,
    require_permission,
)
from app.security.rbac_contracts import Permission
from app.api.persistent_audit import persistent_audit_dependency
from app.services.persistent_audit_service import PersistentAuditSpec

# security 路由。
router = APIRouter(prefix="/api/v1", tags=["security"])
logger = get_logger(__name__)


@router.get("/users/me", response_model=ApiResponse[CurrentUserResponse])
async def read_current_user(
    current_user: CurrentUser = Depends(get_authenticated_user),
) -> ApiResponse[CurrentUserResponse]:
    """返回 JWT Dependency 已认证的当前用户，不执行权限判断。"""

    log_event(
        logger,
        "info",
        "security_current_user_read",
        "Current user snapshot read",
        task_id=current_user.user_id,
        status="authenticated",
    )
    return success_response(
        CurrentUserResponse.from_current_user(current_user), get_request_id()
    )


@router.get(
    "/security/roles",
    response_model=ApiResponse[RoleListResponse],
    dependencies=[
        Depends(require_permission(Permission.SECURITY_MANAGE)),
        Depends(
            persistent_audit_dependency(
                PersistentAuditSpec(
                    action="security.manage",
                    resource_type="security_catalog",
                    resource_id="roles",
                    success_status_code=200,
                    permission=Permission.SECURITY_MANAGE.value,
                )
            )
        ),
    ],
)
async def get_roles(
    service: AuthorizationService = Depends(get_authorization_service),
) -> ApiResponse[RoleListResponse]:
    """返回当前集中 Role Mapping。"""

    roles = service.registry.list_role_mappings()
    log_event(
        logger,
        "info",
        "security_role_catalog_read",
        "Role catalog read",
        status="success",
    )
    return success_response(RoleListResponse.from_contract(roles), get_request_id())


@router.get(
    "/security/permissions",
    response_model=ApiResponse[PermissionListResponse],
    dependencies=[
        Depends(require_permission(Permission.SECURITY_MANAGE)),
        Depends(
            persistent_audit_dependency(
                PersistentAuditSpec(
                    action="security.manage",
                    resource_type="security_catalog",
                    resource_id="permissions",
                    success_status_code=200,
                    permission=Permission.SECURITY_MANAGE.value,
                )
            )
        ),
    ],
)
async def get_permissions(
    service: AuthorizationService = Depends(get_authorization_service),
) -> ApiResponse[PermissionListResponse]:
    """返回集中 Permission Registry，供治理工具展示。"""

    permissions = service.registry.list_permissions()
    log_event(
        logger,
        "info",
        "security_permission_catalog_read",
        "Permission catalog read",
        status="success",
    )
    return success_response(
        PermissionListResponse.from_contract(permissions), get_request_id()
    )
