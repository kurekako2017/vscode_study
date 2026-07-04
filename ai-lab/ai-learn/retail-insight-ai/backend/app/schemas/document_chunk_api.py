"""文档 chunk API 的请求/响应 schema。

文件职责：
- 定义 Document Chunk Pipeline MVP 的对外响应结构。
- 把 chunk 切片结果固定为可序列化 schema，方便后续替换成异步或持久化实现。

谁会调用它：
- `backend/app/api/document_chunks.py` 路由，以及 chunk 相关测试。

它调用谁：
- 只依赖 Pydantic 和文档领域模型，不依赖仓储实现。

输入是什么：
- chunk ID、document_id、版本、chunk 内容、字符数与父文档快照。

输出是什么：
- 可序列化的 `DocumentChunkResponse` 与 `DocumentChunkListResponse`。

为什么需要这一层：
- 先把 chunk 结果字段固定下来，再让切分算法和存储实现演进。

日本现场面试怎么讲：
- 这是文档切片流水线的稳定输出合同，未来切数据库或检索层时也能保持兼容。
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.models.document import Document, DocumentChunk
from app.schemas.document_api import DocumentResponse


class DocumentChunkResponse(BaseModel):
    """定义单个 chunk 的响应合同。"""

    document_id: str
    version: int
    chunk_id: str
    chunk_index: int
    content: str
    character_count: int
    metadata: DocumentResponse
    created_at: datetime

    @classmethod
    def from_domain(cls, chunk: DocumentChunk) -> "DocumentChunkResponse":
        """把领域 chunk 转成可序列化响应。"""

        document = Document(
            content=chunk.content,
            metadata=chunk.metadata,
            created_at=chunk.created_at,
            updated_at=chunk.metadata.updated_at,
        )
        return cls(
            document_id=chunk.document_id,
            version=chunk.version,
            chunk_id=chunk.chunk_id,
            chunk_index=chunk.chunk_index,
            content=chunk.content,
            character_count=chunk.character_count,
            metadata=DocumentResponse.from_domain(document),
            created_at=chunk.created_at,
        )


class DocumentChunkListResponse(BaseModel):
    """定义 GET /api/v1/documents/{document_id}/chunks 的响应合同。"""

    document_id: str
    version: int
    items: list[DocumentChunkResponse]
    next_cursor: str | None = None

    @classmethod
    def from_domain(cls, document: Document, chunks: list[DocumentChunk]) -> "DocumentChunkListResponse":
        """把 chunk 集合转换为对外响应。"""

        return cls(
            document_id=document.document_id,
            version=document.version,
            items=[DocumentChunkResponse.from_domain(chunk) for chunk in chunks],
            next_cursor=None,
        )


__all__ = ["DocumentChunkListResponse", "DocumentChunkResponse"]
