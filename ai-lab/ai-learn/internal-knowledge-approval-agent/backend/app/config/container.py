from __future__ import annotations

from dataclasses import dataclass

from app.config.settings import Settings
from app.repositories.sqlite_repository import SQLiteRepository
from app.services.approval_service import ApprovalService
from app.services.question_service import QuestionService
from app.workflow.graph import KnowledgeApprovalWorkflow


@dataclass(frozen=True)
class AppContainer:
    settings: Settings
    repository: SQLiteRepository
    question_service: QuestionService
    approval_service: ApprovalService

    @property
    def service(self) -> QuestionService:
        """Compatibility alias for existing callers."""
        return self.question_service


def build_container(settings: Settings | None = None) -> AppContainer:
    """唯一组合根：具体 SQLite 和 Workflow 只在这里连接。"""

    resolved = settings or Settings()
    repository = SQLiteRepository(resolved.database_path)
    repository.initialize()
    workflow = KnowledgeApprovalWorkflow(resolved.workflow_step_delay_seconds)
    question_service = QuestionService(repository, workflow)
    approval_service = ApprovalService(question_service)
    return AppContainer(resolved, repository, question_service, approval_service)
