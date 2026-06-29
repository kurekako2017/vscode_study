from app.agents.answer_generator import generate_answer
from app.approval.policy import classify_risk
from app.rag.retriever import retrieve_documents
from app.workflow.state import WorkflowState


def risk_checked(state: WorkflowState) -> dict[str, str]:
    return {"risk_level": classify_risk(state["question"]), "status": "risk_checked"}


def answer_generated(state: WorkflowState) -> dict[str, str]:
    documents = retrieve_documents(state["question"])
    return {"status": "completed", "report": generate_answer(state, documents)}
