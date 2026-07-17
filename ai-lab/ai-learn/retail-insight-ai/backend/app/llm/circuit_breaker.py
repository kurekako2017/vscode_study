"""Provider Circuit Breaker：closed / open / half_open。

文件职责：在 Provider 连续失败时打开熔断，保护后续请求并允许有限 probe。
谁调用它：ProviderChain。
它调用谁：Postgres 共享状态表或内存 store（测试可控时钟）。
设计理由：多进程部署不能只依赖单进程内存；默认测试不 sleep。
日本现场面试：熔断是可用性保护，open 时跳过不得记成收费 attempt。
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol
from uuid import uuid4


CircuitStateName = str  # closed | open | half_open


@dataclass(frozen=True)
class CircuitState:
    provider_name: str
    state: CircuitStateName
    failure_count: int
    opened_at: datetime | None
    half_open_probes: int
    updated_at: datetime


@dataclass(frozen=True)
class CircuitBreakerConfig:
    failure_threshold: int = 3
    open_duration_seconds: float = 30.0
    half_open_probe_limit: int = 1


class Clock(Protocol):
    def now(self) -> datetime: ...


class SystemClock:
    def now(self) -> datetime:
        return datetime.now(timezone.utc)


class ControllableClock:
    """测试用可控时钟；禁止真实 sleep。"""

    def __init__(self, start: datetime | None = None) -> None:
        self._now = start or datetime(2026, 7, 17, tzinfo=timezone.utc)

    def now(self) -> datetime:
        return self._now

    def advance(self, seconds: float) -> None:
        from datetime import timedelta

        self._now = self._now + timedelta(seconds=seconds)


class CircuitBreakerStore(Protocol):
    def get(self, provider_name: str) -> CircuitState: ...

    def save(self, state: CircuitState) -> None: ...


class InMemoryCircuitBreakerStore:
    """单测与 stub 默认 store；生产 fallback_chain 应使用 PostgreSQL store。"""

    def __init__(self) -> None:
        self._states: dict[str, CircuitState] = {}

    def get(self, provider_name: str) -> CircuitState:
        existing = self._states.get(provider_name)
        if existing is not None:
            return existing
        now = datetime.now(timezone.utc)
        return CircuitState(provider_name, "closed", 0, None, 0, now)

    def save(self, state: CircuitState) -> None:
        self._states[state.provider_name] = state


class CircuitBreaker:
    """按 Provider 隔离的熔断器；open 跳过不算收费 attempt。"""

    def __init__(
        self,
        *,
        store: CircuitBreakerStore,
        config: CircuitBreakerConfig | None = None,
        clock: Clock | None = None,
        on_state_change: callable | None = None,
    ) -> None:
        self._store = store
        self._config = config or CircuitBreakerConfig()
        self._clock = clock or SystemClock()
        self._on_state_change = on_state_change

    def allow_request(self, provider_name: str) -> tuple[bool, str]:
        """返回 (allowed, reason)。open 跳过；half_open 限流 probe。"""

        state = self._refresh(provider_name)
        if state.state == "closed":
            return True, "closed"
        if state.state == "open":
            return False, "circuit_open"
        # half_open
        if state.half_open_probes >= self._config.half_open_probe_limit:
            return False, "circuit_half_open_limit"
        return True, "half_open_probe"

    def mark_probe_started(self, provider_name: str) -> None:
        state = self._refresh(provider_name)
        if state.state != "half_open":
            return
        now = self._clock.now()
        self._store.save(
            CircuitState(
                provider_name=provider_name,
                state="half_open",
                failure_count=state.failure_count,
                opened_at=state.opened_at,
                half_open_probes=state.half_open_probes + 1,
                updated_at=now,
            )
        )

    def record_success(self, provider_name: str) -> CircuitState:
        now = self._clock.now()
        previous = self._store.get(provider_name)
        new_state = CircuitState(provider_name, "closed", 0, None, 0, now)
        self._store.save(new_state)
        if previous.state != "closed":
            self._emit(provider_name, previous.state, "closed")
        return new_state

    def record_failure(self, provider_name: str) -> CircuitState:
        now = self._clock.now()
        previous = self._refresh(provider_name)
        if previous.state == "half_open":
            new_state = CircuitState(
                provider_name=provider_name,
                state="open",
                failure_count=previous.failure_count + 1,
                opened_at=now,
                half_open_probes=0,
                updated_at=now,
            )
            self._store.save(new_state)
            self._emit(provider_name, previous.state, "open")
            return new_state

        failure_count = previous.failure_count + 1
        if failure_count >= self._config.failure_threshold:
            new_state = CircuitState(
                provider_name=provider_name,
                state="open",
                failure_count=failure_count,
                opened_at=now,
                half_open_probes=0,
                updated_at=now,
            )
            self._store.save(new_state)
            if previous.state != "open":
                self._emit(provider_name, previous.state, "open")
            return new_state

        new_state = CircuitState(
            provider_name=provider_name,
            state="closed",
            failure_count=failure_count,
            opened_at=None,
            half_open_probes=0,
            updated_at=now,
        )
        self._store.save(new_state)
        return new_state

    def _refresh(self, provider_name: str) -> CircuitState:
        state = self._store.get(provider_name)
        if state.state != "open" or state.opened_at is None:
            return state
        elapsed = (self._clock.now() - state.opened_at).total_seconds()
        if elapsed < self._config.open_duration_seconds:
            return state
        now = self._clock.now()
        half = CircuitState(
            provider_name=provider_name,
            state="half_open",
            failure_count=state.failure_count,
            opened_at=state.opened_at,
            half_open_probes=0,
            updated_at=now,
        )
        self._store.save(half)
        self._emit(provider_name, "open", "half_open")
        return half

    def _emit(self, provider_name: str, from_state: str, to_state: str) -> None:
        if self._on_state_change is None:
            return
        event = {
            "closed": "llm_provider.circuit_closed",
            "open": "llm_provider.circuit_opened",
            "half_open": "llm_provider.circuit_half_open",
        }.get(to_state, "llm_provider.circuit_changed")
        self._on_state_change(
            event=event,
            provider_name=provider_name,
            from_state=from_state,
            to_state=to_state,
            correlation_id=f"cb-{uuid4().hex[:12]}",
        )


__all__ = [
    "CircuitBreaker",
    "CircuitBreakerConfig",
    "CircuitBreakerStore",
    "CircuitState",
    "ControllableClock",
    "InMemoryCircuitBreakerStore",
    "SystemClock",
]
