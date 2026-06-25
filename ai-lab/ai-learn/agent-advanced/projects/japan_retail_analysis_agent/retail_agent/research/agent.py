from __future__ import annotations

"""Research agent planner.

教学要点：
- 这里模拟“深度研搜”的 planning + tool selection。
- 当前用规则规划，便于离线学习；生产系统可替换为 LLM tool calling。
- 每个工具都必须返回 EvidenceBlock，保证来源、引用、展示方式一致。
"""

import json
from typing import Callable

from ..models import AnalysisState, AuditEvent, EvidenceBlock, ResearchPlan
from .tools import LocalResearchTools


class ResearchAgent:
    """Small autonomous agent simulator with planning and dynamic tool choice."""

    def __init__(self, tools: LocalResearchTools | None = None) -> None:
        self.toolkit = tools or LocalResearchTools()
        self.tools: dict[str, Callable[[str], EvidenceBlock]] = {
            "market_trend_search": self.toolkit.market_trend_search,
            "competitor_search": self.toolkit.competitor_search,
            "internal_policy_search": self.toolkit.internal_policy_search,
        }

    def run(self, state: AnalysisState) -> AnalysisState:
        """Plan tools, execute them, append research evidence blocks."""
        plan = self.plan(state.question)
        state.audit.append(
            AuditEvent(
                "research_agent.plan",
                "research-agent",
                json.dumps(
                    {"goal": plan.goal, "tools": plan.tool_names, "reason": plan.reason},
                    ensure_ascii=False,
                ),
            )
        )
        for tool_name in plan.tool_names:
            block = self.tools[tool_name](state.question)
            state.audit.append(AuditEvent("research_agent.tool", "research-agent", tool_name))
            state.research_blocks.append(block)
        return state

    def plan(self, question: str) -> ResearchPlan:
        """Create a minimal research plan from the user question.

        生产系统中，这一步会加入：
        - 工具权限
        - token/cost budget
        - max tool calls
        - prompt injection 防御
        """

        tool_names: list[str] = []
        reasons: list[str] = []
        if any(key in question for key in ["市場", "トレンド", "需要", "季節", "夏"]):
            tool_names.append("market_trend_search")
            reasons.append("市場・需要に関する問い")
        if any(key in question for key in ["競合", "競争", "他社", "コンビニ", "スーパー"]):
            tool_names.append("competitor_search")
            reasons.append("競合比較が必要")
        if any(key in question for key in ["報告", "会議", "確認", "稟議", "リスク"]):
            tool_names.append("internal_policy_search")
            reasons.append("社内確認ルールと報告要件が必要")
        if not tool_names:
            tool_names = ["market_trend_search", "internal_policy_search"]
            reasons.append("調査範囲が曖昧なため市場情報と社内ルールを確認")
        return ResearchPlan(
            goal="経営判断に必要な非構造化情報を収集する",
            tool_names=list(dict.fromkeys(tool_names)),
            reason="; ".join(reasons),
        )
