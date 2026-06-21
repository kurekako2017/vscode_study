"""代码审查 Agent 示例：用本地规则生成 review 草稿，不执行 push 或 merge。"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared.core import Result, run_guarded


def review(diff: str) -> Result:
    """用两条可读的安全规则扫描 diff，并生成待人工批准的 review 草稿。"""
    findings = []
    # 第一条规则检查常见密钥变量被直接赋值的情况。
    if re.search(r"(?i)(api[_-]?key|password)\s*=", diff):
        findings.append({"severity": "high", "issue": "疑似硬编码密钥"})
    if "except Exception: pass" in diff:
        # 第二条规则检查异常被吞掉、导致故障不可观测的情况。
        findings.append({"severity": "medium", "issue": "异常被静默吞掉"})
    status = "blocked" if any(item["severity"] == "high" for item in findings) else "proposal"
    return Result(
        status,
        f"发现 {len(findings)} 个问题；仅生成 review 草稿，不自动 push/merge",
        {"findings": findings},
        requires_approval=True,
    )


def main() -> None:
    """读取 diff，运行本地审查规则并输出待审批的 review 结果。"""
    parser = argparse.ArgumentParser(description="本地规则版代码审查 Agent")
    parser.add_argument("diff", nargs="?", default="+ api_key = 'demo'")
    args = parser.parse_args()
    print("MODEL: provider=local model=none mode=rule-based", file=sys.stderr)
    result = run_guarded("coding-github", "review", lambda: review(args.diff))
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
