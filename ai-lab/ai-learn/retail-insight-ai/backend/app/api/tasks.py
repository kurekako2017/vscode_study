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

# 定义 FastAPI 应用实例
router = APIRouter(prefix="/api/tasks", tags=["tasks"])
logger = get_logger(__name__)


# 注册任务服务依赖 `get_task_service`，用于在路由中注入 TaskService 实例,参数是 FastAPI 的 Depends 函数，用于声明依赖关系。
# router 是 FastAPI 的路由器实例，用于注册路由和处理请求。Post 请求用于创建任务，Get 请求用于查询任务状态和事件流，Get 请求用于获取任务报告。
@router.post(
    path="",
    response_model=ApiResponse[TaskCreateResponse],
    status_code=status.HTTP_202_ACCEPTED,
)
# 调用服务层方法创建任务，并返回响应.
#  payload 是请求体中的数据，background_tasks 是 FastAPI 提供的后台任务处理器，service 是通过依赖注入获取的 TaskService 实例。
#  background_tasks是 FastAPI 提供的一个工具，用于在请求处理完成后执行后台任务。它允许你在响应返回给客户端后继续执行一些耗时的操作，而不会阻塞主线程。
#  service 是通过依赖注入获取的 TaskService 实例，用于处理任务相关的业务逻辑。
async def create_task(
    payload: TaskCreateRequest,
    background_tasks: BackgroundTasks,
    service: TaskService = Depends(dependency=get_task_service),
) -> ApiResponse[TaskCreateResponse]:
    """创建任务并把执行安排到响应后的 BackgroundTasks。"""

    task = service.create_task(payload.question, payload.mode)
    # 先返回 202，再执行分析，避免长流程占用创建任务的 HTTP 请求。
    background_tasks.add_task(service.run_task, task.task_id)
    data = TaskCreateResponse(task_id=task.task_id, status=task.status)
    return success_response(data, get_request_id())


# 注册任务状态查询接口
@router.get(path="/{task_id}", response_model=ApiResponse[TaskResponse])
async def get_task(
    task_id: str,
    service: TaskService = Depends(get_task_service),
) -> ApiResponse[TaskResponse]:
    """读取任务当前状态，任务不存在时转换为稳定的 404。"""
    # 调用服务层方法获取任务状态，并返回响应
    data = TaskResponse.from_domain(service.get_task(task_id))
    return success_response(data, get_request_id())


# 注册任务事件流接口
@router.get("/{task_id}/events")
async def get_task_events(
    task_id: str,
    after: int = Query(default=0, ge=0),
    service: TaskService = Depends(get_task_service),
    event_repository: EventRepository = Depends(get_event_repository),
) -> StreamingResponse:
    """建立 SSE 连接，从指定事件序号继续发送任务进度。"""
    # SSE 连接在任务不存在时返回 404，任务已完成时仍然可以继续接收事件流。
    # SSE 是长连接，客户端可以在任务完成后继续接收事件流，直到连接关闭。
    # 任务不存在时抛出异常，FastAPI 会自动转换为 404 响应。
    service.get_task(task_id)
    log_event(
        logger,
        "info",
        "sse_connection_started",
        "SSE connection started",
        task_id=task_id,
        status="connected",
    )
    # 返回 StreamingResponse，使用 stream_task_events 生成器函数作为响应体，设置媒体类型为 text/event-stream，并添加缓存控制和加速缓冲头。
    return StreamingResponse(
        stream_task_events(event_repository, task_id, after_sequence=after),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


# 注册任务报告查询接口
@router.get("/{task_id}/report", response_model=ApiResponse[ReportResponse])
async def get_report(
    task_id: str,
    service: TaskService = Depends(get_task_service),
) -> ApiResponse[ReportResponse]:
    """返回已完成报告；尚未生成时用 409 表示资源状态冲突。"""

    data = ReportResponse.from_domain(service.get_report(task_id))
    return success_response(data, get_request_id())
