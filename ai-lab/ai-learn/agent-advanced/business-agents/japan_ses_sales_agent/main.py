from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared.core import Result, run_guarded

ENGINEERS = [
    {"name": "A", "skills": {"java", "spring", "aws"}, "japanese": 3, "rate": 70, "available": True},
    {"name": "B", "skills": {"python", "langgraph", "rag"}, "japanese": 2, "rate": 80, "available": True},
    {"name": "C", "skills": {"react", "typescript"}, "japanese": 3, "rate": 65, "available": False},
]


def match(skills: set[str], min_japanese: int, max_rate: int) -> Result:
    ranked = []
    for engineer in ENGINEERS:
        if not engineer["available"] or engineer["japanese"] < min_japanese or engineer["rate"] > max_rate:
            continue
        overlap = len(skills & engineer["skills"])
        if overlap == 0:
            continue
        ranked.append({"name": engineer["name"], "score": overlap * 10 + engineer["japanese"], "matched": sorted(skills & engineer["skills"]), "rate": engineer["rate"]})
    ranked.sort(key=lambda item: item["score"], reverse=True)
    return Result("proposal", f"找到 {len(ranked)} 位候选人", {"candidates": ranked}, requires_approval=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skills", default="python,rag")
    parser.add_argument("--japanese", type=int, default=2)
    parser.add_argument("--max-rate", type=int, default=85)
    args = parser.parse_args()
    result = run_guarded("ses-sales", "match", lambda: match(set(args.skills.lower().split(",")), args.japanese, args.max_rate))
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__": main()
