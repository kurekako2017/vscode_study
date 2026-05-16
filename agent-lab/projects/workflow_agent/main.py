"""workflow_agent: 分阶段工作流生成示例（分析→计划→总结），带注释。

此示例展示如何把复杂任务分解为多个模型阶段：
1. `analyze` 阶段提取目标与限制
2. `plan` 阶段生成结构化执行步骤（并用 Pydantic 验证）
3. `finalize` 阶段基于前两步生成最终建议

使用分阶段方法能让模型在每一步聚焦单一子任务，提高可控性与可验证性。
"""

import argparse
import json
import os
import sys
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel, Field


DEFAULT_MODEL = "gpt-5"
ANALYZE_INSTRUCTIONS = (
    "You are a workflow analyzer. Read the user's request and summarize the goal, "
    "constraints, and desired deliverables in concise bullet points."
)
PLAN_INSTRUCTIONS = (
    "You are a workflow planner. Create a structured plan based on the analysis."
)
FINALIZE_INSTRUCTIONS = (
    "You are a workflow assistant. Write a short final recommendation based only "
    "on the analysis and plan."
)


class WorkflowPlan(BaseModel):
    """Pydantic 定义的计划 schema，用于在计划阶段验证模型输出结构。"""
    # This schema keeps the planning step stable enough for the next workflow stage.
    goal: str = Field(description="The main goal of the task.")
    priority: Literal["low", "medium", "high"] = Field(
        description="Estimated priority of the task."
    )
    steps: list[str] = Field(description="Recommended execution steps.")
    deliverables: list[str] = Field(description="Expected outputs.")
    risks: list[str] = Field(description="Main risks or cautions.")


def parse_args() -> argparse.Namespace:
    """解析命令行参数：用户任务与可选模型名。"""
    parser = argparse.ArgumentParser(
        description="Minimal workflow agent demo with staged OpenAI Responses API calls."
    )
    parser.add_argument("prompt", help="User task for the workflow agent.")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model name to use. Default: {DEFAULT_MODEL}",
    )
    return parser.parse_args()


def build_client() -> OpenAI:
    """创建 OpenAI 客户端，需通过环境变量提供 API Key。"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)
    return OpenAI(api_key=api_key)


def analyze_task(client: OpenAI, model: str, prompt: str) -> str:
    """分析阶段：把用户请求转换为简洁的分析文本，供下一步计划使用。"""
    response = client.responses.create(
        model=model,
        instructions=ANALYZE_INSTRUCTIONS,
        input=prompt,
    )
    return response.output_text


def plan_task(client: OpenAI, model: str, analysis: str) -> WorkflowPlan:
    """计划阶段：基于分析文本生成结构化的 `WorkflowPlan`（Pydantic 验证）。"""
    response = client.responses.parse(
        model=model,
        instructions=PLAN_INSTRUCTIONS,
        input=analysis,
        text_format=WorkflowPlan,
    )
    return response.output_parsed


def finalize_task(client: OpenAI, model: str, analysis: str, plan: WorkflowPlan) -> str:
    """总结阶段：基于分析与计划生成最终简短建议。"""
    # The final step consumes prior workflow state instead of re-reading the original task alone.
    final_input = (
        "Analysis:\n"
        f"{analysis}\n\n"
        "Plan:\n"
        f"{json.dumps(plan.model_dump(), ensure_ascii=False, indent=2)}"
    )
    response = client.responses.create(
        model=model,
        instructions=FINALIZE_INSTRUCTIONS,
        input=final_input,
    )
    return response.output_text


def main() -> None:
    args = parse_args()
    client = build_client()

    try:
        # 分阶段执行：先分析，再计划，最后总结
        analysis = analyze_task(client, args.model, args.prompt)
        plan = plan_task(client, args.model, analysis)
        final_summary = finalize_task(client, args.model, analysis, plan)
    except Exception as exc:
        print(f"ERROR: request failed: {exc}", file=sys.stderr)
        sys.exit(1)

    # 打印每个阶段的结果，便于学习和调试
    print("=== Step 1: Analysis ===")
    print(analysis)
    print("\n=== Step 2: Plan ===")
    print(json.dumps(plan.model_dump(), ensure_ascii=False, indent=2))
    print("\n=== Step 3: Final Summary ===")
    print(final_summary)


if __name__ == "__main__":
    main()
