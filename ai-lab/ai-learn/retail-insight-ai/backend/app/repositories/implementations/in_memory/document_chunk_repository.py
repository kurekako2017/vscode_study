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
from threading import RLock

from app.models.document import DocumentChunk


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


__all__ = ["InMemoryDocumentChunkRepository"]
