"""ReportRepository 的单进程内存实现。"""

from __future__ import annotations

from copy import deepcopy
from threading import RLock

from app.models.report import Report


class InMemoryReportRepository:
    """线程安全的本地报告仓库，每个任务只保留一份最终报告。"""

    def __init__(self) -> None:
        """初始化报告映射和保护并发访问的进程内锁。"""

        self._reports: dict[str, Report] = {}
        self._lock = RLock()

    def save(self, report: Report) -> None:
        """保存报告深拷贝，隔离仓库与调用方对象。"""

        with self._lock:
            self._reports[report.task_id] = deepcopy(report)

    def get(self, task_id: str) -> Report | None:
        """返回报告深拷贝；任务尚无报告时返回 None。"""

        with self._lock:
            report = self._reports.get(task_id)
            return deepcopy(report) if report is not None else None
