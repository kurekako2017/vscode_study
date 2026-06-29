"""FastAPI 依赖注入适配层。

文件职责：从 ``application.state`` 取得容器，并向 Route 提供 Service/Repository。
谁调用它：各 API Route 的 ``Depends``；它调用启动时创建的 ``AppContainer``。
输入：当前 Request；输出：同一应用实例持有的依赖对象。
为什么需要这一层：Route 不自行 new 数据库或 Service，测试也可覆盖依赖。
初学者重点：理解 Depends 只是取得对象，不执行业务流程。
日本现场面试：可说明这是 Web Framework 与应用组合根之间的薄适配层。
企业级替换：可提供事务 Unit of Work、用户上下文和权限对象。
"""

from fastapi import Depends, Request

from app.config.container import AppContainer
from app.repositories.sqlite_repository import SQLiteRepository
from app.services.approval_service import ApprovalService
from app.services.question_service import QuestionService


async def get_container(request: Request) -> AppContainer:
    return request.app.state.container


async def get_question_service(
    container: AppContainer = Depends(get_container),
) -> QuestionService:
    return container.question_service


async def get_approval_service(
    container: AppContainer = Depends(get_container),
) -> ApprovalService:
    return container.approval_service


async def get_repository(
    container: AppContainer = Depends(get_container),
) -> SQLiteRepository:
    return container.repository
