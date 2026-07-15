from __future__ import annotations

import json
import unittest

import httpx

from app.config.settings import Settings
from app.main import create_app
from tests.postgres_test_utils import reset_postgres_state_if_needed
from tests.auth_test_utils import authorization_headers


class DocumentUploadAPITest(unittest.IsolatedAsyncioTestCase):
    """验证 POST /api/v1/documents 的同步 MVP 合同。"""

    async def asyncSetUp(self) -> None:
        settings = Settings(workflow_step_delay_seconds=0, log_level="CRITICAL")
        reset_postgres_state_if_needed(settings)
        self.app = create_app(settings)
        transport = httpx.ASGITransport(app=self.app)
        self.client = httpx.AsyncClient(
            transport=transport,
            base_url="http://test",
            headers=authorization_headers(self.app),
        )

    async def asyncTearDown(self) -> None:
        await self.client.aclose()

    async def _upload_document(
        self,
        *,
        filename: str,
        content: bytes,
        metadata: dict[str, object],
        content_type: str = "text/markdown",
        idempotency_key: str | None = None,
    ) -> httpx.Response:
        files = {
            "file": (filename, content, content_type),
            "metadata": (None, json.dumps(metadata), "application/json"),
        }
        headers = {"X-Request-ID": "upload-request"}
        if idempotency_key is not None:
            headers["Idempotency-Key"] = idempotency_key
        return await self.client.post("/api/v1/documents", files=files, headers=headers)

    def _document_count(self) -> int:
        return len(self.app.state.container.document_repository.list_all())

    async def test_upload_markdown_success(self) -> None:
        response = await self._upload_document(
            filename="monthly-review.md",
            content=b"# Monthly Review\n\nSales summary.",
            metadata={
                "title": "Monthly Review",
                "description": "Internal monthly summary",
                "owner": "analysis-team",
                "tags": ["sales", "monthly"],
                "language": "en",
            },
        )

        self.assertEqual(response.status_code, 201)
        payload = response.json()
        self.assertTrue(payload["success"])
        session = payload["data"]
        self.assertEqual(session["status"], "completed")
        self.assertEqual(session["progress"], 100)
        self.assertIsNone(session["error_code"])
        self.assertIsNone(session["error_message"])
        self.assertEqual(self._document_count(), 1)

    async def test_unsupported_extension_returns_error(self) -> None:
        response = await self._upload_document(
            filename="malware.exe",
            content=b"MZ",
            content_type="application/octet-stream",
            metadata={
                "title": "Unsupported",
                "owner": "analysis-team",
                "tags": [],
                "language": "en",
            },
        )

        self.assertEqual(response.status_code, 415)
        payload = response.json()
        self.assertFalse(payload["success"])
        self.assertEqual(payload["error"]["code"], "unsupported_document_type")

    async def test_empty_file_returns_error(self) -> None:
        response = await self._upload_document(
            filename="empty.md",
            content=b"",
            metadata={
                "title": "Empty File",
                "owner": "analysis-team",
                "tags": [],
                "language": "en",
            },
        )

        self.assertEqual(response.status_code, 422)
        payload = response.json()
        self.assertFalse(payload["success"])
        self.assertEqual(payload["error"]["code"], "empty_file")

    async def test_missing_title_returns_missing_title(self) -> None:
        response = await self._upload_document(
            filename="missing-title.md",
            content=b"# Missing Title",
            metadata={
                "description": "No title field",
                "owner": "analysis-team",
                "tags": [],
                "language": "en",
            },
        )

        self.assertEqual(response.status_code, 422)
        payload = response.json()
        self.assertFalse(payload["success"])
        self.assertEqual(payload["error"]["code"], "missing_title")

    async def test_duplicate_checksum_returns_existing_result(self) -> None:
        first = await self._upload_document(
            filename="duplicate.md",
            content=b"# Duplicate\n",
            metadata={
                "title": "Duplicate",
                "owner": "analysis-team",
                "tags": [],
                "language": "en",
            },
        )
        second = await self._upload_document(
            filename="duplicate-copy.md",
            content=b"# Duplicate\n",
            metadata={
                "title": "Duplicate copy",
                "owner": "analysis-team",
                "tags": [],
                "language": "en",
            },
        )

        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 201)
        self.assertEqual(first.json()["data"], second.json()["data"])
        self.assertEqual(self._document_count(), 1)

    async def test_idempotency_same_key_same_checksum_returns_existing_result(self) -> None:
        first = await self._upload_document(
            filename="idempotent.md",
            content=b"# Idempotent\n",
            metadata={
                "title": "Idempotent",
                "owner": "analysis-team",
                "tags": [],
                "language": "en",
            },
            idempotency_key="idem-123",
        )
        second = await self._upload_document(
            filename="idempotent.md",
            content=b"# Idempotent\n",
            metadata={
                "title": "Idempotent",
                "owner": "analysis-team",
                "tags": [],
                "language": "en",
            },
            idempotency_key="idem-123",
        )

        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 201)
        self.assertEqual(first.json()["data"], second.json()["data"])
        self.assertEqual(self._document_count(), 1)

    async def test_idempotency_same_key_different_checksum_conflicts(self) -> None:
        first = await self._upload_document(
            filename="idempotency-a.md",
            content=b"# A\n",
            metadata={
                "title": "Idempotency A",
                "owner": "analysis-team",
                "tags": [],
                "language": "en",
            },
            idempotency_key="idem-conflict",
        )
        second = await self._upload_document(
            filename="idempotency-b.md",
            content=b"# B\n",
            metadata={
                "title": "Idempotency B",
                "owner": "analysis-team",
                "tags": [],
                "language": "en",
            },
            idempotency_key="idem-conflict",
        )

        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 409)
        payload = second.json()
        self.assertFalse(payload["success"])
        self.assertEqual(payload["error"]["code"], "idempotency_conflict")
        self.assertEqual(self._document_count(), 1)


if __name__ == "__main__":
    unittest.main()
