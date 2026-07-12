from __future__ import annotations

import unittest

from app.errors.exceptions import ValidationAppException
from app.models.document import (
    ApprovalStatus,
    Document,
    DocumentMetadata,
    DocumentSource,
    DocumentStatus,
    DocumentType,
    ImportBatch,
    Language,
)
from app.models.persistence import DataImport
from app.repositories.implementations.in_memory.document_repository import InMemoryDocumentRepository
from app.repositories.interfaces.document_repository import DocumentRepository


class DocumentDomainModelTest(unittest.TestCase):
    """验证 Document 域模型、状态迁移和元数据校验。"""

    def test_document_creation_uses_uploaded_status_and_reuses_import_batch(self) -> None:
        metadata = DocumentMetadata.from_mapping(
            {
                "document_id": "doc-001",
                "title": "Monthly Policy",
                "description": "Internal policy document",
                "owner": "ops",
                "version": 1,
                "language": Language.EN,
                "document_type": DocumentType.MARKDOWN,
                "status": DocumentStatus.UPLOADED,
                "tags": ["policy", "monthly"],
                "source": {
                    "source_type": "local_file",
                    "uri": "backend/data/documents/monthly-policy.md",
                },
                "checksum": "sha256:abc123",
            }
        )

        document = Document.create("Document body", metadata)

        self.assertEqual(document.document_id, "doc-001")
        self.assertEqual(document.status, DocumentStatus.UPLOADED)
        self.assertEqual(document.approval_status, ApprovalStatus.GENERATED)
        self.assertEqual(document.to_version().version, 1)
        self.assertIs(ImportBatch, DataImport)

    def test_metadata_validation_rejects_missing_title(self) -> None:
        with self.assertRaises(ValidationAppException):
            DocumentMetadata.from_mapping(
                {
                    "document_id": "doc-002",
                    "owner": "ops",
                    "source": {
                        "source_type": "local_file",
                        "uri": "backend/data/documents/missing-title.md",
                    },
                    "checksum": "sha256:def456",
                }
            )

    def test_document_creation_rejects_empty_file(self) -> None:
        metadata = DocumentMetadata.from_mapping(
            {
                "document_id": "doc-003",
                "title": "Empty File",
                "owner": "ops",
                "document_type": DocumentType.MARKDOWN,
                "source": {
                    "source_type": "local_file",
                    "uri": "backend/data/documents/empty.md",
                },
                "checksum": "sha256:ghi789",
            }
        )

        with self.assertRaises(ValidationAppException):
            Document.create("   ", metadata)

    def test_document_creation_rejects_future_image_type(self) -> None:
        metadata = DocumentMetadata.from_mapping(
            {
                "document_id": "doc-004",
                "title": "Image Placeholder",
                "owner": "ops",
                "document_type": DocumentType.IMAGE,
                "source": {
                    "source_type": "local_file",
                    "uri": "backend/data/documents/image.png",
                },
                "checksum": "sha256:jkl012",
            }
        )

        with self.assertRaises(ValidationAppException):
            Document.create("binary placeholder", metadata)

    def test_status_transition_advances_by_one_step_only(self) -> None:
        metadata = DocumentMetadata.from_mapping(
            {
                "document_id": "doc-005",
                "title": "Lifecycle",
                "owner": "ops",
                "source": {
                    "source_type": "local_file",
                    "uri": "backend/data/documents/lifecycle.md",
                },
                "checksum": "sha256:mno345",
            }
        )
        document = Document.create("Document body", metadata)

        document.transition_status(DocumentStatus.VALIDATED)

        self.assertEqual(document.status, DocumentStatus.VALIDATED)
        self.assertEqual(document.metadata.updated_at, document.updated_at)

        with self.assertRaises(ValidationAppException):
            document.transition_status(DocumentStatus.PUBLISHED)


class DocumentMetadataValidationTest(unittest.TestCase):
    """验证元数据对象本身的来源与字段转换。"""

    def test_document_source_validation(self) -> None:
        source = DocumentSource.from_mapping(
            {
                "source_type": "api",
                "uri": "https://example.invalid/doc/1",
            }
        )

        self.assertEqual(source.source_type, "api")
        self.assertEqual(source.uri, "https://example.invalid/doc/1")


class InMemoryDocumentRepositoryTest(unittest.TestCase):
    """验证文档仓库 CRUD 和 checksum 去重。"""
    # 设置测试环境
    def setUp(self) -> None:
        self.repository = InMemoryDocumentRepository()
    # 测试仓库实现
    def test_repository_implements_protocol(self) -> None:
        self.assertIsInstance(self.repository, DocumentRepository)
    # 测试仓库 CRUD
    def test_repository_crud(self) -> None:
        document = self._build_document("doc-100", "sha256:repo-100")
        self.repository.create(document)
        # 测试文档加载
        loaded = self.repository.get("doc-100")
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.document_id, "doc-100")
        self.assertEqual(len(self.repository.list_all()), 1)

        loaded.transition_status(DocumentStatus.VALIDATED)
        loaded.content = "Updated document body"
        self.repository.update(loaded)

        updated = self.repository.get("doc-100")
        self.assertIsNotNone(updated)
        self.assertEqual(updated.status, DocumentStatus.VALIDATED)
        self.assertEqual(updated.content, "Updated document body")

        self.repository.delete("doc-100")
        archived = self.repository.get("doc-100")
        self.assertIsNotNone(archived)
        self.assertEqual(archived.status, DocumentStatus.ARCHIVED)

        self.repository.delete("doc-100")
        archived_again = self.repository.get("doc-100")
        self.assertIsNotNone(archived_again)
        self.assertEqual(archived_again.status, DocumentStatus.ARCHIVED)
    # 
    def test_repository_rejects_duplicate_checksum(self) -> None:
        first = self._build_document("doc-200", "sha256:dup-200")
        second = self._build_document("doc-201", "sha256:dup-200")

        self.repository.create(first)
        with self.assertRaises(ValidationAppException):
            self.repository.create(second)

    def _build_document(self, document_id: str, checksum: str) -> Document:
        metadata = DocumentMetadata.from_mapping(
            {
                "document_id": document_id,
                "title": f"Document {document_id}",
                "owner": "ops",
                "document_type": DocumentType.MARKDOWN,
                "source": {
                    "source_type": "local_file",
                    "uri": f"backend/data/documents/{document_id}.md",
                },
                "checksum": checksum,
            }
        )
        return Document.create(f"# {document_id}", metadata)


if __name__ == "__main__":
    unittest.main()
