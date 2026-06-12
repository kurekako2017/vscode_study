"""Project-wide environment bootstrap.

This module is imported automatically by Python when it is present on the
import path. It keeps the examples runnable from the repository root by:

1. Loading a local `.env` file if present.
2. Mirroring `OPENROUTER_*` into `OPENAI_*` for OpenAI-compatible clients.
3. Providing a sane default model name when only OpenRouter is configured.

The implementation is dependency-free on purpose so it works before project
dependencies are installed.
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

    if os.getenv("OPENROUTER_API_KEY"):
        os.environ.setdefault("OPENAI_API_KEY", os.getenv("OPENROUTER_API_KEY", ""))
    if os.getenv("OPENROUTER_BASE_URL"):
        os.environ.setdefault("OPENAI_BASE_URL", os.getenv("OPENROUTER_BASE_URL", ""))
    if os.getenv("OPENROUTER_MODEL") and not os.getenv("LLM_QWEN_MAX"):
        os.environ.setdefault("LLM_QWEN_MAX", os.getenv("OPENROUTER_MODEL", ""))
    if os.getenv("OPENROUTER_API_KEY") and not os.getenv("LLM_QWEN_MAX"):
        os.environ.setdefault("LLM_QWEN_MAX", "openai/gpt-4o-mini")


_bootstrap()

