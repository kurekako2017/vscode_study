from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """集中保存可通过环境变量覆盖的运行配置。"""

    app_name: str = "Retail Insight AI"
    environment: str = "local"
    log_level: str = "INFO"
    mock_provider: str = "mock"
    mock_step_delay_seconds: float = 0.05
    mock_fail_research: bool = False

    @classmethod
    def from_env(cls) -> "Settings":
        """从环境变量构造配置，避免业务代码到处直接读取操作系统环境。"""

        return cls(
            environment=os.getenv("APP_ENV", "local"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            mock_step_delay_seconds=float(os.getenv("MOCK_STEP_DELAY_SECONDS", "0.05")),
            mock_fail_research=os.getenv("MOCK_FAIL_RESEARCH", "false").lower()
            in {"1", "true", "yes"},
        )
