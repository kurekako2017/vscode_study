"""tool_agent_demo: 最小 Tool-Calling Agent 示例（带注释）。

此示例展示如何：
- 定义一组可供模型调用的本地工具（列出目录、读取文件、文本检索）
- 以循环方式让模型选择工具、执行工具、并把工具输出反馈回模型

示例的安全考虑：所有文件操作被限制在指定的 `workdir` 内，防止路径跳出。

学习地图：
- 运行命令：
    - python3 main.py "请概览当前目录结构" --workdir .
    - python3 main.py "请搜索 README 中的 RAG 关键词并总结" --workdir .
- 输入输出：
    - 输入：用户任务 + workdir 目录范围
    - 输出：模型最终回答（中间通过工具调用收集证据）
- 改造练习点：
    - 新增 write_file 工具并做白名单限制
    - 给 search_text 增加文件类型过滤参数
    - 记录每轮工具调用日志到本地
"""

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
    # 层次: 输入层 — 解析用户任务、模型与工作目录范围
    """解析命令行参数：用户任务、模型名与允许访问的工作目录。"""
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
    # 层次: 基础设施层 — 构建 OpenAI 客户端并处理缺失 Key 的退出策略
    """从环境变量读取 API Key 并返回 OpenAI 客户端实例（不存在则退出）。"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)
    return OpenAI(api_key=api_key)


def resolve_path(base_dir: Path, relative_path: str) -> Path:
    # 层次: 安全/IO 层 — 解析路径并确保文件操作受限于 workdir
    """解析相对路径并确保不越出 base_dir（安全限制）。"""
    candidate = (base_dir / relative_path).resolve()
    base_resolved = base_dir.resolve()
    # Keep every file operation inside the declared workdir.
    if candidate != base_resolved and base_resolved not in candidate.parents:
        raise ValueError("Path escapes the allowed working directory.")
    return candidate


def list_files(base_dir: Path, path: str = ".") -> dict[str, Any]:
    # 层次: 工具层 — 列出目录供模型参考的工具接口
    """列出目录内容，返回结构化的 entries 对象供模型参考。"""
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
    # 层次: 工具层 — 读取文件并限制返回大小以避免过大返回
    """读取文件并返回前 12000 字符，避免一次性返回过大内容。"""
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
    # 层次: 工具层 — 在文件中搜索文本，返回行级证据供模型引用
    """在路径下所有文件中按行搜索 query（不区分大小写），返回匹配的行和行号。

    返回行级别证据便于模型在最终回答中引用来源。
    """
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
    # 层次: 工具协调层 — 根据模型请求分发到具体工具实现
    """根据模型返回的工具调用名执行相应工具函数并返回结果。"""
    if name == "list_files":
        return list_files(base_dir, path=args.get("path", "."))
    if name == "read_file":
        return read_file(base_dir, path=args["path"])
    if name == "search_text":
        return search_text(base_dir, query=args["query"], path=args.get("path", "."))
    return {"ok": False, "error": f"Unknown tool: {name}"}


def build_tools() -> list[dict[str, Any]]:
    # 层次: 工具描述层 — 向模型暴露可用工具的 schema 与说明
    """返回供模型调用的工具描述（用于 Responses API 的 tools 参数）。"""
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
    # 层次: Agent 控制层 — 驱动模型与工具交互的主循环
    """运行一个最小的 agent 控制循环：

    1. 把用户指令传给模型
    2. 如果模型发起工具调用，则执行本地工具并把结果反馈回模型
    3. 重复直到模型返回最终回答或超过最大轮次
    """
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
            # 如果没有工具调用，说明模型产出了最终回答文本，直接返回
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
    # 层次: 程序入口 — 验证输入并启动 agent 控制循环
    """主流程：校验工作目录后进入工具调用循环并输出最终答案。"""
    args = parse_args()
    client = build_client()
    base_dir = Path(args.workdir).resolve()

    if not base_dir.exists() or not base_dir.is_dir():
        print("ERROR: --workdir must be an existing directory.", file=sys.stderr)
        sys.exit(1)

    try:
        # 这里会触发“模型判断 -> 调工具 -> 回填结果 -> 再判断”的闭环。
        answer = run_agent(client, args.model, base_dir, args.prompt)
    except Exception as exc:
        print(f"ERROR: request failed: {exc}", file=sys.stderr)
        sys.exit(1)

    print(answer)


if __name__ == "__main__":
    main()
