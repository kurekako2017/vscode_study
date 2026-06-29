"""根据 Mock 股票数据生成中性的研究辅助文字。"""

from __future__ import annotations

from typing import Any


INDUSTRY_CONTEXT = {
    "汽车制造": "可继续关注全球汽车需求、汇率、原材料成本与新能源转型进度。",
    "银行与金融服务": "可继续关注利率环境、信贷成本、资本充足率与宏观经济变化。",
    "通信服务": "可继续关注用户增长、资费竞争、基础设施投入与监管政策变化。",
}


def analyze_stock(stock_data: dict[str, Any]) -> dict[str, Any]:
    """生成 AI 风格的规则化总结和风险提示。

    这里没有调用真实 AI 模型。输出只用于演示报告结构，不给出投资指令。
    """

    company_name = stock_data["company_name"]
    industry = stock_data["industry"]
    per = stock_data["per"]
    pbr = stock_data["pbr"]
    dividend_yield = stock_data["dividend_yield"]

    summary = (
        f"{company_name}属于{industry}行业。本报告中的价格与估值指标均为 Mock 数据。"
        f"模拟 PER 为 {per:.2f}，模拟 PBR 为 {pbr:.2f}，模拟股息率为 "
        f"{dividend_yield:.2f}%。这些指标只能用于学习如何组织研究信息，"
        "不能单独用于判断公司价值或作出投资决定。"
    )

    industry_risk = INDUSTRY_CONTEXT.get(
        industry, "可继续关注行业周期、竞争格局、监管政策与公司经营变化。"
    )
    risks = [
        "本报告全部行情与估值数据均为模拟值，可能与真实市场数据完全不同。",
        industry_risk,
        "PER、PBR 和股息率只是历史或静态指标，不能代表未来收益。",
        "投资还可能受到市场波动、汇率、政策、流动性及公司经营风险影响。",
    ]

    return {
        "ai_summary": summary,
        "risk_notes": risks,
    }
