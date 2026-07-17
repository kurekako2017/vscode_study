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

from decimal import Decimal
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
    # 兼容旧变量；权威开关为 llm_provider_mode（LLM_PROVIDER_MODE）。
    # stub：仅 stub-low/high；fallback_chain：OpenRouter→NVIDIA→Gemini→Local Qwen；
    # openrouter：单 Provider 兼容模式（不绕过 Gateway/Ledger/Audit）。
    llm_provider: Literal["stub", "openrouter", "fallback_chain"] = "stub"
    llm_provider_mode: Literal["stub", "openrouter", "fallback_chain"] = "stub"
    # 保留旧环境变量的解析兼容，但组合根永久禁止普通 RAG 调用 Provider。
    internal_rag_use_llm: bool = False
    llm_stub_behavior: Literal["success", "timeout", "failure", "rate_limit", "partial_failure"] = "success"
    llm_timeout_seconds: float = Field(default=10.0, gt=0, le=120)
    # Fallback Chain 总时间与最大 attempt（每个 Provider 默认一次）
    llm_total_timeout_seconds: float = Field(default=120.0, gt=0, le=600)
    llm_max_provider_attempts: int = Field(default=4, ge=1, le=4)
    # Circuit Breaker（秒级；测试注入可控时钟，不 sleep）
    llm_circuit_failure_threshold: int = Field(default=3, ge=1, le=20)
    llm_circuit_open_duration_seconds: float = Field(default=30.0, gt=0, le=3600)
    llm_circuit_half_open_probe_limit: int = Field(default=1, ge=1, le=5)
    # low_cost / ai_analysis 政策（Stub 默认；OpenRouter 模式由 validator 覆盖 alias/model/price）
    llm_low_cost_provider_alias: str = "stub-low-cost"
    llm_low_cost_model_name: str = "stub-low-cost-v1"
    llm_max_input_tokens: int = Field(default=2048, ge=128, le=100_000)
    llm_max_output_tokens: int = Field(default=256, ge=1, le=4096)
    llm_evidence_max_count: int = Field(default=5, ge=1, le=20)
    llm_evidence_max_chars: int = Field(default=6000, ge=128, le=100_000)
    llm_request_max_cost: Decimal = Field(default=Decimal("0.050000"), ge=0)
    llm_user_daily_request_limit: int = Field(default=20, ge=1)
    llm_user_daily_token_limit: int = Field(default=50_000, ge=1)
    llm_user_daily_cost_limit: Decimal = Field(default=Decimal("0.500000"), ge=0)
    llm_global_daily_request_limit: int = Field(default=200, ge=1)
    llm_global_daily_token_limit: int = Field(default=500_000, ge=1)
    llm_global_daily_cost_limit: Decimal = Field(default=Decimal("5.000000"), ge=0)
    llm_input_price_per_million: Decimal = Field(default=Decimal("0.500000"), ge=0)
    llm_output_price_per_million: Decimal = Field(default=Decimal("1.500000"), ge=0)
    # high_quality / executive_report 独立政策
    llm_high_quality_provider_alias: str = "stub-high-quality"
    llm_high_quality_model_name: str = "stub-high-quality-v1"
    llm_hq_max_input_tokens: int = Field(default=4096, ge=128, le=100_000)
    llm_hq_max_output_tokens: int = Field(default=1024, ge=1, le=8192)
    llm_hq_evidence_max_chars: int = Field(default=12000, ge=128, le=200_000)
    llm_hq_request_max_cost: Decimal = Field(default=Decimal("0.250000"), ge=0)
    llm_hq_user_daily_request_limit: int = Field(default=5, ge=1)
    llm_hq_user_daily_token_limit: int = Field(default=40_000, ge=1)
    llm_hq_user_daily_cost_limit: Decimal = Field(default=Decimal("1.000000"), ge=0)
    llm_hq_global_daily_request_limit: int = Field(default=50, ge=1)
    llm_hq_global_daily_token_limit: int = Field(default=200_000, ge=1)
    llm_hq_global_daily_cost_limit: Decimal = Field(default=Decimal("10.000000"), ge=0)
    llm_hq_input_price_per_million: Decimal = Field(default=Decimal("3.000000"), ge=0)
    llm_hq_output_price_per_million: Decimal = Field(default=Decimal("9.000000"), ge=0)
    llm_currency: str = Field(default="USD", min_length=3, max_length=3)
    # ---- OpenRouter ----
    # 价格单位：USD / 百万 tokens（input 与 output 分开）；历史价格写入 Ledger snapshot。
    openrouter_enabled: bool = False
    openrouter_api_key: SecretStr | None = None
    openrouter_base_url: str = Field(default="https://openrouter.ai/api/v1", min_length=8, max_length=256)
    openrouter_low_cost_model: str | None = Field(default=None, max_length=200)
    openrouter_high_quality_model: str | None = Field(default=None, max_length=200)
    openrouter_low_input_price: Decimal = Field(default=Decimal("0.500000"), ge=0)
    openrouter_low_output_price: Decimal = Field(default=Decimal("1.500000"), ge=0)
    openrouter_high_input_price: Decimal = Field(default=Decimal("3.000000"), ge=0)
    openrouter_high_output_price: Decimal = Field(default=Decimal("9.000000"), ge=0)
    openrouter_http_referer: str | None = Field(default=None, max_length=512)
    openrouter_app_title: str | None = Field(default=None, max_length=128)
    openrouter_attempt_timeout_seconds: float = Field(default=20.0, gt=0, le=300)
    real_llm_timeout_seconds: float = Field(default=30.0, gt=0, le=120)
    real_llm_max_retries: int = Field(default=1, ge=0, le=2)
    # ---- NVIDIA ----
    nvidia_enabled: bool = False
    nvidia_api_key: SecretStr | None = None
    nvidia_base_url: str = Field(default="https://integrate.api.nvidia.com/v1", min_length=8, max_length=256)
    nvidia_low_cost_model: str | None = Field(default=None, max_length=200)
    nvidia_high_quality_model: str | None = Field(default=None, max_length=200)
    nvidia_low_input_price: Decimal = Field(default=Decimal("0.200000"), ge=0)
    nvidia_low_output_price: Decimal = Field(default=Decimal("0.600000"), ge=0)
    nvidia_high_input_price: Decimal = Field(default=Decimal("1.000000"), ge=0)
    nvidia_high_output_price: Decimal = Field(default=Decimal("3.000000"), ge=0)
    nvidia_attempt_timeout_seconds: float = Field(default=20.0, gt=0, le=300)
    # ---- Gemini ----
    gemini_enabled: bool = False
    gemini_api_key: SecretStr | None = None
    gemini_base_url: str = Field(
        default="https://generativelanguage.googleapis.com/v1beta", min_length=8, max_length=256
    )
    gemini_low_cost_model: str | None = Field(default=None, max_length=200)
    gemini_high_quality_model: str | None = Field(default=None, max_length=200)
    gemini_low_input_price: Decimal = Field(default=Decimal("0.100000"), ge=0)
    gemini_low_output_price: Decimal = Field(default=Decimal("0.400000"), ge=0)
    gemini_high_input_price: Decimal = Field(default=Decimal("1.250000"), ge=0)
    gemini_high_output_price: Decimal = Field(default=Decimal("5.000000"), ge=0)
    gemini_attempt_timeout_seconds: float = Field(default=20.0, gt=0, le=300)
    # ---- Local Qwen（本地 OpenAI-compatible；不自动下载/启动模型服务）----
    local_qwen_enabled: bool = False
    local_qwen_api_key: SecretStr | None = None
    local_qwen_require_api_key: bool = False
    local_qwen_base_url: str = Field(default="http://127.0.0.1:11434/v1", min_length=8, max_length=256)
    local_qwen_low_cost_model: str | None = Field(default=None, max_length=200)
    local_qwen_high_quality_model: str | None = Field(default=None, max_length=200)
    # Local 通常无云费用；仍用 Decimal 价格快照（可为 0）以统一账本。
    local_qwen_low_input_price: Decimal = Field(default=Decimal("0.000000"), ge=0)
    local_qwen_low_output_price: Decimal = Field(default=Decimal("0.000000"), ge=0)
    local_qwen_high_input_price: Decimal = Field(default=Decimal("0.000000"), ge=0)
    local_qwen_high_output_price: Decimal = Field(default=Decimal("0.000000"), ge=0)
    local_qwen_attempt_timeout_seconds: float = Field(default=60.0, gt=0, le=600)
    # 仅手动 smoke；默认测试 suite 永远不得打开。
    run_real_llm_smoke: bool = False
    run_openrouter_smoke: bool = False
    run_nvidia_smoke: bool = False
    run_gemini_smoke: bool = False
    run_local_qwen_smoke: bool = False
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
    def validate_jwt_and_llm_provider_mode(self) -> "Settings":
        """拒绝短密钥，并在真实 Provider 模式下 fail-closed 校验必要配置。"""

        secret = self.jwt_secret_key.get_secret_value()
        if len(secret) < 32:
            raise ValueError("JWT_SECRET_KEY must contain at least 32 characters")
        if self.app_env in {"staging", "production"} and secret == _LOCAL_JWT_SECRET:
            raise ValueError(
                "JWT_SECRET_KEY must be overridden outside local/test environments"
            )

        # 兼容 LLM_PROVIDER 与 LLM_PROVIDER_MODE；任一非 stub 时以 mode 为准。
        mode = self.llm_provider_mode
        if self.llm_provider in {"openrouter", "fallback_chain"} and mode == "stub":
            mode = self.llm_provider
            object.__setattr__(self, "llm_provider_mode", mode)
        object.__setattr__(self, "llm_provider", mode)

        if mode == "stub":
            object.__setattr__(self, "llm_low_cost_provider_alias", "stub-low-cost")
            object.__setattr__(self, "llm_high_quality_provider_alias", "stub-high-quality")
            if not self.llm_low_cost_model_name:
                object.__setattr__(self, "llm_low_cost_model_name", "stub-low-cost-v1")
            if not self.llm_high_quality_model_name:
                object.__setattr__(self, "llm_high_quality_model_name", "stub-high-quality-v1")
            return self

        if mode not in {"openrouter", "fallback_chain"}:
            raise ValueError("LLM_PROVIDER_MODE must be stub, openrouter, or fallback_chain")

        # 延迟导入避免循环：registry 依赖 Settings 类型但不在 import 时构建实例。
        from app.llm.provider_registry import (
            build_provider_endpoints,
            enabled_chain_endpoints,
            validate_endpoint_or_raise,
        )

        if mode == "openrouter":
            # 单 Provider 兼容模式：强制仅 OpenRouter，不建立第二套业务逻辑。
            object.__setattr__(self, "openrouter_enabled", True)
            object.__setattr__(self, "nvidia_enabled", False)
            object.__setattr__(self, "gemini_enabled", False)
            object.__setattr__(self, "local_qwen_enabled", False)
            # 兼容旧单超时配置
            object.__setattr__(self, "openrouter_attempt_timeout_seconds", self.real_llm_timeout_seconds)

            api_key = self.openrouter_api_key.get_secret_value().strip() if self.openrouter_api_key else ""
            if not api_key:
                raise ValueError("OPENROUTER_API_KEY is required when LLM_PROVIDER_MODE=openrouter")
            low_model = (self.openrouter_low_cost_model or "").strip()
            high_model = (self.openrouter_high_quality_model or "").strip()
            if not low_model:
                raise ValueError("OPENROUTER_LOW_COST_MODEL is required when LLM_PROVIDER_MODE=openrouter")
            if not high_model:
                raise ValueError("OPENROUTER_HIGH_QUALITY_MODEL is required when LLM_PROVIDER_MODE=openrouter")
            if low_model == high_model:
                raise ValueError("OPENROUTER low_cost and high_quality models must be distinct")

            object.__setattr__(self, "llm_low_cost_provider_alias", "openrouter-low-cost")
            object.__setattr__(self, "llm_high_quality_provider_alias", "openrouter-high-quality")
            object.__setattr__(self, "llm_low_cost_model_name", low_model)
            object.__setattr__(self, "llm_high_quality_model_name", high_model)
            object.__setattr__(self, "llm_input_price_per_million", self.openrouter_low_input_price)
            object.__setattr__(self, "llm_output_price_per_million", self.openrouter_low_output_price)
            object.__setattr__(self, "llm_hq_input_price_per_million", self.openrouter_high_input_price)
            object.__setattr__(self, "llm_hq_output_price_per_million", self.openrouter_high_output_price)
            object.__setattr__(self, "llm_timeout_seconds", self.real_llm_timeout_seconds)
            return self

        # fallback_chain：至少一个 enabled 且配置完整的 Provider。
        endpoints = build_provider_endpoints(self)
        for endpoint in endpoints:
            if endpoint.enabled:
                validate_endpoint_or_raise(endpoint)

        enabled = enabled_chain_endpoints(self)
        if not enabled:
            raise ValueError(
                "LLM_PROVIDER_MODE=fallback_chain requires at least one enabled and fully configured provider"
            )

        # Policy 快照使用 Chain 首个 enabled Provider 的价格与模型作为初始预占参考。
        first = enabled[0]
        object.__setattr__(self, "llm_low_cost_provider_alias", first.name)
        object.__setattr__(self, "llm_high_quality_provider_alias", first.name)
        object.__setattr__(self, "llm_low_cost_model_name", first.low_cost_model)
        object.__setattr__(self, "llm_high_quality_model_name", first.high_quality_model)
        object.__setattr__(self, "llm_input_price_per_million", first.low_input_price_per_million)
        object.__setattr__(self, "llm_output_price_per_million", first.low_output_price_per_million)
        object.__setattr__(self, "llm_hq_input_price_per_million", first.high_input_price_per_million)
        object.__setattr__(self, "llm_hq_output_price_per_million", first.high_output_price_per_million)
        object.__setattr__(self, "llm_timeout_seconds", self.llm_total_timeout_seconds)
        return self

    def openrouter_api_key_configured(self) -> bool:
        """只报告是否配置，不暴露值、长度或前后缀。"""

        if self.openrouter_api_key is None:
            return False
        return bool(self.openrouter_api_key.get_secret_value().strip())

    def nvidia_api_key_configured(self) -> bool:
        if self.nvidia_api_key is None:
            return False
        return bool(self.nvidia_api_key.get_secret_value().strip())

    def gemini_api_key_configured(self) -> bool:
        if self.gemini_api_key is None:
            return False
        return bool(self.gemini_api_key.get_secret_value().strip())

    def local_qwen_api_key_configured(self) -> bool:
        if self.local_qwen_api_key is None:
            return False
        return bool(self.local_qwen_api_key.get_secret_value().strip())
