"""Security API schemas.

文件职责：
- 定义 users/me、roles 和 permissions 的 HTTP response schema。
- 把 security service 的领域对象转换成对外稳定合同。

谁会调用它：
- `backend/app/api/security.py` 路由和对应测试。

它调用谁：
- 只依赖 Pydantic 和 security domain models，不依赖 repository 实现。

输入是什么：
- 当前用户、角色目录、权限目录。

输出是什么：
- 可序列化的用户快照和冻结目录 response。

为什么需要这一层：
- 路由不应该直接把领域对象返回给客户端，需要在这里固定公开字段。

日本现场面试怎么讲：
- 这是 security read model 的 HTTP boundary，未来接真实认证也只改内部映射，不改输出格式。
"""

from __future__ import annotations

from pydantic import BaseModel

from app.security.contracts import CurrentUser
from app.security.rbac_contracts import (
    Permission,
    PermissionDefinition,
    RoleMapping,
)


class CurrentUserResponse(BaseModel):
    """GET /api/v1/users/me 返回 JWT 认证后的最小身份。"""

    user_id: str
    username: str
    role: str

    @classmethod
    def from_current_user(cls, user: CurrentUser) -> "CurrentUserResponse":
        """从认证 dependency 返回的主体生成对外 response。"""

        return cls(
            user_id=user.user_id,
            username=user.username,
            role=user.role,
        )


class RoleResponse(BaseModel):
    """冻结角色目录中的单条记录。"""

    role: str
    description: str
    permissions: list[str]

    @classmethod
    def from_contract(cls, role: RoleMapping) -> "RoleResponse":
        """从集中 Role Mapping 生成稳定排序的对外 response。"""

        return cls(
            role=role.role.value,
            description=role.description,
            permissions=[
                permission.value
                for permission in Permission
                if permission in role.permissions
            ],
        )


class RoleListResponse(BaseModel):
    """冻结 GET /api/v1/security/roles 的列表输出。"""

    items: list[RoleResponse]
    next_cursor: str | None = None

    @classmethod
    def from_contract(cls, roles: tuple[RoleMapping, ...]) -> "RoleListResponse":
        """把集中角色目录转成 response list。"""

        return cls(
            items=[RoleResponse.from_contract(role) for role in roles],
            next_cursor=None,
        )


class PermissionResponse(BaseModel):
    """冻结权限目录中的单条记录。"""

    permission: str
    description: str
    category: str

    @classmethod
    def from_contract(cls, permission: PermissionDefinition) -> "PermissionResponse":
        """从 Permission Registry 定义生成对外 response。"""

        return cls(
            permission=permission.permission.value,
            description=permission.description,
            category=permission.category,
        )


class PermissionListResponse(BaseModel):
    """冻结 GET /api/v1/security/permissions 的列表输出。"""

    items: list[PermissionResponse]
    next_cursor: str | None = None

    @classmethod
    def from_contract(
        cls, permissions: tuple[PermissionDefinition, ...]
    ) -> "PermissionListResponse":
        """把集中权限目录转成 response list。"""

        return cls(
            items=[
                PermissionResponse.from_contract(permission)
                for permission in permissions
            ],
            next_cursor=None,
        )
