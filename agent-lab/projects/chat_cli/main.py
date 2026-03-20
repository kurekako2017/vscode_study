import argparse
import os
import sys

from openai import OpenAI


DEFAULT_MODEL = "gpt-5"
SYSTEM_INSTRUCTIONS = (
    "You are a concise assistant for an LLM agent learning lab. "
    "Answer clearly and briefly."
)


def parse_args() -> argparse.Namespace:
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
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)
    return OpenAI(api_key=api_key)


def ask_once(client: OpenAI, model: str, prompt: str) -> str:
    # This is the smallest possible model-call path used in the lab.
    response = client.responses.create(
        model=model,
        instructions=SYSTEM_INSTRUCTIONS,
        input=prompt,
    )
    return response.output_text


def run_interactive(client: OpenAI, model: str) -> None:
    print(f"chat_cli started with model: {model}")
    print("Type 'exit' or 'quit' to stop.")

    # Interactive mode is useful for learning the API flow before adding history or tools.
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
            answer = ask_once(client, model, user_input)
        except Exception as exc:
            print(f"ERROR: request failed: {exc}", file=sys.stderr)
            continue

        print(f"\nAssistant> {answer}")


def main() -> None:
    args = parse_args()
    client = build_client()

    # Support both one-shot and interactive usage so the demo stays easy to test.
    if args.prompt:
        try:
            print(ask_once(client, args.model, args.prompt))
        except Exception as exc:
            print(f"ERROR: request failed: {exc}", file=sys.stderr)
            sys.exit(1)
        return

    run_interactive(client, args.model)


if __name__ == "__main__":
    main()
