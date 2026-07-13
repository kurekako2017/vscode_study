"""文档导入服务。

文件职责：
- 提供 POST /api/v1/documents/{document_id}/import 的同步 MVP。
- 负责导入前校验、状态推进、事件发布与最终结果缓存。

谁会调用它：
- `backend/app/api/document_imports.py` 路由通过依赖注入调用它。

它调用谁：
- `DocumentRepository` 读取并更新文档事实。
- `EventPublisher` 记录导入事件。
- `DocumentImportRecord` 维护导入会话状态。

输入是什么：
- `document_id`。

输出是什么：
- `DocumentImportResponse`，或者抛出稳定的应用异常。

为什么需要这一层：
- 导入是文档域的独立流水线，不能混在上传、读取或归档 service 里。

日本现场面试怎么讲：
- 这是文档导入的应用服务层，先做最小同步 MVP，未来可以切换成异步批处理或队列消费者。
"""

from __future__ import annotations

from threading import RLock
from uuid import uuid4

from app.core.learning_trace import trace_step
from app.errors.base import AppException
from app.errors.error_codes import ErrorCode
from app.errors.exceptions import (
    DocumentArchivedException,
    DocumentImportAlreadyRunningException,
    DocumentImportNotFoundException,
    DocumentNotFoundException,
)
from app.events.publisher import EventPublisher
from app.models.document import Document, DocumentStatus, DocumentType
from app.models.document_import import DocumentImportRecord, DocumentImportStatus
from app.observability.logging import get_logger, get_request_id, log_event
from app.repositories.interfaces.document_repository import DocumentRepository
from app.repositories.interfaces.document_import_repository import DocumentImportRepository
from app.repositories.implementations.in_memory.document_import_repository import InMemoryDocumentImportRepository
from app.schemas.document_import_api import DocumentImportResponse

logger = get_logger(__name__)

_SUPPORTED_IMPORT_TYPES = {
    DocumentType.MARKDOWN,
    DocumentType.TEXT,
    DocumentType.CSV,
    DocumentType.JSON,
}


class DocumentImportService:
    """封装文档导入会话、状态推进和导入结果缓存。"""

    def __init__(
        self,
        repository: DocumentRepository,
        event_publisher: EventPublisher,
        import_repository: DocumentImportRepository | None = None,
    ) -> None:
        """保存文档仓储、事件发布器和可切换的导入会话仓储。"""

        self._repository = repository
        self._event_publisher = event_publisher
        self._lock = RLock()
        self._import_repository = import_repository or InMemoryDocumentImportRepository()

    def import_document(self, document_id: str) -> DocumentImportResponse:
        """执行同步导入：校验、验证、状态更新和事件发布。"""

        # 记录进入导入 Service，区分 Router 接收请求和导入业务流程。
        trace_step(
            "POST",
            f"/api/v1/documents/{document_id}/import",
            "Service",
            "DocumentImportService.import_document()",
            class_name="DocumentImportService",
            method_name="import_document",
            file_path="backend/app/services/document_import_service.py",
            document_id=document_id,
            label="DocumentImportService.import_document()",
        )
        with self._lock:
            existing = self._import_repository.get_by_document_id(document_id)
            if existing is not None:
                if existing.status in {DocumentImportStatus.PENDING, DocumentImportStatus.RUNNING}:
                    raise DocumentImportAlreadyRunningException(document_id)
                return DocumentImportResponse.from_domain(existing)

            # 先确认文档存在，避免 PostgreSQL 外键错误覆盖稳定的 document_not_found API。
            document = self._load_document(document_id)
            record = DocumentImportRecord(import_id=f"imp-{uuid4().hex}", document_id=document_id)
            record.mark_running()
            self._import_repository.save(record)

        self._publish(record, "document.import.started", "Document import started")

        try:
            self._validate_document_state(document)
            self._validate_document_type(document)

            self._publish(record, "document.import.validated", "Document import validated")
            document.transition_status(DocumentStatus.VALIDATED)
            # 记录导入状态写回仓库的步骤，帮助初学者理解状态如何持久化。
            trace_step(
                "POST",
                f"/api/v1/documents/{document_id}/import",
                "Repository",
                "InMemoryDocumentRepository.update()",
                class_name=self._repository.__class__.__name__,
                method_name="update",
                file_path=(
                    "backend/app/repositories/implementations/"
                    "in_memory/document_repository.py"
                ),
                document_id=document_id,
                label="InMemoryDocumentRepository.update()",
            )
            self._repository.update(document)

            with self._lock:
                record.mark_completed()
                self._import_repository.save(record)

            self._publish(record, "document.import.completed", "Document import completed")
            # 记录真实导入状态，帮助初学者确认状态推进已完成。
            trace_step(
                "POST",
                f"/api/v1/documents/{document_id}/import",
                "Result",
                f"Import result: {document.status.value}",
                document_id=document_id,
                status="201",
                label=f"Import result: {document.status.value}",
            )
            # 只记录真实标题，避免输出正文、checksum 或敏感 metadata。
            trace_step(
                "POST",
                f"/api/v1/documents/{document_id}/import",
                "Result",
                f"Document: {document.metadata.title}",
                document_id=document_id,
                status="201",
                label=f"Document: {document.metadata.title}",
            )
            return DocumentImportResponse.from_domain(record)
        except AppException as exc:
            with self._lock:
                record.mark_failed(exc.error_code.value, exc.message)
                self._import_repository.save(record)
            self._publish(record, "document.import.failed", "Document import failed", error_code=exc.error_code.value)
            raise
        except Exception as exc:  # noqa: BLE001
            with self._lock:
                record.mark_failed(ErrorCode.REPOSITORY_ERROR.value, "Repository operation failed")
                self._import_repository.save(record)
            self._publish(record, "document.import.failed", "Document import failed", error_code=ErrorCode.REPOSITORY_ERROR.value)
            raise AppException(
                ErrorCode.REPOSITORY_ERROR,
                "Repository operation failed",
                500,
                detail={"document_id": document_id},
                task_id=document_id,
            ) from exc

    def get_import(self, import_id: str) -> DocumentImportResponse:
        """按 import_id 读取导入记录。"""

        # 记录进入导入记录查询 Service，说明下一步读取本地导入会话缓存。
        trace_step(
            "GET",
            f"/api/v1/document-imports/{import_id}",
            "Service",
            "DocumentImportService.get_import()",
            class_name="DocumentImportService",
            method_name="get_import",
            file_path="backend/app/services/document_import_service.py",
            label="DocumentImportService.get_import()",
        )
        with self._lock:
            record = self._import_repository.get(import_id)
            if record is None:
                # 单独记录未命中，帮助初学者区分查询完成和业务 404。
                trace_step(
                    "GET",
                    f"/api/v1/document-imports/{import_id}",
                    "Result",
                    "Import not found",
                    status="404",
                    label="Import not found",
                )
                raise DocumentImportNotFoundException(import_id)
            # 记录真实导入状态和 ID，不输出正文或敏感 metadata。
            trace_step(
                "GET",
                f"/api/v1/document-imports/{import_id}",
                "Result",
                f"Import status: {record.status.value}",
                status="200",
                label=f"Import status: {record.status.value}",
            )
            trace_step(
                "GET",
                f"/api/v1/document-imports/{import_id}",
                "Result",
                f"Import ID: {record.import_id}",
                status="200",
                label=f"Import ID: {record.import_id}",
            )
            return DocumentImportResponse.from_domain(record)

    def _load_document(self, document_id: str) -> Document:
        """从仓储读取文档，不存在时映射为稳定 404。"""

        # 记录导入前读取目标文档的 Repository 步骤，404 也保留完整链路。
        trace_step(
            "POST",
            f"/api/v1/documents/{document_id}/import",
            "Repository",
            "InMemoryDocumentRepository.get()",
            class_name=self._repository.__class__.__name__,
            method_name="get",
            file_path=(
                "backend/app/repositories/implementations/"
                "in_memory/document_repository.py"
            ),
            document_id=document_id,
            label="InMemoryDocumentRepository.get()",
        )
        document = self._repository.get(document_id)
        if document is None:
            # 单独记录未命中，帮助初学者区分查询完成和业务 404。
            trace_step(
                "POST",
                f"/api/v1/documents/{document_id}/import",
                "Result",
                "Document not found",
                document_id=document_id,
                status="404",
                label="Document not found",
            )
            raise DocumentNotFoundException(document_id)
        return document

    def _validate_document_state(self, document: Document) -> None:
        """导入前校验文档状态。"""

        if document.status is DocumentStatus.ARCHIVED:
            raise DocumentArchivedException(document.document_id)
        if document.status not in {DocumentStatus.UPLOADED, DocumentStatus.VALIDATED}:
            raise AppException(
                ErrorCode.INVALID_METADATA,
                "Document is not in an importable state",
                422,
                detail={"document_id": document.document_id, "status": document.status.value},
                task_id=document.document_id,
            )

    def _validate_document_type(self, document: Document) -> None:
        """只允许当前阶段已冻结的轻量类型进入导入闭环。"""

        if document.metadata.document_type not in _SUPPORTED_IMPORT_TYPES:
            raise AppException(
                ErrorCode.UNSUPPORTED_DOCUMENT_TYPE,
                "Document type is not supported for import",
                415,
                detail={
                    "document_id": document.document_id,
                    "document_type": document.metadata.document_type.value,
                },
                task_id=document.document_id,
            )

    def _publish(self, record: DocumentImportRecord, event_type: str, message: str, *, error_code: str | None = None) -> None:
        """把导入状态变化写入统一事件仓库。"""

        payload = {
            "import_id": record.import_id,
            "document_id": record.document_id,
            "request_id": get_request_id(),
            "trace_id": get_request_id(),
            "status": record.status.value,
        }
        event = self._event_publisher.publish(record.import_id, event_type, message, payload)
        log_event(
            logger,
            "info",
            event_type,
            message,
            request_id=get_request_id(),
            task_id=record.import_id,
            status=record.status.value,
            node="document_import",
            error_code=error_code,
            sequence=event.sequence,
        )


__all__ = ["DocumentImportService"]
