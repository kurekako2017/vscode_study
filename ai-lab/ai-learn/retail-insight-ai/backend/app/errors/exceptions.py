"""按业务场景定义可被统一处理器识别的应用异常。"""

from __future__ import annotations

from typing import Any

from app.errors.base import AppException
from app.errors.error_codes import ErrorCode


class ValidationAppException(AppException):
    """表示请求字段或业务参数未通过校验。"""

    def __init__(self, detail: dict[str, Any] | None = None) -> None:
        """返回 422，并保留经过 JSON 安全转换的字段错误。"""

        super().__init__(ErrorCode.VALIDATION_ERROR, "Request validation failed", 422, detail=detail)


class TaskNotFoundException(AppException):
    """表示指定 task_id 不存在。"""

    def __init__(self, task_id: str) -> None:
        """返回 404，同时把 task_id 保留给日志关联。"""

        super().__init__(
            ErrorCode.TASK_NOT_FOUND,
            "Task not found",
            404,
            detail={"task_id": task_id},
            task_id=task_id,
        )


class ReportNotFoundException(AppException):
    """表示任务存在，但最终报告尚未生成。"""

    def __init__(self, task_id: str) -> None:
        """返回 409，区分资源未就绪和任务不存在。"""

        super().__init__(
            ErrorCode.REPORT_NOT_FOUND,
            "Report is not ready",
            409,
            detail={"task_id": task_id},
            task_id=task_id,
        )


class InvalidTaskStateException(AppException):
    """表示 Task 状态迁移违反生命周期规则。"""

    def __init__(self, task_id: str, current: str, target: str) -> None:
        """记录当前和目标状态，帮助定位重复执行或错误恢复。"""

        super().__init__(
            ErrorCode.INVALID_TASK_STATE,
            "Invalid task state transition",
            409,
            detail={"current": current, "target": target},
            task_id=task_id,
        )


class WorkflowExecutionException(AppException):
    """表示 Workflow 出现未归类的执行失败。"""

    def __init__(self, task_id: str, detail: dict[str, Any] | None = None) -> None:
        """隐藏原始异常正文，只暴露安全的错误分类信息。"""

        super().__init__(
            ErrorCode.WORKFLOW_EXECUTION_ERROR,
            "Workflow execution failed",
            500,
            detail=detail,
            task_id=task_id,
        )


class ResearchProviderException(AppException):
    """表示 Research Provider 无法返回有效结果。"""

    def __init__(self, task_id: str | None = None, provider: str | None = None) -> None:
        """只公开 Provider 名称，不公开查询正文或外部响应。"""

        super().__init__(
            ErrorCode.RESEARCH_PROVIDER_ERROR,
            "Research provider failed",
            502,
            detail={"provider": provider} if provider else {},
            task_id=task_id,
        )


class ReportGenerationException(AppException):
    """表示报告合成阶段失败。"""

    def __init__(self, task_id: str | None = None) -> None:
        """使用稳定错误信息，避免把报告正文写入 API 或日志。"""

        super().__init__(
            ErrorCode.REPORT_GENERATION_ERROR,
            "Report generation failed",
            500,
            task_id=task_id,
        )
