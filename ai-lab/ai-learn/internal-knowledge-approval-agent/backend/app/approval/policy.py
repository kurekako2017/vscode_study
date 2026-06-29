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
