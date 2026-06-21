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
    # 当前主题。
    topic: str
    # 分类后的任务意图。
    intent: str
    # 研究阶段收集到的笔记。
    research_notes: list[str]
    # 草稿文本。
    draft: str
    # 审核意见。
    review_notes: list[str]
    # 修订轮次。
    revision_round: int
    # 最终输出。
    final_answer: str


# 解析命令行参数，决定主题输入。
def parse_args() -> argparse.Namespace:
    # 创建命令行参数解析器。
    parser = argparse.ArgumentParser(description="LangGraph 风格最小状态图 demo")
    # 主题参数有默认值，这样可以直接运行。
    parser.add_argument(
        "topic",
        nargs="?",
        default="LangGraph 适合什么场景",
        help="要处理的主题",
    )
    # 默认不打印 Mermaid 图，需要时再显式打开。
    parser.add_argument(
        "--show-graph",
        action="store_true",
        help="打印 Mermaid 图",
    )
    # 解析参数并返回。
    return parser.parse_args()


# 根据主题判断任务意图，并初始化修订轮次。
def classify_intent(state: WorkflowState) -> dict:
    # 从状态里取出主题。
    topic = state["topic"]
    # 根据主题中的关键词来判断任务类型。
    if any(key in topic for key in ["区别", "对比", "比较"]):
        intent = "compare"
    elif any(key.lower() in topic.lower() for key in ["rag", "retrieval"]):
        intent = "rag"
    else:
        intent = "explain"
    # 返回局部更新值，LangGraph 会把它合并进状态。
    return {"intent": intent, "revision_round": state.get("revision_round", 0)}


# 根据意图生成研究阶段的要点笔记。
def research(state: WorkflowState) -> dict:
    # 根据意图准备不同的研究笔记。
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
    # 只更新 research_notes。
    return {"research_notes": notes}


# 把研究要点整理成第一版草稿。
def draft(state: WorkflowState) -> dict:
    # 读取前面节点的输入。
    topic = state["topic"]
    intent = state["intent"]
    notes = state["research_notes"]
    # 把研究笔记整理成草稿文本。
    draft_text = (
        f"主题：{topic}\n"
        f"意图：{intent}\n"
        "要点：\n- " + "\n- ".join(notes)
    )
    # 返回草稿。
    return {"draft": draft_text}


# 检查草稿是否足够完整，生成审核意见。
def review(state: WorkflowState) -> dict:
    # 审核阶段只检查草稿够不够完整。
    draft_text = state["draft"]
    # review_notes 用于存放问题列表。
    review_notes = []
    # 太短说明内容还不够展开。
    if len(draft_text) < 120:
        review_notes.append("内容偏短，建议补充实践建议。")
    # 如果没有“步骤”这个词，就提示补步骤。
    if "步骤" not in draft_text:
        review_notes.append("建议加入步骤化表达。")
    # 没有问题就直接通过。
    if not review_notes:
        review_notes.append("通过。")
    # 返回审核意见。
    return {"review_notes": review_notes}


# 在草稿基础上补充内容，形成修订版。
def revise(state: WorkflowState) -> dict:
    # 在原草稿基础上追加补充说明。
    revised = state["draft"] + "\n\n补充：\n- 这是一条从状态到节点再到边的最小工作流。"
    # revision_round + 1 表示修订次数加一。
    return {"draft": revised, "revision_round": state.get("revision_round", 0) + 1}


# 根据审核结果决定继续修订还是直接收尾。
def route_after_review(state: WorkflowState) -> Literal["revise", "finalize"]:
    # 如果还没修订过，而且审核意见不是通过，就走 revise。
    if state.get("revision_round", 0) < 1 and state.get("review_notes") != ["通过。"]:
        return "revise"
    # 否则直接收尾。
    return "finalize"


# 汇总草稿和审核意见，生成最终答案。
def finalize(state: WorkflowState) -> dict:
    # 把草稿和审核意见拼起来，形成最终答案。
    final = (
        f"{state['draft']}\n\n"
        f"审核结果：{'；'.join(state.get('review_notes', []))}\n"
        "结论：这张图已经具备最小的规划、执行和回路控制能力。"
    )
    # 只写回 final_answer。
    return {"final_answer": final}


# 从最终答案里提取更适合终端阅读的摘要。
def summarize_final_answer(final_answer: str) -> str:
    # 只保留“审核结果”和“结论”两行，减少终端噪音。
    summary_lines = []
    for line in final_answer.splitlines():
        if line.startswith("审核结果：") or line.startswith("结论："):
            summary_lines.append(line)
    return "\n".join(summary_lines) if summary_lines else final_answer


# 组装 LangGraph 节点、边和条件分支。
def build_app():
    # 创建一个 StateGraph，泛型参数是 WorkflowState。
    graph = StateGraph(WorkflowState)
    # 添加节点。
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("research", research)
    graph.add_node("draft", draft)
    graph.add_node("review", review)
    graph.add_node("revise", revise)
    graph.add_node("finalize", finalize)

    # 从 START 进入第一个节点。
    graph.add_edge(START, "classify_intent")
    # 按固定顺序连接前半段。
    graph.add_edge("classify_intent", "research")
    graph.add_edge("research", "draft")
    graph.add_edge("draft", "review")
    # 审核节点后面要根据状态决定走哪条边。
    graph.add_conditional_edges(
        "review",
        route_after_review,
        {
            "revise": "revise",
            "finalize": "finalize",
        },
    )
    # revise 后回到 review，形成循环。
    graph.add_edge("revise", "review")
    # finalize 后结束。
    graph.add_edge("finalize", END)
    # 编译后得到可执行 app。
    return graph.compile()


# 程序入口，执行完整工作流并打印结果。
def main() -> None:
    print("MODEL: provider=local model=none mode=graph-demo")
    # 解析命令行主题。
    args = parse_args()
    # 构建并编译工作流。
    app = build_app()
    # 初始状态里放入主题和修订轮次。
    result = app.invoke({"topic": args.topic, "revision_round": 0})

    # 需要时才打印流程图，默认保持终端简洁。
    if args.show_graph:
        print("=== LangGraph Mermaid ===")
        print(app.get_graph().draw_mermaid())

    # 默认只打印摘要，降低终端噪音。
    print("=== 最终结果 ===")
    print(f"主题：{result['topic']}")
    print(f"意图：{result['intent']}")
    print(summarize_final_answer(result["final_answer"]))


if __name__ == "__main__":
    main()
