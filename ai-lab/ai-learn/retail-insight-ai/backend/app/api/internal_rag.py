"""Internal RAG HTTP 路由。

文件职责：
- 提供 `POST /api/v1/internal-rag/answer` 的 HTTP 入口。
- 保持 request / response contract 与 service 实现分离。

谁会调用它：
- FastAPI 路由系统。

它调用谁：
- `InternalRagService` 执行检索、引用校验和 deterministic answer assembly。

输入是什么：
- `InternalRagAnswerRequest`。

输出是什么：
- `ApiResponse[InternalRagAnswerResponse]`。

为什么需要这一层：
- 先固定 HTTP contract，再让 service 处理业务编排，后续接 LLM provider 时不用改路由。

日本现场面试怎么讲：
- 这是 internal RAG 的 API 边界，路由只负责把请求交给 service，不承载回答逻辑。
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_internal_rag_service
from app.observability.logging import get_request_id
from app.schemas.common import ApiResponse, success_response
from app.schemas.internal_rag_api import InternalRagAnswerRequest, InternalRagAnswerResponse
from app.services.internal_rag_service import InternalRagService
from app.security.dependencies import require_permission
from app.security.rbac_contracts import Permission

# internal RAG 路由只承载 answer 的 HTTP 入口，不负责检索排名或引用组装细节。
router = APIRouter(
    prefix="/api/v1/internal-rag",
    tags=["internal-rag"],
    dependencies=[Depends(require_permission(Permission.ANALYSIS_EXECUTE))],
)


@router.post(
    path="/answer",
    response_model=ApiResponse[InternalRagAnswerResponse],
    status_code=status.HTTP_200_OK,
)
async def answer_internal_rag(
    request: InternalRagAnswerRequest,
    service: InternalRagService = Depends(get_internal_rag_service),
) -> ApiResponse[InternalRagAnswerResponse]:
    """执行 internal RAG answer assembly，并返回稳定的 grounded citation 结果。"""

    data = service.answer(request)
    return success_response(data, get_request_id())
