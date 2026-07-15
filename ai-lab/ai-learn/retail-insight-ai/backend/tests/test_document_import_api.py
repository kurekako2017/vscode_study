from __future__ import annotations

import json
import unittest

import httpx

from app.config.settings import Settings
from app.main import create_app
from tests.postgres_test_utils import reset_postgres_state_if_needed
from tests.auth_test_utils import authorization_headers


class DocumentImportAPITest(unittest.IsolatedAsyncioTestCase):
    """验证文档导入流水线的同步 MVP。"""

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
        content_type: str,
    ) -> httpx.Response:
        files = {
            "file": (filename, content, content_type),
            "metadata": (None, json.dumps(metadata), "application/json"),
        }
        return await self.client.post("/api/v1/documents", files=files, headers={"X-Request-ID": "upload-request"})

    async def _import_document(self, document_id: str) -> httpx.Response:
        return await self.client.post(f"/api/v1/documents/{document_id}/import", headers={"X-Request-ID": "import-request"})

    async def test_upload_markdown_then_import_succeeds(self) -> None:
        upload = await self._upload_document(
            filename="import-markdown.md",
            content=b"# Markdown Import",
            metadata={"title": "Markdown Import", "owner": "analysis-team", "tags": ["import"], "language": "en"},
            content_type="text/markdown",
        )
        document_id = upload.json()["data"]["document_id"]

        response = await self._import_document(document_id)

        self.assertEqual(response.status_code, 201)
        payload = response.json()["data"]
        self.assertEqual(payload["document_id"], document_id)
        self.assertEqual(payload["status"], "completed")

        document = await self.client.get(f"/api/v1/documents/{document_id}")
        self.assertEqual(document.json()["data"]["status"], "validated")

    async def test_upload_text_then_import_succeeds(self) -> None:
        upload = await self._upload_document(
            filename="import-text.txt",
            content=b"plain text import",
            metadata={"title": "Text Import", "owner": "analysis-team", "tags": ["import"], "language": "en"},
            content_type="text/plain",
        )
        document_id = upload.json()["data"]["document_id"]

        response = await self._import_document(document_id)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["data"]["status"], "completed")

    async def test_upload_pdf_then_import_fails_cleanly(self) -> None:
        upload = await self._upload_document(
            filename="import-pdf.pdf",
            content=b"%PDF-1.4",
            metadata={"title": "PDF Import", "owner": "analysis-team", "tags": ["import"], "language": "en"},
            content_type="application/pdf",
        )
        document_id = upload.json()["data"]["document_id"]

        response = await self._import_document(document_id)

        self.assertEqual(response.status_code, 415)
        payload = response.json()
        self.assertFalse(payload["success"])
        self.assertEqual(payload["error"]["code"], "unsupported_document_type")

    async def test_import_missing_document_returns_document_not_found(self) -> None:
        response = await self._import_document("missing-document")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"]["code"], "document_not_found")

    async def test_import_archived_document_returns_document_archived(self) -> None:
        upload = await self._upload_document(
            filename="archived-import.md",
            content=b"# Archived Import",
            metadata={"title": "Archived Import", "owner": "analysis-team", "tags": ["import"], "language": "en"},
            content_type="text/markdown",
        )
        document_id = upload.json()["data"]["document_id"]
        await self.client.delete(f"/api/v1/documents/{document_id}")

        response = await self._import_document(document_id)

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["error"]["code"], "document_archived")

    async def test_repeated_import_behavior_is_deterministic(self) -> None:
        upload = await self._upload_document(
            filename="repeat-import.md",
            content=b"# Repeat Import",
            metadata={"title": "Repeat Import", "owner": "analysis-team", "tags": ["import"], "language": "en"},
            content_type="text/markdown",
        )
        document_id = upload.json()["data"]["document_id"]

        first = await self._import_document(document_id)
        second = await self._import_document(document_id)

        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 201)
        self.assertEqual(first.json()["data"], second.json()["data"])

    async def test_import_status_can_be_read(self) -> None:
        upload = await self._upload_document(
            filename="status-import.md",
            content=b"# Status Import",
            metadata={"title": "Status Import", "owner": "analysis-team", "tags": ["import"], "language": "en"},
            content_type="text/markdown",
        )
        document_id = upload.json()["data"]["document_id"]
        started = await self._import_document(document_id)
        import_id = started.json()["data"]["import_id"]

        response = await self.client.get(f"/api/v1/document-imports/{import_id}")

        self.assertEqual(response.status_code, 200)
        payload = response.json()["data"]
        self.assertEqual(payload["import_id"], import_id)
        self.assertEqual(payload["status"], "completed")

    async def test_import_events_are_recorded(self) -> None:
        upload = await self._upload_document(
            filename="event-import.md",
            content=b"# Event Import",
            metadata={"title": "Event Import", "owner": "analysis-team", "tags": ["import"], "language": "en"},
            content_type="text/markdown",
        )
        document_id = upload.json()["data"]["document_id"]
        started = await self._import_document(document_id)
        import_id = started.json()["data"]["import_id"]

        events = self.app.state.container.event_repository.list_after(import_id)
        self.assertEqual([event.event_type for event in events], ["document.import.started", "document.import.validated", "document.import.completed"])


if __name__ == "__main__":
    unittest.main()
