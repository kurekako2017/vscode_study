from __future__ import annotations

"""HTTP request/response schemas.

教学要点：
- 内部 domain model 不直接暴露给 API。
- Pydantic schema 负责 HTTP 边界的类型和校验。
"""

from typing import Literal

from pydantic import BaseModel, Field


RunMode = Literal["auto", "data", "research", "hybrid"]


class CreateTaskRequest(BaseModel):
    """Request body for creating an analysis task.

    `question` 是业务用户输入；`mode` 决定走 data/research/hybrid，
    auto 则交给 Orchestrator 的规则路由。
    """

    question: str = Field(..., min_length=1)
    mode: RunMode = "auto"


class CreateTaskResponse(BaseModel):
    """Response returned immediately after task creation.

    后端不会等报告完成才返回。前端拿到 task_id 后，通过 sse_url 或
    websocket_url 继续订阅执行进度。
    """

    task_id: str
    status: str
    sse_url: str
    websocket_url: str


class TaskSummary(BaseModel):
    """Short task record for list endpoints.

    只包含列表页需要的字段，避免历史列表一次性传回大段 Markdown 报告。
    """

    task_id: str
    question: str
    mode: str
    status: str
    created_at: str
    updated_at: str

class TaskDetail(TaskSummary):
    """Full task detail including report and events."""

    report_markdown: str
    events: list[dict]
