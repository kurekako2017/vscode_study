"""文档检索 API 的请求/响应 schema。

文件职责：
- 定义 POST /api/v1/document-retrieval/search 的请求与响应合同。
- 让 keyword-only 检索结果保持稳定的 JSON 结构，便于未来替换搜索后端。

谁会调用它：
- `backend/app/api/document_retrieval.py` 路由，以及检索相关测试。

它调用谁：
- 只依赖 Pydantic 和文档领域枚举，不依赖仓储、Workflow 或 LLM。

输入是什么：
- 查询文本、limit、归档过滤、文档类型过滤、语言过滤、标签过滤。

输出是什么：
- `DocumentRetrievalSearchResponse` 与结果项列表。

为什么需要这一层：
- 先冻结检索响应字段，再让 service 只负责 keyword ranking 与来源追踪。

日本现场面试怎么讲：
- 这是文档检索的稳定输出合同，后续换成 PostgreSQL full-text、hybrid search 或 retrieval provider 时，接口可以保持兼容。
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator
from app.schemas.document_api import DocumentResponse, DocumentSourceResponse


class DocumentRetrievalSearchRequest(BaseModel):
    """冻结 keyword-only 检索请求。"""

    query: str
    limit: int = Field(default=10)
    include_archived: bool = False
    document_type: str | None = None
    language: str | None = None
    tags: list[str] | None = None

    @field_validator("query")
    @classmethod
    def _normalize_query(cls, value: str) -> str:
        """保留原始文本，但去掉首尾空白，避免空 query 混入业务层。"""

        return value.strip()

    @field_validator("tags")
    @classmethod
    def _normalize_tags(cls, value: list[str] | None) -> list[str] | None:
        """确保 tags 只包含非空字符串。"""

        if value is None:
            return None
        normalized: list[str] = []
        for tag in value:
            if not isinstance(tag, str) or not tag.strip():
                raise ValueError("tags must contain non-empty strings")
            normalized.append(tag.strip())
        return normalized


class DocumentRetrievalResultResponse(BaseModel):
    """单条检索结果。"""

    document_id: str
    chunk_id: str
    chunk_index: int
    content_excerpt: str
    score: float
    source: DocumentSourceResponse
    metadata: DocumentResponse


class DocumentRetrievalSearchResponse(BaseModel):
    """冻结 POST /api/v1/document-retrieval/search 的成功响应。"""

    results: list[DocumentRetrievalResultResponse]
    total: int
    query: str
    retrieval_mode: str = "keyword"


__all__ = [
    "DocumentRetrievalResultResponse",
    "DocumentRetrievalSearchRequest",
    "DocumentRetrievalSearchResponse",
]
