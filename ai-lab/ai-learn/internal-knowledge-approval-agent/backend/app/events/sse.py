"""把持久化 Question Event 编码为 SSE 数据流。

文件职责：按 sequence 轮询 SQLite、输出 SSE 帧，并在终态关闭连接。
谁调用它：Events Route；它调用 SQLiteRepository 和结构化日志。
输入：repository、question_id、起始 sequence；输出：异步字符串迭代器。
为什么需要这一层：隔离 SSE 协议格式，Service 只发布领域状态事件。
初学者重点：``id/event/data`` 组成一帧；keep-alive 不是业务事件。
日本现场面试：可说明 error、rejected、completed 都是终态，error 后不会再发 done/completed。
企业级替换：可由消息代理推送并支持 Last-Event-ID，但数据库仍是业务事实来源。
"""

from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator

from app.config.logging import get_logger, log_event
from app.repositories.sqlite_repository import SQLiteRepository


logger = get_logger(__name__)
TERMINAL_EVENTS = {"completed", "rejected", "error"}


async def stream_question_events(
    repository: SQLiteRepository,
    question_id: str,
    after_sequence: int = 0,
) -> AsyncIterator[str]:
    """从 SQLite 按序读取事件；审批等待期间连接继续保持。

    每轮先发送新业务事件，再发送注释型 keep-alive；遇到终态立即 return，保证
    ``error`` 后不会继续产生 ``completed``。
    """

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
