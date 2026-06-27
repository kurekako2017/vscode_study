from __future__ import annotations

from dataclasses import dataclass

from app.agents.providers.static_research import StaticResearchProvider
from app.agents.research_agent import ResearchAgent
from app.config.settings import Settings
from app.events.publisher import EventPublisher
from app.kpi.workflow import FixedKPIWorkflow
from app.repositories.implementations.in_memory.event_repository import InMemoryEventRepository
from app.repositories.implementations.in_memory.report_repository import InMemoryReportRepository
from app.repositories.implementations.in_memory.task_repository import InMemoryTaskRepository
from app.repositories.interfaces.event_repository import EventRepository
from app.reports.generator import ReportGenerator
from app.services.task_service import TaskService
from app.workflow.graph import AnalysisWorkflow


@dataclass(frozen=True)
class AppContainer:
    """保存应用级共享依赖，保证同一个 App 内使用同一组 Repository。"""

    settings: Settings
    task_service: TaskService
    event_repository: EventRepository


def build_container(settings: Settings | None = None) -> AppContainer:
    """在唯一组合根中连接接口与当前 InMemory/Static 实现。"""

    settings = settings or Settings()
    # 所有具体实现都只在这里出现，业务层因此可以依赖稳定接口。
    task_repository = InMemoryTaskRepository()
    report_repository = InMemoryReportRepository()
    event_repository = InMemoryEventRepository()
    event_publisher = EventPublisher(event_repository)
    research_provider = StaticResearchProvider(fail=settings.static_research_fail)
    research_agent = ResearchAgent(research_provider)
    report_generator = ReportGenerator()
    workflow = AnalysisWorkflow(
        kpi_workflow=FixedKPIWorkflow(),
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
        event_repository=event_repository,
    )
