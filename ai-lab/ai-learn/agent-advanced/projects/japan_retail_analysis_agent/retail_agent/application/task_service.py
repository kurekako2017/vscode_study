from __future__ import annotations

"""Application service for analysis task lifecycle.

教学要点：
- Router 不应该直接启动 Agent，也不应该直接写 DB。
- Application Service 承担 use case：创建任务、更新状态、执行后台任务、发布事件。
- 这里是后端“业务用例层”，连接 HTTP、Repository、EventBus、LangGraph Orchestrator。
"""

import asyncio
from dataclasses import asdict
from uuid import uuid4

from ..events.bus import EventBus, RunEvent
from ..infrastructure.observability.metrics import InMemoryMetrics
from ..infrastructure.repositories.task_repository import TaskRepository
from ..orchestration.orchestrator import RetailAnalysisOrchestrator


class TaskService:
    """Application service for task lifecycle and background execution.

    初学者可以把它理解成“一个业务用例”：HTTP 层告诉它要分析一个问题，
    它负责排队、执行、持久化、发事件和统计 metrics。
    """

    def __init__(
        self,
        repository: TaskRepository,
        event_bus: EventBus,
        metrics: InMemoryMetrics,
    ) -> None:
        self.repository = repository
        self.event_bus = event_bus
        self.metrics = metrics

    def create_task(self, question: str, mode: str) -> str:
        """Create a queued task and return its id.

        生产系统通常还会在这里写入 user_id、tenant_id、request_id、权限上下文。
        """

        task_id = uuid4().hex
        self.repository.create(task_id, question, mode)
        self.metrics.count_task_created()
        return task_id

    def get_task(self, task_id: str) -> dict | None:
        """Return one task row, or None when the id does not exist."""
        return self.repository.get(task_id)

    def list_tasks(self, limit: int = 20) -> list[dict]:
        """Return recent tasks for a history view."""
        return self.repository.list(limit)

    def get_events(self, task_id: str) -> list[dict]:
        """Return persisted events, used by detail pages and refresh recovery."""
        return self.repository.events(task_id)

    async def run_task(self, task_id: str, question: str, mode: str) -> None:
        """Run one analysis task in the background.

        流程：
        1. task 状态改为 running。
        2. 发布 started 事件。
        3. 在线程池中执行 LangGraph orchestrator，避免阻塞 event loop。
        4. 保存最终 report。
        5. 发布 completed 或 failed。
        """

        loop = asyncio.get_running_loop()

        async def record_event_async(event_type: str, message: str, payload: dict | None = None) -> None:
            # Async path: used when already running inside the FastAPI event loop.
            # 顺序很重要：先写 repository，再 publish。这样页面断线后仍能从 DB 读回事件。
            event = RunEvent(task_id=task_id, type=event_type, message=message, payload=payload or {})
            self.repository.save_event(task_id, asdict(event))
            self.metrics.count_event(event_type)
            await self.event_bus.publish(event)

        def record_event_from_worker(event_type: str, message: str, payload: dict | None = None) -> None:
            # Worker-thread path: persist event synchronously, then hand off publication to the event loop.
            # LangGraph 在 asyncio.to_thread 里执行，不能直接 await event_bus.publish。
            # 所以这里用 call_soon_threadsafe 把发布动作交回 FastAPI 所在的 event loop。
            event = RunEvent(task_id=task_id, type=event_type, message=message, payload=payload or {})
            self.repository.save_event(task_id, asdict(event))
            self.metrics.count_event(event_type)
            loop.call_soon_threadsafe(asyncio.create_task, self.event_bus.publish(event))

        try:
            self.repository.update_status(task_id, "running")
            await record_event_async("started", "Task started", {"mode": mode})

            def run_orchestrator():
                # The SQLite-backed warehouse must be created and used in the same worker thread.
                # 如果在主线程创建连接、工作线程使用，sqlite3 默认会抛线程错误。
                orchestrator = RetailAnalysisOrchestrator(event_callback=record_event_from_worker)
                return orchestrator.run(question, mode, task_id=task_id)

            state = await asyncio.to_thread(run_orchestrator)
            self.repository.save_state(task_id, state, "completed")
            self.metrics.count_task_completed()
            await record_event_async(
                "completed",
                "Report completed",
                {
                    "mode": state.mode,
                    "data_blocks": len(state.data_blocks),
                    "research_blocks": len(state.research_blocks),
                    "report_markdown": state.report_markdown,
                },
            )
        except Exception as exc:
            # 对外只暴露失败事件，不让异常把后台任务静默吞掉。
            # 生产系统还会记录结构化日志、trace_id，并按错误类型决定是否重试。
            self.repository.update_status(task_id, "failed")
            self.metrics.count_task_failed()
            await record_event_async("failed", "Task failed", {"error": f"{type(exc).__name__}: {exc}"})
