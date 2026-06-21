"""真实 FastMCP Server：stdio 或 Streamable HTTP。"""
from __future__ import annotations

import argparse
import os
import sys

from mcp.server.fastmcp import FastMCP


PROFILE = os.getenv("MCP_PROFILE", "office")
# 同一份 server 代码通过 PROFILE 模拟不同业务域。
mcp = FastMCP(f"ai-lab-{PROFILE}", host="127.0.0.1", port=8765)


@mcp.tool()
def search_documents(query: str, limit: int = 3) -> list[dict[str, str]]:
    """在当前域的模拟文档中搜索；limit 必须在 1..10。"""
    if not 1 <= limit <= 10:
        raise ValueError("limit must be between 1 and 10")
    documents = {
        "office": ["费用申请需要经理审批", "会议室可通过 Office Portal 预约"],
        "engineering": ["PR 合并前需要 review", "发布失败时执行 rollback playbook"],
    }.get(PROFILE, ["通用知识库"])
    # 工具只返回当前 profile 的资料，模拟服务端的数据隔离。
    return [
        {"domain": PROFILE, "text": item}
        for item in documents
        if query.lower() in item.lower() or query in item
    ][:limit]


@mcp.tool()
def create_draft(title: str, content: str) -> dict[str, str]:
    """只创建草稿，不执行发送等有副作用操作。"""
    if not title.strip() or not content.strip():
        raise ValueError("title and content are required")
    return {"status": "draft", "domain": PROFILE, "title": title, "content": content}


def main() -> None:
    """选择 stdio 或 HTTP transport 并启动 MCP server。"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--transport", choices=["stdio", "streamable-http"], default="stdio")
    args = parser.parse_args()
    # MCP 负责工具通信，不负责模型推理；写到 stderr 可避免破坏 stdio 协议消息。
    print("MODEL: provider=local model=none mode=mcp-server", file=sys.stderr, flush=True)
    print(f"starting MCP server: profile={PROFILE} transport={args.transport}", file=sys.stderr, flush=True)
    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
