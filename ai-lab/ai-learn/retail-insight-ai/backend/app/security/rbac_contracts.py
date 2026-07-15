"""Enterprise RBAC 的稳定合同。

文件职责：集中定义 Role、Permission、Role Mapping、Authorization Result 与 Checker 协议。
谁调用它：Permission Registry、Resolver、Authorization Service、FastAPI Dependency 和测试。
它调用谁：仅使用 Python 标准库，不依赖业务 Service、Repository 或 JWT 实现。
输入：CurrentUser 中的 role 与 API 声明的 permission。
输出：不可变的权限元数据、角色映射和授权结果。
设计理由：JWT 只携带身份，权限由服务端目录解析，未来可以替换映射来源而不改变 Token。
日本现场面试：认证回答“你是谁”，本合同让授权独立回答“你能做什么”。
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from app.security.contracts import CurrentUser


class Role(str, Enum):
    """当前企业认证账号支持的三个稳定角色。"""

    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"


class Permission(str, Enum):
    """API 能力目录；名称描述能力，不写入具体业务对象或 JWT。"""

    DOCUMENTS_READ = "documents.read"
    DOCUMENTS_WRITE = "documents.write"
    DOCUMENTS_ARCHIVE = "documents.archive"
    RETRIEVAL_QUERY = "retrieval.query"
    ANALYSIS_EXECUTE = "analysis.execute"
    APPROVAL_SUBMIT = "approval.submit"
    APPROVAL_REVIEW = "approval.review"
    APPROVAL_ADMIN = "approval.admin"
    AUDIT_READ = "audit.read"
    SECURITY_MANAGE = "security.manage"


@dataclass(frozen=True)
class PermissionDefinition:
    """Permission Registry 中可展示、可审计的单条权限元数据。"""

    permission: Permission
    description: str
    category: str


@dataclass(frozen=True)
class RoleMapping:
    """一个角色到权限集合的不可变映射合同。"""

    role: Role
    description: str
    permissions: frozenset[Permission]


@dataclass(frozen=True)
class AuthorizationResult:
    """授权判定结果；成功与失败均可使用同一稳定结构。"""

    allowed: bool
    user_id: str
    role: str
    permission: Permission


class PermissionChecker(Protocol):
    """授权检查接口，便于未来替换成外部 Policy Engine。"""

    def check_permission(
        self, current_user: CurrentUser, permission: Permission
    ) -> AuthorizationResult:
        """检查当前用户是否拥有指定权限，不修改任何状态。"""

