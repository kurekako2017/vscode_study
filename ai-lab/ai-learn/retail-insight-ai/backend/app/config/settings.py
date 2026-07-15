"""应用配置入口。

文件职责：统一从环境变量或 .env 读取并校验部署参数。
谁调用它：应用组合根、启动入口和配置测试。
它调用谁：Pydantic Settings，不调用业务 Service 或 Repository。
输入：环境变量、.env 或测试显式参数。
输出：类型安全 Settings，包括集中 JWT 算法、密钥与 30 分钟有效期。
设计理由：非法或不安全配置在启动时失败，避免运行中才出现认证漏洞。
日本现场面试：生产环境禁止沿用公开本地 JWT secret，配置校验采用 fail-fast。
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_LOCAL_JWT_SECRET = "erip-local-jwt-signing-key-change-before-deployment-2026"


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
    # JWT 参数集中管理；本地默认密钥只为 deterministic 开发/测试，部署时必须由环境变量覆盖。
    jwt_secret_key: SecretStr = SecretStr(_LOCAL_JWT_SECRET)
    jwt_algorithm: Literal["HS256"] = "HS256"
    jwt_access_token_expire_minutes: int = Field(default=30, ge=1, le=1440)
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
    # Reranker 只处理 retrieval 候选；Top-N 与默认 Final Top-K 在组合根集中注入。
    reranker_enabled: bool = True
    reranker_provider: Literal["deterministic"] = "deterministic"
    reranker_candidate_limit: int = Field(default=20, ge=1, le=100)
    reranker_top_k: int = Field(default=5, ge=1, le=100)
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

    @model_validator(mode="after")
    def validate_jwt_deployment_secret(self) -> "Settings":
        """拒绝短密钥，并禁止 staging/production 沿用公开的本地默认值。"""

        secret = self.jwt_secret_key.get_secret_value()
        if len(secret) < 32:
            raise ValueError("JWT_SECRET_KEY must contain at least 32 characters")
        if self.app_env in {"staging", "production"} and secret == _LOCAL_JWT_SECRET:
            raise ValueError(
                "JWT_SECRET_KEY must be overridden outside local/test environments"
            )
        return self
