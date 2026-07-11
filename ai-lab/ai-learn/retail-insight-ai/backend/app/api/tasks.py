from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, Depends, Query, status
from fastapi.responses import StreamingResponse

from app.api.dependencies import get_event_repository, get_task_service
from app.core.learning_trace import trace_source_chain, trace_step
from app.events.sse import stream_task_events
from app.observability.logging import get_logger, get_request_id, log_event
from app.repositories.interfaces.event_repository import EventRepository
from app.schemas.common import ApiResponse, success_response
from app.schemas.report_api import ReportResponse
from app.schemas.task_api import TaskCreateRequest, TaskCreateResponse, TaskResponse
from app.services.task_service import TaskService

# 定义 tasks 路由器。
router = APIRouter(prefix="/api/tasks", tags=["tasks"])
logger = get_logger(__name__)

#   
@router.post(
    path="",
    response_model=ApiResponse[TaskCreateResponse],
    status_code=status.HTTP_202_ACCEPTED,
)
# 创建任务并返回一个响应。
async def create_task(
    payload: TaskCreateRequest,                                 # 请求体中的任务创建请求。
    background_tasks: BackgroundTasks,                          # FastAPI 提供的 BackgroundTasks，用于安排后台任务。
    service: TaskService = Depends(dependency=get_task_service),    # 依赖注入获取任务服务。
) -> ApiResponse[TaskCreateResponse]:
    """创建任务并把执行安排到响应后的 BackgroundTasks。"""

    trace_source_chain(
        "POST",  # HTTP 方法
        "/api/tasks",  # API 路径
        [
            ("backend/app/api/tasks.py", 'router = APIRouter(prefix="/api/tasks")'),  # 路由定义
            ("", '@router.post("")'),  # POST 入口
            ("", "create_task()"),  # 当前执行步骤
        ],
    )
    # 创建任务并安排后台执行。  
    task = service.create_task(payload.question, payload.mode)
    # 安排后台任务执行，避免阻塞响应。
    background_tasks.add_task(service.run_task, task.task_id)
    trace_step(
        "POST",  # HTTP 方法
        "/api/tasks",  # API 路径
        "Router",  # Learning Trace 分类
        "BackgroundTasks.add_task()",  # 当前执行步骤
        class_name="BackgroundTasks",  # 当前执行类
        method_name="add_task",  # 当前执行方法
        file_path="backend/app/api/tasks.py",  # 源码文件
        task_id=task.task_id,  # 当前任务ID
        label="BackgroundTasks.add_task()",
    )
    data = TaskCreateResponse(task_id=task.task_id, status=task.status)
    response = success_response(data, get_request_id())
    return response


@router.get(path="/{task_id}", response_model=ApiResponse[TaskResponse])
async def get_task(
    task_id: str,
    service: TaskService = Depends(get_task_service),
) -> ApiResponse[TaskResponse]:
    """读取任务当前状态，任务不存在时转换为稳定的 404。"""
    trace_step(
        "GET",  # HTTP 方法
        f"/api/tasks/{task_id}",  # API 路径
        "Router",  # Learning Trace 分类
        "get_task()",  # 当前执行步骤
        class_name="tasks.py",  # 当前执行类
        method_name="get_task",  # 当前执行方法
        file_path="backend/app/api/tasks.py",  # 源码文件
        task_id=task_id,  # 当前任务ID
    )
    data = TaskResponse.from_domain(service.get_task(task_id))
    response = success_response(data, get_request_id())
    trace_step(
        "GET",  # HTTP 方法
        f"/api/tasks/{task_id}",  # API 路径
        "Schema(Response Model)",  # Learning Trace 分类
        "TaskResponse.from_domain()",  # 当前执行步骤
        class_name="TaskResponse",  # 当前执行类
        method_name="from_domain",  # 当前执行方法
        file_path="backend/app/schemas/task_api.py",  # 源码文件
        task_id=task_id,  # 当前任务ID
    )
    return response

#   Router（接口）、StreamingResponse（建立连接） 和 stream_task_events（发送事件）
@router.get("/{task_id}/events")
async def get_task_events(
    task_id: str,
    after: int = Query(default=0, ge=0),
    service: TaskService = Depends(get_task_service),
    event_repository: EventRepository = Depends(get_event_repository),
) -> StreamingResponse:
    """建立 SSE 连接，从指定事件序号继续发送任务进度。"""
    trace_step(
        "GET",  # HTTP 方法
        f"/api/tasks/{task_id}/events",  # API 路径
        "Router",  # Learning Trace 分类
        "get_task_events()",  # 当前执行步骤
        class_name="tasks.py",  # 当前执行类
        method_name="get_task_events",  # 当前执行方法
        file_path="backend/app/api/tasks.py",  # 源码文件
        task_id=task_id,  # 当前任务ID
    )
    # 确认任务存在，否则 SSE 连接会一直挂起。
    service.get_task(task_id)
    log_event(
        logger,
        "info",
        "sse_connection_started",
        "SSE connection started",
        task_id=task_id,
        status="connected",
    )
    # 发送 SSE 消息  
    return StreamingResponse(
        # stream_task_events() 是一个生成器函数，返回一个异步迭代器，用于逐条发送任务事件。
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
