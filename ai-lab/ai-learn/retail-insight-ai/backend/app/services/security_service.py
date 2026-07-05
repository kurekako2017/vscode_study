"""Security service.

文件职责：
- 提供当前用户快照、冻结角色目录与冻结权限目录。
- 作为 users/me、roles、permissions 这些只读安全 API 的稳定业务层。

谁会调用它：
- `backend/app/api/security.py` 路由和对应测试。

它调用谁：
- 只读取本地冻结目录，不依赖认证 provider 或数据库。

输入是什么：
- 不需要外部输入；当前阶段是静态目录和 placeholder principal。

输出是什么：
- 当前用户、角色列表、权限列表。

为什么需要这一层：
- 路由不应该直接硬编码目录；把目录集中在 service 里更容易后续替换成数据库。

日本现场面试怎么讲：
- 这是 security foundation 的 read seam，先用静态目录把 contract 跑通，未来再接认证和 RBAC。
"""

from __future__ import annotations

from app.models.security import (
    Department,
    Organization,
    Permission,
    Policy,
    PolicyEffect,
    Role,
    User,
    UserStatus,
)
from app.services.audit_service import AuditService

_ORGANIZATION = Organization(
    organization_id="org-system",
    name="system",
    display_name="System Organization",
)
_DEPARTMENT = Department(
    department_id="dept-system",
    organization_id=_ORGANIZATION.organization_id,
    name="system",
    display_name="System Department",
)
_FROZEN_PERMISSIONS: tuple[Permission, ...] = (
    Permission(
        "system.admin", "Manage platform settings and privileged operations.", "system"
    ),
    Permission("document.read", "Read documents and document metadata.", "document"),
    Permission(
        "document.upload",
        "Upload documents into the local document pipeline.",
        "document",
    ),
    Permission(
        "document.archive", "Archive a document without deleting facts.", "document"
    ),
    Permission("document.import", "Run the document import pipeline.", "document"),
    Permission("document.chunk", "Generate or refresh document chunks.", "document"),
    Permission(
        "document.search", "Search document chunks and retrieval results.", "document"
    ),
    Permission(
        "rag.answer", "Generate grounded RAG answers from retrieved evidence.", "rag"
    ),
    Permission("report.read", "Read analysis reports and report versions.", "report"),
    Permission("report.submit_approval", "Submit a report for approval.", "report"),
    Permission("approval.review", "Review pending approval requests.", "approval"),
    Permission("approval.approve", "Approve a pending report revision.", "approval"),
    Permission("approval.reject", "Reject a pending report revision.", "approval"),
    Permission("approval.revise", "Revise a report version snapshot.", "approval"),
    Permission("audit.read", "Read append-only audit logs.", "audit"),
)
_ALL_PERMISSION_NAMES = tuple(
    permission.permission for permission in _FROZEN_PERMISSIONS
)
_ALL_ROLES: tuple[Role, ...] = (
    Role(
        role="admin",
        description="Full platform administration access.",
        permissions=_ALL_PERMISSION_NAMES,
    ),
    Role(
        role="manager",
        description="Manages approvals and reviews operational reports.",
        permissions=(
            "document.read",
            "report.read",
            "report.submit_approval",
            "approval.review",
            "approval.approve",
            "approval.reject",
            "approval.revise",
            "audit.read",
        ),
    ),
    Role(
        role="analyst",
        description="Creates documents, retrieves context, and submits reports for approval.",
        permissions=(
            "document.read",
            "document.upload",
            "document.import",
            "document.chunk",
            "document.search",
            "rag.answer",
            "report.read",
            "report.submit_approval",
        ),
    ),
    Role(
        role="viewer",
        description="Reads documents and reports without write access.",
        permissions=("document.read", "report.read"),
    ),
    Role(
        role="approver",
        description="Reviews and decides on pending report revisions.",
        permissions=(
            "approval.review",
            "approval.approve",
            "approval.reject",
            "approval.revise",
            "report.read",
            "audit.read",
        ),
    ),
    Role(
        role="auditor",
        description="Reads audit facts and reviews approval activity.",
        permissions=("audit.read", "approval.review", "report.read"),
    ),
)
_CURRENT_USER = User(
    user_id="system",
    username="system",
    display_name="System User",
    organization=_ORGANIZATION,
    department=_DEPARTMENT,
    roles=("admin",),
    permissions=_ALL_PERMISSION_NAMES,
    status=UserStatus.ACTIVE,
)
_POLICY_PLACEHOLDER = Policy(
    role="admin",
    permission="system.admin",
    effect=PolicyEffect.ALLOW,
)


class SecurityService:
    """返回当前用户快照和冻结目录。"""

    def __init__(self, current_user: User | None = None) -> None:
        """允许测试注入受限主体，默认仍是 system admin 占位用户。"""

        self._current_user = current_user or _CURRENT_USER

    def get_current_user(self) -> User:
        """返回系统占位用户，后续可由认证中间件替换。"""

        return self._current_user

    def has_permission(self, user: User, permission: str) -> bool:
        """判断当前主体是否拥有目标权限，system.admin 视为全权通过。"""

        return self.is_admin(user) or permission in user.permissions

    def has_role(self, user: User, role: str) -> bool:
        """判断当前主体是否拥有指定角色。"""

        return role in user.roles

    def has_permissions(
        self,
        user: User,
        permissions: tuple[str, ...],
        *,
        require_all: bool = True,
    ) -> bool:
        """判断当前主体是否满足多权限要求。"""

        if not permissions:
            return True
        if require_all:
            return all(
                self.has_permission(user, permission) for permission in permissions
            )
        return any(self.has_permission(user, permission) for permission in permissions)

    def has_roles(
        self,
        user: User,
        roles: tuple[str, ...],
        *,
        require_all: bool = False,
    ) -> bool:
        """判断当前主体是否满足多角色要求。"""

        if not roles:
            return True
        if require_all:
            return all(self.has_role(user, role) for role in roles)
        return any(self.has_role(user, role) for role in roles)

    def is_admin(self, user: User) -> bool:
        """判断当前主体是否为系统管理员占位用户。"""

        return "system.admin" in user.permissions or "admin" in user.roles

    def require_permission(
        self,
        permission: str,
        *,
        action: str,
        resource_type: str,
        resource_id: str,
        audit_service: AuditService,
    ) -> User:
        """校验当前用户权限；拒绝时先写审计事实，再抛出 403。"""

        from app.services.rbac_guard import RBACGuard

        guard = RBACGuard(self, audit_service)
        return guard.require(
            permission=permission,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
        )

    def list_roles(self) -> tuple[Role, ...]:
        """返回 frozen role catalog。"""

        return _ALL_ROLES

    def list_permissions(self) -> tuple[Permission, ...]:
        """返回 frozen permission catalog。"""

        return _FROZEN_PERMISSIONS

    def get_policy_placeholder(self) -> Policy:
        """返回策略占位对象，供未来 RBAC / scope 规则扩展。"""

        return _POLICY_PLACEHOLDER
