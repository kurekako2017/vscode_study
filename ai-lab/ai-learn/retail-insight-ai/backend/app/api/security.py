"""Security Read API。

文件职责：返回 JWT 认证后的 Current User，并保留既有角色/权限目录读接口。
谁调用它：Swagger 或其他 HTTP 客户端。
它调用谁：CurrentUser Dependency 与既有 SecurityService 目录读取方法。
输入：Bearer JWT；目录接口无额外业务输入。
输出：统一 CurrentUser / Role / Permission response envelope。
设计理由：身份来自 Authentication，权限目录继续独立，避免在 JWT 中写权限逻辑。
日本现场面试：本轮只替换 current-user seam，不扩展或修改 RBAC 判定。
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.dependencies import get_security_service
from app.observability.logging import get_logger, get_request_id, log_event
from app.schemas.common import ApiResponse, success_response
from app.schemas.security_api import CurrentUserResponse, PermissionListResponse, RoleListResponse
from app.services.security_service import SecurityService
from app.security.contracts import CurrentUser
from app.security.dependencies import get_current_user as get_authenticated_user

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
