"""审批领域模型。

文件职责：
- 定义 ApprovalRequest、ApprovalEvent 和 ReportVersion 的冻结领域结构。
- 把审批请求、审批事件和报告版本快照固定成可审计、可回放的本地模型。

谁会调用它：
- `backend/app/services/approval_service.py`、approval repository、API schema 转换层和测试。

它调用谁：
- 只依赖 `ReportStatus` 和统一时间工具，不依赖 API 或数据库细节。

输入是什么：
- task_id、report_version_id、审批状态、决策人、原因、版本快照。

输出是什么：
- 可序列化、可审计、不可变的审批领域对象。

为什么需要这一层：
- 审批流程必须把“当前报告”和“历史版本”分开，避免审批结果被后续 revision 覆盖。

日本现场面试怎么讲：
- 这是 approval workflow 的领域边界，审批请求和报告版本快照分开后，后续接 PostgreSQL 或 RBAC 时更容易保持不可变事实。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from app.models.report import ReportStatus
from app.models.task import utc_now


def _uuid() -> str:
    """生成领域对象使用的稳定字符串 ID。"""

    return str(uuid4())


@dataclass(frozen=True)
class ReportVersion:
    """保存单个报告版本快照，内容一旦落库就不再修改。"""

    task_id: str
    version_no: int
    markdown: str
    status: ReportStatus
    revision_reason: str | None = None
    revised_from_version_id: str | None = None
    id: str = field(default_factory=_uuid)
    created_at: datetime = field(default_factory=utc_now)
    created_by: str | None = None


@dataclass(frozen=True)
class ApprovalRequest:
    """保存审批申请的当前状态。"""

    task_id: str
    report_version_id: str
    status: ReportStatus
    requested_by: str | None = None
    id: str = field(default_factory=_uuid)
    requested_at: datetime = field(default_factory=utc_now)
    approver_id: str | None = None
    decision_at: datetime | None = None
    decision_reason: str | None = None
    revision_no: int = 1
    revised_from_version_id: str | None = None


@dataclass(frozen=True)
class ApprovalEvent:
    """保存审批审计事件。"""

    approval_id: str
    task_id: str
    event_type: str
    actor_id: str | None = None
    reason: str | None = None
    id: str = field(default_factory=_uuid)
    created_at: datetime = field(default_factory=utc_now)


__all__ = ["ApprovalEvent", "ApprovalRequest", "ReportVersion"]
