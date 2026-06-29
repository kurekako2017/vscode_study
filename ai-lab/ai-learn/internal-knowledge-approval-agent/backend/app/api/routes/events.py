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
