"""把股票研究结果转换并保存为 Markdown 报告。"""

from __future__ import annotations

from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REPORTS_DIR = PROJECT_ROOT / "reports"


def build_markdown_report(
    stock_data: dict[str, Any], analysis: dict[str, Any]
) -> str:
    """根据股票数据和分析结果构造 Markdown 文本。"""

    risk_lines = "\n".join(f"- {item}" for item in analysis["risk_notes"])

    return f"""# 日本股票公开信息研究报告（Mock）

> 本报告仅用于编程学习与研究辅助，不构成任何投资建议。

## 基本信息

| 项目 | 内容 |
| --- | --- |
| 股票代码 | {stock_data['stock_code']} |
| 公司名称 | {stock_data['company_name']} |
| 行业 | {stock_data['industry']} |
| 模拟当前价格 | {stock_data['current_price']:.2f} 日元 |
| 模拟 PER | {stock_data['per']:.2f} |
| 模拟 PBR | {stock_data['pbr']:.2f} |
| 模拟股息率 | {stock_data['dividend_yield']:.2f}% |

## AI 总结（规则化 Mock）

{analysis['ai_summary']}

## 风险提示

{risk_lines}

## 数据来源说明

- 数据来源：项目内置 Mock 数据。
- 数据性质：固定教学样例，不是真实行情，也不会自动更新。
- 系统行为：不读取 `.env`，不访问证券账户，不执行交易。
- 使用边界：只输出研究辅助报告，不输出买入、卖出或强烈推荐等投资指令。
"""


def write_report(
    stock_data: dict[str, Any],
    analysis: dict[str, Any],
    reports_dir: Path = DEFAULT_REPORTS_DIR,
) -> Path:
    """创建报告目录并写入以股票代码命名的 Markdown 文件。"""

    reports_dir.mkdir(parents=True, exist_ok=True)
    report_path = reports_dir / f"{stock_data['stock_code']}_report.md"
    report_path.write_text(
        build_markdown_report(stock_data, analysis),
        encoding="utf-8",
    )
    return report_path
