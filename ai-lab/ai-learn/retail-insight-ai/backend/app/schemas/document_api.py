"""文档上传 API 的请求/响应 schema。

文件职责：
- 定义 Document Upload MVP 的对外响应结构。
- 把服务层返回的会话状态包装成稳定的 HTTP schema。

谁会调用它：
- `backend/app/api/documents.py` 路由，以及文档上传测试。

它调用谁：
- 只依赖 Pydantic 和领域层 enum，不依赖仓储或工作流。

输入是什么：
- 上传会话状态、上传 ID、文档 ID、时间戳与错误信息。

输出是什么：
- 可序列化的 `DocumentUploadSessionResponse`。

为什么需要这一层：
- 先把 Upload Session 的响应字段固定下来，再让实现细节在 service 层演进。

日本现场面试怎么讲：
- 这是上传接口的稳定输出合同，后续即使换成 PostgreSQL 或异步处理，字段也可以保持兼容。
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field

from app.models.document import (
    Document,
    DocumentSource,
    DocumentStatus,
    DocumentType,
    Language,
)


class UploadSessionStatus(StrEnum):
    """定义上传会话的冻结状态。"""

    ACCEPTED = "accepted"
    VALIDATING = "validating"
    STORING = "storing"
    COMPLETED = "completed"
    FAILED = "failed"


class DocumentUploadSessionResponse(BaseModel):
    """定义 POST /api/v1/documents 的成功响应合同。"""

    upload_id: str
    document_id: str
    status: UploadSessionStatus
    progress: int = Field(ge=0, le=100)
    created_at: datetime
    updated_at: datetime
    error_code: str | None = None
    error_message: str | None = None


class DocumentSourceResponse(BaseModel):
    """对外公开文档来源信息。"""

    source_type: str
    uri: str
    label: str | None = None
    external_id: str | None = None

    @classmethod
    def from_domain(cls, source: DocumentSource) -> "DocumentSourceResponse":
        """把领域来源对象转成可序列化响应。"""

        return cls(
            source_type=source.source_type,
            uri=source.uri,
            label=source.label,
            external_id=source.external_id,
        )


class DocumentResponse(BaseModel):
    """定义 GET /api/v1/documents/{document_id} 的响应合同。"""

    document_id: str
    title: str
    description: str | None
    owner: str
    created_at: datetime
    updated_at: datetime
    version: int
    language: Language
    document_type: DocumentType
    status: DocumentStatus
    tags: tuple[str, ...]
    source: DocumentSourceResponse | None
    checksum: str
    # 列表页可用性字段：chunk 数 / 是否可检索 / 是否归档
    chunk_count: int = 0
    searchable: bool = False
    archived: bool = False

    @classmethod
    def from_domain(
        cls,
        document: Document,
        *,
        chunk_count: int | None = None,
    ) -> "DocumentResponse":
        """显式选择对 API 公开的文档字段。"""

        source = document.metadata.source
        status = document.metadata.status
        count = 0 if chunk_count is None else max(0, int(chunk_count))
        archived = status is DocumentStatus.ARCHIVED
        searchable = (not archived) and count > 0
        return cls(
            document_id=document.document_id,
            title=document.metadata.title,
            description=document.metadata.description,
            owner=document.metadata.owner,
            created_at=document.created_at,
            updated_at=document.updated_at,
            version=document.version,
            language=document.metadata.language,
            document_type=document.metadata.document_type,
            status=status,
            tags=document.metadata.tags,
            source=DocumentSourceResponse.from_domain(source) if source is not None else None,
            checksum=document.metadata.checksum,
            chunk_count=count,
            searchable=searchable,
            archived=archived,
        )


class DocumentArchiveResponse(BaseModel):
    """定义 DELETE /api/v1/documents/{document_id} 的归档响应。"""

    document_id: str
    status: DocumentStatus

    @classmethod
    def from_domain(cls, document: Document) -> "DocumentArchiveResponse":
        """返回归档后的最小响应视图。"""

        return cls(document_id=document.document_id, status=document.status)


class DocumentListResponse(BaseModel):
    """定义 GET /api/v1/documents 的分页式响应合同。"""

    items: list[DocumentResponse]
    next_cursor: str | None = None

    @classmethod
    def from_domain(
        cls,
        documents: list[Document],
        *,
        chunk_counts: dict[str, int] | None = None,
    ) -> "DocumentListResponse":
        """把领域文档列表转换为对外响应。"""

        counts = chunk_counts or {}
        return cls(
            items=[
                DocumentResponse.from_domain(
                    document,
                    chunk_count=counts.get(document.document_id, 0),
                )
                for document in documents
            ],
            next_cursor=None,
        )


__all__ = [
    "DocumentArchiveResponse",
    "DocumentListResponse",
    "DocumentResponse",
    "DocumentSourceResponse",
    "DocumentUploadSessionResponse",
    "UploadSessionStatus",
]
