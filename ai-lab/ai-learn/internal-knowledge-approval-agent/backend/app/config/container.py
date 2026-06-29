"""应用依赖的组合根（Composition Root）。

文件职责：按固定顺序创建 Settings、SQLiteRepository、Workflow 和 Service。
谁调用它：``app.main.create_app``；它调用所有具体基础设施构造器。
输入：可选 Settings；输出：不可变的 ``AppContainer``。
为什么需要这一层：具体实现只在一处组装，业务对象不负责寻找自己的依赖。
初学者重点：从这里能看清 Backend 的对象依赖方向和启动顺序。
日本现场面试：可说明当前是单进程显式 DI，便于测试与替换。
企业级替换：Service 应进一步依赖 Repository Interface，再在这里绑定 PostgreSQL 实现。
"""

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
    """唯一组合根：具体 SQLite 和 Workflow 只在这里连接。

    输入是可选配置，输出是 Route 后续复用的完整依赖集合；函数本身不处理业务请求。
    """

    resolved = settings or Settings()
    repository = SQLiteRepository(resolved.database_path)
    repository.initialize()
    workflow = KnowledgeApprovalWorkflow(resolved.workflow_step_delay_seconds)
    question_service = QuestionService(repository, workflow)
    approval_service = ApprovalService(question_service)
    return AppContainer(resolved, repository, question_service, approval_service)
