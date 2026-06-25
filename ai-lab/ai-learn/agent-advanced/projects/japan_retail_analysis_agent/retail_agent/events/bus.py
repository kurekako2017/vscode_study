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
    task_id: str
    type: str
    message: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)


class EventBus:
    """In-process pub/sub for SSE and WebSocket clients."""

    def __init__(self) -> None:
        self._history: dict[str, list[RunEvent]] = {}
        self._subscribers: dict[str, set[asyncio.Queue[RunEvent]]] = {}
        self._lock = asyncio.Lock()

    async def publish(self, event: RunEvent) -> None:
        """Store event in memory and fan out to active subscribers."""
        async with self._lock:
            self._history.setdefault(event.task_id, []).append(event)
            subscribers = list(self._subscribers.get(event.task_id, set()))
        for queue in subscribers:
            await queue.put(event)

    async def subscribe(self, task_id: str) -> asyncio.Queue[RunEvent]:
        """Subscribe to a task and replay in-memory history first."""
        queue: asyncio.Queue[RunEvent] = asyncio.Queue()
        async with self._lock:
            self._subscribers.setdefault(task_id, set()).add(queue)
            for event in self._history.get(task_id, []):
                queue.put_nowait(event)
        return queue

    async def unsubscribe(self, task_id: str, queue: asyncio.Queue[RunEvent]) -> None:
        async with self._lock:
            queues = self._subscribers.get(task_id)
            if not queues:
                return
            queues.discard(queue)
            if not queues:
                self._subscribers.pop(task_id, None)

    async def history(self, task_id: str) -> list[RunEvent]:
        async with self._lock:
            return list(self._history.get(task_id, []))
