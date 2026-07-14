"""应用配置入口，统一从环境变量或 .env 读取部署参数。"""

from __future__ import annotations

from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """使用 Pydantic 校验配置，避免非法值进入业务流程后才失败。"""

    model_config = SettingsConfigDict(
        # 从 backend 启动时优先读取项目根 .env；backend/.env 可用于本机临时覆盖。
        env_file=("../.env", ".env"),
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
    llm_provider: Literal["stub"] = "stub"
    internal_rag_use_llm: bool = False
    # deterministic_test 只服务本地回归；默认 disabled，生产不会把测试向量当成语义向量。
    embedding_provider: Literal[
        "disabled", "deterministic_test", "local", "openai", "openrouter", "nvidia"
    ] = "disabled"
    embedding_model: str | None = None
    embedding_dimensions: int = Field(default=384, gt=0)
    hybrid_keyword_weight: float = Field(default=0.5, ge=0, le=1)
    hybrid_vector_weight: float = Field(default=0.5, ge=0, le=1)
    learning_trace: bool = False
    repository_backend: Literal["inmemory", "postgres"] = "inmemory"
    # PostgreSQL 模式优先使用标准 DATABASE_URL；InMemory 默认模式不会读取或连接它。
    database_url: str | None = None
    postgres_host: str = "127.0.0.1"
    postgres_port: int = 5432
    postgres_db: str = "retail_insight_ai"
    postgres_user: str = "retail_user"
    postgres_password: str = "retail_password"
    cors_origins: list[str] = Field(
        default_factory=lambda: [
            "http://127.0.0.1:5173",
            "http://localhost:5173",
        ]
    )

    # 下面两项仅控制本地演示节奏和故障测试，不改变 Provider 类型。
    workflow_step_delay_seconds: float = Field(default=0.05, ge=0, le=10)
    static_research_fail: bool = False
