"""MCP client：发现并调用 stdio 或 remote server。"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from contextlib import asynccontextmanager

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client


@asynccontextmanager
async def connect(transport: str, url: str):
    """建立 MCP 会话；stdio 启动子进程，remote 连接已运行的 HTTP server。"""
    if transport == "stdio":
        # sys.executable 保证 server 使用与 client 相同的 Python 环境。
        params = StdioServerParameters(command=sys.executable, args=["server.py"])
        async with stdio_client(params) as streams:
            async with ClientSession(*streams) as session:
                yield session
    else:
        async with streamable_http_client(url) as streams:
            async with ClientSession(streams[0], streams[1]) as session:
                yield session


async def run(args: argparse.Namespace) -> None:
    """初始化协议、发现工具，再调用 search_documents。"""
    print(f"connecting: transport={args.transport}", flush=True)
    async with connect(args.transport, args.url) as session:
        print("connected; initializing", flush=True)
        await session.initialize()
        tools = await session.list_tools()
        # 先发现工具而不是假设 server 一定提供某个工具，是 MCP 的核心步骤之一。
        print("tools:", [tool.name for tool in tools.tools])
        result = await asyncio.wait_for(
            session.call_tool("search_documents", {"query": args.query, "limit": args.limit}),
            timeout=args.timeout,
        )
        print(json.dumps([item.model_dump() for item in result.content], ensure_ascii=False))


def main() -> None:
    """解析连接参数，并用 asyncio.run 启动异步 MCP 客户端。"""
    print("MODEL: provider=local model=none mode=mcp-client")
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="?", default="审批")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--timeout", type=float, default=5)
    parser.add_argument("--transport", choices=["stdio", "remote"], default="stdio")
    parser.add_argument("--url", default="http://127.0.0.1:8765/mcp")
    asyncio.run(run(parser.parse_args()))


if __name__ == "__main__":
    main()
