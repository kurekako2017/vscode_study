"""
Shared structured logging helpers.

The project previously relied on scattered ``print`` statements, which are hard
to filter when tracing a bug. This module centralises runtime logging so the
backend can emit consistent, context-rich records that are easy to grep.
"""

# 这个工具文件负责把项目里零散的日志输出方式统一起来。
# 初学者只需要记住：
# - get_logger(name) 负责拿到 logger
# - log_event(...) 负责按统一 JSON 结构输出关键上下文

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any

_CONFIGURED = False


def configure_logging() -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return

    level_name = os.getenv("DEEPSEARCH_LOG_LEVEL", os.getenv("LOG_LEVEL", "INFO"))
    level = getattr(logging, level_name.upper(), logging.INFO)
    # 所有日志统一使用“时间 | 级别 | logger 名称 | 消息体”的格式，
    # 消息体本身再放一层 JSON，后续 grep 会比较方便。
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    if not root_logger.handlers:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        root_logger.addHandler(stream_handler)

    log_file = os.getenv("DEEPSEARCH_LOG_FILE", "").strip()
    if log_file:
        # 如果用户提供了日志文件路径，就额外再挂一个 FileHandler。
        file_path = Path(log_file).expanduser()
        file_path.parent.mkdir(parents=True, exist_ok=True)
        existing_file_handler = any(
            isinstance(handler, logging.FileHandler)
            and Path(getattr(handler, "baseFilename", "")) == file_path
            for handler in root_logger.handlers
        )
        if not existing_file_handler:
            file_handler = logging.FileHandler(file_path, encoding="utf-8")
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)

    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    configure_logging()
    return logging.getLogger(name)


def _safe_value(value: Any) -> Any:
    # 日志里不适合原样塞过大的对象，所以这里做一层截断和转换。
    if value is None:
        return None
    if isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        return value if len(value) <= 500 else value[:500] + "...(truncated)"
    if isinstance(value, (list, tuple, set)):
        return [_safe_value(item) for item in list(value)[:20]]
    if isinstance(value, dict):
        limited_items = list(value.items())[:30]
        return {str(key): _safe_value(item) for key, item in limited_items}
    return str(value)


def _current_context() -> dict[str, Any]:
    # 如果当前代码运行在某个任务上下文里，就自动把 thread_id / session_dir
    # 加进日志，后面排查 bug 时就不用手动层层传参。
    try:
        from app.api.context import get_session_context, get_thread_context

        return {
            "thread_id": get_thread_context(),
            "session_dir": get_session_context(),
        }
    except Exception:
        return {}


def log_event(logger: logging.Logger, level: int, event: str, **fields: Any) -> None:
    # 统一日志入口：
    # 1. 先带上 event 名
    # 2. 再自动带上上下文
    # 3. 最后把额外字段做安全转换后一起打出
    payload = {"event": event, **_current_context()}
    payload.update({key: _safe_value(value) for key, value in fields.items()})
    logger.log(level, json.dumps(payload, ensure_ascii=False, sort_keys=True))
