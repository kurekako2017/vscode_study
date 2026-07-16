"""ApprovalRepository 的 Protocol。

文件职责：
- 定义审批请求、审批事件和报告版本快照的持久化合同。
- 让 ApprovalService 不绑定内存实现或未来数据库实现。

谁会调用它：
- `backend/app/services/approval_service.py` 和 in-memory / future PostgreSQL repository。

它调用谁：
- 只依赖 approval 领域模型，不依赖 API 或 workflow。

输入是什么：
- ApprovalRequest、ApprovalEvent、ReportVersion、task_id、approval_id、report_version_id。

输出是什么：
- 审批请求、事件和版本快照的稳定领域对象，或者空值。

为什么需要这一层：
- 审批流程需要把“当前审批状态”和“历史版本快照”分开存储，避免后续 revision 覆盖已批准事实。

日本现场面试怎么讲：
- 这是 approval workflow 的事实层接口，先做内存实现，后续换成 PostgreSQL 只改 repository，不改 service。
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from app.models.approval import ApprovalEvent, ApprovalRequest, ReportVersion
from app.models.report import ReportStatus


@runtime_checkable
class ApprovalRepository(Protocol):
    """定义审批请求、事件和报告版本快照的 CRUD 合同。"""

    def save_report_version(self, version: ReportVersion) -> None:
        """保存不可变报告版本快照。"""

        ...

    def get_report_version(self, version_id: str) -> ReportVersion | None:
        """按版本 ID 读取报告版本快照。"""

        ...

    def list_report_versions(self, task_id: str) -> list[ReportVersion]:
        """按 task_id 读取报告版本快照列表。"""

        ...

    def get_latest_report_version(self, task_id: str) -> ReportVersion | None:
        """读取指定 task_id 的最新报告版本快照。"""

        ...

    def save_approval_request(self, request: ApprovalRequest) -> None:
        """创建或更新审批请求。"""

        ...

    def get_approval_request(self, approval_id: str) -> ApprovalRequest | None:
        """按 approval_id 读取审批请求。"""

        ...

    def list_approval_requests(
        self,
        *,
        task_id: str | None = None,
        status: ReportStatus | None = None,
    ) -> list[ApprovalRequest]:
        """按任务和状态过滤审批请求。"""

        ...

    def save_approval_event(self, event: ApprovalEvent) -> None:
        """追加审批审计事件。"""

        ...

    def list_approval_events(self, approval_id: str) -> list[ApprovalEvent]:
        """按 approval_id 读取审计事件。"""

        ...


@runtime_checkable
class EnterpriseApprovalRepository(Protocol):
    """PostgreSQL-only 并发与历史能力；InMemory 不需要实现。"""

    def lock_report(self, task_id: str) -> bool:
        """锁定报告审批作用域；资源不存在时返回 False。"""

        ...

    def get_approval_request_for_update(
        self, approval_id: str
    ) -> ApprovalRequest | None:
        """在当前事务内锁定审批请求，防止并发决定覆盖。"""

        ...

    def list_task_approval_events(self, task_id: str) -> list[ApprovalEvent]:
        """按任务读取跨多次提交的完整业务历史。"""

        ...


__all__ = ["ApprovalRepository", "EnterpriseApprovalRepository"]
