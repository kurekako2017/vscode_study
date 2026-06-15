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

from app.runtime_config import apply_openai_compatible_env, load_local_env_file, resolve_llm_config


def _bootstrap() -> None:
    root = Path(__file__).resolve().parent
    load_local_env_file(root)
    apply_openai_compatible_env(resolve_llm_config())


_bootstrap()
