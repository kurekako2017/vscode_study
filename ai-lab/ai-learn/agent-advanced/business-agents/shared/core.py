"""业务 Agent 共用的审批、审计与结果模型。"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable


@dataclass
class Result:
    status: str
    summary: str
    data: dict[str, Any] = field(default_factory=dict)
    requires_approval: bool = False
    audit: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def run_guarded(agent: str, action: str, operation: Callable[[], Result]) -> Result:
    started = datetime.now(timezone.utc).isoformat()
    try:
        result = operation()
    except (ValueError, PermissionError) as exc:
        result = Result("rejected", str(exc))
    result.audit.append({"time": started, "agent": agent, "action": action, "status": result.status})
    return result
