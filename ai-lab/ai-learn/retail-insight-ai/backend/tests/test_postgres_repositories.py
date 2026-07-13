"""完整 PostgreSQL Repository 合同测试；没有 DATABASE_URL 时明确跳过。"""

from __future__ import annotations

import os
import unittest
from uuid import uuid4

from app.db.connection import PostgresConfig, PostgresConnectionFactory
from app.db.unit_of_work import PostgresUnitOfWork
from app.models.approval import ApprovalEvent, ApprovalRequest, ReportVersion
from app.models.audit import AuditLog, AuditLogResult
from app.models.document import Document, DocumentChunk, DocumentMetadata
from app.models.document_import import DocumentImportRecord
from app.models.report import Report, ReportStatus
from app.models.task import Task, TaskStatus, utc_now
from app.models.upload import UploadSessionRecord
from app.repositories.postgres.approval_repository import PostgresApprovalRepository
from app.repositories.postgres.audit_repository import PostgresAuditRepository
from app.repositories.postgres.document_chunk_repository import PostgresDocumentChunkRepository
from app.repositories.postgres.document_import_repository import PostgresDocumentImportRepository
from app.repositories.postgres.document_repository import PostgresDocumentRepository
from app.repositories.postgres.event_repository import PostgresEventRepository
from app.repositories.postgres.report_repository import PostgresReportRepository
from app.repositories.postgres.task_repository import PostgresTaskRepository
from app.repositories.postgres.upload_session_repository import PostgresUploadSessionRepository


class PostgresRepositoryIntegrationTest(unittest.TestCase):
    """同一组领域合同在真实 PostgreSQL 上验证重启后可恢复的事实。"""

    @classmethod
    def setUpClass(cls) -> None:
        database_url = os.environ.get("DATABASE_URL")
        if not database_url:
            raise unittest.SkipTest("DATABASE_URL is not set; PostgreSQL repository contract tests skipped")
        try:
            import psycopg  # noqa: F401
        except ImportError as exc:
            raise unittest.SkipTest("psycopg is not installed; PostgreSQL repository contract tests skipped") from exc

        cls.connection_factory = PostgresConnectionFactory(
            PostgresConfig(host="", port=5432, db="", user="", password="", database_url=database_url)
        )
        try:
            # 开发测试脚本只验证既有数据库，不负责修改 schema；初始化仍由显式 schema/migration 步骤负责。
            cls.connection_factory.health_check()
        except Exception as exc:
            raise unittest.SkipTest(
                f"PostgreSQL unavailable or schema incompatible: {type(exc).__name__}"
            ) from exc

    def setUp(self) -> None:
        factory = self.connection_factory
        self.task = PostgresTaskRepository(factory)
        self.event = PostgresEventRepository(factory)
        self.report = PostgresReportRepository(factory)
        self.document = PostgresDocumentRepository(factory)
        self.chunk = PostgresDocumentChunkRepository(factory)
        self.document_import = PostgresDocumentImportRepository(factory)
        self.upload = PostgresUploadSessionRepository(factory)
        self.approval = PostgresApprovalRepository(factory)
        self.audit = PostgresAuditRepository(factory)
        self.uow = PostgresUnitOfWork(factory)
        with factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """TRUNCATE upload_idempotency_keys,upload_sessions,document_imports,
                    document_chunks,documents,audit_logs,approval_events,approval_requests,
                    report_versions,reports,events,tasks RESTART IDENTITY CASCADE"""
                )

    def test_task_report_and_generic_event_contract(self) -> None:
        task = self._task()
        self.task.create(task)
        self.event.append(task.task_id, "status", "queued", {"status": "queued"})
        upload_event = self.event.append("upl-independent", "document.upload.started", "started")
        self.report.save(Report(task.task_id, "# report", "static"))

        self.assertEqual(self.task.get(task.task_id).status, TaskStatus.QUEUED)
        self.assertEqual(self.report.get(task.task_id).markdown, "# report")
        self.assertEqual(upload_event.sequence, 1)
        self.assertEqual(self.event.list_after("upl-independent")[0].event_type, "document.upload.started")
        self.assertEqual(self.approval.list_report_versions(task.task_id), [])
        # 重新创建 Repository 等价于应用重启后重新装配，数据库事实仍然可恢复。
        restarted_task_repository = PostgresTaskRepository(self.connection_factory)
        restarted_report_repository = PostgresReportRepository(self.connection_factory)
        self.assertEqual(restarted_task_repository.get(task.task_id).question, "売上を分析")
        self.assertEqual(restarted_report_repository.get(task.task_id).markdown, "# report")

    def test_document_chunk_import_and_upload_session_contract(self) -> None:
        document = self._document()
        self.document.create(document)
        chunk = DocumentChunk(
            document_id=document.document_id,
            version=1,
            chunk_id=f"chk-{uuid4().hex}",
            chunk_index=0,
            content="persistent keyword",
            character_count=18,
            metadata=document.metadata,
        )
        self.chunk.replace_for_document(document.document_id, 1, [chunk])
        import_record = DocumentImportRecord(f"imp-{uuid4().hex}", document.document_id)
        import_record.mark_completed()
        self.document_import.save(import_record)
        now = utc_now()
        session = UploadSessionRecord(
            upload_id=f"upl-{uuid4().hex}", document_id=document.document_id,
            checksum=document.metadata.checksum, status="completed", progress=100,
            created_at=now, updated_at=now, idempotency_key="idem-1",
        )
        self.upload.save(session)

        self.assertEqual(self.document.get(document.document_id).metadata.title, "Persistent document")
        self.assertEqual(self.chunk.list_for_document(document.document_id)[0].content, "persistent keyword")
        self.assertEqual(self.document_import.get(import_record.import_id).status.value, "completed")
        self.assertEqual(self.upload.get_by_idempotency_key("idem-1").upload_id, session.upload_id)

    def test_approval_report_version_and_audit_contract(self) -> None:
        task = self._task()
        self.task.create(task)
        self.report.save(Report(task.task_id, "# versioned", "static"))
        version = ReportVersion(task.task_id, 1, "# versioned", ReportStatus.PENDING_APPROVAL)
        request = ApprovalRequest(task.task_id, version.id, ReportStatus.PENDING_APPROVAL, requested_by="reviewer-a")
        event = ApprovalEvent(request.id, task.task_id, "approval.submitted", actor_id="reviewer-a")
        self.approval.save_report_version(version)
        self.approval.save_approval_request(request)
        self.approval.save_approval_event(event)
        log = AuditLog(
            operation_type="approval.submit", actor_id="reviewer-a", organization_id="org-1",
            department_id="dept-1", resource_type="approval", resource_id=request.id,
            result=AuditLogResult.SUCCESS, request_id="req-1", trace_id="req-1",
            metadata={"comment": "review"},
        )
        self.audit.append(log)

        self.assertEqual(self.approval.get_latest_report_version(task.task_id).id, version.id)
        self.assertEqual(self.approval.get_approval_request(request.id).requested_by, "reviewer-a")
        self.assertEqual(self.approval.list_approval_events(request.id)[0].id, event.id)
        self.assertEqual(self.audit.list_all()[0].metadata, {"comment": "review"})

    def test_unit_of_work_rolls_back_all_task_completion_writes(self) -> None:
        task = self._task()
        self.task.create(task)
        with self.assertRaisesRegex(RuntimeError, "rollback"):
            with self.uow.transaction():
                self.report.save(Report(task.task_id, "# rollback", "static"))
                task.transition(TaskStatus.COMPLETED)
                self.task.save(task)
                self.event.append(task.task_id, "done", "completed")
                raise RuntimeError("rollback")

        self.assertIsNone(self.report.get(task.task_id))
        self.assertEqual(self.task.get(task.task_id).status, TaskStatus.QUEUED)
        self.assertEqual(self.event.list_after(task.task_id), [])

    def _task(self) -> Task:
        return Task(task_id=str(uuid4()), question="売上を分析", mode="hybrid")

    def _document(self) -> Document:
        document_id = f"doc-{uuid4().hex}"
        metadata = DocumentMetadata.from_mapping(
            {
                "document_id": document_id,
                "title": "Persistent document",
                "owner": "analysis-team",
                "language": "en",
                "document_type": "text",
                "status": "uploaded",
                "source": {"source_type": "test", "uri": f"test://{document_id}"},
                "checksum": f"sha256:{uuid4().hex}",
            }
        )
        return Document.create("persistent keyword", metadata)


if __name__ == "__main__":
    unittest.main()
