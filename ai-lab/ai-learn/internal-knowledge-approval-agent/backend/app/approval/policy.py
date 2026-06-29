"""问题风险的确定性分类策略。

文件职责：依据高风险关键词把问题分类为 LOW 或 HIGH。
谁调用它：Workflow RiskClassifier Node；它不调用数据库或外部模型。
输入：员工问题文本；输出：``LOW``/``HIGH``。
为什么需要这一层：关键审批门槛必须显式、可测试，不能隐藏在回答生成器中。
初学者重点：``casefold`` 负责大小写无关匹配；命中任意关键词即进入人工审批。
日本现场面试：可说明当前规则可解释且确定，分类异常应按高风险处理。
企业级替换：策略表/Policy Engine/受评估分类器，并加入版本、理由和领域权限。
"""

from typing import Literal


HIGH_RISK_KEYWORDS = {
    "契約",
    "個人情報",
    "セキュリティ",
    "経費",
    "法務",
    "障害対応",
    "退職",
    "給与",
    # Minimal multilingual aliases retained from the existing implementation.
    "合同",
    "个人信息",
    "安全",
    "报销",
    "法律",
    "障害",
    "故障",
    "incident",
    "security",
}


def classify_risk(question: str) -> Literal["LOW", "HIGH"]:
    normalized = question.casefold()
    return "HIGH" if any(word.casefold() in normalized for word in HIGH_RISK_KEYWORDS) else "LOW"
