from __future__ import annotations

import asyncio
import json
import unittest

import httpx

from app.config.settings import Settings
from app.main import create_app


class RetailInsightAPITest(unittest.IsolatedAsyncioTestCase):
    """验证普通 API envelope、Workflow 终态与 SSE 合同。"""

    async def asyncSetUp(self) -> None:
        self.app = create_app(
            Settings(workflow_step_delay_seconds=0, log_level="CRITICAL")
        )
        transport = httpx.ASGITransport(app=self.app)
        self.client = httpx.AsyncClient(transport=transport, base_url="http://test")

    async def asyncTearDown(self) -> None:
        await self.client.aclose()

    async def _create_task(self, mode: str = "hybrid") -> str:
        response = await self.client.post(
            "/api/tasks",
            headers={"X-Request-ID": "create-request"},
            json={"question": "売上と在庫の状況を分析してください", "mode": mode},
        )
        self.assertEqual(response.status_code, 202)
        payload = response.json()
        self.assertTrue(payload["success"])
        self.assertIsNone(payload["error"])
        return payload["data"]["task_id"]

    async def _wait_for_terminal_status(self, task_id: str) -> dict[str, object]:
        for _ in range(100):
            response = await self.client.get(f"/api/tasks/{task_id}")
            self.assertEqual(response.status_code, 200)
            payload = response.json()["data"]
            if payload["status"] in {"completed", "failed"}:
                return payload
            await asyncio.sleep(0.01)
        self.fail("Task did not reach a terminal status")

    async def test_health_keeps_simple_contract_with_request_id(self) -> None:
        response = await self.client.get("/health", headers={"X-Request-ID": "health-request"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["X-Request-ID"], "health-request")
        self.assertEqual(response.json()["status"], "ok")
        self.assertEqual(response.json()["provider"], "static")
        self.assertEqual(response.json()["request_id"], "health-request")

    async def test_create_task_uses_success_envelope(self) -> None:
        response = await self.client.post(
            "/api/tasks",
            headers={"X-Request-ID": "task-envelope-request"},
            json={"question": "会員と販促を分析してください", "mode": "hybrid"},
        )
        self.assertEqual(response.status_code, 202)
        payload = response.json()
        self.assertEqual(payload["request_id"], "task-envelope-request")
        self.assertTrue(payload["success"])
        self.assertEqual(payload["data"]["status"], "queued")
        self.assertIsNone(payload["error"])

    async def test_get_task_status_uses_success_envelope(self) -> None:
        task_id = await self._create_task(mode="kpi")
        payload = await self._wait_for_terminal_status(task_id)
        self.assertEqual(payload["status"], "completed")
        self.assertIsNone(payload["error"])

    async def test_report_generation_uses_success_envelope(self) -> None:
        task_id = await self._create_task(mode="hybrid")
        await self._wait_for_terminal_status(task_id)

        response = await self.client.get(f"/api/tasks/{task_id}/report")
        self.assertEqual(response.status_code, 200)
        envelope = response.json()
        self.assertTrue(envelope["success"])
        report = envelope["data"]
        self.assertEqual(report["provider"], "static")
        self.assertIn("# Retail Insight AI 経営分析レポート", report["markdown"])
        self.assertIn("## KPI サマリー", report["markdown"])
        self.assertIn("## Research サマリー", report["markdown"])

    async def test_validation_failure_uses_error_envelope(self) -> None:
        response = await self.client.post(
            "/api/tasks",
            headers={"X-Request-ID": "validation-request"},
            json={"question": "", "mode": "hybrid"},
        )
        self.assertEqual(response.status_code, 422)
        payload = response.json()
        self.assertFalse(payload["success"])
        self.assertEqual(payload["request_id"], "validation-request")
        self.assertIsNone(payload["data"])
        self.assertEqual(payload["error"]["code"], "VALIDATION_ERROR")
        self.assertTrue(payload["error"]["detail"]["errors"])

    async def test_task_not_found_uses_error_envelope(self) -> None:
        response = await self.client.get(
            "/api/tasks/missing-task",
            headers={"X-Request-ID": "missing-task-request"},
        )
        self.assertEqual(response.status_code, 404)
        payload = response.json()
        self.assertFalse(payload["success"])
        self.assertEqual(payload["request_id"], "missing-task-request")
        self.assertEqual(payload["error"]["code"], "TASK_NOT_FOUND")
        self.assertEqual(payload["error"]["detail"]["task_id"], "missing-task")

    async def test_report_not_found_uses_error_envelope(self) -> None:
        task = self.app.state.container.task_service.create_task("在庫を確認", "kpi")
        response = await self.client.get(f"/api/tasks/{task.task_id}/report")
        self.assertEqual(response.status_code, 409)
        payload = response.json()
        self.assertFalse(payload["success"])
        self.assertEqual(payload["error"]["code"], "REPORT_NOT_FOUND")

    async def test_sse_status_and_done_events(self) -> None:
        task_id = await self._create_task(mode="hybrid")
        response = await self.client.get(f"/api/tasks/{task_id}/events")
        self.assertEqual(response.status_code, 200)
        self.assertIn("event: status", response.text)
        self.assertIn("event: done", response.text)
        self.assertNotIn("event: error", response.text)

    async def test_sse_error_event_has_standard_fields_and_no_done(self) -> None:
        app = create_app(
            Settings(
                workflow_step_delay_seconds=0,
                static_research_fail=True,
                log_level="CRITICAL",
            )
        )
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            create_response = await client.post(
                "/api/tasks",
                headers={"X-Request-ID": "failed-task-request"},
                json={"question": "市場を調査してください", "mode": "research"},
            )
            task_id = create_response.json()["data"]["task_id"]
            status_response = await client.get(f"/api/tasks/{task_id}")
            self.assertEqual(status_response.json()["data"]["status"], "failed")

            event_response = await client.get(f"/api/tasks/{task_id}/events")
            self.assertIn("event: error", event_response.text)
            self.assertNotIn("event: done", event_response.text)
            payloads = [
                json.loads(line.removeprefix("data: "))
                for line in event_response.text.splitlines()
                if line.startswith("data: ")
            ]
            error_event = next(item for item in payloads if item["event"] == "error")
            self.assertEqual(error_event["task_id"], task_id)
            self.assertEqual(error_event["status"], "failed")
            self.assertEqual(error_event["error_code"], "RESEARCH_PROVIDER_ERROR")
            self.assertEqual(error_event["message"], "Research provider failed")
            self.assertEqual(error_event["request_id"], "failed-task-request")


if __name__ == "__main__":
    unittest.main()
