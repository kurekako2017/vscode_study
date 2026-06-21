"""Checkpoint、Memory、HITL、Subgraph、Streaming 的真实 LangGraph 示例。"""
from __future__ import annotations

import argparse
import operator
from typing import Annotated, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.runtime import Runtime
from langgraph.store.memory import InMemoryStore
from langgraph.types import Command, interrupt


class State(TypedDict, total=False):
    thread_id: str
    request: str
    customer: str
    draft: str
    approved: bool
    answer: str
    events: Annotated[list[str], operator.add]


def normalize(state: State) -> dict:
    return {"request": state["request"].strip(), "events": ["subgraph:normalized"]}


def enrich(state: State) -> dict:
    return {"draft": f"为 {state['customer']} 执行：{state['request']}", "events": ["subgraph:drafted"]}


def build_preparation_subgraph():
    graph = StateGraph(State)
    graph.add_node("normalize", normalize)
    graph.add_node("enrich", enrich)
    graph.add_edge(START, "normalize")
    graph.add_edge("normalize", "enrich")
    graph.add_edge("enrich", END)
    return graph.compile()


def approval(state: State) -> dict:
    decision = interrupt({"question": "是否批准执行？", "draft": state["draft"]})
    approved = str(decision).lower() in {"yes", "y", "true", "批准"}
    return {"approved": approved, "events": [f"human:approved={approved}"]}


def route(state: State) -> str:
    return "execute" if state["approved"] else "reject"


def execute(state: State, runtime: Runtime) -> dict:
    store = runtime.store
    if store is None:
        raise RuntimeError("graph store is required")
    namespace = ("customers", state["customer"])
    previous = store.get(namespace, "profile")
    count = int(previous.value["runs"]) + 1 if previous else 1
    store.put(namespace, "profile", {"runs": count, "last_request": state["request"]})
    return {"answer": f"已执行（该客户累计 {count} 次）：{state['draft']}", "events": ["executor:done"]}


def reject(state: State) -> dict:
    return {"answer": f"已拒绝：{state['draft']}", "events": ["executor:rejected"]}


def build_graph():
    graph = StateGraph(State)
    graph.add_node("prepare", build_preparation_subgraph())
    graph.add_node("approval", approval)
    graph.add_node("execute", execute)
    graph.add_node("reject", reject)
    graph.add_edge(START, "prepare")
    graph.add_edge("prepare", "approval")
    graph.add_conditional_edges("approval", route, {"execute": "execute", "reject": "reject"})
    graph.add_edge("execute", END)
    graph.add_edge("reject", END)
    return graph.compile(checkpointer=InMemorySaver(), store=InMemoryStore())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("request", nargs="?", default="发送报价单")
    parser.add_argument("--thread", default="demo-thread")
    parser.add_argument("--customer", default="ACME")
    parser.add_argument("--decision", default="yes")
    args = parser.parse_args()
    app = build_graph()
    config = {"configurable": {"thread_id": args.thread}}
    initial: State = {"thread_id": args.thread, "request": args.request, "customer": args.customer, "events": []}
    for chunk in app.stream(initial, config, stream_mode="updates"):
        print("stream:", chunk)
    snapshot = app.get_state(config)
    if snapshot.next:
        print("checkpoint next:", snapshot.next)
        for chunk in app.stream(Command(resume=args.decision), config, stream_mode="updates"):
            print("stream:", chunk)
    print("final:", app.get_state(config).values)


if __name__ == "__main__":
    main()
