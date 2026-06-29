from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator

from app.config.logging import get_logger, log_event
from app.repositories.sqlite_repository import SQLiteRepository


logger = get_logger(__name__)
TERMINAL_EVENTS = {"done", "rejected", "error"}


async def stream_question_events(
    repository: SQLiteRepository,
    question_id: str,
    after_sequence: int = 0,
) -> AsyncIterator[str]:
    """从 SQLite 按序读取事件；审批等待期间连接继续保持。"""

    cursor = after_sequence
    while True:
        events = repository.list_events_after(question_id, cursor)
        for event in events:
            cursor = int(event["sequence"])
            log_event(
                logger,
                "info",
                "sse_event_sent",
                "SSE event sent",
                request_id=event["request_id"],
                question_id=question_id,
                status=event.get("status"),
                sequence=cursor,
            )
            yield (
                f"id: {cursor}\n"
                f"event: {event['event']}\n"
                f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
            )
            if event["event"] in TERMINAL_EVENTS:
                return
        # keep-alive 可避免部分代理把空闲连接关闭。
        yield ": keep-alive\n\n"
        await asyncio.sleep(0.25)

