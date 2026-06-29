"""LangGraph 审批工作流定义与流式执行适配器。

文件职责：定义初次执行图、审批恢复图、Node、Edge 和条件路由。
谁调用它：QuestionService；它调用 ``workflow.nodes`` 并输出每个 Node 的状态 Patch。
输入：WorkflowState；输出：``(node_name, patch)`` 异步事件流。
为什么需要这一层：把可视化业务流程从 Service 的持久化/事件副作用中分离。
初学者重点：State 是共享数据，Node 计算 Patch，Edge 决定下一步；两个图分别处理首次和恢复。
日本现场面试：可说明审批等待是持久业务状态，不占线程；恢复输入从 SQLite 重建。
企业级替换：使用正式 Checkpointer、interrupt/resume、超时重试和状态版本迁移。
"""

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
        """构建首次执行图：START → 风险分类 → 回答生成或审批等待 → END。"""

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
        """构建恢复图：根据已持久化审批决定进入批准生成或拒绝终止。"""

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
        """Node: ResumeRoute。

        输入为带 approval_decision 的 State，输出 ``status=routing``；它只显式标记恢复阶段，
        随后的条件 Edge 才读取决定。失败由 Service 统一收敛；生产可在此校验 checkpoint 版本。
        """

        return {"status": "routing"}

    @staticmethod
    async def _resume_route(state: WorkflowState) -> str:
        """条件 Edge：把审批决定映射到 approved/rejected 分支。"""

        return state.get("approval_decision") or "rejected"

    @staticmethod
    async def _risk_route(state: WorkflowState) -> str:
        """条件 Edge：HIGH 进入 approval_wait，LOW 进入 answer_generator。"""

        return "high" if state["risk_level"] == "HIGH" else "low"

    async def _delay(self) -> None:
        if self._delay_seconds:
            await asyncio.sleep(self._delay_seconds)

    async def _risk_classifier(self, state: WorkflowState) -> dict[str, str]:
        """Node 包装：输入完整 State，输出风险 Patch，并模拟可观察的处理延迟。"""

        await self._delay()
        return risk_checked(state)

    async def _answer_generator(self, state: WorkflowState) -> dict[str, str]:
        """Node 包装：固定模板生成正式报告，不调用 LLM 或外部网络。"""

        await self._delay()
        return answer_generated(state)

    async def _approval_wait(self, _: WorkflowState) -> dict[str, str]:
        """Node: ApprovalWait；输出 approval_required，Service 随后创建持久审批记录。

        需要它把 HIGH 分支停在明确等待态；失败由 Service 发布 error。企业级由 LangGraph
        interrupt + 持久 Checkpointer 表达等待和恢复。
        """

        await self._delay()
        return {"status": "approval_required"}

    async def _approved(self, _: WorkflowState) -> dict[str, str]:
        """Node: Approved；输出 approved，随后 Edge 进入 AnswerGenerator。

        生产版本应先校验审批人权限、草案版本和幂等键。
        """

        await self._delay()
        return {"status": "approved"}

    async def _rejected(self, _: WorkflowState) -> dict[str, str]:
        """Node: Rejected；输出 rejected 并通过 Edge 终止，不生成正式回答。

        生产版本可附加审批理由和策略版本，但拒绝路径仍不得发布答案。
        """

        await self._delay()
        return {"status": "rejected"}

    async def stream(self, state: WorkflowState) -> AsyncIterator[tuple[str, dict[str, Any]]]:
        """选择首次/恢复图，并以 updates 模式把每个 Node Patch 交给 Service 持久化。"""

        graph = self._resume_graph if state.get("approval_decision") else self._initial_graph
        async for update in graph.astream(state, stream_mode="updates"):
            for node_name, patch in update.items():
                yield node_name, patch
