"""Project-wide environment bootstrap for all-in-rag-main.

This keeps the example scripts runnable from the repository root by:
1. Loading a local `.env` file when present.
2. Mirroring `OPENROUTER_*` into OpenAI-compatible variables for libraries that
   only understand `OPENAI_*`.
3. Supplying a safe default model name if none was configured.
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
    root = Path(__file__).resolve().parent
    _load_env_file(root / ".env")
    _load_env_file(root / "code" / ".env")

    os.environ.setdefault("OPENROUTER_API_KEY", "offline")
    os.environ.setdefault("OPENAI_API_KEY", os.getenv("OPENROUTER_API_KEY", "offline"))
    os.environ.setdefault("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    os.environ.setdefault("OPENAI_BASE_URL", os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"))
    os.environ.setdefault("OPENROUTER_MODEL", "openai/gpt-4o-mini")
    os.environ.setdefault("LLM_QWEN_MAX", os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"))


_bootstrap()
