"""chat_cli: 最小可运行命令行对话示例（带注释）

此文件在 `llm-lab/projects` 下为学习者提供了可运行的最小示例。
它演示了如何：
- 读取环境变量 `OPENAI_API_KEY`
- 使用 OpenAI Responses API 发起单次请求
- 支持一口气提问和交互模式

注意：此文件为教学用途，交互模式不保存历史，上线或生产时请添加重试、超时和认证等逻辑。
"""

import argparse
import os
import sys

from openai import OpenAI


DEFAULT_MODEL = "gpt-5"
"""默认模型名。可通过 `--model` 覆盖。"""

SYSTEM_INSTRUCTIONS = (
    "You are a concise assistant for an LLM agent learning lab. "
    "Answer clearly and briefly."
)
"""系统指令，传给模型以控制总体回答风格。"""


def parse_args() -> argparse.Namespace:
    """解析命令行参数。

    支持两种用法：
    1. 一次性提问：`python main.py "一句话提问"`
    2. 交互模式：`python main.py`（回车进入交互）
    """
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
    return parser.parse_args()


def build_client() -> OpenAI:
    """从环境变量读取 API Key 并构建 OpenAI 客户端。

    如果未设置，则打印错误并退出。实际项目中建议使用更安全的密钥管理方式。
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)
    # OpenAI client 将在内部处理网络请求
    return OpenAI(api_key=api_key)


def ask_once(client: OpenAI, model: str, prompt: str) -> str:
    """发送一次性查询并返回纯文本回答。

    这里使用 Responses API 的 `create` 方法。
    """
    response = client.responses.create(
        model=model,
        instructions=SYSTEM_INSTRUCTIONS,
        input=prompt,
    )
    # Responses API 在返回对象上提供 `output_text` 便于快速取到主回答内容
    return response.output_text


def run_interactive(client: OpenAI, model: str) -> None:
    """进入交互模式：不断读取用户输入并逐次请求模型。

    交互模式主要用于学习 API 调用流程，生产环境请加入限速、超时和错误重试策略。
    """
    print(f"chat_cli started with model: {model}")
    print("Type 'exit' or 'quit' to stop.")

    while True:
        try:
            # 读取用户输入并去除首尾空白
            user_input = input("\nYou> ").strip()
        except (EOFError, KeyboardInterrupt):
            # 捕获 Ctrl+C / Ctrl+D 并优雅退出
            print("\nBye.")
            return

        if not user_input:
            # 空输入忽略
            continue

        if user_input.lower() in {"exit", "quit"}:
            print("Bye.")
            return

        try:
            # 发起请求并打印回答
            answer = ask_once(client, model, user_input)
        except Exception as exc:
            # 简单错误处理：打印错误并继续交互
            print(f"ERROR: request failed: {exc}", file=sys.stderr)
            continue

        print(f"\nAssistant> {answer}")


def main() -> None:
    """主入口：支持一次性提问与交互模式两种运行方式。"""
    args = parse_args()
    client = build_client()

    # 如果传入 prompt，则作为一次性请求并退出
    if args.prompt:
        try:
            print(ask_once(client, args.model, args.prompt))
        except Exception as exc:
            print(f"ERROR: request failed: {exc}", file=sys.stderr)
            sys.exit(1)
        return

    # 否则进入交互模式
    run_interactive(client, args.model)


if __name__ == "__main__":
    main()
