"""workflow_agent: 分阶段工作流生成示例（分析→计划→总结），带注释。

此示例展示如何把复杂任务分解为多个模型阶段：
1. `analyze` 阶段提取目标与限制
2. `plan` 阶段生成结构化执行步骤（并用 Pydantic 验证）
3. `finalize` 阶段基于前两步生成最终建议

使用分阶段方法能让模型在每一步聚焦单一子任务，提高可控性与可验证性。

学习地图：
- 运行命令：
    - python3 main.py "我要做一个面向日本现场的需求整理 Agent"
    - python3 main.py "帮我规划 4 周的 LLM 学习与作品集计划"
- 输入输出：
    - 输入：用户任务描述
    - 输出：三阶段结果（analysis、结构化 plan、final summary）
- 改造练习点：
    - 在 plan 阶段增加 effort_estimate 字段
    - 把三阶段耗时统计打印出来
    - 允许跳过 finalize，只输出前两阶段
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel, Field

for _parent in Path(__file__).resolve().parents:
    if (_parent / "llm_runtime.py").exists():
        sys.path.insert(0, str(_parent))
        break
from llm_runtime import build_fallback_client, has_real_provider

DEFAULT_MODEL = "gpt-5"
# OpenRouter 兼容服务默认基址。
DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
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
    # 层次: 输入层 — 解析用户任务与模型配置
    """解析命令行参数：用户任务与可选模型名（支持 mock/real）。"""
    parser = argparse.ArgumentParser(
        description="包含分阶段 OpenAI Responses API 调用的最小工作流代理演示."
    )
    #   解析用户任务参数     （解析用户任务参数）
    parser.add_argument("prompt", help="工作流代理的用户任务.")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"要使用的模型名称。默认值: {DEFAULT_MODEL}",
    )
    parser.add_argument(
        "--mock", action="store_true", help="Run in offline mock mode (no API calls)."
    )
    parser.add_argument(
        "--real",
        action="store_true",
        help="Force real API mode (requires OPENROUTER_API_KEY or OPENAI_API_KEY).",
    )
    return parser.parse_args()


# 从命令行参数中获取模型名称和
def _has_real_credentials() -> bool:
    return has_real_provider()


def build_client() -> OpenAI:
    # 层次: 基础设施层 — 构建 OpenAI 客户端并处理缺失 Key 的退出策略
    """创建 OpenAI 兼容客户端，需通过环境变量提供 API Key。

    说明：该函数在需要真实调用时才会被执行；在 mock 模式下上层会绕过此函数以避免外部依赖。
    """
    return build_fallback_client()


def resolve_mode(force_mock: bool, force_real: bool) -> str:
    # 如果 force_mock 为 True，则返回 "mock"
    if force_mock:
        # 返回 "mock"     （返回 "mock"）
        return "mock"
    if force_real:
        # 如果 OPENAI_API_KEY 未设置，则打印错误信息并退出     （如果 OPENAI_API_KEY 未设置，则打印错误信息并退出）
        if not _has_real_credentials():
            # 退出程序     （退出程序）
            print(
                "ERROR: --real requested but OPENROUTER_API_KEY or OPENAI_API_KEY is not set.",
                file=sys.stderr,
            )
            sys.exit(1)
        # 返回 "real"     （返回 "real"）
        return "real"
    # 如果 OPENAI / OpenRouter key 已设置，则返回 "real"
    return "real" if _has_real_credentials() else "mock"


def build_mock_analysis(prompt: str) -> str:
    """生成离线用的分析文本示例，便于学习流程。"""
    # 返回一个符合分析文本示例的文本     （返回一个符合分析文本示例的文本）
    return (
        f"[MOCK MODE] Analysis for: {prompt}\n- goals: mock goal\n- constraints: none"
    )


def build_mock_plan(prompt: str) -> WorkflowPlan:
    """生成离线用的结构化计划示例（Pydantic 模型）。"""
    # 返回一个符合 WorkflowPlan 结构的示例数据     （返回一个符合 WorkflowPlan 结构的示例数据）
    return WorkflowPlan(
        goal=f"Mock plan for: {prompt}",
        priority="medium",
        steps=["step1", "step2"],
        deliverables=["demo"],
        risks=["mock only"],
    )


def build_mock_final(prompt: str) -> str:
    """生成离线用的最终建议示例。"""
    # 返回一个符合最终建议示例的文本     （返回一个符合最终建议示例的文本）
    return f"[MOCK MODE] Final recommendation for: {prompt}"


def analyze_task(client: OpenAI | None, model: str, prompt: str, mode: str) -> str:
    """分析阶段：把用户请求转换为简洁的分析文本，供下一步计划使用。

    - mock 模式下返回示例分析文本，便于离线学习。
    - 真实模式下使用 Responses API 请求模型，返回的文本将作为 plan 阶段的输入。
    """
    if mode == "mock":
        return build_mock_analysis(prompt)
    # 使用 Responses API 请求模型，返回的文本将作为 plan 阶段的输入     （使用 Responses API 请求模型，返回的文本将作为 plan 阶段的输入）
    # 返回模型的输出文本     （返回模型的输出文本）
    response = client.responses.create(
        model=model,
        instructions=ANALYZE_INSTRUCTIONS,
        input=prompt,
    )
    # 返回模型的输出文本     （返回模型的输出文本）
    return response.output_text


def plan_task(
    client: OpenAI | None, model: str, analysis: str, mode: str
) -> WorkflowPlan:
    """计划阶段：基于分析文本生成结构化的 `WorkflowPlan`（Pydantic 验证）。

    - 在真实模式下使用 SDK 的 `parse` 功能把模型输出直接映射为 `WorkflowPlan`，以便下一阶段可靠消费。
    - 在 mock 模式下返回示例 `WorkflowPlan`。
    """
    if mode == "mock":
        return build_mock_plan(analysis)
    # 使用 Responses API 请求模型，返回的文本将作为 plan 阶段的输入     （使用 Responses API 请求模型，返回的文本将作为 plan 阶段的输入）
    # 返回模型的输出文本     （返回模型的输出文本）
    response = client.responses.parse(
        model=model,
        instructions=PLAN_INSTRUCTIONS,
        input=analysis,
        text_format=WorkflowPlan,
    )
    # 返回模型的输出文本     （返回模型的输出文本）
    return response.output_parsed


def finalize_task(
    client: OpenAI | None, model: str, analysis: str, plan: WorkflowPlan, mode: str
) -> str:
    """总结阶段：基于分析与计划生成最终简短建议。

    - 该阶段会把前两阶段的输出拼接为模型输入，提醒模型只基于已验证的信息生成最终建议，减少幻觉风险。
    - mock 模式下直接返回示例文本。
    """
    if mode == "mock":
        return build_mock_final(analysis)
    # The final step consumes prior workflow state instead of re-reading the original task alone.
    final_input = (
        "Analysis:\n"
        f"{analysis}\n\n"
        "Plan:\n"
        f"{json.dumps(plan.model_dump(), ensure_ascii=False, indent=2)}"
    )
    # 使用 Responses API 请求模型，返回的文本将作为 plan 阶段的输入     （使用 Responses API 请求模型，返回的文本将作为 plan 阶段的输入）
    # 返回模型的输出文本     （返回模型的输出文本）
    response = client.responses.create(
        model=model,
        instructions=FINALIZE_INSTRUCTIONS,
        input=final_input,
    )
    # 返回模型的输出文本     （返回模型的输出文本）
    return response.output_text


def main() -> None:
    # 层次: 程序入口 — 按阶段顺序执行工作流并展示每阶段输出
    """主流程：执行 analyze -> plan -> finalize 三阶段，并逐段输出结果。"""
    args = parse_args()
    mode = resolve_mode(args.mock, args.real)
    # 先把运行方式说清楚；真实模式会在每次请求成功后打印实际 provider/model。
    if mode == "mock":
        print("MODEL: provider=local model=mock mode=mock", file=sys.stderr)
    client = None
    # 如果 mode 为 "real"，则构建客户端     （如果 mode 为 "real"，则构建客户端）
    if mode == "real":
        # 构建客户端     （构建客户端）
        client = build_client()

    try:
        # 分阶段执行：先分析，再计划，最后总结
        analysis = analyze_task(client, args.model, args.prompt, mode)
        # 计划阶段：基于分析文本生成结构化的 `WorkflowPlan`（Pydantic 验证）     （计划阶段：基于分析文本生成结构化的 `WorkflowPlan`（Pydantic 验证））
        plan = plan_task(client, args.model, analysis, mode)
        # 总结阶段：基于分析与计划生成最终简短建议     （总结阶段：基于分析与计划生成最终简短建议）
        final_summary = finalize_task(client, args.model, analysis, plan, mode)
    except Exception as exc:
        # 打印错误信息     （打印错误信息）
        print(f"ERROR: request failed: {exc}", file=sys.stderr)
        sys.exit(1)

    # 打印每个阶段的结果，便于学习和调试
    print("=== Step 1: Analysis ===")
    # 打印分析结果     （打印分析结果）
    print(analysis)
    # 打印计划结果     （打印计划结果）
    print("\n=== Step 2: Plan ===")
    print(json.dumps(plan.model_dump(), ensure_ascii=False, indent=2))
    # 打印总结结果     （打印总结结果）
    print("\n=== Step 3: Final Summary ===")
    # 打印总结结果     （打印总结结果）
    print(final_summary)


if __name__ == "__main__":
    main()
