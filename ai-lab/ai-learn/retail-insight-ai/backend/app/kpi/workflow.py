from app.models.analysis import KPIResult


class FixedKPIWorkflow:
    """使用固定规则计算教学版 KPI，刻意与非确定性模型调用分离。"""

    def run(self, question: str) -> KPIResult:
        """根据安全的长度因子生成可重复 KPI，不解释或记录问题正文。"""

        # 长度因子只为演示“输入会影响结果”；上限防止超长输入无限放大销售额。
        question_factor = min(len(question.strip()), 100)
        return KPIResult(
            sales_amount_jpy=12_500_000 + question_factor * 1_000,
            gross_margin_rate=0.318,
            inventory_turnover=4.7,
            active_members=1_840,
            promotion_lift_rate=0.126,
        )
