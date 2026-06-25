from __future__ import annotations

"""LangGraph orchestration layer.

教学要点：
- StateGraph = State + Node + Edge + Conditional Edge。
- 本项目的 State 是 `{"analysis": AnalysisState}`。
- Node 分别是 route、data_workflow、research_agent、report。
- Conditional Edge 根据 mode 决定只跑 data、只跑 research，还是 hybrid。
- SqliteSaver 用 task_id 作为 thread_id 保存图执行 checkpoint。
"""

from contextlib import AbstractContextManager
from typing import Callable
from uuid import uuid4

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

from ..data.warehouse import RetailDataWarehouse
from ..models import AnalysisMode, AnalysisState, AuditEvent, RunMode
from ..reporting.composer import ReportComposer
from ..research.agent import ResearchAgent
from ..settings import PROJECT_DIR
from ..workflows.business import FixedBusinessWorkflow


class RetailAnalysisOrchestrator:
    """Coordinates deterministic data workflow and autonomous research workflow."""

    def __init__(
        self,
        fixed_workflow: FixedBusinessWorkflow | None = None,
        research_agent: ResearchAgent | None = None,
        report_composer: ReportComposer | None = None,
        event_callback: Callable[[str, str, dict], None] | None = None,
    ) -> None:
        self.fixed_workflow = fixed_workflow or FixedBusinessWorkflow(RetailDataWarehouse())
        self.research_agent = research_agent or ResearchAgent()
        self.report_composer = report_composer or ReportComposer()
        self.event_callback = event_callback
        self._checkpointer_context: AbstractContextManager | None = None

    def run(self, question: str, mode: RunMode = "auto", task_id: str | None = None) -> AnalysisState:
        """Run the graph and return the final AnalysisState.

        `mode=auto` 时先用规则路由；真实项目可以把这一步替换为意图分类模型。
        """

        effective_mode = self._route(question) if mode == "auto" else mode
        state = AnalysisState(question=question, mode=effective_mode)
        state.audit.append(AuditEvent("orchestrator.route", "orchestrator", f"mode={effective_mode}"))
        app = self._build_graph()
        result = app.invoke(
            {"analysis": state},
            config={"configurable": {"thread_id": task_id or uuid4().hex}},
        )
        return result["analysis"]

    def _build_graph(self):
        """Build the executable LangGraph workflow.

        纯文本图：
        START -> route
        route -> data_workflow | research_agent
        data_workflow -> research_agent | report
        research_agent -> report
        report -> END
        """

        graph = StateGraph(dict)
        graph.add_node("route", self._route_node)
        graph.add_node("data_workflow", self._data_node)
        graph.add_node("research_agent", self._research_node)
        graph.add_node("report", self._report_node)
        graph.add_edge(START, "route")
        graph.add_conditional_edges(
            "route",
            self._after_route,
            {
                "data": "data_workflow",
                "research": "research_agent",
                "hybrid": "data_workflow",
            },
        )
        graph.add_conditional_edges(
            "data_workflow",
            self._after_data,
            {
                "research": "research_agent",
                "report": "report",
            },
        )
        graph.add_edge("research_agent", "report")
        graph.add_edge("report", END)
        checkpointer = self._checkpointer()
        return graph.compile(checkpointer=checkpointer)

    def _checkpointer(self):
        """Create LangGraph SqliteSaver.

        这里保存的是 LangGraph 图执行状态；TaskRepository 保存的是业务任务和报告。
        两者职责不同，生产系统也常常同时存在 workflow checkpoint 和业务表。
        """

        runtime_dir = PROJECT_DIR / "runtime"
        runtime_dir.mkdir(parents=True, exist_ok=True)
        self._checkpointer_context = SqliteSaver.from_conn_string(str(runtime_dir / "langgraph.sqlite3"))
        return self._checkpointer_context.__enter__()

    def _route_node(self, graph_state: dict) -> dict:
        """Node: record selected mode and pass state forward."""
        state: AnalysisState = graph_state["analysis"]
        self._emit("route", "Mode selected", {"mode": state.mode})
        return {"analysis": state}

    def _data_node(self, graph_state: dict) -> dict:
        """Node: run the controlled Text-to-SQL-like business workflow."""
        state: AnalysisState = graph_state["analysis"]
        self._emit("workflow_started", "Fixed business workflow started", {})
        self.fixed_workflow.run(state)
        self._emit("workflow_completed", "Fixed business workflow completed", {"blocks": len(state.data_blocks)})
        return {"analysis": state}

    def _research_node(self, graph_state: dict) -> dict:
        """Node: run the research planner and local research tools."""
        state: AnalysisState = graph_state["analysis"]
        self._emit("research_started", "Research agent started", {})
        self.research_agent.run(state)
        self._emit("research_completed", "Research agent completed", {"blocks": len(state.research_blocks)})
        return {"analysis": state}

    def _report_node(self, graph_state: dict) -> dict:
        """Node: compose final Japanese markdown report."""
        state: AnalysisState = graph_state["analysis"]
        self._emit("report_started", "Report composition started", {})
        return {"analysis": self.report_composer.run(state)}

    @staticmethod
    def _after_route(graph_state: dict) -> str:
        """Conditional edge after route: choose the first executable branch."""
        return graph_state["analysis"].mode

    @staticmethod
    def _after_data(graph_state: dict) -> str:
        """Conditional edge after data workflow: hybrid continues to research."""
        return "research" if graph_state["analysis"].mode == "hybrid" else "report"

    def _emit(self, event_type: str, message: str, payload: dict) -> None:
        if self.event_callback:
            self.event_callback(event_type, message, payload)

    @staticmethod
    def _route(question: str) -> AnalysisMode:
        has_data = any(key in question for key in ["売上", "粗利", "在庫", "欠品", "カテゴリ", "商品", "KPI"])
        has_research = any(key in question for key in ["市場", "トレンド", "競合", "報告", "会議", "リスク", "施策"])
        if has_data and has_research:
            return "hybrid"
        if has_data:
            return "data"
        if has_research:
            return "research"
        return "hybrid"
