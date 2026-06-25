from __future__ import annotations

"""Local data warehouse adapter.

教学要点：
- 用 SQLite in-memory 模拟企业 DWH，方便离线运行和测试。
- Repository/adapter 负责数据加载和查询，不负责 Agent planning。
- 生产系统可把这里替换为 PostgreSQL/MySQL/BigQuery/Snowflake 只读连接。
"""

import csv
import sqlite3
from pathlib import Path

from ..settings import DATA_DIR
from .sql_guard import assert_select_only
from .templates import QUERY_TEMPLATES


class RetailDataWarehouse:
    """SQLite-backed local warehouse with explicit read-only query templates.

    教学版把 CSV 装进内存 SQLite，让 SQL 聚合结果可重复、可测试。
    生产版可以把这个类替换成只读 DWH adapter，而上层 workflow 不需要改。
    """

    def __init__(self, data_dir: Path = DATA_DIR) -> None:
        self.data_dir = data_dir
        # 使用 :memory: 保证示例离线运行；每个实例启动时都从 CSV 重建小型仓库。
        self.connection = sqlite3.connect(":memory:")
        self.connection.row_factory = sqlite3.Row
        self._load()

    def _load(self) -> None:
        """Create demo tables and load CSV fixtures."""
        cur = self.connection.cursor()
        # sales 表模拟销售事实表：日期、区域、门店、品类、销售额、粗利、客数。
        cur.execute(
            """
            CREATE TABLE sales (
                date TEXT,
                region TEXT,
                store TEXT,
                category TEXT,
                product TEXT,
                sales_yen INTEGER,
                gross_profit_yen INTEGER,
                units INTEGER,
                customers INTEGER
            )
            """
        )
        # inventory 表模拟库存事实表：库存、日销、补货点、供应商提前期。
        cur.execute(
            """
            CREATE TABLE inventory (
                date TEXT,
                region TEXT,
                store TEXT,
                category TEXT,
                product TEXT,
                stock_units INTEGER,
                daily_sales_units INTEGER,
                reorder_point INTEGER,
                supplier_lead_days INTEGER
            )
            """
        )
        self._insert_csv("sales", self.data_dir / "sales.csv")
        self._insert_csv("inventory", self.data_dir / "inventory.csv")
        self.connection.commit()

    def _insert_csv(self, table: str, path: Path) -> None:
        """Load a CSV file into the given SQLite table."""
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
        if not rows:
            return
        columns = list(rows[0].keys())
        placeholders = ",".join("?" for _ in columns)
        # 表名来自内部调用，不来自用户输入；列名来自项目内 CSV 表头。
        sql = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})"
        values = [[row[column] for column in columns] for row in rows]
        self.connection.executemany(sql, values)

    def query_template(self, name: str) -> tuple[str, list[sqlite3.Row]]:
        """Execute one whitelisted SQL template.

        关键边界：调用方只能传 template name，不能传任意 SQL。
        """

        if name not in QUERY_TEMPLATES:
            raise ValueError(f"unknown query template: {name}")
        sql = " ".join(QUERY_TEMPLATES[name].sql.split())
        assert_select_only(sql)
        return sql, list(self.connection.execute(sql))
