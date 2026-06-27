from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator

from app.repositories.interfaces.event_repository import EventRepository
from app.observability.logging import get_logger, log_event
from app.schemas.events import TaskEventResponse

logger = get_logger(__name__)


async def stream_task_events(
    repository: EventRepository,
    task_id: str,
    after_sequence: int = 0,
) -> AsyncIterator[str]:
    """把仓库事件编码为 SSE，并在终态事件后主动结束连接。

    ``after_sequence`` 是最小断线续传边界：客户端重连时可以只读取尚未消费的事件。
    当前轮询只适合教学版 Memory Repository，生产环境应替换为可等待的新事件机制。
    """

    cursor = after_sequence
    while True:
        events = repository.list_after(task_id, cursor)
        for event in events:
            cursor = event.sequence
            payload = TaskEventResponse.from_domain(event).model_dump(mode="json")
            level = "error" if event.event_type == "error" else "info"
            log_event(
                logger,
                level,
                "sse_event_sent",
                "SSE task event sent",
                task_id=task_id,
                status=str(event.data.get("status", "unknown")),
                error_code=event.data.get("error_code") if event.event_type == "error" else None,
                sequence=event.sequence,
            )
            # SSE 使用空行分隔事件；id 让客户端能记录最后成功接收的位置。
            yield (
                f"id: {event.sequence}\n"
                f"event: {event.event_type}\n"
                f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"
            )
            if event.event_type in {"done", "error"}:
                return
        await asyncio.sleep(0.05)
