"""chat_cli: 最小可运行命令行对话示例（带注释）

演示内容：
- 从环境变量读取 `OPENAI_API_KEY` 并构建客户端
- 支持一次性提问或交互模式
- 调用 Responses API 并打印文本回答

此文件为学习用途，生产环境需要补入重试、超时和安全的密钥管理。

学习地图：
- 运行命令：
    - python3 main.py "问题"
    - python3 main.py --mock "问题"
    - python3 main.py --mock --max-chars 120 "问题"
- 输入输出：
    - 输入：命令行 prompt、--mock/--real 模式参数、--max-chars 截断参数
    - 输出：模型回答（可选截断），或 mock 固定风格回答
- 改造练习点：
    - 增加 --max-lines 参数，限制输出行数
    - 为 mock 输出增加多种模板风格
    - 把模式决策提取为独立策略类
"""

import argparse
import os
import sys
from typing import Any

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - used only when dependency is missing
    OpenAI = None


DEFAULT_MODEL = "gpt-5"
"""默认模型名，可用 `--model` 覆盖。"""

SYSTEM_INSTRUCTIONS = (
    "You are a concise assistant for an LLM agent learning lab. "
    "Answer clearly and briefly."
)


def parse_args() -> argparse.Namespace:
    # 层次: 输入层 — 负责命令行参数的定义与解析
    """解析命令行参数：支持自动模式、强制模式与输出截断配置。"""
    parser = argparse.ArgumentParser(
        description="Minimal OpenAI Responses API chat CLI demo."
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        help="Optional one-shot prompt. If omitted, interactive mode starts.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model name to use. Default: {DEFAULT_MODEL}",
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--mock",
        action="store_true",
        help="Force mock mode (no API key required).",
    )
    mode_group.add_argument(
        "--real",
        action="store_true",
        help="Force real API mode (requires OPENAI_API_KEY).",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=None,
        help="Optional max output characters. Example: --max-chars 120",
    )
    return parser.parse_args()


def build_client(use_mock: bool) -> Any:
    # 层次: 基础设施层 — 负责客户端构建与外部依赖读取
    """从环境变量读取 API Key 并返回 OpenAI 客户端实例。

    若未配置 `OPENAI_API_KEY`，则打印错误并退出。
    """
    if use_mock:
        return None

    if OpenAI is None:
        print("ERROR: openai package is not installed. Run: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)
    return OpenAI(api_key=api_key)


def resolve_mode(force_mock: bool, force_real: bool) -> bool:
    # 层次: 基础设施/配置层 — 决定运行时是 mock 模式还是真实模式
    """解析运行模式并返回 use_mock。

    默认自动模式：
    - 明确 `--mock`：使用 mock
    - 明确 `--real`：使用真实 API
    - 未指定：检测环境，缺少 Key 或 SDK 时自动使用 mock
    """
    if force_mock:
        return True

    if force_real:
        return False

    if not os.getenv("OPENAI_API_KEY"):
        print("INFO: OPENAI_API_KEY not set, auto-switching to MOCK mode.", file=sys.stderr)
        return True

    if OpenAI is None:
        print("INFO: openai package not installed, auto-switching to MOCK mode.", file=sys.stderr)
        return True

    return False


def build_mock_answer(prompt: str) -> str:
    # 层次: 练习辅助层 — 本地 mock 响应生成逻辑（无外部依赖）
    """生成固定风格的本地 mock 回答，用于零成本练习程序结构。"""
    normalized = " ".join(prompt.strip().split())
    preview = normalized[:60] + ("..." if len(normalized) > 60 else "")
    return (
        "[MOCK MODE]\n"
        f"收到问题: {preview}\n"
        "练习建议:\n"
        "1) 观察 parse_args() 如何接收参数\n"
        "2) 观察 run_interactive() 的循环与退出条件\n"
        "3) 后续再切换真实 API 调用"
    )


def ask_once(client: Any, model: str, prompt: str, use_mock: bool) -> str:
    # 层次: 调用层 — 封装单次模型调用（支持 mock 或真实调用）
    """对给定 prompt 发起一次 Responses API 请求并返回主文本回答。"""
    if use_mock:
        return build_mock_answer(prompt)

    response = client.responses.create(
        model=model,
        instructions=SYSTEM_INSTRUCTIONS,
        input=prompt,
    )
    return response.output_text


def format_output(answer: str, max_chars: int | None) -> str:
    # 层次: 业务逻辑层 — 根据参数对模型输出做后处理（例如截断）
    """按 max_chars 对输出做截断，便于练习参数驱动的业务逻辑。"""
    if max_chars is None:
        return answer

    if max_chars <= 0:
        raise ValueError("--max-chars must be greater than 0")

    if len(answer) <= max_chars:
        return answer

    omitted = len(answer) - max_chars
    return f"{answer[:max_chars]}\n...[truncated {omitted} chars]"


def run_interactive(client: Any, model: str, use_mock: bool, max_chars: int | None) -> None:
    # 层次: 控制层 — 实现交互循环、退出条件与异常处理
    """进入交互循环，逐条读取用户输入并请求模型回答。"""
    print(f"chat_cli started with model: {model}")
    if use_mock:
        print("Running in MOCK mode (no API key required).")
    print("Type 'exit' or 'quit' to stop.")

    while True:
        try:
            user_input = input("\nYou> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            return

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit"}:
            print("Bye.")
            return

        try:
            answer = ask_once(client, model, user_input, use_mock)
            answer = format_output(answer, max_chars)
        except Exception as exc:
            print(f"ERROR: request failed: {exc}", file=sys.stderr)
            continue

        print(f"\nAssistant> {answer}")


def main() -> None:
    # 层次: 程序入口 — 组织整体流程：解析参数、决策模式、调用和输出
    """程序入口：串起参数解析、模式决策、模型调用与输出格式化。"""
    args = parse_args()
    # 先根据参数和环境决定是否使用 mock，再构建客户端，减少分支散落。
    use_mock = resolve_mode(args.mock, args.real)
    client = build_client(use_mock)

    if args.prompt:
        try:
            # 一次性调用：请求 -> 输出截断（可选）-> 打印。
            answer = ask_once(client, args.model, args.prompt, use_mock)
            print(format_output(answer, args.max_chars))
        except Exception as exc:
            print(f"ERROR: request failed: {exc}", file=sys.stderr)
            sys.exit(1)
        return

    # 交互调用：循环读取输入并复用同一套业务逻辑。
    run_interactive(client, args.model, use_mock, args.max_chars)


if __name__ == "__main__":
    main()
