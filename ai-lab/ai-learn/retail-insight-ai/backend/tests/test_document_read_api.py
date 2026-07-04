from __future__ import annotations

import json
import unittest

import httpx

from app.config.settings import Settings
from app.main import create_app


class DocumentReadAPITest(unittest.IsolatedAsyncioTestCase):
    """验证 GET /api/v1/documents 与 GET /api/v1/documents/{document_id}。"""

    async def asyncSetUp(self) -> None:
        self.app = create_app(Settings(workflow_step_delay_seconds=0, log_level="CRITICAL"))
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
        content_type: str = "text/markdown",
    ) -> httpx.Response:
        files = {
            "file": (filename, content, content_type),
            "metadata": (None, json.dumps(metadata), "application/json"),
        }
        return await self.client.post("/api/v1/documents", files=files, headers={"X-Request-ID": "upload-request"})

    async def test_list_documents_empty(self) -> None:
        response = await self.client.get("/api/v1/documents")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["success"])
        self.assertEqual(payload["data"]["items"], [])
        self.assertIsNone(payload["data"]["next_cursor"])

    async def test_upload_then_list_documents(self) -> None:
        await self._upload_document(
            filename="read-list.md",
            content=b"# Read List",
            metadata={
                "title": "Read List",
                "owner": "analysis-team",
                "tags": ["list", "read"],
                "language": "en",
            },
        )

        response = await self.client.get("/api/v1/documents")

        self.assertEqual(response.status_code, 200)
        payload = response.json()["data"]
        self.assertEqual(len(payload["items"]), 1)
        self.assertEqual(payload["items"][0]["title"], "Read List")
        self.assertEqual(payload["items"][0]["status"], "uploaded")

    async def test_upload_then_get_document(self) -> None:
        upload = await self._upload_document(
            filename="read-get.md",
            content=b"# Read Get",
            metadata={
                "title": "Read Get",
                "owner": "analysis-team",
                "tags": ["detail"],
                "language": "en",
            },
        )
        document_id = upload.json()["data"]["document_id"]

        response = await self.client.get(f"/api/v1/documents/{document_id}")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["success"])
        self.assertEqual(payload["data"]["document_id"], document_id)
        self.assertEqual(payload["data"]["title"], "Read Get")
        self.assertEqual(payload["data"]["status"], "uploaded")

    async def test_get_missing_document_returns_document_not_found(self) -> None:
        response = await self.client.get("/api/v1/documents/missing-document")

        self.assertEqual(response.status_code, 404)
        payload = response.json()
        self.assertFalse(payload["success"])
        self.assertEqual(payload["error"]["code"], "document_not_found")

    async def test_list_filters_by_status_type_language_tag(self) -> None:
        await self._upload_document(
            filename="filter-a.md",
            content=b"# Filter A",
            metadata={
                "title": "Filter A",
                "owner": "analysis-team",
                "tags": ["sales", "monthly"],
                "language": "en",
            },
        )
        await self._upload_document(
            filename="filter-b.csv",
            content=b"month,sales\n2026-06,100",
            content_type="text/csv",
            metadata={
                "title": "Filter B",
                "owner": "analysis-team",
                "tags": ["ops"],
                "language": "ja",
                "document_type": "csv",
            },
        )

        by_status = await self.client.get("/api/v1/documents", params={"status": "uploaded"})
        self.assertEqual(len(by_status.json()["data"]["items"]), 2)

        by_type = await self.client.get("/api/v1/documents", params={"document_type": "csv"})
        self.assertEqual(len(by_type.json()["data"]["items"]), 1)
        self.assertEqual(by_type.json()["data"]["items"][0]["document_type"], "csv")

        by_language = await self.client.get("/api/v1/documents", params={"language": "ja"})
        self.assertEqual(len(by_language.json()["data"]["items"]), 1)
        self.assertEqual(by_language.json()["data"]["items"][0]["language"], "ja")

        by_tag = await self.client.get("/api/v1/documents", params={"tag": "monthly"})
        self.assertEqual(len(by_tag.json()["data"]["items"]), 1)
        self.assertEqual(by_tag.json()["data"]["items"][0]["title"], "Filter A")


if __name__ == "__main__":
    unittest.main()
