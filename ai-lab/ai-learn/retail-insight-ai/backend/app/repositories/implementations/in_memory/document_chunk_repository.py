"""DocumentChunkRepository 的单进程内存实现。

文件职责：
- 保存文档 chunk 的替换式写入和读取。
- 作为 chunk pipeline MVP 的本地实现，支撑单元测试与本地运行。

谁会调用它：
- DocumentChunkService 和后续检索 / RAG 组件。

它调用谁：
- 只调用文档切片领域模型，不依赖 API、Workflow 或数据库细节。

输入是什么：
- document_id、version、DocumentChunk 列表。

输出是什么：
- DocumentChunk 列表快照，或空列表。

为什么需要这一层：
- 先把 chunk 切片事实固定住，再替换成 PostgreSQL 或别的持久化实现。

日本现场面试怎么讲：
- 这是文档切片的本地事实仓库，先确保 chunk 输出稳定，再升级持久化。
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import math
from collections.abc import Mapping, Sequence
from threading import RLock

from app.embeddings.service import validate_embedding_vector
from app.models.document import DocumentChunk
from app.repositories.interfaces.document_chunk_repository import VectorChunkMatch


class InMemoryDocumentChunkRepository:
    """线程安全的本地 chunk 仓库。"""

    def __init__(self) -> None:
        """初始化按 document/version 分组的 chunk 容器。"""

        self._chunks: dict[tuple[str, int], list[DocumentChunk]] = {}
        self._lock = RLock()

    def replace_for_document(self, document_id: str, version: int, chunks: list[DocumentChunk]) -> None:
        """替换某个文档版本的全部 chunks。"""

        with self._lock:
            self._chunks[(document_id, version)] = deepcopy(chunks)

    def list_for_document(self, document_id: str, version: int | None = None) -> list[DocumentChunk]:
        """返回某个文档版本的 chunk 快照。"""

        with self._lock:
            if version is None:
                candidates = [
                    (doc_version, chunks)
                    for (doc_id, doc_version), chunks in self._chunks.items()
                    if doc_id == document_id
                ]
                if not candidates:
                    return []
                _, latest_chunks = max(candidates, key=lambda item: item[0])
                return deepcopy(latest_chunks)
            return deepcopy(self._chunks.get((document_id, version), []))

    def update_embedding(self, chunk_id: str, embedding: Sequence[float] | None) -> None:
        """更新现有 chunk；找不到时明确失败，避免把写错 ID 静默当成功。"""

        normalized = validate_embedding_vector(embedding) if embedding is not None else None
        with self._lock:
            for key, chunks in self._chunks.items():
                for index, chunk in enumerate(chunks):
                    if chunk.chunk_id == chunk_id:
                        chunks[index] = replace(chunk, embedding=normalized)
                        return
        raise KeyError(f"document chunk not found: {chunk_id}")

    def search_by_embedding(
        self,
        embedding: Sequence[float],
        *,
        limit: int,
        document_ids: Sequence[str] | None = None,
        document_versions: Mapping[str, int] | None = None,
    ) -> list[VectorChunkMatch]:
        """在内存中计算 cosine，作为默认 backend 的兼容实现。"""

        query = validate_embedding_vector(embedding)
        if limit < 1:
            raise ValueError("vector search limit must be greater than zero")
        allowed = set(document_ids) if document_ids is not None else None
        matches: list[VectorChunkMatch] = []
        query_norm = math.sqrt(sum(value * value for value in query))
        with self._lock:
            for chunks in self._chunks.values():
                for chunk in chunks:
                    if chunk.embedding is None:
                        continue
                    if allowed is not None and chunk.document_id not in allowed:
                        continue
                    if (
                        document_versions is not None
                        and document_versions.get(chunk.document_id) != chunk.version
                    ):
                        continue
                    chunk_norm = math.sqrt(sum(value * value for value in chunk.embedding))
                    if query_norm == 0 or chunk_norm == 0:
                        similarity = 0.0
                    else:
                        similarity = sum(
                            left * right for left, right in zip(query, chunk.embedding, strict=True)
                        ) / (query_norm * chunk_norm)
                    matches.append(VectorChunkMatch(deepcopy(chunk), similarity))
        matches.sort(
            key=lambda item: (
                -item.cosine_similarity,
                item.chunk.document_id,
                item.chunk.chunk_index,
                item.chunk.chunk_id,
            )
        )
        return matches[:limit]


__all__ = ["InMemoryDocumentChunkRepository"]
