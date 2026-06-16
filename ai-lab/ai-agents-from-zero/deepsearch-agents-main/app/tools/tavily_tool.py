"""
Tavily 网络搜索工具模块

封装 internet_search 工具，供网络搜索子智能体检索互联网公开信息
工具内部会先通过 monitor 上报调用参数，再请求 Tavily API 返回结构化搜索结果
"""

import os
import logging
from typing import Literal

from dotenv import load_dotenv
from langchain_core.tools import tool
from tavily import TavilyClient

from app.api.monitor import monitor
from app.utils.logging_utils import log_event

logger = logging.getLogger(__name__)

load_dotenv()

_tavily_client = None


def _get_tavily_client():
    """Create a Tavily client on demand so the API can boot without the key."""
    global _tavily_client
    if _tavily_client is not None:
        return _tavily_client

    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return None

    _tavily_client = TavilyClient(api_key=api_key)
    return _tavily_client


# @tool 会把函数签名和 docstring 暴露给 DeepAgents，模型据此决定是否调用以及如何填参
@tool
def internet_search(
    query: str,
    topic: Literal["news", "finance", "general"] = "general",
    max_results: int = 5,
    include_raw_content: bool = False,
):
    """
    根据用户问题检索互联网公开信息

    注意：本工具只用于外部公开网页、新闻、政策等信息，不用于查询业务数据库或本地知识库
    :param query: 搜索关键词或自然语言问题
    :param topic: 搜索主题，可选 news、finance、general
    :param max_results: 返回的最大结果数
    :param include_raw_content: 是否返回网页原文内容；False 返回摘要，True 尝试返回更完整正文
    :return: Tavily 返回的结构化搜索结果
    """
    # 工具内部埋点比外层 stream 解析更直接：只要工具被调用，前端就能看到本次搜索参数
    # 这里只上报查询参数，不上报搜索结果正文，避免监控事件体过大
    monitor.report_tool(
        tool_name="网络搜索工具",
        args={
            "query": query,
            "topic": topic,
            "max_results": max_results,
            "include_raw_content": include_raw_content,
        },
    )
    log_event(
        logger,
        logging.INFO,
        "internet_search_started",
        query=query,
        topic=topic,
        max_results=max_results,
        include_raw_content=include_raw_content,
    )

    tavily_client = _get_tavily_client()
    if tavily_client is None:
        log_event(logger, logging.WARNING, "internet_search_missing_api_key")
        return "TAVILY_API_KEY 未配置，当前环境无法执行网络搜索。"

    # Tavily 返回 query、results、title、url、content 等结构化字段，后续由子智能体阅读并汇总
    result = tavily_client.search(
        query=query,
        topic=topic,
        max_results=max_results,
        include_raw_content=include_raw_content,
    )
    log_event(
        logger,
        logging.INFO,
        "internet_search_completed",
        query=query,
        result_count=len(result.get("results", [])) if isinstance(result, dict) else None,
    )
    return result


if __name__ == "__main__":
    from pprint import pprint

    # 本地调试入口：直接运行本文件可验证 TAVILY_API_KEY 和 Tavily API 是否可用
    pprint(
        internet_search.invoke(
            {"query": "2026中国法定节假日放假安排表，我天天都想要放假"}
        )
    )
