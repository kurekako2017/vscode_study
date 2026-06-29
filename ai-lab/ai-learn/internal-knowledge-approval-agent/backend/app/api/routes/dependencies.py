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
