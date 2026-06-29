"""Question 进度的 SSE HTTP 接口。

文件职责：校验问题存在，并把持久事件转换为 ``text/event-stream``。
谁调用它：Frontend ``EventSource``；它调用 QuestionService 和 SSE Generator。
输入：question_id、断线续传游标 after；输出：StreamingResponse。
为什么需要这一层：SSE 只承担通知，业务事实仍由 SQLite 中的状态和事件保存。
初学者重点：先查 Question 可得到 404，再开始长连接；after 用于跳过已消费事件。
日本现场面试：可说明禁用代理缓冲，并通过持久序号支持恢复读取。
企业级替换：可接事件总线或多实例广播，但终态和权限检查仍必须可靠。
"""

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse

from app.api.routes.dependencies import get_question_service, get_repository
from app.events.sse import stream_question_events
from app.repositories.sqlite_repository import SQLiteRepository
from app.services.question_service import QuestionService


router = APIRouter(prefix="/api/questions")


@router.get("/{question_id}/events")
async def question_events(
    question_id: str,
    after: int = Query(default=0, ge=0),
    service: QuestionService = Depends(get_question_service),
    repository: SQLiteRepository = Depends(get_repository),
) -> StreamingResponse:
    service.get_question(question_id)
    return StreamingResponse(
        stream_question_events(repository, question_id, after),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
