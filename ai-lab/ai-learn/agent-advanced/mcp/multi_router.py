"""两个 MCP server 的工具目录、路由和冲突处理。"""
from __future__ import annotations

import argparse
import asyncio
import os
import sys
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run(query: str) -> None:
    """连接两个 MCP 域，建立带域名前缀的工具目录，再按规则选择目标。"""
    # AsyncExitStack 统一管理多个异步连接，函数结束时会逆序关闭它们。
    async with AsyncExitStack() as stack:
        sessions: dict[str, ClientSession] = {}
        catalog: dict[str, tuple[str, str]] = {}
        for domain in ("office", "engineering"):
            print(f"connecting: {domain}", flush=True)
            env = os.environ.copy()
            env["MCP_PROFILE"] = domain
            params = StdioServerParameters(command=sys.executable, args=["server.py"], env=env)
            streams = await stack.enter_async_context(stdio_client(params))
            session = await stack.enter_async_context(ClientSession(*streams))
            await session.initialize()
            sessions[domain] = session
            for tool in (await session.list_tools()).tools:
                # 加 domain 前缀可避免两个 server 暴露同名工具时发生冲突。
                catalog[f"{domain}.{tool.name}"] = (domain, tool.name)
        domain = "engineering" if any(word in query.lower() for word in ["pr", "发布", "代码", "github"]) else "office"
        # 当前路由是可预测的关键词规则，没有调用 LLM 做工具选择。
        qualified = f"{domain}.search_documents"
        target, tool = catalog[qualified]
        print("catalog:", sorted(catalog), "route:", qualified)
        result = await sessions[target].call_tool(tool, {"query": query})
        print([item.model_dump() for item in result.content])


def main() -> None:
    """读取查询并运行多 server 路由演示。"""
    print("MODEL: provider=local model=none mode=rule-router")
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="?", default="费用审批")
    asyncio.run(run(parser.parse_args().query))


if __name__ == "__main__":
    main()
