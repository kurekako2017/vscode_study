from __future__ import annotations

from typing import Literal, TypedDict

from app.models.analysis import KPIResult, ResearchResult


# 定义 LangGraph 节点共享的类型化状态；每个 Node 只更新自己负责的字段。
class AnalysisState(TypedDict, total=False):
    """LangGraph 节点共享的类型化状态；每个 Node 只更新自己负责的字段。"""

    task_id: str
    question: str
    mode: Literal["hybrid", "kpi", "research"]
    route: str
    kpi_result: KPIResult
    research_result: ResearchResult
    report_markdown: str
