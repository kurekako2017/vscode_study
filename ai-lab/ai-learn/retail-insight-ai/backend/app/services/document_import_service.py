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

    def __init__(self, repository: DocumentRepository, event_publisher: EventPublisher) -> None:
        """保存仓储与事件发布器，并初始化导入会话缓存。"""

        self._repository = repository
        self._event_publisher = event_publisher
        self._lock = RLock()
        self._imports_by_id: dict[str, DocumentImportRecord] = {}
        self._imports_by_document_id: dict[str, DocumentImportRecord] = {}

    def import_document(self, document_id: str) -> DocumentImportResponse:
        """执行同步导入：校验、验证、状态更新和事件发布。"""

        with self._lock:
            existing = self._imports_by_document_id.get(document_id)
            if existing is not None:
                if existing.status in {DocumentImportStatus.PENDING, DocumentImportStatus.RUNNING}:
                    raise DocumentImportAlreadyRunningException(document_id)
                return DocumentImportResponse.from_domain(existing)

            record = DocumentImportRecord(import_id=f"imp-{uuid4().hex}", document_id=document_id)
            self._imports_by_id[record.import_id] = record
            self._imports_by_document_id[document_id] = record
            record.mark_running()

        self._publish(record, "document.import.started", "Document import started")

        try:
            document = self._load_document(document_id)
            self._validate_document_state(document)
            self._validate_document_type(document)

            self._publish(record, "document.import.validated", "Document import validated")
            document.transition_status(DocumentStatus.VALIDATED)
            self._repository.update(document)

            with self._lock:
                record.mark_completed()

            self._publish(record, "document.import.completed", "Document import completed")
            return DocumentImportResponse.from_domain(record)
        except AppException as exc:
            with self._lock:
                record.mark_failed(exc.error_code.value, exc.message)
            self._publish(record, "document.import.failed", "Document import failed", error_code=exc.error_code.value)
            raise
        except Exception as exc:  # noqa: BLE001
            with self._lock:
                record.mark_failed(ErrorCode.REPOSITORY_ERROR.value, "Repository operation failed")
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

        with self._lock:
            record = self._imports_by_id.get(import_id)
            if record is None:
                raise DocumentImportNotFoundException(import_id)
            return DocumentImportResponse.from_domain(record)

    def _load_document(self, document_id: str) -> Document:
        """从仓储读取文档，不存在时映射为稳定 404。"""

        document = self._repository.get(document_id)
        if document is None:
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
