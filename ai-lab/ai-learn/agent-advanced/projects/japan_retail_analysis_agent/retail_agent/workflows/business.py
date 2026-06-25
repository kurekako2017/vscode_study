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
    """Deterministic data path: route question to safe templates and fixed charts.

    它模拟企业经营问数链路：业务问题 -> 指标模板 -> 只读 SQL -> 结果证据。
    这里故意不让 Agent 自由写 SQL，因为 KPI 口径必须稳定、可复查。
    """

    def __init__(self, warehouse: RetailDataWarehouse) -> None:
        self.warehouse = warehouse

    def run(self, state: AnalysisState) -> AnalysisState:
        """Select safe query templates, execute them, and append data evidence blocks."""
        state.audit.append(AuditEvent("fixed_workflow.start", "system", "Use white-listed SQL templates."))
        templates = self._select_templates(state.question)
        for name in templates:
            # query_template 返回规范化 SQL 和 sqlite row；SQL 本身也写入 audit，方便复盘。
            sql, rows = self.warehouse.query_template(name)
            state.audit.append(AuditEvent("fixed_workflow.sql", "data-workflow", f"{name}: {sql}"))
            state.data_blocks.append(self._block_from_rows(name, rows))
        if not state.data_blocks:
            # 教学项目一般会 fallback 到默认模板；这里保留风险提示，说明没有命中明确数据意图。
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
        # 这些关键词是“意图路由”的最小版本。生产系统会参考指标目录、同义词库和权限。
        if any(key in question for key in ["売上", "売上高", "粗利", "業績"]) or "sales" in lower:
            selected.extend(["monthly_sales", "region_sales"])
        if any(key in question for key in ["在庫", "欠品", "補充"]) or "inventory" in lower:
            selected.append("inventory_risk")
        if any(key in question for key in ["カテゴリ", "商品", "品目"]):
            selected.append("category_sales")
        if not selected:
            # 默认给一个数据概览，避免初学者输入宽泛问题时没有任何结果。
            selected = ["monthly_sales", "inventory_risk"]
        # dict.fromkeys 用来去重并保持原顺序，避免同一个模板重复执行。
        return list(dict.fromkeys(selected))

    def _block_from_rows(self, template_name: str, rows: list[sqlite3.Row]) -> EvidenceBlock:
        """Convert SQL rows into a report/frontend friendly evidence block."""
        template = QUERY_TEMPLATES[template_name]
        # ReportComposer 不直接认识 sqlite3.Row，所以这里先转成 Markdown table。
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
