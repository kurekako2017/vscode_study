from typing import Any, Literal

from app.services.question_service import QuestionService


class ApprovalService:
    """Approval API boundary keyed by question_id, as defined by the public contract."""

    def __init__(self, question_service: QuestionService) -> None:
        self._questions = question_service

    def list_pending(self) -> list[dict[str, Any]]:
        return self._questions.list_approvals()

    async def decide(
        self,
        question_id: str,
        decision: Literal["approved", "rejected"],
        request_id: str,
    ) -> dict[str, Any]:
        approval = self._questions.get_approval_for_question(question_id)
        if approval is None:
            # Preserve the API's not-found behavior for both unknown questions and
            # questions that do not have an approval resource.
            self._questions.get_question(question_id)
            raise KeyError(question_id)
        item = self._questions.decide_approval(approval["approval_id"], decision, request_id)
        await self._questions.resume_after_decision(approval["approval_id"], request_id)
        return item
