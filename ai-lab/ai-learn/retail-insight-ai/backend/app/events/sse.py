from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator

from app.core.learning_trace import trace_exit, trace_step
from app.observability.logging import get_logger, log_event
from app.repositories.interfaces.event_repository import EventRepository
from app.schemas.events import TaskEventResponse

logger = get_logger(__name__)

#stream_task_events() 就是真正负责发送 SSE 数据的函数
async def stream_task_events(
    repository: EventRepository,
    task_id: str,
    after_sequence: int = 0,
) -> AsyncIterator[str]:
    """把仓库事件编码为 SSE，并在终态事件后主动结束连接。

    ``after_sequence`` 是最小断线续传边界：客户端重连时可以只读取尚未消费的事件。
    当前轮询只适合教学版 Memory Repository，生产环境应替换为可等待的新事件机制。
    """

    # 记录已经进入 SSE 事件流函数，方便初学者从 Router 继续追踪到 SSE 层。
    trace_step(
        "GET",
        f"/api/tasks/{task_id}/events",
        "SSE",
        "stream_task_events()",
        class_name="sse.py",
        method_name="stream_task_events",
        file_path="backend/app/events/sse.py",
        task_id=task_id,
        status="connected",
        label="stream_task_events()",
    )

    # cursor 保存客户端已经读取到的最后一个事件序号，避免重复发送旧事件。
    cursor = after_sequence

    # Repository 查询位于轮询循环内，但源码链只需要打印一次，避免每 0.05 秒刷屏。
    repository_trace_printed = False

    while True:
        # 第一次轮询时记录 EventRepository.list_after()，之后不再重复打印。
        if not repository_trace_printed:
            trace_step(
                "GET",
                f"/api/tasks/{task_id}/events",
                "Repository",
                "InMemoryEventRepository.list_after()",
                class_name=repository.__class__.__name__,
                method_name="list_after",
                file_path=(
                    "backend/app/repositories/implementations/"
                    "in_memory/event_repository.py"
                ),
                task_id=task_id,
                status="running",
                label="InMemoryEventRepository.list_after()",
            )
            repository_trace_printed = True

        # 只读取 sequence 大于 cursor 的新事件，实现最小断线续传。
        events = repository.list_after(task_id, cursor)

        # 按事件序号逐条转换并发送给 SSE 客户端。
        for event in events:
            # 更新 cursor，下一轮只查询当前事件之后的新事件。
            cursor = event.sequence

            # 把领域事件转换成对外返回的 SSE 数据结构。
            payload = TaskEventResponse.from_domain(event).model_dump(mode="json")

            # error 事件使用 error 日志级别，其他事件使用 info。
            level = "error" if event.event_type == "error" else "info"
            event_status = str(event.data.get("status", event.event_type))

            # 记录当前发送的是哪一个 SSE 事件，便于观察任务状态变化。
            trace_step(
                "GET",
                f"/api/tasks/{task_id}/events",
                "SSE",
                f"event {event_status}",
                class_name="sse.py",
                method_name="stream_task_events",
                file_path="backend/app/events/sse.py",
                task_id=task_id,
                status=str(event.data.get("status", "unknown")),
                sequence=event.sequence,
                error_code=(
                    event.data.get("error_code")
                    if event.event_type == "error"
                    else None
                ),
                label=f"SSE event {event.sequence}",
            )

            # 写入结构化日志，方便后续排查某个 task_id 的事件发送情况。
            log_event(
                logger,
                level,
                "sse_event_sent",
                "SSE task event sent",
                task_id=task_id,
                status=str(event.data.get("status", "unknown")),
                error_code=(
                    event.data.get("error_code")
                    if event.event_type == "error"
                    else None
                ),
                sequence=event.sequence,
            )
            #yield 可以理解成　"先把当前这条数据交给 StreamingResponse 发给浏览器，然后函数停在这里；下次有新事件时，再从这里继续执行，而不是重新从函数开头执行。"

            # SSE 使用空行分隔事件；id 让客户端记录最后成功接收的事件序号。
            #  event: 指定事件类型，客户端可通过 event.type 过滤事件。
            #  data: 事件数据，必须是 JSON 字符串，客户端可通过 JSON.parse() 解析。
            #  SSE 规范要求每条消息必须以两个换行符结尾，表示事件结束。
            #  https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#sending_events
            #  yield 语句将事件数据发送给 StreamingResponse，StreamingResponse 会把数据写入 HTTP 响应流。
            #  这里使用 f-string 格式化字符串，确保 JSON 数据中包含中文时不会被转义。
            #  例如，payload = {"message": "你好"}，json.dumps(payload, ensure_ascii=False) 会返回 '{"message": "你好"}'，而不是 '{"message": "\u4f60\u597d"}'。
            #  这样客户端接收到的 SSE 数据就可以直接解析为原始的中文字符串，而不会出现乱码。
            #  SSE 规范要求每条消息必须以两个换行符结尾，表示事件结束。
            #  yield 把这一条数据交给 StreamingResponse 的 `stream` 方法，这样客户端就可以接收到完整的 SSE 消息。 ※todo
            yield (
                f"id: {event.sequence}\n"
                f"event: {event.event_type}\n"
                f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"
            )

            # done 和 error 都表示任务已经进入终态，此时主动结束 SSE 连接。
            if event.event_type in {"done", "error"}:
                trace_exit(
                    "GET",
                    f"/api/tasks/{task_id}/events",
                    response_status=200,
                    task_id=task_id,
                    detail="SSE stream closed",
                    status=event_status,
                    error_code=(
                        event.data.get("error_code")
                        if event.event_type == "error"
                        else None
                    ),
                )
                return

        # 当前没有新事件时短暂等待，避免 while True 持续空转占用 CPU。
        await asyncio.sleep(0.05)
