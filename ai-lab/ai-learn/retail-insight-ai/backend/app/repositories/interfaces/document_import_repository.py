"""Document Import 会话的持久化合同。"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from app.models.document_import import DocumentImportRecord


@runtime_checkable
class DocumentImportRepository(Protocol):
    def save(self, record: DocumentImportRecord) -> None: ...

    def get(self, import_id: str) -> DocumentImportRecord | None: ...

    def get_by_document_id(self, document_id: str) -> DocumentImportRecord | None: ...


__all__ = ["DocumentImportRepository"]
