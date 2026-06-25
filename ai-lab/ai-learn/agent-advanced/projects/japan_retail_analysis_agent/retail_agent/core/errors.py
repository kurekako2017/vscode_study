from __future__ import annotations


class AppError(Exception):
    status_code = 500
    code = "internal_error"

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class TaskNotFoundError(AppError):
    status_code = 404
    code = "task_not_found"


class TaskExecutionError(AppError):
    status_code = 500
    code = "task_execution_failed"

