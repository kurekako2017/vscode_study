from __future__ import annotations

"""Command-line interface.

教学要点：
- CLI 和 FastAPI 共用同一个 RetailAnalysisOrchestrator。
- 这能证明核心业务能力不依赖 Web 框架，便于测试和批处理。
"""

import argparse
from pathlib import Path

from .orchestration.orchestrator import RetailAnalysisOrchestrator


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for local learning runs."""
    parser = argparse.ArgumentParser(description="日本小売经营分析 Agent")
    parser.add_argument(
        "question",
        nargs="?",
        default="6月の売上・在庫リスクを確認し、市場トレンドと競合状況を踏まえて経営会議向けに報告してください。",
    )
    parser.add_argument("--mode", choices=["auto", "data", "research", "hybrid"], default="auto")
    parser.add_argument("--output", default="", help="Markdown report output path")
    parser.add_argument("--show-audit-only", action="store_true", help="Only print audit events")
    return parser.parse_args()


def main() -> None:
    """Run one analysis from terminal and print/report markdown."""
    print("MODEL: provider=local model=none mode=deterministic+agent-simulation")
    args = parse_args()
    orchestrator = RetailAnalysisOrchestrator()
    state = orchestrator.run(args.question, args.mode)
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(state.report_markdown, encoding="utf-8")
        print(f"REPORT: {output_path}")
    if args.show_audit_only:
        for event in state.audit:
            print(f"{event.timestamp} [{event.actor}] {event.step}: {event.detail}")
        return
    print(state.report_markdown)
