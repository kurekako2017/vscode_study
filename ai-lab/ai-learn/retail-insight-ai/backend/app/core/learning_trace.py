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
    label: str | None = None
    class_name: str | None = None
    method_name: str | None = None
    file_path: str | None = None
    http_method: str | None = None
    http_path: str | None = None
    status: str | None = None
    task_id: str | None = None
    document_id: str | None = None
    phase: str = "http"


@dataclass
class LearningTraceSession:
    """按请求保存学习步骤，结束时一次性打印。"""

    title: str
    request_id: str
    defer_flush: bool = False
    steps: list[TraceStep] = field(default_factory=list)
    pending_exit_step: TraceStep | None = None
    request_body_lines: list[str] = field(default_factory=list)
    closed: bool = False

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
    session = _current_trace.get()
    if session is not None and session.closed:
        return None
    return session


def _ensure_session(http_method: str, http_path: str, title: str | None = None) -> LearningTraceSession:
    """创建或复用当前请求的学习会话。"""

    session = _session()
    expected_title = title or f"{http_method} {http_path}"
    expected_request_id = get_request_id()
    if session is not None and session.title == expected_title and session.request_id == expected_request_id:
        return session
    session = LearningTraceSession(
        title=expected_title,
        request_id=expected_request_id,
    )
    _current_trace.set(session)
    return session


def _task_id(session: LearningTraceSession) -> str:
    """从当前学习会话中提取最有代表性的 task_id。"""

    for step in session.steps:
        if step.task_id:
            return step.task_id
    return "-"


def _step_label(step: TraceStep) -> str:
    """把学习节点收敛成终端里一眼可读的业务调用链。"""

    if step.label is not None:
        return step.label
    if step.node == "HTTP Request":
        return "HTTP Request"
    if step.node == "HTTP Response":
        response_status = step.status or "-"
        return f"HTTP {response_status} Response"
    if step.node == "Router":
        return f"Router.{step.method_name or 'handle'}()"
    if step.node == "Service":
        return f"TaskService.{step.method_name or 'handle'}()"
    if step.node == "Repository":
        repository_name = step.class_name or "Repository"
        method_name = step.method_name or "save"
        if step.status:
            return f"{repository_name}.{method_name}({step.status})"
        return f"{repository_name}.{method_name}()"
    if step.node == "Event":
        return f"EventPublisher.publish({step.status or 'event'})"
    if step.node == "Workflow":
        return f"{step.class_name or 'Workflow'}.{step.method_name or 'run'}()"
    return step.node


def _render_steps(steps: list[TraceStep]) -> list[str]:
    """将步骤列表渲染成单列学习链路。"""

    visible_steps = [step for step in steps if step.node != "Schema(Response Model)"]
    lines: list[str] = []
    for index, step in enumerate(visible_steps):
        lines.append(_step_label(step))
        if index != len(visible_steps) - 1:
            lines.append(f"    {_ARROW}")
    return lines


def _render_session(session: LearningTraceSession) -> str:
    """把整条调用链渲染成终端可读块。"""

    lines = [
        _BANNER,
        session.title,
        f"request_id : {session.request_id}",
        f"task_id    : {_task_id(session)}",
        _BANNER,
    ]
    if session.request_body_lines:
        lines.extend(
            [
                "-" * 48,
                "Request Body",
                "-" * 48,
                *session.request_body_lines,
                "-" * 48,
                "",
            ]
        )

    if session.defer_flush:
        http_steps = [step for step in session.steps if step.phase == "http"]
        background_steps = [step for step in session.steps if step.phase == "background"]
        lines.append("HTTP Request")
        http_chain_steps = http_steps[1:] if http_steps and http_steps[0].node == "HTTP Request" else http_steps
        lines.extend([f"    {line}" if line != f"    {_ARROW}" else line for line in _render_steps(http_chain_steps)])
        if background_steps:
            lines.extend(
                [
                    "",
                    "---------------- Background Task ----------------",
                    "",
                    *[
                        f"    {line}" if line != f"    {_ARROW}" else line
                        for line in _render_steps(background_steps)
                    ],
                ]
            )
    else:
        lines.extend(_render_steps(session.steps))
    lines.append("")
    lines.append(_BANNER)
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
            phase="http",
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
    label: str | None = None,
    phase: str = "http",
) -> None:
    """记录 Router / Service / Workflow / Provider / Repository / Schema 中间节点。"""

    del detail, error_code, sequence  # 学习格式只保留人能直接看懂的节点信息。
    session = _session()
    if session is None:
        return
    session.add(
        TraceStep(
            node=node,
            label=label,
            class_name=class_name,
            method_name=method_name,
            file_path=file_path,
            http_method=http_method,
            http_path=http_path,
            task_id=task_id,
            document_id=document_id,
            status=status,
            phase=phase,
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
            label=f"HTTP {response_status_value} Response" if node == "HTTP Response" else None,
            class_name=class_name,
            method_name=method_name,
            file_path=file_path,
            http_method=http_method,
            http_path=http_path,
            task_id=task_id,
            document_id=document_id,
            status=exit_status if exit_status is not None else response_status_value,
            phase="http",
        )
        return
    session.add(
        TraceStep(
            node=node,
            label=f"HTTP {response_status_value} Response" if node == "HTTP Response" else None,
            class_name=class_name,
            method_name=method_name,
            file_path=file_path,
            http_method=http_method,
            http_path=http_path,
            task_id=task_id,
            document_id=document_id,
            status=exit_status if exit_status is not None else response_status_value,
            phase="http",
        )
    )
    _flush_session(session)
    session.closed = True
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
    session.closed = True
    _current_trace.set(None)


def trace_request_body(http_method: str, http_path: str, *, question: str, mode: str, task_id: str) -> None:
    """把学习用请求体内容绑定到当前 trace，会在最终 block 里统一显示。"""

    session = _ensure_session(http_method, http_path)
    session.request_body_lines = [
        f"question : {question}",
        f"mode     : {mode}",
    ]
    for step in session.steps:
        if step.task_id is None:
            step.task_id = task_id
