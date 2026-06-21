from __future__ import annotations

import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared.core import Result, run_guarded

ALLOWED = {"search_documents", "create_draft"}


def office(tool: str, text: str) -> Result:
    if tool not in ALLOWED:
        raise PermissionError(f"tool not allowed: {tool}")
    if tool == "search_documents":
        return Result("completed", "检索完成", {"matches": ["费用申请需要经理审批"] if "费用" in text else []})
    return Result("draft", "Office 内容已生成草稿，尚未发送", {"content": text}, requires_approval=True)


def main() -> None:
    p=argparse.ArgumentParser(); p.add_argument("tool", choices=sorted(ALLOWED)); p.add_argument("text"); a=p.parse_args()
    print(json.dumps(run_guarded("mcp-office", a.tool, lambda: office(a.tool,a.text)).to_dict(), ensure_ascii=False, indent=2))
if __name__ == "__main__": main()
