"""Approval API 的应用服务边界。

文件职责：用公开合同中的 question_id 定位审批资源，原子决定后恢复 Workflow。
谁调用它：Approval Route；它调用 QuestionService，不直接操作数据库。
输入：question_id、approved/rejected、request_id；输出：审批记录 dict。
为什么需要这一层：把审批用例从通用 Question 生命周期中提供为清晰 API。
初学者重点：先更新 pending 审批，再按持久结果恢复图；重复决定会得到 409。
日本现场面试：可说明 Route、Use Case、Workflow 三层职责分开，并保留幂等冲突语义。
企业级替换：加入当前用户、领域 RBAC、自问自批限制、草案版本和审批审计记录。
"""

from typing import Any, Literal

from app.services.question_service import QuestionService


class ApprovalService:
    """以公开 API 约定的 question_id 为键提供审批用例。"""

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
            # 未知问题、或问题不存在审批资源，都保持公开 API 的 404 语义。
            self._questions.get_question(question_id)
            raise KeyError(question_id)
        item = self._questions.decide_approval(approval["approval_id"], decision, request_id)
        await self._questions.resume_after_decision(approval["approval_id"], request_id)
        return item
