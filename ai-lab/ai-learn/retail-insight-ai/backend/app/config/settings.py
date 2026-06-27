"""应用配置入口，统一从环境变量或 .env 读取部署参数。"""

from __future__ import annotations

from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """使用 Pydantic 校验配置，避免非法值进入业务流程后才失败。"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Retail Insight AI"
    app_env: Literal["local", "development", "test", "staging", "production"] = "local"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    service_name: str = "retail-insight-ai"
    task_execution_mode: Literal["background"] = "background"
    research_provider: Literal["static"] = "static"
    data_provider: Literal["static"] = "static"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://127.0.0.1:5173"])

    # 下面两项仅控制本地演示节奏和故障测试，不改变 Provider 类型。
    workflow_step_delay_seconds: float = Field(default=0.05, ge=0, le=10)
    static_research_fail: bool = False
