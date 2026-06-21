"""面试回答教练示例：按固定 STAR 评分表检查要素，不调用大模型。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared.core import Result, run_guarded

# 字典值是每个要素的分数，总分正好为 10。
RUBRIC = {"situation": 1, "task": 1, "action": 2, "result": 2, "metric": 2, "reflection": 2}


def coach(answer: str) -> Result:
    """用固定评分表检查回答包含哪些 STAR 要素。这里没有调用大模型。"""
    lower = answer.lower()
    # hits 保存已出现的要素及其分值；missing 保存下一轮需要补充的要素。
    hits = {key: weight for key, weight in RUBRIC.items() if key in lower}
    missing = [key for key in RUBRIC if key not in hits]
    score = sum(hits.values())
    return Result("completed", f"STAR 回答得分 {score}/10", {"score": score, "missing": missing, "next_question": "你如何量化结果并说明复盘？"})


def main() -> None:
    """读取面试回答，执行评分并以统一 Result JSON 输出。"""
    parser = argparse.ArgumentParser(description="用本地规则检查 STAR 面试回答")
    parser.add_argument("answer", nargs="?", default="situation task action result metric")
    args = parser.parse_args()
    print("MODEL: provider=local model=none mode=rule-based", file=sys.stderr)
    result = run_guarded("interview", "coach", lambda: coach(args.answer))
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
