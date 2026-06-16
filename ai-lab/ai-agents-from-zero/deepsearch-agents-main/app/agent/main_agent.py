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
from app.tools.local_kb_tools import create_ask_delete, get_assistant_list
from app.tools.upload_file_read_tool import read_file_content


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
    """Build the main DeepAgent with the requested provider."""
    selected_model = model if provider is None else build_llm_model(provider)
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
    """Normalize LangChain message content into displayable text."""
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
    provider = str(config.get("provider") or "unknown")
    source = str(config.get("source") or provider)
    model_name = str(config.get("model") or "unknown-model")
    return f"{provider} / {source} / {model_name}"


def _extract_json_objects(text: str) -> list[dict[str, object]]:
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

# 下面的工具调用执行函数负责解析模型回复中的工具调用意图，并调用对应工具获取结果。
def _normalize_text_tool_call(payload: dict[str, object]) -> tuple[str, dict[str, object]] | None:
    raw_name = payload.get("name") or payload.get("function")
    if isinstance(raw_name, dict):
        raw_name = raw_name.get("name")
    if not isinstance(raw_name, str):
        return None
    # 通过 TOOL_NAME_ALIASES 把模型可能使用的工具名称映射到我们实际定义的工具函数，避免模型因为小差错调用失败
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
    lowered = task_query.lower()
    return "pdf" in lowered or "转 pdf" in lowered or "转换成 pdf" in lowered


def _clean_report_filename(filename: object, default_name: str = "调研报告") -> str:
    raw = str(filename or default_name).strip() or default_name
    path = Path(raw)
    stem = path.stem if path.suffix else raw
    if not stem.strip():
        stem = default_name
    return f"{stem.strip()}.md"


def _execute_text_tool_call(text: str, task_query: str = "") -> str | None:
    for payload in _extract_json_objects(text):
        normalized = _normalize_text_tool_call(payload)
        if not normalized:
            continue

        tool_name, args = normalized
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
    keywords = ["上传", "附件", "文件读取", "读取文件", "我上传的文件"]
    return any(keyword in task_query for keyword in keywords)


def _is_local_kb_task(task_query: str) -> bool:
    keywords = ["本地知识库", "知识库", "内部文档", "白皮书", "研报"]
    return any(keyword in task_query for keyword in keywords)


def _query_local_knowledge(question: str) -> str:
    assistant_info = get_assistant_list.invoke({})
    retrieved = create_ask_delete.invoke(
        {"chat_name": "本地知识库助手", "question": question}
    )
    return f"[可用助手]\n{assistant_info}\n\n[检索结果]\n{retrieved}"


def _truncate_content(content: str, limit: int = 12000) -> str:
    if len(content) <= limit:
        return content
    return content[:limit] + f"\n\n[内容过长，已截断，原始长度 {len(content)} 字符]"


def _analyze_uploaded_files_sync(task_query: str, uploaded_files: list[Path]) -> str:
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
    timeout_seconds = float(os.getenv("AGENT_RUN_TIMEOUT", "120"))
    return await asyncio.wait_for(
        asyncio.to_thread(_analyze_uploaded_files_sync, task_query, uploaded_files),
        timeout=timeout_seconds,
    )


def _answer_local_kb_sync(task_query: str) -> str:
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
    """Stream a single agent run and forward monitor events."""
    config = {"configurable": {"thread_id": session_id}}
    final_result_reported = False
    last_model_text = ""

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

                if node_name:
                    monitor._emit(
                        "agent_progress",
                        f"Agent 节点已推进: {node_name}",
                        {"node": node_name},
                    )

                if tool_calls:
                    for tool_call in tool_calls:
                        if tool_call.get("name") == "task":
                            args = tool_call.get("args") or {}
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
                    print(f"主智能体执行结果，最终结果：{text[:100]}")
                    monitor.report_task_result(text)
                    final_result_reported = True

    if not final_result_reported:
        if last_model_text:
            monitor.report_task_result(last_model_text)
            return
        raise RuntimeError("模型执行结束但没有生成最终回复，请检查模型是否支持工具调用。")


async def _run_agent_with_timeout(agent, task_query: str, session_id: str, path_instruction: str) -> None:
    timeout_seconds = float(os.getenv("AGENT_RUN_TIMEOUT", "120"))
    stop_event = threading.Event()
    result_queue: queue.Queue[BaseException | None] = queue.Queue(maxsize=1)
    context = copy_context()

    def run_worker() -> None:
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

    loop = asyncio.get_running_loop()
    deadline = loop.time() + timeout_seconds
    while True:
        try:
            result = result_queue.get_nowait()
        except queue.Empty:
            if loop.time() >= deadline:
                stop_event.set()
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
    print(f"[MainAgent] 开始执行会话，session_id={session_id}")

    # 每个会话独立使用 output/session_{session_id}，避免不同用户的产物互相覆盖
    session_dir = project_root_path / "output" / f"session_{session_id}"
    session_dir.mkdir(parents=True, exist_ok=True)

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

    if _is_upload_file_task(task_query) and not uploaded_files:
        monitor._emit(
            "error",
            "没有检测到当前会话的上传文件。请先点击输入框左下角的附件按钮上传文件，等提示上传成功后再发送文件读取任务。",
        )
        reset_session_context(session_dir_token, session_id_token)
        return

    if _is_upload_file_task(task_query) and uploaded_files:
        try:
            monitor._emit(
                "agent_progress",
                f"开始读取上传文件：{', '.join(file.name for file in uploaded_files)}",
            )
            result = await _analyze_uploaded_files(task_query, uploaded_files)
            monitor.report_task_result(result)
        except asyncio.TimeoutError:
            monitor._emit("error", "上传文件分析超时：本地模型长时间没有返回。")
        except Exception as e:
            monitor._emit("error", f"上传文件分析失败：{str(e)}")
        finally:
            reset_session_context(session_dir_token, session_id_token)
        return

    if _is_local_kb_task(task_query):
        try:
            monitor._emit("agent_progress", "开始检索本地知识库")
            result = await _answer_local_kb(task_query)
            monitor.report_task_result(result)
        except asyncio.TimeoutError:
            monitor._emit("error", "本地知识库回答超时：本地模型长时间没有返回。")
        except Exception as e:
            monitor._emit("error", f"本地知识库回答失败：{str(e)}")
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

    primary_config = resolve_llm_config()
    primary_provider = str(primary_config.get("provider") or "openrouter")
    fallback_to_nvidia = (
        primary_provider == "openrouter"
        and resolve_llm_config("nvidia").get("configured")
    )

    try:
        try:
            monitor._emit("agent_progress", f"开始调用模型：{_llm_label(primary_config)}")
            await _run_agent_with_timeout(main_agent, task_query, session_id, path_instruction)
        except Exception as first_error:
            should_try_nvidia = fallback_to_nvidia and (
                _looks_like_openrouter_payment_error(first_error)
                or isinstance(first_error, asyncio.TimeoutError)
            )
            if not should_try_nvidia:
                raise

            reason = "超时" if isinstance(first_error, asyncio.TimeoutError) else "返回 402"
            print(f"[MainAgent] OpenRouter {reason}，尝试切换到 NVIDIA 继续执行。")
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
                if _looks_like_openrouter_payment_error(second_error):
                    raise RuntimeError(_payment_error_message("nvidia")) from second_error
                raise

    except asyncio.CancelledError:
        monitor.report_task_cancelled()
        raise
    except Exception as e:
        # 异步执行异常也走 monitor，保证前端能收到明确错误事件
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
        reset_session_context(session_dir_token, session_id_token)


if __name__ == "__main__":
    import asyncio

    asyncio.run(
        run_deep_agent("从网络查询机器人信息，并生成Markdown文件", "test_session_001")
    )
