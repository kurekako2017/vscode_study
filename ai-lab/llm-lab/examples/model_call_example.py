"""model_call_example.py

示例：最小的模型调用封装，支持 mock / real 两种模式。

运行：
- 无 API Key 也能跑：`python3 model_call_example.py --mock "请给出三步学习计划"`
- 自动模式：`python3 model_call_example.py "请给出三步学习计划"`
- 真实模式：`python3 model_call_example.py --real "请给出三步学习计划"`
"""

import argparse
import os
import sys
from typing import Optional

# 尝试导入 OpenAI SDK。
# 如果当前环境没安装 openai，也不让程序立刻崩掉；
# 后面会根据 mock/real 模式决定是否真的需要 SDK。
try:
    from openai import OpenAI
except Exception:  # pragma: no cover - graceful fallback if package missing
    OpenAI = None


# 默认模型名。真实调用时可通过 --model 覆盖。
DEFAULT_MODEL = "gpt-5"
# 系统指令：告诉模型回答风格。
# 学习阶段可以尝试修改这里，观察输出变化。
SYSTEM_INSTRUCTIONS = (
    "You are a concise assistant for an LLM learning lab. Answer briefly and clearly."
)


def resolve_mode(force_mock: bool, force_real: bool) -> str:
    """决定运行模式：mock 或 real。

    默认自动模式：
    - 有 OPENAI_API_KEY 且安装 openai SDK：real
    - 否则：mock
    """
    # 用户显式传 --mock 时，不检查 API Key，也不调用真实网络。
    if force_mock:
        return "mock"

    # 用户显式传 --real 时，必须提前检查真实调用需要的条件。
    if force_real:
        if not os.getenv("OPENAI_API_KEY"):
            print("ERROR: --real requested but OPENAI_API_KEY is not set.", file=sys.stderr)
            sys.exit(1)
        if OpenAI is None:
            print("ERROR: openai package is not installed. Run: pip install openai", file=sys.stderr)
            sys.exit(1)
        return "real"

    # 自动模式：没有 API Key 就自动降级为 mock，保证初学者也能运行。
    if not os.getenv("OPENAI_API_KEY"):
        print("INFO: OPENAI_API_KEY not set, auto-switching to MOCK mode.", file=sys.stderr)
        return "mock"

    # 有 API Key 但没安装 SDK，也自动降级为 mock。
    if OpenAI is None:
        print("INFO: openai package not installed, auto-switching to MOCK mode.", file=sys.stderr)
        return "mock"

    return "real"


def build_client() -> Optional[OpenAI]:
    """构建 OpenAI 客户端。真实模式才会调用此函数。"""
    # API Key 从环境变量读取，避免写死在代码里。
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)
    if OpenAI is None:
        print("ERROR: openai package is not installed. Run: pip install openai", file=sys.stderr)
        sys.exit(1)
    # 返回 SDK 客户端，后续由 ask_once() 使用。
    return OpenAI(api_key=api_key)


def build_mock_answer(prompt: str) -> str:
    """生成本地 mock 回答，用于无 API Key 的学习环境。"""
    return (
        "[MOCK MODE]\n"
        f"收到问题: {prompt}\n"
        "这次没有调用真实 API。\n"
        "学习重点: build_client() 负责真实客户端，ask_once() 负责一次模型调用。"
    )


def ask_once(client: Optional[OpenAI], model: str, prompt: str, mode: str) -> str:
    """发送一次性请求并返回文本回答。"""
    # mock 模式只返回本地字符串，不消耗 API，也不需要网络。
    if mode == "mock":
        return build_mock_answer(prompt)

    # 防御式检查：真实模式必须有 client。
    if client is None:
        raise RuntimeError("client is required in real mode")

    # 真实模式：调用 Responses API。
    response = client.responses.create(
        model=model,
        instructions=SYSTEM_INSTRUCTIONS,
        input=prompt,
    )
    # Responses API 提供简化的输出接口 `output_text`
    # 注意：在复杂场景下，response 还包含 token-level 顶层结构、工具调用信息等。
    # 这里为了教学简洁，直接返回主文本回答；如果需要详细调试，可打印完整的 response 对象。
    return response.output_text


def main():
    # argparse 负责命令行参数解析。
    # 示例：
    #   python3 model_call_example.py --mock "你好"
    #   python3 model_call_example.py --real --model gpt-5 "你好"
    parser = argparse.ArgumentParser(description="Minimal model call example")
    # prompt 是位置参数；不传时使用默认问题。
    parser.add_argument("prompt", nargs="?", default="Hello, explain agents in one line")
    # --model 用于真实调用时切换模型。
    parser.add_argument("--model", default=DEFAULT_MODEL)
    # 互斥参数组：--mock 和 --real 不能同时出现。
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--mock", action="store_true", help="Force mock mode (no API key required)")
    mode_group.add_argument("--real", action="store_true", help="Force real API mode (requires OPENAI_API_KEY)")
    args = parser.parse_args()

    # 先决定运行模式，再决定是否需要构建真实客户端。
    mode = resolve_mode(args.mock, args.real)
    client = build_client() if mode == "real" else None
    # 执行一次问答，并把结果打印到终端。
    print(ask_once(client, args.model, args.prompt, mode))


if __name__ == "__main__":
    main()
