"""Document Import 会话的默认 InMemory 实现。"""

from __future__ import annotations

from copy import deepcopy
from threading import RLock

from app.models.document_import import DocumentImportRecord


class InMemoryDocumentImportRepository:
    def __init__(self) -> None:
        self._by_id: dict[str, DocumentImportRecord] = {}
        self._by_document: dict[str, DocumentImportRecord] = {}
        self._lock = RLock()

    def save(self, record: DocumentImportRecord) -> None:
        with self._lock:
            stored = deepcopy(record)
            self._by_id[record.import_id] = stored
            self._by_document[record.document_id] = stored

    def get(self, import_id: str) -> DocumentImportRecord | None:
        with self._lock:
            record = self._by_id.get(import_id)
            return deepcopy(record) if record else None

    def get_by_document_id(self, document_id: str) -> DocumentImportRecord | None:
        with self._lock:
            record = self._by_document.get(document_id)
            return deepcopy(record) if record else None


__all__ = ["InMemoryDocumentImportRepository"]
