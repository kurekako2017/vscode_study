"""日本 SES 人员匹配示例：使用本地规则筛选候选人，不调用大模型。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared.core import Result, run_guarded

# 内置数据用于演示；生产系统通常从 CRM 或人员数据库读取。
ENGINEERS = [
    {"name": "A", "skills": {"java", "spring", "aws"}, "japanese": 3, "rate": 70, "available": True},
    {"name": "B", "skills": {"python", "langgraph", "rag"}, "japanese": 2, "rate": 80, "available": True},
    {"name": "C", "skills": {"react", "typescript"}, "japanese": 3, "rate": 65, "available": False},
]


def match(skills: set[str], min_japanese: int, max_rate: int) -> Result:
    """按技能交集、日语等级、单价和可用状态筛选工程师。这里不调用 LLM。"""
    ranked = []
    for engineer in ENGINEERS:
        # 先应用必须满足的硬条件，不满足时直接跳过该候选人。
        if not engineer["available"] or engineer["japanese"] < min_japanese or engineer["rate"] > max_rate:
            continue
        overlap = len(skills & engineer["skills"])
        if overlap == 0:
            continue
        # 技能命中是主要权重，日语等级作为次要排序依据。
        ranked.append({
            "name": engineer["name"],
            "score": overlap * 10 + engineer["japanese"],
            "matched": sorted(skills & engineer["skills"]),
            "rate": engineer["rate"],
        })
    ranked.sort(key=lambda item: item["score"], reverse=True)
    return Result("proposal", f"找到 {len(ranked)} 位候选人", {"candidates": ranked}, requires_approval=True)


def main() -> None:
    """读取案件条件，执行受审计保护的匹配动作并打印 JSON。"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--skills", default="python,rag")
    parser.add_argument("--japanese", type=int, default=2)
    parser.add_argument("--max-rate", type=int, default=85)
    args = parser.parse_args()
    print("MODEL: provider=local model=none mode=rule-based", file=sys.stderr)
    requested_skills = set(args.skills.lower().split(","))
    result = run_guarded(
        "ses-sales",
        "match",
        lambda: match(requested_skills, args.japanese, args.max_rate),
    )
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
