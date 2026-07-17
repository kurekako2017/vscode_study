"""PostgreSQL AI Runtime Settings Repository。

文件职责：读写 ai_runtime_settings 单例行，支持 expected_version 乐观锁。
谁调用它：AiRuntimeService、build_container 启动恢复。
它调用谁：PostgresConnectionFactory。
输入：mode / kill_switch / actor / expected_version。
输出：AiRuntimeSettingsRecord；冲突抛 VersionConflict。
为什么需要：Backend 重启与多实例必须共享同一配置事实。
日本现场面试：配置走 Repository + 乐观锁，不把 Key 写入表。
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from app.db.connection import PostgresConnectionFactory
from app.models.ai_runtime_settings import (
    AI_RUNTIME_SINGLETON_KEY,
    AiRuntimeMode,
    AiRuntimeSettingsRecord,
)


@dataclass(frozen=True)
class AiRuntimeVersionConflictError(Exception):
    """expected_version 与库中 version 不一致。"""

    current: AiRuntimeSettingsRecord | None
    expected_version: int


class PostgresAiRuntimeSettingsRepository:
    """ai_runtime_settings 单例仓储；仅 PostgreSQL。"""

    def __init__(self, connection_factory: PostgresConnectionFactory) -> None:
        self._factory = connection_factory

    def get(self, setting_key: str = AI_RUNTIME_SINGLETON_KEY) -> AiRuntimeSettingsRecord | None:
        with self._factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT setting_key, mode, real_calls_enabled, kill_switch,
                           version, updated_by_user_id, updated_by_username, updated_at
                    FROM ai_runtime_settings
                    WHERE setting_key = %s
                    """,
                    (setting_key,),
                )
                row = cursor.fetchone()
        if row is None:
            return None
        return self._to_record(row)

    def get_or_initialize(
        self,
        *,
        default_mode: AiRuntimeMode,
        setting_key: str = AI_RUNTIME_SINGLETON_KEY,
    ) -> AiRuntimeSettingsRecord:
        """缺少记录时用 LLM_PROVIDER_MODE 默认值插入单例行。"""

        existing = self.get(setting_key)
        if existing is not None:
            return existing
        now = datetime.now(timezone.utc)
        real_calls = default_mode != "stub"
        with self._factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO ai_runtime_settings (
                      setting_key, mode, real_calls_enabled, kill_switch,
                      version, updated_by_user_id, updated_by_username, updated_at
                    ) VALUES (%s, %s, %s, FALSE, 1, NULL, NULL, %s)
                    ON CONFLICT (setting_key) DO NOTHING
                    """,
                    (setting_key, default_mode, real_calls, now),
                )
        loaded = self.get(setting_key)
        if loaded is None:
            raise RuntimeError("failed to initialize ai_runtime_settings singleton")
        return loaded

    def update_with_version(
        self,
        *,
        mode: AiRuntimeMode,
        real_calls_enabled: bool,
        kill_switch: bool,
        expected_version: int,
        updated_by_user_id: str,
        updated_by_username: str,
        setting_key: str = AI_RUNTIME_SINGLETON_KEY,
    ) -> AiRuntimeSettingsRecord:
        """乐观锁更新；version 不匹配时抛 AiRuntimeVersionConflictError。"""

        now = datetime.now(timezone.utc)
        with self._factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE ai_runtime_settings
                    SET mode = %s,
                        real_calls_enabled = %s,
                        kill_switch = %s,
                        version = version + 1,
                        updated_by_user_id = %s,
                        updated_by_username = %s,
                        updated_at = %s
                    WHERE setting_key = %s AND version = %s
                    RETURNING setting_key, mode, real_calls_enabled, kill_switch,
                              version, updated_by_user_id, updated_by_username, updated_at
                    """,
                    (
                        mode,
                        real_calls_enabled,
                        kill_switch,
                        updated_by_user_id,
                        updated_by_username,
                        now,
                        setting_key,
                        expected_version,
                    ),
                )
                row = cursor.fetchone()
        if row is None:
            current = self.get(setting_key)
            raise AiRuntimeVersionConflictError(
                current=current, expected_version=expected_version
            )
        return self._to_record(row)

    @staticmethod
    def _to_record(row: tuple) -> AiRuntimeSettingsRecord:
        return AiRuntimeSettingsRecord(
            setting_key=row[0],
            mode=row[1],  # type: ignore[arg-type]
            real_calls_enabled=bool(row[2]),
            kill_switch=bool(row[3]),
            version=int(row[4]),
            updated_by_user_id=row[5],
            updated_by_username=row[6],
            updated_at=row[7],
        )


__all__ = [
    "AiRuntimeVersionConflictError",
    "PostgresAiRuntimeSettingsRepository",
]
