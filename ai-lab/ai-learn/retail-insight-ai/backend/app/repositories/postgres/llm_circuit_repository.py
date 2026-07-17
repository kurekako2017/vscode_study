"""PostgreSQL 共享 Circuit Breaker 状态。

文件职责：多进程共享 closed/open/half_open 状态，不引入 Redis。
谁调用它：CircuitBreaker（经 CircuitBreakerStore 协议）。
设计理由：最小状态表，不做大型监控平台。
"""

from __future__ import annotations

from datetime import datetime, timezone

from app.db.connection import PostgresConnectionFactory
from app.llm.circuit_breaker import CircuitState


class PostgresCircuitBreakerStore:
    """llm_provider_circuit_state 表的读写；行级更新保证跨进程可见。"""

    def __init__(self, connection_factory: PostgresConnectionFactory) -> None:
        self._factory = connection_factory

    def get(self, provider_name: str) -> CircuitState:
        with self._factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT provider_name,state,failure_count,opened_at,half_open_probes,updated_at
                    FROM llm_provider_circuit_state WHERE provider_name=%s""",
                    (provider_name,),
                )
                row = cursor.fetchone()
        if row is None:
            now = datetime.now(timezone.utc)
            return CircuitState(provider_name, "closed", 0, None, 0, now)
        return CircuitState(
            provider_name=row[0],
            state=row[1],
            failure_count=int(row[2]),
            opened_at=row[3],
            half_open_probes=int(row[4]),
            updated_at=row[5],
        )

    def save(self, state: CircuitState) -> None:
        with self._factory.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO llm_provider_circuit_state (
                    provider_name,state,failure_count,opened_at,half_open_probes,updated_at)
                    VALUES (%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (provider_name) DO UPDATE SET
                    state=EXCLUDED.state,
                    failure_count=EXCLUDED.failure_count,
                    opened_at=EXCLUDED.opened_at,
                    half_open_probes=EXCLUDED.half_open_probes,
                    updated_at=EXCLUDED.updated_at""",
                    (
                        state.provider_name,
                        state.state,
                        state.failure_count,
                        state.opened_at,
                        state.half_open_probes,
                        state.updated_at,
                    ),
                )


__all__ = ["PostgresCircuitBreakerStore"]
