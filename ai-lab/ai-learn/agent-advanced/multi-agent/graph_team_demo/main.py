"""Supervisor/Handoff/预算/终止条件组成的真实 Multi-Agent 状态图。"""
from __future__ import annotations

import argparse
import operator
from typing import Annotated, Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class TeamState(TypedDict, total=False):
    """团队共享状态；每个“Agent”节点只负责其中一部分字段。"""
    task: str
    plan: list[str]
    evidence: Annotated[list[str], operator.add]
    draft: str
    review: str
    next_agent: str
    steps: int
    budget: int


def supervisor(state: TeamState) -> dict:
    """根据当前状态决定下一个角色，并用 budget 限制总调度次数。"""
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
    """规划角色：生成固定的三步工作计划。"""
    return {"plan": ["明确目标", "收集证据", "形成建议"], "next_agent": "supervisor"}


def researcher(state: TeamState) -> dict:
    """研究角色：生成一条本地模拟证据。"""
    return {"evidence": [f"证据：{state['task']} 需要状态、职责和终止条件"], "next_agent": "supervisor"}


def writer(state: TeamState) -> dict:
    """写作角色：把任务和证据整理成草稿，并清空旧审校结果。"""
    evidence = "；".join(state.get("evidence", []))
    return {"draft": f"任务：{state['task']}。方案：{evidence}。风险：限制步骤与预算。", "review": "", "next_agent": "supervisor"}


def reviewer(state: TeamState) -> dict:
    """审校角色：草稿包含风险说明才通过，否则要求重写。"""
    decision = "pass" if "风险" in state.get("draft", "") else "revise"
    return {"review": decision, "next_agent": "supervisor"}


def route(state: TeamState) -> Literal["planner", "researcher", "writer", "reviewer", "finish"]:
    """把 supervisor 写入的角色名交给 LangGraph 条件边。"""
    return state["next_agent"]  # type: ignore[return-value]


def build_graph():
    """构建 supervisor 与四个工作角色之间的循环状态图。"""
    graph = StateGraph(TeamState)
    for name, node in {"supervisor": supervisor, "planner": planner, "researcher": researcher, "writer": writer, "reviewer": reviewer}.items():
        graph.add_node(name, node)
    graph.add_edge(START, "supervisor")
    graph.add_conditional_edges("supervisor", route, {"planner": "planner", "researcher": "researcher", "writer": "writer", "reviewer": "reviewer", "finish": END})
    for worker in ["planner", "researcher", "writer", "reviewer"]:
        graph.add_edge(worker, "supervisor")
    return graph.compile()


def main() -> None:
    """创建初始团队状态并执行，直到完成或耗尽步骤预算。"""
    print("MODEL: provider=local model=none mode=graph-demo")
    parser = argparse.ArgumentParser()
    parser.add_argument("task", nargs="?", default="设计企业客服 Agent")
    parser.add_argument("--budget", type=int, default=8)
    args = parser.parse_args()
    initial: TeamState = {
        "task": args.task,
        "budget": args.budget,
        "steps": 0,
        "evidence": [],
    }
    result = build_graph().invoke(initial, {"recursion_limit": 30})
    print(result)


if __name__ == "__main__":
    main()
