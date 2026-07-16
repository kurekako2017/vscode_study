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
from app.repositories.interfaces.approval_repository import EnterpriseApprovalRepository
from app.repositories.interfaces.report_repository import ReportRepository
from app.repositories.interfaces.unit_of_work import UnitOfWork
from app.db.unit_of_work import InMemoryUnitOfWork
from app.schemas.approval_api import ApprovalRevisionResponse
from app.security.authorization_service import AuthorizationService
from app.security.contracts import CurrentUser
from app.security.errors import ForbiddenError
from app.security.rbac_contracts import Permission

logger = get_logger(__name__)


class ApprovalService:
    """审批工作流的应用层编排。

    这个 service 负责状态机、版本快照、业务历史和 ownership policy。
    API permission 仍由统一 Dependency 执行；Service 只做 PostgreSQL 企业路径的
    防御式权限校验，不解析 JWT，也不判断具体 role 字符串。
    """

    def __init__(
        self,
        report_repository: ReportRepository,
        approval_repository: ApprovalRepository,
        event_publisher: EventPublisher,
        unit_of_work: UnitOfWork | None = None,
        *,
        enterprise_repository: EnterpriseApprovalRepository | None = None,
        authorization_service: AuthorizationService | None = None,
    ) -> None:
        """注入报告仓库、审批仓库和事件发布器。"""

        self._report_repository = report_repository
        self._approval_repository = approval_repository
        self._event_publisher = event_publisher
        self._unit_of_work = unit_of_work or InMemoryUnitOfWork()
        # PostgreSQL-only 能力显式注入；InMemory 不需要扩展 Repository。
        self._enterprise_repository = enterprise_repository
        self._authorization_service = authorization_service

    def submit_approval(
        self,
        task_id: str,
        comment: str | None = None,
        *,
        current_user: CurrentUser | None = None,
    ) -> ApprovalRequest:
        """以单一事务提交版本、审批请求、报告状态和事件。"""

        self._require_permission(current_user, Permission.APPROVAL_SUBMIT)
        with self._unit_of_work.transaction():
            self._lock_report(task_id)
            return self._submit_approval(task_id, comment, current_user)

    def _submit_approval(
        self,
        task_id: str,
        comment: str | None,
        current_user: CurrentUser | None,
    ) -> ApprovalRequest:
        """把当前 report 快照冻结成待审版本。"""

        try:
            report = self._get_report(task_id)
            self._ensure_submit_allowed(report)
            actor_id, actor_username, actor_role = self._actor_identity(current_user)
            latest_version = self._approval_repository.get_latest_report_version(task_id)
            version = self._create_version_snapshot(
                task_id=task_id,
                markdown=report.markdown,
                status=ReportStatus.PENDING_APPROVAL,
                revision_reason=comment,
                previous_version=latest_version,
                created_by=actor_id,
            )
            approval = ApprovalRequest(
                task_id=task_id,
                report_version_id=version.id,
                status=ReportStatus.PENDING_APPROVAL,
                requested_by=actor_id,
                requested_by_username=actor_username,
                requested_by_role=actor_role,
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
                current_user=current_user,
                reason=comment,
                from_status=report.status,
                to_status=ReportStatus.PENDING_APPROVAL,
                report_version_id=version.id,
                extra={
                    "approval_id": approval.id,
                    "report_version_id": version.id,
                    "revision_no": version.version_no,
                    "status": approval.status.value,
                },
            )
            return approval
        except AppException as exc:
            self._record_failed_event(
                task_id=task_id,
                approval_id=task_id,
                exc=exc,
                current_user=current_user,
            )
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

    def get_approval_history(self, task_id: str) -> list[ApprovalEvent]:
        """PostgreSQL 返回跨轮次业务历史；InMemory 冻结路径保持空扩展。"""

        if self._enterprise_repository is None:
            return []
        return self._enterprise_repository.list_task_approval_events(task_id)

    def require_revision_access(
        self,
        task_id: str,
        current_user: CurrentUser,
    ) -> None:
        """集中执行 submitter ownership；approval.admin 可处理例外情况。"""

        if self._enterprise_repository is None:
            return
        self._require_permission(current_user, Permission.APPROVAL_SUBMIT)
        latest = self._get_latest_approval(task_id)
        if latest is None:
            return
        if latest.requested_by == current_user.user_id:
            return
        if self._authorization_service is not None:
            admin_result = self._authorization_service.check_permission(
                current_user,
                Permission.APPROVAL_ADMIN,
            )
            if admin_result.allowed:
                return
        raise ForbiddenError(
            permission=Permission.APPROVAL_SUBMIT.value,
            role=current_user.role,
        )

    def require_approval_read_access(
        self,
        approval_id: str,
        current_user: CurrentUser,
    ) -> str:
        """集中执行 reviewer-or-owner 的单资源读取策略。

        reviewer 直接通过 ``approval.review``；只有 PostgreSQL 企业路径允许
        拥有 ``approval.submit`` 的原 submitter 读取自己的 Approval/History。
        InMemory 不启用 owner 例外，从而保持冻结行为不扩展。
        """

        if self._authorization_service is None:
            raise ForbiddenError(
                permission=Permission.APPROVAL_REVIEW.value,
                role=current_user.role,
            )

        review_result = self._authorization_service.check_permission(
            current_user,
            Permission.APPROVAL_REVIEW,
        )
        if review_result.allowed:
            return Permission.APPROVAL_REVIEW.value

        submit_result = self._authorization_service.check_permission(
            current_user,
            Permission.APPROVAL_SUBMIT,
        )
        if submit_result.allowed and self._enterprise_repository is not None:
            approval = self._approval_repository.get_approval_request(approval_id)
            if approval is not None and approval.requested_by == current_user.user_id:
                return Permission.APPROVAL_SUBMIT.value

        raise ForbiddenError(
            permission=Permission.APPROVAL_REVIEW.value,
            role=current_user.role,
        )

    def approve(
        self,
        approval_id: str,
        comment: str | None = None,
        *,
        current_user: CurrentUser | None = None,
    ) -> ApprovalRequest:
        """以单一事务提交审批决定、报告状态和事件。"""

        self._require_permission(current_user, Permission.APPROVAL_REVIEW)
        with self._unit_of_work.transaction():
            return self._approve(approval_id, comment, current_user)

    def _approve(
        self,
        approval_id: str,
        comment: str | None,
        current_user: CurrentUser | None,
    ) -> ApprovalRequest:
        """批准待审版本，并把当前 report 推进到 approved。"""

        try:
            approval = self._get_approval_for_decision(approval_id)
            report = self._get_report(approval.task_id)
            self._ensure_decision_allowed(approval, report, ReportStatus.APPROVED)
            actor_id, actor_username, actor_role = self._actor_identity(current_user)
            decided = replace(
                approval,
                status=ReportStatus.APPROVED,
                approver_id=actor_id,
                approver_username=actor_username,
                approver_role=actor_role,
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
                current_user=current_user,
                reason=comment,
                from_status=ReportStatus.PENDING_APPROVAL,
                to_status=ReportStatus.APPROVED,
                report_version_id=approval.report_version_id,
                extra={
                    "approval_id": approval.id,
                    "report_version_id": approval.report_version_id,
                    "status": decided.status.value,
                },
            )
            return decided
        except AppException as exc:
            self._record_failed_event(
                self._approval_task_id(approval_id),
                approval_id,
                exc,
                current_user=current_user,
            )
            raise

    def reject(
        self,
        approval_id: str,
        reason: str | None = None,
        *,
        current_user: CurrentUser | None = None,
    ) -> ApprovalRequest:
        """以单一事务提交拒绝决定、原因、报告状态和事件。"""

        self._require_permission(current_user, Permission.APPROVAL_REVIEW)
        with self._unit_of_work.transaction():
            return self._reject(approval_id, reason, current_user)

    def _reject(
        self,
        approval_id: str,
        reason: str | None,
        current_user: CurrentUser | None,
    ) -> ApprovalRequest:
        """拒绝待审版本，并保留拒绝原因。"""

        try:
            if reason is None or not reason.strip():
                raise MissingRejectionReasonException(approval_id)

            approval = self._get_approval_for_decision(approval_id)
            report = self._get_report(approval.task_id)
            self._ensure_decision_allowed(approval, report, ReportStatus.REJECTED)
            actor_id, actor_username, actor_role = self._actor_identity(current_user)
            decided = replace(
                approval,
                status=ReportStatus.REJECTED,
                approver_id=actor_id,
                approver_username=actor_username,
                approver_role=actor_role,
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
                current_user=current_user,
                reason=reason.strip(),
                from_status=ReportStatus.PENDING_APPROVAL,
                to_status=ReportStatus.REJECTED,
                report_version_id=approval.report_version_id,
                extra={
                    "approval_id": approval.id,
                    "report_version_id": approval.report_version_id,
                    "status": decided.status.value,
                },
            )
            return decided
        except AppException as exc:
            self._record_failed_event(
                self._approval_task_id(approval_id),
                approval_id,
                exc,
                current_user=current_user,
            )
            raise

    def revise(
        self,
        task_id: str,
        revision_reason: str | None = None,
        *,
        markdown: str | None = None,
        current_user: CurrentUser | None = None,
    ) -> ApprovalRevisionResponse:
        """以单一事务提交修订版本、报告状态和事件。"""

        self._require_permission(current_user, Permission.APPROVAL_SUBMIT)
        with self._unit_of_work.transaction():
            self._lock_report(task_id)
            return self._revise(task_id, revision_reason, markdown, current_user)

    def _revise(
        self,
        task_id: str,
        revision_reason: str | None,
        markdown: str | None,
        current_user: CurrentUser | None,
    ) -> ApprovalRevisionResponse:
        """基于 rejected report 创建新的不可变修订版本。"""

        try:
            report = self._get_report(task_id)
            if report.status != ReportStatus.REJECTED:
                raise ReportRevisionConflictException(task_id, report.status.value)

            latest_approval = self._get_latest_approval(task_id)
            if latest_approval is None or latest_approval.status != ReportStatus.REJECTED:
                raise ReportRevisionConflictException(task_id, report.status.value)
            if current_user is not None:
                self.require_revision_access(task_id, current_user)

            latest_version = self._approval_repository.get_latest_report_version(task_id)
            revised_markdown = markdown if markdown is not None else report.markdown
            actor_id, _, _ = self._actor_identity(current_user)
            version = self._create_version_snapshot(
                task_id=task_id,
                markdown=revised_markdown,
                status=ReportStatus.REVISED,
                revision_reason=revision_reason,
                previous_version=latest_version,
                created_by=actor_id,
            )
            self._approval_repository.save_report_version(version)
            self._report_repository.save(
                replace(
                    report,
                    markdown=revised_markdown,
                    status=ReportStatus.REVISED,
                )
            )
            self._record_event(
                task_id=task_id,
                approval_id=latest_approval.id,
                event_type="approval.revised",
                message="Approval revised",
                current_user=current_user,
                reason=revision_reason,
                from_status=ReportStatus.REJECTED,
                to_status=ReportStatus.REVISED,
                report_version_id=version.id,
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
            self._record_failed_event(
                task_id=task_id,
                approval_id=self._approval_task_id(task_id),
                exc=exc,
                current_user=current_user,
            )
            raise

    def resubmit(
        self,
        task_id: str,
        comment: str | None = None,
        *,
        current_user: CurrentUser | None = None,
    ) -> ApprovalRequest:
        """把已修订版本重新送审；不再复制一份相同 ReportVersion。"""

        if self._enterprise_repository is None:
            raise InvalidApprovalStateException(
                task_id,
                ReportStatus.REVISED.value,
                ReportStatus.PENDING_APPROVAL.value,
            )
        self._require_permission(current_user, Permission.APPROVAL_SUBMIT)
        with self._unit_of_work.transaction():
            self._lock_report(task_id)
            return self._resubmit(task_id, comment, current_user)

    def _resubmit(
        self,
        task_id: str,
        comment: str | None,
        current_user: CurrentUser | None,
    ) -> ApprovalRequest:
        """重新使用 latest revised version 创建新的 pending ApprovalRequest。"""

        try:
            report = self._get_report(task_id)
            if report.status != ReportStatus.REVISED:
                raise InvalidApprovalStateException(
                    task_id,
                    report.status.value,
                    ReportStatus.PENDING_APPROVAL.value,
                )
            if current_user is not None:
                self.require_revision_access(task_id, current_user)
            latest_version = self._approval_repository.get_latest_report_version(task_id)
            if latest_version is None or latest_version.status != ReportStatus.REVISED:
                raise ReportRevisionConflictException(task_id, report.status.value)
            actor_id, actor_username, actor_role = self._actor_identity(current_user)
            approval = ApprovalRequest(
                task_id=task_id,
                report_version_id=latest_version.id,
                status=ReportStatus.PENDING_APPROVAL,
                requested_by=actor_id,
                requested_by_username=actor_username,
                requested_by_role=actor_role,
                revision_no=latest_version.version_no,
                revised_from_version_id=latest_version.revised_from_version_id,
            )
            self._approval_repository.save_approval_request(approval)
            self._report_repository.save(
                replace(report, status=ReportStatus.PENDING_APPROVAL)
            )
            self._record_event(
                task_id=task_id,
                approval_id=approval.id,
                event_type="approval.resubmitted",
                message="Approval resubmitted",
                current_user=current_user,
                reason=comment,
                from_status=ReportStatus.REVISED,
                to_status=ReportStatus.PENDING_APPROVAL,
                report_version_id=latest_version.id,
                extra={
                    "approval_id": approval.id,
                    "report_version_id": latest_version.id,
                    "revision_no": latest_version.version_no,
                    "status": approval.status.value,
                },
            )
            return approval
        except AppException as exc:
            self._record_failed_event(
                task_id=task_id,
                approval_id=self._approval_task_id(task_id),
                exc=exc,
                current_user=current_user,
            )
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
        if (
            self._enterprise_repository is not None
            and report.status == ReportStatus.REVISED
        ):
            raise InvalidApprovalStateException(
                report.task_id,
                report.status.value,
                ReportStatus.PENDING_APPROVAL.value,
            )
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
        created_by: str,
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
            created_by=created_by,
        )

    def _record_event(
        self,
        *,
        task_id: str,
        approval_id: str,
        event_type: str,
        message: str,
        current_user: CurrentUser | None,
        reason: str | None = None,
        from_status: ReportStatus | None = None,
        to_status: ReportStatus | None = None,
        report_version_id: str | None = None,
        extra: dict[str, object] | None = None,
    ) -> ApprovalEvent:
        """把 approval 事件同时写入审计仓库和任务事件流。"""

        actor_id, actor_username, actor_role = self._actor_identity(current_user)
        event = ApprovalEvent(
            approval_id=approval_id,
            task_id=task_id,
            event_type=event_type,
            actor_id=actor_id,
            reason=reason,
            from_status=from_status,
            to_status=to_status,
            actor_username=actor_username,
            actor_role=actor_role,
            report_version_id=report_version_id,
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
                "from_status": from_status.value if from_status is not None else None,
                "to_status": to_status.value if to_status is not None else None,
                "report_version_id": report_version_id,
                **(extra or {}),
            },
        )
        return event

    def _record_failed_event(
        self,
        task_id: str,
        approval_id: str,
        exc: AppException,
        *,
        current_user: CurrentUser | None,
    ) -> None:
        """把失败也记录成 approval.failed，便于审计和回放。"""

        actor_id, _, _ = self._actor_identity(current_user)
        # 申请尚未创建时不能写带外键的 ApprovalEvent，但通用事件流仍可记录失败。
        if self._approval_repository.get_approval_request(approval_id) is None:
            self._event_publisher.publish(
                task_id,
                "approval.failed",
                "Approval failed",
                {
                    "approval_id": approval_id,
                    "task_id": task_id,
                    "actor_id": actor_id,
                    "reason": exc.error_code.value,
                    "error_code": exc.error_code.value,
                    "message": exc.message,
                },
            )
            return
        self._record_event(
            task_id=task_id,
            approval_id=approval_id,
            event_type="approval.failed",
            message="Approval failed",
            current_user=current_user,
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

    def _lock_report(self, task_id: str) -> None:
        """PostgreSQL 用报告行锁串行化同一 task 的审批写操作。"""

        if self._enterprise_repository is not None:
            self._enterprise_repository.lock_report(task_id)

    def _get_approval_for_decision(self, approval_id: str) -> ApprovalRequest:
        """PostgreSQL 决策读取使用行锁；InMemory 保持原有读取。"""

        if self._enterprise_repository is None:
            return self.get_approval(approval_id)
        approval = self._enterprise_repository.get_approval_request_for_update(
            approval_id
        )
        if approval is None:
            raise ApprovalNotFoundException(approval_id)
        return approval

    def _actor_identity(
        self,
        current_user: CurrentUser | None,
    ) -> tuple[str, str | None, str | None]:
        """企业路径使用 JWT actor；InMemory 冻结路径继续使用 system。"""

        if self._enterprise_repository is not None and current_user is not None:
            return current_user.user_id, current_user.username, current_user.role
        return "system", None, None

    def _require_permission(
        self,
        current_user: CurrentUser | None,
        permission: Permission,
    ) -> None:
        """Service 侧防御式校验，未知角色继续 fail-closed。"""

        if self._enterprise_repository is None:
            return
        if current_user is None or self._authorization_service is None:
            raise ForbiddenError(
                permission=permission.value,
                role=current_user.role if current_user is not None else "unknown",
            )
        self._authorization_service.require_permission(current_user, permission)


__all__ = ["ApprovalService"]
