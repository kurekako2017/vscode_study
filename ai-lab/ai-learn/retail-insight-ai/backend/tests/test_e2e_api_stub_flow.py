"""最小企业业务 API E2E（Stub LLM，零真实外呼）。

可运行模式：
1) 进程内 ASGI + PostgreSQL（REPOSITORY_BACKEND=postgres + DATABASE_URL）
2) 对外部 BASE_URL（E2E_BASE_URL）发 HTTP（Compose 已 up 时）

不打印 Token / Key / 正文全文。
"""

from __future__ import annotations

import json
import os
import sys
import unittest
from decimal import Decimal
from uuid import uuid4

import httpx

from tests.auth_test_utils import (
    ADMIN_PASSWORD,
    ADMIN_USERNAME,
    EMPLOYEE_PASSWORD,
    EMPLOYEE_USERNAME,
    MANAGER_PASSWORD,
    MANAGER_USERNAME,
)


def _base_url() -> str | None:
    return os.environ.get("E2E_BASE_URL") or os.environ.get("BASE_URL")


def _use_remote() -> bool:
    return bool(_base_url())


class StubEnterpriseE2E(unittest.IsolatedAsyncioTestCase):
    """admin/employee/manager 主链：文档 → 检索 → AI分析 → 报告 → 审批。"""

    async def asyncSetUp(self) -> None:
        if _use_remote():
            self.remote = True
            self.base = _base_url().rstrip("/")
            self.client = httpx.AsyncClient(base_url=self.base, timeout=30.0)
            self.app = None
            return

        # 默认不在 InMemory 全量 suite 中强制跑 E2E，避免污染进程环境变量。
        backend = (os.environ.get("REPOSITORY_BACKEND") or "inmemory").lower()
        if backend != "postgres" and os.environ.get("RUN_API_E2E") != "1":
            self.skipTest(
                "API E2E is PostgreSQL-only; set REPOSITORY_BACKEND=postgres or RUN_API_E2E=1"
            )

        # 进程内：需要 PostgreSQL（不修改 os.environ，避免污染同进程其他用例）
        from app.config.settings import Settings
        from app.main import create_app
        from tests.postgres_test_utils import reset_postgres_state_if_needed

        database_url = os.environ.get("DATABASE_URL") or (
            "postgresql+psycopg:///erip_integration_test?host=/var/run/postgresql"
        )
        try:
            settings = Settings(
                repository_backend="postgres",
                llm_provider_mode="stub",
                log_level="CRITICAL",
                workflow_step_delay_seconds=0,
                database_url=database_url,
                _env_file=None,
            )
            reset_postgres_state_if_needed(settings)
            self.app = create_app(settings)
        except Exception as exc:  # noqa: BLE001
            self.skipTest(f"PostgreSQL unavailable: {type(exc).__name__}")
        self.remote = False
        self.client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=self.app),
            base_url="http://test",
            timeout=30.0,
        )

    async def asyncTearDown(self) -> None:
        await self.client.aclose()

    async def _login(self, username: str, password: str) -> str:
        response = await self.client.post(
            "/api/v1/auth/login",
            json={"username": username, "password": password},
        )
        self.assertEqual(response.status_code, 200, response.text[:200])
        token = response.json()["data"]["access_token"]
        self.assertTrue(token)
        # 绝不打印 token
        return token

    def _auth(self, token: str) -> dict[str, str]:
        return {"Authorization": f"Bearer {token}"}

    async def test_full_stub_enterprise_chain(self) -> None:
        # Health 匿名
        health = await self.client.get("/health")
        self.assertEqual(health.status_code, 200)
        health_text = health.text.lower()
        self.assertNotIn("api_key", health_text)
        self.assertNotIn("password", health_text)
        self.assertNotIn("secret", health_text)

        admin_token = await self._login(ADMIN_USERNAME, ADMIN_PASSWORD)
        employee_token = await self._login(EMPLOYEE_USERNAME, EMPLOYEE_PASSWORD)
        manager_token = await self._login(MANAGER_USERNAME, MANAGER_PASSWORD)

        # employee me
        me = await self.client.get("/api/v1/users/me", headers=self._auth(employee_token))
        self.assertEqual(me.status_code, 200)
        me_data = me.json().get("data") or me.json()
        self.assertEqual(me_data.get("username"), "employee")
        self.assertNotIn("access_token", json.dumps(me.json()).lower())

        # 上传文档
        meta = {
            "title": "E2E Sales Evidence",
            "description": "stub e2e",
            "owner": "analysis-team",
            "tags": ["e2e", "sales"],
            "language": "en",
        }
        files = {
            "file": ("e2e-sales.md", b"# Sales\n\nControlled e2e evidence about beverage sales decline in Kanto.", "text/markdown"),
            "metadata": (None, json.dumps(meta), "application/json"),
        }
        upload = await self.client.post(
            "/api/v1/documents",
            files=files,
            headers={**self._auth(employee_token), "Idempotency-Key": f"e2e-up-{uuid4().hex[:12]}"},
        )
        self.assertEqual(upload.status_code, 201, upload.text[:300])
        document_id = upload.json()["data"]["document_id"]

        # Import
        imp = await self.client.post(
            f"/api/v1/documents/{document_id}/import",
            headers=self._auth(employee_token),
        )
        self.assertIn(imp.status_code, {200, 201}, imp.text[:300])

        # Chunk
        chunk_resp = await self.client.post(
            f"/api/v1/documents/{document_id}/chunks",
            headers=self._auth(employee_token),
        )
        self.assertIn(chunk_resp.status_code, {200, 201}, chunk_resp.text[:300])
        chunk_data = chunk_resp.json().get("data") or chunk_resp.json()
        items = chunk_data.get("items") or chunk_data.get("chunks") or []
        if not items:
            # list chunks
            listed = await self.client.get(
                f"/api/v1/documents/{document_id}/chunks",
                headers=self._auth(employee_token),
            )
            self.assertEqual(listed.status_code, 200, listed.text[:300])
            items = (listed.json().get("data") or listed.json()).get("items") or []
        self.assertGreaterEqual(len(items), 1)
        chunk_id = items[0].get("chunk_id") or items[0].get("id")
        self.assertTrue(chunk_id)

        # Retrieval
        retrieval = await self.client.post(
            "/api/v1/document-retrieval/search",
            json={"query": "beverage sales decline Kanto", "limit": 5},
            headers=self._auth(employee_token),
        )
        self.assertEqual(retrieval.status_code, 200, retrieval.text[:300])
        results = (retrieval.json().get("data") or retrieval.json()).get("results") or []
        self.assertGreaterEqual(len(results), 1)
        evidence_doc = results[0]["document_id"]
        evidence_chunk = results[0]["chunk_id"]
        score = results[0].get("score", 0.9)

        # Internal RAG 不触发 LLM provider（进程内可验证 call_count）
        rag = await self.client.post(
            "/api/v1/internal-rag/answer",
            json={
                "question": "Why did sales decline?",
                "answer_mode": "extractive",
                "require_citations": True,
                "limit": 3,
            },
            headers=self._auth(employee_token),
        )
        self.assertIn(rag.status_code, {200, 422}, rag.text[:300])
        if self.app is not None:
            self.assertEqual(self.app.state.container.llm_provider.call_count, 0)

        # AI Analysis stub low_cost
        analysis = await self.client.post(
            "/api/v1/ai-analysis",
            json={
                "question": "Summarize beverage sales decline evidence",
                "evidence": [
                    {
                        "document_id": evidence_doc,
                        "chunk_id": evidence_chunk,
                        "score": str(score) if not isinstance(score, str) else score,
                    }
                ],
                "confirmed": True,
            },
            headers={
                **self._auth(employee_token),
                "Idempotency-Key": f"e2e-ai-{uuid4().hex[:12]}",
            },
        )
        self.assertEqual(analysis.status_code, 200, analysis.text[:400])
        analysis_data = analysis.json()["data"]
        self.assertEqual(analysis_data["route_tier"], "low_cost")
        self.assertTrue(str(analysis_data["provider"]).startswith("stub"))
        self.assertGreater(analysis_data["usage"]["total_tokens"], 0)
        Decimal(str(analysis_data["cost"]))
        analysis_id = analysis_data["analysis_id"]
        if self.app is not None:
            self.assertGreaterEqual(self.app.state.container.llm_provider.call_count, 1)

        # Executive report high_quality
        report = await self.client.post(
            "/api/v1/executive-reports",
            json={
                "ai_analysis_id": analysis_id,
                "title": "E2E Board Report",
                "confirmed": True,
            },
            headers={
                **self._auth(employee_token),
                "Idempotency-Key": f"e2e-er-{uuid4().hex[:12]}",
            },
        )
        self.assertEqual(report.status_code, 200, report.text[:400])
        report_data = report.json()["data"]
        self.assertEqual(report_data["route_tier"], "high_quality")
        self.assertTrue(str(report_data["provider"]).startswith("stub"))
        task_id = report_data["task_id"]
        report_version_id = report_data["report_version_id"]
        self.assertTrue(task_id)
        self.assertTrue(report_version_id)

        # employee submit approval
        submit = await self.client.post(
            f"/api/v1/reports/{task_id}/submit-approval",
            json={"comment": "please review"},
            headers=self._auth(employee_token),
        )
        # some APIs use empty body
        if submit.status_code == 422:
            submit = await self.client.post(
                f"/api/v1/reports/{task_id}/submit-approval",
                headers=self._auth(employee_token),
            )
        self.assertIn(submit.status_code, {200, 201}, submit.text[:400])
        approval = submit.json().get("data") or submit.json()
        approval_id = approval.get("approval_id") or approval.get("id")
        self.assertTrue(approval_id)

        # employee cannot approve
        denied = await self.client.post(
            f"/api/v1/approvals/{approval_id}/approve",
            json={"comment": "employee should fail"},
            headers=self._auth(employee_token),
        )
        self.assertEqual(denied.status_code, 403, denied.text[:300])

        # manager can review/approve
        listed = await self.client.get(
            "/api/v1/approvals",
            headers=self._auth(manager_token),
        )
        self.assertEqual(listed.status_code, 200, listed.text[:300])
        approved = await self.client.post(
            f"/api/v1/approvals/{approval_id}/approve",
            json={"comment": "manager approved e2e"},
            headers=self._auth(manager_token),
        )
        self.assertEqual(approved.status_code, 200, approved.text[:400])

        # unknown role fail-closed: use garbage token
        bad = await self.client.get(
            "/api/v1/approvals",
            headers={"Authorization": "Bearer not-a-jwt"},
        )
        self.assertEqual(bad.status_code, 401)

        # admin can read audit
        audit = await self.client.get(
            "/api/v1/audit-logs",
            headers=self._auth(admin_token),
        )
        self.assertEqual(audit.status_code, 200, audit.text[:300])
        audit_payload = json.dumps(audit.json())
        self.assertNotIn("Employee#2026", audit_payload)
        self.assertNotIn("Bearer ", audit_payload)

        # Ledger exists (process-local)
        if self.app is not None:
            factory = self.app.state.container.audit_repository._connection_factory
            with factory.connection() as connection, connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM llm_usage_ledger WHERE status='succeeded'")
                self.assertGreaterEqual(cursor.fetchone()[0], 2)
                # attempt table may be empty in stub single-provider path
                cursor.execute(
                    "SELECT to_regclass('public.llm_provider_attempts'), to_regclass('public.llm_usage_ledger')"
                )
                rows = cursor.fetchone()
                self.assertIsNotNone(rows[1])


if __name__ == "__main__":
    # 允许脚本直接执行
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(StubEnterpriseE2E)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
