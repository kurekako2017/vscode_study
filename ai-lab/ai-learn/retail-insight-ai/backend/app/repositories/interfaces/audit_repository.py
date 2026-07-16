"""AuditRepository 的 Protocol。

文件职责：
- 定义 append-only audit log 的持久化合同。
- 让 audit service 不绑定内存实现或未来数据库实现。

谁会调用它：
- `backend/app/services/audit_service.py` 和 in-memory / future PostgreSQL repository。

它调用谁：
- 只依赖 audit 领域模型，不依赖 API 或 workflow。

输入是什么：
- AuditLog 事实对象。

输出是什么：
- 已存储的 AuditLog 快照，或审计日志列表。

为什么需要这一层：
- 审计记录必须 write-once，后续只允许追加，不允许回写历史。

日本现场面试怎么讲：
- 这是 audit trail 的事实层接口，先做 in-memory 实现，未来换 PostgreSQL 只改 repository。
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from app.models.audit import AuditLog, AuditLogFilter, AuditLogPage


@runtime_checkable
class AuditRepository(Protocol):
    """定义审计日志的追加与读取合同。"""

    def append(self, log: AuditLog) -> AuditLog:
        """追加一条审计事实并返回存储快照。"""

        ...

    def list_all(self) -> list[AuditLog]:
        """返回按追加顺序排列的全部审计事实。"""

        ...


@runtime_checkable
class PersistentAuditRepository(AuditRepository, Protocol):
    """仅 PostgreSQL 实现的企业审计查询合同。"""

    def query(self, filters: AuditLogFilter) -> AuditLogPage:
        """按过滤条件、分页和稳定倒序返回审计事实。"""

        ...


__all__ = ["AuditRepository", "PersistentAuditRepository"]
