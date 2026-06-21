"""structured_output_demo: 演示如何让模型返回结构化数据并用 Pydantic 验证。

该示例展示：
- 使用 Pydantic 定义输出 schema（`AgentPlan`）作为 contract
- 用 Responses API 的 `parse` 将模型输出解析并验证为 Pydantic 模型

对下游系统而言，稳定的 schema 能显著降低解析错误和生产风险。

学习地图：
- 运行命令：
    - python3 main.py "做一个客服 Agent 的开发计划"
    - python3 main.py "给我一个 RAG 学习路线" --model gpt-4o
- 输入输出：
    - 输入：自然语言需求 prompt
    - 输出：通过 Pydantic 校验后的 AgentPlan JSON
- 改造练习点：
    - 在 AgentPlan 中新增 timeline 字段并更新提示词
    - 对 user_type 增加默认值与兜底策略
    - 将结果保存到本地 JSON 文件
"""

import argparse
import json
import os
import sys
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel, Field

#   默认模型名，可用 `--model` 覆盖。
DEFAULT_MODEL = "gpt-4o"
#   OpenRouter 兼容服务默认基址。
DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
#  系统指令：引导模型生成符合 `AgentPlan` 结构的输出，强调清晰简洁。
SYSTEM_INSTRUCTIONS = (
    "您是LLM智能体学习实验室的助理. "
    "分析用户的想法并返回一份结构化的开发计划."
)

#   AgentPlan 模型定义：使用 Pydantic 定义期望的输出结构，包括字段类型和描述。
class AgentPlan(BaseModel):
    """Pydantic 模型：定义期望的结构化输出字段与类型。

    当将模型输出解析到该类型时，若字段缺失或类型不匹配，SDK 会抛出错误，便于及早发现问题。
    """
    goal: str = Field(description="所请求代理的主要目标.")
    user_type: Literal["beginner", "intermediate", "advanced"] = Field(
        description="此项目的预计用户级别."
    )
    # core_capabilities 字段展示了如何使用列表类型来表达多个条目，增加输出的丰富度和实用性。
    core_capabilities: list[str] = Field(
        description="代理应具备的关键能力."
    )
    # tools 和 deliverables 字段展示了如何使用列表类型来表达多个条目，增加输出的丰富度和实用性。
    tools: list[str] = Field(description="Recommended tools or functions.")
    deliverables: list[str] = Field(
        description="要构建的具体输出成果或演示。"
    )
    # risks 字段展示了如何使用列表类型来表达多个条目，增加输出的丰富度和实用性。
    risks: list[str] = Field(description="Main development risks or cautions.")


def parse_args() -> argparse.Namespace:
    # 层次: 输入层 — 解析用户的自然语言请求与模型选项
    """解析命令行参数：接收自然语言请求并可选择模型。"""
    parser = argparse.ArgumentParser(
        description="使用 OpenAI Responses API 的最小结构化输出演示。"
    )
    parser.add_argument("prompt", help="Natural-language project request.")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model name to use. Default: {DEFAULT_MODEL}",
    )
    parser.add_argument("--mock", action="store_true", help="Run in offline mock mode (no API calls).")
    parser.add_argument("--real", action="store_true", help="Force real API mode (requires OPENROUTER_API_KEY or OPENAI_API_KEY).")
    return parser.parse_args()


def _has_real_credentials() -> bool:
    return bool(os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY"))


def build_client() -> OpenAI:
    # 层次: 基础设施层 — 构建 OpenAI 客户端并处理缺失情况
    """创建 OpenAI 兼容客户端，优先支持 OpenRouter。

    说明：在 mock 模式下不会调用此函数；在真实模式下，如果没有 API Key，程序会提示错误并退出。
    """
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY or OPENAI_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)
    kwargs: dict[str, str] = {"api_key": api_key}
    if os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_BASE_URL"):
        kwargs["base_url"] = os.getenv("OPENROUTER_BASE_URL", DEFAULT_OPENROUTER_BASE_URL)
    elif os.getenv("OPENAI_BASE_URL"):
        kwargs["base_url"] = os.getenv("OPENAI_BASE_URL")
    return OpenAI(**kwargs)


def resolve_mode(force_mock: bool, force_real: bool) -> str:
    """决定运行模式：mock 或 real。

    - force_mock 为真时强制 mock
    - force_real 为真时强制 real（无 Key 则报错）
    - 否则根据是否配置 OpenRouter / OpenAI key 自动选择
    """
    # 如果 force_mock 为 True，则返回 "mock"
    if force_mock:
        return "mock"
    # 如果 force_real 为 True，则返回 "real"
    if force_real:
        # 如果 OPENAI_API_KEY 未设置，则打印错误信息并退出     （如果 OPENAI_API_KEY 未设置，则打印错误信息并退出）
        if not _has_real_credentials():
            print("ERROR: --real requested but OPENROUTER_API_KEY or OPENAI_API_KEY is not set.", file=sys.stderr)
            # 退出程序     （退出程序）
            sys.exit(1)
        # 返回 "real"     （返回 "real"）
        return "real"
    # 如果没有可用 key，则返回 "mock"
    return "real" if _has_real_credentials() else "mock"


def build_mock_plan(prompt: str) -> AgentPlan:
    """构造本地示例计划，用于离线演练结构化输出。"""
    # 层次: 调用层 — 在 mock 模式下返回一个符合 AgentPlan 结构的示例数据，便于离线测试和学习。
    # 返回一个符合 AgentPlan 结构的示例数据     （返回一个符合 AgentPlan 结构的示例数据）
    return AgentPlan(
        goal=f"Mock goal for: {prompt}",
        user_type="beginner",
        core_capabilities=["search", "summarize"],
        tools=["local_docs"],
        deliverables=["demo"],
        risks=["mock-only"],
    )


def generate_plan(client: OpenAI | None, model: str, prompt: str, mode: str) -> AgentPlan:
    """根据模式生成结构化计划：mock 返回示例，real 调用模型。"""
    # 层次: 调用层 — 请求模型并使用 SDK 的 parse 功能将输出映射为 `AgentPlan`（支持 mock）
    # 如果是 mock 模式，直接返回示例结构；用于离线学习与测试。
    if mode == "mock":
        return build_mock_plan(prompt)

    # 在真实模式下，使用 SDK 的 `parse` 功能直接把模型输出解析为 Pydantic 类型（`AgentPlan`）。
    # 这能让我们在模型输出与后续系统之间建立一个明确的契约（contract）。
    response = client.responses.parse(
        model=model,
        instructions=SYSTEM_INSTRUCTIONS,
        input=prompt,
        text_format=AgentPlan,
    )
    return response.output_parsed


def main() -> None:
    # 层次: 程序入口 — 读取参数、调用构建流程并展示结果
    """主流程：读取参数 -> 请求结构化输出 -> 打印可读 JSON。"""
    args = parse_args()
    # 模式决策。先根据参数和环境决定是否使用 mock，再构建客户端，减少分支散落。
    mode = resolve_mode(args.mock, args.real)
    # 以下是与客户端交互的设置，后续调用 generate_plan 时会根据 mode 决定是否发起真实请求。
    client = None
    # 只有在 real 模式下才构建客户端，mock 模式下直接使用本地生成的示例数据，避免不必要的环境依赖。
    if mode == "real":
        client = build_client()

    try:
        # 根据模式生成计划  — mock 模式下返回示例数据，real 模式下调用模型并解析输出为 AgentPlan。
        plan = generate_plan(client, args.model, args.prompt, mode)
    except Exception as exc:
        print(f"ERROR: request failed: {exc}", file=sys.stderr)
        sys.exit(1)

    # 同时打印 pretty 和 compact 两种 JSON，便于对比“人读友好”与“机器传输”格式。
    pretty_json = json.dumps(plan.model_dump(), ensure_ascii=False, indent=2)
    compact_json = plan.model_dump_json(ensure_ascii=False)
    # 打印 pretty JSON     （打印 pretty JSON）
    print("=== Parsed JSON ===")
    print(pretty_json)
    # 打印 raw JSON     （打印 raw JSON）
    print("\n=== Raw JSON ===")
    print(compact_json)
    

if __name__ == "__main__":
    main()
