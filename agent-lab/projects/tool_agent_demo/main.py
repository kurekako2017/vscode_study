import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from openai import OpenAI


DEFAULT_MODEL = "gpt-5"
MAX_TOOL_ROUNDS = 8
SYSTEM_INSTRUCTIONS = (
    "You are a minimal filesystem assistant for an LLM agent learning lab. "
    "Use tools when needed to inspect files. "
    "Only use available tool results; do not invent file contents."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Minimal tool-calling agent demo for listing files, reading files, and searching text."
    )
    parser.add_argument("prompt", help="Task request for the tool agent.")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model name to use. Default: {DEFAULT_MODEL}",
    )
    parser.add_argument(
        "--workdir",
        default=".",
        help="Working directory the tools can access. Default: current directory.",
    )
    return parser.parse_args()


def build_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)
    return OpenAI(api_key=api_key)


def resolve_path(base_dir: Path, relative_path: str) -> Path:
    candidate = (base_dir / relative_path).resolve()
    base_resolved = base_dir.resolve()
    # Keep every file operation inside the declared workdir.
    if candidate != base_resolved and base_resolved not in candidate.parents:
        raise ValueError("Path escapes the allowed working directory.")
    return candidate


def list_files(base_dir: Path, path: str = ".") -> dict[str, Any]:
    target = resolve_path(base_dir, path)
    if not target.exists():
        return {"ok": False, "error": "Path does not exist."}
    if not target.is_dir():
        return {"ok": False, "error": "Path is not a directory."}

    entries = []
    for item in sorted(target.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
        entries.append(
            {
                "name": item.name,
                "type": "dir" if item.is_dir() else "file",
            }
        )
    return {"ok": True, "path": str(target), "entries": entries}


def read_file(base_dir: Path, path: str) -> dict[str, Any]:
    target = resolve_path(base_dir, path)
    if not target.exists():
        return {"ok": False, "error": "File does not exist."}
    if not target.is_file():
        return {"ok": False, "error": "Path is not a file."}

    try:
        content = target.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return {"ok": False, "error": "File is not valid UTF-8 text."}

    return {"ok": True, "path": str(target), "content": content[:12000]}


def search_text(base_dir: Path, query: str, path: str = ".") -> dict[str, Any]:
    target = resolve_path(base_dir, path)
    if not target.exists():
        return {"ok": False, "error": "Path does not exist."}

    matches = []
    files = [target] if target.is_file() else [p for p in target.rglob("*") if p.is_file()]

    for file_path in files:
        try:
            lines = file_path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue

        # Return line-level matches so the final answer can point to concrete evidence.
        for line_number, line in enumerate(lines, start=1):
            if query.lower() in line.lower():
                matches.append(
                    {
                        "file": str(file_path),
                        "line": line_number,
                        "text": line.strip(),
                    }
                )
                if len(matches) >= 50:
                    return {"ok": True, "query": query, "matches": matches, "truncated": True}

    return {"ok": True, "query": query, "matches": matches, "truncated": False}


def call_tool(base_dir: Path, name: str, args: dict[str, Any]) -> dict[str, Any]:
    if name == "list_files":
        return list_files(base_dir, path=args.get("path", "."))
    if name == "read_file":
        return read_file(base_dir, path=args["path"])
    if name == "search_text":
        return search_text(base_dir, query=args["query"], path=args.get("path", "."))
    return {"ok": False, "error": f"Unknown tool: {name}"}


def build_tools() -> list[dict[str, Any]]:
    return [
        {
            "type": "function",
            "name": "list_files",
            "description": "List files and subdirectories under a relative directory path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative directory path. Use '.' for the current working directory.",
                    }
                },
                "required": [],
                "additionalProperties": False,
            },
            "strict": True,
        },
        {
            "type": "function",
            "name": "read_file",
            "description": "Read a UTF-8 text file under the working directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative file path to read.",
                    }
                },
                "required": ["path"],
                "additionalProperties": False,
            },
            "strict": True,
        },
        {
            "type": "function",
            "name": "search_text",
            "description": "Search case-insensitive text in files under a relative path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Text to search for.",
                    },
                    "path": {
                        "type": "string",
                        "description": "Relative directory or file path. Use '.' for the working directory.",
                    },
                },
                "required": ["query"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    ]


def run_agent(client: OpenAI, model: str, base_dir: Path, prompt: str) -> str:
    tools = build_tools()
    input_items: list[dict[str, Any]] = [
        {
            "role": "user",
            "content": (
                f"Working directory: {base_dir.resolve()}\n"
                f"User task: {prompt}"
            ),
        }
    ]

    # Minimal tool loop: ask the model, execute tool calls, then feed tool results back.
    for _ in range(MAX_TOOL_ROUNDS):
        response = client.responses.create(
            model=model,
            instructions=SYSTEM_INSTRUCTIONS,
            input=input_items,
            tools=tools,
        )

        tool_calls = [item for item in response.output if item.type == "function_call"]
        if not tool_calls:
            return response.output_text

        for tool_call in tool_calls:
            try:
                args = json.loads(tool_call.arguments)
                result = call_tool(base_dir, tool_call.name, args)
            except Exception as exc:
                result = {"ok": False, "error": str(exc)}

            # function_call_output is the bridge between local tool execution and the next model step.
            input_items.append(
                {
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": json.dumps(result, ensure_ascii=False),
                }
            )

    return "ERROR: Agent stopped because it exceeded the maximum number of tool rounds."


def main() -> None:
    args = parse_args()
    client = build_client()
    base_dir = Path(args.workdir).resolve()

    if not base_dir.exists() or not base_dir.is_dir():
        print("ERROR: --workdir must be an existing directory.", file=sys.stderr)
        sys.exit(1)

    try:
        answer = run_agent(client, args.model, base_dir, args.prompt)
    except Exception as exc:
        print(f"ERROR: request failed: {exc}", file=sys.stderr)
        sys.exit(1)

    print(answer)


if __name__ == "__main__":
    main()
