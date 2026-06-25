from __future__ import annotations

"""Research tools.

教学要点：
- 这些工具模拟外部搜索、竞品情报和社内 Wiki。
- 当前读取本地 Markdown，生产系统可替换为搜索 API、SharePoint、Confluence。
- 工具返回必须带 sources，报告才可审计。
"""

from pathlib import Path

from ..models import EvidenceBlock, Source
from ..settings import DATA_DIR
from ..utils import extract_section


class LocalResearchTools:
    """Offline tools that stand in for search, competitor intelligence, and wiki tools."""

    def __init__(self, notes_path: Path = DATA_DIR / "research_notes.md") -> None:
        self.notes_path = notes_path
        self.notes = notes_path.read_text(encoding="utf-8")

    def market_trend_search(self, _: str) -> EvidenceBlock:
        """Tool: retrieve market trend notes."""
        content = extract_section(self.notes, "市場トレンド")
        return self._research_block("市場トレンド調査", content, "market_trend_search")

    def competitor_search(self, _: str) -> EvidenceBlock:
        """Tool: retrieve competitor observation notes."""
        content = extract_section(self.notes, "競合観察")
        return self._research_block("競合観察", content, "competitor_search")

    def internal_policy_search(self, _: str) -> EvidenceBlock:
        """Tool: retrieve internal reporting and approval rules."""
        content = extract_section(self.notes, "社内資料")
        return self._research_block("社内確認ルール", content, "internal_policy_search")

    def _research_block(self, title: str, content: str, locator: str) -> EvidenceBlock:
        """Normalize research output into an EvidenceBlock."""
        return EvidenceBlock(
            title=title,
            content=content,
            sources=[
                Source(
                    title="Local research snapshot",
                    source_type="markdown",
                    locator=f"data/research_notes.md#{locator}",
                    retrieved_at="2026-06-30",
                )
            ],
            chart_kind="agent_report_section",
            use_fixed_chart=False,
            rationale="市場・競合・社内資料の調査は問いにより必要ソースが変わるため、Agent が計画してツールを選ぶ。",
        )
