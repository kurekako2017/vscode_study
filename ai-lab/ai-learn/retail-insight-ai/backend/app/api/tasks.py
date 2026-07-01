from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, Depends, Query, status
from fastapi.responses import StreamingResponse

from app.api.dependencies import get_event_repository, get_task_service
from app.events.sse import stream_task_events
from app.observability.logging import get_logger, get_request_id, log_event
from app.repositories.interfaces.event_repository import EventRepository
from app.schemas.common import ApiResponse, success_response
from app.schemas.report_api import ReportResponse
from app.schemas.task_api import TaskCreateRequest, TaskCreateResponse, TaskResponse
from app.services.task_service import TaskService

router = APIRouter(prefix="/api/tasks", tags=["tasks"])
logger = get_logger(__name__)


@router.post(path="", response_model=ApiResponse[TaskCreateResponse], status_code=status.HTTP_202_ACCEPTED)
async def create_task(
    payload: TaskCreateRequest,
    background_tasks: BackgroundTasks,
    service: TaskService = Depends(get_task_service),
) -> ApiResponse[TaskCreateResponse]:
    """创建任务并把执行安排到响应后的 BackgroundTasks。"""

    task = service.create_task(payload.question, payload.mode)
    # 先返回 202，再执行分析，避免长流程占用创建任务的 HTTP 请求。
    background_tasks.add_task(service.run_task, task.task_id)
    data = TaskCreateResponse(task_id=task.task_id, status=task.status)
    return success_response(data, get_request_id())


@router.get(path="/{task_id}", response_model=ApiResponse[TaskResponse])
async def get_task(
    task_id: str,
    service: TaskService = Depends(get_task_service),
) -> ApiResponse[TaskResponse]:
    """读取任务当前状态，任务不存在时转换为稳定的 404。"""

    data = TaskResponse.from_domain(service.get_task(task_id))
    return success_response(data, get_request_id())


@router.get("/{task_id}/events")
async def get_task_events(
    task_id: str,
    after: int = Query(default=0, ge=0),
    service: TaskService = Depends(get_task_service),
    event_repository: EventRepository = Depends(get_event_repository),
) -> StreamingResponse:
    """建立 SSE 连接，从指定事件序号继续发送任务进度。"""

    service.get_task(task_id)
    log_event(
        logger,
        "info",
        "sse_connection_started",
        "SSE connection started",
        task_id=task_id,
        status="connected",
    )
    return StreamingResponse(
        stream_task_events(event_repository, task_id, after_sequence=after),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/{task_id}/report", response_model=ApiResponse[ReportResponse])
async def get_report(
    task_id: str,
    service: TaskService = Depends(get_task_service),
) -> ApiResponse[ReportResponse]:
    """返回已完成报告；尚未生成时用 409 表示资源状态冲突。"""

    data = ReportResponse.from_domain(service.get_report(task_id))
    return success_response(data, get_request_id())
