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
    """SQLite-backed local warehouse with explicit read-only query templates."""

    def __init__(self, data_dir: Path = DATA_DIR) -> None:
        self.data_dir = data_dir
        self.connection = sqlite3.connect(":memory:")
        self.connection.row_factory = sqlite3.Row
        self._load()

    def _load(self) -> None:
        """Create demo tables and load CSV fixtures."""
        cur = self.connection.cursor()
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
