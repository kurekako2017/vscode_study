from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from app.models.task import utc_now


class DataImportStatus(StrEnum):
    """定义导入批次状态。"""

    ACCEPTED = "accepted"
    FAILED = "failed"
    PROCESSED = "processed"


@dataclass(frozen=True)
class DataImport:
    """保存导入批次元数据；当前只用于 schema 和后续 Repository 设计。"""

    id: str
    import_type: str
    file_name: str
    file_path: str
    schema_version: str
    status: DataImportStatus
    record_count: int
    started_at: datetime = field(default_factory=utc_now)
    completed_at: datetime | None = None
    created_by: str | None = None


@dataclass(frozen=True)
class ImportErrorRecord:
    """保存导入错误明细；当前只用于 schema 和后续 Repository 设计。"""

    id: str
    data_import_id: str
    error_code: str
    field_name: str | None = None
    row_number: int | None = None
    message: str = ""
    created_at: datetime = field(default_factory=utc_now)


@dataclass(frozen=True)
class ReportVersion:
    """保存报告版本历史；当前由 PostgreSQL ReportRepository 追加版本数据。"""

    id: str | None
    task_id: str
    version_no: int
    markdown: str
    status: str
    revision_reason: str | None = None
    created_at: datetime = field(default_factory=utc_now)
    created_by: str | None = None


@dataclass(frozen=True)
class ApprovalRequest:
    """保存审批申请；当前只建模不接 API。"""

    id: str
    report_version_id: str
    requested_by: str | None = None
    requested_at: datetime = field(default_factory=utc_now)
    status: str = "pending_approval"
    approver_id: str | None = None
    decision_at: datetime | None = None


@dataclass(frozen=True)
class ApprovalEvent:
    """保存审批事件；当前只建模不接 API。"""

    id: str
    approval_request_id: str
    event_type: str
    actor_id: str | None = None
    reason: str | None = None
    created_at: datetime = field(default_factory=utc_now)
