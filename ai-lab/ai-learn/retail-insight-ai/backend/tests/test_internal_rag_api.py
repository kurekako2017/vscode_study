from __future__ import annotations

import json
import unittest

import httpx

from app.config.settings import Settings
from app.errors.error_codes import ErrorCode
from app.main import create_app
from tests.postgres_test_utils import reset_postgres_state_if_needed


class InternalRagAPITest(unittest.IsolatedAsyncioTestCase):
    """验证 `POST /api/v1/internal-rag/answer` 的 deterministic MVP。"""

    async def asyncSetUp(self) -> None:
        settings = Settings(workflow_step_delay_seconds=0, log_level="CRITICAL")
        reset_postgres_state_if_needed(settings)
        self.app = create_app(settings)
        transport = httpx.ASGITransport(app=self.app)
        self.client = httpx.AsyncClient(transport=transport, base_url="http://test")

    async def asyncTearDown(self) -> None:
        await self.client.aclose()

    async def _upload_document(
        self,
        *,
        filename: str,
        content: bytes,
        metadata: dict[str, object],
        content_type: str,
    ) -> httpx.Response:
        files = {
            "file": (filename, content, content_type),
            "metadata": (None, json.dumps(metadata), "application/json"),
        }
        return await self.client.post("/api/v1/documents", files=files, headers={"X-Request-ID": "upload-request"})

    async def _import_document(self, document_id: str) -> httpx.Response:
        return await self.client.post(f"/api/v1/documents/{document_id}/import", headers={"X-Request-ID": "import-request"})

    async def _chunk_document(self, document_id: str) -> httpx.Response:
        return await self.client.post(f"/api/v1/documents/{document_id}/chunks", headers={"X-Request-ID": "chunk-request"})

    async def _prepare_searchable_document(
        self,
        *,
        filename: str,
        content: bytes,
        title: str,
        tags: list[str],
        language: str = "en",
        content_type: str = "text/markdown",
    ) -> str:
        upload = await self._upload_document(
            filename=filename,
            content=content,
            metadata={
                "title": title,
                "owner": "analysis-team",
                "tags": tags,
                "language": language,
            },
            content_type=content_type,
        )
        document_id = upload.json()["data"]["document_id"]
        await self._import_document(document_id)
        await self._chunk_document(document_id)
        return document_id

    async def _answer_internal_rag(
        self,
        payload: dict[str, object],
        *,
        request_id: str = "internal-rag-request",
    ) -> httpx.Response:
        return await self.client.post(
            "/api/v1/internal-rag/answer",
            json=payload,
            headers={"X-Request-ID": request_id},
        )

    async def test_upload_import_chunk_then_extractive_answer_succeeds(self) -> None:
        document_id = await self._prepare_searchable_document(
            filename="rag-extractive.md",
            content=b"# Monthly Sales Policy\n\nMonthly sales policy summary and rules for the team.",
            title="Monthly Sales Policy",
            tags=["sales", "policy"],
        )

        response = await self._answer_internal_rag(
            {
                "question": "What is the monthly sales policy?",
                "limit": 5,
                "include_archived": False,
                "document_type": "markdown",
                "language": "en",
                "tags": ["sales", "policy"],
                "answer_mode": "extractive",
                "require_citations": True,
            }
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()["data"]
        self.assertEqual(payload["retrieval_mode"], "keyword")
        self.assertEqual(payload["answer_mode"], "extractive")
        self.assertIn("Extractive answer", payload["answer"])
        self.assertGreaterEqual(len(payload["citations"]), 1)
        citation = payload["citations"][0]
        self.assertEqual(citation["document_id"], document_id)
        self.assertIn("monthly sales policy", citation["excerpt"].lower())
        self.assertIn("source", citation)
        self.assertIn("score", citation)
        self.assertGreaterEqual(payload["confidence"], 0.0)
        self.assertLessEqual(payload["confidence"], 1.0)
        self.assertIn("weak_match", payload["warnings"])

        events = self.app.state.container.event_repository.list_after("internal_rag:internal-rag-request")
        self.assertEqual(
            [event.event_type for event in events],
            [
                "internal_rag.started",
                "internal_rag.retrieval_completed",
                "internal_rag.answer_generated",
            ],
        )

    async def test_low_context_warning_is_returned_for_partial_coverage(self) -> None:
        await self._prepare_searchable_document(
            filename="rag-low-context.md",
            content=(
                b"# Monthly Policy\n\nMonthly policy paragraph one.\n\n"
                b"Monthly policy paragraph two.\n\nMonthly policy paragraph three."
            ),
            title="Monthly Policy",
            tags=["policy"],
        )

        response = await self._answer_internal_rag(
            {
                "question": "monthly policy",
                "limit": 1,
                "answer_mode": "extractive",
                "require_citations": True,
            }
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()["data"]
        self.assertIn("low_context", payload["warnings"])
        self.assertGreaterEqual(len(payload["citations"]), 1)

    async def test_summary_mode_is_deterministic(self) -> None:
        await self._prepare_searchable_document(
            filename="rag-summary.md",
            content=b"# Sales Summary\n\nThe monthly sales policy is stable. The team should follow the policy.",
            title="Sales Summary",
            tags=["sales", "summary"],
        )

        first = await self._answer_internal_rag(
            {
                "question": "Summarize the sales policy",
                "limit": 3,
                "answer_mode": "summary",
                "require_citations": True,
            }
        )
        second = await self._answer_internal_rag(
            {
                "question": "Summarize the sales policy",
                "limit": 3,
                "answer_mode": "summary",
                "require_citations": True,
            }
        )

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(first.json()["data"], second.json()["data"])
        self.assertTrue(first.json()["data"]["answer"].startswith("Summary:"))

    async def test_no_context_returns_insufficient_context(self) -> None:
        await self._prepare_searchable_document(
            filename="rag-empty.md",
            content=b"# Sales Summary\n\nThis content does not contain the requested topic.",
            title="Sales Summary",
            tags=["sales"],
        )

        response = await self._answer_internal_rag(
            {
                "question": "ultra rare safety token qwertyuiopzzzz",
                "answer_mode": "extractive",
                "require_citations": True,
            }
        )

        self.assertEqual(response.status_code, 422)
        payload = response.json()
        self.assertFalse(payload["success"])
        self.assertEqual(payload["error"]["code"], ErrorCode.INSUFFICIENT_CONTEXT.value)

    async def test_empty_question_returns_invalid_question(self) -> None:
        await self._prepare_searchable_document(
            filename="rag-invalid-question.md",
            content=b"# Invalid Question\n\nQuestion target.",
            title="Invalid Question",
            tags=["question"],
        )

        response = await self._answer_internal_rag(
            {
                "question": "   ",
                "answer_mode": "extractive",
                "require_citations": True,
            }
        )

        self.assertEqual(response.status_code, 422)
        payload = response.json()
        self.assertFalse(payload["success"])
        self.assertEqual(payload["error"]["code"], ErrorCode.INVALID_QUESTION.value)

    async def test_archived_documents_are_excluded_unless_requested(self) -> None:
        document_id = await self._prepare_searchable_document(
            filename="rag-archived.md",
            content=b"# Archived Policy\n\nArchived policy content.",
            title="Archived Policy",
            tags=["archive"],
        )
        await self.client.delete(f"/api/v1/documents/{document_id}")

        excluded = await self._answer_internal_rag(
            {
                "question": "What is the archived policy?",
                "answer_mode": "extractive",
                "require_citations": True,
            }
        )
        included = await self._answer_internal_rag(
            {
                "question": "What is the archived policy?",
                "include_archived": True,
                "answer_mode": "extractive",
                "require_citations": True,
            }
        )

        self.assertEqual(excluded.status_code, 422)
        self.assertEqual(excluded.json()["error"]["code"], ErrorCode.INSUFFICIENT_CONTEXT.value)
        self.assertEqual(included.status_code, 200)
        self.assertGreaterEqual(len(included.json()["data"]["citations"]), 1)
        self.assertEqual(included.json()["data"]["citations"][0]["document_id"], document_id)

    async def test_citations_are_present(self) -> None:
        await self._prepare_searchable_document(
            filename="rag-citations.md",
            content=b"# Citation Policy\n\nThe team follows a clear citation policy for monthly analysis.",
            title="Citation Policy",
            tags=["citations"],
        )

        response = await self._answer_internal_rag(
            {
                "question": "What is the citation policy?",
                "limit": 3,
                "answer_mode": "extractive",
                "require_citations": True,
            }
        )

        self.assertEqual(response.status_code, 200)
        citations = response.json()["data"]["citations"]
        self.assertGreaterEqual(len(citations), 1)
        for citation in citations:
            self.assertIn("document_id", citation)
            self.assertIn("chunk_id", citation)
            self.assertIn("chunk_index", citation)
            self.assertIn("excerpt", citation)
            self.assertIn("source", citation)
            self.assertIn("score", citation)


if __name__ == "__main__":
    unittest.main()
