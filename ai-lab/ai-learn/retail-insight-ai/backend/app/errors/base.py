"""所有可预期应用异常的共同基类。"""

from __future__ import annotations

from typing import Any

from app.errors.error_codes import ErrorCode


class AppException(Exception):
    """携带 HTTP、日志和 SSE 都需要的标准错误信息。"""

    def __init__(
        self,
        error_code: ErrorCode,
        message: str,
        status_code: int,
        *,
        detail: dict[str, Any] | None = None,
        request_id: str | None = None,
        task_id: str | None = None,
    ) -> None:
        """保存安全、结构化的错误字段，不要求调用方暴露原始异常正文。"""

        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.status_code = status_code
        self.detail = detail or {}
        self.request_id = request_id
        self.task_id = task_id
