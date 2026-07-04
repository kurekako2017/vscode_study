"""DocumentRepository 的单进程内存实现。

文件职责：
- 保存文档域的创建、读取、更新、删除与 checksum 去重逻辑。
- 作为当前默认本地实现，支撑 Document Domain Model 的单元测试与本地运行。

谁会调用它：
- 未来的 Upload / Version / Approval / Retrieval Service，以及当前的架构和单元测试。

它调用谁：
- 只调用文档领域模型和统一的验证异常，不依赖 API、Workflow 或数据库细节。

输入是什么：
- Document 聚合根、document_id、checksum 查询条件。

输出是什么：
- Document、Document 列表，或空值。

为什么需要这一层：
- 先把文档事实和重复 checksum 约束固定住，再替换成 PostgreSQL Repository。

日本现场面试怎么讲：
- 这是文档域的本地事实仓库，先确保 CRUD 和去重正确，再把存储实现平滑升级到数据库。
"""

from __future__ import annotations

from copy import deepcopy
from threading import RLock

from app.errors.exceptions import ValidationAppException
from app.models.document import Document


class InMemoryDocumentRepository:
    """线程安全的本地文档仓库，保存文档事实和重复 checksum 约束。"""

    def __init__(self) -> None:
        """初始化文档映射和保护并发访问的进程内锁。"""

        self._documents: dict[str, Document] = {}
        self._lock = RLock()

    def create(self, document: Document) -> None:
        """创建文档并拒绝重复 ID / 重复 checksum。"""

        with self._lock:
            document.validate_for_creation()
            if document.document_id in self._documents:
                raise ValidationAppException(
                    {
                        "field": "document_id",
                        "reason": "document already exists",
                        "document_id": document.document_id,
                    }
                )
            if self.find_by_checksum(document.metadata.checksum) is not None:
                raise ValidationAppException(
                    {
                        "field": "checksum",
                        "reason": "duplicate checksum",
                        "checksum": document.metadata.checksum,
                    }
                )
            self._documents[document.document_id] = deepcopy(document)

    def get(self, document_id: str) -> Document | None:
        """返回文档深拷贝，避免调用方绕过 update 修改仓库状态。"""

        with self._lock:
            document = self._documents.get(document_id)
            return deepcopy(document) if document is not None else None

    def list_all(self) -> list[Document]:
        """返回全部文档快照，便于后台管理和测试验证。"""

        with self._lock:
            return [deepcopy(document) for document in self._documents.values()]

    def update(self, document: Document) -> None:
        """保存已存在文档的最新状态。"""

        with self._lock:
            if document.document_id not in self._documents:
                raise KeyError(document.document_id)
            document.validate_for_storage()
            duplicate = self.find_by_checksum(document.metadata.checksum)
            if duplicate is not None and duplicate.document_id != document.document_id:
                raise ValidationAppException(
                    {
                        "field": "checksum",
                        "reason": "duplicate checksum",
                        "checksum": document.metadata.checksum,
                    }
                )
            self._documents[document.document_id] = deepcopy(document)

    def delete(self, document_id: str) -> None:
        """将指定文档软删除为 archived，保留历史事实。"""

        with self._lock:
            document = self._documents.get(document_id)
            if document is None:
                raise KeyError(document_id)
            document.archive()
            self._documents[document_id] = deepcopy(document)

    def find_by_checksum(self, checksum: str) -> Document | None:
        """按 checksum 查找文档，供重复检测和未来导入去重使用。"""

        with self._lock:
            for document in self._documents.values():
                if document.metadata.checksum == checksum:
                    return deepcopy(document)
        return None


__all__ = ["InMemoryDocumentRepository"]
