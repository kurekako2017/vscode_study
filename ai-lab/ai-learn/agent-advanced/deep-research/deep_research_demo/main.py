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
    """图中所有节点共享的状态；节点只返回自己新增或修改的字段。"""
    question: str
    queries: list[str]
    evidence: list[dict]
    report: str
    review: str
    rounds: int
    max_rounds: int


def plan(state: ResearchState) -> dict:
    """把原始问题扩展成多个检索方向。真实系统通常会让 LLM 生成这些查询。"""
    return {"queries": [state["question"], f"{state['question']} 安全", f"{state['question']} 持久化"]}


def search(state: ResearchState) -> dict:
    """用词语交集搜索内置语料，并记录已经执行的研究轮数。"""
    words = set(state["question"].lower().replace("/", " ").split())
    hits = [doc for doc in CORPUS if words & set((doc["title"] + " " + doc["text"]).lower().split())]
    return {"evidence": hits or CORPUS[:2], "rounds": state.get("rounds", 0) + 1}


def deduplicate(state: ResearchState) -> dict:
    """以资料 id 去重，防止同一证据在报告里重复出现。"""
    unique = {item["id"]: item for item in state["evidence"]}
    return {"evidence": list(unique.values())}


def write(state: ResearchState) -> dict:
    """把证据拼成带引用编号的 Markdown 报告；这里只使用字符串模板。"""
    claims = "\n".join(f"- {item['text']} [{item['id']}]" for item in state["evidence"])
    sources = "\n".join(f"[{item['id']}] {item['title']}" for item in state["evidence"])
    return {"report": f"# {state['question']}\n\n## 结论\n{claims}\n\n## 来源\n{sources}"}


def review(state: ResearchState) -> dict:
    """检查每条证据是否被引用，以及证据数量是否达到最低要求。"""
    has_citations = all(f"[{item['id']}]" in state["report"] for item in state["evidence"])
    enough = len(state["evidence"]) >= 2
    return {"review": "pass" if has_citations and enough else "revise"}


def route(state: ResearchState) -> Literal["finish", "research"]:
    """审校通过或达到轮数上限时结束，否则回到检索节点。"""
    return "finish" if state["review"] == "pass" or state["rounds"] >= state["max_rounds"] else "research"


def build_graph():
    """注册节点和边，编译为可执行的 LangGraph。"""
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
    """读取命令行问题，执行完整研究图并输出报告及审校状态。"""
    print("MODEL: provider=local model=none mode=research-simulation")
    parser = argparse.ArgumentParser()
    parser.add_argument("question", nargs="?", default="LangGraph MCP Agent 如何保证安全")
    parser.add_argument("--max-rounds", type=int, default=2)
    args = parser.parse_args()
    # 初始状态必须包含循环计数；recursion_limit 是额外的死循环保护。
    initial: ResearchState = {
        "question": args.question,
        "evidence": [],
        "rounds": 0,
        "max_rounds": args.max_rounds,
    }
    result = build_graph().invoke(initial, {"recursion_limit": 30})
    print(result["report"])
    print(f"\nreview={result['review']} rounds={result['rounds']}")


if __name__ == "__main__":
    main()
