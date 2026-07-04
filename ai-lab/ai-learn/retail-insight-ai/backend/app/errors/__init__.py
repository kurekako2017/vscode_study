"""应用异常、错误码和 FastAPI 统一处理器。"""

from app.errors.base import AppException
from app.errors.error_codes import ErrorCode
from app.errors.exceptions import (
    DocumentArchivedException,
    DocumentImportAlreadyRunningException,
    DocumentImportNotFoundException,
    DocumentNotFoundException,
    CitationRequiredException,
    InsufficientContextException,
    InvalidQueryException,
    InvalidQuestionException,
    InvalidTaskStateException,
    LocalDataFileException,
    ReportGenerationException,
    ReportNotFoundException,
    ResearchProviderException,
    TaskNotFoundException,
    ValidationAppException,
    WorkflowExecutionException,
)

__all__ = [
    "AppException",
    "ErrorCode",
    "DocumentArchivedException",
    "DocumentImportAlreadyRunningException",
    "DocumentImportNotFoundException",
    "DocumentNotFoundException",
    "CitationRequiredException",
    "InsufficientContextException",
    "InvalidQueryException",
    "InvalidQuestionException",
    "InvalidTaskStateException",
    "LocalDataFileException",
    "ReportGenerationException",
    "ReportNotFoundException",
    "ResearchProviderException",
    "TaskNotFoundException",
    "ValidationAppException",
    "WorkflowExecutionException",
]
