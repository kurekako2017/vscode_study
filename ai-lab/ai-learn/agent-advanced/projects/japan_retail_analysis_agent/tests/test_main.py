from __future__ import annotations

"""Business/orchestration unit tests.

教学要点：
- 测试不仅验证代码没坏，也说明系统边界。
- data 模式不能偷跑 research；research 模式不能偷跑 SQL。
- SQL guard 是经营问数系统最重要的安全边界之一。
"""

import sys
import unittest
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from retail_agent.data.sql_guard import assert_select_only  # noqa: E402
from retail_agent.data.warehouse import RetailDataWarehouse  # noqa: E402
from retail_agent.orchestration.orchestrator import RetailAnalysisOrchestrator  # noqa: E402


class RetailAnalysisAgentTest(unittest.TestCase):
    def test_hybrid_question_uses_data_and_research(self) -> None:
        """Hybrid mode should combine verifiable data and research evidence."""
        state = RetailAnalysisOrchestrator().run("売上と在庫を確認し、市場トレンドと競合を含めて報告")

        self.assertEqual(state.mode, "hybrid")
        self.assertTrue(state.data_blocks)
        self.assertTrue(state.research_blocks)
        self.assertIn("固定 LangGraph 相当ワークフロー", state.report_markdown)
        self.assertIn("自主 Agent", state.report_markdown)

    def test_read_only_templates_return_verifiable_rows(self) -> None:
        """Inventory template should return rows from controlled SQLite data."""
        warehouse = RetailDataWarehouse()
        sql, rows = warehouse.query_template("inventory_risk")

        self.assertTrue(sql.lower().startswith("select"))
        self.assertTrue(rows)
        self.assertTrue(any(row["risk_level"] == "要補充" for row in rows))

    def test_data_mode_does_not_run_research_agent(self) -> None:
        """Data mode demonstrates the fixed workflow boundary."""
        state = RetailAnalysisOrchestrator().run("6月の売上と在庫リスクを確認", "data")

        self.assertEqual(state.mode, "data")
        self.assertTrue(state.data_blocks)
        self.assertFalse(state.research_blocks)
        self.assertNotIn("research_agent.tool", "\n".join(event.step for event in state.audit))

    def test_research_mode_does_not_run_fixed_sql(self) -> None:
        """Research mode demonstrates the autonomous research boundary."""
        state = RetailAnalysisOrchestrator().run("市場トレンドと競合を調査して報告", "research")

        self.assertEqual(state.mode, "research")
        self.assertFalse(state.data_blocks)
        self.assertTrue(state.research_blocks)
        self.assertNotIn("fixed_workflow.sql", "\n".join(event.step for event in state.audit))

    def test_sql_guard_rejects_non_select(self) -> None:
        """Non-read SQL must be rejected before touching a real database."""
        with self.assertRaisesRegex(ValueError, "SELECT"):
            assert_select_only("DELETE FROM sales")


if __name__ == "__main__":
    unittest.main()
