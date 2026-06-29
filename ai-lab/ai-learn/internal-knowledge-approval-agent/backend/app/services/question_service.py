from __future__ import annotations

from time import perf_counter
from typing import Any
from uuid import uuid4

from app.config.logging import get_logger, log_event
from app.repositories.sqlite_repository import SQLiteRepository
from app.workflow.graph import KnowledgeApprovalWorkflow
from app.workflow.state import WorkflowState


logger = get_logger(__name__)


class QuestionService:
    """协调 Question 生命周期、LangGraph、审批、事件和 SQLite。"""

    def __init__(self, repository: SQLiteRepository, workflow: KnowledgeApprovalWorkflow) -> None:
        self._repository = repository
        self._workflow = workflow

    def create_question(self, question: str, request_id: str) -> dict[str, Any]:
        question_id = str(uuid4())
        item = self._repository.create_question(question_id, question.strip(), request_id)
        self._publish(question_id, "received", "Question received", request_id, status="received", node=None)
        log_event(
            logger,
            "info",
            "question_created",
            "Question created",
            request_id=request_id,
            question_id=question_id,
            status="received",
        )
        return item

    def get_question(self, question_id: str) -> dict[str, Any]:
        item = self._repository.get_question(question_id)
        if item is None:
            raise KeyError(question_id)
        approval = self._approval_for_question(question_id)
        item["approval_id"] = approval["approval_id"] if approval else None
        return item

    def get_report(self, question_id: str) -> dict[str, Any]:
        item = self.get_question(question_id)
        if item["status"] != "completed" or not item["report"]:
            raise RuntimeError("REPORT_NOT_READY")
        return {
            "question_id": question_id,
            "report": item["report"],
            "risk_level": item["risk_level"],
            "created_at": item["created_at"],
            "updated_at": item["updated_at"],
        }

    def list_approvals(self) -> list[dict[str, Any]]:
        return self._repository.list_approvals("pending")

    def get_approval_for_question(self, question_id: str) -> dict[str, Any] | None:
        return self._repository.get_approval_by_question(question_id)

    def decide_approval(self, approval_id: str, decision: str, request_id: str) -> dict[str, Any]:
        approval = self._repository.decide_approval(approval_id, decision)
        question_id = approval["question_id"]
        log_event(
            logger,
            "info",
            "approval_decided",
            "Approval decision accepted",
            request_id=request_id,
            question_id=question_id,
            approval_id=approval_id,
            status=decision,
        )
        return approval

    async def run_initial(self, question_id: str, request_id: str) -> None:
        item = self.get_question(question_id)
        state: WorkflowState = {
            "question_id": question_id,
            "question": item["question"],
            "request_id": request_id,
            "approval_decision": None,
        }
        await self._run_graph(state, request_id)

    async def resume_after_decision(self, approval_id: str, request_id: str) -> None:
        approval = self._repository.get_approval(approval_id)
        if approval is None:
            raise KeyError(approval_id)
        item = self.get_question(approval["question_id"])
        state: WorkflowState = {
            "question_id": item["question_id"],
            "question": item["question"],
            "request_id": request_id,
            "risk_level": item["risk_level"] or "HIGH",
            "approval_decision": approval["status"],
        }
        await self._run_graph(state, request_id)

    async def _run_graph(self, state: WorkflowState, request_id: str) -> None:
        started = perf_counter()
        question_id = state["question_id"]
        try:
            async for node_name, patch in self._workflow.stream(state):
                state.update(patch)  # type: ignore[typeddict-item]
                await self._apply_node(question_id, node_name, state, request_id)
            log_event(
                logger,
                "info",
                "workflow_run_finished",
                "Workflow run finished",
                request_id=request_id,
                question_id=question_id,
                status=state.get("status"),
                duration_ms=(perf_counter() - started) * 1000,
            )
        except Exception as exc:
            self._transition(question_id, "failed", request_id, error_code="WORKFLOW_EXECUTION_ERROR")
            self._publish(
                question_id,
                "error",
                "Workflow execution failed",
                request_id,
                status="failed",
                node=None,
                error_code="WORKFLOW_EXECUTION_ERROR",
            )
            log_event(
                logger,
                "error",
                "workflow_failed",
                "Workflow execution failed",
                request_id=request_id,
                question_id=question_id,
                status="failed",
                error_code="WORKFLOW_EXECUTION_ERROR",
                duration_ms=(perf_counter() - started) * 1000,
            )
            # Background task 不能把异常泄露给已经收到 202 的客户端，错误通过 SSE 返回。
            _ = exc

    async def _apply_node(
        self,
        question_id: str,
        node_name: str,
        state: WorkflowState,
        request_id: str,
    ) -> None:
        if node_name == "risk_classifier":
            self._transition(
                question_id,
                "risk_checked",
                request_id,
                risk_level=state["risk_level"],
                node=node_name,
            )
            self._publish(
                question_id,
                "risk_checked",
                f"Risk classified: {state['risk_level']}",
                request_id,
                status="risk_checked",
                node=node_name,
                risk_level=state["risk_level"],
            )
        elif node_name == "approval_wait":
            approval_id = str(uuid4())
            self._repository.create_approval(approval_id, question_id)
            self._transition(question_id, "approval_required", request_id, node=node_name)
            self._publish(
                question_id,
                "approval_required",
                "High-risk question requires approval",
                request_id,
                status="approval_required",
                node=node_name,
                approval_id=approval_id,
                risk_level=state["risk_level"],
            )
        elif node_name == "approved":
            self._transition(question_id, "approved", request_id, node=node_name)
            self._publish(
                question_id,
                "approved",
                "Approved; generating final answer",
                request_id,
                status="approved",
                node=node_name,
            )
        elif node_name == "rejected":
            self._transition(question_id, "rejected", request_id, node=node_name)
            self._publish(
                question_id,
                "rejected",
                "Question answer was rejected",
                request_id,
                status="rejected",
                node=node_name,
            )
        elif node_name == "answer_generator":
            self._publish(
                question_id,
                "answer_generated",
                "Answer generated",
                request_id,
                status="answer_generated",
                node=node_name,
            )
            self._transition(
                question_id,
                "completed",
                request_id,
                risk_level=state.get("risk_level"),
                report=state["report"],
                node=node_name,
            )
            self._publish(
                question_id,
                "completed",
                "Final report generated",
                request_id,
                status="completed",
                node=node_name,
                report_path=f"/api/questions/{question_id}/report",
            )

    def _transition(
        self,
        question_id: str,
        status: str,
        request_id: str,
        *,
        risk_level: str | None = None,
        report: str | None = None,
        error_code: str | None = None,
        node: str | None = None,
    ) -> None:
        previous = self.get_question(question_id)["status"]
        self._repository.update_question(
            question_id,
            status=status,
            risk_level=risk_level,
            report=report,
            error_code=error_code,
        )
        log_event(
            logger,
            "info" if error_code is None else "error",
            "question_status_transition",
            "Question status transitioned",
            request_id=request_id,
            question_id=question_id,
            status=status,
            from_status=previous,
            to_status=status,
            node=node,
            error_code=error_code,
        )

    def _publish(
        self,
        question_id: str,
        event_type: str,
        message: str,
        request_id: str,
        *,
        status: str,
        node: str | None,
        **data: Any,
    ) -> None:
        event = self._repository.append_event(
            question_id,
            event_type,
            message,
            {"status": status, "node": node, "error_code": data.pop("error_code", None), **data},
            request_id,
        )
        log_event(
            logger,
            "info" if event_type != "error" else "error",
            "question_event_published",
            "Question event published",
            request_id=request_id,
            question_id=question_id,
            approval_id=event.get("approval_id"),
            status=status,
            node=node,
            sequence=event["sequence"],
            error_code=event.get("error_code"),
        )

    def _approval_for_question(self, question_id: str) -> dict[str, Any] | None:
        return self._repository.get_approval_by_question(question_id)
