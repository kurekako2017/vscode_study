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
from app.core.learning_trace import finalize_learning_trace, trace_request_body, trace_step
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
    # 初始化参数，包括仓库、报告库和事件
    def __init__(
        self,
        task_repository: TaskRepository,         # 任务仓库接口
        report_repository: ReportRepository,        # 报告仓库接口
        event_publisher: EventPublisher,         # 事件发布器接口
        workflow: AnalysisWorkflow,                # 分析工作流接口
        provider_name: str = "static",              # 分析报告提供者名称
    ) -> None:
        """注入接口依赖，使 Service 不绑定 InMemory Repository 的具体实现。"""

        self._task_repository = task_repository
        self._report_repository = report_repository
        self._event_publisher = event_publisher
        self._workflow = workflow
        self._provider_name = provider_name

    def create_task(self, question: str, mode: str) -> Task:
        """建立 queued 任务并发布首个进度事件。"""
        # 生成唯一任务 ID，避免前端重复提交时覆盖已有任务。
        task = Task(task_id=str(uuid4()), question=question.strip(), mode=mode)
        trace_request_body(
            "POST",  # HTTP 方法
            "/api/tasks",  # API 路径
            question=task.question,  # 用户问题
            mode=task.mode,  # 分析模式
            task_id=task.task_id,  # 当前任务ID
        )
        trace_step(
            "POST",  # HTTP 方法
            "/api/tasks",  # API 路径
            "Service",  # Learning Trace 分类
            "TaskService.create_task()",  # 当前执行步骤
            class_name="TaskService",  # 当前执行类
            method_name="create_task",  # 当前执行方法
            file_path="backend/app/services/task_service.py",  # 源码文件
            task_id=task.task_id,  # 当前任务ID
        )
        # 创建任务并保存到 Repository。
        self._task_repository.create(task)
        trace_step(
            "POST",  # HTTP 方法
            "/api/tasks",  # API 路径
            "Repository",  # Learning Trace 分类
            "TaskRepository.create()",  # 当前执行步骤
            class_name="TaskRepository",  # 当前执行类
            method_name="create",  # 当前执行方法
            file_path="backend/app/repositories/implementations/in_memory/task_repository.py",  # 源码文件
            task_id=task.task_id,  # 当前任务ID
        )
        log_event(
            logger,  # logger
            "info",  # level
            "task_created",  # event
            "Task created",  # message
            task_id=task.task_id,  # 当前任务ID
            status=task.status.value,  # 当前任务状态
        )
        # 发布 queued 事件给 SSE，方便前端立即显示任务状态。
        self._event_publisher.publish(  # 发布 queued 事件给 SSE。
            task.task_id,  # 当前任务ID
            "status",  # event_type
            "Task queued",  # message
            {"status": "queued"},  # event data
        )
        trace_step(
            "POST",  # HTTP 方法
            "/api/tasks",  # API 路径
            "Event",  # Learning Trace 分类
            "publish queued event",  # 当前执行步骤
            class_name="EventPublisher",  # 当前执行类
            method_name="publish",  # 当前执行方法
            file_path="backend/app/events/publisher.py",  # 源码文件
            task_id=task.task_id,  # 当前任务ID
            status="queued",  # 当前任务状态
        )
        log_event(
            logger,  # logger
            "info",  # level
            "task_queued",  # event
            "Task entered queued state",  # message
            task_id=task.task_id,  # 当前任务ID
            status=task.status.value,  # 当前任务状态
        )
        return task

    def get_task(self, task_id: str, *, emit_trace: bool = True, trace_phase: str = "http") -> Task:
        """读取任务，并把 Repository 的 ``None`` 转成明确领域异常。"""

        if emit_trace:
            trace_step(
                "GET",  # HTTP 方法
                f"/api/tasks/{task_id}",  # API 路径
                "Service",  # Learning Trace 分类
                "TaskService.get_task()",  # 当前执行步骤
                class_name="TaskService",  # 当前执行类
                method_name="get_task",  # 当前执行方法
                file_path="backend/app/services/task_service.py",  # 源码文件
                task_id=task_id,  # 当前任务ID
                phase=trace_phase,  # 执行阶段
            )
        # 读取任务，如果不存在则抛出 TaskNotFoundException。    
        task = self._task_repository.get(task_id)
        if emit_trace:
            trace_step(
                "GET",  # HTTP 方法
                f"/api/tasks/{task_id}",  # API 路径
                "Repository",  # Learning Trace 分类
                "TaskRepository.get()",  # 当前执行步骤
                class_name="TaskRepository",  # 当前执行类
                method_name="get",  # 当前执行方法
                file_path="backend/app/repositories/implementations/in_memory/task_repository.py",  # 源码文件
                task_id=task_id,  # 当前任务ID
                status="found" if task is not None else "missing",  # 查询结果
                phase=trace_phase,  # 执行阶段
            )
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
        # 记录任务开始时间，方便计算耗时。
        started_at = perf_counter()
        # 读取任务并进入 running 状态，保存到 Repository。
        task = self.get_task(task_id, emit_trace=False)
        try:
            # 进入 running 状态，避免前端长时间停留在 queued。
            task.transition(TaskStatus.RUNNING)
            # 记录任务状态变更到 Repository。
            self._task_repository.save(task)
            trace_step(
                "POST",  # HTTP 方法
                "/api/tasks",  # API 路径
                "Repository",  # Learning Trace 分类
                "TaskRepository.save()",  # 当前执行步骤
                class_name="TaskRepository",  # 当前执行类
                method_name="save",  # 当前执行方法
                file_path="backend/app/repositories/implementations/in_memory/task_repository.py",  # 源码文件
                task_id=task_id,  # 当前任务ID
                status=task.status.value,  # 当前任务状态
                phase="background",  # 执行阶段
            )
            log_event(
                logger,  # logger
                "info",  # level
                "task_running",  # event
                "Task entered running state",  # message
                task_id=task_id,  # 当前任务ID
                status=task.status.value,  # 当前任务状态
            )
            # 发布 running 事件给 SSE，方便前端显示任务状态。
            self._event_publisher.publish(
                task_id,  # 当前任务ID
                "status",  # event_type
                "Task started",  # message
                {"status": "running"},  # event data
            )
            trace_step(
                "POST",  # HTTP 方法
                "/api/tasks",  # API 路径
                "Event",  # Learning Trace 分类
                "publish running event",  # 当前执行步骤
                class_name="EventPublisher",  # 当前执行类
                method_name="publish",  # 当前执行方法
                file_path="backend/app/events/publisher.py",  # 源码文件
                task_id=task_id,  # 当前任务ID
                status="running",  # 当前任务状态
                phase="background",  # 执行阶段
            )

            initial_state: AnalysisState = {
                "task_id": task.task_id,
                "question": task.question,
                "mode": task.mode,
            }
            final_state = initial_state
            trace_step(
                "POST",  # HTTP 方法
                "/api/tasks",  # API 路径
                "Workflow",  # Learning Trace 分类
                "AnalysisWorkflow.stream()",  # 当前执行步骤
                class_name="AnalysisWorkflow",  # 当前执行类
                method_name="stream",  # 当前执行方法
                file_path="backend/app/workflow/graph.py",  # 源码文件
                task_id=task_id,  # 当前任务ID
                phase="background",  # 执行阶段
            )
            messages = {
                "route": "Route selected",
                "kpi": "KPI analysis completed",
                "research": "Research completed",
                "report": "Report generated",
            }
            # 迭代 Workflow 流程，逐步发布进度事件。
            async for node_name, state in self._workflow.stream(initial_state):
                final_state = state
                self._event_publisher.publish(
                    task_id,  # 当前任务ID
                    "status",  # event_type
                    messages[node_name],  # message
                    {"status": "running", "node": node_name},  # event data
                )
            # 生成报告并保存到 Repository。
            report = Report(
                task_id=task_id,
                markdown=final_state["report_markdown"],
                provider=self._provider_name,
            )
            self._report_repository.save(report)
            task.transition(TaskStatus.COMPLETED)
            self._task_repository.save(task)
            trace_step(
                "POST",  # HTTP 方法
                "/api/tasks",  # API 路径
                "Repository",  # Learning Trace 分类
                "TaskRepository.save()",  # 当前执行步骤
                class_name="TaskRepository",  # 当前执行类
                method_name="save",  # 当前执行方法
                file_path="backend/app/repositories/implementations/in_memory/task_repository.py",  # 源码文件
                task_id=task_id,  # 当前任务ID
                status=task.status.value,  # 当前任务状态
                phase="background",  # 执行阶段
            )
            duration_ms = (perf_counter() - started_at) * 1000
            log_event(
                logger,  # logger
                "info",  # level
                "task_completed",  # event
                "Task completed",  # message
                task_id=task_id,  # 当前任务ID
                status=task.status.value,  # 当前任务状态
                duration_ms=duration_ms,  # 耗时
            )
            self._event_publisher.publish(
                task_id,  # 当前任务ID
                "done",  # event_type
                "Task completed",  # message
                {"status": "completed", "report_path": f"/api/tasks/{task_id}/report"},  # event data
            )
            trace_step(
                "POST",  # HTTP 方法
                "/api/tasks",  # API 路径
                "Event",  # Learning Trace 分类
                "publish completed event",  # 当前执行步骤
                class_name="EventPublisher",  # 当前执行类
                method_name="publish",  # 当前执行方法
                file_path="backend/app/events/publisher.py",  # 源码文件
                task_id=task_id,  # 当前任务ID
                status="completed",  # 当前任务状态
                phase="background",  # 执行阶段
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
            task = self.get_task(task_id, emit_trace=False)
            task.transition(TaskStatus.FAILED, error=failure.message)
            self._task_repository.save(task)
            trace_step(
                "POST",  # HTTP 方法
                "/api/tasks",  # API 路径
                "Repository",  # Learning Trace 分类
                "TaskRepository.save()",  # 当前执行步骤
                class_name="TaskRepository",  # 当前执行类
                method_name="save",  # 当前执行方法
                file_path="backend/app/repositories/implementations/in_memory/task_repository.py",  # 源码文件
                task_id=task_id,  # 当前任务ID
                status=task.status.value,  # 当前任务状态
                error_code=failure.error_code.value,  # 错误码
                phase="background",  # 执行阶段
            )
            log_event(
                logger,  # logger
                "error",  # level
                "task_failed",  # event
                "Task execution failed",  # message
                task_id=task_id,  # 当前任务ID
                status=task.status.value,  # 当前任务状态
                error_code=failure.error_code.value,  # 错误码
                duration_ms=(perf_counter() - started_at) * 1000,  # 耗时
            )
            self._event_publisher.publish(
                task_id,  # 当前任务ID
                "error",  # event_type
                failure.message,  # message
                {
                    "status": "failed",  # 当前任务状态
                    "error_code": failure.error_code.value,  # 错误码
                },
            )
        finally:
            finalize_learning_trace()
