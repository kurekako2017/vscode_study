"""AuditRepository 的单进程内存实现。"""

from __future__ import annotations

from copy import deepcopy
from threading import RLock

from app.errors.exceptions import ValidationAppException
from app.models.audit import AuditLog


class InMemoryAuditRepository:
    """线程安全的本地审计仓库，只允许追加，不提供修改或删除。"""

    def __init__(self) -> None:
        """初始化审计日志列表和并发锁。"""

        self._logs: list[AuditLog] = []
        self._log_ids: set[str] = set()
        self._lock = RLock()

    def append(self, log: AuditLog) -> AuditLog:
        """追加审计事实，重复 ID 会被拒绝以保持写一次语义。"""

        with self._lock:
            if log.audit_log_id in self._log_ids:
                raise ValidationAppException(
                    {
                        "field": "audit_log_id",
                        "reason": "audit log already exists",
                        "audit_log_id": log.audit_log_id,
                    }
                )
            stored = deepcopy(log)
            self._logs.append(stored)
            self._log_ids.add(stored.audit_log_id)
            return deepcopy(stored)

    def list_all(self) -> list[AuditLog]:
        """按追加顺序返回深拷贝，避免调用方修改仓库内部事实。"""

        with self._lock:
            return [deepcopy(log) for log in self._logs]

