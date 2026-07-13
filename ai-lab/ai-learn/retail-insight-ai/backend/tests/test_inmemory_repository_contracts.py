"""默认 InMemory Bundle 的完整 Repository 合同测试。"""

from __future__ import annotations

import unittest
from uuid import uuid4

from app.models.approval import ApprovalEvent, ApprovalRequest, ReportVersion
from app.models.audit import AuditLog, AuditLogResult
from app.models.document import Document, DocumentChunk, DocumentMetadata
from app.models.document_import import DocumentImportRecord
from app.models.report import Report, ReportStatus
from app.models.task import Task, TaskStatus, utc_now
from app.models.upload import UploadSessionRecord
from app.repositories.implementations.in_memory.approval_repository import InMemoryApprovalRepository
from app.repositories.implementations.in_memory.audit_repository import InMemoryAuditRepository
from app.repositories.implementations.in_memory.document_chunk_repository import InMemoryDocumentChunkRepository
from app.repositories.implementations.in_memory.document_import_repository import InMemoryDocumentImportRepository
from app.repositories.implementations.in_memory.document_repository import InMemoryDocumentRepository
from app.repositories.implementations.in_memory.event_repository import InMemoryEventRepository
from app.repositories.implementations.in_memory.report_repository import InMemoryReportRepository
from app.repositories.implementations.in_memory.task_repository import InMemoryTaskRepository
from app.repositories.implementations.in_memory.upload_session_repository import InMemoryUploadSessionRepository


class InMemoryRepositoryContractTest(unittest.TestCase):
    """与 PostgreSQL integration suite 对齐的核心事实合同。"""

    def setUp(self) -> None:
        self.task = InMemoryTaskRepository()
        self.report = InMemoryReportRepository()
        self.event = InMemoryEventRepository()
        self.document = InMemoryDocumentRepository()
        self.chunk = InMemoryDocumentChunkRepository()
        self.document_import = InMemoryDocumentImportRepository()
        self.upload = InMemoryUploadSessionRepository()
        self.approval = InMemoryApprovalRepository()
        self.audit = InMemoryAuditRepository()

    def test_complete_repository_bundle_contract(self) -> None:
        task = Task(str(uuid4()), "売上を分析", "hybrid")
        self.task.create(task)
        task.transition(TaskStatus.RUNNING)
        self.task.save(task)
        self.report.save(Report(task.task_id, "# report", "static"))
        self.event.append(task.task_id, "status", "running")
        self.event.append("upl-independent", "document.upload.started", "started")

        document_id = f"doc-{uuid4().hex}"
        metadata = DocumentMetadata.from_mapping(
            {
                "document_id": document_id, "title": "Contract", "owner": "team",
                "language": "en", "document_type": "text", "status": "uploaded",
                "source": {"source_type": "test", "uri": f"test://{document_id}"},
                "checksum": f"sha256:{uuid4().hex}",
            }
        )
        document = Document.create("persistent keyword", metadata)
        self.document.create(document)
        chunk = DocumentChunk(document_id, 1, f"chk-{uuid4().hex}", 0, "persistent keyword", 18, metadata)
        self.chunk.replace_for_document(document_id, 1, [chunk])
        imported = DocumentImportRecord(f"imp-{uuid4().hex}", document_id)
        imported.mark_completed()
        self.document_import.save(imported)
        now = utc_now()
        session = UploadSessionRecord(
            f"upl-{uuid4().hex}", document_id, metadata.checksum, "completed", 100,
            now, now, idempotency_key="idem-contract",
        )
        self.upload.save(session)

        version = ReportVersion(task.task_id, 1, "# report", ReportStatus.PENDING_APPROVAL)
        approval = ApprovalRequest(task.task_id, version.id, ReportStatus.PENDING_APPROVAL)
        approval_event = ApprovalEvent(approval.id, task.task_id, "approval.submitted")
        self.approval.save_report_version(version)
        self.approval.save_approval_request(approval)
        self.approval.save_approval_event(approval_event)
        audit = AuditLog(
            "approval.submit", "user-1", "org-1", "dept-1", "approval", approval.id,
            AuditLogResult.SUCCESS, "req-1", "req-1",
        )
        self.audit.append(audit)

        self.assertEqual(self.task.get(task.task_id).status, TaskStatus.RUNNING)
        self.assertEqual(self.report.get(task.task_id).markdown, "# report")
        self.assertEqual(self.event.list_after("upl-independent")[0].sequence, 1)
        self.assertEqual(self.document.get(document_id).metadata.title, "Contract")
        self.assertEqual(self.chunk.list_for_document(document_id)[0].chunk_id, chunk.chunk_id)
        self.assertEqual(self.document_import.get(imported.import_id).status.value, "completed")
        self.assertEqual(self.upload.get_by_idempotency_key("idem-contract").upload_id, session.upload_id)
        self.assertEqual(self.approval.get_approval_request(approval.id).id, approval.id)
        self.assertEqual(self.audit.list_all()[0].audit_log_id, audit.audit_log_id)


if __name__ == "__main__":
    unittest.main()
