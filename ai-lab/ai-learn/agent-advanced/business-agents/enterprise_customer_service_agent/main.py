from __future__ import annotations

import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared.core import Result, run_guarded

KB = {"退款": ("标准退款在 5 个工作日内处理。", "KB-REFUND"), "密码": ("请使用自助重置页面，不要向客服提供密码。", "KB-SECURITY")}


def answer(question: str, tenant: str) -> Result:
    if tenant not in {"acme", "globex"}: raise PermissionError("unknown tenant")
    for key,(text,source) in KB.items():
        if key in question: return Result("completed", text, {"source": source, "tenant": tenant})
    return Result("handoff", "知识库证据不足，已转人工", {"tenant": tenant}, requires_approval=False)


def main() -> None:
    p=argparse.ArgumentParser(); p.add_argument("question"); p.add_argument("--tenant",default="acme"); a=p.parse_args()
    print(json.dumps(run_guarded("customer-service","answer",lambda: answer(a.question,a.tenant)).to_dict(),ensure_ascii=False,indent=2))
if __name__ == "__main__": main()
