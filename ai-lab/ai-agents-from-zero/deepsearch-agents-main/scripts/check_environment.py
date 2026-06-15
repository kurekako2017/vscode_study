#!/usr/bin/env python3
"""Check the local environment needed by DeepSearch Agents.

This script is intentionally dependency-free so it can run before the full
project dependencies are installed.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.runtime_config import resolve_llm_config


REQUIRED_COMMANDS = ["python3", "node", "npm"]
MYSQL_REQUIRED_ENV_VARS = [
    "MYSQL_HOST",
    "MYSQL_PORT",
    "MYSQL_USER",
    "MYSQL_PASSWORD",
    "MYSQL_DATABASE",
]
OPTIONAL_ENV_VARS = [
    "LLM_PROVIDER",
    "OPENROUTER_BASE_URL",
    "OPENROUTER_API_KEY",
    "OPENROUTER_MODEL",
    "LLM_QWEN_MAX",
    "NVIDIA_API_KEY",
    "NVIDIA_BASE_URL",
    "NVIDIA_MODEL",
    "MYSQL_CHARSET",
    "MYSQL_COLLATION",
    "MYSQL_SQL_MODE",
    "TAVILY_API_KEY",
    "RAGFLOW_API_URL",
    "RAGFLOW_API_KEY",
]


def load_dotenv_if_present() -> None:
    """Load a simple .env file from the project root if present."""
    env_path = ROOT / ".env"
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


def check_commands() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    for cmd in REQUIRED_COMMANDS:
        resolved = shutil.which(cmd)
        results.append((cmd, resolved is not None, resolved or "missing"))
    return results


def check_env_vars() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    for name in MYSQL_REQUIRED_ENV_VARS:
        value = os.getenv(name, "").strip()
        if value:
            masked = value if name in {"MYSQL_PORT", "MYSQL_HOST", "MYSQL_DATABASE"} else value[:4] + "..."
            results.append((name, True, masked))
        else:
            results.append((name, False, "missing"))
    return results


def check_llm_config() -> tuple[bool, str]:
    """Check whether the effective LLM configuration is usable."""
    config = resolve_llm_config()
    if config["configured"]:
        return True, f"LLM config looks usable via {config['source']}."

    missing = ", ".join(config.get("missing", [])) or "unknown"
    return False, f"LLM config missing: {missing}"


def print_section(title: str) -> None:
    print(f"\n== {title} ==")


def main() -> int:
    load_dotenv_if_present()

    print_section("Runtime")
    print(f"python: {sys.version.split()[0]}")
    print(f"executable: {sys.executable}")

    print_section("Commands")
    for name, ok, detail in check_commands():
        status = "OK" if ok else "MISSING"
        print(f"{name:8} {status:7} {detail}")

    print_section("Environment Variables")
    missing = 0
    for name, ok, detail in check_env_vars():
        status = "OK" if ok else "MISSING"
        if not ok:
            missing += 1
        print(f"{name:24} {status:7} {detail}")

    llm_ok, llm_detail = check_llm_config()
    print(f"{'LLM (OpenAI-compatible)':24} {'OK' if llm_ok else 'MISSING':7} {llm_detail}")
    if not llm_ok:
        missing += 1

    print_section("Optional Environment Variables")
    for name in OPTIONAL_ENV_VARS:
        value = os.getenv(name, "").strip()
        status = "OK" if value else "EMPTY"
        detail = value if value and name in {"NVIDIA_BASE_URL", "OPENROUTER_BASE_URL"} else (value[:4] + "..." if value else "empty")
        print(f"{name:24} {status:7} {detail}")

    print_section("Summary")
    if missing:
        print(f"Environment is incomplete: {missing} required variable(s) missing.")
    else:
        print("Environment variables look ready.")

    return 0 if missing == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
