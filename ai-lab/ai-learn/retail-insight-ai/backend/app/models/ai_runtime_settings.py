"""AI Runtime 持久化领域模型。

文件职责：描述 PostgreSQL 单例配置行（mode / kill_switch / version / actor）。
谁调用它：Repository、AiRuntimeService、Admin API。
它调用谁：无（纯数据合同）。
输入：数据库行或服务层构造。
输出：不可变 dataclass。
为什么需要：进程内切换会在重启后丢失；多实例必须共享同一 PostgreSQL 事实。
日本现场面试：配置与 Secret 分离——DB 只存开关，Key 只在环境变量。
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal

AiRuntimeMode = Literal["stub", "openrouter", "fallback_chain"]

# 单例行主键；全进程 / 多实例共用这一行。
AI_RUNTIME_SINGLETON_KEY = "default"

# Stub → Real 二次确认固定文案（前端展示，后端校验）。
ENABLE_REAL_CONFIRMATION_TEXT = "ENABLE_REAL_LLM"

ALLOWED_AI_RUNTIME_MODES: frozenset[str] = frozenset({"stub", "openrouter", "fallback_chain"})


@dataclass(frozen=True)
class AiRuntimeSettingsRecord:
    """ai_runtime_settings 表的领域快照；不含任何 Secret。"""

    setting_key: str
    mode: AiRuntimeMode
    real_calls_enabled: bool
    kill_switch: bool
    version: int
    updated_by_user_id: str | None
    updated_by_username: str | None
    updated_at: datetime

    @property
    def effective_mode(self) -> AiRuntimeMode:
        """Kill Switch 打开时强制 stub，否则使用已配置 mode。"""

        if self.kill_switch:
            return "stub"
        return self.mode


__all__ = [
    "AI_RUNTIME_SINGLETON_KEY",
    "ALLOWED_AI_RUNTIME_MODES",
    "AiRuntimeMode",
    "AiRuntimeSettingsRecord",
    "ENABLE_REAL_CONFIRMATION_TEXT",
]
