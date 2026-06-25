from __future__ import annotations

"""Teaching metrics collector.

教学要点：
- 这是最小内存 metrics，便于 `/api/metrics` 展示运行情况。
- 生产系统应替换为 Prometheus/OpenTelemetry。
"""

from dataclasses import dataclass, field


@dataclass
class InMemoryMetrics:
    tasks_created: int = 0
    tasks_completed: int = 0
    tasks_failed: int = 0
    events_published: int = 0
    event_counts: dict[str, int] = field(default_factory=dict)

    def count_task_created(self) -> None:
        self.tasks_created += 1

    def count_task_completed(self) -> None:
        self.tasks_completed += 1

    def count_task_failed(self) -> None:
        self.tasks_failed += 1

    def count_event(self, event_type: str) -> None:
        self.events_published += 1
        self.event_counts[event_type] = self.event_counts.get(event_type, 0) + 1

    def snapshot(self) -> dict:
        """Return a serializable metrics snapshot."""
        return {
            "tasks_created": self.tasks_created,
            "tasks_completed": self.tasks_completed,
            "tasks_failed": self.tasks_failed,
            "events_published": self.events_published,
            "event_counts": dict(self.event_counts),
        }
