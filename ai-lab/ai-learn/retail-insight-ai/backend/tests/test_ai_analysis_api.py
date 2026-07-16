"""PostgreSQL AI Analysis 成本、幂等、Evidence 与 Audit 集成测试。"""

from __future__ import annotations

import asyncio
import unittest
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from uuid import uuid4

import httpx

from app.config.settings import Settings
from app.main import create_app
from app.models.document import Document, DocumentChunk, DocumentMetadata
from app.schemas.ai_analysis_api import AIAnalysisRequest
from app.security.contracts import CurrentUser
from app.services.persistent_audit_service import PersistentAuditContext
from tests.auth_test_utils import EMPLOYEE_PASSWORD, EMPLOYEE_USERNAME, authorization_headers
from tests.postgres_test_utils import reset_postgres_state_if_needed


class AIAnalysisPostgresAPITest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.settings = Settings(log_level="CRITICAL", workflow_step_delay_seconds=0)
        if self.settings.repository_backend != "postgres":
            self.skipTest("PostgreSQL-only AI analysis integration tests")
        reset_postgres_state_if_needed(self.settings)
        self.app = create_app(self.settings)
        self.client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=self.app), base_url="http://test",
            headers=authorization_headers(self.app, username=EMPLOYEE_USERNAME, password=EMPLOYEE_PASSWORD),
        )
        self.document_id, self.chunk_id = self._seed_evidence("Controlled enterprise evidence")

    async def asyncTearDown(self) -> None:
        if hasattr(self, "client"):
            await self.client.aclose()

    def _seed_evidence(self, content: str) -> tuple[str, str]:
        document_id = f"doc-{uuid4().hex}"
        metadata = DocumentMetadata.from_mapping({
            "document_id": document_id, "title": "AI evidence", "owner": "analysis-team",
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

    def _payload(self, **overrides):
        payload = {
            "question": "Summarize the controlled evidence",
            "evidence": [{"document_id": self.document_id, "chunk_id": self.chunk_id, "score": "0.91"}],
            "confirmed": True,
        }
        payload.update(overrides)
        return payload

    async def _post(self, key: str = "ai-idempotency-0001", **overrides):
        return await self.client.post("/api/v1/ai-analysis", json=self._payload(**overrides),
                                      headers={"Idempotency-Key": key, "X-Request-ID": f"req-{key}"})

    async def test_success_persists_decimal_usage_result_and_single_audit(self) -> None:
        response = await self._post()
        self.assertEqual(response.status_code, 200, response.text)
        data = response.json()["data"]
        self.assertEqual(data["provider"], "stub")
        self.assertEqual(data["model"], "stub-enterprise-v1")
        self.assertEqual(data["status"], "succeeded")
        self.assertGreater(data["usage"]["total_tokens"], 0)
        self.assertEqual(data["currency"], "USD")
        Decimal(data["cost"])
        with self.app.state.container.unit_of_work.transaction():
            factory = self.app.state.container.audit_repository._connection_factory
            with factory.connection() as connection, connection.cursor() as cursor:
                cursor.execute("SELECT status,actor_user_id,evidence_refs,provider_request_id,finish_reason FROM llm_usage_ledger")
                row = cursor.fetchone()
                self.assertEqual(row[0:2], ("succeeded", "user-employee"))
                self.assertNotIn("Controlled enterprise evidence", str(row[2]))
                self.assertTrue(row[3])
                self.assertEqual(row[4], "stop")
                cursor.execute("SELECT COUNT(*) FROM audit_logs WHERE operation_type='analysis.execute.succeeded'")
                self.assertEqual(cursor.fetchone()[0], 1)

    async def test_idempotent_replay_returns_same_result_without_call_or_charge(self) -> None:
        first = await self._post("ai-idempotency-replay")
        second = await self._post("ai-idempotency-replay")
        self.assertEqual(first.json()["data"]["analysis_id"], second.json()["data"]["analysis_id"])
        self.assertEqual(self.app.state.container.llm_provider.call_count, 1)
        factory = self.app.state.container.audit_repository._connection_factory
        with factory.connection() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*),SUM(request_count) FROM llm_usage_ledger CROSS JOIN llm_quota_buckets WHERE status='succeeded'")
            count, _ = cursor.fetchone()
            self.assertEqual(count, 2)  # one ledger x two user/global buckets

    async def test_confirmation_missing_evidence_and_bad_key_never_call_provider(self) -> None:
        unconfirmed = await self._post("ai-unconfirmed-0001", confirmed=False)
        empty = await self._post("ai-empty-evidence-01", evidence=[])
        bad_key = await self.client.post("/api/v1/ai-analysis", json=self._payload(), headers={"Idempotency-Key": "bad key"})
        self.assertEqual(unconfirmed.status_code, 422)
        self.assertEqual(empty.status_code, 422)
        self.assertEqual(bad_key.status_code, 422)
        self.assertEqual(self.app.state.container.llm_provider.call_count, 0)

    async def test_missing_and_archived_evidence_never_call_provider(self) -> None:
        missing = await self._post("ai-missing-evidence", evidence=[{"document_id": "missing", "chunk_id": "missing", "score": 1}])
        document = self.app.state.container.document_repository.get(self.document_id)
        assert document is not None
        document.archive()
        self.app.state.container.document_repository.update(document)
        archived = await self._post("ai-archived-evidence")
        self.assertEqual(missing.status_code, 422)
        self.assertEqual(archived.status_code, 422)
        self.assertEqual(self.app.state.container.llm_provider.call_count, 0)

    async def test_user_quota_rejection_is_429_persisted_and_audited(self) -> None:
        limited = self.settings.model_copy(update={"llm_user_daily_request_limit": 1})
        reset_postgres_state_if_needed(limited)
        await self.client.aclose()
        self.app = create_app(limited)
        self.client = httpx.AsyncClient(transport=httpx.ASGITransport(app=self.app), base_url="http://test",
                                       headers=authorization_headers(self.app, username=EMPLOYEE_USERNAME, password=EMPLOYEE_PASSWORD))
        self.document_id, self.chunk_id = self._seed_evidence("quota evidence")
        self.assertEqual((await self._post("ai-quota-first-01")).status_code, 200)
        rejected = await self._post("ai-quota-second-02")
        self.assertEqual(rejected.status_code, 429)
        self.assertEqual(rejected.json()["error"]["code"], "llm_quota_exceeded")
        self.assertEqual(self.app.state.container.llm_provider.call_count, 1)
        logs = self.app.state.container.audit_repository.list_all()
        self.assertEqual(sum(log.operation_type == "analysis.execute.quota_rejected" for log in logs), 1)

    async def test_provider_timeout_failure_and_rate_limit_are_settled(self) -> None:
        for index, (behavior, status, code) in enumerate((("timeout", 504, "provider_timeout"), ("failure", 502, "provider_failed"), ("rate_limit", 429, "provider_rate_limited"), ("partial_failure", 502, "provider_failed"))):
            self.app.state.container.llm_provider.behavior = behavior
            response = await self._post(f"ai-provider-{index:04d}")
            self.assertEqual(response.status_code, status)
            self.assertEqual(response.json()["error"]["code"], code)
        factory = self.app.state.container.audit_repository._connection_factory
        with factory.connection() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM llm_usage_ledger WHERE status='failed'")
            self.assertEqual(cursor.fetchone()[0], 4)
            cursor.execute("SELECT COUNT(*) FROM audit_logs WHERE operation_type='analysis.execute.failed'")
            self.assertEqual(cursor.fetchone()[0], 4)
            cursor.execute("SELECT input_tokens,output_tokens,actual_cost FROM llm_usage_ledger WHERE error_code='provider_partial_failure'")
            partial = cursor.fetchone()
            self.assertEqual(partial[0:2], (7, 3))
            self.assertGreater(Decimal(partial[2]), 0)

    async def test_per_request_cap_rejects_before_reservation(self) -> None:
        service = self.app.state.container.ai_analysis_service
        service._settings = self.settings.model_copy(update={"llm_request_max_cost": Decimal("0")})
        response = await self._post("ai-cost-cap-0001")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"]["code"], "llm_request_cost_exceeded")
        self.assertEqual(self.app.state.container.llm_provider.call_count, 0)

    async def test_no_ledger_mutation_or_delete_routes_exist(self) -> None:
        paths = self.app.openapi()["paths"]
        self.assertNotIn("/api/v1/llm-usage", paths)
        self.assertEqual(set(paths["/api/v1/ai-analysis"]), {"post"})

    async def test_restart_recovers_idempotent_result_without_provider_call(self) -> None:
        first = await self._post("ai-restart-idempotent")
        self.assertEqual(first.status_code, 200)
        await self.client.aclose()
        self.app = create_app(self.settings)
        self.client = httpx.AsyncClient(transport=httpx.ASGITransport(app=self.app), base_url="http://test",
                                       headers=authorization_headers(self.app, username=EMPLOYEE_USERNAME, password=EMPLOYEE_PASSWORD))
        second = await self._post("ai-restart-idempotent")
        self.assertEqual(second.status_code, 200)
        self.assertEqual(first.json()["data"]["analysis_id"], second.json()["data"]["analysis_id"])
        self.assertEqual(self.app.state.container.llm_provider.call_count, 0)

    async def test_unknown_role_denied_and_client_actor_fields_are_rejected(self) -> None:
        payload = self._payload()
        payload["actor_user_id"] = "forged-user"
        forged = await self.client.post("/api/v1/ai-analysis", json=payload, headers={"Idempotency-Key": "ai-forged-actor-01"})
        self.assertEqual(forged.status_code, 422)
        unknown = CurrentUser(user_id="unknown-user", username="unknown", role="unknown-role")
        token = self.app.state.container.jwt_service.create_access_token(unknown)
        denied = await self.client.post("/api/v1/ai-analysis", json=self._payload(), headers={
            "Authorization": f"Bearer {token.access_token}", "Idempotency-Key": "ai-unknown-role-01",
        })
        self.assertEqual(denied.status_code, 403)
        self.assertEqual(self.app.state.container.llm_provider.call_count, 0)
        self.assertEqual(self.app.state.container.audit_repository.list_all()[-1].operation_type, "authorization.denied")

    async def test_internal_rag_setting_cannot_implicitly_call_provider(self) -> None:
        settings = self.settings.model_copy(update={"internal_rag_use_llm": True})
        reset_postgres_state_if_needed(settings)
        await self.client.aclose()
        self.app = create_app(settings)
        self.client = httpx.AsyncClient(transport=httpx.ASGITransport(app=self.app), base_url="http://test",
                                       headers=authorization_headers(self.app, username=EMPLOYEE_USERNAME, password=EMPLOYEE_PASSWORD))
        self.document_id, self.chunk_id = self._seed_evidence("ordinary rag evidence keyword")
        response = await self.client.post("/api/v1/internal-rag/answer", json={
            "question": "ordinary rag evidence keyword", "limit": 5,
            "answer_mode": "extractive", "require_citations": True,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.app.state.container.llm_provider.call_count, 0)
        factory = self.app.state.container.audit_repository._connection_factory
        with factory.connection() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM llm_usage_ledger")
            self.assertEqual(cursor.fetchone()[0], 0)

    async def test_concurrent_same_key_calls_provider_at_most_once(self) -> None:
        service = self.app.state.container.ai_analysis_service
        actor = CurrentUser(user_id="user-employee", username="employee", role="employee")
        payload = AIAnalysisRequest.model_validate(self._payload())
        def execute(index: int):
            try:
                return service.execute(payload, actor=actor, idempotency_key="ai-concurrent-key-01",
                                       context=PersistentAuditContext(request_id=f"concurrent-{index}", http_method="POST",
                                                                      api_path="/api/v1/ai-analysis", resource_id="ai-analysis", current_user=actor))
            except Exception as exc:  # 并发的第二个请求可稳定返回 in-progress。
                return exc
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(execute, (1, 2)))
        self.assertEqual(self.app.state.container.llm_provider.call_count, 1)
        self.assertGreaterEqual(sum(hasattr(item, "analysis_id") for item in results), 1)

    async def test_missing_bearer_is_401_and_zero_call(self) -> None:
        response = await self.client.post("/api/v1/ai-analysis", json=self._payload(),
                                          headers={"Authorization": "", "Idempotency-Key": "ai-no-bearer-0001"})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(self.app.state.container.llm_provider.call_count, 0)

    async def test_missing_idempotency_header_is_422_and_zero_call(self) -> None:
        response = await self.client.post("/api/v1/ai-analysis", json=self._payload())
        self.assertEqual(response.status_code, 422)
        self.assertEqual(self.app.state.container.llm_provider.call_count, 0)

    async def test_blank_question_is_422_and_zero_call(self) -> None:
        response = await self._post("ai-blank-question-01", question="   ")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(self.app.state.container.llm_provider.call_count, 0)

    async def test_question_length_limit_is_422_and_zero_call(self) -> None:
        response = await self._post("ai-long-question-001", question="x" * 2001)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(self.app.state.container.llm_provider.call_count, 0)

    async def test_evidence_count_limit_is_422_and_zero_call(self) -> None:
        evidence = [{"document_id": self.document_id, "chunk_id": self.chunk_id, "score": 1}] * 21
        response = await self._post("ai-too-many-evidence", evidence=evidence)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(self.app.state.container.llm_provider.call_count, 0)

    async def test_negative_score_is_422_and_zero_call(self) -> None:
        response = await self._post("ai-negative-score-01", evidence=[{"document_id": self.document_id, "chunk_id": self.chunk_id, "score": -1}])
        self.assertEqual(response.status_code, 422)
        self.assertEqual(self.app.state.container.llm_provider.call_count, 0)

    async def test_blank_document_id_is_422_and_zero_call(self) -> None:
        response = await self._post("ai-blank-document-01", evidence=[{"document_id": "", "chunk_id": self.chunk_id, "score": 1}])
        self.assertEqual(response.status_code, 422)
        self.assertEqual(self.app.state.container.llm_provider.call_count, 0)

    async def test_blank_chunk_id_is_422_and_zero_call(self) -> None:
        response = await self._post("ai-blank-chunk-0001", evidence=[{"document_id": self.document_id, "chunk_id": "", "score": 1}])
        self.assertEqual(response.status_code, 422)
        self.assertEqual(self.app.state.container.llm_provider.call_count, 0)

    async def test_missing_confirmation_field_is_422_and_zero_call(self) -> None:
        payload = self._payload()
        payload.pop("confirmed")
        response = await self.client.post("/api/v1/ai-analysis", json=payload, headers={"Idempotency-Key": "ai-no-confirm-0001"})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(self.app.state.container.llm_provider.call_count, 0)

    async def test_extra_provider_field_is_rejected_and_zero_call(self) -> None:
        response = await self._post("ai-forged-provider-1", provider="paid-provider")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(self.app.state.container.llm_provider.call_count, 0)

    async def test_malformed_json_is_422_and_zero_call(self) -> None:
        response = await self.client.post("/api/v1/ai-analysis", content="{", headers={
            "Content-Type": "application/json", "Idempotency-Key": "ai-malformed-json-1",
        })
        self.assertEqual(response.status_code, 422)
        self.assertEqual(self.app.state.container.llm_provider.call_count, 0)

    async def test_duplicate_evidence_is_deduplicated(self) -> None:
        ref = {"document_id": self.document_id, "chunk_id": self.chunk_id, "score": "0.9"}
        response = await self._post("ai-deduplicate-0001", evidence=[ref, ref])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["data"]["citations"]), 1)

    async def test_evidence_is_score_sorted_with_stable_tie_break(self) -> None:
        doc_b, chunk_b = self._seed_evidence("second evidence")
        response = await self._post("ai-stable-order-0001", evidence=[
            {"document_id": doc_b, "chunk_id": chunk_b, "score": "0.4"},
            {"document_id": self.document_id, "chunk_id": self.chunk_id, "score": "0.9"},
        ])
        citations = response.json()["data"]["citations"]
        self.assertEqual(citations[0]["document_id"], self.document_id)

    async def test_evidence_is_capped_to_configured_count(self) -> None:
        evidence = [{"document_id": self.document_id, "chunk_id": self.chunk_id, "score": "1"}]
        for index in range(5):
            document_id, chunk_id = self._seed_evidence(f"evidence {index}")
            evidence.append({"document_id": document_id, "chunk_id": chunk_id, "score": str(index / 10)})
        response = await self._post("ai-evidence-cap-0001", evidence=evidence)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["data"]["citations"]), self.settings.llm_evidence_max_count)

    async def test_price_and_currency_snapshot_are_persisted(self) -> None:
        self.assertEqual((await self._post("ai-price-snapshot-1")).status_code, 200)
        factory = self.app.state.container.audit_repository._connection_factory
        with factory.connection() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT input_price_per_million,output_price_per_million,currency FROM llm_usage_ledger")
            row = cursor.fetchone()
        self.assertEqual(Decimal(row[0]), self.settings.llm_input_price_per_million)
        self.assertEqual(Decimal(row[1]), self.settings.llm_output_price_per_million)
        self.assertEqual(row[2].strip(), self.settings.llm_currency)

    async def test_success_reserves_both_user_and_global_buckets(self) -> None:
        self.assertEqual((await self._post("ai-two-buckets-0001")).status_code, 200)
        factory = self.app.state.container.audit_repository._connection_factory
        with factory.connection() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT scope_type,request_count FROM llm_quota_buckets ORDER BY scope_type")
            rows = cursor.fetchall()
        self.assertEqual(rows, [("global", 1), ("user", 1)])

    async def test_provider_failure_releases_reserved_tokens_and_cost(self) -> None:
        self.app.state.container.llm_provider.behavior = "failure"
        self.assertEqual((await self._post("ai-release-failure-1")).status_code, 502)
        factory = self.app.state.container.audit_repository._connection_factory
        with factory.connection() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT token_count,cost,request_count FROM llm_quota_buckets")
            rows = cursor.fetchall()
        self.assertTrue(all(row[0] == 0 and Decimal(row[1]) == 0 and row[2] == 1 for row in rows))

    async def test_request_id_and_identity_come_from_server_context(self) -> None:
        self.assertEqual((await self._post("ai-server-context-1")).status_code, 200)
        factory = self.app.state.container.audit_repository._connection_factory
        with factory.connection() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT request_id,actor_user_id,actor_username,actor_role FROM llm_usage_ledger")
            row = cursor.fetchone()
        self.assertEqual(row, ("req-ai-server-context-1", "user-employee", "employee", "employee"))


if __name__ == "__main__":
    unittest.main()
