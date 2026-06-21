"""Office Agent 安全边界示例：只允许检索和创建草稿，不执行发送。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared.core import Result, run_guarded

# 允许列表是工具调用的第一层安全检查。
ALLOWED = {"search_documents", "create_draft"}


def office(tool: str, text: str) -> Result:
    """执行允许列表中的本地模拟工具，不会连接真实 Office，也不会调用 LLM。"""
    if tool not in ALLOWED:
        raise PermissionError(f"tool not allowed: {tool}")
    if tool == "search_documents":
        # 用关键词规则模拟文档检索，便于离线观察工具返回结构。
        return Result("completed", "检索完成", {"matches": ["费用申请需要经理审批"] if "费用" in text else []})
    # 创建草稿属于可逆操作，但仍标记为需要人工批准后才能发送。
    return Result("draft", "Office 内容已生成草稿，尚未发送", {"content": text}, requires_approval=True)


def main() -> None:
    """读取工具名和文本，通过安全包装器执行并输出审计结果。"""
    parser = argparse.ArgumentParser(description="演示 Office 工具允许列表与审批边界")
    parser.add_argument("tool", choices=sorted(ALLOWED))
    parser.add_argument("text")
    args = parser.parse_args()
    print("MODEL: provider=local model=none mode=rule-based", file=sys.stderr)
    result = run_guarded("mcp-office", args.tool, lambda: office(args.tool, args.text))
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
