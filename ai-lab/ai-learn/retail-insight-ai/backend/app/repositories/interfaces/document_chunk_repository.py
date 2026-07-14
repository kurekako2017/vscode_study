"""DocumentChunkRepository 的 Protocol。

文件职责：
- 定义文档 chunk 的保存与读取合同。
- 把 chunk 存储从 service 中抽离出来，便于未来切 PostgreSQL 或对象存储。

谁会调用它：
- DocumentChunkService，以及后续的检索 / RAG 组件。

它调用谁：
- 不直接调用其他层，只依赖文档切片领域模型。

输入是什么：
- document_id、version、DocumentChunk 列表。

输出是什么：
- 某个文档版本对应的 chunk 列表，或空列表。

为什么需要这一层：
- 先固定 chunk 存储边界，再让实现从内存平滑替换到数据库。

日本现场面试怎么讲：
- 这是文档切片事实的存储接口，先用内存实现跑通，后续可以无痛升级持久化。
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from app.models.document import DocumentChunk


@dataclass(frozen=True)
class VectorChunkMatch:
    """Repository 返回的 chunk 与原始 cosine similarity。"""

    chunk: DocumentChunk
    cosine_similarity: float


@runtime_checkable
class DocumentChunkRepository(Protocol):
    """定义文档 chunk 的替换式保存和读取合同。"""

    def replace_for_document(self, document_id: str, version: int, chunks: list[DocumentChunk]) -> None:
        """替换某个文档版本的全部 chunks。"""

        ...

    def list_for_document(self, document_id: str, version: int | None = None) -> list[DocumentChunk]:
        """读取某个文档版本的 chunks。"""

        ...

    def update_embedding(self, chunk_id: str, embedding: Sequence[float] | None) -> None:
        """更新单个 chunk 向量；None 用于保留或恢复旧数据兼容状态。"""

        ...

    def search_by_embedding(
        self,
        embedding: Sequence[float],
        *,
        limit: int,
        document_ids: Sequence[str] | None = None,
        document_versions: Mapping[str, int] | None = None,
    ) -> list[VectorChunkMatch]:
        """按 cosine similarity 查询带向量的 chunks。"""

        ...


__all__ = ["DocumentChunkRepository", "VectorChunkMatch"]
