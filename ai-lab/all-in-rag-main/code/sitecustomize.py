"""Code-directory startup hooks for all-in-rag-main.

This file lets `python ...` launched from `code/` automatically:
1. Load a nearby `.env` file if present.
2. Fall back to the repository root `.env`.
3. Mirror `OPENROUTER_*` into OpenAI-compatible variables for libraries that
   only understand `OPENAI_*`.
4. Provide a safe default model name when only OpenRouter credentials are set.
"""

from __future__ import annotations

import os
from pathlib import Path


def _load_env_file(env_path: Path) -> None:
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


def _bootstrap() -> None:
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
