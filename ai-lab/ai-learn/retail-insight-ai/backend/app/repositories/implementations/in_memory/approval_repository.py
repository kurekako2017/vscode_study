"""ApprovalRepository 的单进程内存实现。"""

from __future__ import annotations

from copy import deepcopy
from threading import RLock

from app.models.approval import ApprovalEvent, ApprovalRequest, ReportVersion
from app.models.report import ReportStatus


class InMemoryApprovalRepository:
    """线程安全的本地审批仓库，保存审批请求、事件和不可变报告版本。"""

    def __init__(self) -> None:
        """初始化审批请求、事件和报告版本容器。"""

        self._approval_requests: dict[str, ApprovalRequest] = {}
        self._approval_events: dict[str, list[ApprovalEvent]] = {}
        self._report_versions: dict[str, list[ReportVersion]] = {}
        self._report_versions_by_id: dict[str, ReportVersion] = {}
        self._lock = RLock()

    def save_report_version(self, version: ReportVersion) -> None:
        """保存不可变报告版本快照。"""

        with self._lock:
            self._report_versions.setdefault(version.task_id, [])
            existing = self._report_versions_by_id.get(version.id)
            if existing is None:
                self._report_versions[version.task_id].append(deepcopy(version))
            else:
                index = self._report_versions[version.task_id].index(existing)
                self._report_versions[version.task_id][index] = deepcopy(version)
            self._report_versions_by_id[version.id] = deepcopy(version)

    def get_report_version(self, version_id: str) -> ReportVersion | None:
        """按版本 ID 读取报告版本快照。"""

        with self._lock:
            version = self._report_versions_by_id.get(version_id)
            return deepcopy(version) if version is not None else None

    def list_report_versions(self, task_id: str) -> list[ReportVersion]:
        """按 task_id 读取报告版本列表。"""

        with self._lock:
            return [deepcopy(version) for version in self._report_versions.get(task_id, [])]

    def get_latest_report_version(self, task_id: str) -> ReportVersion | None:
        """读取指定 task_id 的最新报告版本。"""

        with self._lock:
            versions = self._report_versions.get(task_id, [])
            return deepcopy(versions[-1]) if versions else None

    def save_approval_request(self, request: ApprovalRequest) -> None:
        """创建或更新审批请求。"""

        with self._lock:
            self._approval_requests[request.id] = deepcopy(request)

    def get_approval_request(self, approval_id: str) -> ApprovalRequest | None:
        """按 approval_id 读取审批请求。"""

        with self._lock:
            request = self._approval_requests.get(approval_id)
            return deepcopy(request) if request is not None else None

    def list_approval_requests(
        self,
        *,
        task_id: str | None = None,
        status: ReportStatus | None = None,
    ) -> list[ApprovalRequest]:
        """按任务和状态过滤审批请求。"""

        with self._lock:
            items = list(self._approval_requests.values())
            if task_id is not None:
                items = [item for item in items if item.task_id == task_id]
            if status is not None:
                items = [item for item in items if item.status == status]
            items.sort(key=lambda item: (item.requested_at, item.id))
            return [deepcopy(item) for item in items]

    def save_approval_event(self, event: ApprovalEvent) -> None:
        """追加审批审计事件。"""

        with self._lock:
            events = self._approval_events.setdefault(event.approval_id, [])
            events.append(deepcopy(event))

    def list_approval_events(self, approval_id: str) -> list[ApprovalEvent]:
        """按 approval_id 读取审批事件。"""

        with self._lock:
            return [deepcopy(event) for event in self._approval_events.get(approval_id, [])]


__all__ = ["InMemoryApprovalRepository"]
