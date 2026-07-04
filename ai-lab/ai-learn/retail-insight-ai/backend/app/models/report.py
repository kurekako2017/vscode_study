from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from app.models.task import utc_now


class ReportStatus(StrEnum):
    """定义报告当前状态，并为后续 Approval Workflow 预留边界。"""

    GENERATED = "generated"
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVISED = "revised"
    PUBLISHED = "published"
    ARCHIVED = "archived"


@dataclass(frozen=True)
class Report:
    """保存最终 Markdown 报告及生成 Provider，并预留审批状态边界。"""

    task_id: str
    markdown: str
    provider: str
    status: ReportStatus = ReportStatus.GENERATED
    created_at: datetime = field(default_factory=utc_now)
