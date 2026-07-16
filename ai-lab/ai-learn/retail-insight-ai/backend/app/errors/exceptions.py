"""按业务场景定义可被统一处理器识别的应用异常。"""

from __future__ import annotations

from typing import Any

from app.errors.base import AppException
from app.errors.error_codes import ErrorCode


class ValidationAppException(AppException):
    """表示请求字段或业务参数未通过校验。"""

    def __init__(self, detail: dict[str, Any] | None = None) -> None:
        """返回 422，并保留经过 JSON 安全转换的字段错误。"""

        super().__init__(
            ErrorCode.VALIDATION_ERROR, "Request validation failed", 422, detail=detail
        )


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


class LocalDataFileException(AppException):
    """表示本地 CSV / JSON 输入缺失或格式不合法。"""

    def __init__(self, path: object, data_kind: str, reason: str) -> None:
        """只公开安全的路径和原因摘要，不暴露原始堆栈。"""

        super().__init__(
            ErrorCode.LOCAL_DATA_FILE_ERROR,
            "Local data file is invalid",
            500,
            detail={
                "path": str(path),
                "data_kind": data_kind,
                "reason": reason,
            },
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


class DocumentNotFoundException(AppException):
    """表示指定 document_id 不存在。"""

    def __init__(self, document_id: str) -> None:
        """返回 404，并把 document_id 保留给日志关联。"""

        super().__init__(
            ErrorCode.DOCUMENT_NOT_FOUND,
            "Document not found",
            404,
            detail={"document_id": document_id},
            task_id=document_id,
        )


class DocumentArchivedException(AppException):
    """表示文档已归档，当前导入或写入操作不允许继续。"""

    def __init__(self, document_id: str) -> None:
        """返回 409，并把 document_id 保留给日志关联。"""

        super().__init__(
            ErrorCode.DOCUMENT_ARCHIVED,
            "Document is archived",
            409,
            detail={"document_id": document_id},
            task_id=document_id,
        )


class DocumentImportNotFoundException(AppException):
    """表示指定 import_id 不存在。"""

    def __init__(self, import_id: str) -> None:
        """返回 404，并把 import_id 保留给日志关联。"""

        super().__init__(
            ErrorCode.DOCUMENT_IMPORT_NOT_FOUND,
            "Document import not found",
            404,
            detail={"import_id": import_id},
            task_id=import_id,
        )


class DocumentImportAlreadyRunningException(AppException):
    """表示同一文档已有导入会话正在运行。"""

    def __init__(self, document_id: str) -> None:
        """返回 409，并把 document_id 保留给日志关联。"""

        super().__init__(
            ErrorCode.IMPORT_ALREADY_RUNNING,
            "Document import already running",
            409,
            detail={"document_id": document_id},
            task_id=document_id,
        )


class DocumentNotValidatedException(AppException):
    """表示文档尚未完成导入验证，不能进入 chunk pipeline。"""

    def __init__(self, document_id: str) -> None:
        """返回 409，并把 document_id 保留给日志关联。"""

        super().__init__(
            ErrorCode.DOCUMENT_NOT_VALIDATED,
            "Document is not validated",
            409,
            detail={"document_id": document_id},
            task_id=document_id,
        )


class InvalidQueryException(AppException):
    """表示检索 query 为空或不符合冻结约束。"""

    def __init__(self, detail: dict[str, Any] | None = None) -> None:
        """返回 422，并保留安全的查询校验摘要。"""

        super().__init__(
            ErrorCode.INVALID_QUERY,
            "Query is invalid",
            422,
            detail=detail,
        )


class InvalidQuestionException(AppException):
    """表示 internal RAG 的 question 为空或不合法。"""

    def __init__(self, detail: dict[str, Any] | None = None) -> None:
        """返回 422，并保留安全的 question 校验摘要。"""

        super().__init__(
            ErrorCode.INVALID_QUESTION,
            "Question is invalid",
            422,
            detail=detail,
        )


class AIAnalysisException(AppException):
    """AI Analysis 成本、证据、幂等与 Provider 统一异常。"""

    def __init__(self, code: ErrorCode, message: str, status_code: int, detail: dict[str, Any] | None = None) -> None:
        super().__init__(code, message, status_code, detail=detail)


class InsufficientContextException(AppException):
    """表示检索返回的证据不足以生成 grounded answer。"""

    def __init__(self, detail: dict[str, Any] | None = None) -> None:
        """返回 422，并保留上下文不足的稳定原因。"""

        super().__init__(
            ErrorCode.INSUFFICIENT_CONTEXT,
            "Not enough context was found",
            422,
            detail=detail,
        )


class CitationRequiredException(AppException):
    """表示请求要求 citations，但当前结果无法提供完整引用。"""

    def __init__(self, detail: dict[str, Any] | None = None) -> None:
        """返回 400，让客户端知道必须开启或保留 citations。"""

        super().__init__(
            ErrorCode.CITATION_REQUIRED,
            "Citations are required",
            400,
            detail=detail,
        )


class PermissionDeniedException(AppException):
    """表示当前主体没有执行该操作所需的权限。"""

    def __init__(
        self,
        permission: str,
        *,
        action: str,
        resource_type: str,
        resource_id: str,
        detail: dict[str, Any] | None = None,
    ) -> None:
        """返回 403，并保留安全的权限拒绝上下文。"""

        payload = {
            "required_permission": permission,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
        }
        if detail:
            payload.update(detail)

        super().__init__(
            ErrorCode.PERMISSION_DENIED,
            "This action is not permitted",
            403,
            detail=payload,
        )


class ApprovalNotFoundException(AppException):
    """表示指定 approval_id 不存在。"""

    def __init__(self, approval_id: str) -> None:
        """返回 404，并把 approval_id 保留给日志关联。"""

        super().__init__(
            ErrorCode.APPROVAL_NOT_FOUND,
            "Approval not found",
            404,
            detail={"approval_id": approval_id},
            task_id=approval_id,
        )


class ApprovalAlreadySubmittedException(AppException):
    """表示当前报告版本已经处于 pending_approval。"""

    def __init__(self, task_id: str) -> None:
        """返回 409，并把 task_id 保留给日志关联。"""

        super().__init__(
            ErrorCode.APPROVAL_ALREADY_SUBMITTED,
            "Approval already submitted",
            409,
            detail={"task_id": task_id},
            task_id=task_id,
        )


class ApprovalAlreadyDecidedException(AppException):
    """表示审批已经有最终结果。"""

    def __init__(self, approval_id: str, status: str) -> None:
        """返回 409，并把最终状态保留给日志关联。"""

        super().__init__(
            ErrorCode.APPROVAL_ALREADY_DECIDED,
            "Approval already decided",
            409,
            detail={"approval_id": approval_id, "status": status},
            task_id=approval_id,
        )


class ApprovalRejectedReportException(AppException):
    """表示报告已经被拒绝，不能继续当前审批流。"""

    def __init__(self, task_id: str) -> None:
        """返回 409，并把 task_id 保留给日志关联。"""

        super().__init__(
            ErrorCode.APPROVAL_REJECTED,
            "Report was rejected",
            409,
            detail={"task_id": task_id},
            task_id=task_id,
        )


class MissingRejectionReasonException(AppException):
    """表示 reject 请求缺少原因。"""

    def __init__(self, approval_id: str | None = None) -> None:
        """返回 422，确保拒绝理由始终被保留。"""

        super().__init__(
            ErrorCode.MISSING_REJECTION_REASON,
            "Rejection reason is required",
            422,
            detail={"approval_id": approval_id} if approval_id else {},
            task_id=approval_id,
        )


class InvalidApprovalStateException(AppException):
    """表示审批状态迁移违反冻结状态机。"""

    def __init__(self, approval_id: str | None, current: str, target: str) -> None:
        """返回 409，帮助定位非法状态跳转。"""

        super().__init__(
            ErrorCode.INVALID_APPROVAL_STATE,
            "Invalid approval state transition",
            409,
            detail={"current": current, "target": target},
            task_id=approval_id,
        )


class ApprovalReportNotFoundException(AppException):
    """表示审批关联的报告尚不存在。"""

    def __init__(self, task_id: str) -> None:
        """返回 404，并把 task_id 保留给日志关联。"""

        super().__init__(
            ErrorCode.REPORT_NOT_FOUND_APPROVAL,
            "Report not found",
            404,
            detail={"task_id": task_id},
            task_id=task_id,
        )


class ReportRevisionConflictException(AppException):
    """表示报告版本不能在当前状态下创建修订。"""

    def __init__(self, task_id: str, current: str) -> None:
        """返回 409，并记录当前状态。"""

        super().__init__(
            ErrorCode.REPORT_REVISION_CONFLICT,
            "Report revision conflict",
            409,
            detail={"current": current},
            task_id=task_id,
        )


class AuditLogAppendException(AppException):
    """表示审计日志追加失败。"""

    def __init__(
        self, audit_log_id: str | None = None, detail: dict[str, Any] | None = None
    ) -> None:
        """返回 500，并保留安全的审计追加失败信息。"""

        super().__init__(
            ErrorCode.AUDIT_LOG_FAILED,
            "Audit log append failed",
            500,
            detail=detail,
            task_id=audit_log_id,
        )
