"""PostgreSQL Executive Report 双路由、额度分离、Report 与零调用测试。"""

from __future__ import annotations

import unittest
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from uuid import uuid4

import httpx

from app.config.settings import Settings
from app.main import create_app
from app.models.document import Document, DocumentChunk, DocumentMetadata
from app.models.report import ReportStatus
from app.schemas.executive_report_api import ExecutiveReportRequest
from app.security.contracts import CurrentUser
from app.services.persistent_audit_service import PersistentAuditContext
from tests.auth_test_utils import EMPLOYEE_PASSWORD, EMPLOYEE_USERNAME, authorization_headers
from tests.postgres_test_utils import reset_postgres_state_if_needed


class ExecutiveReportPostgresAPITest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.settings = Settings(log_level="CRITICAL", workflow_step_delay_seconds=0)
        if self.settings.repository_backend != "postgres":
            self.skipTest("PostgreSQL-only executive report integration tests")
        reset_postgres_state_if_needed(self.settings)
        self.app = create_app(self.settings)
        self.client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=self.app),
            base_url="http://test",
            headers=authorization_headers(
                self.app, username=EMPLOYEE_USERNAME, password=EMPLOYEE_PASSWORD,
            ),
        )
        self.document_id, self.chunk_id = self._seed_evidence("Board-ready controlled evidence")

    async def asyncTearDown(self) -> None:
        if hasattr(self, "client"):
            await self.client.aclose()

    def _seed_evidence(self, content: str) -> tuple[str, str]:
        document_id = f"doc-{uuid4().hex}"
        metadata = DocumentMetadata.from_mapping({
            "document_id": document_id, "title": "Board evidence", "owner": "analysis-team",
            "language": "en", "document_type": "text", "status": "uploaded",
            "source": {"source_type": "test", "uri": f"test://{document_id}"},
            "checksum": f"sha256:{uuid4().hex}",
        })
        document = Document.create(content, metadata)
        chunk_id = f"chk-{uuid4().hex}"
        chunk = DocumentChunk(document_id, 1, chunk_id, 0, content, len(content), metadata)
        self.app.state.container.document_repository.create(document)
        self.app.state.container.document_chunk_repository.replace_for_document(document_id, 1, [chunk])
        return document_id, chunk_id

    def _analysis_payload(self, **overrides):
        payload = {
            "question": "Summarize board evidence",
            "evidence": [{"document_id": self.document_id, "chunk_id": self.chunk_id, "score": "0.93"}],
            "confirmed": True,
        }
        payload.update(overrides)
        return payload

    async def _create_analysis(self, key: str = "er-analysis-base-01") -> str:
        response = await self.client.post(
            "/api/v1/ai-analysis",
            json=self._analysis_payload(),
            headers={"Idempotency-Key": key, "X-Request-ID": f"req-{key}"},
        )
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()["data"]["analysis_id"]

    async def _post_report(self, analysis_id: str, key: str = "er-report-base-01", **overrides):
        payload = {
            "ai_analysis_id": analysis_id,
            "title": "Board Report Q1",
            "confirmed": True,
        }
        payload.update(overrides)
        return await self.client.post(
            "/api/v1/executive-reports",
            json=payload,
            headers={"Idempotency-Key": key, "X-Request-ID": f"req-{key}"},
        )

    async def test_routes_to_high_quality_and_not_low_cost(self) -> None:
        analysis_id = await self._create_analysis()
        low_before = self.app.state.container.llm_provider.call_count
        hq_before = self.app.state.container.llm_provider_high_quality.call_count
        response = await self._post_report(analysis_id)
        self.assertEqual(response.status_code, 200, response.text)
        data = response.json()["data"]
        self.assertEqual(data["provider"], "stub-high-quality")
        self.assertEqual(data["model"], "stub-high-quality-v1")
        self.assertEqual(data["route_tier"], "high_quality")
        self.assertEqual(self.app.state.container.llm_provider.call_count, low_before)
        self.assertEqual(self.app.state.container.llm_provider_high_quality.call_count, hq_before + 1)
        self.assertTrue(data["report_id"])
        self.assertTrue(data["report_version_id"])
        self.assertTrue(data["executive_summary"])
        self.assertGreater(len(data["kpi_findings"]), 0)
        Decimal(data["actual_cost"])

    async def test_ai_analysis_never_enters_high_quality_stub(self) -> None:
        hq_before = self.app.state.container.llm_provider_high_quality.call_count
        response = await self.client.post(
            "/api/v1/ai-analysis",
            json=self._analysis_payload(),
            headers={"Idempotency-Key": "er-low-only-0001", "X-Request-ID": "req-er-low-only"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["provider"], "stub-low-cost")
        self.assertEqual(self.app.state.container.llm_provider_high_quality.call_count, hq_before)

    async def test_client_cannot_select_provider_model_or_tier(self) -> None:
        analysis_id = await self._create_analysis("er-client-fields-01")
        forged = await self.client.post(
            "/api/v1/executive-reports",
            json={
                "ai_analysis_id": analysis_id,
                "title": "Forged",
                "confirmed": True,
                "provider": "real-vendor",
                "model": "gpt-x",
                "route_tier": "low_cost",
            },
            headers={"Idempotency-Key": "er-forged-fields-01"},
        )
        self.assertEqual(forged.status_code, 422)
        self.assertEqual(self.app.state.container.llm_provider_high_quality.call_count, 0)

    async def test_requires_succeeded_analysis_and_never_calls_without_it(self) -> None:
        missing = await self._post_report("ana-missing", "er-missing-analysis")
        self.assertEqual(missing.status_code, 422)
        self.assertEqual(missing.json()["error"]["code"], "executive_report_analysis_required")
        self.assertEqual(self.app.state.container.llm_provider_high_quality.call_count, 0)

    async def test_unconfirmed_and_archived_evidence_zero_call(self) -> None:
        analysis_id = await self._create_analysis("er-gates-analysis")
        unconfirmed = await self._post_report(analysis_id, "er-unconfirmed", confirmed=False)
        document = self.app.state.container.document_repository.get(self.document_id)
        assert document is not None
        document.archive()
        self.app.state.container.document_repository.update(document)
        archived = await self._post_report(analysis_id, "er-archived")
        self.assertEqual(unconfirmed.status_code, 422)
        self.assertEqual(archived.status_code, 422)
        self.assertEqual(self.app.state.container.llm_provider_high_quality.call_count, 0)

    async def test_high_quality_quota_is_independent_of_low_cost(self) -> None:
        limited = self.settings.model_copy(update={
            "llm_hq_user_daily_request_limit": 1,
            "llm_user_daily_request_limit": 50,
        })
        reset_postgres_state_if_needed(limited)
        await self.client.aclose()
        self.app = create_app(limited)
        self.client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=self.app), base_url="http://test",
            headers=authorization_headers(self.app, username=EMPLOYEE_USERNAME, password=EMPLOYEE_PASSWORD),
        )
        self.document_id, self.chunk_id = self._seed_evidence("quota separation evidence")
        first_analysis = await self._create_analysis("er-quota-a1")
        second_analysis = await self._create_analysis("er-quota-a2")
        first = await self._post_report(first_analysis, "er-quota-r1")
        second = await self._post_report(second_analysis, "er-quota-r2")
        third_analysis = await self._create_analysis("er-quota-a3")
        self.assertEqual(first.status_code, 200, first.text)
        self.assertEqual(second.status_code, 429, second.text)
        self.assertEqual(third_analysis, third_analysis)
        self.assertEqual(self.app.state.container.llm_provider.call_count, 3)
        self.assertEqual(self.app.state.container.llm_provider_high_quality.call_count, 1)

    async def test_idempotent_report_does_not_duplicate_version_or_provider_call(self) -> None:
        analysis_id = await self._create_analysis("er-idem-analysis")
        first = await self._post_report(analysis_id, "er-idem-report")
        second = await self._post_report(analysis_id, "er-idem-report")
        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(first.json()["data"]["report_version_id"], second.json()["data"]["report_version_id"])
        self.assertEqual(self.app.state.container.llm_provider_high_quality.call_count, 1)
        versions = self.app.state.container.approval_repository.list_report_versions(first.json()["data"]["task_id"])
        self.assertEqual(len(versions), 1)

    async def test_report_can_enter_approval_submit_without_auto_submit(self) -> None:
        analysis_id = await self._create_analysis("er-approval-analysis")
        report = await self._post_report(analysis_id, "er-approval-report")
        self.assertEqual(report.status_code, 200)
        task_id = report.json()["data"]["task_id"]
        current = self.app.state.container.report_repository.get(task_id)
        assert current is not None
        self.assertEqual(current.status, ReportStatus.GENERATED)
        approvals_before = self.app.state.container.approval_repository.list_approval_requests(task_id=task_id)
        self.assertEqual(approvals_before, [])
        submitted = await self.client.post(
            f"/api/v1/reports/{task_id}/submit-approval", json={"comment": "ready"},
        )
        self.assertIn(submitted.status_code, {200, 201}, submitted.text)
        self.assertEqual(submitted.json()["data"]["status"], "pending_approval")
        self.assertEqual(self.app.state.container.llm_provider_high_quality.call_count, 1)

    async def test_permission_denied_zero_call(self) -> None:
        analysis_id = await self._create_analysis("er-denied-analysis")
        unknown = CurrentUser(user_id="unknown-user", username="unknown", role="unknown-role")
        token = self.app.state.container.jwt_service.create_access_token(unknown)
        denied = await self.client.post(
            "/api/v1/executive-reports",
            json={"ai_analysis_id": analysis_id, "title": "Denied", "confirmed": True},
            headers={"Authorization": f"Bearer {token.access_token}", "Idempotency-Key": "er-denied-01"},
        )
        self.assertEqual(denied.status_code, 403)
        self.assertEqual(self.app.state.container.llm_provider_high_quality.call_count, 0)

    async def test_provider_failures_settle_and_single_audit(self) -> None:
        analysis_id = await self._create_analysis("er-fail-analysis")
        for index, (behavior, status, code) in enumerate((
            ("timeout", 504, "provider_timeout"),
            ("failure", 502, "provider_failed"),
            ("rate_limit", 429, "provider_rate_limited"),
            ("partial_failure", 502, "provider_failed"),
        )):
            self.app.state.container.llm_provider_high_quality.behavior = behavior
            response = await self._post_report(analysis_id, f"er-provider-fail-{index:02d}", title=f"Fail {index}")
            self.assertEqual(response.status_code, status)
            self.assertEqual(response.json()["error"]["code"], code)
        self.app.state.container.llm_provider_high_quality.behavior = "success"
        factory = self.app.state.container.audit_repository._connection_factory
        with factory.connection() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM llm_usage_ledger WHERE operation='executive_report' AND status='failed'")
            self.assertEqual(cursor.fetchone()[0], 4)
            cursor.execute("SELECT COUNT(*) FROM audit_logs WHERE operation_type='executive_report.failed'")
            self.assertEqual(cursor.fetchone()[0], 4)

    async def test_policy_snapshot_and_route_tier_persisted(self) -> None:
        analysis_id = await self._create_analysis("er-policy-analysis")
        response = await self._post_report(analysis_id, "er-policy-report")
        self.assertEqual(response.status_code, 200)
        factory = self.app.state.container.audit_repository._connection_factory
        with factory.connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                """SELECT operation,route_tier,selected_provider,selected_model,
                policy_snapshot->>'route_tier',price_snapshot->>'currency',report_id,report_version_id
                FROM llm_usage_ledger WHERE operation='executive_report' AND status='succeeded'"""
            )
            row = cursor.fetchone()
            self.assertEqual(row[0:4], ("executive_report", "high_quality", "stub-high-quality", "stub-high-quality-v1"))
            self.assertEqual(row[4], "high_quality")
            self.assertEqual(row[5], "USD")
            self.assertTrue(row[6] and row[7])

    async def test_restart_recovers_idempotent_report_without_provider_call(self) -> None:
        analysis_id = await self._create_analysis("er-restart-analysis")
        first = await self._post_report(analysis_id, "er-restart-report")
        self.assertEqual(first.status_code, 200)
        await self.client.aclose()
        self.app = create_app(self.settings)
        self.client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=self.app), base_url="http://test",
            headers=authorization_headers(self.app, username=EMPLOYEE_USERNAME, password=EMPLOYEE_PASSWORD),
        )
        second = await self._post_report(analysis_id, "er-restart-report")
        self.assertEqual(second.status_code, 200)
        self.assertEqual(first.json()["data"]["report_version_id"], second.json()["data"]["report_version_id"])
        self.assertEqual(self.app.state.container.llm_provider_high_quality.call_count, 0)

    async def test_concurrent_same_key_calls_provider_at_most_once(self) -> None:
        analysis_id = await self._create_analysis("er-concurrent-analysis")
        service = self.app.state.container.executive_report_service
        actor = CurrentUser(user_id="user-employee", username="employee", role="employee")
        payload = ExecutiveReportRequest.model_validate({
            "ai_analysis_id": analysis_id, "title": "Concurrent Board", "confirmed": True,
        })

        def execute(index: int):
            try:
                return service.execute(
                    payload, actor=actor, idempotency_key="er-concurrent-key-01",
                    context=PersistentAuditContext(
                        request_id=f"er-concurrent-{index}", http_method="POST",
                        api_path="/api/v1/executive-reports", resource_id="executive-report",
                        current_user=actor,
                    ),
                )
            except Exception as exc:
                return exc

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(execute, (1, 2)))
        self.assertEqual(self.app.state.container.llm_provider_high_quality.call_count, 1)
        self.assertGreaterEqual(sum(hasattr(item, "report_version_id") for item in results), 1)

    async def test_ordinary_business_paths_do_not_call_either_provider(self) -> None:
        low_before = self.app.state.container.llm_provider.call_count
        hq_before = self.app.state.container.llm_provider_high_quality.call_count
        rag = await self.client.post("/api/v1/internal-rag/answer", json={
            "question": "Board-ready controlled evidence", "limit": 5,
            "answer_mode": "extractive", "require_citations": True,
        })
        retrieval = await self.client.post("/api/v1/document-retrieval/search", json={
            "query": "Board-ready controlled evidence", "limit": 5,
        })
        self.assertIn(rag.status_code, {200, 422})
        self.assertEqual(retrieval.status_code, 200)
        self.assertEqual(self.app.state.container.llm_provider.call_count, low_before)
        self.assertEqual(self.app.state.container.llm_provider_high_quality.call_count, hq_before)

    async def test_unknown_operation_fail_closed_at_gateway(self) -> None:
        with self.assertRaises(LookupError):
            self.app.state.container.llm_gateway.policy_for("billing_invoice")
        with self.assertRaises(LookupError):
            self.app.state.container.llm_gateway.resolve_provider("unknown_op")


if __name__ == "__main__":
    unittest.main()
