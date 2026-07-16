"""Audit log domain models.

文件职责：
- 定义 append-only AuditLog 领域对象与结果状态。
- 作为 future audit write path 和 current audit read path 的稳定事实层。

谁会调用它：
- audit service、audit repository、API schema 转换层和测试。

它调用谁：
- 只依赖统一时间工具，不依赖 API 或数据库细节。

输入是什么：
- actor、资源、操作类型、结果、request_id、trace_id、metadata。

输出是什么：
- 不可变、可追加、可读取的审计日志事实。

为什么需要这一层：
- 审计事实必须 append-only，不能用 update/delete 去改写历史。

日本现场面试怎么讲：
- 这是 audit trail 的事实模型，先把 write-once 语义固定住，后续换数据库也不会破坏审计可追溯性。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from app.models.task import utc_now


class AuditLogResult(StrEnum):
    """定义审计事实的最终结果。"""

    SUCCESS = "success"
    DENIED = "denied"
    FAILURE = "failure"
    # 兼容既有调用方名称；持久化值统一升级为企业合同要求的 failure。
    FAILED = "failure"

    @classmethod
    def _missing_(cls, value: object) -> "AuditLogResult | None":
        """兼容 migration 前已经写入 PostgreSQL 的 ``failed`` 旧值。"""

        if value == "failed":
            return cls.FAILURE
        return None


@dataclass(frozen=True)
class AuditLog:
    """保存一条 append-only 审计事实。"""

    operation_type: str
    actor_id: str | None
    organization_id: str | None
    department_id: str | None
    resource_type: str
    resource_id: str
    result: AuditLogResult
    request_id: str
    trace_id: str
    metadata: dict[str, Any] = field(default_factory=dict)
    error_code: str | None = None
    audit_log_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=utc_now)
    actor_username: str | None = None
    actor_role: str | None = None
    permission: str | None = None
    http_method: str | None = None
    api_path: str | None = None
    status_code: int | None = None


@dataclass(frozen=True)
class AuditLogFilter:
    """PostgreSQL Persistent Audit 的查询条件。"""

    actor_user_id: str | None = None
    actor_username: str | None = None
    actor_role: str | None = None
    action: str | None = None
    resource_type: str | None = None
    resource_id: str | None = None
    result: AuditLogResult | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    request_id: str | None = None
    limit: int = 50
    offset: int = 0


@dataclass(frozen=True)
class AuditLogPage:
    """保存稳定倒序查询的一页审计事实。"""

    items: list[AuditLog]
    next_offset: int | None
