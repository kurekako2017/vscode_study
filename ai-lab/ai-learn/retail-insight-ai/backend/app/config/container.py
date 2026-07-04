from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.agents.providers.static_research import StaticResearchProvider
from app.agents.research_agent import ResearchAgent
from app.config.settings import Settings
from app.data_loaders import LocalBusinessDataLoader, LocalResearchDataLoader
from app.db.connection import PostgresConfig, PostgresConnectionFactory
from app.events.publisher import EventPublisher
from app.kpi.workflow import FixedKPIWorkflow
from app.repositories.implementations.in_memory.document_repository import InMemoryDocumentRepository
from app.repositories.implementations.in_memory.event_repository import InMemoryEventRepository
from app.repositories.implementations.in_memory.report_repository import InMemoryReportRepository
from app.repositories.implementations.in_memory.task_repository import InMemoryTaskRepository
from app.repositories.interfaces.document_repository import DocumentRepository
from app.repositories.interfaces.event_repository import EventRepository
from app.repositories.interfaces.report_repository import ReportRepository
from app.repositories.interfaces.task_repository import TaskRepository
from app.repositories.postgres.event_repository import PostgresEventRepository
from app.repositories.postgres.report_repository import PostgresReportRepository
from app.repositories.postgres.task_repository import PostgresTaskRepository
from app.reports.generator import ReportGenerator
from app.services.document_read_service import DocumentReadService
from app.services.document_upload_service import DocumentUploadService
from app.services.task_service import TaskService
from app.workflow.graph import AnalysisWorkflow


@dataclass(frozen=True)
class AppContainer:
    """保存应用级共享依赖，保证同一个 App 内使用同一组 Repository。"""

    settings: Settings
    task_service: TaskService
    document_repository: DocumentRepository
    document_read_service: DocumentReadService
    document_upload_service: DocumentUploadService
    event_repository: EventRepository
    repository_backend: str


def build_container(settings: Settings | None = None) -> AppContainer:
    """在唯一组合根中连接接口与当前 InMemory/Static 实现。"""

    settings = settings or Settings()
    task_repository, report_repository, event_repository = _build_repositories(settings)
    event_publisher = EventPublisher(event_repository)
    document_repository = InMemoryDocumentRepository()
    document_read_service = DocumentReadService(document_repository)
    document_upload_service = DocumentUploadService(
        repository=document_repository,
        event_publisher=event_publisher,
    )
    business_data_loader = LocalBusinessDataLoader()
    research_data_loader = LocalResearchDataLoader()
    research_provider = StaticResearchProvider(
        data_loader=research_data_loader,
        fail=settings.static_research_fail,
    )
    research_agent = ResearchAgent(research_provider)
    report_generator = ReportGenerator()
    workflow = AnalysisWorkflow(
        kpi_workflow=FixedKPIWorkflow(data_loader=business_data_loader),
        research_agent=research_agent,
        report_generator=report_generator,
        step_delay_seconds=settings.workflow_step_delay_seconds,
    )
    task_service = TaskService(
        task_repository=task_repository,
        report_repository=report_repository,
        event_publisher=event_publisher,
        workflow=workflow,
        provider_name=settings.research_provider,
    )
    return AppContainer(
        settings=settings,
        task_service=task_service,
        document_repository=document_repository,
        document_read_service=document_read_service,
        document_upload_service=document_upload_service,
        event_repository=event_repository,
        repository_backend=settings.repository_backend,
    )


def _build_repositories(
    settings: Settings,
) -> tuple[TaskRepository, ReportRepository, EventRepository]:
    """根据配置选择 InMemory 或 PostgreSQL Repository。"""

    if settings.repository_backend == "inmemory":
        return (
            InMemoryTaskRepository(),
            InMemoryReportRepository(),
            InMemoryEventRepository(),
        )

    connection_factory = PostgresConnectionFactory(
        PostgresConfig(
            host=settings.postgres_host,
            port=settings.postgres_port,
            db=settings.postgres_db,
            user=settings.postgres_user,
            password=settings.postgres_password,
        )
    )
    schema_path = Path(__file__).resolve().parents[2] / "db" / "schema.sql"
    connection_factory.initialize_schema(schema_path)
    return (
        PostgresTaskRepository(connection_factory),
        PostgresReportRepository(connection_factory),
        PostgresEventRepository(connection_factory),
    )
