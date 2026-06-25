from __future__ import annotations

"""Shared domain models.

教学要点：
- 这些 dataclass 是后端内部统一语言。
- Router、workflow、research、report 都围绕 AnalysisState 和 EvidenceBlock 协作。
- 生产系统可以拆成 domain/entity/value object，但教学项目保持集中便于阅读。
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal


AnalysisMode = Literal["data", "research", "hybrid"]
RunMode = Literal["auto", "data", "research", "hybrid"]
ChartKind = Literal["fixed_bar", "fixed_line", "fixed_table", "agent_report_section"]


@dataclass(frozen=True)
class Source:
    """A traceable source used by data and research evidence."""

    title: str
    source_type: str
    locator: str
    retrieved_at: str


@dataclass(frozen=True)
class EvidenceBlock:
    """One reportable piece of evidence.

    data workflow 和 research agent 都输出这个结构，所以 ReportComposer 不关心来源类型。
    """

    title: str
    content: str
    sources: list[Source]
    chart_kind: ChartKind
    use_fixed_chart: bool
    rationale: str


@dataclass
class AuditEvent:
    """Audit log entry appended during orchestration."""

    step: str
    actor: str
    detail: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class AnalysisState:
    """LangGraph state payload.

    StateGraph 实际传递 `{"analysis": AnalysisState}`，这个对象保存所有节点累计结果。
    """

    question: str
    mode: AnalysisMode = "hybrid"
    data_blocks: list[EvidenceBlock] = field(default_factory=list)
    research_blocks: list[EvidenceBlock] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    human_confirmation: list[str] = field(default_factory=list)
    audit: list[AuditEvent] = field(default_factory=list)
    report_markdown: str = ""


@dataclass(frozen=True)
class QueryTemplate:
    """Whitelisted SQL template metadata."""

    name: str
    title: str
    sql: str
    chart_kind: ChartKind
    source_file: str


@dataclass(frozen=True)
class ResearchPlan:
    """Research agent plan: goal, selected tools, and reason."""

    goal: str
    tool_names: list[str]
    reason: str
