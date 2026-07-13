from __future__ import annotations

import inspect
import unittest

from app.repositories.implementations.in_memory.document_repository import InMemoryDocumentRepository
from app.repositories.implementations.in_memory.report_repository import InMemoryReportRepository
from app.repositories.implementations.in_memory.task_repository import InMemoryTaskRepository
from app.repositories.implementations.in_memory.approval_repository import InMemoryApprovalRepository
from app.repositories.implementations.in_memory.audit_repository import InMemoryAuditRepository
from app.repositories.implementations.in_memory.document_chunk_repository import InMemoryDocumentChunkRepository
from app.repositories.implementations.in_memory.document_import_repository import InMemoryDocumentImportRepository
from app.repositories.implementations.in_memory.event_repository import InMemoryEventRepository
from app.repositories.implementations.in_memory.upload_session_repository import InMemoryUploadSessionRepository
from app.repositories.interfaces.approval_repository import ApprovalRepository
from app.repositories.interfaces.audit_repository import AuditRepository
from app.repositories.interfaces.document_chunk_repository import DocumentChunkRepository
from app.repositories.interfaces.document_import_repository import DocumentImportRepository
from app.repositories.interfaces.event_repository import EventRepository
from app.repositories.interfaces.upload_session_repository import UploadSessionRepository
from app.repositories.interfaces.document_repository import DocumentRepository
from app.repositories.interfaces.report_repository import ReportRepository
from app.repositories.interfaces.task_repository import TaskRepository
from app.services.task_service import TaskService


class RepositoryBoundaryTest(unittest.TestCase):
    """保护 Service 依赖接口、组合根选择实现的架构边界。"""

    def test_in_memory_repositories_implement_protocols(self) -> None:
        self.assertIsInstance(InMemoryTaskRepository(), TaskRepository)
        self.assertIsInstance(InMemoryReportRepository(), ReportRepository)
        self.assertIsInstance(InMemoryDocumentRepository(), DocumentRepository)
        self.assertIsInstance(InMemoryApprovalRepository(), ApprovalRepository)
        self.assertIsInstance(InMemoryAuditRepository(), AuditRepository)
        self.assertIsInstance(InMemoryDocumentChunkRepository(), DocumentChunkRepository)
        self.assertIsInstance(InMemoryDocumentImportRepository(), DocumentImportRepository)
        self.assertIsInstance(InMemoryEventRepository(), EventRepository)
        self.assertIsInstance(InMemoryUploadSessionRepository(), UploadSessionRepository)

    def test_task_service_does_not_import_repository_implementation(self) -> None:
        source = inspect.getsource(inspect.getmodule(TaskService))
        self.assertNotIn("repositories.implementations", source)
        self.assertIn("repositories.interfaces.task_repository", source)
        self.assertIn("repositories.interfaces.report_repository", source)


if __name__ == "__main__":
    unittest.main()
