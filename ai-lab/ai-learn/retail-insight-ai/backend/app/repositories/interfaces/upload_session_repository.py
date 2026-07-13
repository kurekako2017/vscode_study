"""上传会话与幂等键的持久化合同。"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from app.models.upload import UploadSessionRecord


@runtime_checkable
class UploadSessionRepository(Protocol):
    def save(self, record: UploadSessionRecord) -> None: ...

    def get_by_checksum(self, checksum: str) -> UploadSessionRecord | None: ...

    def get_by_idempotency_key(self, idempotency_key: str) -> UploadSessionRecord | None: ...


__all__ = ["UploadSessionRepository"]
