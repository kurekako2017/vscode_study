"""Supervisor/Handoff/预算/终止条件组成的真实 Multi-Agent 状态图。"""
from __future__ import annotations

import argparse
import operator
from typing import Annotated, Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class TeamState(TypedDict, total=False):
    task: str
    plan: list[str]
    evidence: Annotated[list[str], operator.add]
    draft: str
    review: str
    next_agent: str
    steps: int
    budget: int


def supervisor(state: TeamState) -> dict:
    steps = state.get("steps", 0) + 1
    if steps >= state["budget"]:
        next_agent = "finish"
    elif not state.get("plan"):
        next_agent = "planner"
    elif not state.get("evidence"):
        next_agent = "researcher"
    elif not state.get("draft") or state.get("review") == "revise":
        next_agent = "writer"
    elif not state.get("review"):
        next_agent = "reviewer"
    else:
        next_agent = "finish"
    return {"next_agent": next_agent, "steps": steps}


def planner(state: TeamState) -> dict:
    return {"plan": ["明确目标", "收集证据", "形成建议"], "next_agent": "supervisor"}


def researcher(state: TeamState) -> dict:
    return {"evidence": [f"证据：{state['task']} 需要状态、职责和终止条件"], "next_agent": "supervisor"}


def writer(state: TeamState) -> dict:
    evidence = "；".join(state.get("evidence", []))
    return {"draft": f"任务：{state['task']}。方案：{evidence}。风险：限制步骤与预算。", "review": "", "next_agent": "supervisor"}


def reviewer(state: TeamState) -> dict:
    decision = "pass" if "风险" in state.get("draft", "") else "revise"
    return {"review": decision, "next_agent": "supervisor"}


def route(state: TeamState) -> Literal["planner", "researcher", "writer", "reviewer", "finish"]:
    return state["next_agent"]  # type: ignore[return-value]


def build_graph():
    graph = StateGraph(TeamState)
    for name, node in {"supervisor": supervisor, "planner": planner, "researcher": researcher, "writer": writer, "reviewer": reviewer}.items():
        graph.add_node(name, node)
    graph.add_edge(START, "supervisor")
    graph.add_conditional_edges("supervisor", route, {"planner": "planner", "researcher": "researcher", "writer": "writer", "reviewer": "reviewer", "finish": END})
    for worker in ["planner", "researcher", "writer", "reviewer"]:
        graph.add_edge(worker, "supervisor")
    return graph.compile()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("task", nargs="?", default="设计企业客服 Agent")
    parser.add_argument("--budget", type=int, default=8)
    args = parser.parse_args()
    result = build_graph().invoke({"task": args.task, "budget": args.budget, "steps": 0, "evidence": []}, {"recursion_limit": 30})
    print(result)


if __name__ == "__main__":
    main()
