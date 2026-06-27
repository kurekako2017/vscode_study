from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from time import perf_counter
from typing import Any

from langgraph.graph import END, START, StateGraph

from app.agents.research_agent import ResearchAgent
from app.kpi.workflow import FixedKPIWorkflow
from app.observability.logging import get_logger, log_event
from app.reports.generator import ReportGenerator
from app.workflow.state import AnalysisState

logger = get_logger(__name__)


class AnalysisWorkflow:
    """用 LangGraph 显式表达分析流程的 State、Node、Edge 和条件路由。

    Workflow 只负责编排，不保存 Task 的 queued/completed 生命周期。这样 Node 可以专注
    输入与状态增量，TaskService 则统一处理持久化、终态和对外事件。
    """

    def __init__(
        self,
        kpi_workflow: FixedKPIWorkflow,
        research_agent: ResearchAgent,
        report_generator: ReportGenerator,
        step_delay_seconds: float = 0.05,
    ) -> None:
        """注入各业务步骤并编译一次 StateGraph，供后续任务复用。"""

        self._kpi_workflow = kpi_workflow
        self._research_agent = research_agent
        self._report_generator = report_generator
        self._step_delay_seconds = step_delay_seconds
        self._graph = self._build_graph()

    def _build_graph(self) -> Any:
        """声明 Node 与 Edge；图结构集中在一处便于 Review 实际执行路径。"""

        builder = StateGraph(AnalysisState)
        builder.add_node("route", self._route_node)
        builder.add_node("kpi", self._kpi_node)
        builder.add_node("research", self._research_node)
        builder.add_node("report", self._report_node)

        # route 先把 API mode 转成显式路径，避免 Node 内部隐藏复杂 if/else。
        builder.add_edge(START, "route")
        builder.add_conditional_edges(
            "route",
            self._after_route,
            {"kpi": "kpi", "research": "research"},
        )
        builder.add_conditional_edges(
            "kpi",
            self._after_kpi,
            {"research": "research", "report": "report"},
        )
        builder.add_edge("research", "report")
        builder.add_edge("report", END)
        return builder.compile()

    async def _delay(self) -> None:
        """模拟节点耗时，让教学界面能够观察流式进度；生产实现不需要此延迟。"""

        if self._step_delay_seconds > 0:
            await asyncio.sleep(self._step_delay_seconds)

    async def _route_node(self, state: AnalysisState) -> dict[str, str]:
        """读取 mode 并写入 route；Node 返回增量而不是复制整个 State。"""

        await self._delay()
        return {"route": state["mode"]}

    async def _after_route(self, state: AnalysisState) -> str:
        """Research-only 跳过 KPI，其余模式先执行确定性计算。"""

        return "research" if state["route"] == "research" else "kpi"

    async def _kpi_node(self, state: AnalysisState) -> dict[str, object]:
        """执行确定性 KPI，并把结果写入 ``kpi_result``。"""

        task_id = state.get("task_id")
        started_at = perf_counter()
        log_event(
            logger,
            "info",
            "kpi_started",
            "KPI analysis started",
            task_id=task_id,
            status="running",
            node="kpi",
        )
        await self._delay()
        result = self._kpi_workflow.run(state["question"])
        log_event(
            logger,
            "info",
            "kpi_completed",
            "KPI analysis completed",
            task_id=task_id,
            status="running",
            node="kpi",
            duration_ms=(perf_counter() - started_at) * 1000,
        )
        return {"kpi_result": result}

    async def _after_kpi(self, state: AnalysisState) -> str:
        """Hybrid 继续调查，KPI-only 直接进入报告。"""

        return "research" if state["mode"] == "hybrid" else "report"

    async def _research_node(self, state: AnalysisState) -> dict[str, object]:
        """调用 Research Agent，并记录非确定性步骤的执行时间。"""

        task_id = state.get("task_id")
        started_at = perf_counter()
        log_event(
            logger,
            "info",
            "research_started",
            "Research started",
            task_id=task_id,
            status="running",
            node="research",
        )
        await self._delay()
        result = await self._research_agent.run(state["question"])
        log_event(
            logger,
            "info",
            "research_completed",
            "Research completed",
            task_id=task_id,
            status="running",
            node="research",
            duration_ms=(perf_counter() - started_at) * 1000,
        )
        return {"research_result": result}

    async def _report_node(self, state: AnalysisState) -> dict[str, str]:
        """把可选 KPI/Research 结果合成为统一 Markdown 报告。"""

        task_id = state.get("task_id")
        started_at = perf_counter()
        log_event(
            logger,
            "info",
            "report_generation_started",
            "Report generation started",
            task_id=task_id,
            status="running",
            node="report",
        )
        await self._delay()
        report_markdown = self._report_generator.generate(
            question=state["question"],
            kpi_result=state.get("kpi_result"),
            research_result=state.get("research_result"),
        )
        log_event(
            logger,
            "info",
            "report_generation_completed",
            "Report generation completed",
            task_id=task_id,
            status="running",
            node="report",
            duration_ms=(perf_counter() - started_at) * 1000,
        )
        return {"report_markdown": report_markdown}

    async def stream(self, initial_state: AnalysisState) -> AsyncIterator[tuple[str, AnalysisState]]:
        """按 Node 增量流式执行，并为 TaskService 重建当前完整 State。"""

        current_state: AnalysisState = dict(initial_state)
        # updates 模式只返回 Node patch，适合发布逐节点进度，避免重复传输整个 State。
        async for update in self._graph.astream(initial_state, stream_mode="updates"):
            for node_name, patch in update.items():
                current_state.update(patch)
                yield node_name, dict(current_state)
