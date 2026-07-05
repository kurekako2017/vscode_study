from __future__ import annotations

import asyncio
import unittest
from dataclasses import replace

import httpx
from app.config.settings import Settings
from app.main import create_app
from app.models.audit import AuditLogResult
from app.models.report import ReportStatus
from app.models.security import Department, Organization, User, UserStatus
from app.services.security_service import SecurityService


class ApprovalApiTest(unittest.IsolatedAsyncioTestCase):
    """验证 Approval Workflow MVP 的 HTTP contract 和状态机。"""

    async def asyncSetUp(self) -> None:
        self.app = create_app(
            Settings(workflow_step_delay_seconds=0, log_level="CRITICAL")
        )
        transport = httpx.ASGITransport(app=self.app)
        self.client = httpx.AsyncClient(transport=transport, base_url="http://test")

    async def asyncTearDown(self) -> None:
        await self.client.aclose()

    async def _create_task(self) -> str:
        response = await self.client.post(
            "/api/tasks",
            headers={"X-Request-ID": "approval-create-request"},
            json={"question": "売上と在庫の状況を分析してください", "mode": "hybrid"},
        )
        self.assertEqual(response.status_code, 202)
        return response.json()["data"]["task_id"]

    async def _wait_for_report(self, task_id: str) -> None:
        for _ in range(100):
            response = await self.client.get(f"/api/tasks/{task_id}")
            self.assertEqual(response.status_code, 200)
            if response.json()["data"]["status"] in {"completed", "failed"}:
                break
            await asyncio.sleep(0.01)
        report_response = await self.client.get(f"/api/tasks/{task_id}/report")
        self.assertEqual(report_response.status_code, 200)
        self.assertEqual(report_response.json()["data"]["status"], "generated")

    async def _create_report_task(self) -> str:
        task_id = await self._create_task()
        await self._wait_for_report(task_id)
        return task_id

    def _set_current_user(self, permissions: tuple[str, ...]) -> None:
        """测试里替换 current user，用来覆盖 RBAC 允许和拒绝分支。"""

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
            roles=("viewer",),
            permissions=permissions,
            status=UserStatus.ACTIVE,
        )
        self.app.state.container = replace(
            self.app.state.container,
            security_service=SecurityService(current_user=current_user),
        )

    async def _assert_permission_denied(
        self,
        *,
        method: str,
        url: str,
        payload: dict[str, object] | None,
        required_permission: str,
        resource_id: str,
        action: str,
    ) -> None:
        """断言 RBAC 拒绝时既返回 permission_denied，也会写入审计事实。"""

        before_count = len(self.app.state.container.audit_repository.list_all())
        request_kwargs: dict[str, object] = {}
        if payload is not None:
            request_kwargs["json"] = payload

        response = await self.client.request(method, url, **request_kwargs)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["error"]["code"], "permission_denied")

        logs = self.app.state.container.audit_repository.list_all()
        self.assertEqual(len(logs), before_count + 1)
        log = logs[-1]
        self.assertEqual(log.operation_type, "security.permission.denied")
        self.assertEqual(log.result, AuditLogResult.DENIED)
        self.assertEqual(log.resource_id, resource_id)
        self.assertEqual(log.metadata["required_permission"], required_permission)
        self.assertEqual(log.metadata["action"], action)

    async def test_submit_approval_succeeds(self) -> None:
        task_id = await self._create_report_task()
        response = await self.client.post(
            f"/api/v1/reports/{task_id}/submit-approval",
            json={"comment": "Ready for review"},
        )
        self.assertEqual(response.status_code, 201)
        payload = response.json()["data"]
        self.assertEqual(payload["task_id"], task_id)
        self.assertEqual(payload["status"], "pending_approval")
        self.assertIsNone(payload["decided_at"])
        self.assertEqual(payload["revision_no"], 1)

    async def test_submit_approval_denied_without_permission(self) -> None:
        self._set_current_user(("report.read",))
        await self._assert_permission_denied(
            method="POST",
            url="/api/v1/reports/task-unauthorized/submit-approval",
            payload={"comment": "Ready for review"},
            required_permission="report.submit_approval",
            resource_id="task-unauthorized",
            action="submit_approval",
        )

    async def test_submit_already_submitted_returns_error(self) -> None:
        task_id = await self._create_report_task()
        first = await self.client.post(
            f"/api/v1/reports/{task_id}/submit-approval", json={"comment": "Ready"}
        )
        self.assertEqual(first.status_code, 201)

        second = await self.client.post(
            f"/api/v1/reports/{task_id}/submit-approval", json={"comment": "Again"}
        )
        self.assertEqual(second.status_code, 409)
        payload = second.json()
        self.assertFalse(payload["success"])
        self.assertEqual(payload["error"]["code"], "approval_already_submitted")

        events = self.app.state.container.event_repository.list_after(task_id)
        approval_events = [
            event.event_type
            for event in events
            if event.event_type.startswith("approval.")
        ]
        self.assertIn("approval.submitted", approval_events)
        self.assertIn("approval.failed", approval_events)

    async def test_approve_pending_approval_succeeds(self) -> None:
        task_id = await self._create_report_task()
        submit = await self.client.post(
            f"/api/v1/reports/{task_id}/submit-approval", json={"comment": "Ready"}
        )
        approval_id = submit.json()["data"]["approval_id"]

        response = await self.client.post(
            f"/api/v1/approvals/{approval_id}/approve",
            json={"comment": "Approved after review"},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()["data"]
        self.assertEqual(payload["status"], "approved")
        self.assertIsNotNone(payload["decided_at"])
        self.assertEqual(payload["decision_reason"], "Approved after review")

    async def test_approve_denied_without_permission(self) -> None:
        self._set_current_user(("approval.review",))
        await self._assert_permission_denied(
            method="POST",
            url="/api/v1/approvals/approval-unauthorized/approve",
            payload={"comment": "Approved after review"},
            required_permission="approval.approve",
            resource_id="approval-unauthorized",
            action="approve_approval",
        )

    async def test_reject_without_reason_returns_error(self) -> None:
        task_id = await self._create_report_task()
        submit = await self.client.post(
            f"/api/v1/reports/{task_id}/submit-approval", json={"comment": "Ready"}
        )
        approval_id = submit.json()["data"]["approval_id"]

        response = await self.client.post(
            f"/api/v1/approvals/{approval_id}/reject", json={}
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"]["code"], "missing_rejection_reason")

    async def test_reject_with_reason_succeeds(self) -> None:
        task_id = await self._create_report_task()
        submit = await self.client.post(
            f"/api/v1/reports/{task_id}/submit-approval", json={"comment": "Ready"}
        )
        approval_id = submit.json()["data"]["approval_id"]

        response = await self.client.post(
            f"/api/v1/approvals/{approval_id}/reject",
            json={"reason": "Need clearer source trace"},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()["data"]
        self.assertEqual(payload["status"], "rejected")
        self.assertEqual(payload["decision_reason"], "Need clearer source trace")

    async def test_reject_denied_without_permission(self) -> None:
        self._set_current_user(("approval.review",))
        await self._assert_permission_denied(
            method="POST",
            url="/api/v1/approvals/approval-unauthorized/reject",
            payload={"reason": "Need clearer source trace"},
            required_permission="approval.reject",
            resource_id="approval-unauthorized",
            action="reject_approval",
        )

    async def test_approve_already_decided_returns_error(self) -> None:
        task_id = await self._create_report_task()
        submit = await self.client.post(
            f"/api/v1/reports/{task_id}/submit-approval", json={"comment": "Ready"}
        )
        approval_id = submit.json()["data"]["approval_id"]

        approve = await self.client.post(
            f"/api/v1/approvals/{approval_id}/approve", json={"comment": "Approved"}
        )
        self.assertEqual(approve.status_code, 200)

        second = await self.client.post(
            f"/api/v1/approvals/{approval_id}/approve", json={"comment": "Again"}
        )
        self.assertEqual(second.status_code, 409)
        self.assertEqual(second.json()["error"]["code"], "approval_already_decided")

    async def test_revise_rejected_report_creates_new_version(self) -> None:
        task_id = await self._create_report_task()
        submit = await self.client.post(
            f"/api/v1/reports/{task_id}/submit-approval", json={"comment": "Ready"}
        )
        approval_id = submit.json()["data"]["approval_id"]

        reject = await self.client.post(
            f"/api/v1/approvals/{approval_id}/reject",
            json={"reason": "Need clearer source trace"},
        )
        self.assertEqual(reject.status_code, 200)

        revise = await self.client.post(
            f"/api/v1/reports/{task_id}/revise",
            json={"revision_reason": "Clarify source trace"},
        )
        self.assertEqual(revise.status_code, 201)
        payload = revise.json()["data"]
        self.assertEqual(payload["status"], "revised")
        self.assertEqual(payload["revision_no"], 2)
        self.assertIsNotNone(payload["revised_from_version_id"])

        report = self.app.state.container.report_repository.get(task_id)
        self.assertIsNotNone(report)
        self.assertEqual(report.status, ReportStatus.REVISED)

        versions = self.app.state.container.approval_repository.list_report_versions(
            task_id
        )
        self.assertEqual(len(versions), 2)
        self.assertEqual(versions[-1].status, ReportStatus.REVISED)

    async def test_revise_denied_without_permission(self) -> None:
        self._set_current_user(("approval.review",))
        await self._assert_permission_denied(
            method="POST",
            url="/api/v1/reports/task-unauthorized/revise",
            payload={"revision_reason": "Clarify source trace"},
            required_permission="approval.revise",
            resource_id="task-unauthorized",
            action="revise_approval",
        )

    async def test_missing_report_returns_error(self) -> None:
        response = await self.client.post(
            "/api/v1/reports/missing-task/submit-approval",
            json={"comment": "Ready"},
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"]["code"], "report_not_found")

    async def test_review_denied_without_permission(self) -> None:
        self._set_current_user(("report.read",))
        await self._assert_permission_denied(
            method="GET",
            url="/api/v1/approvals",
            payload=None,
            required_permission="approval.review",
            resource_id="all",
            action="list_approvals",
        )

        await self._assert_permission_denied(
            method="GET",
            url="/api/v1/approvals/approval-unauthorized",
            payload=None,
            required_permission="approval.review",
            resource_id="approval-unauthorized",
            action="get_approval",
        )

    async def test_list_and_get_approval(self) -> None:
        task_id = await self._create_report_task()
        submit = await self.client.post(
            f"/api/v1/reports/{task_id}/submit-approval", json={"comment": "Ready"}
        )
        approval_id = submit.json()["data"]["approval_id"]

        list_response = await self.client.get(
            "/api/v1/approvals", params={"task_id": task_id}
        )
        self.assertEqual(list_response.status_code, 200)
        items = list_response.json()["data"]["items"]
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["approval_id"], approval_id)

        get_response = await self.client.get(f"/api/v1/approvals/{approval_id}")
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()["data"]["approval_id"], approval_id)


if __name__ == "__main__":
    unittest.main()
