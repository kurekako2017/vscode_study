"""集中式 Permission Registry 与 Role Mapping。

文件职责：保存唯一权限目录和 admin / manager / employee 的不可变映射。
谁调用它：PermissionResolver、AuthorizationService 与 Security Catalog API。
它调用谁：只依赖 RBAC contracts。
输入：Role 或 Permission 枚举。
输出：稳定排序的权限定义、角色映射与查询结果。
设计理由：新增权限只改一个目录，API 不散落角色字符串和权限矩阵。
日本现场面试：Registry 是 server-side policy source，Token 不承载易过期的 permission 列表。
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Mapping

from app.security.rbac_contracts import (
    Permission,
    PermissionDefinition,
    Role,
    RoleMapping,
)


class PermissionRegistry:
    """提供只读权限目录与角色映射。"""

    _PERMISSIONS = (
        PermissionDefinition(Permission.DOCUMENTS_READ, "读取企业文档", "documents"),
        PermissionDefinition(Permission.DOCUMENTS_WRITE, "上传、切片或导入企业文档", "documents"),
        PermissionDefinition(Permission.DOCUMENTS_ARCHIVE, "归档企业文档", "documents"),
        PermissionDefinition(Permission.RETRIEVAL_QUERY, "执行企业知识检索", "retrieval"),
        PermissionDefinition(Permission.ANALYSIS_EXECUTE, "执行分析任务或 Internal RAG", "analysis"),
        PermissionDefinition(Permission.APPROVAL_SUBMIT, "提交报告审批", "approval"),
        PermissionDefinition(Permission.APPROVAL_REVIEW, "查看审批队列和详情", "approval"),
        PermissionDefinition(Permission.APPROVAL_ADMIN, "批准、拒绝或修订审批", "approval"),
        PermissionDefinition(Permission.AUDIT_READ, "读取审计事实", "audit"),
        PermissionDefinition(Permission.SECURITY_MANAGE, "读取和管理安全策略目录", "security"),
    )

    _ROLE_MAPPINGS: Mapping[Role, RoleMapping] = MappingProxyType(
        {
            Role.ADMIN: RoleMapping(
                Role.ADMIN,
                "平台安全管理员，拥有全部当前权限",
                frozenset(Permission),
            ),
            Role.MANAGER: RoleMapping(
                Role.MANAGER,
                "业务经理，可管理文档、分析、审批和审计",
                frozenset(
                    {
                        Permission.DOCUMENTS_READ,
                        Permission.DOCUMENTS_WRITE,
                        Permission.DOCUMENTS_ARCHIVE,
                        Permission.RETRIEVAL_QUERY,
                        Permission.ANALYSIS_EXECUTE,
                        Permission.APPROVAL_SUBMIT,
                        Permission.APPROVAL_REVIEW,
                        Permission.APPROVAL_ADMIN,
                        Permission.AUDIT_READ,
                    }
                ),
            ),
            Role.EMPLOYEE: RoleMapping(
                Role.EMPLOYEE,
                "一般员工，可读写文档、检索、分析和提交审批",
                frozenset(
                    {
                        Permission.DOCUMENTS_READ,
                        Permission.DOCUMENTS_WRITE,
                        Permission.RETRIEVAL_QUERY,
                        Permission.ANALYSIS_EXECUTE,
                        Permission.APPROVAL_SUBMIT,
                    }
                ),
            ),
        }
    )

    def list_permissions(self) -> tuple[PermissionDefinition, ...]:
        """按注册顺序返回完整权限目录。"""

        return self._PERMISSIONS

    def list_role_mappings(self) -> tuple[RoleMapping, ...]:
        """按 Role 枚举顺序返回完整角色目录。"""

        return tuple(self._ROLE_MAPPINGS[role] for role in Role)

    def get_role_mapping(self, role: Role) -> RoleMapping:
        """读取一个已验证角色的不可变映射。"""

        return self._ROLE_MAPPINGS[role]
