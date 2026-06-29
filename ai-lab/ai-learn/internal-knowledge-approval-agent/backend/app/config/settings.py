"""Backend 配置模型。

文件职责：集中读取环境变量并提供带类型和默认值的 Settings。
谁调用它：Container 和 Main；它调用 pydantic-settings，不访问业务层。
输入：环境变量或构造参数；输出：经过校验的配置对象。
为什么需要这一层：避免各文件直接读取环境变量，也避免密钥进入代码。
初学者重点：字段默认值用于纯本地运行，``.env`` 只覆盖配置。
日本现场面试：可说明配置与代码分离；企业级由 Secret Manager 注入敏感值。
"""

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
