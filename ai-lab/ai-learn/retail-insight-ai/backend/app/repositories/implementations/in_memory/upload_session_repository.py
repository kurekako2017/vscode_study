"""上传会话幂等缓存的默认 InMemory Repository。"""

from __future__ import annotations

from copy import deepcopy
from threading import RLock

from app.models.upload import UploadSessionRecord


class InMemoryUploadSessionRepository:
    def __init__(self) -> None:
        self._by_checksum: dict[str, UploadSessionRecord] = {}
        self._by_key: dict[str, UploadSessionRecord] = {}
        self._lock = RLock()

    def save(self, record: UploadSessionRecord) -> None:
        with self._lock:
            stored = deepcopy(record)
            self._by_checksum[record.checksum] = stored
            if record.idempotency_key is not None:
                self._by_key[record.idempotency_key] = stored

    def get_by_checksum(self, checksum: str) -> UploadSessionRecord | None:
        with self._lock:
            value = self._by_checksum.get(checksum)
            return deepcopy(value) if value else None

    def get_by_idempotency_key(self, idempotency_key: str) -> UploadSessionRecord | None:
        with self._lock:
            value = self._by_key.get(idempotency_key)
            return deepcopy(value) if value else None


__all__ = ["InMemoryUploadSessionRepository"]
