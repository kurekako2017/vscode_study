from __future__ import annotations

from typing import Literal, NotRequired, TypedDict


class WorkflowState(TypedDict):
    """LangGraph 节点共享状态；节点只返回自己产生的增量字段。"""

    question_id: str
    question: str
    request_id: str
    approval_decision: NotRequired[Literal["approved", "rejected"] | None]
    risk_level: NotRequired[Literal["LOW", "HIGH"]]
    status: NotRequired[str]
    report: NotRequired[str]

