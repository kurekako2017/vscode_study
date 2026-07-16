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

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.audit import AuditLog, AuditLogFilter, AuditLogPage, AuditLogResult


class AuditLogQuery(BaseModel):
    """Audit 查询参数；限制页大小并强制合法 UTC/带时区时间范围。"""

    model_config = ConfigDict(extra="forbid")

    actor_user_id: str | None = Field(default=None, min_length=1, max_length=128)
    actor_username: str | None = Field(default=None, min_length=1, max_length=128)
    actor_role: str | None = Field(default=None, min_length=1, max_length=64)
    action: str | None = Field(default=None, min_length=1, max_length=128)
    resource_type: str | None = Field(default=None, min_length=1, max_length=128)
    resource_id: str | None = Field(default=None, min_length=1, max_length=256)
    result: AuditLogResult | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    request_id: str | None = Field(default=None, min_length=1, max_length=128)
    limit: int = Field(default=50, ge=1, le=200)
    offset: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def validate_time_range(self) -> "AuditLogQuery":
        """拒绝无时区时间和逆序范围，由统一 validation handler 返回 422。"""

        for field_name, value in (
            ("start_time", self.start_time),
            ("end_time", self.end_time),
        ):
            if value is not None and value.tzinfo is None:
                raise ValueError(f"{field_name} must include timezone")
        if (
            self.start_time is not None
            and self.end_time is not None
            and self.start_time > self.end_time
        ):
            raise ValueError("start_time must be earlier than or equal to end_time")
        return self

    def to_domain(self) -> AuditLogFilter:
        """转换为不依赖 HTTP/Pydantic 的 Repository 查询条件。"""

        return AuditLogFilter(**self.model_dump())


class AuditLogResponse(BaseModel):
    """冻结 GET /api/v1/audit-logs 的单条记录。"""

    audit_log_id: str
    occurred_at: datetime
    actor_user_id: str | None
    actor_username: str | None
    actor_role: str | None
    action: str
    permission: str | None
    http_method: str | None
    api_path: str | None
    status_code: int | None
    # 以下旧字段继续输出，保证既有客户端与学习测试不被迁移破坏。
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
            occurred_at=log.timestamp,
            actor_user_id=log.actor_id,
            actor_username=log.actor_username,
            actor_role=log.actor_role,
            action=log.operation_type,
            permission=log.permission,
            http_method=log.http_method,
            api_path=log.api_path,
            status_code=log.status_code,
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
    def from_page(cls, page: AuditLogPage) -> "AuditLogListResponse":
        """把审计分页结果转成对外 response。"""

        return cls(
            items=[AuditLogResponse.from_domain(log) for log in page.items],
            next_cursor=(
                str(page.next_offset) if page.next_offset is not None else None
            ),
        )

    @classmethod
    def from_domain(cls, logs: list[AuditLog]) -> "AuditLogListResponse":
        """保留旧调用方式，内部统一转换成无下一页的 page。"""

        return cls.from_page(AuditLogPage(items=logs, next_offset=None))
