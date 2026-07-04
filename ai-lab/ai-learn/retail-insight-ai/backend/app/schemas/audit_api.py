"""Audit API schemas.

文件职责：
- 定义 audit-logs 的 read-only response schema。
- 把 audit service 返回的领域事实转换成对外稳定合同。

谁会调用它：
- `backend/app/api/audit_logs.py` 路由和对应测试。

它调用谁：
- 只依赖 Pydantic 和 audit domain model，不依赖 repository 实现。

输入是什么：
- AuditLog 事实对象列表。

输出是什么：
- 可序列化的审计日志列表与分页占位字段。

为什么需要这一层：
- 审计事实是 append-only，但 HTTP 输出仍然需要稳定字段与排序。

日本现场面试怎么讲：
- 这是 audit trail 的 read model，未来即使换 PostgreSQL，输出字段也不需要改。
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.models.audit import AuditLog


class AuditLogResponse(BaseModel):
    """冻结 GET /api/v1/audit-logs 的单条记录。"""

    audit_log_id: str
    operation_type: str
    actor_id: str | None
    organization_id: str | None
    department_id: str | None
    resource_type: str
    resource_id: str
    result: str
    error_code: str | None
    request_id: str
    trace_id: str
    timestamp: datetime
    metadata: dict[str, Any]

    @classmethod
    def from_domain(cls, log: AuditLog) -> "AuditLogResponse":
        """从领域审计日志生成对外 response。"""

        return cls(
            audit_log_id=log.audit_log_id,
            operation_type=log.operation_type,
            actor_id=log.actor_id,
            organization_id=log.organization_id,
            department_id=log.department_id,
            resource_type=log.resource_type,
            resource_id=log.resource_id,
            result=log.result.value,
            error_code=log.error_code,
            request_id=log.request_id,
            trace_id=log.trace_id,
            timestamp=log.timestamp,
            metadata=log.metadata,
        )


class AuditLogListResponse(BaseModel):
    """冻结 GET /api/v1/audit-logs 的列表输出。"""

    items: list[AuditLogResponse]
    next_cursor: str | None = None

    @classmethod
    def from_domain(cls, logs: list[AuditLog]) -> "AuditLogListResponse":
        """把审计日志列表转成对外 response。"""

        return cls(items=[AuditLogResponse.from_domain(log) for log in logs], next_cursor=None)

