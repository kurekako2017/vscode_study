"""提供日本股票的本地 Mock 数据。

第一版不访问网络、不读取 .env，也不连接任何证券账户。
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any


# 所有数字均为教学用模拟值，不代表真实或实时市场数据。
MOCK_STOCKS: dict[str, dict[str, Any]] = {
    "7203": {
        "stock_code": "7203",
        "company_name": "丰田汽车（Mock）",
        "industry": "汽车制造",
        "current_price": 2715.50,
        "per": 10.80,
        "pbr": 1.15,
        "dividend_yield": 3.10,
    },
    "8306": {
        "stock_code": "8306",
        "company_name": "三菱日联金融集团（Mock）",
        "industry": "银行与金融服务",
        "current_price": 1850.00,
        "per": 12.50,
        "pbr": 1.05,
        "dividend_yield": 3.40,
    },
    "9432": {
        "stock_code": "9432",
        "company_name": "日本电信电话（Mock）",
        "industry": "通信服务",
        "current_price": 154.30,
        "per": 11.80,
        "pbr": 1.35,
        "dividend_yield": 3.38,
    },
}


def normalize_stock_code(stock_code: str) -> str:
    """清理并校验四位日本股票代码。"""

    normalized = stock_code.strip()
    if len(normalized) != 4 or not normalized.isdigit():
        raise ValueError("股票代码必须是四位数字，例如 7203。")
    return normalized


def fetch_stock_data(stock_code: str) -> dict[str, Any]:
    """返回指定股票的 Mock 数据，不发起任何外部请求。"""

    normalized = normalize_stock_code(stock_code)
    if normalized not in MOCK_STOCKS:
        supported = "、".join(sorted(MOCK_STOCKS))
        raise ValueError(f"第一版仅支持 Mock 股票代码：{supported}。")

    # 返回副本，避免分析过程意外修改原始 Mock 数据表。
    return deepcopy(MOCK_STOCKS[normalized])
