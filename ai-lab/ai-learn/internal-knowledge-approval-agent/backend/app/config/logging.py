"""结构化 JSON 运行日志。

日志只接受白名单字段，避免把员工问题或报告正文误写进日志平台。

文件职责：配置 JSON Formatter、维护 request_id 上下文并提供统一 ``log_event``。
谁调用它：Main、Service 和 SSE Publisher；它调用 Python 标准 logging。
输入：事件名、级别和允许的结构化字段；输出：单行 JSON 运行日志。
为什么需要这一层：让请求和业务状态可追踪，同时阻止任意正文进入日志。
初学者重点：``ContextVar`` 隔离并发请求；``_SAFE_FIELDS`` 是额外字段白名单。
日本现场面试：可说明运行日志用于诊断，不等同不可篡改的业务 Audit Record。
企业级替换：接 OpenTelemetry/集中日志平台，并加入 trace_id 与脱敏策略。

固定字段用途：request_id 追踪 HTTP 请求，question_id 追踪业务问题，event 说明发生了
什么，status 表示当前状态，error_code 用于错误分类，duration_ms 用于性能分析。
"""

from __future__ import annotations

import json
import logging
import sys
from contextvars import ContextVar, Token
from datetime import datetime, timezone
from typing import Any, Literal


LOGGER_NAMESPACE = "knowledge_approval"
_request_id: ContextVar[str] = ContextVar("request_id", default="-")
_SAFE_FIELDS = {
    "question_id",
    "approval_id",
    "status",
    "from_status",
    "to_status",
    "node",
    "sequence",
    "http_method",
    "http_path",
}


class JsonFormatter(logging.Formatter):
    def __init__(self, service_name: str) -> None:
        super().__init__()
        self._service_name = service_name

    def format(self, record: logging.LogRecord) -> str:
        values: dict[str, Any] = getattr(record, "structured", {})
        payload: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "service": self._service_name,
            "request_id": values.get("request_id") or _request_id.get(),
            "question_id": values.get("question_id") or "-",
            "event": values.get("event", "application_log"),
            "status": values.get("status") or "-",
            "message": record.getMessage(),
            "error_code": values.get("error_code"),
            "duration_ms": values.get("duration_ms"),
        }
        for key in _SAFE_FIELDS:
            if values.get(key) is not None:
                payload[key] = values[key]
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def configure_logging(service_name: str, level: str) -> None:
    logger = logging.getLogger(LOGGER_NAMESPACE)
    logger.setLevel(level.upper())
    logger.propagate = False
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter(service_name))
    logger.handlers.clear()
    logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"{LOGGER_NAMESPACE}.{name}")


def bind_request_id(value: str) -> Token[str]:
    return _request_id.set(value)


def reset_request_id(token: Token[str]) -> None:
    _request_id.reset(token)


def get_request_id() -> str:
    return _request_id.get()


def log_event(
    logger: logging.Logger,
    level: Literal["debug", "info", "warning", "error"],
    event: str,
    message: str,
    *,
    request_id: str | None = None,
    question_id: str | None = None,
    approval_id: str | None = None,
    error_code: str | None = None,
    duration_ms: float | None = None,
    **safe_fields: Any,
) -> None:
    """记录企业可采集字段；未知字段会被 Formatter 丢弃。"""

    values = {
        "event": event,
        "request_id": request_id,
        "question_id": question_id,
        "approval_id": approval_id,
        "error_code": error_code,
        "duration_ms": round(duration_ms, 2) if duration_ms is not None else None,
        **safe_fields,
    }
    getattr(logger, level)(message, extra={"structured": values})
