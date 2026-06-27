from datetime import datetime

from pydantic import BaseModel

from app.models.report import Report


class ReportResponse(BaseModel):
    """定义最终报告的 HTTP 响应合同。"""

    task_id: str
    markdown: str
    provider: str
    created_at: datetime

    @classmethod
    def from_domain(cls, report: Report) -> "ReportResponse":
        """把领域报告转换为可序列化 API Schema。"""

        return cls(
            task_id=report.task_id,
            markdown=report.markdown,
            provider=report.provider,
            created_at=report.created_at,
        )
