from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import httpx

from app.config.settings import Settings
from app.main import create_app


class KnowledgeApprovalAPITest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        settings = Settings(
            database_path=Path(self.temp_dir.name) / "test.db",
            workflow_step_delay_seconds=0,
            log_level="CRITICAL",
        )
        self.app = create_app(settings)
        self.client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=self.app),
            base_url="http://test",
        )

    async def asyncTearDown(self) -> None:
        await self.client.aclose()
        self.temp_dir.cleanup()

    async def create_question(self, question: str) -> dict[str, object]:
        response = await self.client.post(
            "/api/questions",
            headers={"X-Request-ID": "test-create-request"},
            json={"question": question},
        )
        self.assertEqual(response.status_code, 202)
        return response.json()["data"]

    async def test_health(self) -> None:
        response = await self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        self.assertTrue(response.headers["X-Request-ID"])

    async def test_low_risk_question_completes_without_approval(self) -> None:
        created = await self.create_question("休暇申請の手順を確認したい")
        question_id = created["question_id"]

        state = (await self.client.get(f"/api/questions/{question_id}")).json()["data"]
        self.assertEqual(state["status"], "completed")
        self.assertEqual(state["risk_level"], "LOW")
        self.assertIsNone(state["approval_id"])

        events = await self.client.get(f"/api/questions/{question_id}/events")
        self.assertIn("event: received", events.text)
        self.assertIn("event: risk_checked", events.text)
        self.assertIn("event: answer_generated", events.text)
        self.assertIn("event: completed", events.text)

        report = await self.client.get(f"/api/questions/{question_id}/report")
        self.assertEqual(report.status_code, 200)
        self.assertIn("低リスク判定により自動確定", report.json()["data"]["report"])

    async def test_high_risk_question_waits_for_approval_then_completes(self) -> None:
        created = await self.create_question("個人情報を含む障害ログの共有手順")
        question_id = created["question_id"]

        state = (await self.client.get(f"/api/questions/{question_id}")).json()["data"]
        self.assertEqual(state["status"], "approval_required")
        self.assertEqual(state["risk_level"], "HIGH")
        approval_id = state["approval_id"]
        self.assertTrue(approval_id)

        approvals = (await self.client.get("/api/approvals")).json()["data"]
        self.assertEqual([item["approval_id"] for item in approvals], [approval_id])

        approved = await self.client.post(f"/api/approvals/{question_id}/approve")
        self.assertEqual(approved.status_code, 200)
        self.assertEqual(approved.json()["data"]["status"], "approved")

        final_state = (await self.client.get(f"/api/questions/{question_id}")).json()["data"]
        self.assertEqual(final_state["status"], "completed")
        report = await self.client.get(f"/api/questions/{question_id}/report")
        self.assertIn("承認者による確認済み", report.json()["data"]["report"])

        events = await self.client.get(f"/api/questions/{question_id}/events")
        self.assertIn("event: approval_required", events.text)
        self.assertIn("event: approved", events.text)
        self.assertIn("event: completed", events.text)

    async def test_rejected_question_has_no_report(self) -> None:
        created = await self.create_question("契約内容を確認したい")
        question_id = created["question_id"]
        state = (await self.client.get(f"/api/questions/{question_id}")).json()["data"]

        rejected = await self.client.post(f"/api/approvals/{question_id}/reject")
        self.assertEqual(rejected.status_code, 200)
        final_state = (await self.client.get(f"/api/questions/{question_id}")).json()["data"]
        self.assertEqual(final_state["status"], "rejected")

        report = await self.client.get(f"/api/questions/{question_id}/report")
        self.assertEqual(report.status_code, 409)
        self.assertEqual(report.json()["error"]["code"], "REPORT_NOT_READY")

    async def test_duplicate_approval_returns_conflict(self) -> None:
        created = await self.create_question("セキュリティ設定を確認したい")
        state = (await self.client.get(f"/api/questions/{created['question_id']}")).json()["data"]
        self.assertEqual((await self.client.post(f"/api/approvals/{created['question_id']}/approve")).status_code, 200)
        duplicate = await self.client.post(f"/api/approvals/{created['question_id']}/approve")
        self.assertEqual(duplicate.status_code, 409)
        self.assertEqual(duplicate.json()["error"]["code"], "APPROVAL_CONFLICT")

    async def test_question_not_found(self) -> None:
        response = await self.client.get("/api/questions/not-found")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"]["code"], "RESOURCE_NOT_FOUND")

    async def test_all_required_risk_keywords_require_approval(self) -> None:
        for keyword in ("契約", "個人情報", "セキュリティ", "経費", "法務", "障害対応", "退職", "給与"):
            created = await self.create_question(f"{keyword}について確認したい")
            state = (await self.client.get(f"/api/questions/{created['question_id']}")).json()["data"]
            self.assertEqual(state["status"], "approval_required", keyword)
            self.assertEqual(state["risk_level"], "HIGH", keyword)


if __name__ == "__main__":
    unittest.main()
