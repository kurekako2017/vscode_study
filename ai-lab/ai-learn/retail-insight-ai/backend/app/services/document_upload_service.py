"""文档上传 MVP 的业务服务。

文件职责：
- 执行 POST /api/v1/documents 的同步上传流程。
- 负责文件校验、元数据校验、checksum、幂等与重复检测。
- 把上传事件写入现有 EventRepository，方便未来扩展 SSE / 审计。

谁会调用它：
- `backend/app/api/documents.py` 路由通过依赖注入调用它。

它调用谁：
- `DocumentRepository` 保存或查询文档事实。
- `EventPublisher` 记录上传事件。
- `DocumentMetadata` / `Document` 保护领域约束。

输入是什么：
- 文件名、文件内容、MIME 类型、multipart metadata JSON、Idempotency-Key。

输出是什么：
- `DocumentUploadSessionResponse`，或者抛出冻结的应用异常。

为什么需要这一层：
- 路由只负责接收 HTTP；真正的文件校验、幂等和重复检测放在 service 层更容易测试。

日本现场面试怎么讲：
- 这是文档上传的应用服务层，未来如果接入 PostgreSQL、对象存储或异步队列，只需要替换仓储和发布实现，不改 API 契约。
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from threading import RLock
from typing import Any
from uuid import uuid4

from app.errors.base import AppException
from app.errors.error_codes import ErrorCode
from app.errors.exceptions import ValidationAppException
from app.events.publisher import EventPublisher
from app.models.document import (
    Document,
    DocumentMetadata,
    DocumentStatus,
    DocumentType,
    Language,
)
from app.observability.logging import get_logger, get_request_id, log_event
from app.core.learning_trace import trace_step
from app.repositories.interfaces.document_repository import DocumentRepository
from app.repositories.interfaces.upload_session_repository import UploadSessionRepository
from app.repositories.interfaces.unit_of_work import UnitOfWork
from app.repositories.implementations.in_memory.upload_session_repository import InMemoryUploadSessionRepository
from app.db.unit_of_work import InMemoryUnitOfWork
from app.models.upload import UploadSessionRecord
from app.schemas.document_api import DocumentUploadSessionResponse, UploadSessionStatus
from app.models.task import utc_now

logger = get_logger(__name__)

_MAX_FILE_SIZE_BYTES = 20 * 1024 * 1024

_EXTENSION_TO_DOCUMENT_TYPE: dict[str, DocumentType] = {
    ".md": DocumentType.MARKDOWN,
    ".txt": DocumentType.TEXT,
    ".pdf": DocumentType.PDF,
    ".docx": DocumentType.WORD,
    ".xlsx": DocumentType.EXCEL,
    ".csv": DocumentType.CSV,
    ".json": DocumentType.JSON,
}

_DOCUMENT_TYPE_MIME_TYPES: dict[DocumentType, set[str]] = {
    DocumentType.MARKDOWN: {"text/markdown", "text/plain", "text/x-markdown"},
    DocumentType.TEXT: {"text/plain"},
    DocumentType.PDF: {"application/pdf"},
    DocumentType.WORD: {
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    },
    DocumentType.EXCEL: {
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    },
    DocumentType.CSV: {"text/csv", "application/csv"},
    DocumentType.JSON: {"application/json", "text/json"},
}

_TEXTUAL_DOCUMENT_TYPES = {
    DocumentType.MARKDOWN,
    DocumentType.TEXT,
    DocumentType.CSV,
    DocumentType.JSON,
}


class DocumentUploadService:
    """同步处理文档上传、重复检测和事件发布。"""

    def __init__(
        self,
        repository: DocumentRepository,
        event_publisher: EventPublisher,
        upload_session_repository: UploadSessionRepository | None = None,
        unit_of_work: UnitOfWork | None = None,
    ) -> None:
        """注入文档、上传会话 Repository 与统一事务边界。"""

        self._repository = repository
        self._event_publisher = event_publisher
        self._lock = RLock()
        self._upload_session_repository = upload_session_repository or InMemoryUploadSessionRepository()
        self._unit_of_work = unit_of_work or InMemoryUnitOfWork()

    def upload_document(
        self,
        *,
        filename: str,
        content: bytes,
        content_type: str | None,
        metadata_json: str,
        idempotency_key: str | None = None,
    ) -> DocumentUploadSessionResponse:
        """让 Upload Session、Document 与成功事件在 PostgreSQL 中原子提交。"""

        with self._unit_of_work.transaction():
            return self._upload_document(
                filename=filename,
                content=content,
                content_type=content_type,
                metadata_json=metadata_json,
                idempotency_key=idempotency_key,
            )

    def _upload_document(
        self,
        *,
        filename: str,
        content: bytes,
        content_type: str | None,
        metadata_json: str,
        idempotency_key: str | None = None,
    ) -> DocumentUploadSessionResponse:
        """执行同步上传，并在成功时返回完成态的上传会话。"""

        upload_id = f"upl-{uuid4().hex}"
        document_id = f"doc-{uuid4().hex}"
        accepted_at = utc_now()
        normalized_content_type = (content_type or "").split(";", 1)[0].strip().lower()

        # 记录进入上传业务方法，说明 Router 已把文件交给 Service。
        trace_step(
            "POST",
            "/api/v1/documents",
            "Service",
            "DocumentUploadService.upload_document()",
            class_name="DocumentUploadService",
            method_name="upload_document",
            file_path="backend/app/services/document_upload_service.py",
            document_id=document_id,
            status=UploadSessionStatus.ACCEPTED.value,
            label="DocumentUploadService.upload_document()",
        )

        self._publish(
            upload_id,
            "document.upload.accepted",
            "Upload request accepted",
            status=UploadSessionStatus.ACCEPTED.value,
            document_id=document_id,
            extra={"filename": filename},
        )
        self._publish(
            upload_id,
            "document.upload.started",
            "Upload validation started",
            status=UploadSessionStatus.ACCEPTED.value,
            document_id=document_id,
            extra={"filename": filename},
        )
        self._publish(
            upload_id,
            "document.upload.validating",
            "File and metadata validation started",
            status=UploadSessionStatus.VALIDATING.value,
            document_id=document_id,
            extra={"filename": filename},
        )

        # 将 metadata 与文件规则分开记录，便于初学者理解校验发生的位置。
        trace_step(
            "POST",
            "/api/v1/documents",
            "Validation",
            "DocumentUploadService._parse_metadata()",
            class_name="DocumentUploadService",
            method_name="_parse_metadata",
            file_path="backend/app/services/document_upload_service.py",
            document_id=document_id,
            status=UploadSessionStatus.VALIDATING.value,
            label="metadata/file validation",
        )
        # 解析 metadata JSON，提取 title、owner、description、tags、language、document_type、checksum。
        metadata_payload = self._parse_metadata(metadata_json)
        title = self._require_title(metadata_payload)
        owner = self._require_owner(metadata_payload)
        description = self._coerce_optional_text(metadata_payload.get("description"))
        tags = self._normalize_tags(metadata_payload.get("tags"))
        language = self._coerce_language(metadata_payload.get("language", Language.UNKNOWN))
        provided_checksum = self._coerce_optional_text(metadata_payload.get("checksum"))
        requested_type = self._coerce_optional_document_type(metadata_payload.get("document_type"))

        if not content:
            self._fail_upload(
                upload_id,
                document_id,
                ErrorCode.EMPTY_FILE,
                "File cannot be empty.",
                status=UploadSessionStatus.FAILED.value,
                extra={"filename": filename},
            )

        if len(content) > _MAX_FILE_SIZE_BYTES:
            self._fail_upload(
                upload_id,
                document_id,
                ErrorCode.UPLOAD_TOO_LARGE,
                "File exceeds the allowed size.",
                status=UploadSessionStatus.FAILED.value,
                extra={"filename": filename},
            )

        document_type = self._infer_document_type(filename)
        if requested_type is not None and requested_type is not document_type:
            self._fail_upload(
                upload_id,
                document_id,
                ErrorCode.INVALID_METADATA,
                "Metadata document_type does not match the uploaded file.",
                status=UploadSessionStatus.FAILED.value,
                extra={"filename": filename, "document_type": requested_type.value},
            )

        if not self._mime_matches(document_type, normalized_content_type):
            self._fail_upload(
                upload_id,
                document_id,
                ErrorCode.UNSUPPORTED_DOCUMENT_TYPE,
                "Uploaded MIME type is not supported.",
                status=UploadSessionStatus.FAILED.value,
                extra={"filename": filename, "document_type": document_type.value},
            )

        checksum = f"sha256:{hashlib.sha256(content).hexdigest()}"
        if provided_checksum is not None and provided_checksum != checksum:
            self._fail_upload(
                upload_id,
                document_id,
                ErrorCode.INVALID_METADATA,
                "Provided checksum does not match the file content.",
                status=UploadSessionStatus.FAILED.value,
                extra={"filename": filename},
            )

        self._publish(
            upload_id,
            "document.upload.validated",
            "File and metadata validation passed",
            status="validated",
            document_id=document_id,
            extra={"filename": filename, "document_type": document_type.value},
        )

        # 单独记录 checksum 查询，避免把重复判断误认为新文档保存。
        trace_step(
            "POST",
            "/api/v1/documents",
            "Upload",
            "DocumentUploadService._lookup_cached_result()",
            class_name="DocumentUploadService",
            method_name="_lookup_cached_result",
            file_path="backend/app/services/document_upload_service.py",
            document_id=document_id,
            status="checking",
            label="checksum duplicate check",
        )
        cached_response = self._lookup_cached_result(idempotency_key, checksum)
        if cached_response is not None:
            self._cache_result(idempotency_key, checksum, cached_response)
            # 重复文件只返回已有结果，因此这里不能打印新文档保存节点。
            trace_step(
                "POST",
                "/api/v1/documents",
                "Upload",
                "Existing document result returned",
                class_name="DocumentUploadService",
                method_name="upload_document",
                file_path="backend/app/services/document_upload_service.py",
                document_id=cached_response.document_id,
                status=UploadSessionStatus.COMPLETED.value,
                label="Existing document returned",
            )
            self._publish(
                upload_id,
                "document.upload.duplicate_detected",
                "Duplicate checksum matched an existing document",
                status=UploadSessionStatus.COMPLETED.value,
                document_id=cached_response.document_id,
                extra={"filename": filename, "checksum": checksum},
            )
            self._publish(
                upload_id,
                "document.upload.completed",
                "Existing document result returned",
                status=UploadSessionStatus.COMPLETED.value,
                document_id=cached_response.document_id,
                extra={"filename": filename, "checksum": checksum},
            )
            return cached_response

        metadata = self._build_metadata(
            document_id=document_id,
            title=title,
            description=description,
            owner=owner,
            tags=tags,
            language=language,
            document_type=document_type,
            checksum=checksum,
            upload_id=upload_id,
            filename=filename,
            metadata_payload=metadata_payload,
        )

        content_text = self._build_document_content(content, document_type, filename)
        document = Document.create(content_text, metadata)

        self._publish(
            upload_id,
            "document.upload.storing",
            "Document repository save started",
            status=UploadSessionStatus.STORING.value,
            document_id=document_id,
            extra={"filename": filename, "checksum": checksum},
        )

        try:
            # 记录真正执行的新文档保存调用，节点必须对应实际 Repository 方法。
            trace_step(
                "POST",
                "/api/v1/documents",
                "Repository",
                "InMemoryDocumentRepository.create()",
                class_name=self._repository.__class__.__name__,
                method_name="create",
                file_path="backend/app/repositories/implementations/in_memory/document_repository.py",
                document_id=document_id,
                status=UploadSessionStatus.STORING.value,
                label="InMemoryDocumentRepository.create()",
            )
            self._repository.create(document)
        except ValidationAppException as exc:
            detail = exc.detail or {}
            if detail.get("field") == "checksum":
                # 竞争条件下再次查询真实仓库，单独记录该重复分支节点。
                trace_step(
                    "POST",
                    "/api/v1/documents",
                    "Repository",
                    "InMemoryDocumentRepository.find_by_checksum()",
                    class_name=self._repository.__class__.__name__,
                    method_name="find_by_checksum",
                    file_path="backend/app/repositories/implementations/in_memory/document_repository.py",
                    document_id=document_id,
                    status="duplicate_check",
                    label="InMemoryDocumentRepository.find_by_checksum()",
                )
                existing = self._repository.find_by_checksum(checksum)
                if existing is not None:
                    response = self._build_response(upload_id, existing.document_id, accepted_at)
                    self._cache_result(idempotency_key, checksum, response)
                    # 重复文件没有完成保存，Learning Trace 只显示已有文档读取结果。
                    trace_step(
                        "POST",
                        "/api/v1/documents",
                        "Upload",
                        "Existing document result returned",
                        class_name="DocumentUploadService",
                        method_name="upload_document",
                        file_path="backend/app/services/document_upload_service.py",
                        document_id=existing.document_id,
                        status=UploadSessionStatus.COMPLETED.value,
                        label="Existing document returned",
                    )
                    self._publish(
                        upload_id,
                        "document.upload.duplicate_detected",
                        "Duplicate checksum matched an existing document",
                        status=UploadSessionStatus.COMPLETED.value,
                        document_id=existing.document_id,
                        extra={"filename": filename, "checksum": checksum},
                    )
                    self._publish(
                        upload_id,
                        "document.upload.completed",
                        "Existing document result returned",
                        status=UploadSessionStatus.COMPLETED.value,
                        document_id=existing.document_id,
                        extra={"filename": filename, "checksum": checksum},
                    )
                    return response
            self._fail_upload(
                upload_id,
                document_id,
                ErrorCode.REPOSITORY_ERROR,
                "Repository write failed.",
                status=UploadSessionStatus.FAILED.value,
                extra={"filename": filename},
            )

        response = self._build_response(upload_id, document_id, accepted_at)
        self._cache_result(idempotency_key, checksum, response)

        self._publish(
            upload_id,
            "document.version.created",
            "Frozen document version created",
            status=UploadSessionStatus.COMPLETED.value,
            document_id=document_id,
            extra={"filename": filename, "checksum": checksum},
        )
        self._publish(
            upload_id,
            "document.upload.completed",
            "Document upload completed",
            status=UploadSessionStatus.COMPLETED.value,
            document_id=document_id,
            extra={"filename": filename, "checksum": checksum},
        )
        return response
    # ---------------------------- 辅助方法 ----------------------------
    def _parse_metadata(self, metadata_json: str) -> dict[str, Any]:
        """把 multipart metadata JSON 转成字典。"""

        try:
            payload = json.loads(metadata_json)             # 
        except json.JSONDecodeError as exc:
            self._raise_upload_error(
                ErrorCode.INVALID_METADATA,
                "Metadata payload is not valid JSON.",
                detail={"reason": "invalid json"},
                status_code=422,
                cause=exc,
            )
        if not isinstance(payload, dict):
            self._raise_upload_error(
                ErrorCode.INVALID_METADATA,
                "Metadata payload must be a JSON object.",
                detail={"reason": "metadata must be an object"},
                status_code=422,
            )
        return payload

    def _require_title(self, metadata: dict[str, Any]) -> str:
        title = self._coerce_optional_text(metadata.get("title"))
        if title is None:
            self._raise_upload_error(
                ErrorCode.MISSING_TITLE,
                "Title is required.",
                detail={"field": "title"},
                status_code=422,
            )
        return title

    def _require_owner(self, metadata: dict[str, Any]) -> str:
        owner = self._coerce_optional_text(metadata.get("owner"))
        if owner is None:
            self._raise_upload_error(
                ErrorCode.INVALID_METADATA,
                "Owner is required.",
                detail={"field": "owner"},
                status_code=422,
            )
        return owner

    def _coerce_optional_text(self, value: Any) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str):
            return None
        value = value.strip()
        return value or None

    def _normalize_tags(self, value: Any) -> tuple[str, ...]:
        if value is None:
            return ()
        if not isinstance(value, list):
            self._raise_upload_error(
                ErrorCode.INVALID_METADATA,
                "Tags must be a list of strings.",
                detail={"field": "tags"},
                status_code=422,
            )
        tags: list[str] = []
        for tag in value:
            if not isinstance(tag, str) or not tag.strip():
                self._raise_upload_error(
                    ErrorCode.INVALID_METADATA,
                    "Each tag must be a non-empty string.",
                    detail={"field": "tags"},
                    status_code=422,
                )
            tags.append(tag.strip())
        return tuple(tags)

    def _coerce_language(self, value: Any) -> Language:
        try:
            return Language(str(value))
        except ValueError as exc:
            self._raise_upload_error(
                ErrorCode.INVALID_METADATA,
                "Unsupported language.",
                detail={"field": "language"},
                status_code=422,
                cause=exc,
            )

    def _coerce_optional_document_type(self, value: Any) -> DocumentType | None:
        if value is None:
            return None
        try:
            return DocumentType(str(value))
        except ValueError:
            self._raise_upload_error(
                ErrorCode.INVALID_METADATA,
                "Unsupported requested document type.",
                detail={"field": "document_type"},
                status_code=422,
            )

    def _infer_document_type(self, filename: str) -> DocumentType:
        suffix = Path(filename).suffix.lower()
        document_type = _EXTENSION_TO_DOCUMENT_TYPE.get(suffix)
        if document_type is None:
            self._raise_upload_error(
                ErrorCode.UNSUPPORTED_DOCUMENT_TYPE,
                "Unsupported document extension.",
                detail={"filename": filename, "suffix": suffix},
                status_code=415,
            )
        return document_type

    def _mime_matches(self, document_type: DocumentType, content_type: str) -> bool:
        allowed = _DOCUMENT_TYPE_MIME_TYPES.get(document_type, set())
        return content_type in allowed

    def _build_document_content(
        self,
        content: bytes,
        document_type: DocumentType,
        filename: str,
    ) -> str:
        if document_type in _TEXTUAL_DOCUMENT_TYPES:
            try:
                return content.decode("utf-8")
            except UnicodeDecodeError as exc:
                self._raise_upload_error(
                    ErrorCode.UNSUPPORTED_ENCODING,
                    "File encoding is not supported.",
                    detail={"filename": filename},
                    status_code=422,
                    cause=exc,
                )
        return f"[binary {document_type.value} upload placeholder: {filename}]"
    # 把上传结果整理成接口响应
    def _build_metadata(
        self,
        *,
        document_id: str,
        title: str,
        description: str | None,
        owner: str,
        tags: tuple[str, ...],
        language: Language,
        document_type: DocumentType,
        checksum: str,
        upload_id: str,
        filename: str,
        metadata_payload: dict[str, Any],
    ) -> DocumentMetadata:
        source = metadata_payload.get("source")
        if isinstance(source, dict):
            source_uri = source.get("uri") or source.get("source_uri") or f"upload://{upload_id}/{filename}"
            source_type = source.get("source_type") or "upload_form"
            source_label = source.get("label")
            source_external_id = source.get("external_id")
            source_mapping: dict[str, Any] = {
                "source_type": source_type,
                "uri": source_uri,
            }
            if source_label is not None:
                source_mapping["label"] = source_label
            if source_external_id is not None:
                source_mapping["external_id"] = source_external_id
        else:
            source_mapping = {
                "source_type": "upload_form",
                "uri": f"upload://{upload_id}/{filename}",
                "label": filename,
            }

        try:
            return DocumentMetadata.from_mapping(
                {
                    "document_id": document_id,
                    "title": title,
                    "description": description,
                    "owner": owner,
                    "version": 1,
                    "language": language,
                    "document_type": document_type,
                    "status": DocumentStatus.UPLOADED,
                    "tags": tags,
                    "source": source_mapping,
                    "checksum": checksum,
                }
            )
        except AppException as exc:
            if exc.error_code is ErrorCode.MISSING_TITLE:
                raise
            self._raise_upload_error(
                ErrorCode.INVALID_METADATA,
                "Metadata payload is invalid.",
                detail=exc.detail or {"reason": "metadata validation failed"},
                status_code=422,
                cause=exc,
            )

    def _build_response(
        self,
        upload_id: str,
        document_id: str,
        timestamp: datetime,
    ) -> DocumentUploadSessionResponse:
        return DocumentUploadSessionResponse(
            upload_id=upload_id,
            document_id=document_id,
            status=UploadSessionStatus.COMPLETED,
            progress=100,
            created_at=timestamp,
            updated_at=timestamp,
            error_code=None,
            error_message=None,
        )

    def _lookup_cached_result(
        self,
        idempotency_key: str | None,
        checksum: str,
    ) -> DocumentUploadSessionResponse | None:
        with self._lock:
            if idempotency_key is not None:
                cached = self._upload_session_repository.get_by_idempotency_key(idempotency_key)
                if cached is not None:
                    if cached.checksum != checksum:
                        self._raise_upload_error(
                            ErrorCode.IDEMPOTENCY_CONFLICT,
                            "Same idempotency key was reused with a different file.",
                            detail={"idempotency_key": idempotency_key},
                            status_code=409,
                        )
                    return self._session_to_response(cached)
            cached = self._upload_session_repository.get_by_checksum(checksum)
            return self._session_to_response(cached) if cached is not None else None

    def _cache_result(
        self,
        idempotency_key: str | None,
        checksum: str,
        response: DocumentUploadSessionResponse,
    ) -> None:
        with self._lock:
            self._upload_session_repository.save(
                UploadSessionRecord(
                    upload_id=response.upload_id,
                    document_id=response.document_id,
                    checksum=checksum,
                    idempotency_key=idempotency_key,
                    status=response.status.value,
                    progress=response.progress,
                    created_at=response.created_at,
                    updated_at=response.updated_at,
                    error_code=response.error_code,
                    error_message=response.error_message,
                )
            )

    def _session_to_response(self, record: UploadSessionRecord) -> DocumentUploadSessionResponse:
        """把跨进程上传会话恢复为原有 API 响应，不改变字段。"""

        return DocumentUploadSessionResponse(
            upload_id=record.upload_id,
            document_id=record.document_id,
            status=UploadSessionStatus(record.status),
            progress=record.progress,
            created_at=record.created_at,
            updated_at=record.updated_at,
            error_code=record.error_code,
            error_message=record.error_message,
        )

    def _publish(
        self,
        upload_id: str,
        event_type: str,
        message: str,
        *,
        status: str,
        document_id: str,
        extra: dict[str, Any] | None = None,
    ) -> None:
        payload = {
            "upload_id": upload_id,
            "document_id": document_id,
            "request_id": get_request_id(),
            "trace_id": get_request_id(),
            "status": status,
        }
        if extra:
            payload.update(extra)
        event = self._event_publisher.publish(upload_id, event_type, message, payload)
        log_event(
            logger,
            "info",
            event_type,
            message,
            request_id=get_request_id(),
            task_id=upload_id,
            status=status,
            node="document_upload",
            sequence=event.sequence,
        )

    def _fail_upload(
        self,
        upload_id: str,
        document_id: str,
        error_code: ErrorCode,
        message: str,
        *,
        status: str,
        detail: dict[str, Any] | None = None,
        extra: dict[str, Any] | None = None,
        cause: Exception | None = None,
    ) -> None:
        self._publish(
            upload_id,
            "document.validation.failed",
            message,
            status=status,
            document_id=document_id,
            extra=extra,
        )
        self._publish(
            upload_id,
            "document.upload.failed",
            message,
            status=UploadSessionStatus.FAILED.value,
            document_id=document_id,
            extra=extra,
        )
        self._raise_upload_error(error_code, message, detail=detail or {}, status_code=self._status_code_for_error(error_code), cause=cause)

    def _status_code_for_error(self, error_code: ErrorCode) -> int:
        if error_code is ErrorCode.IDEMPOTENCY_CONFLICT:
            return 409
        if error_code is ErrorCode.UPLOAD_TOO_LARGE:
            return 413
        if error_code is ErrorCode.UNSUPPORTED_DOCUMENT_TYPE:
            return 415
        if error_code in {ErrorCode.EMPTY_FILE, ErrorCode.MISSING_TITLE, ErrorCode.INVALID_METADATA, ErrorCode.UNSUPPORTED_ENCODING}:
            return 422
        if error_code is ErrorCode.DUPLICATE_CHECKSUM:
            return 409
        if error_code is ErrorCode.REPOSITORY_ERROR:
            return 500
        return 500

    def _raise_upload_error(
        self,
        error_code: ErrorCode,
        message: str,
        *,
        detail: dict[str, Any] | None = None,
        status_code: int,
        cause: Exception | None = None,
    ) -> None:
        raise AppException(error_code, message, status_code, detail=detail) from cause


__all__ = ["DocumentUploadService"]
