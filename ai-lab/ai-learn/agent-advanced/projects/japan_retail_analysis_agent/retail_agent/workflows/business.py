from __future__ import annotations

"""Deterministic business workflow.

教学要点：
- 经营 KPI 查询不要让 Agent 自由生成任意 SQL。
- 本层把用户问题映射到白名单 QueryTemplate，再由 warehouse 执行。
- 输出 EvidenceBlock，供前端和报告统一展示。
"""

import sqlite3

from ..data.templates import QUERY_TEMPLATES
from ..data.warehouse import RetailDataWarehouse
from ..models import AnalysisState, AuditEvent, EvidenceBlock, Source
from ..utils import format_table


class FixedBusinessWorkflow:
    """Deterministic data path: route question to safe templates and fixed charts."""

    def __init__(self, warehouse: RetailDataWarehouse) -> None:
        self.warehouse = warehouse

    def run(self, state: AnalysisState) -> AnalysisState:
        """Select safe query templates, execute them, and append data evidence blocks."""
        state.audit.append(AuditEvent("fixed_workflow.start", "system", "Use white-listed SQL templates."))
        templates = self._select_templates(state.question)
        for name in templates:
            sql, rows = self.warehouse.query_template(name)
            state.audit.append(AuditEvent("fixed_workflow.sql", "data-workflow", f"{name}: {sql}"))
            state.data_blocks.append(self._block_from_rows(name, rows))
        if not state.data_blocks:
            state.risks.append("構造化データに該当する質問が検出されませんでした。")
        return state

    def _select_templates(self, question: str) -> list[str]:
        """Map Japanese business terms to query templates.

        生产系统可替换为：
        - metadata search
        - schema linking
        - metric catalog
        - LLM-assisted but policy-guarded routing
        """

        lower = question.lower()
        selected: list[str] = []
        if any(key in question for key in ["売上", "売上高", "粗利", "業績"]) or "sales" in lower:
            selected.extend(["monthly_sales", "region_sales"])
        if any(key in question for key in ["在庫", "欠品", "補充"]) or "inventory" in lower:
            selected.append("inventory_risk")
        if any(key in question for key in ["カテゴリ", "商品", "品目"]):
            selected.append("category_sales")
        if not selected:
            selected = ["monthly_sales", "inventory_risk"]
        return list(dict.fromkeys(selected))

    def _block_from_rows(self, template_name: str, rows: list[sqlite3.Row]) -> EvidenceBlock:
        """Convert SQL rows into a report/frontend friendly evidence block."""
        template = QUERY_TEMPLATES[template_name]
        content = format_table([dict(row) for row in rows])
        return EvidenceBlock(
            title=template.title,
            content=content,
            sources=[
                Source(
                    title=f"{template.name} query result",
                    source_type="sqlite",
                    locator=f"data/{template.source_file}",
                    retrieved_at="2026-06-30",
                )
            ],
            chart_kind=template.chart_kind,
            use_fixed_chart=True,
            rationale="経営 KPI は同じ定義で繰り返し確認するため、固定テンプレートと固定チャートで再現性を優先する。",
        )
