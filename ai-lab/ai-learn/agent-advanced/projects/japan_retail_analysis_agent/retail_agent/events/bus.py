from __future__ import annotations

"""In-process event bus for task streaming.

教学要点：
- FastAPI 后台任务发布 RunEvent。
- SSE 和 WebSocket 订阅同一个 EventBus。
- 生产系统可替换为 Redis Pub/Sub、Kafka、NATS 或云消息服务。
"""

import asyncio
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class RunEvent:
    """One progress event shared by REST history, SSE, and WebSocket."""

    task_id: str
    type: str
    message: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_json(self) -> str:
        """Serialize with Japanese text preserved for browser display."""
        return json.dumps(asdict(self), ensure_ascii=False)


class EventBus:
    """In-process pub/sub for SSE and WebSocket clients.

    这是单进程教学实现。多 worker 或多容器部署时，内存里的 subscribers
    无法共享，需要换成 Redis Pub/Sub、Kafka、NATS 等外部消息系统。
    """

    def __init__(self) -> None:
        self._history: dict[str, list[RunEvent]] = {}
        self._subscribers: dict[str, set[asyncio.Queue[RunEvent]]] = {}
        self._lock = asyncio.Lock()

    async def publish(self, event: RunEvent) -> None:
        """Store event in memory and fan out to active subscribers."""
        async with self._lock:
            self._history.setdefault(event.task_id, []).append(event)
            # 拷贝 subscriber 列表后再逐个 put，避免持锁等待慢客户端。
            subscribers = list(self._subscribers.get(event.task_id, set()))
        for queue in subscribers:
            await queue.put(event)

    async def subscribe(self, task_id: str) -> asyncio.Queue[RunEvent]:
        """Subscribe to a task and replay in-memory history first."""
        queue: asyncio.Queue[RunEvent] = asyncio.Queue()
        async with self._lock:
            self._subscribers.setdefault(task_id, set()).add(queue)
            # 先回放历史，解决“前端连接 SSE 时任务已经开始”的竞态。
            for event in self._history.get(task_id, []):
                queue.put_nowait(event)
        return queue

    async def unsubscribe(self, task_id: str, queue: asyncio.Queue[RunEvent]) -> None:
        """Remove a client queue when SSE/WebSocket disconnects."""
        async with self._lock:
            queues = self._subscribers.get(task_id)
            if not queues:
                return
            queues.discard(queue)
            if not queues:
                self._subscribers.pop(task_id, None)

    async def history(self, task_id: str) -> list[RunEvent]:
        """Return in-memory event history for one task."""
        async with self._lock:
            return list(self._history.get(task_id, []))
