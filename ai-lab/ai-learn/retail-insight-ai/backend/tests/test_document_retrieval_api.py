from __future__ import annotations

import json
import os
import unittest

import httpx

from app.config.settings import Settings
from app.errors.error_codes import ErrorCode
from app.main import create_app
from tests.postgres_test_utils import reset_postgres_state_if_needed


class DocumentRetrievalAPITest(unittest.IsolatedAsyncioTestCase):
    """验证 POST /api/v1/document-retrieval/search 的 keyword-only MVP。"""

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

    async def _search_documents(
        self,
        payload: dict[str, object],
        *,
        request_id: str = "search-request",
    ) -> httpx.Response:
        return await self.client.post(
            "/api/v1/document-retrieval/search",
            json=payload,
            headers={"X-Request-ID": request_id},
        )

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

    async def test_upload_markdown_import_chunk_then_search_succeeds(self) -> None:
        document_id = await self._prepare_searchable_document(
            filename="retrieval-markdown.md",
            content=b"# Monthly Sales Policy\n\nMonthly sales policy summary and rules.",
            title="Monthly Sales Policy",
            tags=["sales", "policy"],
        )

        response = await self._search_documents(
            {
                "query": "monthly sales policy",
                "limit": 10,
                "include_archived": False,
                "document_type": "markdown",
                "language": "en",
                "tags": ["sales", "policy"],
            }
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()["data"]
        self.assertEqual(payload["query"], "monthly sales policy")
        self.assertEqual(payload["retrieval_mode"], "keyword")
        self.assertGreaterEqual(payload["total"], 1)
        self.assertGreaterEqual(len(payload["results"]), 1)
        result = payload["results"][0]
        self.assertEqual(result["document_id"], document_id)
        self.assertIn("Monthly Sales Policy", result["content_excerpt"])
        self.assertEqual(result["metadata"]["document_id"], document_id)
        self.assertEqual(result["source"]["source_type"], "upload_form")
        self.assertTrue(result["source"]["uri"].startswith("upload://"))

        events = self.app.state.container.event_repository.list_after("document_retrieval:search-request")
        self.assertEqual(
            [event.event_type for event in events],
            ["document.retrieval.started", "document.retrieval.completed"],
        )

    async def test_search_no_match_returns_empty_list(self) -> None:
        await self._prepare_searchable_document(
            filename="nomatch.md",
            content=b"# Sales Policy\n\nThis content does not contain the magic query.",
            title="No Match",
            tags=["sales"],
        )

        response = await self._search_documents({"query": "completely missing phrase"})

        self.assertEqual(response.status_code, 200)
        payload = response.json()["data"]
        self.assertEqual(payload["total"], 0)
        self.assertEqual(payload["results"], [])

    async def test_empty_query_returns_invalid_query(self) -> None:
        await self._prepare_searchable_document(
            filename="invalid-query.md",
            content=b"# Invalid Query\n\nQuery target.",
            title="Invalid Query",
            tags=["query"],
        )

        response = await self._search_documents({"query": "   "})

        self.assertEqual(response.status_code, 422)
        payload = response.json()
        self.assertFalse(payload["success"])
        self.assertEqual(payload["error"]["code"], ErrorCode.INVALID_QUERY.value)
        events = self.app.state.container.event_repository.list_after("document_retrieval:search-request")
        self.assertEqual(
            [event.event_type for event in events],
            ["document.retrieval.started", "document.retrieval.failed"],
        )

    async def test_archived_document_chunks_are_excluded(self) -> None:
        document_id = await self._prepare_searchable_document(
            filename="archived-retrieval.md",
            content=b"# Archived Retrieval\n\nArchived retrieval content.",
            title="Archived Retrieval",
            tags=["archive"],
        )
        await self.client.delete(f"/api/v1/documents/{document_id}")

        response = await self._search_documents({"query": "archived retrieval"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["results"], [])

    async def test_include_archived_includes_archived_chunks(self) -> None:
        document_id = await self._prepare_searchable_document(
            filename="include-archived.md",
            content=b"# Include Archived\n\nArchived retrieval content.",
            title="Include Archived",
            tags=["archive"],
        )
        await self.client.delete(f"/api/v1/documents/{document_id}")

        response = await self._search_documents(
            {
                "query": "archived retrieval",
                "include_archived": True,
            }
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()["data"]
        self.assertGreaterEqual(len(payload["results"]), 1)
        self.assertEqual(payload["results"][0]["document_id"], document_id)

    async def test_score_ordering_is_deterministic(self) -> None:
        await self._prepare_searchable_document(
            filename="ordering-a.md",
            content=b"# Ordering A\n\nkeyword only chunk.",
            title="Ordering A",
            tags=["ordering"],
        )
        await self._prepare_searchable_document(
            filename="ordering-b.md",
            content=b"# Ordering B\n\nkeyword only chunk.",
            title="Ordering B",
            tags=["ordering"],
        )

        first = await self._search_documents({"query": "keyword"})
        second = await self._search_documents({"query": "keyword"})

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(first.json()["data"], second.json()["data"])

    async def test_explicit_vector_mode_requires_configured_embedding_provider(self) -> None:
        response = await self._search_documents(
            {"query": "vector query", "retrieval_mode": "vector"}
        )

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["error"]["code"], ErrorCode.RETRIEVAL_UNAVAILABLE.value)

    async def test_vector_and_hybrid_modes_run_with_explicit_test_provider(self) -> None:
        await self.client.aclose()
        settings = Settings(
            workflow_step_delay_seconds=0,
            log_level="CRITICAL",
            embedding_provider="deterministic_test",
            embedding_model="deterministic-test-sha256-v1",
        )
        self.app = create_app(settings)
        self.client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=self.app),
            base_url="http://test",
        )
        await self._prepare_searchable_document(
            filename="vector.txt",
            content=b"semantic evidence without query terms",
            title="Vector Evidence",
            tags=["vector"],
            content_type="text/plain",
        )

        vector = await self._search_documents(
            {"query": "unrelated vector query", "retrieval_mode": "vector", "top_k": 1}
        )
        hybrid = await self._search_documents(
            {"query": "unrelated vector query", "retrieval_mode": "hybrid", "top_k": 1}
        )

        self.assertEqual(vector.status_code, 200)
        self.assertEqual(vector.json()["data"]["retrieval_mode"], "vector")
        self.assertEqual(vector.json()["data"]["results"][0]["retrieval_method"], "vector")
        self.assertEqual(hybrid.status_code, 200)
        self.assertEqual(hybrid.json()["data"]["retrieval_mode"], "hybrid")
        self.assertEqual(hybrid.json()["data"]["results"][0]["retrieval_method"], "hybrid")


if __name__ == "__main__":
    unittest.main()
