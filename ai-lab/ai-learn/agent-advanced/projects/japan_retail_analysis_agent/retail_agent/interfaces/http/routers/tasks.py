from __future__ import annotations

"""Task REST router.

教学要点：
- Router 只处理 HTTP 语义：request schema、response schema、404 等。
- 业务执行委托给 TaskService。
"""

import asyncio

from fastapi import APIRouter, Depends, HTTPException

from ...http.dependencies import get_task_service
from ...http.schemas import CreateTaskRequest, CreateTaskResponse, TaskDetail, TaskSummary
from ....application.task_service import TaskService


router = APIRouter(tags=["tasks"])


@router.post("/api/tasks", response_model=CreateTaskResponse)
async def create_task(
    request: CreateTaskRequest,
    service: TaskService = Depends(get_task_service),
) -> CreateTaskResponse:
    """Create a task and start background execution."""
    task_id = service.create_task(request.question, request.mode)
    asyncio.create_task(service.run_task(task_id, request.question, request.mode))
    return CreateTaskResponse(
        task_id=task_id,
        status="queued",
        sse_url=f"/api/tasks/{task_id}/events",
        websocket_url=f"/ws/tasks/{task_id}",
    )


@router.get("/api/tasks", response_model=list[TaskSummary])
async def list_tasks(service: TaskService = Depends(get_task_service)) -> list[TaskSummary]:
    """Return recent tasks for the UI history panel."""
    return [TaskSummary(**row) for row in service.list_tasks()]


@router.get("/api/tasks/{task_id}", response_model=TaskDetail)
async def get_task(task_id: str, service: TaskService = Depends(get_task_service)) -> TaskDetail:
    """Return task detail, events, and final report."""
    row = service.get_task(task_id)
    if not row:
        raise HTTPException(status_code=404, detail="task not found")
    return TaskDetail(**row, events=service.get_events(task_id))
