"""本地确定性回答生成器。

文件职责：根据 Workflow State 和检索文档拼装带引用的日文正式报告。
谁调用它：Workflow ``answer_generated`` Node；它读取 Document 和 WorkflowState。
输入：问题状态与文档片段；输出：Markdown 字符串报告。
为什么需要这一层：把回答格式与 Workflow 路由拆开，当前不依赖任何真实 LLM。
初学者重点：批准路径与低风险路径只影响“确定方法”，引用来自 Retriever 结果。
日本现场面试：可称为 Static Answer Provider，用确定性输出验证审批闭环。
企业级替换：实现 AnswerGenerator Interface 后接受控 LLM，必须保留 Citation、ACL 和拒答规则。
"""

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
