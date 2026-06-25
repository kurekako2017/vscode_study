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
    """A traceable source used by data and research evidence.

    初学者要关注 `locator`：它不是展示用标题，而是以后追溯证据时能定位
    到 CSV、数据库表、搜索结果 URL 或企业 Wiki 页面的字段。
    """

    title: str
    source_type: str
    locator: str
    retrieved_at: str


@dataclass(frozen=True)
class EvidenceBlock:
    """One reportable piece of evidence.

    data workflow 和 research agent 都输出这个结构，所以 ReportComposer 不关心来源类型。
    这就是 Agent 项目里常见的“统一证据合同”：上游怎么查不重要，下游只读同一种结构。
    """

    title: str
    content: str
    sources: list[Source]
    chart_kind: ChartKind
    use_fixed_chart: bool
    rationale: str


@dataclass
class AuditEvent:
    """Audit log entry appended during orchestration.

    审计日志记录“谁在什么步骤做了什么”。真实系统会继续补 user_id、
    request_id、tenant_id、tool_call_id，方便排查误答和权限问题。
    """

    step: str
    actor: str
    detail: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class AnalysisState:
    """LangGraph state payload.

    StateGraph 实际传递 `{"analysis": AnalysisState}`，这个对象保存所有节点累计结果。
    每个节点不要返回零散变量，而是把新增结果写回这个 state，再交给下一条边。
    """

    question: str
    mode: AnalysisMode = "hybrid"
    # 固定经营问数工作流产出的证据，例如月次销售、地域销售、库存风险。
    data_blocks: list[EvidenceBlock] = field(default_factory=list)
    # 自主研究 Agent 产出的证据，例如市场趋势、竞品观察、社内规则。
    research_blocks: list[EvidenceBlock] = field(default_factory=list)
    # 给经营报告使用的风险提示，既可以来自数据，也可以来自研究结论。
    risks: list[str] = field(default_factory=list)
    # 当前只是记录人工确认事项；生产版可升级为 LangGraph interrupt/resume。
    human_confirmation: list[str] = field(default_factory=list)
    # 全流程审计日志，用来解释 Agent 为什么得出这个报告。
    audit: list[AuditEvent] = field(default_factory=list)
    # 最终给前端、CLI 或文件输出的 Markdown 报告正文。
    report_markdown: str = ""


@dataclass(frozen=True)
class QueryTemplate:
    """Whitelisted SQL template metadata.

    它把“指标名、SQL、图表类型、来源文件”绑在一起，模拟企业 BI
    semantic layer。调用方只能选择模板名，不能自由传 SQL。
    """

    name: str
    title: str
    sql: str
    chart_kind: ChartKind
    source_file: str


@dataclass(frozen=True)
class ResearchPlan:
    """Research agent plan: goal, selected tools, and reason.

    这里的 plan 是教学版规则结果；真实 Agent 可由 LLM 生成，但仍然需要
    工具白名单、预算、最大调用次数和权限校验。
    """

    goal: str
    tool_names: list[str]
    reason: str
