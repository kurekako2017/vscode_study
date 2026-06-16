"""Shared runtime configuration helpers.

This module stays dependency-free so it can be imported from early bootstrap
code such as ``sitecustomize.py`` and from scripts before the full project
dependencies are loaded.
"""

from __future__ import annotations

import os
from pathlib import Path

DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_OPENROUTER_MODEL = "openai/gpt-4o-mini"
DEFAULT_NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
DEFAULT_OLLAMA_BASE_URL = "http://localhost:11434/v1"
DEFAULT_OLLAMA_MODEL = "qwen2.5-coder:1.5b"


def load_local_env_file(root: Path | None = None) -> None:
    """Load a simple ``.env`` file from the project root if present."""
    env_root = root or Path(__file__).resolve().parents[1]
    env_path = env_root / ".env"
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


def _pick_llm_provider() -> str:
    provider = os.getenv("LLM_PROVIDER", "openrouter").strip().lower()
    if provider not in {"openrouter", "nvidia", "ollama", "auto"}:
        return "openrouter"
    return provider


def _build_openrouter_config() -> dict[str, str | bool | list[str]]:
    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    base_url = os.getenv("OPENROUTER_BASE_URL", DEFAULT_OPENROUTER_BASE_URL).strip()
    model = (
        os.getenv("OPENROUTER_MODEL")
        or os.getenv("LLM_QWEN_MAX")
        or DEFAULT_OPENROUTER_MODEL
    ).strip()
    missing: list[str] = []
    if not api_key:
        missing.append("OPENROUTER_API_KEY")
    if not base_url:
        missing.append("OPENROUTER_BASE_URL")
    if not model:
        missing.append("LLM_QWEN_MAX")

    return {
        "provider": "openrouter",
        "source": "openrouter",
        "api_key": api_key,
        "base_url": base_url,
        "model": model,
        "configured": not missing,
        "missing": missing,
    }


def _build_nvidia_config() -> dict[str, str | bool | list[str]]:
    api_key = os.getenv("NVIDIA_API_KEY", "").strip()
    base_url = os.getenv("NVIDIA_BASE_URL", DEFAULT_NVIDIA_BASE_URL).strip()
    model = os.getenv("NVIDIA_MODEL", "").strip()
    missing: list[str] = []
    if not api_key:
        missing.append("NVIDIA_API_KEY")
    if not base_url:
        missing.append("NVIDIA_BASE_URL")
    if not model:
        missing.append("NVIDIA_MODEL")

    return {
        "provider": "nvidia",
        "source": "nvidia",
        "api_key": api_key,
        "base_url": base_url,
        "model": model,
        "configured": not missing,
        "missing": missing,
    }


def _build_ollama_config() -> dict[str, str | bool | list[str]]:
    api_key = os.getenv("OLLAMA_API_KEY", "ollama").strip() or "ollama"
    base_url = os.getenv("OLLAMA_BASE_URL", DEFAULT_OLLAMA_BASE_URL).strip()
    model = os.getenv("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL).strip()
    missing: list[str] = []
    if not base_url:
        missing.append("OLLAMA_BASE_URL")
    if not model:
        missing.append("OLLAMA_MODEL")

    return {
        "provider": "ollama",
        "source": "ollama",
        "api_key": api_key,
        "base_url": base_url,
        "model": model,
        "configured": not missing,
        "missing": missing,
    }


def resolve_llm_config(preferred_provider: str | None = None) -> dict[str, str | bool | list[str]]:
    """Resolve the effective LLM backend.

    OpenRouter is the default cloud path. NVIDIA and Ollama are available when
    selected explicitly, and ``auto`` prefers configured cloud settings before
    falling back to the local Ollama model.
    """
    provider = (preferred_provider or _pick_llm_provider()).strip().lower()
    if provider not in {"openrouter", "nvidia", "ollama", "auto"}:
        provider = _pick_llm_provider()
    openrouter = _build_openrouter_config()
    nvidia = _build_nvidia_config()
    ollama = _build_ollama_config()

    if provider == "openrouter":
        return openrouter
    if provider == "nvidia":
        return nvidia
    if provider == "ollama":
        return ollama

    if openrouter["configured"]:
        return openrouter
    if nvidia["configured"]:
        return nvidia
    if ollama["configured"]:
        return ollama

    return openrouter


def apply_openai_compatible_env(
    config: dict[str, str | bool | list[str]],
    *,
    override: bool = False,
) -> None:
    """Map the resolved backend into OpenAI-compatible environment variables."""
    api_key = str(config.get("api_key") or "")
    base_url = str(config.get("base_url") or "")
    model = str(config.get("model") or "")

    if api_key:
        if override or not os.getenv("OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] = api_key
    if base_url:
        if override or not os.getenv("OPENAI_BASE_URL"):
            os.environ["OPENAI_BASE_URL"] = base_url
    if model:
        if override or not os.getenv("LLM_QWEN_MAX"):
            os.environ["LLM_QWEN_MAX"] = model
