from typing import Protocol, runtime_checkable

from app.models.report import Report


@runtime_checkable
class ReportRepository(Protocol):
    """定义报告写入和按任务读取合同。"""

    def save(self, report: Report) -> None:
        """保存或替换指定任务的最终报告。"""

        ...

    def get(self, task_id: str) -> Report | None:
        """读取报告；尚未生成时返回 None。"""

        ...
