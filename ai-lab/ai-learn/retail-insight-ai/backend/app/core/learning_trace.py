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
class LearningTraceSession:
    """按请求保存学习步骤，结束时一次性打印。"""

    title: str
    request_id: str
    defer_flush: bool = False
    steps: list[TraceStep] = field(default_factory=list)

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


def _format_step(step: TraceStep, index: int) -> str:
    """把单个节点转成多行可读文本。"""

    lines = [f"{index} {step.node}"]
    if step.http_method is not None:
        lines.append(f"   method: {step.http_method}")
    if step.http_path is not None:
        lines.append(f"   path  : {step.http_path}")
    if step.class_name is not None:
        lines.append(f"   class : {step.class_name}")
    if step.method_name is not None:
        method_value = step.method_name if step.method_name.endswith("()") else f"{step.method_name}()"
        lines.append(f"   method: {method_value}")
    if step.file_path is not None:
        lines.append(f"   file  : {step.file_path}")
    if step.status is not None:
        lines.append(f"   status: {step.status}")
    if step.task_id is not None:
        lines.append(f"   task_id: {step.task_id}")
    if step.document_id is not None:
        lines.append(f"   document_id: {step.document_id}")
    return "\n".join(lines)


def _render_session(session: LearningTraceSession) -> str:
    """把整条调用链渲染成终端可读块。"""

    lines = [
        _BANNER,
        f"LEARNING TRACE: {session.title}",
        f"request_id: {session.request_id}",
        _BANNER,
    ]
    for index, step in enumerate(session.steps, start=1):
        lines.append(_format_step(step, index))
        if index != len(session.steps):
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
    if session.defer_flush and node == "HTTP Response":
        return
    _flush_session(session)
    _current_trace.set(None)


def finalize_learning_trace() -> None:
    """在后台任务完成时手动冲刷延迟的学习会话。"""

    session = _session()
    if session is None:
        return
    _flush_session(session)
    _current_trace.set(None)
