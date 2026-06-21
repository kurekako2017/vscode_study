"""业务 Agent 共用的审批、审计与结果模型。"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable


@dataclass
class Result:
    """所有业务 Agent 共用的返回格式，便于 UI、日志和测试统一处理。"""

    # status/summary 是最小结果；data 保存各 Agent 自己的业务字段。
    status: str
    summary: str
    data: dict[str, Any] = field(default_factory=dict)
    requires_approval: bool = False
    audit: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """把 dataclass 及其嵌套字段递归转换为可 JSON 序列化的字典。"""
        return asdict(self)


def run_guarded(agent: str, action: str, operation: Callable[[], Result]) -> Result:
    """执行一个业务动作，把可预期异常转换成拒绝结果，并追加审计记录。"""
    # 使用 UTC 时间可避免不同部署时区导致审计记录无法排序。
    started = datetime.now(timezone.utc).isoformat()
    try:
        result = operation()
    except (ValueError, PermissionError) as exc:
        # 只转换已知业务错误；编程错误仍应抛出，方便开发者及时发现。
        result = Result("rejected", str(exc))
    result.audit.append({"time": started, "agent": agent, "action": action, "status": result.status})
    return result
