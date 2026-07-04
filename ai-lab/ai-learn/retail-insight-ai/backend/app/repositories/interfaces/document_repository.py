"""DocumentRepository 的 Protocol。

文件职责：
- 定义文档域的创建、读取、更新、删除与 checksum 查询合同。
- 给 Service 和测试提供稳定接口，不暴露具体存储实现。

谁会调用它：
- 未来的 Upload / Version / Approval / Retrieval Service，以及当前的内存实现测试。

它调用谁：
- 不直接调用其他层，只依赖文档领域模型。

输入是什么：
- Document 聚合根、document_id、checksum 查询条件。

输出是什么：
- Document 或 Document 列表，或空值。

为什么需要这一层：
- 先固定 Repository 合同，再替换成 PostgreSQL 或其他持久化实现。

日本现场面试怎么讲：
- 这是文档事实的存储接口，先保留内存实现，后续可以无痛切到数据库。
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from app.models.document import Document


@runtime_checkable
class DocumentRepository(Protocol):
    """定义文档域的 CRUD 和 checksum 查询合同。"""

    def create(self, document: Document) -> None:
        """创建文档，重复 ID 或重复 checksum 应被拒绝。"""

        ...

    def get(self, document_id: str) -> Document | None:
        """按 ID 读取文档；不存在时返回 None。"""

        ...

    def list_all(self) -> list[Document]:
        """返回全部文档的快照列表。"""

        ...

    def update(self, document: Document) -> None:
        """保存文档的最新状态。"""

        ...

    def delete(self, document_id: str) -> None:
        """软删除指定文档，语义上应将状态归档；不存在时应报错。"""

        ...

    def find_by_checksum(self, checksum: str) -> Document | None:
        """按 checksum 查询文档，便于重复检测。"""

        ...


__all__ = ["DocumentRepository"]
