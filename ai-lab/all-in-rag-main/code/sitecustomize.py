"""
文件功能概述：`code/sitecustomize.py` 主要是 sitecustomize，这个文件里有 0 个类、2 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 函数 `_load_env_file`：先接收输入参数 env_path，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 splitlines、env_path.exists、raw_line.strip 等内部步骤完成主要工作，最后返回结果。
2. 函数 `_bootstrap`：先进入当前步骤，再调用 _load_env_file、os.environ.setdefault、resolve 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
"""


from __future__ import annotations

import os
from pathlib import Path


def _load_env_file(env_path: Path) -> None:  # 中文名称：加载envfile
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        os.environ.setdefault(key, value)


def _bootstrap() -> None:  # 中文名称：bootstrap
    current_dir = Path(__file__).resolve().parent
    repo_root = current_dir.parent
    _load_env_file(current_dir / ".env")
    _load_env_file(repo_root / ".env")

    os.environ.setdefault("OPENROUTER_API_KEY", "offline")
    os.environ.setdefault("OPENAI_API_KEY", os.getenv("OPENROUTER_API_KEY", "offline"))
    os.environ.setdefault("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    os.environ.setdefault("OPENAI_BASE_URL", os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"))
    os.environ.setdefault("OPENROUTER_MODEL", "openai/gpt-4o-mini")
    os.environ.setdefault("LLM_QWEN_MAX", os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"))


_bootstrap()
