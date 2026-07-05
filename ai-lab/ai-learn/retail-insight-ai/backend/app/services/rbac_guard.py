"""Reusable RBAC guard for approval and future backend authorization checks.

文件职责：
- 把 permission / role / multi-permission 判定收敛到一个可注入的 guard。
- 在拒绝时自动写入 append-only audit fact，再返回统一的 permission_denied 错误。
- 保留 current user 来源为 SecurityService.get_current_user()。

谁会调用它：
- approval 路由依赖、未来需要统一授权的 backend 路由和测试。

它调用谁：
- SecurityService 读取 current user 和基础角色/权限判定。
- AuditService 追加拒绝审计事实。
- 统一错误和日志辅助函数。
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from app.errors.exceptions import PermissionDeniedException
from app.models.audit import AuditLogResult
from app.models.security import User
from app.observability.logging import get_logger, get_request_id, log_event
from app.services.audit_service import AuditService
from app.services.security_service import SecurityService

logger = get_logger(__name__)


@dataclass(frozen=True)
class RBACRequirement:
    """描述一条可复用的授权要求。"""

    permission: str | None = None
    permissions: tuple[str, ...] = ()
    role: str | None = None
    roles: tuple[str, ...] = ()
    require_all_permissions: bool = True
    require_all_roles: bool = False


class RBACGuard:
    """聚合 permission / role 判定、审计和统一拒绝响应。"""

    def __init__(
        self, security_service: SecurityService, audit_service: AuditService
    ) -> None:
        self._security_service = security_service
        self._audit_service = audit_service

    def allows(
        self,
        user: User | None = None,
        *,
        permission: str | None = None,
        permissions: Iterable[str] = (),
        role: str | None = None,
        roles: Iterable[str] = (),
        require_all_permissions: bool = True,
        require_all_roles: bool = False,
    ) -> bool:
        """判断当前主体是否满足任意一种授权要求。"""

        current_user = user or self._security_service.get_current_user()
        requirement = self._normalize_requirement(
            permission=permission,
            permissions=permissions,
            role=role,
            roles=roles,
            require_all_permissions=require_all_permissions,
            require_all_roles=require_all_roles,
        )
        if self._security_service.is_admin(current_user):
            return True
        if (
            not requirement.permissions
            and not requirement.roles
            and requirement.permission is None
            and requirement.role is None
        ):
            return True

        permission_allowed = True
        if requirement.permission is not None:
            permission_allowed = self._security_service.has_permission(
                current_user, requirement.permission
            )
        if requirement.permissions:
            permission_allowed = self._security_service.has_permissions(
                current_user,
                requirement.permissions,
                require_all=requirement.require_all_permissions,
            )
        role_allowed = True
        if requirement.role is not None:
            role_allowed = self._security_service.has_role(
                current_user, requirement.role
            )
        if requirement.roles:
            role_allowed = self._security_service.has_roles(
                current_user,
                requirement.roles,
                require_all=requirement.require_all_roles,
            )

        if requirement.permissions and requirement.roles:
            return permission_allowed or role_allowed
        return permission_allowed and role_allowed

    def require(
        self,
        *,
        permission: str | None = None,
        permissions: Iterable[str] = (),
        role: str | None = None,
        roles: Iterable[str] = (),
        action: str,
        resource_type: str,
        resource_id: str,
        require_all_permissions: bool = True,
        require_all_roles: bool = False,
    ) -> User:
        """校验当前主体；拒绝时自动记录审计事实并抛出 403。"""

        user = self._security_service.get_current_user()
        requirement = self._normalize_requirement(
            permission=permission,
            permissions=permissions,
            role=role,
            roles=roles,
            require_all_permissions=require_all_permissions,
            require_all_roles=require_all_roles,
        )
        if self.allows(
            user,
            permission=requirement.permission,
            permissions=requirement.permissions,
            role=requirement.role,
            roles=requirement.roles,
            require_all_permissions=requirement.require_all_permissions,
            require_all_roles=requirement.require_all_roles,
        ):
            return user

        request_id = get_request_id()
        required_permission = self._describe_requirement(requirement)
        self._audit_service.record_audit_log(
            operation_type="security.permission.denied",
            actor_id=user.user_id,
            organization_id=user.organization.organization_id,
            department_id=user.department.department_id,
            resource_type=resource_type,
            resource_id=resource_id,
            result=AuditLogResult.DENIED,
            request_id=request_id,
            trace_id=request_id,
            metadata={
                "action": action,
                "required_permission": required_permission,
                "required_permissions": list(requirement.permissions),
                "required_role": requirement.role,
                "required_roles": list(requirement.roles),
                "require_all_permissions": requirement.require_all_permissions,
                "require_all_roles": requirement.require_all_roles,
                "current_roles": list(user.roles),
            },
            error_code="permission_denied",
        )
        log_event(
            logger,
            "warning",
            "security_permission_denied",
            "Permission denied",
            request_id=request_id,
            task_id=resource_id,
            error_code="permission_denied",
            status="denied",
        )
        raise PermissionDeniedException(
            required_permission,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            detail={
                "required_permissions": list(requirement.permissions),
                "required_role": requirement.role,
                "required_roles": list(requirement.roles),
                "require_all_permissions": requirement.require_all_permissions,
                "require_all_roles": requirement.require_all_roles,
            },
        )

    def _normalize_requirement(
        self,
        *,
        permission: str | None,
        permissions: Iterable[str],
        role: str | None,
        roles: Iterable[str],
        require_all_permissions: bool,
        require_all_roles: bool,
    ) -> RBACRequirement:
        """把调用侧传入的参数标准化为冻结的授权要求。"""

        normalized_permissions = self._unique_values((permission, *permissions))
        normalized_roles = self._unique_values((role, *roles))
        primary_permission = (
            normalized_permissions[0] if normalized_permissions else None
        )
        primary_role = normalized_roles[0] if normalized_roles else None
        return RBACRequirement(
            permission=primary_permission,
            permissions=normalized_permissions,
            role=primary_role,
            roles=normalized_roles,
            require_all_permissions=require_all_permissions,
            require_all_roles=require_all_roles,
        )

    def _unique_values(self, values: Iterable[str | None]) -> tuple[str, ...]:
        """去重并保留顺序，避免重复权限影响日志和判定。"""

        unique_values: list[str] = []
        for value in values:
            if value is None:
                continue
            if value not in unique_values:
                unique_values.append(value)
        return tuple(unique_values)

    def _describe_requirement(self, requirement: RBACRequirement) -> str:
        """给拒绝错误提供一个可读的主要求字符串。"""

        permission_parts = self._unique_values(
            (requirement.permission, *requirement.permissions)
        )
        role_parts = self._unique_values((requirement.role, *requirement.roles))
        if permission_parts and role_parts:
            return (
                f"permissions={','.join(permission_parts)};roles={','.join(role_parts)}"
            )
        if permission_parts:
            return ",".join(permission_parts)
        if role_parts:
            return f"role={','.join(role_parts)}"
        return "access"


__all__ = ["RBACGuard", "RBACRequirement"]
