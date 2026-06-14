from __future__ import annotations

import importlib.machinery
import importlib.util
import os
import sys
from pathlib import Path


DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_OPENROUTER_MODEL = "openai/gpt-4o-mini"
CODE_DIR = Path(__file__).resolve().parent


def resolve_openrouter_api_key() -> str:
    for name in ("OPENROUTER_API_KEY", "openRouterAPI", "openRouter"):
        value = os.getenv(name)
        if value:
            cleaned = value.strip()
            if cleaned:
                return cleaned
    return ""


def resolve_openrouter_base_url() -> str:
    value = os.getenv("OPENROUTER_BASE_URL", DEFAULT_OPENROUTER_BASE_URL)
    return value.strip() or DEFAULT_OPENROUTER_BASE_URL


def resolve_openrouter_model() -> str:
    value = os.getenv("OPENROUTER_MODEL", DEFAULT_OPENROUTER_MODEL)
    return value.strip() or DEFAULT_OPENROUTER_MODEL


def ensure_openrouter_env() -> None:
    api_key = resolve_openrouter_api_key()
    if api_key:
        os.environ["OPENROUTER_API_KEY"] = api_key
        os.environ.setdefault("OPENAI_API_KEY", api_key)

    base_url = resolve_openrouter_base_url()
    os.environ["OPENROUTER_BASE_URL"] = base_url
    os.environ.setdefault("OPENAI_BASE_URL", base_url)

    model = resolve_openrouter_model()
    os.environ["OPENROUTER_MODEL"] = model
    os.environ.setdefault("LLM_QWEN_MAX", model)


def describe_openrouter_runtime() -> str:
    ensure_openrouter_env()
    return f"OpenRouter model: {os.environ['OPENROUTER_MODEL']} | base_url: {os.environ['OPENROUTER_BASE_URL']}"


def load_real_openai_class():
    module_name = "_all_in_rag_real_openai"
    cached = sys.modules.get(module_name)
    if cached is not None:
        return getattr(cached, "OpenAI", None)

    search_paths = []
    for item in sys.path:
        try:
            if Path(item).resolve() == CODE_DIR:
                continue
        except Exception:
            pass
        search_paths.append(item)

    spec = importlib.machinery.PathFinder.find_spec("openai", search_paths)
    if spec is None or spec.origin is None:
        return None

    origin = Path(spec.origin).resolve()
    if origin == (CODE_DIR / "openai.py").resolve():
        return None

    if spec.submodule_search_locations:
        alias_spec = importlib.util.spec_from_file_location(
            module_name,
            spec.origin,
            submodule_search_locations=list(spec.submodule_search_locations),
        )
    else:
        alias_spec = importlib.util.spec_from_file_location(module_name, spec.origin)

    if alias_spec is None or alias_spec.loader is None:
        return None

    module = importlib.util.module_from_spec(alias_spec)
    sys.modules[module_name] = module
    alias_spec.loader.exec_module(module)
    return getattr(module, "OpenAI", None)
