from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class KPIResult:
    """保存一次确定性 KPI 计算结果及其数据、规则版本。"""

    sales_amount_jpy: int
    gross_margin_rate: float
    inventory_turnover: float
    active_members: int
    promotion_lift_rate: float
    data_version: str = "local-static-2026-06"
    rule_version: str = "kpi-v1"


@dataclass(frozen=True)
class ResearchResult:
    """保存调查摘要、来源与 Provider 名称，便于报告说明证据边界。"""

    summary: str
    sources: list[str] = field(default_factory=list)
    provider: str = "static"
