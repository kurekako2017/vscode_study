"""Security domain models.

文件职责：
- 定义 User、Organization、Department、Role、Permission 与 Policy 的冻结领域结构。
- 把未来 RBAC 和审计读取所依赖的身份与权限概念先固定下来。

谁会调用它：
- security service、audit service、API schema 转换层和测试。

它调用谁：
- 只依赖统一时间工具，不依赖 API、Repository 或数据库细节。

输入是什么：
- 当前用户快照、组织/部门归属、角色目录、权限目录、策略占位信息。

输出是什么：
- 可序列化、可复制、可替换的安全域对象。

为什么需要这一层：
- 先把身份和权限语义冻结成领域对象，后续无论接真实认证还是 RBAC，
  都只需要替换 service 和 middleware，不需要重写核心模型。

日本现场面试怎么讲：
- 这是 security foundation 的 domain boundary，先把 user / role / permission
  的结构固定住，未来接 PostgreSQL、认证中间件或 RBAC 引擎时不会破坏接口。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from uuid import uuid4

from app.models.task import utc_now


class UserStatus(StrEnum):
    """定义当前用户快照状态。"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class PolicyEffect(StrEnum):
    """定义策略占位的允许与拒绝效果。"""

    ALLOW = "allow"
    DENY = "deny"


@dataclass(frozen=True)
class Organization:
    """保存组织边界，作为 user 的归属事实。"""

    organization_id: str
    name: str
    display_name: str
    status: UserStatus = UserStatus.ACTIVE


@dataclass(frozen=True)
class Department:
    """保存部门边界，作为 user 的归属事实。"""

    department_id: str
    organization_id: str
    name: str
    display_name: str
    status: UserStatus = UserStatus.ACTIVE


@dataclass(frozen=True)
class Role:
    """保存角色目录项及其授权权限集合。"""

    role: str
    description: str
    permissions: tuple[str, ...] = field(default_factory=tuple)
    status: UserStatus = UserStatus.ACTIVE


@dataclass(frozen=True)
class Permission:
    """保存权限目录项。"""

    permission: str
    description: str
    category: str


@dataclass(frozen=True)
class Policy:
    """策略占位模型，先冻结 role -> permission 的映射语义。"""

    role: str
    permission: str
    effect: PolicyEffect = PolicyEffect.ALLOW
    resource_scope: str | None = None
    policy_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=utc_now)


@dataclass(frozen=True)
class User:
    """保存当前主体快照，供 users/me 和未来 RBAC 判断读取。"""

    user_id: str
    username: str
    display_name: str
    organization: Organization
    department: Department
    roles: tuple[str, ...] = field(default_factory=tuple)
    permissions: tuple[str, ...] = field(default_factory=tuple)
    status: UserStatus = UserStatus.ACTIVE
