"""Enterprise RBAC Authorization Service。

文件职责：使用 CurrentUser 与 PermissionResolver 作统一授权判定。
谁调用它：FastAPI Permission Dependency、Security Catalog API 和测试。
它调用谁：PermissionResolver、PermissionRegistry 与 ForbiddenError。
输入：已认证 CurrentUser 和 API 所需 Permission。
输出：AuthorizationResult；拒绝时抛出稳定 ForbiddenError。
设计理由：业务 Router/Service 不出现 role if 判断，未来可在此替换 Policy Engine。
日本现场面试：依赖链严格保持 Authentication → CurrentUser → Authorization → API。
"""

from __future__ import annotations

from app.security.contracts import CurrentUser
from app.security.errors import ForbiddenError
from app.security.permission_registry import PermissionRegistry
from app.security.permission_resolver import PermissionResolver
from app.security.rbac_contracts import AuthorizationResult, Permission


class AuthorizationService:
    """集中检查和强制执行 API 权限。"""

    def __init__(
        self, resolver: PermissionResolver, registry: PermissionRegistry
    ) -> None:
        self._resolver = resolver
        self._registry = registry

    @property
    def registry(self) -> PermissionRegistry:
        """向只读 Security Catalog API 暴露同一 Registry。"""

        return self._registry

    def check_permission(
        self, current_user: CurrentUser, permission: Permission
    ) -> AuthorizationResult:
        """返回无副作用判定结果，供策略测试或组合检查使用。"""

        return AuthorizationResult(
            allowed=permission in self._resolver.resolve(current_user.role),
            user_id=current_user.user_id,
            role=current_user.role,
            permission=permission,
        )

    def require_permission(
        self, current_user: CurrentUser, permission: Permission
    ) -> AuthorizationResult:
        """要求指定权限；不足时统一转换为 403 Forbidden。"""

        result = self.check_permission(current_user, permission)
        if not result.allowed:
            raise ForbiddenError(permission=permission.value, role=current_user.role)
        return result
