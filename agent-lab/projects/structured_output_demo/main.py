import argparse
import json
import os
import sys
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel, Field


DEFAULT_MODEL = "gpt-4o"
SYSTEM_INSTRUCTIONS = (
    "You are an assistant for an LLM agent learning lab. "
    "Analyze the user's idea and return a structured development plan."
)


class AgentPlan(BaseModel):
    # The schema is the contract that keeps model output stable enough for downstream code.
    goal: str = Field(description="The main goal of the requested agent.")
    user_type: Literal["beginner", "intermediate", "advanced"] = Field(
        description="Estimated user level for this project."
    )
    core_capabilities: list[str] = Field(
        description="Key capabilities the agent should have."
    )
    tools: list[str] = Field(description="Recommended tools or functions.")
    deliverables: list[str] = Field(
        description="Concrete output artifacts or demos to build."
    )
    risks: list[str] = Field(description="Main development risks or cautions.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Minimal structured output demo with OpenAI Responses API."
    )
    parser.add_argument("prompt", help="Natural-language project request.")
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


def generate_plan(client: OpenAI, model: str, prompt: str) -> AgentPlan:
    # responses.parse lets the SDK validate the model output against the Pydantic schema.
    response = client.responses.parse(
        model=model,
        instructions=SYSTEM_INSTRUCTIONS,
        input=prompt,
        text_format=AgentPlan,
    )
    return response.output_parsed


def main() -> None:
    args = parse_args()
    client = build_client()

    try:
        plan = generate_plan(client, args.model, args.prompt)
    except Exception as exc:
        print(f"ERROR: request failed: {exc}", file=sys.stderr)
        sys.exit(1)

    # Show both a readable view and a compact JSON string for API-oriented learning.
    pretty_json = json.dumps(plan.model_dump(), ensure_ascii=False, indent=2)
    compact_json = plan.model_dump_json(ensure_ascii=False)

    print("=== Parsed JSON ===")
    print(pretty_json)
    print("\n=== Raw JSON ===")
    print(compact_json)


if __name__ == "__main__":
    main()
