"""完整 PostgreSQL Repository 合同测试；没有 DATABASE_URL 时明确跳过。"""

from __future__ import annotations

import asyncio
import json
import os
import unittest
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import httpx

from app.db.connection import PostgresConfig, PostgresConnectionFactory
from app.config.settings import Settings
from app.db.unit_of_work import PostgresUnitOfWork
from app.embeddings.provider import DeterministicTestEmbeddingProvider
from app.embeddings.service import EmbeddingService
from app.models.approval import ApprovalEvent, ApprovalRequest, ReportVersion
from app.errors.exceptions import AuditLogAppendException
from app.main import create_app
from app.models.audit import AuditLog, AuditLogFilter, AuditLogResult
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
from app.security.contracts import CurrentUser
from app.services.audit_service import AuditService
from app.services.persistent_audit_service import (
    PersistentAuditContext,
    PersistentAuditService,
    PersistentAuditSpec,
)
from tests.auth_test_utils import ADMIN_PASSWORD
from tests.postgres_test_utils import reset_postgres_state_if_needed


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
        reset_postgres_state_if_needed(Settings(log_level="CRITICAL"))

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

        stored = self.chunk.list_for_document(document.document_id)[0]
        self.assertIsNone(stored.embedding)
        embedding = EmbeddingService(DeterministicTestEmbeddingProvider()).embed_text("persistent keyword")
        self.chunk.update_embedding(chunk.chunk_id, embedding)
        restarted_chunk_repository = PostgresDocumentChunkRepository(self.connection_factory)
        persisted = restarted_chunk_repository.list_for_document(document.document_id)[0]
        self.assertEqual(len(persisted.embedding or ()), len(embedding))
        for stored_value, expected_value in zip(persisted.embedding or (), embedding, strict=True):
            self.assertAlmostEqual(stored_value, expected_value, places=6)
        matches = restarted_chunk_repository.search_by_embedding(
            embedding,
            limit=1,
            document_ids=[document.document_id],
        )
        self.assertEqual(matches[0].chunk.chunk_id, chunk.chunk_id)
        self.assertAlmostEqual(matches[0].cosine_similarity, 1.0, places=6)

    def test_pgvector_schema_contract(self) -> None:
        """真实数据库必须存在 extension、vector(384) 列和 cosine HNSW 索引。"""

        with self.connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT extversion FROM pg_extension WHERE extname='vector'")
                self.assertIsNotNone(cursor.fetchone())
                cursor.execute(
                    """
                    SELECT format_type(a.atttypid, a.atttypmod)
                    FROM pg_attribute a
                    JOIN pg_class c ON c.oid=a.attrelid
                    WHERE c.relname='document_chunks' AND a.attname='embedding'
                      AND a.attnum > 0 AND NOT a.attisdropped
                    """
                )
                self.assertEqual(cursor.fetchone(), ("vector(384)",))
                cursor.execute(
                    """
                    SELECT indexdef FROM pg_indexes
                    WHERE tablename='document_chunks'
                      AND indexname='idx_document_chunks_embedding_hnsw'
                    """
                )
                index_row = cursor.fetchone()
                self.assertIsNotNone(index_row)
                self.assertIn("vector_cosine_ops", index_row[0])

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

    def test_persistent_audit_schema_query_and_restart_contract(self) -> None:
        """验证新增列、索引、过滤、分页、稳定排序与 Repository 重建读取。"""

        occurred_at = datetime(2026, 7, 16, 1, 0, tzinfo=timezone.utc)
        first = AuditLog(
            operation_type="retrieval.query",
            actor_id="user-manager",
            organization_id=None,
            department_id=None,
            resource_type="document_retrieval",
            resource_id="query-a",
            result=AuditLogResult.SUCCESS,
            request_id="audit-query-request",
            trace_id="audit-query-request",
            metadata={"mode": "keyword"},
            audit_log_id="audit-a",
            timestamp=occurred_at,
            actor_username="manager",
            actor_role="manager",
            permission="retrieval.query",
            http_method="POST",
            api_path="/api/v1/document-retrieval/search",
            status_code=200,
        )
        second = AuditLog(
            operation_type="retrieval.query",
            actor_id="user-manager",
            organization_id=None,
            department_id=None,
            resource_type="document_retrieval",
            resource_id="query-b",
            result=AuditLogResult.FAILURE,
            request_id="audit-query-request-2",
            trace_id="audit-query-request-2",
            metadata={"exception_type": "InvalidQueryException"},
            error_code="invalid_query",
            audit_log_id="audit-z",
            timestamp=occurred_at,
            actor_username="manager",
            actor_role="manager",
            permission="retrieval.query",
            http_method="POST",
            api_path="/api/v1/document-retrieval/search",
            status_code=422,
        )
        self.audit.append(first)
        self.audit.append(second)

        page = self.audit.query(
            AuditLogFilter(
                actor_user_id="user-manager",
                actor_username="manager",
                actor_role="manager",
                action="retrieval.query",
                resource_type="document_retrieval",
                result=AuditLogResult.FAILURE,
                start_time=occurred_at - timedelta(seconds=1),
                end_time=occurred_at + timedelta(seconds=1),
                request_id="audit-query-request-2",
                limit=1,
            )
        )
        self.assertEqual([item.audit_log_id for item in page.items], ["audit-z"])
        self.assertIsNone(page.next_offset)

        stable_first_page = self.audit.query(AuditLogFilter(limit=1))
        stable_second_page = self.audit.query(AuditLogFilter(limit=1, offset=1))
        self.assertEqual(stable_first_page.items[0].audit_log_id, "audit-z")
        self.assertEqual(stable_first_page.next_offset, 1)
        self.assertEqual(stable_second_page.items[0].audit_log_id, "audit-a")

        restarted = PostgresAuditRepository(self.connection_factory)
        restored = restarted.query(
            AuditLogFilter(resource_id="query-b", limit=10)
        ).items[0]
        self.assertEqual(restored.actor_username, "manager")
        self.assertEqual(restored.result, AuditLogResult.FAILURE)
        self.assertEqual(restored.status_code, 422)

        with self.connection_factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name = 'audit_logs'
                      AND column_name IN (
                          'actor_username','actor_role','permission',
                          'http_method','api_path','status_code'
                      )
                    ORDER BY column_name
                    """
                )
                self.assertEqual(len(cursor.fetchall()), 6)
                cursor.execute(
                    """
                    SELECT indexname
                    FROM pg_indexes
                    WHERE tablename = 'audit_logs'
                      AND indexname IN (
                          'idx_audit_logs_created_id_desc',
                          'idx_audit_logs_actor_created',
                          'idx_audit_logs_action_created',
                          'idx_audit_logs_request_id'
                      )
                    """
                )
                self.assertEqual(len(cursor.fetchall()), 4)

    def test_audit_append_failure_rolls_back_successful_business_write(self) -> None:
        """审计不可用时，业务事实与成功响应都不能被提交。"""

        class FailingAuditRepository:
            def append(self, log: AuditLog) -> AuditLog:
                raise RuntimeError("audit unavailable")

            def list_all(self) -> list[AuditLog]:
                return []

        task = self._task()
        persistent = PersistentAuditService(
            AuditService(FailingAuditRepository()),
            self.uow,
            enabled=True,
        )
        context = PersistentAuditContext(
            request_id="audit-write-failure",
            http_method="POST",
            api_path="/api/tasks",
            resource_id=task.task_id,
            current_user=CurrentUser(
                user_id="user-admin",
                username="admin",
                role="admin",
            ),
        )

        async def execute() -> None:
            async with persistent.operation(
                PersistentAuditSpec(
                    action="analysis.execute",
                    resource_type="task",
                    resource_id=task.task_id,
                    success_status_code=202,
                    permission="analysis.execute",
                ),
                lambda: context,
            ):
                self.task.create(task)

        with self.assertRaises(AuditLogAppendException):
            asyncio.run(execute())
        self.assertIsNone(self.task.get(task.task_id))

    def test_persistent_audit_http_chain_and_read_only_api(self) -> None:
        """验证关键 HTTP 事件、CurrentUser actor、403、敏感信息和去重。"""

        asyncio.run(self._assert_persistent_audit_http_chain())

    async def _assert_persistent_audit_http_chain(self) -> None:
        settings = Settings(log_level="CRITICAL")
        app = create_app(settings)
        client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        )
        try:
            login_success = await client.post(
                "/api/v1/auth/login",
                headers={"X-Request-ID": "login-success-request"},
                json={"username": "admin", "password": ADMIN_PASSWORD},
            )
            self.assertEqual(login_success.status_code, 200)
            admin_token = login_success.json()["data"]["access_token"]
            admin_headers = {
                "Authorization": f"Bearer {admin_token}",
                "X-Actor-User-ID": "client-spoofed-user",
            }

            login_failure = await client.post(
                "/api/v1/auth/login",
                headers={"X-Request-ID": "login-failure-request"},
                json={"username": "admin", "password": "do-not-store-this-password"},
            )
            self.assertEqual(login_failure.status_code, 401)

            upload = await client.post(
                "/api/v1/documents",
                headers={**admin_headers, "X-Request-ID": "document-upload-request"},
                files={
                    "file": ("audit.md", b"# Audit\npersistent audit", "text/markdown"),
                    "metadata": (
                        None,
                        json.dumps(
                            {
                                "title": "Audit Document",
                                "owner": "audit-team",
                                "password": "must-not-be-audited",
                            }
                        ),
                    ),
                },
            )
            self.assertEqual(upload.status_code, 201)
            document_id = upload.json()["data"]["document_id"]

            imported = await client.post(
                f"/api/v1/documents/{document_id}/import",
                headers={**admin_headers, "X-Request-ID": "document-import-request"},
            )
            self.assertEqual(imported.status_code, 201)

            archived = await client.delete(
                f"/api/v1/documents/{document_id}",
                headers={**admin_headers, "X-Request-ID": "document-archive-request"},
            )
            self.assertEqual(archived.status_code, 202)
            archive_failure = await client.delete(
                "/api/v1/documents/missing-audit-document",
                headers={
                    **admin_headers,
                    "X-Request-ID": "document-archive-failure-request",
                },
            )
            self.assertEqual(archive_failure.status_code, 404)

            retrieval = await client.post(
                "/api/v1/document-retrieval/search",
                headers={**admin_headers, "X-Request-ID": "retrieval-request"},
                json={"query": "audit", "retrieval_mode": "keyword"},
            )
            self.assertEqual(retrieval.status_code, 200)

            task_response = await client.post(
                "/api/tasks",
                headers={**admin_headers, "X-Request-ID": "analysis-request"},
                json={"question": "監査対象を分析", "mode": "kpi"},
            )
            self.assertEqual(task_response.status_code, 202)
            task_id = task_response.json()["data"]["task_id"]

            submit = await client.post(
                f"/api/v1/reports/{task_id}/submit-approval",
                headers={**admin_headers, "X-Request-ID": "approval-submit-request"},
                json={"comment": "review"},
            )
            self.assertEqual(submit.status_code, 201)
            approval_id = submit.json()["data"]["approval_id"]

            review = await client.get(
                "/api/v1/approvals",
                headers={**admin_headers, "X-Request-ID": "approval-review-request"},
            )
            self.assertEqual(review.status_code, 200)

            approved = await client.post(
                f"/api/v1/approvals/{approval_id}/approve",
                headers={**admin_headers, "X-Request-ID": "approval-admin-request"},
                json={"comment": "approved"},
            )
            self.assertEqual(approved.status_code, 200)

            security = await client.get(
                "/api/v1/security/roles",
                headers={**admin_headers, "X-Request-ID": "security-manage-request"},
            )
            self.assertEqual(security.status_code, 200)

            employee = CurrentUser(
                user_id="user-employee",
                username="employee",
                role="employee",
            )
            employee_token = app.state.container.jwt_service.create_access_token(employee)
            denied = await client.get(
                "/api/v1/audit-logs",
                headers={
                    "Authorization": f"Bearer {employee_token.access_token}",
                    "X-Request-ID": "audit-denied-request",
                },
            )
            self.assertEqual(denied.status_code, 403)
            unauthenticated = await client.get(
                "/api/tasks/missing",
                headers={"X-Request-ID": "authentication-failure-request"},
            )
            self.assertEqual(unauthenticated.status_code, 401)

            audit_read = await client.get(
                "/api/v1/audit-logs",
                headers={**admin_headers, "X-Request-ID": "audit-read-request"},
                params={"action": "login.success", "actor_username": "admin", "limit": 1},
            )
            self.assertEqual(audit_read.status_code, 200)
            item = audit_read.json()["data"]["items"][0]
            self.assertEqual(item["action"], "login.success")
            self.assertEqual(item["actor_user_id"], "user-admin")
            self.assertEqual(item["actor_role"], "admin")
            self.assertEqual(item["http_method"], "POST")
            self.assertEqual(item["api_path"], "/api/v1/auth/login")

            invalid_range = await client.get(
                "/api/v1/audit-logs",
                headers=admin_headers,
                params={
                    "start_time": "2026-07-17T00:00:00+00:00",
                    "end_time": "2026-07-16T00:00:00+00:00",
                },
            )
            self.assertEqual(invalid_range.status_code, 422)
            too_large = await client.get(
                "/api/v1/audit-logs",
                headers=admin_headers,
                params={"limit": 201},
            )
            self.assertEqual(too_large.status_code, 422)

            methods = set(app.openapi()["paths"]["/api/v1/audit-logs"])
            self.assertEqual(methods, {"get"})
        finally:
            await client.aclose()

        logs = PostgresAuditRepository(self.connection_factory).query(
            AuditLogFilter(limit=200)
        ).items
        by_request = {log.request_id: log for log in logs}
        expected = {
            "login-success-request": ("login.success", AuditLogResult.SUCCESS),
            "login-failure-request": ("login.failure", AuditLogResult.FAILURE),
            "document-upload-request": ("document.upload", AuditLogResult.SUCCESS),
            "document-import-request": ("document.import", AuditLogResult.SUCCESS),
            "document-archive-request": ("document.archive", AuditLogResult.SUCCESS),
            "document-archive-failure-request": (
                "document.archive",
                AuditLogResult.FAILURE,
            ),
            "retrieval-request": ("retrieval.query", AuditLogResult.SUCCESS),
            "analysis-request": ("analysis.execute", AuditLogResult.SUCCESS),
            "approval-submit-request": ("approval.submitted", AuditLogResult.SUCCESS),
            "approval-review-request": ("approval.listed", AuditLogResult.SUCCESS),
            "approval-admin-request": ("approval.approved", AuditLogResult.SUCCESS),
            "security-manage-request": ("security.manage", AuditLogResult.SUCCESS),
            "audit-denied-request": ("authorization.denied", AuditLogResult.DENIED),
            "authentication-failure-request": (
                "authentication.failure",
                AuditLogResult.FAILURE,
            ),
            "audit-read-request": ("audit.read", AuditLogResult.SUCCESS),
        }
        for request_id, (action, result) in expected.items():
            with self.subTest(request_id=request_id):
                self.assertIn(request_id, by_request)
                self.assertEqual(by_request[request_id].operation_type, action)
                self.assertEqual(by_request[request_id].result, result)

        self.assertEqual(by_request["retrieval-request"].actor_id, "user-admin")
        self.assertEqual(by_request["retrieval-request"].actor_username, "admin")
        self.assertNotEqual(
            by_request["retrieval-request"].actor_id,
            "client-spoofed-user",
        )
        self.assertEqual(by_request["audit-denied-request"].permission, "audit.read")
        self.assertEqual(by_request["audit-denied-request"].status_code, 403)
        self.assertEqual(
            len(
                [
                    log
                    for log in logs
                    if log.request_id == "approval-submit-request"
                    and log.operation_type == "approval.submitted"
                ]
            ),
            1,
        )
        serialized = json.dumps(
            [
                {
                    "metadata": log.metadata,
                    "actor_username": log.actor_username,
                    "error_code": log.error_code,
                }
                for log in logs
            ],
            ensure_ascii=False,
        )
        self.assertNotIn("do-not-store-this-password", serialized)
        self.assertNotIn("must-not-be-audited", serialized)
        self.assertNotIn(admin_token, serialized)

        # 新 App/Repository/连接重新装配后，审计事实仍可读取。
        restarted_app = create_app(Settings(log_level="CRITICAL"))
        restarted_logs = restarted_app.state.container.audit_service.query_audit_logs(
            AuditLogFilter(request_id="login-success-request", limit=10)
        ).items
        self.assertEqual(restarted_logs[0].operation_type, "login.success")

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
