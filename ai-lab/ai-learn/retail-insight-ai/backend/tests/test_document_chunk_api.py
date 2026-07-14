from __future__ import annotations

import json
import unittest

import httpx

from app.db.connection import PostgresConfig, PostgresConnectionFactory
from app.config.settings import Settings
from app.errors.error_codes import ErrorCode
from app.main import create_app
from app.models.document import Document, DocumentMetadata, DocumentStatus, DocumentType


class DocumentChunkAPITest(unittest.IsolatedAsyncioTestCase):
    """验证文档 chunk 流水线的同步 MVP。"""

    async def asyncSetUp(self) -> None:
        settings = Settings(workflow_step_delay_seconds=0, log_level="CRITICAL")
        self._reset_postgres_state_if_needed(settings)
        self.app = create_app(settings)
        transport = httpx.ASGITransport(app=self.app)
        self.client = httpx.AsyncClient(transport=transport, base_url="http://test")

    async def asyncTearDown(self) -> None:
        await self.client.aclose()

    def _reset_postgres_state_if_needed(self, settings: Settings) -> None:
        """PostgreSQL 模式下清理测试库，避免跨用例残留破坏 API 测试隔离。"""

        if settings.repository_backend != "postgres" or not settings.database_url:
            return

        factory = PostgresConnectionFactory(
            PostgresConfig(host="", port=5432, db="", user="", password="", database_url=settings.database_url)
        )
        with factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """TRUNCATE upload_idempotency_keys,upload_sessions,document_imports,
                    document_chunks,documents,audit_logs,approval_events,approval_requests,
                    report_versions,reports,events,tasks RESTART IDENTITY CASCADE"""
                )

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

    async def _get_chunks(self, document_id: str) -> httpx.Response:
        return await self.client.get(f"/api/v1/documents/{document_id}/chunks")

    def _seed_validated_document(
        self,
        *,
        document_id: str,
        document_type: DocumentType,
        content: str,
    ) -> None:
        repository = self.app.state.container.document_repository
        metadata = DocumentMetadata.from_mapping(
            {
                "document_id": document_id,
                "title": f"Seeded {document_id}",
                "owner": "analysis-team",
                "document_type": document_type,
                "language": "en",
                "status": DocumentStatus.UPLOADED,
                "source": {
                    "source_type": "local_file",
                    "uri": f"backend/data/documents/{document_id}",
                },
                "checksum": f"sha256:{document_id}",
            }
        )
        document = Document.create(content, metadata)
        repository.create(document)
        stored = repository.get(document_id)
        assert stored is not None
        stored.transition_status(DocumentStatus.VALIDATED)
        repository.update(stored)

    async def test_upload_markdown_then_import_then_chunk_succeeds(self) -> None:
        upload = await self._upload_document(
            filename="chunk-markdown.md",
            content=b"# Chunk Markdown\n\nParagraph one.\n\nParagraph two.",
            metadata={"title": "Chunk Markdown", "owner": "analysis-team", "tags": ["chunk"], "language": "en"},
            content_type="text/markdown",
        )
        document_id = upload.json()["data"]["document_id"]

        await self._import_document(document_id)
        response = await self._chunk_document(document_id)

        self.assertEqual(response.status_code, 201)
        payload = response.json()["data"]
        self.assertEqual(payload["document_id"], document_id)
        self.assertGreaterEqual(len(payload["items"]), 2)
        self.assertEqual(payload["items"][0]["chunk_index"], 0)
        self.assertEqual(payload["items"][0]["character_count"], len(payload["items"][0]["content"]))

        events = [event.event_type for event in self.app.state.container.event_repository.list_after(document_id)]
        self.assertIn("document.chunk.started", events)
        self.assertIn("document.chunk.completed", events)

    async def test_upload_text_then_import_then_chunk_succeeds(self) -> None:
        upload = await self._upload_document(
            filename="chunk-text.txt",
            content=b"First paragraph.\n\nSecond paragraph.",
            metadata={"title": "Chunk Text", "owner": "analysis-team", "tags": ["chunk"], "language": "en"},
            content_type="text/plain",
        )
        document_id = upload.json()["data"]["document_id"]

        await self._import_document(document_id)
        response = await self._chunk_document(document_id)

        self.assertEqual(response.status_code, 201)
        self.assertGreater(len(response.json()["data"]["items"]), 0)

    async def test_chunk_before_import_returns_document_not_validated(self) -> None:
        upload = await self._upload_document(
            filename="not-imported.md",
            content=b"# Not Imported",
            metadata={"title": "Not Imported", "owner": "analysis-team", "tags": ["chunk"], "language": "en"},
            content_type="text/markdown",
        )
        document_id = upload.json()["data"]["document_id"]

        response = await self._chunk_document(document_id)

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["error"]["code"], ErrorCode.DOCUMENT_NOT_VALIDATED.value)

    async def test_chunk_archived_document_returns_document_archived(self) -> None:
        upload = await self._upload_document(
            filename="archived-chunk.md",
            content=b"# Archived Chunk",
            metadata={"title": "Archived Chunk", "owner": "analysis-team", "tags": ["chunk"], "language": "en"},
            content_type="text/markdown",
        )
        document_id = upload.json()["data"]["document_id"]
        await self._import_document(document_id)
        await self.client.delete(f"/api/v1/documents/{document_id}")

        response = await self._chunk_document(document_id)

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["error"]["code"], "document_archived")

    async def test_chunk_unsupported_pdf_returns_unsupported_document_type(self) -> None:
        document_id = "doc-seeded-pdf"
        self._seed_validated_document(
            document_id=document_id,
            document_type=DocumentType.PDF,
            content="%PDF-1.4 seed",
        )

        response = await self._chunk_document(document_id)

        self.assertEqual(response.status_code, 415)
        self.assertEqual(response.json()["error"]["code"], "unsupported_document_type")
        events = [event.event_type for event in self.app.state.container.event_repository.list_after(document_id)]
        self.assertIn("document.chunk.started", events)
        self.assertIn("document.chunk.failed", events)

    async def test_get_chunks_returns_stored_chunks(self) -> None:
        upload = await self._upload_document(
            filename="stored-chunks.md",
            content=b"# Stored Chunks\n\nAlpha.\n\nBeta.",
            metadata={"title": "Stored Chunks", "owner": "analysis-team", "tags": ["chunk"], "language": "en"},
            content_type="text/markdown",
        )
        document_id = upload.json()["data"]["document_id"]
        await self._import_document(document_id)
        created = await self._chunk_document(document_id)

        response = await self._get_chunks(document_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["items"], created.json()["data"]["items"])

    async def test_repeated_chunk_behavior_is_deterministic(self) -> None:
        upload = await self._upload_document(
            filename="repeat-chunks.md",
            content=b"# Repeat Chunks\n\nOne.\n\nTwo.",
            metadata={"title": "Repeat Chunks", "owner": "analysis-team", "tags": ["chunk"], "language": "en"},
            content_type="text/markdown",
        )
        document_id = upload.json()["data"]["document_id"]
        await self._import_document(document_id)

        first = await self._chunk_document(document_id)
        second = await self._chunk_document(document_id)

        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 201)
        self.assertEqual(first.json()["data"], second.json()["data"])


if __name__ == "__main__":
    unittest.main()
