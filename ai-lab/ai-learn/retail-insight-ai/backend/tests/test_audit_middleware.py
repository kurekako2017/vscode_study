from __future__ import annotations

import unittest
from dataclasses import replace

from app.config.settings import Settings
from app.errors.exceptions import (
    ApprovalAlreadyDecidedException,
    PermissionDeniedException,
)
from app.main import create_app
from app.models.audit import AuditLogResult
from app.models.security import Department, Organization, User, UserStatus
from app.observability.logging import bind_request_id, reset_request_id
from app.services.audit_middleware import AuditAction, AuditMiddleware
from app.services.rbac_guard import RBACGuard
from app.services.security_service import SecurityService


class AuditMiddlewareTest(unittest.IsolatedAsyncioTestCase):
    """验证 approval 专用审计中间层的写入与错误分支。"""

    async def asyncSetUp(self) -> None:
        self.app = create_app(Settings(log_level="CRITICAL"))

    def _set_current_user(
        self,
        *,
        roles: tuple[str, ...] = ("viewer",),
        permissions: tuple[str, ...] = (),
    ) -> None:
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

    def _build_middleware(self) -> AuditMiddleware:
        security_service = self.app.state.container.security_service
        audit_service = self.app.state.container.audit_service
        return AuditMiddleware(
            audit_service=audit_service,
            security_service=security_service,
            rbac_guard=RBACGuard(security_service, audit_service),
        )

    def _assert_single_log(
        self,
        *,
        operation_type: str,
        resource_type: str,
        resource_id: str,
        result: AuditLogResult,
        request_id: str,
    ) -> None:
        logs = self.app.state.container.audit_repository.list_all()
        self.assertEqual(len(logs), 1)
        log = logs[0]
        self.assertEqual(log.operation_type, operation_type)
        self.assertEqual(log.resource_type, resource_type)
        self.assertEqual(log.resource_id, resource_id)
        self.assertEqual(log.result, result)
        self.assertEqual(log.request_id, request_id)
        self.assertEqual(log.trace_id, request_id)
        self.assertIsNotNone(log.timestamp)

    async def test_success_records_audit(self) -> None:
        self._set_current_user(permissions=("approval.approve",))
        middleware = self._build_middleware()
        token = bind_request_id("audit-request-success")
        try:
            result = await middleware.run(
                action=AuditAction(
                    operation_type="approval.approved",
                    resource_type="approval",
                    resource_id="approval-success",
                    action="approve_approval",
                    metadata={"approval_id": "approval-success"},
                    permission="approval.approve",
                ),
                operation=lambda: "ok",
            )
        finally:
            reset_request_id(token)

        self.assertEqual(result, "ok")
        self._assert_single_log(
            operation_type="approval.approved",
            resource_type="approval",
            resource_id="approval-success",
            result=AuditLogResult.SUCCESS,
            request_id="audit-request-success",
        )
        self.assertEqual(
            self.app.state.container.audit_repository.list_all()[0].metadata[
                "approval_id"
            ],
            "approval-success",
        )

    async def test_multiple_permissions_allow_access(self) -> None:
        self._set_current_user(permissions=("approval.review", "approval.approve"))
        middleware = self._build_middleware()
        token = bind_request_id("audit-request-multi")
        try:
            result = await middleware.run(
                action=AuditAction(
                    operation_type="approval.approved",
                    resource_type="approval",
                    resource_id="approval-multi",
                    action="approve_approval",
                    permissions=("approval.review", "approval.approve"),
                ),
                operation=lambda: "ok",
            )
        finally:
            reset_request_id(token)

        self.assertEqual(result, "ok")
        self._assert_single_log(
            operation_type="approval.approved",
            resource_type="approval",
            resource_id="approval-multi",
            result=AuditLogResult.SUCCESS,
            request_id="audit-request-multi",
        )

    async def test_admin_bypass_records_success(self) -> None:
        self._set_current_user(roles=("admin",), permissions=())
        middleware = self._build_middleware()
        token = bind_request_id("audit-request-admin")
        try:
            result = await middleware.run(
                action=AuditAction(
                    operation_type="approval.read",
                    resource_type="approval",
                    resource_id="approval-admin",
                    action="get_approval",
                    permission="approval.review",
                ),
                operation=lambda: "ok",
            )
        finally:
            reset_request_id(token)

        self.assertEqual(result, "ok")
        self._assert_single_log(
            operation_type="approval.read",
            resource_type="approval",
            resource_id="approval-admin",
            result=AuditLogResult.SUCCESS,
            request_id="audit-request-admin",
        )

    async def test_permission_denied_records_deny_audit(self) -> None:
        self._set_current_user(permissions=("approval.review",))
        middleware = self._build_middleware()
        token = bind_request_id("audit-request-denied")
        try:
            with self.assertRaises(PermissionDeniedException):
                await middleware.run(
                    action=AuditAction(
                        operation_type="approval.approved",
                        resource_type="approval",
                        resource_id="approval-denied",
                        action="approve_approval",
                        permission="approval.approve",
                    ),
                    operation=lambda: "not-run",
                )
        finally:
            reset_request_id(token)

        self._assert_single_log(
            operation_type="security.permission.denied",
            resource_type="approval",
            resource_id="approval-denied",
            result=AuditLogResult.DENIED,
            request_id="audit-request-denied",
        )
        self.assertEqual(
            self.app.state.container.audit_repository.list_all()[0].metadata[
                "required_permission"
            ],
            "approval.approve",
        )

    async def test_app_exception_records_failed_audit(self) -> None:
        self._set_current_user(permissions=("approval.approve",))
        middleware = self._build_middleware()
        token = bind_request_id("audit-request-failed")
        try:
            with self.assertRaises(ApprovalAlreadyDecidedException):
                await middleware.run(
                    action=AuditAction(
                        operation_type="approval.approved",
                        resource_type="approval",
                        resource_id="approval-failed",
                        action="approve_approval",
                        permission="approval.approve",
                    ),
                    operation=lambda: (_ for _ in ()).throw(
                        ApprovalAlreadyDecidedException("approval-failed", "approved")
                    ),
                )
        finally:
            reset_request_id(token)

        self._assert_single_log(
            operation_type="approval.approved",
            resource_type="approval",
            resource_id="approval-failed",
            result=AuditLogResult.FAILED,
            request_id="audit-request-failed",
        )
        log = self.app.state.container.audit_repository.list_all()[0]
        self.assertEqual(
            log.metadata["exception_type"], "ApprovalAlreadyDecidedException"
        )
        self.assertEqual(log.metadata["error_code"], "approval_already_decided")

    async def test_unexpected_exception_records_failed_audit(self) -> None:
        self._set_current_user(permissions=("approval.review",))
        middleware = self._build_middleware()
        token = bind_request_id("audit-request-error")
        try:
            with self.assertRaises(RuntimeError):
                await middleware.run(
                    action=AuditAction(
                        operation_type="approval.read",
                        resource_type="approval",
                        resource_id="approval-error",
                        action="get_approval",
                        permission="approval.review",
                    ),
                    operation=lambda: (_ for _ in ()).throw(RuntimeError("boom")),
                )
        finally:
            reset_request_id(token)

        self._assert_single_log(
            operation_type="approval.read",
            resource_type="approval",
            resource_id="approval-error",
            result=AuditLogResult.FAILED,
            request_id="audit-request-error",
        )
        log = self.app.state.container.audit_repository.list_all()[0]
        self.assertEqual(log.metadata["exception_type"], "RuntimeError")
        self.assertEqual(log.error_code, "internal_error")


if __name__ == "__main__":
    unittest.main()
