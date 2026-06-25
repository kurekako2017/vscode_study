from __future__ import annotations

"""Whitelisted KPI query templates.

教学要点：
- 每个 QueryTemplate 对应一个经营指标/图表。
- 这相当于企业 BI semantic layer 的最小版本。
- 用户问题只会路由到这些模板，避免模型自由拼 SQL。
"""

from ..models import QueryTemplate


QUERY_TEMPLATES: dict[str, QueryTemplate] = {
    "monthly_sales": QueryTemplate(
        name="monthly_sales",
        title="月次売上・粗利率",
        chart_kind="fixed_line",
        source_file="sales.csv",
        sql="""
            SELECT date,
                   SUM(sales_yen) AS sales_yen,
                   SUM(gross_profit_yen) AS gross_profit_yen,
                   ROUND(SUM(gross_profit_yen) * 100.0 / SUM(sales_yen), 1) AS gross_margin_pct
            FROM sales
            GROUP BY date
            ORDER BY date
        """,
    ),
    "region_sales": QueryTemplate(
        name="region_sales",
        title="地域別売上",
        chart_kind="fixed_bar",
        source_file="sales.csv",
        sql="""
            SELECT region,
                   SUM(sales_yen) AS sales_yen,
                   SUM(gross_profit_yen) AS gross_profit_yen,
                   SUM(customers) AS customers,
                   ROUND(SUM(sales_yen) * 1.0 / SUM(customers), 0) AS sales_per_customer_yen
            FROM sales
            GROUP BY region
            ORDER BY sales_yen DESC
        """,
    ),
    "inventory_risk": QueryTemplate(
        name="inventory_risk",
        title="在庫・欠品リスク",
        chart_kind="fixed_table",
        source_file="inventory.csv",
        sql="""
            SELECT region,
                   store,
                   category,
                   product,
                   stock_units,
                   daily_sales_units,
                   reorder_point,
                   ROUND(stock_units * 1.0 / daily_sales_units, 1) AS stock_days,
                   CASE
                       WHEN stock_units < reorder_point THEN '要補充'
                       WHEN stock_units < daily_sales_units * supplier_lead_days THEN 'リードタイム注意'
                       ELSE '通常'
                   END AS risk_level
            FROM inventory
            ORDER BY
                CASE risk_level WHEN '要補充' THEN 1 WHEN 'リードタイム注意' THEN 2 ELSE 3 END,
                stock_days ASC
        """,
    ),
    "category_sales": QueryTemplate(
        name="category_sales",
        title="カテゴリ別売上",
        chart_kind="fixed_bar",
        source_file="sales.csv",
        sql="""
            SELECT category,
                   SUM(sales_yen) AS sales_yen,
                   SUM(units) AS units,
                   ROUND(SUM(gross_profit_yen) * 100.0 / SUM(sales_yen), 1) AS gross_margin_pct
            FROM sales
            GROUP BY category
            ORDER BY sales_yen DESC
        """,
    ),
}
