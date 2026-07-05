from __future__ import annotations

import unittest
from dataclasses import replace

from app.config.settings import Settings
from app.errors.exceptions import PermissionDeniedException
from app.main import create_app
from app.models.audit import AuditLogResult
from app.models.security import Department, Organization, User, UserStatus
from app.services.rbac_guard import RBACGuard
from app.services.security_service import SecurityService


class RBACGuardTest(unittest.TestCase):
    """验证可复用 RBAC guard 的权限、角色和审计行为。"""

    def setUp(self) -> None:
        self.app = create_app(Settings(log_level="CRITICAL"))

    def _build_guard(
        self,
        *,
        roles: tuple[str, ...] = ("viewer",),
        permissions: tuple[str, ...] = (),
    ) -> RBACGuard:
        organization = Organization(
            organization_id="org-test",
            name="test",
            display_name="Test Organization",
        )
        department = Department(
            department_id="dept-test",
            organization_id=organization.organization_id,
            name="test",
            display_name="Test Department",
        )
        current_user = User(
            user_id="user-test",
            username="test-user",
            display_name="Test User",
            organization=organization,
            department=department,
            roles=roles,
            permissions=permissions,
            status=UserStatus.ACTIVE,
        )
        self.app.state.container = replace(
            self.app.state.container,
            security_service=SecurityService(current_user=current_user),
        )
        return RBACGuard(
            self.app.state.container.security_service,
            self.app.state.container.audit_service,
        )

    def test_permission_string_allows_access(self) -> None:
        guard = self._build_guard(permissions=("approval.approve",))

        user = guard.require(
            permission="approval.approve",
            action="approve_approval",
            resource_type="approval",
            resource_id="approval-001",
        )

        self.assertEqual(user.user_id, "user-test")
        self.assertEqual(self.app.state.container.audit_repository.list_all(), [])

    def test_role_allows_access(self) -> None:
        guard = self._build_guard(roles=("approver",))

        user = guard.require(
            role="approver",
            action="review_approval",
            resource_type="approval",
            resource_id="approval-002",
        )

        self.assertEqual(user.user_id, "user-test")
        self.assertEqual(self.app.state.container.audit_repository.list_all(), [])

    def test_admin_bypass_allows_access(self) -> None:
        guard = self._build_guard(roles=("admin",), permissions=())

        user = guard.require(
            permission="approval.approve",
            action="approve_approval",
            resource_type="approval",
            resource_id="approval-003",
        )

        self.assertEqual(user.user_id, "user-test")
        self.assertEqual(self.app.state.container.audit_repository.list_all(), [])

    def test_multiple_permissions_allow_access_when_all_present(self) -> None:
        guard = self._build_guard(
            permissions=("approval.review", "approval.approve"),
        )

        user = guard.require(
            permissions=("approval.review", "approval.approve"),
            action="approve_approval",
            resource_type="approval",
            resource_id="approval-004",
        )

        self.assertEqual(user.user_id, "user-test")
        self.assertEqual(self.app.state.container.audit_repository.list_all(), [])

    def test_permission_denied_creates_audit_log(self) -> None:
        guard = self._build_guard(permissions=("approval.review",))

        with self.assertRaises(PermissionDeniedException) as context:
            guard.require(
                permission="approval.approve",
                action="approve_approval",
                resource_type="approval",
                resource_id="approval-005",
            )

        self.assertEqual(context.exception.error_code.value, "permission_denied")
        logs = self.app.state.container.audit_repository.list_all()
        self.assertEqual(len(logs), 1)
        log = logs[0]
        self.assertEqual(log.operation_type, "security.permission.denied")
        self.assertEqual(log.result, AuditLogResult.DENIED)
        self.assertEqual(log.resource_id, "approval-005")
        self.assertEqual(log.metadata["required_permission"], "approval.approve")
        self.assertEqual(log.metadata["action"], "approve_approval")

    def test_multiple_permissions_deny_and_audit_when_missing_one(self) -> None:
        guard = self._build_guard(permissions=("approval.review",))

        with self.assertRaises(PermissionDeniedException) as context:
            guard.require(
                permissions=("approval.review", "approval.approve"),
                action="approve_approval",
                resource_type="approval",
                resource_id="approval-006",
            )

        self.assertEqual(context.exception.error_code.value, "permission_denied")
        logs = self.app.state.container.audit_repository.list_all()
        self.assertEqual(len(logs), 1)
        log = logs[0]
        self.assertEqual(log.result, AuditLogResult.DENIED)
        self.assertEqual(log.resource_id, "approval-006")
        self.assertEqual(
            log.metadata["required_permissions"],
            ["approval.review", "approval.approve"],
        )
        self.assertEqual(
            log.metadata["required_permission"], "approval.review,approval.approve"
        )


if __name__ == "__main__":
    unittest.main()
