from __future__ import annotations

from time import perf_counter
from uuid import uuid4

from app.errors.base import AppException
from app.errors.exceptions import (
    ReportNotFoundException,
    TaskNotFoundException,
    WorkflowExecutionException,
)
from app.events.publisher import EventPublisher
from app.models.report import Report
from app.models.task import Task, TaskStatus
from app.observability.logging import get_logger, log_event
from app.repositories.interfaces.report_repository import ReportRepository
from app.repositories.interfaces.task_repository import TaskRepository
from app.workflow.graph import AnalysisWorkflow
from app.workflow.state import AnalysisState

logger = get_logger(__name__)


class TaskService:
    """协调任务生命周期、Workflow、Repository 与事件发布。

    Service 层负责“先做什么、失败后如何收敛”，但不负责 KPI 公式、Research
    实现或 HTTP 格式。保持这个边界后，未来替换存储或执行器时无需改业务流程。
    """

    def __init__(
        self,
        task_repository: TaskRepository,
        report_repository: ReportRepository,
        event_publisher: EventPublisher,
        workflow: AnalysisWorkflow,
        provider_name: str = "static",
    ) -> None:
        """注入接口依赖，使 Service 不绑定 InMemory Repository 的具体实现。"""

        self._task_repository = task_repository
        self._report_repository = report_repository
        self._event_publisher = event_publisher
        self._workflow = workflow
        self._provider_name = provider_name

    def create_task(self, question: str, mode: str) -> Task:
        """建立 queued 任务并发布首个进度事件。"""

        task = Task(task_id=str(uuid4()), question=question.strip(), mode=mode)
        self._task_repository.create(task)
        log_event(
            logger,
            "info",
            "task_created",
            "Task created",
            task_id=task.task_id,
            status=task.status.value,
        )
        self._event_publisher.publish(task.task_id, "status", "Task queued", {"status": "queued"})
        log_event(
            logger,
            "info",
            "task_queued",
            "Task entered queued state",
            task_id=task.task_id,
            status=task.status.value,
        )
        return task

    def get_task(self, task_id: str) -> Task:
        """读取任务，并把 Repository 的 ``None`` 转成明确领域异常。"""

        task = self._task_repository.get(task_id)
        if task is None:
            raise TaskNotFoundException(task_id)
        return task

    def get_report(self, task_id: str) -> Report:
        """读取报告，同时区分“任务不存在”和“报告未就绪”。"""

        self.get_task(task_id)
        report = self._report_repository.get(task_id)
        if report is None:
            raise ReportNotFoundException(task_id)
        return report

    async def run_task(self, task_id: str) -> None:
        """执行完整分析流程，并保证成功或失败都落到终态和 SSE 事件。"""

        started_at = perf_counter()
        task = self.get_task(task_id)
        try:
            task.transition(TaskStatus.RUNNING)
            self._task_repository.save(task)
            log_event(
                logger,
                "info",
                "task_running",
                "Task entered running state",
                task_id=task_id,
                status=task.status.value,
            )
            self._event_publisher.publish(
                task_id,
                "status",
                "Task started",
                {"status": "running"},
            )

            # Workflow State 只放节点协作需要的数据，任务生命周期仍由 TaskService 持有。
            initial_state: AnalysisState = {
                "task_id": task.task_id,
                "question": task.question,
                "mode": task.mode,
            }
            final_state = initial_state
            messages = {
                "route": "Route selected",
                "kpi": "KPI analysis completed",
                "research": "Research completed",
                "report": "Report generated",
            }

            # 每个 Node 完成时发布进度；前端无需理解 LangGraph 内部实现。
            async for node_name, state in self._workflow.stream(initial_state):
                final_state = state
                self._event_publisher.publish(
                    task_id,
                    "status",
                    messages[node_name],
                    {"status": "running", "node": node_name},
                )

            report = Report(
                task_id=task_id,
                markdown=final_state["report_markdown"],
                provider=self._provider_name,
            )
            self._report_repository.save(report)
            task.transition(TaskStatus.COMPLETED)
            self._task_repository.save(task)
            duration_ms = (perf_counter() - started_at) * 1000
            log_event(
                logger,
                "info",
                "task_completed",
                "Task completed",
                task_id=task_id,
                status=task.status.value,
                duration_ms=duration_ms,
            )
            self._event_publisher.publish(
                task_id,
                "done",
                "Task completed",
                {"status": "completed", "report_path": f"/api/tasks/{task_id}/report"},
            )
        except Exception as exc:
            # 所有异常在此收敛为 failed，避免任务永远停留在 running。
            failure = (
                exc
                if isinstance(exc, AppException)
                else WorkflowExecutionException(
                    task_id,
                    detail={"exception_type": type(exc).__name__},
                )
            )
            task = self.get_task(task_id)
            task.transition(TaskStatus.FAILED, error=failure.message)
            self._task_repository.save(task)
            log_event(
                logger,
                "error",
                "task_failed",
                "Task execution failed",
                task_id=task_id,
                status=task.status.value,
                error_code=failure.error_code.value,
                duration_ms=(perf_counter() - started_at) * 1000,
            )
            self._event_publisher.publish(
                task_id,
                "error",
                failure.message,
                {
                    "status": "failed",
                    "error_code": failure.error_code.value,
                },
            )
