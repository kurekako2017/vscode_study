from app.rag.documents import Document
from app.workflow.state import WorkflowState


def generate_answer(state: WorkflowState, documents: tuple[Document, ...]) -> str:
    approval_note = (
        "承認者による確認済み"
        if state.get("approval_decision") == "approved"
        else "低リスク判定により自動確定"
    )
    references = "\n".join(f"- {item['title']}（固定ローカル資料）" for item in documents)
    return "\n".join(
        [
            "# 社内文書検索・承認ワークフロー 回答レポート",
            "",
            "## 質問",
            state["question"],
            "",
            "## 正式回答",
            "関連する社内手順を確認しました。担当部門の最新規程と手順書に従って対応してください。",
            "",
            "## リスク・承認状態",
            f"- リスクレベル: {state.get('risk_level', 'HIGH')}",
            f"- 確定方法: {approval_note}",
            "",
            "## 参照資料",
            references,
            "",
            "> 現在は固定データによる回答です。実運用前に文書所有者へ確認してください。",
        ]
    )
