"""LCEL Runnable 组合模式：Parallel、Branch、Passthrough、batch、stream。"""
from __future__ import annotations

import argparse
from operator import itemgetter

from langchain_core.runnables import (
    RunnableBranch,
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)


def classify(data: dict) -> str:
    text = data["question"].lower()
    return "rag" if "rag" in text or "检索" in text else "agent"


def build_chain():
    enrich = RunnablePassthrough.assign(
        intent=RunnableLambda(classify),
        length=RunnableLambda(lambda x: len(x["question"])),
    )
    parallel = RunnableParallel(
        original=itemgetter("question"),
        intent=itemgetter("intent"),
        facts=RunnableLambda(
            lambda x: ["检索、重排、引用"] if x["intent"] == "rag" else ["状态、工具、边界"]
        ),
    )
    route = RunnableBranch(
        (lambda x: x["intent"] == "rag", lambda x: f"RAG 路线：{' → '.join(x['facts'])}"),
        lambda x: f"Agent 路线：{' → '.join(x['facts'])}",
    )
    return enrich | parallel | route


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("questions", nargs="*", default=["高级 RAG 怎么设计", "Agent 如何控制工具"])
    parser.add_argument("--stream", action="store_true")
    args = parser.parse_args()
    chain = build_chain()
    inputs = [{"question": q} for q in args.questions]
    if args.stream:
        for chunk in chain.stream(inputs[0]):
            print(chunk, end="", flush=True)
        print()
    else:
        for answer in chain.batch(inputs):
            print(answer)


if __name__ == "__main__":
    main()
