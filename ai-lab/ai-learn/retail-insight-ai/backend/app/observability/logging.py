"""输出适合日志平台采集的 JSON 结构化日志。

业务代码只通过 :func:`log_event` 写入预先允许的元数据字段。这样可以从设计上
降低把 Prompt、会员资料或密钥误写进日志的风险，而不是依赖开发者每次手工检查。
"""

from __future__ import annotations

import json
import logging
import sys
from contextvars import ContextVar, Token
from datetime import datetime, timezone
from typing import Any, Literal

DEFAULT_SERVICE = "Retail Insight AI"
LOGGER_NAMESPACE = "retail_insight_ai"

# ContextVar 让同一异步请求中的日志自动带上 request_id，同时避免并发请求互相覆盖。
_request_id_context: ContextVar[str] = ContextVar("request_id", default="-")

# 只允许这些字段进入日志。禁止透传任意字典可减少敏感业务数据泄漏的机会。
_SAFE_EXTRA_FIELDS = {"status", "node", "http_method", "http_path", "sequence"}


class JsonLogFormatter(logging.Formatter):
    """把标准 LogRecord 转换为字段稳定的单行 JSON。"""

    def __init__(self, service: str = DEFAULT_SERVICE) -> None:
        """保存服务名，使每条日志都能在集中平台中按服务筛选。"""

        super().__init__()
        self._service = service

    def format(self, record: logging.LogRecord) -> str:
        """生成固定核心字段，并仅追加经过白名单约束的业务元数据。"""

        structured = getattr(record, "structured_data", {})
        payload: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "service": self._service,
            "request_id": structured.get("request_id") or _request_id_context.get(),
            "task_id": structured.get("task_id") or "-",
            "event": structured.get("event") or "application_log",
            "message": record.getMessage(),
            "error_code": structured.get("error_code"),
            "duration_ms": structured.get("duration_ms"),
        }
        for field in _SAFE_EXTRA_FIELDS:
            if field in structured:
                payload[field] = structured[field]
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def configure_logging(service: str = DEFAULT_SERVICE, level: str = "INFO") -> None:
    """配置项目日志命名空间，并保证重复创建测试 App 时不会叠加 Handler。"""

    logger = logging.getLogger(LOGGER_NAMESPACE)
    logger.setLevel(level.upper())
    logger.propagate = False

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonLogFormatter(service))
    logger.handlers.clear()
    logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """返回项目命名空间下的 Logger，便于按 Python 模块定位日志来源。"""

    return logging.getLogger(f"{LOGGER_NAMESPACE}.{name}")


def bind_request_id(request_id: str) -> Token[str]:
    """把 request_id 绑定到当前异步上下文，并返回稍后恢复上下文所需的 Token。"""

    return _request_id_context.set(request_id)


def reset_request_id(token: Token[str]) -> None:
    """请求结束后恢复旧上下文，防止 ID 泄漏到下一个请求。"""

    _request_id_context.reset(token)


def log_event(
    logger: logging.Logger,
    level: Literal["debug", "info", "warning", "error"],
    event: str,
    message: str,
    *,
    request_id: str | None = None,
    task_id: str | None = None,
    error_code: str | None = None,
    duration_ms: float | None = None,
    status: str | None = None,
    node: str | None = None,
    http_method: str | None = None,
    http_path: str | None = None,
    sequence: int | None = None,
) -> None:
    """记录一条安全的结构化事件，不接受 Prompt 或任意业务正文参数。"""

    data: dict[str, Any] = {
        "event": event,
        "request_id": request_id,
        "task_id": task_id,
        "error_code": error_code,
        "duration_ms": round(duration_ms, 2) if duration_ms is not None else None,
    }
    optional_fields = {
        "status": status,
        "node": node,
        "http_method": http_method,
        "http_path": http_path,
        "sequence": sequence,
    }
    data.update({key: value for key, value in optional_fields.items() if value is not None})
    getattr(logger, level)(message, extra={"structured_data": data})
