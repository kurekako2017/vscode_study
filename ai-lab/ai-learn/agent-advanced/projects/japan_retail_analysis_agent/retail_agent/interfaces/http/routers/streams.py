from __future__ import annotations

"""Streaming interfaces.

教学要点：
- SSE 适合浏览器单向接收进度。
- WebSocket 适合更强交互，例如后续加入人工审批、取消任务、继续任务。
"""

import contextlib

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse

from ...http.dependencies import get_event_bus, get_task_service
from ....application.task_service import TaskService
from ....events.bus import EventBus


router = APIRouter(tags=["streams"])


@router.get("/api/tasks/{task_id}/events")
async def sse_events(
    task_id: str,
    service: TaskService = Depends(get_task_service),
    event_bus: EventBus = Depends(get_event_bus),
) -> StreamingResponse:
    """Stream task events as Server-Sent Events."""
    if not service.get_task(task_id):
        raise HTTPException(status_code=404, detail="task not found")

    async def stream():
        queue = await event_bus.subscribe(task_id)
        try:
            while True:
                event = await queue.get()
                yield f"event: {event.type}\ndata: {event.to_json()}\n\n"
                if event.type in {"completed", "failed"}:
                    break
        finally:
            await event_bus.unsubscribe(task_id, queue)

    return StreamingResponse(stream(), media_type="text/event-stream")


@router.websocket("/ws/tasks/{task_id}")
async def websocket_events(websocket: WebSocket, task_id: str) -> None:
    """Stream task events over WebSocket."""
    service: TaskService = websocket.app.state.task_service
    event_bus: EventBus = websocket.app.state.event_bus
    if not service.get_task(task_id):
        await websocket.close(code=1008)
        return
    await websocket.accept()
    queue = await event_bus.subscribe(task_id)
    try:
        while True:
            event = await queue.get()
            await websocket.send_text(event.to_json())
            if event.type in {"completed", "failed"}:
                break
    except WebSocketDisconnect:
        pass
    finally:
        await event_bus.unsubscribe(task_id, queue)
        with contextlib.suppress(Exception):
            await websocket.close()
