from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.models.task import utc_now


@dataclass(frozen=True)
class Report:
    """保存最终 Markdown 报告及生成 Provider，不混入页面展示状态。"""

    task_id: str
    markdown: str
    provider: str
    created_at: datetime = field(default_factory=utc_now)
