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
# OpenRouter 兼容服务默认基址。
DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
SYSTEM_INSTRUCTIONS = (
    "You are a minimal filesystem assistant for an LLM agent learning lab. "
    "Use tools when needed to inspect files. "
    "Only use available tool results; do not invent file contents."
)


def parse_args() -> argparse.Namespace:
    # 层次: 输入层 — 解析用户任务、模型与工作目录范围（支持 mock/real）
    """解析命令行参数：用户任务、模型名与允许访问的工作目录。"""
    parser = argparse.ArgumentParser(
        description="Minimal tool-calling agent demo for listing files, reading files, and searching text."
    )
    # 用户任务 ：用户任务说明
    parser.add_argument("prompt", help="Task request for the tool agent.")
    # 模型名 ：使用的模型名
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model name to use. Default: {DEFAULT_MODEL}",
    )
    # 工作目录 ：工具允许访问的工作目录
    parser.add_argument(
        "--workdir",
        default=".",
        help="Working directory the tools can access. Default: current directory.",
    )
    # 模式选择 ：互斥组，分别强制 mock 或强制 real
    parser.add_argument("--mock", action="store_true", help="Run in offline mock mode (no API calls).")
    # 模式选择 ：互斥组，分别强制 mock 或强制 real
    parser.add_argument("--real", action="store_true", help="Force real API mode (requires OPENROUTER_API_KEY or OPENAI_API_KEY).")
    return parser.parse_args()


def _has_real_credentials() -> bool:
    return bool(os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY"))


def build_client() -> OpenAI:
    # 层次: 基础设施层 — 构建 OpenAI 客户端并处理缺失 Key 的退出策略
    """从环境变量读取 API Key 并返回 OpenAI 兼容客户端实例（不存在则退出）。

    说明：该函数用于在真实模式（非 mock）下构建客户端。若没有设置 API Key，程序将打印错误并退出，避免运行时异常。
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
    """解析运行模式：mock 或 real。

    - `--mock` 强制本地 mock，不发起网络请求。
    - `--real` 强制真实调用，若未设置 API Key 则退出并提示。
    - 未指定时根据环境自动选择（有 API Key -> real，否则 mock）。
    """
    if force_mock:
        return "mock"
    if force_real:
        if not _has_real_credentials():
            print("ERROR: --real requested but OPENROUTER_API_KEY or OPENAI_API_KEY is not set.", file=sys.stderr)
            sys.exit(1)
        return "real"
    return "real" if _has_real_credentials() else "mock"


def build_mock_agent_response(prompt: str) -> str:
    """生成本地 mock 的最终回答文本（不调用 API）。"""
    return f"[MOCK MODE] Mocked tool agent response for: {prompt}\n(Use --real to call the API)"


def resolve_path(base_dir: Path, relative_path: str) -> Path:
    # 层次: 安全/IO 层 — 解析路径并确保文件操作受限于 workdir
    """解析相对路径并确保不越出 base_dir（安全限制）。

    说明：
    - 为避免模型或用户传入类似 `../` 的路径导致访问到不允许的文件，这里会把路径解析为绝对路径并检查其是否位于 `base_dir` 之下。
    - 若路径越界，会抛出 `ValueError`，调用者应捕获并处理。
    """
    candidate = (base_dir / relative_path).resolve()
    base_resolved = base_dir.resolve()
    # Keep every file operation inside the declared workdir.
    if candidate != base_resolved and base_resolved not in candidate.parents:
        raise ValueError("Path escapes the allowed working directory.")
    return candidate


def list_files(base_dir: Path, path: str = ".") -> dict[str, Any]:
    # 层次: 工具层 — 列出目录供模型参考的工具接口
    """列出目录内容，返回结构化的 entries 对象供模型参考。

    说明：该函数作为工具由 agent 在运行时调用，返回结构化数据（而非直接打印）以便模型理解目录结构。
    """
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
    """读取文件并返回前 12000 字符，避免一次性返回过大内容。

    说明：工具向模型返回内容时，通常需要限制大小以防止超出 token 上限或网络负担，因此这里只返回前 12k 字符。
    """
    # 解析路径并确保不越出 base_dir（安全限制）。
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

    说明：返回行级证据能够让模型在最终回答中精确地引用文件位置（例如文件名与行号），比只返回文件名更有助于可验证性。
    """
    # 解析路径并确保不越出 base_dir（安全限制）。
    target = resolve_path(base_dir, path)
    if not target.exists():
        return {"ok": False, "error": "Path does not exist."}
    # 如果目标是一个文件，则直接搜索该文件，否则搜索该目录下的所有文件  （递归搜索）
    matches = []
    files = [target] if target.is_file() else [p for p in target.rglob("*") if p.is_file()]
    # 遍历所有文件，搜索关键词  （不区分大小写）    
    for file_path in files:
        try:
            lines = file_path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        # 遍历所有行，搜索关键词  （不区分大小写）                  （如果匹配到了关键词，则添加到 matches 列表中，如果 matches 列表长度大于 50，则返回结果，否则继续搜索下一个文件）
        for line_number, line in enumerate(lines, start=1):
            if query.lower() in line.lower():
                matches.append({
                    "file": str(file_path),
                    "line": line_number,
                    "text": line.strip(),
                })
                if len(matches) >= 50:
                    return {"ok": True, "query": query, "matches": matches, "truncated": True}
    # 如果 matches 列表长度小于 50，则返回结果，否则返回截断标志（True），表示结果被截断了。            
    return {"ok": True, "query": query, "matches": matches, "truncated": False}


def call_tool(base_dir: Path, name: str, args: dict[str, Any]) -> dict[str, Any]:
    # 层次: 工具协调层 — 根据模型请求分发到具体工具实现
    """根据模型返回的工具调用名执行相应工具函数并返回结果。

    说明：这是模型与本地函数之间的桥梁，模型发起 `function_call`，这里负责把调用映射到真实实现并返回结构化结果。
    """
    # 根据工具名称调用对应函数，任何未识别的工具都会返回错误信息。
    if name == "list_files":
        return list_files(base_dir, path=args.get("path", "."))
    #   这里的工具调用接口非常简单，直接根据工具名称分发到对应函数。实际应用中可以添加更多工具并在此处进行分发。    if name == "read_file":
        return read_file(base_dir, path=args["path"])
    #  search_text 工具需要 query 参数，path 参数可选（默认为当前目录），调用时会返回匹配行的文件名、行号和文本内容。
    if name == "search_text":
        return search_text(base_dir, query=args["query"], path=args.get("path", "."))
    return {"ok": False, "error": f"Unknown tool: {name}"}


def build_tools() -> list[dict[str, Any]]:
    # 层次: 工具描述层 — 向模型暴露可用工具的 schema 与说明
    """返回供模型调用的工具描述（用于 Responses API 的 tools 参数）。"""
    # 说明：这里定义了工具的接口规范，包括参数类型、描述和调用约束，模型会根据这些信息来决定何时以及如何调用工具。
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


def run_agent(client: OpenAI | None, model: str, base_dir: Path, prompt: str, mode: str) -> str:
    # 层次: Agent 控制层 — 驱动模型与工具交互的主循环
    """运行一个最小的 agent 控制循环：

    1. 把用户指令传给模型
    2. 如果模型发起工具调用，则执行本地工具并把结果反馈回模型
    3. 重复直到模型返回最终回答或超过最大轮次
    """
    tools = build_tools()
    # 在 mock 模式下直接返回模拟回答，避免 SDK 调用
    # 改进：在 Mock 模式下模拟简单的工具调用逻辑，以便用户练习
    if mode == "mock":
        print(f"\n[MOCK MODE] 模拟 AI 思考中... 任务: {prompt}")
        
        # 简单的规则引擎：根据关键词模拟模型决定调用哪个工具，如果关键词包含“列出”、“list”、“目录”，则调用 list_files 工具，如果关键词包含“读取”、“read”，则调用 read_file 工具，如果关键词包含“搜索”、“search”，则调用 search_text 工具
        mock_tool_name = None
        mock_args = {}
        # 简单的规则引擎：根据关键词模拟模型决定调用哪个工具
        if "列出" in prompt or "list" in prompt.lower() or "目录" in prompt:
            mock_tool_name = "list_files"
            mock_args = {"path": "."}
        elif "读取" in prompt or "read" in prompt.lower():
            mock_tool_name = "read_file"
            mock_args = {"path": "README.md"} # 默认读取 README
        elif "搜索" in prompt or "search" in prompt.lower():
            mock_tool_name = "search_text"
            mock_args = {"query": "README", "path": "."}

        if mock_tool_name:
            print(f"[MOCK CALL] 模型决定调用工具: {mock_tool_name} 参数: {mock_args}")
            result = call_tool(base_dir, mock_tool_name, mock_args)
            return f"[MOCK RESULT] 工具返回结果: {json.dumps(result, ensure_ascii=False, indent=2)}\n\n(这是模拟运行，设置 API Key 后可体验完整推理)"
        
        return build_mock_agent_response(prompt)

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
        # 调用模型并传入工具描述，模型可能返回 `function_call` 指示需要执行某个工具
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
                # 解析模型提供的工具调用参数并执行对应工具
                args = json.loads(tool_call.arguments)
                # 执行工具并捕获结果，任何异常都被捕获并以错误信息形式返回给模型
                result = call_tool(base_dir, tool_call.name, args)
            except Exception as exc:
                result = {"ok": False, "error": str(exc)}

            # 把工具执行结果以特定消息类型回填给模型，模型会把这些结果纳入下一次推理输入
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
    # 解析运行模式（mock/real）并根据模式构建客户端（仅 real 模式需要）
    mode = resolve_mode(args.mock, args.real)
    # 在 real 模式下构建 OpenAI 客户端，mock 模式下保持 None 以避免 SDK 调用
    client = None
    if mode == "real":
        client = build_client()
        #   在 real 模式下，确保工作目录存在且是一个目录，否则退出并提示错误
    base_dir = Path(args.workdir).resolve()
    # 这里的安全检查确保了所有工具函数在访问文件时都受限于这个 base_dir，防止路径跳出导致安全问题。
    if not base_dir.exists() or not base_dir.is_dir():
        print("ERROR: --workdir must be an existing directory.", file=sys.stderr)
        sys.exit(1)

    try:
        # 这里会触发“模型判断 -> 调工具 -> 回填结果 -> 再判断”的闭环。
        answer = run_agent(client, args.model, base_dir, args.prompt, mode)
    except Exception as exc:
        print(f"ERROR: request failed: {exc}", file=sys.stderr)
        sys.exit(1)

    print(answer)


if __name__ == "__main__":
    main()
