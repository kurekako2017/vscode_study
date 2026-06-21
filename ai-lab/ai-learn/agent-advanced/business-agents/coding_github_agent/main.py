from __future__ import annotations

import argparse, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared.core import Result, run_guarded


def review(diff: str) -> Result:
    findings=[]
    if re.search(r"(?i)(api[_-]?key|password)\s*=",diff): findings.append({"severity":"high","issue":"疑似硬编码密钥"})
    if "except Exception: pass" in diff: findings.append({"severity":"medium","issue":"异常被静默吞掉"})
    status="blocked" if any(x["severity"]=="high" for x in findings) else "proposal"
    return Result(status, f"发现 {len(findings)} 个问题；仅生成 review 草稿，不自动 push/merge", {"findings":findings}, requires_approval=True)


def main() -> None:
    p=argparse.ArgumentParser(); p.add_argument("diff",nargs="?",default="+ api_key = 'demo'"); a=p.parse_args()
    print(json.dumps(run_guarded("coding-github","review",lambda: review(a.diff)).to_dict(),ensure_ascii=False,indent=2))
if __name__ == "__main__": main()
