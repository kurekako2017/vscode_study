"""应用依赖组合根。

文件职责：根据 Settings 组装 Repository、Provider、Service 与 Security 组件。
谁调用它：``app.main.create_app()``。
它调用谁：各层稳定接口及当前 InMemory/PostgreSQL/Static/JWT 实现。
输入：可选 Settings。
输出：同一 FastAPI App 独享且类型明确的 AppContainer。
设计理由：构造关系集中，Router 只通过 Dependency 取组件，不自行 new Security Service。
日本现场面试：Authentication/RBAC 在 composition root 注入，不污染业务 Service 或 Repository。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from app.agents.providers.static_research import StaticResearchProvider
from app.agents.research_agent import ResearchAgent
from app.config.settings import Settings
from app.config.retrieval import HybridRetrievalConfig
from app.config.reranker import RerankerConfig
from app.embeddings.factory import EmbeddingProviderFactory
from app.embeddings.interface import EmbeddingProvider
from app.embeddings.service import EmbeddingService
from app.data_loaders import LocalBusinessDataLoader, LocalResearchDataLoader
from app.db.connection import PostgresConfig, PostgresConnectionFactory
from app.db.unit_of_work import InMemoryUnitOfWork, PostgresUnitOfWork
from app.events.publisher import EventPublisher
from app.kpi.workflow import FixedKPIWorkflow
from app.providers.llm_provider import LLMProvider
from app.providers.stub_llm_provider import StubLLMProvider
from app.repositories.implementations.in_memory.audit_repository import InMemoryAuditRepository
from app.repositories.implementations.in_memory.approval_repository import InMemoryApprovalRepository
from app.repositories.implementations.in_memory.document_chunk_repository import InMemoryDocumentChunkRepository
from app.repositories.implementations.in_memory.document_retrieval import (
    HybridDocumentRetrieval,
    InMemoryKeywordRetrieval,
    VectorDocumentRetrieval,
)
from app.repositories.implementations.in_memory.document_repository import InMemoryDocumentRepository
from app.repositories.implementations.in_memory.event_repository import InMemoryEventRepository
from app.repositories.implementations.in_memory.report_repository import InMemoryReportRepository
from app.repositories.implementations.in_memory.task_repository import InMemoryTaskRepository
from app.repositories.implementations.in_memory.document_import_repository import InMemoryDocumentImportRepository
from app.repositories.implementations.in_memory.upload_session_repository import InMemoryUploadSessionRepository
from app.repositories.interfaces.document_repository import DocumentRepository
from app.repositories.interfaces.document_chunk_repository import DocumentChunkRepository
from app.repositories.interfaces.document_retrieval_provider import DocumentRetrievalProvider
from app.repositories.interfaces.audit_repository import AuditRepository
from app.repositories.interfaces.approval_repository import ApprovalRepository
from app.repositories.interfaces.event_repository import EventRepository
from app.repositories.interfaces.report_repository import ReportRepository
from app.repositories.interfaces.task_repository import TaskRepository
from app.repositories.interfaces.document_import_repository import DocumentImportRepository
from app.repositories.interfaces.upload_session_repository import UploadSessionRepository
from app.repositories.interfaces.unit_of_work import UnitOfWork
from app.repositories.postgres.approval_repository import PostgresApprovalRepository
from app.repositories.postgres.audit_repository import PostgresAuditRepository
from app.repositories.postgres.document_repository import PostgresDocumentRepository
from app.repositories.postgres.document_chunk_repository import PostgresDocumentChunkRepository
from app.repositories.postgres.document_import_repository import PostgresDocumentImportRepository
from app.repositories.postgres.upload_session_repository import PostgresUploadSessionRepository
from app.repositories.postgres.event_repository import PostgresEventRepository
from app.repositories.postgres.report_repository import PostgresReportRepository
from app.repositories.postgres.task_repository import PostgresTaskRepository
from app.repositories.postgres.llm_usage_repository import PostgresLLMUsageRepository
from app.services.document_archive_service import DocumentArchiveService
from app.services.audit_service import AuditService
from app.services.approval_service import ApprovalService
from app.services.document_chunk_service import DocumentChunkService
from app.services.document_retrieval_service import DocumentRetrievalService
from app.reports.generator import ReportGenerator
from app.services.document_import_service import DocumentImportService
from app.services.document_read_service import DocumentReadService
from app.services.internal_rag_service import InternalRagService
from app.services.ai_analysis_service import AIAnalysisService
from app.services.persistent_audit_service import PersistentAuditService
from app.services.rag_answer_generator import RAGAnswerGenerator
from app.services.reranker_provider import DeterministicRerankerProvider, RerankerProvider
from app.services.reranker_service import RerankerService
from app.services.document_upload_service import DocumentUploadService
from app.services.security_service import SecurityService
from app.services.task_service import TaskService
from app.security.authentication import AuthenticationService
from app.security.authorization_service import AuthorizationService
from app.security.config import JWTConfig
from app.security.jwt_provider import PyJWTProvider
from app.security.jwt_service import JWTService
from app.security.password import PasswordService
from app.security.permission_registry import PermissionRegistry
from app.security.permission_resolver import PermissionResolver
from app.security.user_provider import DeterministicTestUserProvider
from app.workflow.graph import AnalysisWorkflow


@dataclass(frozen=True)
class AppContainer:
    """保存应用级共享依赖，保证同一个 App 内使用同一组 Repository。"""

    settings: Settings
    authentication_service: AuthenticationService
    jwt_service: JWTService
    authorization_service: AuthorizationService
    task_service: TaskService
    report_repository: ReportRepository
    approval_repository: ApprovalRepository
    approval_service: ApprovalService
    document_repository: DocumentRepository
    document_chunk_repository: DocumentChunkRepository
    document_retrieval_provider: DocumentRetrievalProvider
    embedding_provider: EmbeddingProvider
    embedding_service: EmbeddingService
    llm_provider: LLMProvider
    rag_answer_generator: RAGAnswerGenerator
    reranker_provider: RerankerProvider
    reranker_service: RerankerService
    document_retrieval_service: DocumentRetrievalService
    internal_rag_service: InternalRagService
    ai_analysis_service: AIAnalysisService
    document_import_service: DocumentImportService
    document_chunk_service: DocumentChunkService
    document_read_service: DocumentReadService
    document_archive_service: DocumentArchiveService
    document_upload_service: DocumentUploadService
    audit_repository: AuditRepository
    audit_service: AuditService
    persistent_audit_service: PersistentAuditService
    security_service: SecurityService
    event_repository: EventRepository
    document_import_repository: DocumentImportRepository
    upload_session_repository: UploadSessionRepository
    unit_of_work: UnitOfWork
    database_health_check: Callable[[], None]
    repository_backend: str


@dataclass(frozen=True)
class RepositoryBundle:
    """保证每种 backend 一次性提供完整 Repository 集合，禁止混用。"""

    task: TaskRepository
    report: ReportRepository
    event: EventRepository
    approval: ApprovalRepository
    audit: AuditRepository
    document: DocumentRepository
    chunk: DocumentChunkRepository
    document_import: DocumentImportRepository
    upload_session: UploadSessionRepository
    unit_of_work: UnitOfWork
    health_check: Callable[[], None]
    llm_usage: PostgresLLMUsageRepository | None

#   读取配置，创建Repository，创建Service，创建所有依赖，以后所有Router都会从这里拿Service
def build_container(settings: Settings | None = None) -> AppContainer:
    """在唯一组合根中连接接口与当前 InMemory/Static 实现。"""
    # 读取配置
    settings = settings or Settings()
    # 根据配置选择 InMemory 或 PostgreSQL Repository
    repositories = _build_repositories(settings)
    # Authentication 只依赖集中配置和 deterministic identity provider，不进入 Repository/RBAC。
    jwt_config = JWTConfig(
        secret_key=settings.jwt_secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm,
        access_token_expire_minutes=settings.jwt_access_token_expire_minutes,
    )
    jwt_service = JWTService(PyJWTProvider(jwt_config), jwt_config)
    authentication_service = AuthenticationService(
        DeterministicTestUserProvider(),
        PasswordService(),
        jwt_service,
    )
    # RBAC 只消费 CurrentUser.role；权限映射留在服务端，不修改 JWT Contract。
    permission_registry = PermissionRegistry()
    authorization_service = AuthorizationService(
        PermissionResolver(permission_registry), permission_registry
    )
    task_repository = repositories.task
    report_repository = repositories.report
    event_repository = repositories.event
    # 创建事件发布器，注入事件仓库
    event_publisher = EventPublisher(event_repository)
    # 创建 InMemory 实现的仓库和服务
    approval_repository = repositories.approval
    # 创建服务，注入仓库和事件发布器
    audit_repository = repositories.audit
    # 创建服务，注入仓库和事件发布器
    audit_service = AuditService(audit_repository)
    # Persistent Audit 只在 PostgreSQL enterprise mode 启用；InMemory 保持冻结。
    persistent_audit_service = PersistentAuditService(
        audit_service,
        repositories.unit_of_work,
        enabled=settings.repository_backend == "postgres",
    )
    #  创建服务，注入仓库和事件发布器
    security_service = SecurityService()
    #  创建服务，注入仓库和事件发布器
    document_repository = repositories.document
    #  创建服务，注入仓库和事件发布器
    document_chunk_repository = repositories.chunk
    #  创建服务，注入仓库和事件发布器
    keyword_retrieval = InMemoryKeywordRetrieval(
        document_repository=document_repository,
        chunk_repository=document_chunk_repository,
    )
    embedding_provider = EmbeddingProviderFactory.from_settings(settings)
    embedding_service = EmbeddingService(embedding_provider)
    vector_retrieval = VectorDocumentRetrieval(
        document_repository=document_repository,
        chunk_repository=document_chunk_repository,
        embedding_service=embedding_service,
    )
    document_retrieval_provider = HybridDocumentRetrieval(
        keyword_retrieval,
        vector_retrieval,
        HybridRetrievalConfig(
            keyword_weight=settings.hybrid_keyword_weight,
            vector_weight=settings.hybrid_vector_weight,
        ),
    )
    #  创建服务，注入仓库和事件发布器
    llm_provider = StubLLMProvider(settings.llm_stub_behavior)
    #  创建服务，注入仓库和事件发布器
    # 普通 Internal RAG 永久使用 deterministic path，环境变量不能绕过成本治理。
    rag_answer_generator = RAGAnswerGenerator(provider=None, use_llm=False)
    # Reranker 是 retrieval 之后的独立二阶段排序，不进入 Repository 或 Retrieval Service。
    reranker_provider = DeterministicRerankerProvider()
    reranker_service = RerankerService(
        reranker_provider,
        RerankerConfig(
            enabled=settings.reranker_enabled,
            provider=settings.reranker_provider,
            candidate_limit=settings.reranker_candidate_limit,
            top_k=settings.reranker_top_k,
        ),
    )
    document_import_service = DocumentImportService(
        document_repository,
        event_publisher,
        repositories.document_import,
        repositories.unit_of_work,
    )
    #  创建服务，注入仓库和事件发布器   
    document_chunk_service = DocumentChunkService(
        document_repository,
        document_chunk_repository,
        event_publisher,
        embedding_service,
    )
    document_retrieval_service = DocumentRetrievalService(
        retrieval_provider=document_retrieval_provider,
        event_publisher=event_publisher,
    )
    #  创建服务，注入仓库和事件发布器
    internal_rag_service = InternalRagService(
        retrieval_service=document_retrieval_service,
        event_publisher=event_publisher,
        answer_generator=rag_answer_generator,
        reranker_service=reranker_service,
    )
    ai_analysis_service = AIAnalysisService(
        settings=settings,
        provider=llm_provider,
        usage_repository=repositories.llm_usage,
        document_repository=document_repository,
        chunk_repository=document_chunk_repository,
        persistent_audit_service=persistent_audit_service,
        unit_of_work=repositories.unit_of_work,
    )
    approval_service = ApprovalService(
        report_repository=report_repository,
        approval_repository=approval_repository,
        event_publisher=event_publisher,
        unit_of_work=repositories.unit_of_work,
        # 企业审批并发/历史能力只在 PostgreSQL 开启，InMemory Repository 保持冻结。
        enterprise_repository=(
            approval_repository
            if settings.repository_backend == "postgres"
            else None
        ),
        authorization_service=authorization_service,
    )
    document_read_service = DocumentReadService(document_repository)
    document_archive_service = DocumentArchiveService(document_repository, event_publisher)
    document_upload_service = DocumentUploadService(
        repository=document_repository,
        event_publisher=event_publisher,
        upload_session_repository=repositories.upload_session,
        unit_of_work=repositories.unit_of_work,
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
        unit_of_work=repositories.unit_of_work,
    )
    return AppContainer(
        settings=settings,
        authentication_service=authentication_service,
        jwt_service=jwt_service,
        authorization_service=authorization_service,
        task_service=task_service,
        report_repository=report_repository,
        approval_repository=approval_repository,
        approval_service=approval_service,
        document_repository=document_repository,
        document_chunk_repository=document_chunk_repository,
        document_retrieval_provider=document_retrieval_provider,
        embedding_provider=embedding_provider,
        embedding_service=embedding_service,
        llm_provider=llm_provider,
        rag_answer_generator=rag_answer_generator,
        reranker_provider=reranker_provider,
        reranker_service=reranker_service,
        document_retrieval_service=document_retrieval_service,
        internal_rag_service=internal_rag_service,
        ai_analysis_service=ai_analysis_service,
        document_import_service=document_import_service,
        document_chunk_service=document_chunk_service,
        document_read_service=document_read_service,
        document_archive_service=document_archive_service,
        document_upload_service=document_upload_service,
        audit_repository=audit_repository,
        audit_service=audit_service,
        persistent_audit_service=persistent_audit_service,
        security_service=security_service,
        event_repository=event_repository,
        document_import_repository=repositories.document_import,
        upload_session_repository=repositories.upload_session,
        unit_of_work=repositories.unit_of_work,
        database_health_check=repositories.health_check,
        repository_backend=settings.repository_backend,
    )


def _build_repositories(
    settings: Settings,
) -> RepositoryBundle:
    """根据配置选择 InMemory 或 PostgreSQL Repository。"""

    if settings.repository_backend == "inmemory":
        return RepositoryBundle(
            task=InMemoryTaskRepository(),
            report=InMemoryReportRepository(),
            event=InMemoryEventRepository(),
            approval=InMemoryApprovalRepository(),
            audit=InMemoryAuditRepository(),
            document=InMemoryDocumentRepository(),
            chunk=InMemoryDocumentChunkRepository(),
            document_import=InMemoryDocumentImportRepository(),
            upload_session=InMemoryUploadSessionRepository(),
            unit_of_work=InMemoryUnitOfWork(),
            health_check=lambda: None,
            llm_usage=None,
        )

    connection_factory = PostgresConnectionFactory(
        PostgresConfig(
            host=settings.postgres_host,
            port=settings.postgres_port,
            db=settings.postgres_db,
            user=settings.postgres_user,
            password=settings.postgres_password,
            database_url=settings.database_url,
        )
    )
    schema_path = Path(__file__).resolve().parents[2] / "db" / "schema.sql"
    connection_factory.initialize_schema(schema_path)
    connection_factory.health_check()
    return RepositoryBundle(
        task=PostgresTaskRepository(connection_factory),
        report=PostgresReportRepository(connection_factory),
        event=PostgresEventRepository(connection_factory),
        approval=PostgresApprovalRepository(connection_factory),
        audit=PostgresAuditRepository(connection_factory),
        document=PostgresDocumentRepository(connection_factory),
        chunk=PostgresDocumentChunkRepository(connection_factory),
        document_import=PostgresDocumentImportRepository(connection_factory),
        upload_session=PostgresUploadSessionRepository(connection_factory),
        unit_of_work=PostgresUnitOfWork(connection_factory),
        health_check=connection_factory.health_check,
        llm_usage=PostgresLLMUsageRepository(connection_factory),
    )
