"""本地文件输入实现。

文件职责：
- 读取 `backend/data/business/` 下的 CSV。
- 读取 `backend/data/research/` 下的 JSON。
- 为 KPI Workflow 和 StaticResearchProvider 输出稳定的数据对象。

谁调用它：
- `backend/app/config/container.py` 在组合根创建实例。
- `backend/app/kpi/workflow.py` 调用业务数据加载器。
- `backend/app/agents/providers/static_research.py` 调用 Research 数据加载器。

它调用谁：
- Python 标准库 `csv` / `json` / `pathlib`。

输入：
- 本地 CSV / JSON 文件。

输出：
- `BusinessKPIData`
- `ResearchDataset`

为什么需要这一层：
- 让 Workflow 和 Provider 只关心“拿到什么数据”，不关心“从哪里拿数据”。
- 当前是文件输入，未来 Phase 2 可以替换成 PostgreSQL Repository。

日本现场面试怎么讲：
- 当前实现是 Local File Provider。
- 企业级替换方向是 Import Pipeline + Repository + Search Layer。
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

from app.errors.exceptions import LocalDataFileException


def default_backend_data_dir() -> Path:
    """返回 backend/data 根目录。"""

    return Path(__file__).resolve().parents[2] / "data"


@dataclass(frozen=True)
class BusinessKPIData:
    """保存从本地 CSV 聚合后的 KPI 中间结果。"""

    revenue_jpy: int
    gross_margin_rate: float
    inventory_turnover: float
    active_members: int
    promotion_lift_rate: float
    data_version: str


@dataclass(frozen=True)
class ResearchDataset:
    """保存从本地 JSON 读取的 Research 结果。"""

    summary: str
    sources: list[str]
    data_version: str


class LocalBusinessDataLoader:
    """读取本地业务 CSV，并输出可直接进入 KPIResult 的聚合值。"""

    def __init__(self, business_dir: Path | None = None) -> None:
        """允许测试注入临时目录；默认读取 backend/data/business。"""

        self._business_dir = business_dir or default_backend_data_dir() / "business"

    def load_kpi_data(self) -> BusinessKPIData:
        """从四类 CSV 读取业务事实，并计算 Phase 1 需要的 KPI。"""

        sales_rows = self._read_csv("sales.csv")
        inventory_rows = self._read_csv("inventory.csv")
        member_rows = self._read_csv("members.csv")
        promotion_rows = self._read_csv("promotions.csv")

        revenue_jpy = sum(self._to_int(row, "revenue_jpy", "sales.csv") for row in sales_rows)
        gross_profit_jpy = sum(
            self._to_int(row, "gross_profit_jpy", "sales.csv") for row in sales_rows
        )
        gross_margin_rate = (
            gross_profit_jpy / revenue_jpy if revenue_jpy > 0 else 0.0
        )

        cost_of_goods_sold_jpy = sum(
            self._to_int(row, "cost_of_goods_sold_jpy", "inventory.csv")
            for row in inventory_rows
        )
        average_inventory_jpy = sum(
            self._to_int(row, "average_inventory_jpy", "inventory.csv")
            for row in inventory_rows
        )
        inventory_turnover = (
            cost_of_goods_sold_jpy / average_inventory_jpy
            if average_inventory_jpy > 0
            else 0.0
        )

        active_members = sum(
            1 for row in member_rows if self._to_bool(row, "is_active", "members.csv")
        )

        promoted_revenue_jpy = sum(
            self._to_int(row, "promoted_revenue_jpy", "promotions.csv")
            for row in promotion_rows
        )
        baseline_revenue_jpy = sum(
            self._to_int(row, "baseline_revenue_jpy", "promotions.csv")
            for row in promotion_rows
        )
        promotion_lift_rate = (
            (promoted_revenue_jpy - baseline_revenue_jpy) / baseline_revenue_jpy
            if baseline_revenue_jpy > 0
            else 0.0
        )

        return BusinessKPIData(
            revenue_jpy=revenue_jpy,
            gross_margin_rate=gross_margin_rate,
            inventory_turnover=inventory_turnover,
            active_members=active_members,
            promotion_lift_rate=promotion_lift_rate,
            data_version=self._build_data_version(
                "sales.csv",
                "inventory.csv",
                "members.csv",
                "promotions.csv",
            ),
        )

    def _read_csv(self, filename: str) -> list[dict[str, str]]:
        """读取单个 CSV，并把缺失或空内容转成稳定异常。"""

        path = self._business_dir / filename
        if not path.exists():
            raise LocalDataFileException(path=path, data_kind="business", reason="missing file")

        with path.open("r", encoding="utf-8", newline="") as handle:
            try:
                reader = csv.DictReader(handle)
                rows = list(reader)
            except csv.Error as exc:
                raise LocalDataFileException(
                    path=path,
                    data_kind="business",
                    reason=f"csv parse error: {type(exc).__name__}",
                ) from exc

        if not rows:
            raise LocalDataFileException(path=path, data_kind="business", reason="empty file")
        return rows

    def _to_int(self, row: dict[str, str], field_name: str, filename: str) -> int:
        """把 CSV 字符串字段转换为 int，并在错误时保留文件上下文。"""

        raw_value = row.get(field_name)
        if raw_value is None:
            raise LocalDataFileException(
                path=self._business_dir / filename,
                data_kind="business",
                reason=f"missing column: {field_name}",
            )
        try:
            return int(raw_value)
        except ValueError as exc:
            raise LocalDataFileException(
                path=self._business_dir / filename,
                data_kind="business",
                reason=f"invalid integer in column: {field_name}",
            ) from exc

    def _to_bool(self, row: dict[str, str], field_name: str, filename: str) -> bool:
        """把布尔字段标准化为 Python bool。"""

        raw_value = row.get(field_name)
        if raw_value is None:
            raise LocalDataFileException(
                path=self._business_dir / filename,
                data_kind="business",
                reason=f"missing column: {field_name}",
            )
        normalized = raw_value.strip().lower()
        if normalized in {"1", "true", "yes", "y"}:
            return True
        if normalized in {"0", "false", "no", "n"}:
            return False
        raise LocalDataFileException(
            path=self._business_dir / filename,
            data_kind="business",
            reason=f"invalid boolean in column: {field_name}",
        )

    def _build_data_version(self, *filenames: str) -> str:
        """根据文件名生成稳定数据版本标签。"""

        stems = [Path(name).stem for name in filenames]
        return f"local-files:{'|'.join(stems)}"


class LocalResearchDataLoader:
    """读取本地 JSON Research 数据，并组合成统一结果。"""

    def __init__(self, research_dir: Path | None = None) -> None:
        """允许测试注入临时目录；默认读取 backend/data/research。"""

        self._research_dir = research_dir or default_backend_data_dir() / "research"

    def load_research_dataset(self) -> ResearchDataset:
        """读取 research 目录全部 JSON，并合并摘要与来源。"""

        paths = sorted(self._research_dir.glob("*.json"))
        if not paths:
            raise LocalDataFileException(
                path=self._research_dir,
                data_kind="research",
                reason="no json files found",
            )

        summary_parts: list[str] = []
        sources: list[str] = []
        data_versions: list[str] = []
        for path in paths:
            payload = self._read_json(path)
            summary = payload.get("summary")
            if not isinstance(summary, str) or not summary.strip():
                raise LocalDataFileException(
                    path=path,
                    data_kind="research",
                    reason="summary must be a non-empty string",
                )
            raw_sources = payload.get("sources")
            if not isinstance(raw_sources, list) or not all(
                isinstance(item, str) and item.strip() for item in raw_sources
            ):
                raise LocalDataFileException(
                    path=path,
                    data_kind="research",
                    reason="sources must be a non-empty string list",
                )
            title = payload.get("title", path.stem)
            summary_parts.append(f"### {title}\n{summary.strip()}")
            sources.extend(raw_sources)
            data_versions.append(path.stem)

        return ResearchDataset(
            summary="\n\n".join(summary_parts),
            sources=sources,
            data_version=f"local-files:{'|'.join(data_versions)}",
        )

    def _read_json(self, path: Path) -> dict[str, object]:
        """读取单个 JSON，并在格式错误时返回统一异常。"""

        if not path.exists():
            raise LocalDataFileException(path=path, data_kind="research", reason="missing file")
        try:
            with path.open("r", encoding="utf-8") as handle:
                payload = json.load(handle)
        except json.JSONDecodeError as exc:
            raise LocalDataFileException(
                path=path,
                data_kind="research",
                reason=f"json parse error: {type(exc).__name__}",
            ) from exc
        if not isinstance(payload, dict):
            raise LocalDataFileException(
                path=path,
                data_kind="research",
                reason="json root must be an object",
            )
        return payload
