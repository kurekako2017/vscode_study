"""学习调用链日志。

这个模块只负责把 Router / Service / Workflow / Provider / Repository / Schema /
HTTP Response 这些学习节点，以人类可读的方式打印到终端。
当 ``LEARNING_TRACE=false`` 时，所有函数立即返回，不影响任何 API 行为、
响应体、SSE 或业务路径。
"""

from __future__ import annotations

from contextvars import ContextVar
from dataclasses import dataclass, field
import sys

from app.observability.logging import get_request_id

_learning_trace_enabled = False
_current_trace: ContextVar["LearningTraceSession | None"] = ContextVar(
    "learning_trace_session",
    default=None,
)
_BANNER = "=" * 60
_ARROW = "↓"


@dataclass
class TraceStep:
    """保存一条学习节点记录，最终统一渲染成终端友好的格式。"""

    node: str
    class_name: str | None = None
    method_name: str | None = None
    file_path: str | None = None
    http_method: str | None = None
    http_path: str | None = None
    status: str | None = None
    task_id: str | None = None
    document_id: str | None = None


@dataclass
class TraceFrame:
    """把一个逻辑节点展开成终端里真正显示的一块内容。

    这样既能保留原始 trace_step 记录，又能在渲染时插入“Entering File”、
    “Schema File” 这类学习提示，让源码阅读顺序和终端输出一一对应。
    """

    heading: str
    node: str
    class_name: str | None = None
    method_name: str | None = None
    file_path: str | None = None
    http_method: str | None = None
    http_path: str | None = None
    status: str | None = None
    task_id: str | None = None
    document_id: str | None = None


@dataclass
class LearningTraceSession:
    """按请求保存学习步骤，结束时一次性打印。"""

    title: str
    request_id: str
    defer_flush: bool = False
    steps: list[TraceStep] = field(default_factory=list)
    pending_exit_step: TraceStep | None = None

    def add(self, step: TraceStep) -> None:
        """追加一条学习节点记录。"""

        self.steps.append(step)


def configure_learning_trace(enabled: bool) -> None:
    """由应用启动时统一设置开关，避免各文件自己判断环境变量。"""

    global _learning_trace_enabled
    _learning_trace_enabled = enabled


def _session() -> LearningTraceSession | None:
    """返回当前请求的学习会话；关闭时或无会话时返回 None。"""

    if not _learning_trace_enabled:
        return None
    return _current_trace.get()


def _ensure_session(http_method: str, http_path: str, title: str | None = None) -> LearningTraceSession:
    """创建或复用当前请求的学习会话。"""

    session = _session()
    if session is not None:
        return session
    session = LearningTraceSession(
        title=title or f"{http_method} {http_path}",
        request_id=get_request_id(),
    )
    _current_trace.set(session)
    return session


def _format_frame(frame: TraceFrame, index: int) -> str:
    """把一个可读 frame 渲染成固定分块格式。"""

    lines = [f"{index}. {frame.heading}", f"   node  : {frame.node}"]
    lines.append(f"   class : {frame.class_name or '-'}")
    method_value = frame.method_name or "-"
    if method_value != "-" and not method_value.endswith("()"):
        method_value = f"{method_value}()"
    lines.append(f"   method: {method_value}")
    lines.append(f"   file  : {frame.file_path or '-'}")
    if frame.http_method is not None:
        lines.append(f"   http  : {frame.http_method} {frame.http_path or '-'}")
    if frame.status is not None:
        lines.append(f"   status: {frame.status}")
    if frame.task_id is not None:
        lines.append(f"   task_id: {frame.task_id}")
    if frame.document_id is not None:
        lines.append(f"   document_id: {frame.document_id}")
    return "\n".join(lines)


def _frame_heading(step: TraceStep) -> str:
    """把原始节点名映射成更适合源码学习的标题。"""

    if step.node == "Schema(Response Model)":
        return "Return"
    return step.node


def _file_entry_heading(file_path: str | None) -> str | None:
    """根据文件路径选择更具体的“进入文件”标题。"""

    if file_path is None:
        return None
    if "/schemas/" in file_path:
        return "Schema File"
    if "/api/" in file_path:
        return "Controller File"
    return "Entering File"


def _file_entry_node(heading: str) -> str:
    """把标题变成真正显示在 node 行上的学习节点。"""

    if heading == "Schema File":
        return "Entering Schema File"
    return "Entering File"


def _build_frames(session: LearningTraceSession) -> list[TraceFrame]:
    """把原始步骤展开成适合教学阅读的 frame 列表。"""

    frames: list[TraceFrame] = []
    previous_file_path: str | None = None
    for step in session.steps:
        file_heading = _file_entry_heading(step.file_path)
        file_changed = (
            previous_file_path is not None
            and step.file_path is not None
            and step.file_path != previous_file_path
        )
        if (
            file_changed
            and step.node != "HTTP Response"
            and file_heading not in {"Controller File", "Schema File"}
        ):
            frames.append(
                TraceFrame(
                    heading=file_heading or "Entering File",
                    node=_file_entry_node(file_heading or "Entering File"),
                    class_name=step.class_name,
                    method_name=step.method_name,
                    file_path=step.file_path,
                    http_method=step.http_method,
                    http_path=step.http_path,
                    status=step.status,
                    task_id=step.task_id,
                    document_id=step.document_id,
                )
            )
        frames.append(
            TraceFrame(
                heading=_frame_heading(step),
                node=step.node,
                class_name=step.class_name,
                method_name=step.method_name,
                file_path=step.file_path,
                http_method=step.http_method,
                http_path=step.http_path,
                status=step.status,
                task_id=step.task_id,
                document_id=step.document_id,
            )
        )
        if file_changed and file_heading == "Controller File":
            frames.append(
                TraceFrame(
                    heading=file_heading,
                    node=_file_entry_node(file_heading),
                    class_name=step.class_name,
                    method_name=step.method_name,
                    file_path=step.file_path,
                    http_method=step.http_method,
                    http_path=step.http_path,
                    status=step.status,
                    task_id=step.task_id,
                    document_id=step.document_id,
                )
            )
            frames.append(
                TraceFrame(
                    heading="Controller Method",
                    node="Controller Method",
                    class_name=step.class_name,
                    method_name=step.method_name,
                    file_path=step.file_path,
                    http_method=step.http_method,
                    http_path=step.http_path,
                    status=step.status,
                    task_id=step.task_id,
                    document_id=step.document_id,
                )
            )
        elif file_changed and file_heading == "Schema File":
            frames.append(
                TraceFrame(
                    heading=file_heading,
                    node=_file_entry_node(file_heading),
                    class_name=step.class_name,
                    method_name=step.method_name,
                    file_path=step.file_path,
                    http_method=step.http_method,
                    http_path=step.http_path,
                    status=step.status,
                    task_id=step.task_id,
                    document_id=step.document_id,
                )
            )
            frames.append(
                TraceFrame(
                    heading="Schema",
                    node="Schema",
                    class_name=step.class_name,
                    method_name=step.method_name,
                    file_path=step.file_path,
                    http_method=step.http_method,
                    http_path=step.http_path,
                    status=step.status,
                    task_id=step.task_id,
                    document_id=step.document_id,
                )
            )
        if step.file_path is not None:
            previous_file_path = step.file_path
    return frames


def _render_session(session: LearningTraceSession) -> str:
    """把整条调用链渲染成终端可读块。"""

    lines = [
        _BANNER,
        "LEARNING TRACE",
        session.title,
        f"request_id: {session.request_id}",
        _BANNER,
    ]
    frames = _build_frames(session)
    for index, frame in enumerate(frames, start=1):
        lines.append(_format_frame(frame, index))
        if index != len(frames):
            lines.append(_ARROW)
    lines.extend([_BANNER, "END LEARNING TRACE"])
    return "\n".join(lines)


def _flush_session(session: LearningTraceSession) -> None:
    """一次性输出当前请求的学习链路。"""

    sys.stdout.write(_render_session(session) + "\n")
    sys.stdout.flush()


def trace_enter(
    http_method: str,
    http_path: str,
    *,
    node: str = "HTTP Request",
    title: str | None = None,
    class_name: str | None = None,
    method_name: str | None = None,
    file_path: str | None = None,
    defer_flush: bool = False,
    task_id: str | None = None,
    document_id: str | None = None,
) -> None:
    """记录一次请求的学习入口，通常放在 FastAPI middleware 最外层。"""

    session = _ensure_session(http_method, http_path, title=title)
    session.defer_flush = defer_flush
    session.add(
        TraceStep(
            node=node,
            class_name=class_name,
            method_name=method_name,
            file_path=file_path,
            http_method=http_method,
            http_path=http_path,
            task_id=task_id,
            document_id=document_id,
            status="started",
        )
    )


def trace_step(
    http_method: str,
    http_path: str,
    node: str,
    detail: str,
    *,
    class_name: str | None = None,
    method_name: str | None = None,
    file_path: str | None = None,
    task_id: str | None = None,
    document_id: str | None = None,
    status: str | None = None,
    error_code: str | None = None,
    sequence: int | None = None,
) -> None:
    """记录 Router / Service / Workflow / Provider / Repository / Schema 中间节点。"""

    del detail, error_code, sequence  # 学习格式只保留人能直接看懂的节点信息。
    session = _session()
    if session is None:
        return
    session.add(
        TraceStep(
            node=node,
            class_name=class_name,
            method_name=method_name,
            file_path=file_path,
            http_method=http_method,
            http_path=http_path,
            task_id=task_id,
            document_id=document_id,
            status=status,
        )
    )


def trace_exit(
    http_method: str,
    http_path: str,
    *,
    response_status: int | str,
    node: str = "HTTP Response",
    detail: str | None = None,
    class_name: str | None = None,
    method_name: str | None = None,
    file_path: str | None = None,
    task_id: str | None = None,
    document_id: str | None = None,
    status: str | None = "completed",
    error_code: str | None = None,
    duration_ms: float | None = None,
) -> None:
    """记录一次请求的学习出口，并在这里统一打印整条链路。"""

    del detail, error_code, duration_ms
    session = _session()
    if session is None:
        return
    response_status_value = str(response_status)
    exit_status = response_status_value if node == "HTTP Response" else status
    if session.defer_flush and node == "HTTP Response":
        session.pending_exit_step = TraceStep(
            node=node,
            class_name=class_name,
            method_name=method_name,
            file_path=file_path,
            http_method=http_method,
            http_path=http_path,
            task_id=task_id,
            document_id=document_id,
            status=exit_status if exit_status is not None else response_status_value,
        )
        return
    session.add(
        TraceStep(
            node=node,
            class_name=class_name,
            method_name=method_name,
            file_path=file_path,
            http_method=http_method,
            http_path=http_path,
            task_id=task_id,
            document_id=document_id,
            status=exit_status if exit_status is not None else response_status_value,
        )
    )
    _flush_session(session)
    _current_trace.set(None)


def finalize_learning_trace() -> None:
    """在后台任务完成时手动冲刷延迟的学习会话。"""

    session = _session()
    if session is None:
        return
    if session.pending_exit_step is not None:
        session.add(session.pending_exit_step)
        session.pending_exit_step = None
    _flush_session(session)
    _current_trace.set(None)
