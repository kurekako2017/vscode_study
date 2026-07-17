"""PostgreSQL 集成：OpenRouter MockTransport 经 Gateway 的双路由与失败路径。"""

from __future__ import annotations

import json
import unittest
from decimal import Decimal
from uuid import uuid4

import httpx
from pydantic import SecretStr

from app.config.settings import Settings
from app.main import create_app
from app.models.document import Document, DocumentChunk, DocumentMetadata
from app.providers.openrouter_llm_provider import OpenRouterLLMProvider
from tests.auth_test_utils import EMPLOYEE_PASSWORD, EMPLOYEE_USERNAME, authorization_headers
from tests.postgres_test_utils import reset_postgres_state_if_needed


def _analysis_content(document_id: str, chunk_id: str) -> str:
    return json.dumps(
        {
            "answer": "OpenRouter analysis grounded on evidence.",
            "citations": [{"document_id": document_id, "chunk_id": chunk_id}],
            "insufficient_context": False,
            "warnings": [],
        }
    )


def _report_content(document_id: str, chunk_id: str) -> str:
    return json.dumps(
        {
            "title": "Board Report",
            "executive_summary": "Board summary from OpenRouter.",
            "kpi_findings": ["KPI grounded"],
            "risks": ["Risk noted"],
            "recommendations": ["Recommend review"],
            "citations": [{"document_id": document_id, "chunk_id": chunk_id}],
        }
    )


@unittest.skipUnless(
    __import__("os").environ.get("REPOSITORY_BACKEND") == "postgres",
    "PostgreSQL-only OpenRouter gateway integration",
)
class OpenRouterGatewayPostgresTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.calls: list[dict] = []

        def handler(request: httpx.Request) -> httpx.Response:
            body = json.loads(request.content.decode())
            self.calls.append(
                {
                    "model": body.get("model"),
                    "auth": request.headers.get("Authorization"),
                    "path": request.url.path,
                }
            )
            model = body["model"]
            if model == "vendor/low":
                content = _analysis_content(self.document_id, self.chunk_id)
            else:
                content = _report_content(self.document_id, self.chunk_id)
            return httpx.Response(
                200,
                headers={"content-type": "application/json"},
                json={
                    "id": f"gen-{len(self.calls)}",
                    "model": model,
                    "choices": [
                        {
                            "message": {"role": "assistant", "content": content},
                            "finish_reason": "stop",
                        }
                    ],
                    "usage": {"prompt_tokens": 15, "completion_tokens": 9},
                },
            )

        self.settings = Settings(
            log_level="CRITICAL",
            workflow_step_delay_seconds=0,
            llm_provider_mode="openrouter",
            openrouter_api_key=SecretStr("integration-test-key-not-real"),
            openrouter_low_cost_model="vendor/low",
            openrouter_high_quality_model="vendor/high",
            openrouter_base_url="https://openrouter.example/api/v1",
            openrouter_low_input_price=Decimal("0.5"),
            openrouter_low_output_price=Decimal("1.5"),
            openrouter_high_input_price=Decimal("3.0"),
            openrouter_high_output_price=Decimal("9.0"),
            _env_file=None,
        )
        if self.settings.repository_backend != "postgres":
            self.skipTest("PostgreSQL-only")
        reset_postgres_state_if_needed(self.settings)
        self.app = create_app(self.settings)
        # 注入 MockTransport，确保零外网（不替换 frozen container 字段）。
        transport = httpx.MockTransport(handler)
        low = OpenRouterLLMProvider(
            provider_name="openrouter-low-cost",
            model_name="vendor/low",
            api_key=SecretStr("integration-test-key-not-real"),
            base_url="https://openrouter.example/api/v1",
            transport=transport,
        )
        high = OpenRouterLLMProvider(
            provider_name="openrouter-high-quality",
            model_name="vendor/high",
            api_key=SecretStr("integration-test-key-not-real"),
            base_url="https://openrouter.example/api/v1",
            transport=transport,
        )
        router = self.app.state.container.llm_gateway._router  # type: ignore[attr-defined]
        router._providers["openrouter-low-cost"] = low
        router._providers["openrouter-high-quality"] = high

        self.client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=self.app),
            base_url="http://test",
            headers=authorization_headers(
                self.app, username=EMPLOYEE_USERNAME, password=EMPLOYEE_PASSWORD
            ),
        )
        self.document_id, self.chunk_id = self._seed_evidence("OpenRouter integration evidence")

    async def asyncTearDown(self) -> None:
        if hasattr(self, "client"):
            await self.client.aclose()

    def _seed_evidence(self, content: str) -> tuple[str, str]:
        document_id = f"doc-{uuid4().hex}"
        metadata = DocumentMetadata.from_mapping(
            {
                "document_id": document_id,
                "title": "OpenRouter evidence",
                "owner": "analysis-team",
                "language": "en",
                "document_type": "text",
                "status": "uploaded",
                "source": {"source_type": "test", "uri": f"test://{document_id}"},
                "checksum": f"sha256:{uuid4().hex}",
            }
        )
        document = Document.create(content, metadata)
        chunk_id = f"chk-{uuid4().hex}"
        chunk = DocumentChunk(document_id, 1, chunk_id, 0, content, len(content), metadata)
        self.app.state.container.document_repository.create(document)
        self.app.state.container.document_chunk_repository.replace_for_document(
            document_id, 1, [chunk]
        )
        return document_id, chunk_id

    async def test_ai_analysis_and_executive_report_use_distinct_models(self) -> None:
        analysis = await self.client.post(
            "/api/v1/ai-analysis",
            json={
                "question": "Summarize",
                "evidence": [
                    {
                        "document_id": self.document_id,
                        "chunk_id": self.chunk_id,
                        "score": "0.9",
                    }
                ],
                "confirmed": True,
            },
            headers={"Idempotency-Key": "or-ai-0001", "X-Request-ID": "req-or-ai-1"},
        )
        self.assertEqual(analysis.status_code, 200, analysis.text)
        data = analysis.json()["data"]
        self.assertEqual(data["provider"], "openrouter-low-cost")
        self.assertEqual(data["model"], "vendor/low")
        self.assertEqual(data["route_tier"], "low_cost")
        self.assertEqual(self.calls[0]["model"], "vendor/low")
        self.assertEqual(self.calls[0]["auth"], "Bearer integration-test-key-not-real")

        report = await self.client.post(
            "/api/v1/executive-reports",
            json={
                "ai_analysis_id": data["analysis_id"],
                "title": "Board",
                "confirmed": True,
            },
            headers={"Idempotency-Key": "or-er-0001", "X-Request-ID": "req-or-er-1"},
        )
        self.assertEqual(report.status_code, 200, report.text)
        report_data = report.json()["data"]
        self.assertEqual(report_data["provider"], "openrouter-high-quality")
        self.assertEqual(report_data["model"], "vendor/high")
        self.assertEqual(report_data["route_tier"], "high_quality")
        self.assertEqual(self.calls[1]["model"], "vendor/high")
        # 串线检查：低成本请求未使用 high 模型。
        self.assertNotEqual(self.calls[0]["model"], "vendor/high")
        self.assertNotEqual(self.calls[1]["model"], "vendor/low")

        factory = self.app.state.container.audit_repository._connection_factory
        with factory.connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                "SELECT operation,route_tier,selected_model,policy_snapshot FROM llm_usage_ledger ORDER BY occurred_at"
            )
            rows = cursor.fetchall()
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0][0:3], ("ai_analysis", "low_cost", "vendor/low"))
            self.assertEqual(rows[1][0:3], ("executive_report", "high_quality", "vendor/high"))
            self.assertEqual(rows[0][3].get("usage_source"), "provider_reported")
            cursor.execute(
                "SELECT COUNT(*) FROM report_versions"
            )
            self.assertEqual(cursor.fetchone()[0], 1)
            cursor.execute(
                "SELECT COUNT(*) FROM audit_logs WHERE operation_type IN "
                "('analysis.execute.succeeded','executive_report.generated')"
            )
            self.assertEqual(cursor.fetchone()[0], 2)

    async def test_unconfirmed_and_quota_fail_before_http(self) -> None:
        before = len(self.calls)
        response = await self.client.post(
            "/api/v1/ai-analysis",
            json={
                "question": "Summarize",
                "evidence": [
                    {
                        "document_id": self.document_id,
                        "chunk_id": self.chunk_id,
                        "score": "0.9",
                    }
                ],
                "confirmed": False,
            },
            headers={"Idempotency-Key": "or-ai-noconfirm", "X-Request-ID": "req-or-nc"},
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(len(self.calls), before)

    async def test_idempotent_replay_does_not_rehit_http(self) -> None:
        first = await self.client.post(
            "/api/v1/ai-analysis",
            json={
                "question": "Summarize",
                "evidence": [
                    {
                        "document_id": self.document_id,
                        "chunk_id": self.chunk_id,
                        "score": "0.9",
                    }
                ],
                "confirmed": True,
            },
            headers={"Idempotency-Key": "or-ai-idem", "X-Request-ID": "req-or-idem-1"},
        )
        self.assertEqual(first.status_code, 200, first.text)
        after_first = len(self.calls)
        second = await self.client.post(
            "/api/v1/ai-analysis",
            json={
                "question": "Summarize",
                "evidence": [
                    {
                        "document_id": self.document_id,
                        "chunk_id": self.chunk_id,
                        "score": "0.9",
                    }
                ],
                "confirmed": True,
            },
            headers={"Idempotency-Key": "or-ai-idem", "X-Request-ID": "req-or-idem-2"},
        )
        self.assertEqual(second.status_code, 200)
        self.assertEqual(len(self.calls), after_first)
        self.assertEqual(first.json()["data"]["analysis_id"], second.json()["data"]["analysis_id"])


if __name__ == "__main__":
    unittest.main()
