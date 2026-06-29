"""日本股票公开信息研究助手的命令行入口。"""

from __future__ import annotations

import argparse
import sys

from analyzer import analyze_stock
from fetcher import fetch_stock_data
from report_writer import write_report


def parse_args() -> argparse.Namespace:
    """读取用户输入的四位日本股票代码。"""

    parser = argparse.ArgumentParser(
        description="使用本地 Mock 数据生成日本股票研究辅助报告"
    )
    parser.add_argument("stock_code", help="四位股票代码，例如 7203")
    return parser.parse_args()


def main() -> int:
    """依次获取 Mock 数据、生成分析并写入 Markdown 报告。"""

    args = parse_args()

    try:
        stock_data = fetch_stock_data(args.stock_code)
        analysis = analyze_stock(stock_data)
        report_path = write_report(stock_data, analysis)
    except ValueError as exc:
        print(f"输入错误：{exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"报告写入失败：{exc}", file=sys.stderr)
        return 1

    print("报告生成成功（Mock 模式）。")
    print(f"输出文件：{report_path}")
    print("提示：本报告仅用于学习和研究辅助，不构成投资建议。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
