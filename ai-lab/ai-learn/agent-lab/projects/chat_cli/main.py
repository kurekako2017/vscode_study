"""chat_cli: 最小可运行命令行对话示例（带注释）

层次划分说明：环境检查、模式决策、客户端构建、单次调用封装、输出格式化、交互循环等功能被划分为不同层次，便于理解和练习程序结构

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
from pathlib import Path
from typing import Any

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - used only when dependency is missing
    OpenAI = None

for _parent in Path(__file__).resolve().parents:
    if (_parent / "llm_runtime.py").exists():
        sys.path.insert(0, str(_parent))
        break
from llm_runtime import build_fallback_client, has_real_provider


DEFAULT_MODEL = "gpt-5"
"""默认模型名，可用 `--model` 覆盖。"""
# OpenRouter 兼容服务默认基址。
DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
# 系统提示词，用于告诉模型如何回答问题
SYSTEM_INSTRUCTIONS = (
    "你是一个简洁的助手，用于一个 LLM 代理学习实验室。"
    "回答清晰明了。"
)

# 层次: 输入层 — 负责命令行参数的定义与解析
def parse_args() -> argparse.Namespace:
    """解析命令行参数：支持自动模式、强制模式与输出截断配置。"""
    parser = argparse.ArgumentParser(
        description="最小 OpenAI 响应 API 聊天 CLI 演示程序."
    )
    # 用户任务 ：用户任务说明
    parser.add_argument(
        "prompt",
        help="用户任务说明",
    )
    # 模型名 ：使用的模型名
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"使用的模型名。默认: {DEFAULT_MODEL}",
    )
    # 模式选择：互斥组，分别强制 mock 或强制 real
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--mock",
        action="store_true",
        help="强制 mock 模式（无需 API 密钥）。",
    )
    mode_group.add_argument(
        "--real",
        action="store_true",
        help="强制真实 API 模式（需要 OPENROUTER_API_KEY 或 OPENAI_API_KEY）。",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=None,
        help="可选的最大输出字符数。示例：--max-chars 120",
    )
    return parser.parse_args()

# 层次划分说明：环境检查、模式决策、客户端构建、单次调用封装、输出格式化、交互循环等功能被划分为不同层次，便于理解和练习程序结构。
# - 基础设施层：负责客户端构建与外部依赖读取     （构建客户端并返回实例）       
def _has_real_credentials() -> bool:
    # 优先支持 OpenRouter，再兼容 OpenAI 官方接口。
    return has_real_provider()


def _build_openai_client() -> Any:
    # 统一构建 OpenAI 兼容客户端。
    if OpenAI is None:
        print("ERROR: openai package is not installed. Run: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

    return build_fallback_client()


def build_client(use_mock: bool) -> Any:
    # 层次: 基础设施层 — 负责客户端构建与外部依赖读取
    """从环境变量读取 API Key 并返回 OpenAI 客户端实例。

    若未配置 OpenRouter 或 OpenAI API Key，则打印错误并退出。
    """
    # 如果处于 mock 模式，直接返回 None，调用方会根据此判断不发起真实网络请求
    if use_mock:
        return None

    # 返回一个已配置的 OpenAI 客户端实例，后续可以调用 client.responses.create(...)
    return _build_openai_client()


def resolve_mode(force_mock: bool, force_real: bool) -> bool:
    # 层次: 基础设施/配置层 — 决定运行时是 mock 模式还是真实模式
    """解析运行模式并返回 use_mock。

    默认自动模式：
    - 明确 `--mock`：使用 mock
    - 明确 `--real`：使用真实 API
    - 未指定：检测环境，缺少 Key 或 SDK 时自动使用 mock
    """
    # 如果明确指定使用 mock 模式，则返回 True
    if force_mock:
        return True

    # 如果明确指定使用真实模式，则返回 False
    if force_real:
        return False

    # 如果未指定模式，则根据环境变量决定使用哪种模式
    if not _has_real_credentials():
        # 没有找到 API Key，自动切换到 mock 模式（本地演练而不触网）     （如果未找到 API Key，则自动切换到 mock 模式）
        print("INFO: 未设置 OPENROUTER_API_KEY / OPENAI_API_KEY，自动切换到 MOCK 模式.", file=sys.stderr)
        return True

    # 如果未指定模式，则根据环境变量决定使用哪种模式     （如果未指定模式，则根据环境变量决定使用哪种模式）
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
    #打印调试信息，显示调用的 prompt 和模式（mock 或 real），帮助理解程序流程
    print(f"DEBUG: ask_once 被调用，提示词为: {prompt[:30]}... (use_mock={use_mock})", file=sys.stderr)
    # 层次: 调用层 — 封装单次模型调用（支持 mock 或真实调用）
    """对给定 prompt 发起一次 Responses API 请求并返回主文本回答。"""
    # 如果是 mock 模式，返回本地生成的示例回答（无需网络）
    if use_mock:
        return build_mock_answer(prompt)

    # 在真实模式下，使用 SDK 发起请求并返回模型的主文本输出
    # 注意：不同 SDK/版本可能返回的结构不同，这里期望 `response.output_text` 为字符串
    response = client.responses.create(
        model=model,
        instructions=SYSTEM_INSTRUCTIONS,
        input=prompt,
    )

    # 直接返回 SDK 提供的文本字段，调用者会处理后续显示或截断
    return response.output_text


def format_output(answer: str, max_chars: int | None) -> str:
    # 层次: 业务逻辑层 — 根据参数对模型输出做后处理（例如截断）
    """按 max_chars 对输出做截断，便于练习参数驱动的业务逻辑。

    说明：
    - 如果 `max_chars` 为 `None`，返回完整 `answer`。
    - 如果 `max_chars` 为正整数且小于 `answer` 长度，返回截断后的字符串并在末尾标注被省略的字符数。
    - 如果 `max_chars` <= 0，会抛出 `ValueError`，提醒调用者传入合法参数。

    示例：
        format_output("Hello world", 5) -> "Hello\n...[truncated 6 chars]"
    """
    # 如果 max_chars 为 None，则返回完整 answer
    if max_chars is None:
        return answer

    # 如果 max_chars 小于等于 0，则抛出异常
    if max_chars <= 0:
        raise ValueError("--max-chars must be greater than 0")

    # 如果 answer 长度小于等于 max_chars，则返回完整 answer
    if len(answer) <= max_chars:
        return answer

    # 计算被截断的字符数
    omitted = len(answer) - max_chars
    # 返回截断后的 answer     （返回截断后的 answer，并在末尾标注被省略的字符数）
    return f"{answer[:max_chars]}\n...[truncated {omitted} chars]"


def run_interactive(client: Any, model: str, use_mock: bool, max_chars: int | None) -> None:
    # 层次: 控制层 — 实现交互循环、退出条件与异常处理
    """进入交互循环，逐条读取用户输入并请求模型回答。"""
    # 启动提示信息
    print(f"chat_cli 以模型启动: {model}")
    # 如果 use_mock 为 True，则打印提示信息
    if use_mock:
        # 打印提示信息     （如果 use_mock 为 True，则打印提示信息）
        print("以模拟模式运行（无需 API 密钥）.")
    # 打印提示信息     （如果 use_mock 为 False，则打印提示信息）
    print("Type 'exit' or 'quit' to stop.")
    # 打印提示信息     （如果 use_mock 为 False，则打印提示信息）

    # 循环读取用户输入，逐次发起模型请求
    while True:
        try:
            # 从标准输入读取用户的问题
            # 从标准输入读取用户的问题     （从标准输入读取用户的问题）
            user_input = input("\nYou> ").strip()
        except (EOFError, KeyboardInterrupt):
            # 当用户按 Ctrl+C 或 Ctrl+D 时优雅退出
            # 当用户按 Ctrl+C 或 Ctrl+D 时优雅退出     （当用户按 Ctrl+C 或 Ctrl+D 时优雅退出）
            print("\nBye.")
            return

        # 忽略空输入
        if not user_input:
            # 忽略空输入     （如果 user_input 为空，则继续循环）
            continue

        # 支持键入 'exit' 或 'quit' 来结束交互
        if user_input.lower() in {"exit", "quit"}:
            print("Bye.")
            return

        try:
            # 发起一次调用并对结果进行可选截断
            answer = ask_once(client, model, user_input, use_mock)
            answer = format_output(answer, max_chars)
        except Exception as exc:
            # 捕获请求或处理过程中的异常，打印并继续交互循环
            print(f"ERROR: request failed: {exc}", file=sys.stderr)
            continue

        # 打印模型或 mock 的回答
        print(f"\nAssistant> {answer}")


def main() -> None:
    # 层次: 程序入口 — 组织整体流程：解析参数、决策模式、调用和输出
    """程序入口：串起参数解析、模式决策、模型调用与输出格式化。"""
    args = parse_args()
    # 模式决策。先根据参数和环境决定是否使用 mock，再构建客户端，减少分支散落。
    use_mock = resolve_mode(args.mock, args.real)
    # 以下是与客户端交互的设置，后续调用 ask_once 时会根据 use_mock 决定是否发起真实请求。
    client = build_client(use_mock)

    if args.prompt:
        try:
            # 一次性（非交互）调用：调用一次 ask 并输出结果
            answer = ask_once(client, args.model, args.prompt, use_mock)
            print(format_output(answer, args.max_chars))
        except Exception as exc:
            # 如果发生任何错误，打印并以非零状态码退出（方便脚本检测失败）
            print(f"ERROR: request failed: {exc}", file=sys.stderr)
            sys.exit(1)
        return

    # 若没有指定 prompt，则进入交互模式，复用同一 client 和参数
    run_interactive(client, args.model, use_mock, args.max_chars)


if __name__ == "__main__":
    main()
