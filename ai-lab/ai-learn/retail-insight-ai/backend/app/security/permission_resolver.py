"""CurrentUser Role 到 Permission 集合的解析器。

文件职责：把 JWT CurrentUser 的 role 解析为服务端权限集合。
谁调用它：AuthorizationService 和单元测试。
它调用谁：PermissionRegistry。
输入：CurrentUser.role 的字符串值。
输出：不可变 Permission 集合；未知角色安全返回空集合。
设计理由：角色解析与允许/拒绝判定分离，避免无效 role 变成 500。
日本现场面试：Resolver 默认拒绝未知角色，是 fail-closed 的企业安全边界。
"""

from __future__ import annotations

from app.security.permission_registry import PermissionRegistry
from app.security.rbac_contracts import Permission, Role


class PermissionResolver:
    """根据集中 Registry 解析角色权限。"""

    def __init__(self, registry: PermissionRegistry) -> None:
        self._registry = registry

    def resolve(self, role_name: str) -> frozenset[Permission]:
        """解析角色；未知或格式异常的值使用空权限集安全降级。"""

        try:
            role = Role(role_name.strip().lower())
        except (AttributeError, ValueError):
            return frozenset()
        return self._registry.get_role_mapping(role).permissions
