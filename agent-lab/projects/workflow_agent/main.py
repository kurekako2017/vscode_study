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
    # This schema keeps the planning step stable enough for the next workflow stage.
    goal: str = Field(description="The main goal of the task.")
    priority: Literal["low", "medium", "high"] = Field(
        description="Estimated priority of the task."
    )
    steps: list[str] = Field(description="Recommended execution steps.")
    deliverables: list[str] = Field(description="Expected outputs.")
    risks: list[str] = Field(description="Main risks or cautions.")


def parse_args() -> argparse.Namespace:
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
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)
    return OpenAI(api_key=api_key)


def analyze_task(client: OpenAI, model: str, prompt: str) -> str:
    response = client.responses.create(
        model=model,
        instructions=ANALYZE_INSTRUCTIONS,
        input=prompt,
    )
    return response.output_text


def plan_task(client: OpenAI, model: str, analysis: str) -> WorkflowPlan:
    response = client.responses.parse(
        model=model,
        instructions=PLAN_INSTRUCTIONS,
        input=analysis,
        text_format=WorkflowPlan,
    )
    return response.output_parsed


def finalize_task(client: OpenAI, model: str, analysis: str, plan: WorkflowPlan) -> str:
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
        analysis = analyze_task(client, args.model, args.prompt)
        plan = plan_task(client, args.model, analysis)
        final_summary = finalize_task(client, args.model, analysis, plan)
    except Exception as exc:
        print(f"ERROR: request failed: {exc}", file=sys.stderr)
        sys.exit(1)

    print("=== Step 1: Analysis ===")
    print(analysis)
    print("\n=== Step 2: Plan ===")
    print(json.dumps(plan.model_dump(), ensure_ascii=False, indent=2))
    print("\n=== Step 3: Final Summary ===")
    print(final_summary)


if __name__ == "__main__":
    main()
