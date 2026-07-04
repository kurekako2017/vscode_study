from __future__ import annotations

import unittest

import httpx

from app.config.settings import Settings
from app.errors.exceptions import AuditLogAppendException
from app.main import create_app
from app.models.audit import AuditLog, AuditLogResult
from app.services.audit_service import AuditService


class SecurityAuditAPITest(unittest.IsolatedAsyncioTestCase):
    """验证 security read API 与 append-only audit MVP。"""

    async def asyncSetUp(self) -> None:
        self.app = create_app(Settings(log_level="CRITICAL"))
        transport = httpx.ASGITransport(app=self.app)
        self.client = httpx.AsyncClient(transport=transport, base_url="http://test")

    async def asyncTearDown(self) -> None:
        await self.client.aclose()

    async def test_current_user_returns_system_placeholder(self) -> None:
        response = await self.client.get("/api/v1/users/me")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["success"])
        user = payload["data"]
        self.assertEqual(user["user_id"], "system")
        self.assertEqual(user["roles"], ["admin"])
        self.assertIn("system.admin", user["permissions"])
        self.assertIn("audit.read", user["permissions"])
        self.assertEqual(user["status"], "active")

    async def test_role_catalog_is_frozen(self) -> None:
        response = await self.client.get("/api/v1/security/roles")
        self.assertEqual(response.status_code, 200)
        payload = response.json()["data"]
        roles = payload["items"]
        self.assertEqual(
            [item["role"] for item in roles],
            ["admin", "manager", "analyst", "viewer", "approver", "auditor"],
        )
        admin_role = roles[0]
        self.assertIn("system.admin", admin_role["permissions"])
        self.assertIn("audit.read", admin_role["permissions"])

    async def test_permission_catalog_is_frozen(self) -> None:
        response = await self.client.get("/api/v1/security/permissions")
        self.assertEqual(response.status_code, 200)
        payload = response.json()["data"]
        permissions = payload["items"]
        permission_names = [item["permission"] for item in permissions]
        self.assertEqual(permission_names[0], "system.admin")
        self.assertIn("audit.read", permission_names)
        self.assertIn("approval.approve", permission_names)

    async def test_audit_log_append_and_read(self) -> None:
        service = self.app.state.container.audit_service
        service.record_audit_log(
            operation_type="security.role.assigned",
            actor_id="system",
            organization_id="org-system",
            department_id="dept-system",
            resource_type="role",
            resource_id="admin",
            result=AuditLogResult.SUCCESS,
            request_id="audit-request-001",
            trace_id="trace-audit-001",
            metadata={"scope": "security"},
        )
        service.record_audit_log(
            operation_type="audit.read",
            actor_id="system",
            organization_id="org-system",
            department_id="dept-system",
            resource_type="audit_log",
            resource_id="audit-2",
            result=AuditLogResult.SUCCESS,
            request_id="audit-request-002",
            trace_id="trace-audit-002",
            metadata={"scope": "read"},
        )

        response = await self.client.get("/api/v1/audit-logs")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["success"])
        items = payload["data"]["items"]
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["operation_type"], "security.role.assigned")
        self.assertEqual(items[0]["result"], "success")
        self.assertEqual(items[0]["request_id"], "audit-request-001")
        self.assertEqual(items[1]["operation_type"], "audit.read")
        self.assertEqual(payload["data"]["next_cursor"], None)

    async def test_audit_repository_is_append_only(self) -> None:
        repository = self.app.state.container.audit_repository
        log = AuditLog(
            operation_type="security.permission.denied",
            actor_id="system",
            organization_id="org-system",
            department_id="dept-system",
            resource_type="permission",
            resource_id="approval.approve",
            result=AuditLogResult.DENIED,
            request_id="audit-request-003",
            trace_id="trace-audit-003",
            metadata={"reason": "read only"},
        )

        stored = repository.append(log)
        stored.metadata["reason"] = "mutated"
        logs = repository.list_all()
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0].metadata["reason"], "read only")
        self.assertFalse(hasattr(repository, "update"))
        self.assertFalse(hasattr(repository, "delete"))

    async def test_audit_service_raises_when_append_fails(self) -> None:
        class FailingRepository:
            def append(self, log: AuditLog) -> AuditLog:
                raise RuntimeError("boom")

            def list_all(self) -> list[AuditLog]:
                return []

        service = AuditService(FailingRepository())
        with self.assertRaises(AuditLogAppendException):
            service.record_audit_log(
                operation_type="audit.read",
                actor_id="system",
                organization_id="org-system",
                department_id="dept-system",
                resource_type="audit_log",
                resource_id="audit-4",
                result=AuditLogResult.FAILED,
                request_id="audit-request-004",
                trace_id="trace-audit-004",
                metadata={"scope": "failure"},
            )


if __name__ == "__main__":
    unittest.main()
