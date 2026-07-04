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

from app.models.security import Permission, Role, User


class CurrentUserResponse(BaseModel):
    """冻结 GET /api/v1/users/me 的响应结构。"""

    user_id: str
    username: str
    display_name: str
    organization_id: str
    department_id: str
    roles: list[str]
    permissions: list[str]
    status: str

    @classmethod
    def from_domain(cls, user: User) -> "CurrentUserResponse":
        """从领域用户快照生成对外 response。"""

        return cls(
            user_id=user.user_id,
            username=user.username,
            display_name=user.display_name,
            organization_id=user.organization.organization_id,
            department_id=user.department.department_id,
            roles=list(user.roles),
            permissions=list(user.permissions),
            status=user.status.value,
        )


class RoleResponse(BaseModel):
    """冻结角色目录中的单条记录。"""

    role: str
    description: str
    permissions: list[str]

    @classmethod
    def from_domain(cls, role: Role) -> "RoleResponse":
        """从领域角色生成对外 response。"""

        return cls(role=role.role, description=role.description, permissions=list(role.permissions))


class RoleListResponse(BaseModel):
    """冻结 GET /api/v1/security/roles 的列表输出。"""

    items: list[RoleResponse]
    next_cursor: str | None = None

    @classmethod
    def from_domain(cls, roles: tuple[Role, ...]) -> "RoleListResponse":
        """把 frozen role catalog 转成 response list。"""

        return cls(items=[RoleResponse.from_domain(role) for role in roles], next_cursor=None)


class PermissionResponse(BaseModel):
    """冻结权限目录中的单条记录。"""

    permission: str
    description: str
    category: str

    @classmethod
    def from_domain(cls, permission: Permission) -> "PermissionResponse":
        """从领域权限生成对外 response。"""

        return cls(
            permission=permission.permission,
            description=permission.description,
            category=permission.category,
        )


class PermissionListResponse(BaseModel):
    """冻结 GET /api/v1/security/permissions 的列表输出。"""

    items: list[PermissionResponse]
    next_cursor: str | None = None

    @classmethod
    def from_domain(cls, permissions: tuple[Permission, ...]) -> "PermissionListResponse":
        """把 frozen permission catalog 转成 response list。"""

        return cls(items=[PermissionResponse.from_domain(permission) for permission in permissions], next_cursor=None)

