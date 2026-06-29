"""Question 创建、状态查询和报告读取接口。

文件职责：把 HTTP 请求转换为 QuestionService 调用，并返回统一 API 合同。
谁调用它：React API Client 或 curl；它调用 QuestionService 和 Pydantic Schema。
输入：问题文本或 question_id；输出：202 创建结果、当前状态或正式报告。
为什么需要这一层：业务状态转换留在 Service，Route 只处理协议边界。
初学者重点：创建后执行初始 Workflow；报告未完成时由统一异常处理返回 409。
日本现场面试：可说明接收、查询、结果资源分离，request_id 贯穿调用链。
企业级替换：可将长任务交给 Queue，但 API 合同与幂等规则需保持清晰。
"""

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
