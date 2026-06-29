from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.responses import StreamingResponse

from app.api.schemas import (
    ApiResponse,
    ApprovalResponse,
    QuestionCreateRequest,
    QuestionResponse,
    ReportResponse,
    success,
)
from app.config.container import AppContainer
from app.config.logging import get_request_id
from app.events.sse import stream_question_events
from app.repositories.sqlite_repository import SQLiteRepository
from app.services.question_service import QuestionService


router = APIRouter(prefix="/api")


async def get_container(request: Request) -> AppContainer:
    return request.app.state.container


async def get_service(container: AppContainer = Depends(get_container)) -> QuestionService:
    return container.service


async def get_repository(container: AppContainer = Depends(get_container)) -> SQLiteRepository:
    return container.repository


def question_response(item: dict[str, Any]) -> QuestionResponse:
    return QuestionResponse.model_validate(item)


def approval_response(item: dict[str, Any]) -> ApprovalResponse:
    return ApprovalResponse.model_validate(item)


@router.post(
    "/questions",
    response_model=ApiResponse[QuestionResponse],
    status_code=status.HTTP_202_ACCEPTED,
)
async def create_question(
    payload: QuestionCreateRequest,
    service: QuestionService = Depends(get_service),
) -> ApiResponse[QuestionResponse]:
    request_id = get_request_id()
    item = service.create_question(payload.question, request_id)
    # 当前本地 Workflow 很短，先完成风险路由再返回，确保 SQLite 状态已可查询。
    # 后续接入长耗时 Provider 时再迁移到可靠 Queue，而不是依赖进程内后台任务。
    await service.run_initial(item["question_id"], request_id)
    return success(question_response({**item, "approval_id": None}), request_id)


@router.get("/questions/{question_id}", response_model=ApiResponse[QuestionResponse])
async def get_question(
    question_id: str,
    service: QuestionService = Depends(get_service),
) -> ApiResponse[QuestionResponse]:
    return success(question_response(service.get_question(question_id)), get_request_id())


@router.get("/questions/{question_id}/events")
async def question_events(
    question_id: str,
    after: int = Query(default=0, ge=0),
    service: QuestionService = Depends(get_service),
    repository: SQLiteRepository = Depends(get_repository),
) -> StreamingResponse:
    service.get_question(question_id)
    return StreamingResponse(
        stream_question_events(repository, question_id, after),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.get("/questions/{question_id}/report", response_model=ApiResponse[ReportResponse])
async def get_report(
    question_id: str,
    service: QuestionService = Depends(get_service),
) -> ApiResponse[ReportResponse]:
    return success(ReportResponse.model_validate(service.get_report(question_id)), get_request_id())


@router.get("/approvals", response_model=ApiResponse[list[ApprovalResponse]])
async def list_approvals(
    service: QuestionService = Depends(get_service),
) -> ApiResponse[list[ApprovalResponse]]:
    items = [approval_response(item) for item in service.list_approvals()]
    return success(items, get_request_id())


@router.post("/approvals/{approval_id}/approve", response_model=ApiResponse[ApprovalResponse])
async def approve(
    approval_id: str,
    service: QuestionService = Depends(get_service),
) -> ApiResponse[ApprovalResponse]:
    request_id = get_request_id()
    item = service.decide_approval(approval_id, "approved", request_id)
    await service.resume_after_decision(approval_id, request_id)
    return success(approval_response(item), request_id)


@router.post("/approvals/{approval_id}/reject", response_model=ApiResponse[ApprovalResponse])
async def reject(
    approval_id: str,
    service: QuestionService = Depends(get_service),
) -> ApiResponse[ApprovalResponse]:
    request_id = get_request_id()
    item = service.decide_approval(approval_id, "rejected", request_id)
    await service.resume_after_decision(approval_id, request_id)
    return success(approval_response(item), request_id)
