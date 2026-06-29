from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from typing import Any

from langgraph.graph import END, START, StateGraph

from app.workflow.nodes import answer_generated, risk_checked
from app.workflow.state import WorkflowState


class KnowledgeApprovalWorkflow:
    """用 LangGraph 表达首次执行与审批后恢复。

    SQLite 保存长期事实；Graph 每次从数据库状态重新构造输入。因此等待审批时
    不占用线程，服务重启后也能通过 approval decision 继续执行。
    """

    def __init__(self, step_delay_seconds: float = 0.08) -> None:
        self._delay_seconds = step_delay_seconds
        self._initial_graph = self._build_initial_graph()
        self._resume_graph = self._build_resume_graph()

    def _build_initial_graph(self) -> Any:
        builder = StateGraph(WorkflowState)
        builder.add_node("risk_classifier", self._risk_classifier)
        builder.add_node("answer_generator", self._answer_generator)
        builder.add_node("approval_wait", self._approval_wait)
        builder.add_edge(START, "risk_classifier")
        builder.add_conditional_edges(
            "risk_classifier",
            self._risk_route,
            {"low": "answer_generator", "high": "approval_wait"},
        )
        builder.add_edge("answer_generator", END)
        builder.add_edge("approval_wait", END)
        return builder.compile()

    def _build_resume_graph(self) -> Any:
        builder = StateGraph(WorkflowState)
        builder.add_node("resume_route", self._resume_route_node)
        builder.add_node("approved", self._approved)
        builder.add_node("rejected", self._rejected)
        builder.add_node("answer_generator", self._answer_generator)
        builder.add_edge(START, "resume_route")
        builder.add_conditional_edges(
            "resume_route",
            self._resume_route,
            {"approved": "approved", "rejected": "rejected"},
        )
        builder.add_edge("approved", "answer_generator")
        builder.add_edge("answer_generator", END)
        builder.add_edge("rejected", END)
        return builder.compile()

    @staticmethod
    async def _resume_route_node(_: WorkflowState) -> dict[str, str]:
        """审批恢复入口只负责显式记录路由阶段。"""

        return {"status": "routing"}

    @staticmethod
    async def _resume_route(state: WorkflowState) -> str:
        return state.get("approval_decision") or "rejected"

    @staticmethod
    async def _risk_route(state: WorkflowState) -> str:
        return "high" if state["risk_level"] == "HIGH" else "low"

    async def _delay(self) -> None:
        if self._delay_seconds:
            await asyncio.sleep(self._delay_seconds)

    async def _risk_classifier(self, state: WorkflowState) -> dict[str, str]:
        await self._delay()
        return risk_checked(state)

    async def _answer_generator(self, state: WorkflowState) -> dict[str, str]:
        """固定模板生成正式报告，不调用 LLM 或外部网络。"""

        await self._delay()
        return answer_generated(state)

    async def _approval_wait(self, _: WorkflowState) -> dict[str, str]:
        await self._delay()
        return {"status": "approval_required"}

    async def _approved(self, _: WorkflowState) -> dict[str, str]:
        await self._delay()
        return {"status": "approved"}

    async def _rejected(self, _: WorkflowState) -> dict[str, str]:
        await self._delay()
        return {"status": "rejected"}

    async def stream(self, state: WorkflowState) -> AsyncIterator[tuple[str, dict[str, Any]]]:
        """updates 模式让 Service 在每个 Node 后保存状态并发布 SSE。"""

        graph = self._resume_graph if state.get("approval_decision") else self._initial_graph
        async for update in graph.astream(state, stream_mode="updates"):
            for node_name, patch in update.items():
                yield node_name, patch
