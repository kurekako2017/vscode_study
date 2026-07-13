"""上传会话领域快照，用于跨进程幂等与重复文件查询。"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class UploadSessionRecord:
    """保存成功上传响应所需的全部稳定字段。"""

    upload_id: str
    document_id: str
    checksum: str
    status: str
    progress: int
    created_at: datetime
    updated_at: datetime
    idempotency_key: str | None = None
    error_code: str | None = None
    error_message: str | None = None


__all__ = ["UploadSessionRecord"]
