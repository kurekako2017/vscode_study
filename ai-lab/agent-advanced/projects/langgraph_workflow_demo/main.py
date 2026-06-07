"""LangGraph 风格的最小状态图 demo。

目标：
1. 认识 State
2. 认识 Node
3. 认识 Edge
4. 认识 conditional edge / loop
"""

from __future__ import annotations

import argparse
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class WorkflowState(TypedDict, total=False):
    topic: str
    intent: str
    research_notes: list[str]
    draft: str
    review_notes: list[str]
    revision_round: int
    final_answer: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LangGraph 风格最小状态图 demo")
    parser.add_argument(
        "topic",
        nargs="?",
        default="LangGraph 适合什么场景",
        help="要处理的主题",
    )
    return parser.parse_args()


def classify_intent(state: WorkflowState) -> dict:
    topic = state["topic"]
    if any(key in topic for key in ["区别", "对比", "比较"]):
        intent = "compare"
    elif any(key.lower() in topic.lower() for key in ["rag", "retrieval"]):
        intent = "rag"
    else:
        intent = "explain"
    return {"intent": intent, "revision_round": state.get("revision_round", 0)}


def research(state: WorkflowState) -> dict:
    intent = state["intent"]
    if intent == "compare":
        notes = [
            "先列出对象的共同点。",
            "再列出核心差异。",
            "最后给出适用场景。",
        ]
    elif intent == "rag":
        notes = [
            "明确文档切分与索引。",
            "加入检索与重排。",
            "最后补来源引用。",
        ]
    else:
        notes = [
            "先解释核心概念。",
            "再补一个最小流程图。",
            "最后给出实践建议。",
        ]
    return {"research_notes": notes}


def draft(state: WorkflowState) -> dict:
    topic = state["topic"]
    intent = state["intent"]
    notes = state["research_notes"]
    draft_text = (
        f"主题：{topic}\n"
        f"意图：{intent}\n"
        "要点：\n- " + "\n- ".join(notes)
    )
    return {"draft": draft_text}


def review(state: WorkflowState) -> dict:
    draft_text = state["draft"]
    review_notes = []
    if len(draft_text) < 120:
        review_notes.append("内容偏短，建议补充实践建议。")
    if "步骤" not in draft_text:
        review_notes.append("建议加入步骤化表达。")
    if not review_notes:
        review_notes.append("通过。")
    return {"review_notes": review_notes}


def revise(state: WorkflowState) -> dict:
    revised = state["draft"] + "\n\n补充：\n- 这是一条从状态到节点再到边的最小工作流。"
    return {"draft": revised, "revision_round": state.get("revision_round", 0) + 1}


def route_after_review(state: WorkflowState) -> Literal["revise", "finalize"]:
    if state.get("revision_round", 0) < 1 and state.get("review_notes") != ["通过。"]:
        return "revise"
    return "finalize"


def finalize(state: WorkflowState) -> dict:
    final = (
        f"{state['draft']}\n\n"
        f"审核结果：{'；'.join(state.get('review_notes', []))}\n"
        "结论：这张图已经具备最小的规划、执行和回路控制能力。"
    )
    return {"final_answer": final}


def build_app():
    graph = StateGraph(WorkflowState)
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("research", research)
    graph.add_node("draft", draft)
    graph.add_node("review", review)
    graph.add_node("revise", revise)
    graph.add_node("finalize", finalize)

    graph.add_edge(START, "classify_intent")
    graph.add_edge("classify_intent", "research")
    graph.add_edge("research", "draft")
    graph.add_edge("draft", "review")
    graph.add_conditional_edges(
        "review",
        route_after_review,
        {
            "revise": "revise",
            "finalize": "finalize",
        },
    )
    graph.add_edge("revise", "review")
    graph.add_edge("finalize", END)
    return graph.compile()


def main() -> None:
    args = parse_args()
    app = build_app()
    result = app.invoke({"topic": args.topic, "revision_round": 0})

    print("=== LangGraph Mermaid ===")
    print(app.get_graph().draw_mermaid())
    print("=== 最终结果 ===")
    print(result["final_answer"])


if __name__ == "__main__":
    main()
