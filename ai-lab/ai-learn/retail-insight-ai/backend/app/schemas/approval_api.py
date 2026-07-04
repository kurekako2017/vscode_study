"""Approval API 的请求/响应 schema。

文件职责：
- 定义审批申请、审批决策和报告修订的 HTTP schema。
- 把 approval workflow 的对外字段固定下来，避免 service 返回内部模型。

谁会调用它：
- `backend/app/api/approvals.py` 路由，以及 approval API 测试。

它调用谁：
- 只依赖 Pydantic 和审批领域 enum，不依赖 repository 实现。

输入是什么：
- task_id、approval_id、comment、reason、revision_reason、列表过滤条件。

输出是什么：
- 可序列化的审批响应对象、列表对象和修订对象。

为什么需要这一层：
- 先把 approval contract 的 HTTP 输出字段固定，再让 service 在内部演进版本存储和审计逻辑。

日本现场面试怎么讲：
- 这是 approval workflow 的稳定输出合同，未来即使换成数据库或 RBAC，外部字段仍可以保持兼容。
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.models.approval import ApprovalRequest, ReportVersion
from app.models.report import ReportStatus


class ApprovalSubmitRequest(BaseModel):
    """冻结 submit-approval 的请求结构。"""

    comment: str | None = None

    @field_validator("comment")
    @classmethod
    def _normalize_comment(cls, value: str | None) -> str | None:
        """保留备注但去掉首尾空白。"""

        if value is None:
            return None
        value = value.strip()
        return value or None


class ApprovalRejectRequest(BaseModel):
    """冻结 reject 的请求结构。"""

    reason: str | None = None

    @field_validator("reason")
    @classmethod
    def _normalize_reason(cls, value: str | None) -> str | None:
        """保留拒绝原因，但保证空字符串不会进入 service。"""

        if value is None:
            return None
        value = value.strip()
        return value or None


class ApprovalReviseRequest(BaseModel):
    """冻结 revise 的请求结构。"""

    revision_reason: str | None = None

    @field_validator("revision_reason")
    @classmethod
    def _normalize_revision_reason(cls, value: str | None) -> str | None:
        """保留修订原因，但保证空字符串不会进入 service。"""

        if value is None:
            return None
        value = value.strip()
        return value or None


class ApprovalResponse(BaseModel):
    """冻结审批记录的对外响应。"""

    approval_id: str
    task_id: str
    report_version_id: str
    status: ReportStatus
    requested_at: datetime
    requested_by: str | None = None
    decided_at: datetime | None = None
    decided_by: str | None = None
    decision_reason: str | None = None
    revision_no: int
    revised_from_version_id: str | None = None

    @classmethod
    def from_domain(cls, approval: ApprovalRequest) -> "ApprovalResponse":
        """把领域审批记录转成对外响应。"""

        return cls(
            approval_id=approval.id,
            task_id=approval.task_id,
            report_version_id=approval.report_version_id,
            status=approval.status,
            requested_at=approval.requested_at,
            requested_by=approval.requested_by,
            decided_at=approval.decision_at,
            decided_by=approval.approver_id,
            decision_reason=approval.decision_reason,
            revision_no=approval.revision_no,
            revised_from_version_id=approval.revised_from_version_id,
        )


class ApprovalListResponse(BaseModel):
    """冻结 GET /api/v1/approvals 的列表输出。"""

    items: list[ApprovalResponse]
    next_cursor: str | None = None

    @classmethod
    def from_domain(cls, approvals: list[ApprovalRequest]) -> "ApprovalListResponse":
        """把领域审批记录列表转换为对外响应。"""

        return cls(items=[ApprovalResponse.from_domain(item) for item in approvals], next_cursor=None)


class ApprovalRevisionResponse(BaseModel):
    """冻结 report revise 的输出。"""

    task_id: str
    report_version_id: str
    status: ReportStatus
    revision_no: int
    revised_from_version_id: str | None = None

    @classmethod
    def from_domain(cls, version: ReportVersion) -> "ApprovalRevisionResponse":
        """把新版本快照转成对外修订结果。"""

        return cls(
            task_id=version.task_id,
            report_version_id=version.id,
            status=version.status,
            revision_no=version.version_no,
            revised_from_version_id=version.revised_from_version_id,
        )


__all__ = [
    "ApprovalListResponse",
    "ApprovalRejectRequest",
    "ApprovalResponse",
    "ApprovalRevisionResponse",
    "ApprovalReviseRequest",
    "ApprovalSubmitRequest",
]
