from __future__ import annotations

from dataclasses import dataclass

from app.config.settings import Settings
from app.repositories.sqlite_repository import SQLiteRepository
from app.services.question_service import QuestionService
from app.workflow.graph import KnowledgeApprovalWorkflow


@dataclass(frozen=True)
class AppContainer:
    settings: Settings
    repository: SQLiteRepository
    service: QuestionService


def build_container(settings: Settings | None = None) -> AppContainer:
    """唯一组合根：具体 SQLite 和 Workflow 只在这里连接。"""

    resolved = settings or Settings()
    repository = SQLiteRepository(resolved.database_path)
    repository.initialize()
    workflow = KnowledgeApprovalWorkflow(resolved.workflow_step_delay_seconds)
    service = QuestionService(repository, workflow)
    return AppContainer(resolved, repository, service)

