from __future__ import annotations

import json
import unittest

import httpx

from app.config.settings import Settings
from app.main import create_app
from tests.postgres_test_utils import reset_postgres_state_if_needed


class DocumentArchiveAPITest(unittest.IsolatedAsyncioTestCase):
    """验证 DELETE /api/v1/documents/{document_id} 的软删除归档语义。"""

    async def asyncSetUp(self) -> None:
        settings = Settings(workflow_step_delay_seconds=0, log_level="CRITICAL")
        reset_postgres_state_if_needed(settings)
        self.app = create_app(settings)
        transport = httpx.ASGITransport(app=self.app)
        self.client = httpx.AsyncClient(transport=transport, base_url="http://test")

    async def asyncTearDown(self) -> None:
        await self.client.aclose()

    async def _upload_document(self, *, filename: str, content: bytes, metadata: dict[str, object]) -> httpx.Response:
        files = {
            "file": (filename, content, "text/markdown"),
            "metadata": (None, json.dumps(metadata), "application/json"),
        }
        return await self.client.post("/api/v1/documents", files=files, headers={"X-Request-ID": "upload-request"})

    async def test_upload_then_archive_document(self) -> None:
        upload = await self._upload_document(
            filename="archive.md",
            content=b"# Archive",
            metadata={
                "title": "Archive",
                "owner": "analysis-team",
                "tags": ["archive"],
                "language": "en",
            },
        )
        document_id = upload.json()["data"]["document_id"]

        response = await self.client.delete(f"/api/v1/documents/{document_id}", headers={"X-Request-ID": "delete-request"})

        self.assertEqual(response.status_code, 202)
        payload = response.json()
        self.assertTrue(payload["success"])
        self.assertEqual(payload["data"]["document_id"], document_id)
        self.assertEqual(payload["data"]["status"], "archived")

    async def test_get_archived_document_succeeds(self) -> None:
        upload = await self._upload_document(
            filename="archived-get.md",
            content=b"# Archived Get",
            metadata={
                "title": "Archived Get",
                "owner": "analysis-team",
                "tags": ["archive"],
                "language": "en",
            },
        )
        document_id = upload.json()["data"]["document_id"]
        await self.client.delete(f"/api/v1/documents/{document_id}", headers={"X-Request-ID": "delete-request"})

        response = await self.client.get(f"/api/v1/documents/{document_id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["status"], "archived")

    async def test_list_default_excludes_archived(self) -> None:
        upload = await self._upload_document(
            filename="default-exclude.md",
            content=b"# Default Exclude",
            metadata={
                "title": "Default Exclude",
                "owner": "analysis-team",
                "tags": ["archive"],
                "language": "en",
            },
        )
        document_id = upload.json()["data"]["document_id"]
        await self.client.delete(f"/api/v1/documents/{document_id}", headers={"X-Request-ID": "delete-request"})

        response = await self.client.get("/api/v1/documents")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["items"], [])

    async def test_list_include_archived_includes_archived(self) -> None:
        upload = await self._upload_document(
            filename="include-archived.md",
            content=b"# Include Archived",
            metadata={
                "title": "Include Archived",
                "owner": "analysis-team",
                "tags": ["archive"],
                "language": "en",
            },
        )
        document_id = upload.json()["data"]["document_id"]
        await self.client.delete(f"/api/v1/documents/{document_id}", headers={"X-Request-ID": "delete-request"})

        response = await self.client.get("/api/v1/documents", params={"include_archived": "true"})

        self.assertEqual(response.status_code, 200)
        payload = response.json()["data"]["items"]
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["status"], "archived")

    async def test_archive_missing_document_returns_document_not_found(self) -> None:
        response = await self.client.delete("/api/v1/documents/missing-document")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"]["code"], "document_not_found")

    async def test_archive_already_archived_is_idempotent(self) -> None:
        upload = await self._upload_document(
            filename="idempotent-archive.md",
            content=b"# Idempotent Archive",
            metadata={
                "title": "Idempotent Archive",
                "owner": "analysis-team",
                "tags": ["archive"],
                "language": "en",
            },
        )
        document_id = upload.json()["data"]["document_id"]

        first = await self.client.delete(f"/api/v1/documents/{document_id}")
        second = await self.client.delete(f"/api/v1/documents/{document_id}")

        self.assertEqual(first.status_code, 202)
        self.assertEqual(second.status_code, 202)
        self.assertEqual(first.json()["data"], second.json()["data"])


if __name__ == "__main__":
    unittest.main()
