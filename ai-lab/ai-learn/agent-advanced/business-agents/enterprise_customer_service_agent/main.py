"""多租户客服示例：先校验租户，再查询本地知识库，不调用大模型。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared.core import Result, run_guarded

# 每个知识条目同时保存答案和来源编号，避免返回无法追溯的答案。
KB = {
    "退款": ("标准退款在 5 个工作日内处理。", "KB-REFUND"),
    "密码": ("请使用自助重置页面，不要向客服提供密码。", "KB-SECURITY"),
}


def answer(question: str, tenant: str) -> Result:
    """先检查租户，再用关键词查本地知识库；找不到证据就转人工。"""
    if tenant not in {"acme", "globex"}:
        raise PermissionError("unknown tenant")
    for key, (text, source) in KB.items():
        if key in question:
            return Result("completed", text, {"source": source, "tenant": tenant})
    # 没有证据时不猜答案，直接进入人工处理路径。
    return Result("handoff", "知识库证据不足，已转人工", {"tenant": tenant}, requires_approval=False)


def main() -> None:
    """读取租户和问题，执行知识库回答或人工转接流程。"""
    parser = argparse.ArgumentParser(description="本地规则版企业客服 Agent")
    parser.add_argument("question")
    parser.add_argument("--tenant", default="acme")
    args = parser.parse_args()
    print("MODEL: provider=local model=none mode=rule-based", file=sys.stderr)
    result = run_guarded(
        "customer-service", "answer", lambda: answer(args.question, args.tenant)
    )
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
