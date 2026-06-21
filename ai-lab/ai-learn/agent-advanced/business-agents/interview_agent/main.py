from __future__ import annotations

import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared.core import Result, run_guarded

RUBRIC = {"situation": 1, "task": 1, "action": 2, "result": 2, "metric": 2, "reflection": 2}


def coach(answer: str) -> Result:
    lower = answer.lower()
    hits = {key: weight for key, weight in RUBRIC.items() if key in lower}
    missing = [key for key in RUBRIC if key not in hits]
    score = sum(hits.values())
    return Result("completed", f"STAR 回答得分 {score}/10", {"score": score, "missing": missing, "next_question": "你如何量化结果并说明复盘？"})


def main() -> None:
    p=argparse.ArgumentParser(); p.add_argument("answer", nargs="?", default="situation task action result metric"); a=p.parse_args()
    print(json.dumps(run_guarded("interview", "coach", lambda: coach(a.answer)).to_dict(), ensure_ascii=False, indent=2))
if __name__ == "__main__": main()
