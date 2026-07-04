from __future__ import annotations

from dataclasses import replace

from app.errors.base import AppException
from app.errors.exceptions import (
    ApprovalAlreadyDecidedException,
    ApprovalAlreadySubmittedException,
    ApprovalNotFoundException,
    ApprovalReportNotFoundException,
    InvalidApprovalStateException,
    MissingRejectionReasonException,
    ReportRevisionConflictException,
)
from app.events.publisher import EventPublisher
from app.models.approval import ApprovalEvent, ApprovalRequest, ReportVersion
from app.models.report import Report, ReportStatus
from app.models.task import utc_now
from app.observability.logging import get_logger, log_event
from app.repositories.interfaces.approval_repository import ApprovalRepository
from app.repositories.interfaces.report_repository import ReportRepository
from app.schemas.approval_api import ApprovalRevisionResponse

logger = get_logger(__name__)


class ApprovalService:
    """审批工作流的应用层编排。

    这个 service 只做状态机、版本快照和审计事件，不碰 RBAC、通知或外部工作流引擎。
    这样后续无论换成 PostgreSQL 还是接入权限系统，都能保持同一套 API contract。
    """

    def __init__(
        self,
        report_repository: ReportRepository,
        approval_repository: ApprovalRepository,
        event_publisher: EventPublisher,
    ) -> None:
        """注入报告仓库、审批仓库和事件发布器。"""

        self._report_repository = report_repository
        self._approval_repository = approval_repository
        self._event_publisher = event_publisher

    def submit_approval(self, task_id: str, comment: str | None = None) -> ApprovalRequest:
        """把当前 report 快照冻结成待审版本。"""

        try:
            report = self._get_report(task_id)
            self._ensure_submit_allowed(report)
            latest_version = self._approval_repository.get_latest_report_version(task_id)
            version = self._create_version_snapshot(
                task_id=task_id,
                markdown=report.markdown,
                status=ReportStatus.PENDING_APPROVAL,
                revision_reason=comment,
                previous_version=latest_version,
            )
            approval = ApprovalRequest(
                task_id=task_id,
                report_version_id=version.id,
                status=ReportStatus.PENDING_APPROVAL,
                requested_by="system",
                revision_no=version.version_no,
                revised_from_version_id=version.revised_from_version_id,
            )
            self._approval_repository.save_report_version(version)
            self._approval_repository.save_approval_request(approval)
            self._report_repository.save(replace(report, status=ReportStatus.PENDING_APPROVAL))
            self._record_event(
                task_id=task_id,
                approval_id=approval.id,
                event_type="approval.submitted",
                message="Approval submitted",
                actor_id="system",
                reason=comment,
                extra={
                    "approval_id": approval.id,
                    "report_version_id": version.id,
                    "revision_no": version.version_no,
                    "status": approval.status.value,
                },
            )
            return approval
        except AppException as exc:
            self._record_failed_event(task_id=task_id, approval_id=task_id, exc=exc)
            raise

    def list_approvals(
        self,
        *,
        task_id: str | None = None,
        status: ReportStatus | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> list[ApprovalRequest]:
        """列出审批记录，cursor 先保留为兼容占位。"""

        approvals = self._approval_repository.list_approval_requests(task_id=task_id, status=status)
        if cursor:
            approvals = [approval for approval in approvals if approval.id > cursor]
        if limit is not None:
            approvals = approvals[:limit]
        return approvals

    def get_approval(self, approval_id: str) -> ApprovalRequest:
        """读取单条审批记录。"""

        approval = self._approval_repository.get_approval_request(approval_id)
        if approval is None:
            raise ApprovalNotFoundException(approval_id)
        return approval

    def approve(self, approval_id: str, comment: str | None = None) -> ApprovalRequest:
        """批准待审版本，并把当前 report 推进到 approved。"""

        try:
            approval = self.get_approval(approval_id)
            report = self._get_report(approval.task_id)
            self._ensure_decision_allowed(approval, report, ReportStatus.APPROVED)
            decided = replace(
                approval,
                status=ReportStatus.APPROVED,
                approver_id="system",
                decision_at=utc_now(),
                decision_reason=comment,
            )
            self._approval_repository.save_approval_request(decided)
            self._report_repository.save(replace(report, status=ReportStatus.APPROVED))
            self._record_event(
                task_id=approval.task_id,
                approval_id=approval.id,
                event_type="approval.approved",
                message="Approval approved",
                actor_id="system",
                reason=comment,
                extra={
                    "approval_id": approval.id,
                    "report_version_id": approval.report_version_id,
                    "status": decided.status.value,
                },
            )
            return decided
        except AppException as exc:
            self._record_failed_event(self._approval_task_id(approval_id), approval_id, exc)
            raise

    def reject(self, approval_id: str, reason: str | None = None) -> ApprovalRequest:
        """拒绝待审版本，并保留拒绝原因。"""

        try:
            if reason is None or not reason.strip():
                raise MissingRejectionReasonException(approval_id)

            approval = self.get_approval(approval_id)
            report = self._get_report(approval.task_id)
            self._ensure_decision_allowed(approval, report, ReportStatus.REJECTED)
            decided = replace(
                approval,
                status=ReportStatus.REJECTED,
                approver_id="system",
                decision_at=utc_now(),
                decision_reason=reason.strip(),
            )
            self._approval_repository.save_approval_request(decided)
            self._report_repository.save(replace(report, status=ReportStatus.REJECTED))
            self._record_event(
                task_id=approval.task_id,
                approval_id=approval.id,
                event_type="approval.rejected",
                message="Approval rejected",
                actor_id="system",
                reason=reason.strip(),
                extra={
                    "approval_id": approval.id,
                    "report_version_id": approval.report_version_id,
                    "status": decided.status.value,
                },
            )
            return decided
        except AppException as exc:
            self._record_failed_event(self._approval_task_id(approval_id), approval_id, exc)
            raise

    def revise(self, task_id: str, revision_reason: str | None = None) -> ApprovalRevisionResponse:
        """基于 rejected report 创建新的不可变修订版本。"""

        try:
            report = self._get_report(task_id)
            if report.status != ReportStatus.REJECTED:
                raise ReportRevisionConflictException(task_id, report.status.value)

            latest_approval = self._get_latest_approval(task_id)
            if latest_approval is None or latest_approval.status != ReportStatus.REJECTED:
                raise ReportRevisionConflictException(task_id, report.status.value)

            latest_version = self._approval_repository.get_latest_report_version(task_id)
            version = self._create_version_snapshot(
                task_id=task_id,
                markdown=report.markdown,
                status=ReportStatus.REVISED,
                revision_reason=revision_reason,
                previous_version=latest_version,
            )
            self._approval_repository.save_report_version(version)
            self._report_repository.save(replace(report, status=ReportStatus.REVISED))
            self._record_event(
                task_id=task_id,
                approval_id=latest_approval.id,
                event_type="approval.revised",
                message="Approval revised",
                actor_id="system",
                reason=revision_reason,
                extra={
                    "approval_id": latest_approval.id,
                    "report_version_id": version.id,
                    "revision_no": version.version_no,
                    "revised_from_version_id": version.revised_from_version_id,
                    "status": version.status.value,
                },
            )
            return ApprovalRevisionResponse.from_domain(version)
        except AppException as exc:
            self._record_failed_event(task_id=task_id, approval_id=self._approval_task_id(task_id), exc=exc)
            raise

    def _get_report(self, task_id: str) -> Report:
        """读取当前报告，缺失时返回冻结错误码。"""

        report = self._report_repository.get(task_id)
        if report is None:
            raise ApprovalReportNotFoundException(task_id)
        return report

    def _get_latest_approval(self, task_id: str) -> ApprovalRequest | None:
        """按时间顺序取最新审批记录。"""

        approvals = self._approval_repository.list_approval_requests(task_id=task_id)
        return approvals[-1] if approvals else None

    def _ensure_submit_allowed(self, report: Report) -> None:
        """冻结 submit-approval 的状态边界。"""

        if report.status == ReportStatus.PENDING_APPROVAL:
            raise ApprovalAlreadySubmittedException(report.task_id)
        if report.status in {ReportStatus.APPROVED, ReportStatus.REJECTED, ReportStatus.PUBLISHED, ReportStatus.ARCHIVED}:
            raise InvalidApprovalStateException(report.task_id, report.status.value, ReportStatus.PENDING_APPROVAL.value)

    def _ensure_decision_allowed(
        self,
        approval: ApprovalRequest,
        report: Report,
        target_status: ReportStatus,
    ) -> None:
        """冻结 approve / reject 的状态边界。"""

        if approval.status != ReportStatus.PENDING_APPROVAL:
            raise ApprovalAlreadyDecidedException(approval.id, approval.status.value)
        if report.status != ReportStatus.PENDING_APPROVAL:
            raise InvalidApprovalStateException(approval.id, report.status.value, target_status.value)

    def _create_version_snapshot(
        self,
        *,
        task_id: str,
        markdown: str,
        status: ReportStatus,
        revision_reason: str | None,
        previous_version: ReportVersion | None,
    ) -> ReportVersion:
        """创建新的不可变报告版本快照。"""

        version_no = 1 if previous_version is None else previous_version.version_no + 1
        return ReportVersion(
            task_id=task_id,
            version_no=version_no,
            markdown=markdown,
            status=status,
            revision_reason=revision_reason,
            revised_from_version_id=previous_version.id if previous_version is not None else None,
            created_by="system",
        )

    def _record_event(
        self,
        *,
        task_id: str,
        approval_id: str,
        event_type: str,
        message: str,
        actor_id: str | None,
        reason: str | None = None,
        extra: dict[str, object] | None = None,
    ) -> ApprovalEvent:
        """把 approval 事件同时写入审计仓库和任务事件流。"""

        event = ApprovalEvent(
            approval_id=approval_id,
            task_id=task_id,
            event_type=event_type,
            actor_id=actor_id,
            reason=reason,
        )
        self._approval_repository.save_approval_event(event)
        log_event(
            logger,
            "info",
            event_type.replace(".", "_"),
            message,
            task_id=task_id,
            error_code=(extra or {}).get("error_code"),
            status=event_type.split(".")[-1],
        )
        self._event_publisher.publish(
            task_id,
            event_type,
            message,
            {
                "approval_id": approval_id,
                "task_id": task_id,
                "actor_id": actor_id,
                "reason": reason,
                **(extra or {}),
            },
        )
        return event

    def _record_failed_event(self, task_id: str, approval_id: str, exc: AppException) -> None:
        """把失败也记录成 approval.failed，便于审计和回放。"""

        self._record_event(
            task_id=task_id,
            approval_id=approval_id,
            event_type="approval.failed",
            message="Approval failed",
            actor_id="system",
            reason=exc.error_code.value,
            extra={
                "error_code": exc.error_code.value,
                "message": exc.message,
            },
        )

    def _approval_task_id(self, approval_id: str) -> str:
        """尽量从审批记录恢复 task_id，失败时回退到 approval_id。"""

        approval = self._approval_repository.get_approval_request(approval_id)
        if approval is None:
            return approval_id
        return approval.task_id


__all__ = ["ApprovalService"]
