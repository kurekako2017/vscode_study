"""可独立测试的 Workflow 领域 Node。

文件职责：实现风险判断与回答生成两个纯业务步骤。
谁调用它：``KnowledgeApprovalWorkflow`` 的异步包装方法。
它调用谁：Risk Policy、Retriever 和 Static Answer Generator。
输入：WorkflowState；输出：只包含本 Node 产生字段的状态 Patch。
为什么需要这一层：Graph 负责路由，Node 负责业务计算，两者可分别测试和替换。
初学者重点：先读 ``state.py``，再比较两个函数分别读写哪些字段。
日本现场面试：可说明 Node 合同明确、无隐藏全局状态，便于评估和失败定位。
企业级替换：风险 Node 接 Policy Engine；回答 Node 接 ACL RAG 与受控 LLM Provider。
"""

from app.agents.answer_generator import generate_answer
from app.approval.policy import classify_risk
from app.rag.retriever import retrieve_documents
from app.workflow.state import WorkflowState


def risk_checked(state: WorkflowState) -> dict[str, str]:
    """Node: RiskClassifier。

    输入 State：``question``；输出 Patch：``risk_level``、``status=risk_checked``。
    状态变化：received/routing → risk_checked；用于决定低风险直出或高风险审批。
    失败处理：异常由 QuestionService 收敛为 failed，并发布唯一终态 error 事件。
    企业级替换：版本化规则表、Policy Engine 或经过离线评估的分类器。
    """

    return {"risk_level": classify_risk(state["question"]), "status": "risk_checked"}


def answer_generated(state: WorkflowState) -> dict[str, str]:
    """Node: AnswerGenerator。

    输入 State：``question``、``risk_level`` 和可选 ``approval_decision``。
    输出 Patch：``status=completed``、``report``；内部先取得本地文档再拼装引用。
    状态变化：risk_checked/approved → completed；低风险和批准路径共用同一生成规则。
    失败处理：Retriever 或 Generator 异常由 Service 记录并发布 error，不再发送 completed。
    企业级替换：ACL 检索、Hybrid Search、Rerank、Context Builder 与受控 LLM。
    """

    documents = retrieve_documents(state["question"])
    return {"status": "completed", "report": generate_answer(state, documents)}
