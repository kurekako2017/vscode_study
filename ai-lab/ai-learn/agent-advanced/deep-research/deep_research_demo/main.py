"""计划、检索、去重、引用、写作、审校闭环的离线 Deep Research 图。"""
from __future__ import annotations

import argparse
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


CORPUS = [
    {"id": "S1", "title": "LangGraph Persistence", "text": "checkpoint 按 thread 保存图状态并支持恢复。"},
    {"id": "S2", "title": "Human in the loop", "text": "interrupt 会暂停图，Command resume 用于恢复。"},
    {"id": "S3", "title": "MCP Architecture", "text": "MCP client 发现并调用 server 暴露的工具。"},
    {"id": "S4", "title": "Agent Safety", "text": "高风险副作用应设置审批、预算和审计。"},
]


class ResearchState(TypedDict, total=False):
    question: str
    queries: list[str]
    evidence: list[dict]
    report: str
    review: str
    rounds: int
    max_rounds: int


def plan(state: ResearchState) -> dict:
    return {"queries": [state["question"], f"{state['question']} 安全", f"{state['question']} 持久化"]}


def search(state: ResearchState) -> dict:
    words = set(state["question"].lower().replace("/", " ").split())
    hits = [doc for doc in CORPUS if words & set((doc["title"] + " " + doc["text"]).lower().split())]
    return {"evidence": hits or CORPUS[:2], "rounds": state.get("rounds", 0) + 1}


def deduplicate(state: ResearchState) -> dict:
    unique = {item["id"]: item for item in state["evidence"]}
    return {"evidence": list(unique.values())}


def write(state: ResearchState) -> dict:
    claims = "\n".join(f"- {item['text']} [{item['id']}]" for item in state["evidence"])
    sources = "\n".join(f"[{item['id']}] {item['title']}" for item in state["evidence"])
    return {"report": f"# {state['question']}\n\n## 结论\n{claims}\n\n## 来源\n{sources}"}


def review(state: ResearchState) -> dict:
    has_citations = all(f"[{item['id']}]" in state["report"] for item in state["evidence"])
    enough = len(state["evidence"]) >= 2
    return {"review": "pass" if has_citations and enough else "revise"}


def route(state: ResearchState) -> Literal["finish", "research"]:
    return "finish" if state["review"] == "pass" or state["rounds"] >= state["max_rounds"] else "research"


def build_graph():
    graph = StateGraph(ResearchState)
    for name, node in {"plan": plan, "search": search, "deduplicate": deduplicate, "write": write, "review": review}.items():
        graph.add_node(name, node)
    graph.add_edge(START, "plan")
    graph.add_edge("plan", "search")
    graph.add_edge("search", "deduplicate")
    graph.add_edge("deduplicate", "write")
    graph.add_edge("write", "review")
    graph.add_conditional_edges("review", route, {"finish": END, "research": "search"})
    return graph.compile()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("question", nargs="?", default="LangGraph MCP Agent 如何保证安全")
    parser.add_argument("--max-rounds", type=int, default=2)
    args = parser.parse_args()
    result = build_graph().invoke({"question": args.question, "evidence": [], "rounds": 0, "max_rounds": args.max_rounds}, {"recursion_limit": 30})
    print(result["report"])
    print(f"\nreview={result['review']} rounds={result['rounds']}")


if __name__ == "__main__":
    main()
