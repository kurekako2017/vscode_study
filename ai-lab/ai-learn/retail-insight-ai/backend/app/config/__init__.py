"""Application configuration.

注意：不在包初始化时导入 container，避免与 app.llm.* 形成循环依赖。
"""

from app.config.settings import Settings

__all__ = ["AppContainer", "Settings", "build_container"]


def __getattr__(name: str):
    if name in {"AppContainer", "build_container"}:
        from app.config.container import AppContainer, build_container

        return AppContainer if name == "AppContainer" else build_container
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
