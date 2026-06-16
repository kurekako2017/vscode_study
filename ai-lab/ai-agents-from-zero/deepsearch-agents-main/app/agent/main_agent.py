"""
主智能体组装与异步执行模块

负责把模型、主提示词、文件类工具和三个专家子智能体组装成 DeepAgent，
并提供 run_deep_agent 作为后续 API 层调用的统一入口。运行时还会为每个
session_id 创建独立工作目录，并把工具调用、子智能体调用和最终结果推送给前端。
"""

import asyncio
import json
import os
import queue
import re
import shutil
import threading
from contextvars import copy_context
from pathlib import Path

from deepagents import create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver

from app.agent.llm import build_llm_model, model
from app.agent.prompts import main_agent_content
from app.agent.subagents.database_query_agent import database_query_agent
from app.agent.subagents.knowledge_base_agent import knowledge_base_agent
from app.agent.subagents.network_search_agent import network_search_agent
from app.runtime_config import resolve_llm_config
from app.api.context import (
    reset_session_context,
    set_session_context,
    set_thread_context,
)
from app.api.monitor import monitor

# 文件类工具由主智能体直接掌握，负责读取上传附件和生成最终交付文档
from app.tools.markdown_tools import generate_markdown
from app.tools.pdf_tools import convert_md_to_pdf
from app.tools.db_tools import get_table_data, list_sql_tables
from app.tools.local_kb_tools import create_ask_delete, get_assistant_list
from app.tools.upload_file_read_tool import read_file_content
from app.utils.logging_utils import get_logger, log_event

logger = get_logger(__name__)


TOOL_NAME_ALIASES = {
    "generate_markdown": "generate_markdown",
    "markdown": "generate_markdown",
    "convert_md_to_pdf": "convert_md_to_pdf",
    "read_file_content": "read_file_content",
    "read_file": "read_file_content",
    "local-knowledge-reviewer": "local_knowledge",
    "local_knowledge": "local_knowledge",
}


def build_main_agent(provider: str | None = None):
    """
    组装主智能体实例。

    这里把四类核心资源拼到一起：
    1. 模型
    2. 主提示词
    3. 主智能体可直接调用的文件工具
    4. 三个专家子智能体

    如果你想看“主智能体究竟能调谁”，这个函数是第一站。
    """
    selected_model = model if provider is None else build_llm_model(provider)
    log_event(logger, 20, "main_agent_build_requested", provider=provider or "default")
    return create_deep_agent(
        model=selected_model,
        system_prompt=main_agent_content["system_prompt"],
        tools=[generate_markdown, convert_md_to_pdf, read_file_content],
        checkpointer=InMemorySaver(),
        subagents=[database_query_agent, network_search_agent, knowledge_base_agent],
    )


# 主智能体是调度中心：
# 1. tools 只放最终交付相关的文件工具
# 2. subagents 放网络、数据库、本地知识库三类信息获取助手
# 3. checkpointer 通过 thread_id 保存同一会话中的执行上下文
main_agent = build_main_agent()

# 当前文件位于 app/agent/main_agent.py，parents[1] 即 app 目录
project_root_path = Path(__file__).parents[1].resolve()


def _looks_like_openrouter_payment_error(exc: Exception) -> bool:
    """Detect the OpenRouter 402 payment-required case."""
    message = str(exc).lower()
    status_code = getattr(exc, "status_code", None)
    return (
        status_code == 402
        or "error code: 402" in message
        or "payment required" in message
        or "insufficient credits" in message
    )


def _payment_error_message(provider: str) -> str:
    """把账单/额度类错误转成用户更容易理解的中文提示。"""
    if provider == "nvidia":
        return (
            "执行主智能发生异常信息：NVIDIA 返回 402，通常表示模型不可用、凭证无效或配额不足。"
            "请检查 NVIDIA_API_KEY 和 NVIDIA_MODEL。"
        )
    return (
        "执行主智能发生异常信息：OpenRouter 返回 402，通常表示额度不足、账单未开通或该模型不可用。"
        "如果你已经配置了 NVIDIA_API_KEY 和 NVIDIA_MODEL，可以把 LLM_PROVIDER 设为 auto 或 nvidia。"
    )


def _message_content_as_text(content) -> str:
    """
    把模型消息内容统一转成纯文本。

    不同模型/框架返回的 content 结构可能是：
    - 纯字符串
    - 带 text 字段的数组
    - 混合对象列表

    这个函数的作用就是把它们都整理成前端可展示、日志可记录的字符串。
    """
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and isinstance(item.get("text"), str):
                parts.append(item["text"])
        return "\n".join(parts).strip()
    return ""


def _llm_label(config: dict[str, object]) -> str:
    """把 provider/source/model 拼成适合日志和前端展示的一行标签。"""
    provider = str(config.get("provider") or "unknown")
    source = str(config.get("source") or provider)
    model_name = str(config.get("model") or "unknown-model")
    return f"{provider} / {source} / {model_name}"


def _extract_json_objects(text: str) -> list[dict[str, object]]:
    """
    从模型文本里尽量提取 JSON 对象。

    某些模型不会严格走标准工具调用协议，而是把工具调用意图直接写进文本。
    这个函数就是为这种情况做兼容解析。
    """
    candidates: list[str] = []
    stripped = text.strip()
    if stripped.startswith("{") and stripped.endswith("}"):
        candidates.append(stripped)

    candidates.extend(match.group(0) for match in re.finditer(r"\{[\s\S]*\}", text))

    objects: list[dict[str, object]] = []
    seen: set[str] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            objects.append(parsed)
    return objects

def _normalize_text_tool_call(payload: dict[str, object]) -> tuple[str, dict[str, object]] | None:
    """
    把模型返回的“文本版工具调用”规范化。

    返回值如果不是 None，说明我们已经成功识别出：
    - 要调用哪个工具
    - 该工具该带什么参数
    """
    raw_name = payload.get("name") or payload.get("function")
    if isinstance(raw_name, dict):
        raw_name = raw_name.get("name")
    if not isinstance(raw_name, str):
        return None
    # 通过 TOOL_NAME_ALIASES 做别名兼容，避免模型因命名小偏差导致调用失败。
    tool_name = TOOL_NAME_ALIASES.get(raw_name)
    if not tool_name:
        return None

    raw_args = payload.get("arguments") or payload.get("args") or {}
    if isinstance(raw_args, str):
        try:
            raw_args = json.loads(raw_args)
        except json.JSONDecodeError:
            return None
    if not isinstance(raw_args, dict):
        return None

    return tool_name, raw_args


def _wants_pdf(task_query: str) -> bool:
    """根据用户提问里的关键词，粗略判断是否要求额外生成 PDF。"""
    lowered = task_query.lower()
    return "pdf" in lowered or "转 pdf" in lowered or "转换成 pdf" in lowered


def _clean_report_filename(filename: object, default_name: str = "调研报告") -> str:
    """清洗模型给出的文件名，统一收敛为安全、可控的 Markdown 文件名。"""
    raw = str(filename or default_name).strip() or default_name
    path = Path(raw)
    stem = path.stem if path.suffix else raw
    if not stem.strip():
        stem = default_name
    return f"{stem.strip()}.md"


def _execute_text_tool_call(text: str, task_query: str = "") -> str | None:
    """
    执行模型文本中携带的工具调用意图。

    这是一个很实用的“兜底层”：
    - 理想情况：模型走标准 tool call
    - 退一步：模型把工具信息写成 JSON 文本
    - 再退一步：我们手工解析 JSON 并主动调用工具
    """
    for payload in _extract_json_objects(text):
        normalized = _normalize_text_tool_call(payload)
        if not normalized:
            continue

        tool_name, args = normalized
        log_event(logger, 20, "text_tool_call_detected", tool_name=tool_name, arg_keys=sorted(args.keys()))
        if tool_name == "generate_markdown":
            args = dict(args)
            args["filename"] = _clean_report_filename(args.get("filename"))
            markdown_result = generate_markdown.invoke(args)
            if not _wants_pdf(task_query):
                return markdown_result

            pdf_result = convert_md_to_pdf.invoke(
                {
                    "md_filename": args["filename"],
                    "pdf_filename": Path(str(args["filename"])).with_suffix(".pdf").name,
                }
            )
            return f"{markdown_result}\n{pdf_result}"
        if tool_name == "convert_md_to_pdf":
            return convert_md_to_pdf.invoke(args)
        if tool_name == "read_file_content":
            return read_file_content.invoke(args)
        if tool_name == "local_knowledge":
            question = str(
                args.get("question")
                or args.get("query")
                or args.get("instruction")
                or args.get("filename")
                or ""
            )
            return _query_local_knowledge(question)

    return None


def _is_upload_file_task(task_query: str) -> bool:
    """用关键词快速识别“读取上传文件”类任务。"""
    keywords = ["上传", "附件", "文件读取", "读取文件", "我上传的文件"]
    return any(keyword in task_query for keyword in keywords)


def _is_local_kb_task(task_query: str) -> bool:
    """用关键词快速识别“本地知识库”类任务。"""
    keywords = ["本地知识库", "知识库", "内部文档", "白皮书", "研报"]
    return any(keyword in task_query for keyword in keywords)


def _is_database_task(task_query: str) -> bool:
    """用关键词快速识别“数据库查询”类任务。"""
    keywords = [
        "数据库",
        "数据表",
        "表结构",
        "sql",
        "SQL",
        "list_sql_tables",
        "get_table_data",
        "execute_sql_query",
    ]
    return any(keyword in task_query for keyword in keywords)


def _query_local_knowledge(question: str) -> str:
    """
    直接调用本地知识库工具，拼出一个可供模型继续总结的上下文块。

    这里故意把“助手列表”和“检索结果”放到一起，便于调试时确认：
    - 当前知识库里到底有哪些助手
    - 这次问题到底检索回来了什么
    """
    assistant_info = get_assistant_list.invoke({})
    retrieved = create_ask_delete.invoke(
        {"chat_name": "本地知识库助手", "question": question}
    )
    return f"[可用助手]\n{assistant_info}\n\n[检索结果]\n{retrieved}"


def _truncate_content(content: str, limit: int = 12000) -> str:
    """截断过长内容，防止大文件全文塞进提示词导致模型上下文爆炸。"""
    if len(content) <= limit:
        return content
    return content[:limit] + f"\n\n[内容过长，已截断，原始长度 {len(content)} 字符]"


def _parse_table_names(table_list_text: str) -> list[str]:
    """从 list_sql_tables 的文本结果里反向解析表名列表。"""
    prefix = "可用的表有："
    if not table_list_text.startswith(prefix):
        return []
    raw_names = table_list_text[len(prefix) :].split(",")
    return [name.strip() for name in raw_names if name.strip()]


def _select_preview_table(task_query: str, table_names: list[str]) -> str | None:
    """优先选用户题目里点名的表，否则默认选第一张表做预览。"""
    lowered_query = task_query.lower()
    for table_name in table_names:
        if table_name.lower() in lowered_query:
            return table_name
    return table_names[0] if table_names else None


def _limit_csv_rows(csv_text: str, limit: int = 5) -> str:
    """把表预览结果限制在前几行，避免提示词过长。"""
    lines = [line for line in csv_text.splitlines() if line.strip()]
    if len(lines) <= 1:
        return csv_text.strip()
    header = lines[0]
    rows = lines[1 : 1 + limit]
    return "\n".join([header, *rows]).strip()


def _answer_database_task_sync(task_query: str) -> str:
    """
    走“数据库直达分支”的同步实现。

    它不会把问题先交给完整多智能体链路，而是直接：
    1. 列表
    2. 预览
    3. 把真实数据交给模型整理成自然语言
    """
    log_event(logger, 20, "database_direct_answer_started", task_query=task_query)
    table_list_text = str(list_sql_tables.invoke({})).strip()
    table_names = _parse_table_names(table_list_text)
    if not table_names:
        return table_list_text or "当前数据库没有可用的表。"

    preview_table = _select_preview_table(task_query, table_names)
    preview_text = ""
    if preview_table:
        preview_raw = str(get_table_data.invoke({"table_name": preview_table})).strip()
        preview_text = _limit_csv_rows(preview_raw, limit=5)
    log_event(logger, 20, "database_direct_answer_context_ready", table_count=len(table_names), preview_table=preview_table)

    prompt = f"""
你正在回答一个数据库查询任务。请严格基于下面的真实数据库结果回答，不要编造未查询到的信息。

用户任务：
{task_query}

数据库表列表：
{table_list_text}

预览表：
{preview_table or "无"}

预览数据（最多前 5 行）：
{preview_text or "无"}

请用中文输出，并满足下面要求：
1. 先列出当前数据库有哪些表。
2. 再说明你选择预览了哪张表，以及为什么选它。
3. 用 Markdown 表格或代码块展示该表前 5 行数据；如果不足 5 行，也如实说明。
4. 如果数据库结果为空或报错，直接说明原因，不要补造数据。
"""
    response = model.invoke(prompt)
    return _message_content_as_text(getattr(response, "content", "")) or str(response)


async def _answer_database_task(task_query: str) -> str:
    """为数据库直达分支补一层超时控制，避免同步调用长期挂起。"""
    timeout_seconds = float(os.getenv("AGENT_RUN_TIMEOUT", "120"))
    return await asyncio.wait_for(
        asyncio.to_thread(_answer_database_task_sync, task_query),
        timeout=timeout_seconds,
    )


def _analyze_uploaded_files_sync(task_query: str, uploaded_files: list[Path]) -> str:
    """
    走“上传文件直达分支”的同步实现。

    逻辑比较朴素但很适合教学：
    1. 逐个读取上传文件
    2. 把真实文本拼进提示词
    3. 让模型只基于这些证据做归纳
    """
    log_event(logger, 20, "uploaded_files_analysis_started", task_query=task_query, uploaded_files=[file.name for file in uploaded_files])
    file_sections = []
    for file in uploaded_files:
        content = read_file_content.invoke(
            {
                "filename": file.name,
                "instruction": "提取核心观点、风险点、待补充信息和下一步分析计划",
            }
        )
        file_sections.append(
            f"## 文件：{file.name}\n\n{_truncate_content(str(content))}"
        )

    analysis_prompt = f"""
你正在分析用户上传的文件。请只基于下面的真实文件内容回答，不要编造文件中没有的信息。

用户任务：
{task_query}

已读取文件内容：
{chr(10).join(file_sections)}

请用中文按以下结构输出：
1. 核心观点
2. 风险点
3. 待补充信息
4. 下一步分析计划

如果文件内容为空、解析失败或证据不足，请明确说明原因。
"""
    response = model.invoke(analysis_prompt)
    return _message_content_as_text(getattr(response, "content", "")) or str(response)


async def _analyze_uploaded_files(task_query: str, uploaded_files: list[Path]) -> str:
    """给上传文件直达分支补一层异步超时包装。"""
    timeout_seconds = float(os.getenv("AGENT_RUN_TIMEOUT", "120"))
    return await asyncio.wait_for(
        asyncio.to_thread(_analyze_uploaded_files_sync, task_query, uploaded_files),
        timeout=timeout_seconds,
    )


def _answer_local_kb_sync(task_query: str) -> str:
    """走“本地知识库直达分支”的同步实现。"""
    log_event(logger, 20, "local_kb_direct_answer_started", task_query=task_query)
    retrieved_context = _query_local_knowledge(task_query)
    prompt = f"""
你正在回答一个本地知识库问题。请只基于下面的检索结果回答，不要编造未检索到的内容。

用户问题：
{task_query}

本地知识库检索结果：
{retrieved_context}

请用中文输出：
1. 检索到的相关资料
2. 可执行建议
3. 证据不足或待补充资料

如果检索结果明确表示没有相关内容，请直接说明当前知识库没有可支持该问题的资料，并建议应补充哪些文档。
"""
    response = model.invoke(prompt)
    return _message_content_as_text(getattr(response, "content", "")) or str(response)


async def _answer_local_kb(task_query: str) -> str:
    """给本地知识库直达分支补一层异步超时包装。"""
    timeout_seconds = float(os.getenv("AGENT_RUN_TIMEOUT", "120"))
    return await asyncio.wait_for(
        asyncio.to_thread(_answer_local_kb_sync, task_query),
        timeout=timeout_seconds,
    )


def _stream_agent_sync(
    agent,
    task_query: str,
    session_id: str,
    path_instruction: str,
    stop_event: threading.Event,
) -> None:
    """
    同步消费 DeepAgent 的流式输出，并把关键节点转成监控事件。

    这是整个项目最值得反复读的函数之一，因为它直接体现了：
    - Agent 是怎样一块块往外吐结果的
    - 子智能体调度是怎样被识别出来的
    - 最终结果又是怎样被推给前端的
    """
    config = {"configurable": {"thread_id": session_id}}
    final_result_reported = False
    last_model_text = ""
    log_event(logger, 20, "agent_stream_started", session_id=session_id, task_query=task_query)

    # agent.stream(...) 会不断产出“按节点切分”的增量结果。
    for chunk in agent.stream(
        {"messages": [{"role": "user", "content": task_query + path_instruction}]},
        config=config,
    ):
        if stop_event.is_set():
            return

        for node_name, state in chunk.items():
            if stop_event.is_set():
                return
            if not state or "messages" not in state:
                continue
            messages = state["messages"]
            if messages and isinstance(messages, list):
                last_msg = messages[-1]
                tool_calls = getattr(last_msg, "tool_calls", None) or []
                text = _message_content_as_text(getattr(last_msg, "content", ""))

                # node_name 往往就是当前 LangGraph/DeepAgent 执行到的节点名。
                if node_name:
                    log_event(logger, 10, "agent_chunk_received", node_name=node_name, has_tool_calls=bool(tool_calls), text_length=len(text))
                    monitor._emit(
                        "agent_progress",
                        f"Agent 节点已推进: {node_name}",
                        {"node": node_name},
                    )

                # 如果这里出现 task 工具调用，通常说明主智能体准备调某个子助手了。
                if tool_calls:
                    for tool_call in tool_calls:
                        if tool_call.get("name") == "task":
                            args = tool_call.get("args") or {}
                            log_event(logger, 20, "subagent_dispatch_detected", subagent_type=args.get("subagent_type", "未知助手"), description=args.get("description", ""))
                            monitor.report_assistant(
                                args.get("subagent_type", "未知助手"),
                                {"description": args.get("description", "")},
                            )
                    continue

                # DeepAgents 常见最终回答在 model 节点；有些版本会把可读文本放在其他非 tools 节点。
                if text and node_name != "tools":
                    tool_result = _execute_text_tool_call(text, task_query)
                    if tool_result:
                        text = f"{tool_result}\n\n{text}"
                    last_model_text = text
                    log_event(logger, 20, "agent_final_result_generated", preview=text[:160], result_length=len(text))
                    monitor.report_task_result(text)
                    final_result_reported = True

    if not final_result_reported:
        if last_model_text:
            log_event(logger, 30, "agent_stream_finished_without_explicit_result", preview=last_model_text[:160])
            monitor.report_task_result(last_model_text)
            return
        raise RuntimeError("模型执行结束但没有生成最终回复，请检查模型是否支持工具调用。")


async def _run_agent_with_timeout(agent, task_query: str, session_id: str, path_instruction: str) -> None:
    """
    在线程里跑同步流式 Agent，并由异步外层负责超时控制。

    之所以这么绕，是因为某些模型/Agent 流式实现不是纯异步接口。
    我们需要：
    - 线程承接阻塞式 stream
    - asyncio 外层负责统一超时和取消
    """
    timeout_seconds = float(os.getenv("AGENT_RUN_TIMEOUT", "120"))
    stop_event = threading.Event()
    result_queue: queue.Queue[BaseException | None] = queue.Queue(maxsize=1)
    context = copy_context()

    def run_worker() -> None:
        # copy_context() 复制了当前 ContextVar，
        # 这样线程里的工具调用也能拿到 session_dir/thread_id。
        try:
            context.run(
                _stream_agent_sync,
                agent,
                task_query,
                session_id,
                path_instruction,
                stop_event,
            )
            result_queue.put_nowait(None)
        except BaseException as exc:
            result_queue.put_nowait(exc)

    thread = threading.Thread(target=run_worker, daemon=True)
    thread.start()
    log_event(logger, 20, "agent_worker_thread_started", session_id=session_id, timeout_seconds=timeout_seconds)

    loop = asyncio.get_running_loop()
    deadline = loop.time() + timeout_seconds
    while True:
        try:
            result = result_queue.get_nowait()
        except queue.Empty:
            if loop.time() >= deadline:
                stop_event.set()
                log_event(logger, 40, "agent_worker_timeout", session_id=session_id, timeout_seconds=timeout_seconds)
                raise asyncio.TimeoutError
            await asyncio.sleep(0.2)
            continue

        if result is None:
            return
        raise result


async def run_deep_agent(task_query, session_id):
    """
    异步流式执行主智能体

    API 层会为每次任务传入用户问题和 session_id。本函数负责准备会话目录、
    复制上传文件、写入 ContextVar，并在流式执行过程中把关键事件上报给前端。
    :param task_query: 前端提交的原始任务问题
    :param session_id: 当前任务 ID，同时用于 thread_id、输出目录和 WebSocket 定向推送
    """
    log_event(logger, 20, "run_deep_agent_started", session_id=session_id, task_query=task_query)

    # 每个会话独立使用 output/session_{session_id}，避免不同用户的产物互相覆盖
    session_dir = project_root_path / "output" / f"session_{session_id}"
    session_dir.mkdir(parents=True, exist_ok=True)
    log_event(logger, 20, "session_output_directory_ready", session_id=session_id, session_dir=str(session_dir))

    # 前端和工具使用绝对路径；提示词里只给模型相对路径，降低模型误用系统绝对路径的概率
    session_dir_str = str(session_dir).replace("\\", "/")
    relative_session_dir_str = str(session_dir.relative_to(project_root_path)).replace(
        "\\", "/"
    )

    # 上传文件先落在 updated/session_{session_id}，执行前复制到本次 output 工作目录
    # 这样读文件工具和生成文件工具都只需要围绕同一个 session_dir 工作
    updated_dir_path = project_root_path / "updated" / f"session_{session_id}"
    updated_info_prompt = ""
    uploaded_files: list[Path] = []
    if updated_dir_path.exists():
        uploaded_files = [f for f in updated_dir_path.iterdir() if f.is_file()]
        if uploaded_files:
            log_event(logger, 20, "session_uploaded_files_found", session_id=session_id, uploaded_files=[f.name for f in uploaded_files])
            for source_file in uploaded_files:
                # copy2 会保留上传文件的修改时间、权限等元数据，便于后续排查文件来源
                shutil.copy2(source_file, session_dir / source_file.name)

            # 把上传文件列表注入用户消息，提醒模型先调用 read_file_content 获取附件内容
            file_lines = [
                f"    - {file.name} ({file.stat().st_size} bytes)"
                for file in uploaded_files
            ]
            updated_info_prompt = (
                "\n    [已上传文件] 已加载到工作目录:\n"
                + "\n".join(file_lines)
                + "\n    必须先调用 read_file_content 读取上述文件，再基于真实内容回答。"
            )

    # ContextVar 让深层工具无需显式传参，也能拿到当前会话目录和 WebSocket thread_id
    session_dir_token = set_session_context(session_dir_str)
    session_id_token = set_thread_context(session_id)

    # 前端拿到工作目录后，可以展示本次任务生成的 Markdown/PDF 等产物
    monitor.report_session_dir(session_dir_str)

    # 下面三段 if 是“直达分支”。
    # 命中后不会先走完整多智能体调度，而是直接执行特定链路，减少歧义并方便教学。
    if _is_upload_file_task(task_query) and not uploaded_files:
        log_event(logger, 30, "upload_task_missing_uploaded_files", session_id=session_id)
        monitor._emit(
            "error",
            "没有检测到当前会话的上传文件。请先点击输入框左下角的附件按钮上传文件，等提示上传成功后再发送文件读取任务。",
        )
        reset_session_context(session_dir_token, session_id_token)
        return

    if _is_upload_file_task(task_query) and uploaded_files:
        try:
            log_event(logger, 20, "upload_task_branch_selected", session_id=session_id, uploaded_files=[file.name for file in uploaded_files])
            monitor._emit(
                "agent_progress",
                f"开始读取上传文件：{', '.join(file.name for file in uploaded_files)}",
            )
            result = await _analyze_uploaded_files(task_query, uploaded_files)
            monitor.report_task_result(result)
        except asyncio.TimeoutError:
            log_event(logger, 40, "upload_task_branch_timeout", session_id=session_id)
            monitor._emit("error", "上传文件分析超时：本地模型长时间没有返回。")
        except Exception as e:
            log_event(logger, 40, "upload_task_branch_failed", session_id=session_id, error=str(e))
            monitor._emit("error", f"上传文件分析失败：{str(e)}")
        finally:
            reset_session_context(session_dir_token, session_id_token)
        return

    if _is_local_kb_task(task_query):
        try:
            log_event(logger, 20, "local_kb_branch_selected", session_id=session_id)
            monitor._emit("agent_progress", "开始检索本地知识库")
            result = await _answer_local_kb(task_query)
            monitor.report_task_result(result)
        except asyncio.TimeoutError:
            log_event(logger, 40, "local_kb_branch_timeout", session_id=session_id)
            monitor._emit("error", "本地知识库回答超时：本地模型长时间没有返回。")
        except Exception as e:
            log_event(logger, 40, "local_kb_branch_failed", session_id=session_id, error=str(e))
            monitor._emit("error", f"本地知识库回答失败：{str(e)}")
        finally:
            reset_session_context(session_dir_token, session_id_token)
        return

    if _is_database_task(task_query):
        try:
            log_event(logger, 20, "database_branch_selected", session_id=session_id)
            monitor._emit("agent_progress", "开始查询数据库表结构与样例数据")
            result = await _answer_database_task(task_query)
            monitor.report_task_result(result)
        except asyncio.TimeoutError:
            log_event(logger, 40, "database_branch_timeout", session_id=session_id)
            monitor._emit("error", "数据库查询超时：本地模型长时间没有返回。")
        except Exception as e:
            log_event(logger, 40, "database_branch_failed", session_id=session_id, error=str(e))
            monitor._emit("error", f"数据库查询失败：{str(e)}")
        finally:
            reset_session_context(session_dir_token, session_id_token)
        return

    # 工作环境指令是运行时动态补充的，约束模型只在当前会话目录读写文件
    path_instruction = f"""
    【工作环境指令】
    工作目录: {relative_session_dir_str}
    {updated_info_prompt}

    规则：
    1. 新生成文件必须保存到工作目录：'{relative_session_dir_str}/filename'
    2. 读取已上传的文件时，请直接将文件名（例如：'开篇.txt'）作为 filename 参数传入（read_file_content）读取工具，不要带上任何目录前缀。
    3. 使用相对路径，禁止使用绝对路径
    4. 若存在上传文件，请先分析内容
    """

    # 如果没有命中直达分支，才进入真正的主智能体调度模式。
    primary_config = resolve_llm_config()
    primary_provider = str(primary_config.get("provider") or "openrouter")
    fallback_to_nvidia = (
        primary_provider == "openrouter"
        and resolve_llm_config("nvidia").get("configured")
    )

    try:
        try:
            log_event(logger, 20, "main_agent_primary_provider_selected", session_id=session_id, provider=primary_provider, model=primary_config.get("model"))
            monitor._emit("agent_progress", f"开始调用模型：{_llm_label(primary_config)}")
            await _run_agent_with_timeout(main_agent, task_query, session_id, path_instruction)
        except Exception as first_error:
            should_try_nvidia = fallback_to_nvidia and (
                _looks_like_openrouter_payment_error(first_error)
                or isinstance(first_error, asyncio.TimeoutError)
            )
            if not should_try_nvidia:
                log_event(logger, 40, "main_agent_primary_provider_failed_no_fallback", session_id=session_id, error=str(first_error))
                raise

            reason = "超时" if isinstance(first_error, asyncio.TimeoutError) else "返回 402"
            log_event(logger, 30, "main_agent_fallback_to_nvidia", session_id=session_id, reason=reason)
            monitor._emit(
                "agent_progress",
                f"OpenRouter {reason}，正在切换到 NVIDIA 继续执行。",
            )
            fallback_agent = build_main_agent("nvidia")
            fallback_config = resolve_llm_config("nvidia")
            monitor._emit("agent_progress", f"开始调用模型：{_llm_label(fallback_config)}")
            try:
                await _run_agent_with_timeout(fallback_agent, task_query, session_id, path_instruction)
            except Exception as second_error:
                log_event(logger, 40, "main_agent_fallback_failed", session_id=session_id, error=str(second_error))
                if _looks_like_openrouter_payment_error(second_error):
                    raise RuntimeError(_payment_error_message("nvidia")) from second_error
                raise

    except asyncio.CancelledError:
        log_event(logger, 30, "run_deep_agent_cancelled", session_id=session_id)
        monitor.report_task_cancelled()
        raise
    except Exception as e:
        # 异步执行异常也走 monitor，保证前端能收到明确错误事件
        log_event(logger, 40, "run_deep_agent_failed", session_id=session_id, error=str(e))
        if _looks_like_openrouter_payment_error(e):
            provider = "nvidia" if "nvidia" in str(e).lower() else "openrouter"
            monitor._emit("error", _payment_error_message(provider))
        elif isinstance(e, asyncio.TimeoutError):
            monitor._emit(
                "error",
                "执行主智能超时：模型长时间没有返回。请稍后重试，或将 LLM_PROVIDER 设置为 nvidia。",
            )
        else:
            monitor._emit("error", f"执行主智能发生异常信息：{str(e)}")
    finally:
        # 任务结束后恢复 ContextVar，避免后续请求复用到本次会话目录或 thread_id
        log_event(logger, 20, "run_deep_agent_cleanup", session_id=session_id)
        reset_session_context(session_dir_token, session_id_token)


if __name__ == "__main__":
    import asyncio

    asyncio.run(
        run_deep_agent("从网络查询机器人信息，并生成Markdown文件", "test_session_001")
    )
