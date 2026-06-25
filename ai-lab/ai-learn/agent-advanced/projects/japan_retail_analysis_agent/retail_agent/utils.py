from __future__ import annotations

from typing import Any

from .models import EvidenceBlock


def format_table(rows: list[dict[str, Any]]) -> str:
    """Render query rows as a Markdown table for reports and CLI output."""
    if not rows:
        return "_no rows_"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def extract_section(markdown: str, heading: str) -> str:
    """Extract one `## heading` section from a local research snapshot."""
    marker = f"## {heading}"
    if marker not in markdown:
        # 找不到标题时返回全文，保证工具仍能产出可读内容。
        return markdown.strip()
    after = markdown.split(marker, 1)[1]
    next_heading = after.find("\n## ")
    section = after[:next_heading] if next_heading >= 0 else after
    return section.strip()


def render_blocks(blocks: list[EvidenceBlock]) -> list[str]:
    """Render EvidenceBlock objects into report sections.

    ReportComposer 只需要调用这个函数，不需要知道 evidence 来自 SQL 还是研究工具。
    """
    lines: list[str] = []
    for block in blocks:
        lines.extend(
            [
                f"### {block.title}",
                "",
                f"- 表示方式: `{block.chart_kind}`",
                f"- 固定図を使うか: {'はい' if block.use_fixed_chart else 'いいえ'}",
                f"- 判断理由: {block.rationale}",
                "",
                block.content,
                "",
                "出典:",
            ]
        )
        for source in block.sources:
            lines.append(
                f"- {source.title} ({source.source_type}, {source.locator}, "
                f"retrieved_at={source.retrieved_at})"
            )
        lines.append("")
    return lines
