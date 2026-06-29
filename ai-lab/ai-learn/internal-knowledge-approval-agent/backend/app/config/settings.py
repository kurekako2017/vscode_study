from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """集中管理可配置项，避免业务代码散落环境变量读取。"""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    service_name: str = "internal-knowledge-approval-agent"
    log_level: str = "INFO"
    database_path: Path = PROJECT_ROOT / "data" / "knowledge_approval.db"
    workflow_step_delay_seconds: float = Field(default=0.08, ge=0, le=5)
    cors_origins: list[str] = ["http://127.0.0.1:5173", "http://localhost:5173"]

