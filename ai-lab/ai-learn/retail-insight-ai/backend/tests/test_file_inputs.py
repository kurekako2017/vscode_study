from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from app.agents.providers.static_research import StaticResearchProvider
from app.data_loaders import LocalBusinessDataLoader, LocalResearchDataLoader
from app.kpi.workflow import FixedKPIWorkflow
from app.models.analysis import ResearchResult
from app.reports.generator import ReportGenerator


class FileInputTest(unittest.TestCase):
    """验证 Phase 1 文件化输入的 KPI、Research 和混合报告路径。"""

    def test_kpi_workflow_reads_csv_and_calculates_metrics(self) -> None:
        workflow = FixedKPIWorkflow(data_loader=LocalBusinessDataLoader())

        result = workflow.run("売上を確認してください")

        self.assertEqual(result.sales_amount_jpy, 15_750_000)
        self.assertAlmostEqual(result.gross_margin_rate, 4_926_000 / 15_750_000)
        self.assertAlmostEqual(result.inventory_turnover, 12_900_000 / 2_930_000)
        self.assertEqual(result.active_members, 5)
        self.assertAlmostEqual(result.promotion_lift_rate, 462_000 / 3_200_000)
        self.assertEqual(
            result.data_version,
            "local-files:sales|inventory|members|promotions",
        )
        self.assertEqual(result.rule_version, "kpi-file-v1")

    def test_hybrid_report_contains_file_input_and_approval_reserve_notes(self) -> None:
        kpi_result = FixedKPIWorkflow(data_loader=LocalBusinessDataLoader()).run("分析してください")
        dataset = LocalResearchDataLoader().load_research_dataset()
        research_result = ResearchResult(
            summary=dataset.summary,
            sources=dataset.sources,
            provider="static",
            data_version=dataset.data_version,
        )

        markdown = ReportGenerator().generate(
            question="売上と市場をまとめて分析してください",
            kpi_result=kpi_result,
            research_result=research_result,
        )

        self.assertIn("## KPI サマリー", markdown)
        self.assertIn("15,750,000 円", markdown)
        self.assertIn("## Research サマリー", markdown)
        self.assertIn("local file input", markdown)
        self.assertIn("draft / pending_approval / approved / rejected / revised", markdown)

    def test_research_loader_rejects_missing_json_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            loader = LocalResearchDataLoader(research_dir=Path(temp_dir))
            with self.assertRaisesRegex(Exception, "Local data file is invalid"):
                loader.load_research_dataset()


class ResearchProviderFileInputTest(unittest.IsolatedAsyncioTestCase):
    """验证 StaticResearchProvider 通过本地 JSON 返回统一 ResearchResult。"""

    async def test_static_research_provider_reads_json_files(self) -> None:
        provider = StaticResearchProvider(data_loader=LocalResearchDataLoader())

        result = await provider.research("市場を調査してください")

        self.assertIn("Market Trend 2026-06", result.summary)
        self.assertIn("Competitor Summary 2026-06", result.summary)
        self.assertEqual(
            result.sources,
            [
                "local://research/competitor-summary-2026-06",
                "internal://sales/competitor-observation-2026-06",
                "local://research/market-trend-2026-06",
                "internal://planning/monthly-market-watch-2026-06",
            ],
        )
        self.assertEqual(
            result.data_version,
            "local-files:competitor_summary_2026_06|market_trend_2026_06",
        )


if __name__ == "__main__":
    unittest.main()
