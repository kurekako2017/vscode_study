"""文档 chunk 服务。

文件职责：
- 提供 POST /api/v1/documents/{document_id}/chunks 和 GET /api/v1/documents/{document_id}/chunks 的业务逻辑。
- 在 import 完成后的 validated 文档上生成稳定 chunk。
- 把 chunk 事件写入统一 EventRepository，便于未来 SSE / 审计扩展。

谁会调用它：
- `backend/app/api/document_chunks.py` 路由通过依赖注入调用它。

它调用谁：
- `DocumentRepository` 读取文档事实。
- `DocumentChunkRepository` 保存 chunk 结果。
- `EventPublisher` 记录 chunk 事件。

输入是什么：
- `document_id`。

输出是什么：
- `DocumentChunkListResponse`，或者抛出冻结的应用异常。

为什么需要这一层：
- chunk 是独立于 upload/import/read/archive 的第二阶段流水线，不能直接塞进路由。

日本现场面试怎么讲：
- 这是文档切片的应用服务层，先做最小可重复实现，后续可以平滑升级到异步队列、全文检索或 RAG。
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import replace
from threading import RLock

from app.core.learning_trace import trace_step
from app.errors.base import AppException
from app.errors.error_codes import ErrorCode
from app.errors.exceptions import DocumentArchivedException, DocumentNotFoundException, DocumentNotValidatedException
from app.events.publisher import EventPublisher
from app.embeddings.service import EmbeddingService
from app.models.document import Document, DocumentChunk, DocumentStatus, DocumentType
from app.observability.logging import get_logger, get_request_id, log_event
from app.repositories.interfaces.document_chunk_repository import DocumentChunkRepository
from app.repositories.interfaces.document_repository import DocumentRepository
from app.schemas.document_chunk_api import DocumentChunkListResponse

logger = get_logger(__name__)

_SUPPORTED_CHUNK_TYPES = {
    DocumentType.MARKDOWN,
    DocumentType.TEXT,
}
_MAX_CHUNK_SIZE = 800
_PARAGRAPH_SPLIT_RE = re.compile(r"\n\s*\n+")


class DocumentChunkService:
    """封装文档切片、重复写入和事件发布逻辑。"""

    def __init__(
        self,
        document_repository: DocumentRepository,
        chunk_repository: DocumentChunkRepository,
        event_publisher: EventPublisher,
        embedding_service: EmbeddingService | None = None,
    ) -> None:
        """保存仓储与事件发布器，并初始化进程内互斥锁。"""

        self._document_repository = document_repository
        self._chunk_repository = chunk_repository
        self._event_publisher = event_publisher
        self._embedding_service = embedding_service
        self._lock = RLock()

    def chunk_document(self, document_id: str) -> DocumentChunkListResponse:
        """对 validated 文档生成确定性的 chunk 列表，并替换旧结果。"""

        # 记录进入 chunk Service，下一步读取文档并执行切分流程。
        trace_step(
            "POST",
            f"/api/v1/documents/{document_id}/chunks",
            "Service",
            "DocumentChunkService.chunk_document()",
            class_name="DocumentChunkService",
            method_name="chunk_document",
            file_path="backend/app/services/document_chunk_service.py",
            document_id=document_id,
            label="DocumentChunkService.chunk_document()",
        )
        with self._lock:
            self._publish(
                document_id,
                "document.chunk.started",
                "Document chunk started",
                status="running",
            )

            document: Document | None = None
            try:
                document = self._load_document(
                    document_id,
                    http_method="POST",
                    http_path=f"/api/v1/documents/{document_id}/chunks",
                )
                self._validate_document_state(document)
                self._validate_document_type(document)

                chunks = self._build_chunks(document)
                # 记录 chunk 结果写入 Repository，下一步返回生成后的列表。
                trace_step(
                    "POST",
                    f"/api/v1/documents/{document_id}/chunks",
                    "Repository",
                    "InMemoryDocumentChunkRepository.replace_for_document()",
                    class_name=self._chunk_repository.__class__.__name__,
                    method_name="replace_for_document",
                    file_path=(
                        "backend/app/repositories/implementations/"
                        "in_memory/document_chunk_repository.py"
                    ),
                    document_id=document_id,
                    label="InMemoryDocumentChunkRepository.replace_for_document()",
                )
                self._chunk_repository.replace_for_document(document.document_id, document.version, chunks)
                response = DocumentChunkListResponse.from_domain(document, chunks)
                # 只记录数量和前 10 个 chunk 标识，不输出 chunk 正文。
                trace_step(
                    "POST",
                    f"/api/v1/documents/{document_id}/chunks",
                    "Result",
                    f"Chunks created: {len(response.items)}",
                    status="201",
                    label=f"Chunks created: {len(response.items)}",
                )
                for item in response.items[:10]:
                    trace_step(
                        "POST",
                        f"/api/v1/documents/{document_id}/chunks",
                        "Result",
                        f"Chunk: {item.chunk_id} (index {item.chunk_index})",
                        document_id=document_id,
                        label=f"Chunk: {item.chunk_id} (index {item.chunk_index})",
                    )
                if len(response.items) > 10:
                    trace_step(
                        "POST",
                        f"/api/v1/documents/{document_id}/chunks",
                        "Result",
                        f"... remaining: {len(response.items) - 10}",
                        document_id=document_id,
                        label=f"... remaining: {len(response.items) - 10}",
                    )
                self._publish(
                    document.document_id,
                    "document.chunk.completed",
                    "Document chunk completed",
                    status="completed",
                    version=document.version,
                    extra={"chunk_count": len(chunks), "document_type": document.metadata.document_type.value},
                )
                return response
            except AppException as exc:
                self._publish(
                    document_id,
                    "document.chunk.failed",
                    "Document chunk failed",
                    status="failed",
                    version=document.version if document is not None else None,
                    extra={"error_code": exc.error_code.value, "document_id": document_id},
                    error_code=exc.error_code.value,
                )
                raise
            except Exception as exc:  # noqa: BLE001
                self._publish(
                    document_id,
                    "document.chunk.failed",
                    "Document chunk failed",
                    status="failed",
                    version=document.version if document is not None else None,
                    extra={"error_code": ErrorCode.CHUNK_FAILED.value, "document_id": document_id},
                    error_code=ErrorCode.CHUNK_FAILED.value,
                )
                raise AppException(
                    ErrorCode.CHUNK_FAILED,
                    "Document chunk failed",
                    500,
                    detail={"document_id": document_id},
                    task_id=document_id,
                ) from exc

    def get_chunks(self, document_id: str) -> DocumentChunkListResponse:
        """按 document_id 读取当前版本的 chunk 列表。"""

        # 记录进入 chunk 查询 Service，下一步读取文档和 chunk Repository。
        trace_step(
            "GET",
            f"/api/v1/documents/{document_id}/chunks",
            "Service",
            "DocumentChunkService.get_chunks()",
            class_name="DocumentChunkService",
            method_name="get_chunks",
            file_path="backend/app/services/document_chunk_service.py",
            document_id=document_id,
            label="DocumentChunkService.get_chunks()",
        )
        document = self._load_document(
            document_id,
            http_method="GET",
            http_path=f"/api/v1/documents/{document_id}/chunks",
        )
        self._validate_document_state(document)
        self._validate_document_type(document)
        chunks = self._chunk_repository.list_for_document(document.document_id, document.version)
        response = DocumentChunkListResponse.from_domain(document, chunks)
        # 记录查询结果数量和最多 10 个非敏感 chunk 标识。
        trace_step(
            "GET",
            f"/api/v1/documents/{document_id}/chunks",
            "Repository",
            "InMemoryDocumentChunkRepository.list_for_document()",
            class_name=self._chunk_repository.__class__.__name__,
            method_name="list_for_document",
            file_path=(
                "backend/app/repositories/implementations/"
                "in_memory/document_chunk_repository.py"
            ),
            document_id=document_id,
            label="InMemoryDocumentChunkRepository.list_for_document()",
        )
        trace_step(
            "GET",
            f"/api/v1/documents/{document_id}/chunks",
            "Result",
            f"Chunks found: {len(response.items)}",
            status="200",
            label=f"Chunks found: {len(response.items)}",
        )
        for item in response.items[:10]:
            trace_step(
                "GET",
                f"/api/v1/documents/{document_id}/chunks",
                "Result",
                f"Chunk: {item.chunk_id} (index {item.chunk_index})",
                document_id=document_id,
                label=f"Chunk: {item.chunk_id} (index {item.chunk_index})",
            )
        if len(response.items) > 10:
            trace_step(
                "GET",
                f"/api/v1/documents/{document_id}/chunks",
                "Result",
                f"... remaining: {len(response.items) - 10}",
                document_id=document_id,
                label=f"... remaining: {len(response.items) - 10}",
            )
        return response

    def _load_document(self, document_id: str, *, http_method: str, http_path: str) -> Document:
        """从仓储读取文档，不存在时映射为稳定 404。"""

        # 记录文档 Repository 查询，404 分支也保留完整调用链。
        trace_step(
            http_method,
            http_path,
            "Repository",
            "InMemoryDocumentRepository.get()",
            class_name=self._document_repository.__class__.__name__,
            method_name="get",
            file_path="backend/app/repositories/implementations/in_memory/document_repository.py",
            document_id=document_id,
            label="InMemoryDocumentRepository.get()",
        )
        document = self._document_repository.get(document_id)
        if document is None:
            # 单独记录未命中，帮助初学者区分查询完成和业务 404。
            trace_step(
                http_method,
                http_path,
                "Result",
                "Document not found",
                document_id=document_id,
                status="404",
                label="Document not found",
            )
            raise DocumentNotFoundException(document_id)
        return document

    def _validate_document_state(self, document: Document) -> None:
        """chunk 前必须是 validated，归档文档直接拒绝。"""

        if document.status is DocumentStatus.ARCHIVED:
            raise DocumentArchivedException(document.document_id)
        if document.status is not DocumentStatus.VALIDATED:
            raise DocumentNotValidatedException(document.document_id)

    def _validate_document_type(self, document: Document) -> None:
        """当前只允许 markdown 与 text 进入 chunk pipeline。"""

        if document.metadata.document_type not in _SUPPORTED_CHUNK_TYPES:
            raise AppException(
                ErrorCode.UNSUPPORTED_DOCUMENT_TYPE,
                "Document type is not supported for chunking",
                415,
                detail={
                    "document_id": document.document_id,
                    "document_type": document.metadata.document_type.value,
                },
                task_id=document.document_id,
            )

    def _build_chunks(self, document: Document) -> list[DocumentChunk]:
        """先按段落切分，长段落再做固定长度 fallback，保持确定性。"""

        text = document.content.strip()
        paragraphs = [paragraph.strip() for paragraph in _PARAGRAPH_SPLIT_RE.split(text) if paragraph.strip()]
        if not paragraphs:
            paragraphs = [text]

        created_at = document.updated_at
        chunks: list[DocumentChunk] = []
        chunk_index = 0
        for paragraph in paragraphs:
            for slice_text in self._slice_paragraph(paragraph):
                chunk_id = self._chunk_id(document.document_id, document.version, chunk_index, slice_text)
                chunks.append(
                    DocumentChunk(
                        document_id=document.document_id,
                        version=document.version,
                        chunk_id=chunk_id,
                        chunk_index=chunk_index,
                        content=slice_text,
                        character_count=len(slice_text),
                        metadata=document.metadata,
                        created_at=created_at,
                    )
                )
                chunk_index += 1
        if self._embedding_service is not None and self._embedding_service.available:
            vectors = self._embedding_service.embed_batch([chunk.content for chunk in chunks])
            chunks = [
                replace(chunk, embedding=vector)
                for chunk, vector in zip(chunks, vectors, strict=True)
            ]
        return chunks

    def _slice_paragraph(self, paragraph: str) -> list[str]:
        """把长段落切成固定大小片段。"""

        if len(paragraph) <= _MAX_CHUNK_SIZE:
            return [paragraph]
        return [paragraph[start : start + _MAX_CHUNK_SIZE] for start in range(0, len(paragraph), _MAX_CHUNK_SIZE)]

    def _chunk_id(self, document_id: str, version: int, chunk_index: int, content: str) -> str:
        """生成可重复的 chunk_id，确保重复 chunking 结果稳定。"""

        digest = hashlib.sha256(f"{document_id}:{version}:{chunk_index}:{content}".encode("utf-8")).hexdigest()
        return f"chk-{digest[:24]}"

    def _publish(
        self,
        document_id: str,
        event_type: str,
        message: str,
        *,
        status: str,
        version: int | None = None,
        extra: dict[str, object] | None = None,
        error_code: str | None = None,
    ) -> None:
        """把 chunk 状态变化写入统一事件仓库。"""

        payload = {
            "document_id": document_id,
            "request_id": get_request_id(),
            "trace_id": get_request_id(),
            "status": status,
        }
        if version is not None:
            payload["version"] = version
        if extra:
            payload.update(extra)
        event = self._event_publisher.publish(document_id, event_type, message, payload)
        log_event(
            logger,
            "info",
            event_type,
            message,
            request_id=get_request_id(),
            task_id=document_id,
            status=status,
            node="document_chunk",
            error_code=error_code,
            sequence=event.sequence,
        )


__all__ = ["DocumentChunkService"]
