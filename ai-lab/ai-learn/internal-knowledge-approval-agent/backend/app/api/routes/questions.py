from typing import Any

from fastapi import APIRouter, Depends, status

from app.api.routes.dependencies import get_question_service
from app.config.logging import get_request_id
from app.schemas import ApiResponse, QuestionCreateRequest, QuestionResponse, ReportResponse, success
from app.services.question_service import QuestionService


router = APIRouter(prefix="/api/questions")


def question_response(item: dict[str, Any]) -> QuestionResponse:
    return QuestionResponse.model_validate(item)


@router.post("", response_model=ApiResponse[QuestionResponse], status_code=status.HTTP_202_ACCEPTED)
async def create_question(
    payload: QuestionCreateRequest,
    service: QuestionService = Depends(get_question_service),
) -> ApiResponse[QuestionResponse]:
    request_id = get_request_id()
    item = service.create_question(payload.question, request_id)
    await service.run_initial(item["question_id"], request_id)
    return success(question_response({**item, "approval_id": None}), request_id)


@router.get("/{question_id}", response_model=ApiResponse[QuestionResponse])
async def get_question(
    question_id: str,
    service: QuestionService = Depends(get_question_service),
) -> ApiResponse[QuestionResponse]:
    return success(question_response(service.get_question(question_id)), get_request_id())


@router.get("/{question_id}/report", response_model=ApiResponse[ReportResponse])
async def get_report(
    question_id: str,
    service: QuestionService = Depends(get_question_service),
) -> ApiResponse[ReportResponse]:
    return success(ReportResponse.model_validate(service.get_report(question_id)), get_request_id())
