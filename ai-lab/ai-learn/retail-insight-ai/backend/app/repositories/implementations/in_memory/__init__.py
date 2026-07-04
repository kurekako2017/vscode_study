"""适合单进程本地部署的 InMemory Repository 实现。"""

from app.repositories.implementations.in_memory.document_repository import InMemoryDocumentRepository
from app.repositories.implementations.in_memory.document_chunk_repository import InMemoryDocumentChunkRepository
from app.repositories.implementations.in_memory.audit_repository import InMemoryAuditRepository
from app.repositories.implementations.in_memory.approval_repository import InMemoryApprovalRepository
from app.repositories.implementations.in_memory.document_retrieval import InMemoryKeywordRetrieval
from app.repositories.implementations.in_memory.event_repository import InMemoryEventRepository
from app.repositories.implementations.in_memory.report_repository import InMemoryReportRepository
from app.repositories.implementations.in_memory.task_repository import InMemoryTaskRepository

__all__ = [
    "InMemoryDocumentChunkRepository",
    "InMemoryAuditRepository",
    "InMemoryApprovalRepository",
    "InMemoryKeywordRetrieval",
    "InMemoryDocumentRepository",
    "InMemoryEventRepository",
    "InMemoryReportRepository",
    "InMemoryTaskRepository",
]
