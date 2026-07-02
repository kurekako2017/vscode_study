from __future__ import annotations

from app.models.analysis import KPIResult, ResearchResult


class ReportGenerator:
    """把领域结果转换为稳定、可直接展示的 Markdown 报告。"""

    def generate(
        self,
        question: str,
        kpi_result: KPIResult | None,
        research_result: ResearchResult | None,
    ) -> str:
        """按实际存在的 KPI/Research 结果组装对应章节。"""

        # 使用列表逐段构建，比分散字符串拼接更容易调整模板和测试章节边界。
        lines = [
            "# Retail Insight AI 経営分析レポート ",
            "",
            "## 分析依頼",
            "",
            question,
            "",
        ]

        # 三种运行模式共享同一个生成器，因此两个结果都必须允许缺省。
        if kpi_result is not None:
            lines.extend(
                [
                    "## KPI サマリー",
                    "",
                    f"- 売上高: {kpi_result.sales_amount_jpy:,} 円",
                    f"- 粗利率: {kpi_result.gross_margin_rate:.1%}",
                    f"- 在庫回転率: {kpi_result.inventory_turnover:.1f}",
                    f"- アクティブ会員数: {kpi_result.active_members:,}",
                    f"- 販促効果: {kpi_result.promotion_lift_rate:.1%}",
                    f"- データバージョン: {kpi_result.data_version}",
                    f"- KPI ルールバージョン: {kpi_result.rule_version}",
                    "",
                ]
            )

        if research_result is not None:
            lines.extend(
                [
                    "## Research サマリー",
                    "",
                    research_result.summary,
                    "",
                    "## 出典",
                    "",
                    *[f"- {source}" for source in research_result.sources],
                    "",
                ]
            )

        lines.extend(
            [
                "## 確認事項",
                "",
                "- 本レポートは static provider とローカル固定データで生成されています。",
                "- 経営判断前に、対象期間と元データを確認してください。",
                "",
            ]
        )
        return "\n".join(lines)
