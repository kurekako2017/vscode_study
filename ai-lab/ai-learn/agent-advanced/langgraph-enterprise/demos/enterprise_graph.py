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
    """主图和子图共用的数据结构；events 使用 reducer 追加而不是覆盖。"""
    thread_id: str
    request: str
    customer: str
    draft: str
    approved: bool
    answer: str
    events: Annotated[list[str], operator.add]


def normalize(state: State) -> dict:
    """子图第一步：清理用户输入两侧的空白。"""
    return {"request": state["request"].strip(), "events": ["subgraph:normalized"]}


def enrich(state: State) -> dict:
    """子图第二步：根据客户和请求生成待审批草稿。"""
    return {"draft": f"为 {state['customer']} 执行：{state['request']}", "events": ["subgraph:drafted"]}


def build_preparation_subgraph():
    """把输入清理和草稿生成封装成可复用子图。"""
    graph = StateGraph(State)
    graph.add_node("normalize", normalize)
    graph.add_node("enrich", enrich)
    graph.add_edge(START, "normalize")
    graph.add_edge("normalize", "enrich")
    graph.add_edge("enrich", END)
    return graph.compile()


def approval(state: State) -> dict:
    """用 interrupt 暂停执行，等待外部人员提交批准或拒绝决定。"""
    decision = interrupt({"question": "是否批准执行？", "draft": state["draft"]})
    approved = str(decision).lower() in {"yes", "y", "true", "批准"}
    return {"approved": approved, "events": [f"human:approved={approved}"]}


def route(state: State) -> str:
    """根据人工审批结果选择执行分支或拒绝分支。"""
    return "execute" if state["approved"] else "reject"


def execute(state: State, runtime: Runtime) -> dict:
    """执行已批准请求，并把客户累计运行次数写入跨线程 Store。"""
    store = runtime.store
    if store is None:
        raise RuntimeError("graph store is required")
    namespace = ("customers", state["customer"])
    previous = store.get(namespace, "profile")
    count = int(previous.value["runs"]) + 1 if previous else 1
    store.put(namespace, "profile", {"runs": count, "last_request": state["request"]})
    return {"answer": f"已执行（该客户累计 {count} 次）：{state['draft']}", "events": ["executor:done"]}


def reject(state: State) -> dict:
    """生成拒绝结果；拒绝路径不会写入客户运行次数。"""
    return {"answer": f"已拒绝：{state['draft']}", "events": ["executor:rejected"]}


def build_graph():
    """组合子图、人工审批和条件分支，并启用内存 checkpoint/store。"""
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
    """流式执行到 interrupt，再用 Command(resume=...) 恢复同一线程。"""
    print("MODEL: provider=local model=none mode=graph-demo")
    parser = argparse.ArgumentParser()
    parser.add_argument("request", nargs="?", default="发送报价单")
    parser.add_argument("--thread", default="demo-thread")
    parser.add_argument("--customer", default="ACME")
    parser.add_argument("--decision", default="yes")
    args = parser.parse_args()
    app = build_graph()
    config = {"configurable": {"thread_id": args.thread}}
    # thread_id 是 checkpoint 的索引；恢复时必须继续使用同一个值。
    initial: State = {"thread_id": args.thread, "request": args.request, "customer": args.customer, "events": []}
    for chunk in app.stream(initial, config, stream_mode="updates"):
        print("stream:", chunk)
    snapshot = app.get_state(config)
    if snapshot.next:
        # snapshot.next 非空表示图停在 interrupt，尚未走到 END。
        print("checkpoint next:", snapshot.next)
        for chunk in app.stream(Command(resume=args.decision), config, stream_mode="updates"):
            print("stream:", chunk)
    print("final:", app.get_state(config).values)


if __name__ == "__main__":
    main()
