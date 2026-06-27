from __future__ import annotations

import asyncio
import unittest

import httpx

from app.config.settings import Settings
from app.main import create_app


class RetailInsightAPITest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        app = create_app(Settings(mock_step_delay_seconds=0, log_level="CRITICAL"))
        transport = httpx.ASGITransport(app=app)
        self.client = httpx.AsyncClient(transport=transport, base_url="http://test")

    async def asyncTearDown(self) -> None:
        await self.client.aclose()

    async def _create_task(self, mode: str = "hybrid") -> str:
        response = await self.client.post(
            "/api/tasks",
            json={"question": "売上と在庫の状況を分析してください", "mode": mode},
        )
        self.assertEqual(response.status_code, 202)
        return response.json()["task_id"]

    async def _wait_for_terminal_status(self, task_id: str) -> dict[str, object]:
        for _ in range(100):
            response = await self.client.get(f"/api/tasks/{task_id}")
            self.assertEqual(response.status_code, 200)
            payload = response.json()
            if payload["status"] in {"completed", "failed"}:
                return payload
            await asyncio.sleep(0.01)
        self.fail("Task did not reach a terminal status")

    async def test_health(self) -> None:
        response = await self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.headers["X-Request-ID"])
        self.assertEqual(response.json()["status"], "ok")
        self.assertEqual(response.json()["provider"], "mock")

    async def test_create_task(self) -> None:
        response = await self.client.post(
            "/api/tasks",
            json={"question": "会員と販促を分析してください", "mode": "hybrid"},
        )
        self.assertEqual(response.status_code, 202)
        payload = response.json()
        self.assertTrue(payload["task_id"])
        self.assertEqual(payload["status"], "queued")

    async def test_get_task_status(self) -> None:
        task_id = await self._create_task(mode="kpi")
        payload = await self._wait_for_terminal_status(task_id)
        self.assertEqual(payload["status"], "completed")
        self.assertIsNone(payload["error"])

    async def test_report_generation(self) -> None:
        task_id = await self._create_task(mode="hybrid")
        payload = await self._wait_for_terminal_status(task_id)
        self.assertEqual(payload["status"], "completed")

        response = await self.client.get(f"/api/tasks/{task_id}/report")
        self.assertEqual(response.status_code, 200)
        report = response.json()
        self.assertEqual(report["provider"], "mock")
        self.assertIn("# Retail Insight AI 経営分析レポート", report["markdown"])
        self.assertIn("## KPI サマリー", report["markdown"])
        self.assertIn("## Research サマリー", report["markdown"])

    async def test_sse_status_and_done_events(self) -> None:
        task_id = await self._create_task(mode="hybrid")
        response = await self.client.get(f"/api/tasks/{task_id}/events")
        self.assertEqual(response.status_code, 200)
        self.assertIn("event: status", response.text)
        self.assertIn("event: done", response.text)

    async def test_sse_error_event(self) -> None:
        app = create_app(
            Settings(
                mock_step_delay_seconds=0,
                mock_fail_research=True,
                log_level="CRITICAL",
            )
        )
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            create_response = await client.post(
                "/api/tasks",
                json={"question": "市場を調査してください", "mode": "research"},
            )
            task_id = create_response.json()["task_id"]
            status_response = await client.get(f"/api/tasks/{task_id}")
            self.assertEqual(status_response.json()["status"], "failed")
            event_response = await client.get(f"/api/tasks/{task_id}/events")
            self.assertIn("event: error", event_response.text)


if __name__ == "__main__":
    unittest.main()
