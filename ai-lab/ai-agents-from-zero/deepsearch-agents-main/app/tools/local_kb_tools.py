"""
Local knowledge base tools.

These tools replace the external RAGFlow dependency with an in-repo retrieval
layer over ``docs/knowledge_base``. The interface stays close to the old
RAGFlow helper functions so the DeepAgents routing logic only needs a small
update.
"""

from __future__ import annotations

import logging

from langchain_core.tools import tool

from app.api.monitor import monitor
from app.knowledge_base.local_index import has_local_knowledge_base, search_knowledge_base
from app.utils.logging_utils import log_event

logger = logging.getLogger(__name__)


@tool
def get_assistant_list() -> str:
    """
    Return the available local knowledge base assistant(s).

    The current project ships a single local knowledge base backed by the
    repository documents under ``docs/knowledge_base``.
    """

    monitor.report_tool(tool_name="本地知识库助手列表查询工具：get_assistant_list")
    log_event(logger, logging.INFO, "local_kb_get_assistant_list_started")

    if not has_local_knowledge_base():
        log_event(logger, logging.WARNING, "local_kb_empty")
        return "本地知识库目录为空，当前没有可用文档。请先把 PDF、MD、DOCX 等资料放入 docs/knowledge_base/。"

    log_event(logger, logging.INFO, "local_kb_assistant_list_completed")
    return "助手名称:本地知识库助手;功能介绍：基于 docs/knowledge_base/ 的本地文档检索与问答; 关联的知识库：docs/knowledge_base/"


@tool
def create_ask_delete(chat_name: str, question: str) -> str:
    """
    Query the local knowledge base and return the top relevant passages.

    ``chat_name`` is kept for compatibility with the previous RAGFlow-based
    interface; the local implementation currently exposes a single assistant.
    """

    monitor.report_tool(
        tool_name="本地知识库提问工具：create_ask_delete",
        args={"chat_name": chat_name, "question": question},
    )
    log_event(logger, logging.INFO, "local_kb_query_started", chat_name=chat_name, question=question)

    if not has_local_knowledge_base():
        log_event(logger, logging.WARNING, "local_kb_query_empty")
        return "本地知识库目录为空，当前没有可检索文档。"

    results = search_knowledge_base(question, top_k=3)
    if not results:
        log_event(logger, logging.WARNING, "local_kb_query_no_results", question=question)
        return "没有检索到与问题明显相关的本地知识库内容。请换一种问法，或补充相关文档。"

    lines: list[str] = []
    for index, result in enumerate(results, start=1):
        lines.append(
            "\n".join(
                [
                    f"[{index}] 文档: {result['title']}",
                    f"路径: {result['path']}",
                    f"相关度: {result['score']}",
                    f"摘录: {result['snippet']}",
                ]
            )
        )
    log_event(logger, logging.INFO, "local_kb_query_completed", question=question, result_count=len(results))
    return "\n\n".join(lines)
