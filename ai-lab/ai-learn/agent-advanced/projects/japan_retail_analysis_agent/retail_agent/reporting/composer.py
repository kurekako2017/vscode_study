from __future__ import annotations

"""Report composition.

教学要点：
- Data workflow 和 Research Agent 都输出 EvidenceBlock。
- ReportComposer 只负责把 evidence、risk、HITL note 和 audit log 组织成日文报告。
- 生产系统可在这里输出 PDF、PowerPoint、Confluence 页面或稟議草稿。
"""

from ..models import AnalysisState, AuditEvent
from ..utils import render_blocks


class ReportComposer:
    """Convert accumulated state into a business-facing Japanese report."""

    def run(self, state: AnalysisState) -> AnalysisState:
        """Append confirmation notes, derive risks, and write final markdown."""
        state.audit.append(AuditEvent("report.compose", "report-composer", "Build Japanese management report."))
        # 当前项目没有真正的审批 UI，所以先把需要人工确认的事项写入报告。
        # 企业版可以把这些事项变成 LangGraph interrupt，等待经理审批后 resume。
        state.human_confirmation.extend(
            [
                "価格改定・仕入先変更・補充ルール変更はエリアマネージャー確認が必要。",
                "外部情報はローカル調査スナップショットであり、本番では検索日時とURLを保存する。",
            ]
        )
        state.risks.extend(self._derive_risks(state))
        state.report_markdown = self._compose(state)
        return state

    def _derive_risks(self, state: AnalysisState) -> list[str]:
        """Derive simple risks from evidence blocks."""
        risks = []
        # 教学版直接从表格文本里找“要補充”；生产版应使用结构化字段或规则引擎。
        inventory_text = "\n".join(block.content for block in state.data_blocks if "在庫" in block.title)
        if "要補充" in inventory_text:
            risks.append("在庫テーブルで「要補充」が検出されたため、欠品による機会損失リスクがある。")
        if not state.research_blocks:
            risks.append("市場・競合情報が不足しているため、施策判断は内部データに偏る。")
        return risks

    def _compose(self, state: AnalysisState) -> str:
        """Build the final report body."""
        # 用 list 收集每一段，最后 join，比反复字符串拼接更容易插入和调整章节。
        lines = [
            "# 日本小売 経営分析レポート",
            "",
            "## 質問",
            "",
            state.question,
            "",
            "## 実行モード",
            "",
            f"`{state.mode}`",
            "",
            "## 使い分け方",
            "",
            "| 領域 | 採用方式 | 理由 |",
            "| --- | --- | --- |",
            "| 売上・粗利・在庫 KPI | 固定 LangGraph 相当ワークフロー | SQL とチャートを固定し、再現性・監査性を優先 |",
            "| 市場・競合・社内資料調査 | 自主 Agent | 問いに応じて調査ツールと引用を選ぶ必要がある |",
            "",
            "## 構造化データ結果",
            "",
        ]
        lines.extend(render_blocks(state.data_blocks))
        lines.extend(["", "## 調査結果", ""])
        lines.extend(render_blocks(state.research_blocks))
        lines.extend(["", "## リスクと確認事項", ""])
        lines.extend([f"- {risk}" for risk in state.risks] or ["- 現時点で重大なリスクは検出されていない。"])
        lines.extend(["", "## 人工確認記録", ""])
        lines.extend([f"- {item}" for item in state.human_confirmation])
        lines.extend(["", "## 監査ログ", ""])
        lines.extend([f"- {event.timestamp} [{event.actor}] {event.step}: {event.detail}" for event in state.audit])
        return "\n".join(lines) + "\n"
