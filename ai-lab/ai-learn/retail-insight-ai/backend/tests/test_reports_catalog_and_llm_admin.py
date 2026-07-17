"""报告目录与 LLM 管理 API 的最小回归。"""

from __future__ import annotations

import unittest

from httpx import ASGITransport, AsyncClient

from app.config.settings import Settings
from app.main import create_app
from app.models.report import Report, ReportStatus
from tests.auth_test_utils import (
    ADMIN_PASSWORD,
    ADMIN_USERNAME,
    EMPLOYEE_PASSWORD,
    EMPLOYEE_USERNAME,
    authorization_headers,
)


class ReportsCatalogAndLlmAdminTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.app = create_app(
            Settings(repository_backend="inmemory", llm_provider_mode="stub", learning_trace=False)
        )
        self.client = AsyncClient(
            transport=ASGITransport(app=self.app),
            base_url="http://test",
        )

    async def asyncTearDown(self) -> None:
        await self.client.aclose()

    async def test_report_catalog_lists_task_ids_for_submitter(self) -> None:
        self.app.state.container.report_repository.save(
            Report(
                task_id="task-catalog-1",
                markdown="# hello board",
                provider="stub-high-quality",
                status=ReportStatus.GENERATED,
            )
        )
        headers = authorization_headers(
            self.app, username=EMPLOYEE_USERNAME, password=EMPLOYEE_PASSWORD
        )
        response = await self.client.get("/api/v1/reports", headers=headers)
        self.assertEqual(response.status_code, 200, response.text)
        items = response.json()["data"]["items"]
        self.assertTrue(any(item["task_id"] == "task-catalog-1" for item in items))
        self.assertNotIn("password", response.text.lower())

    async def test_llm_runtime_admin_only(self) -> None:
        employee = authorization_headers(
            self.app, username=EMPLOYEE_USERNAME, password=EMPLOYEE_PASSWORD
        )
        denied = await self.client.get("/api/v1/admin/llm/runtime", headers=employee)
        self.assertIn(denied.status_code, {401, 403})

        admin = authorization_headers(
            self.app, username=ADMIN_USERNAME, password=ADMIN_PASSWORD
        )
        ok = await self.client.get("/api/v1/admin/llm/runtime", headers=admin)
        self.assertEqual(ok.status_code, 200, ok.text)
        data = ok.json()["data"]
        self.assertEqual(data["llm_provider_mode"], "stub")
        self.assertFalse(data["run_real_llm_smoke"])
        self.assertNotIn("api_key", ok.text.lower())

        put = await self.client.put(
            "/api/v1/admin/llm/runtime",
            headers=admin,
            json={"llm_provider_mode": "stub"},
        )
        self.assertEqual(put.status_code, 200, put.text)
        self.assertEqual(put.json()["data"]["llm_provider_mode"], "stub")


if __name__ == "__main__":
    unittest.main()
