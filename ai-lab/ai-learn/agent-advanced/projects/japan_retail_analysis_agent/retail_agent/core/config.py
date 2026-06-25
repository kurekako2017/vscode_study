from __future__ import annotations

"""Application configuration.

教学要点：
- 真实现场不要把端口、CORS、DB 路径写死在业务代码里。
- 这里用 dataclass 包装环境变量，让 server、repository、Docker 使用同一套配置。
- 后续接 SSO、真实 DWH、企业搜索时，也应该从这一层读取配置。
"""

import os
from dataclasses import dataclass
from pathlib import Path

from ..settings import PROJECT_DIR


@dataclass(frozen=True)
class AppSettings:
    """Runtime settings read from environment variables.

    日本现场项目通常会有 local/dev/stg/prod 多环境。这个类就是最小的
    settings object，避免在 router、service、repository 里到处读 os.getenv。
    """

    app_name: str = "Japan Retail Analysis Agent"
    environment: str = os.getenv("APP_ENV", "local")
    host: str = os.getenv("APP_HOST", "127.0.0.1")
    port: int = int(os.getenv("APP_PORT", "8020"))
    allowed_origins: tuple[str, ...] = tuple(
        origin.strip()
        for origin in os.getenv("CORS_ALLOWED_ORIGINS", "*").split(",")
        if origin.strip()
    )
    runtime_dir: Path = Path(os.getenv("RUNTIME_DIR", str(PROJECT_DIR / "runtime")))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    @property
    def task_db_path(self) -> Path:
        return self.runtime_dir / "checkpoints.sqlite3"

    @property
    def langgraph_db_path(self) -> Path:
        return self.runtime_dir / "langgraph.sqlite3"


def get_settings() -> AppSettings:
    """Factory function kept small so FastAPI dependencies/tests can override it later."""
    return AppSettings()
