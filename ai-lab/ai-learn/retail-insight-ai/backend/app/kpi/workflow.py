"""确定性 KPI Workflow。

文件职责：
- 被 `AnalysisWorkflow` 的 kpi 节点调用。
- 从本地 CSV 读取业务数据并计算 KPI。
- 当前仍是本地文件实现，未来可替换为 PostgreSQL Repository。

输入：
- 用户问题字符串（当前只保留接口兼容，不再参与 KPI 数值计算）
- `LocalBusinessDataLoader`

输出：
- `KPIResult`

为什么需要这一层：
- KPI 必须保持确定性和可审计，不能把公式交给非确定性模型。

日本现场面试怎么讲：
- 当前是 File-based KPI Engine。
- 后续企业化会升级为 Import + Repository + Approval 可追踪的数据来源。
"""

from app.data_loaders import LocalBusinessDataLoader
from app.models.analysis import KPIResult


class FixedKPIWorkflow:
    """使用固定规则计算教学版 KPI，刻意与非确定性模型调用分离。"""

    def __init__(self, data_loader: LocalBusinessDataLoader) -> None:
        """注入本地业务数据加载器，避免 Workflow 自己处理文件路径。"""

        self._data_loader = data_loader

    def run(self, question: str) -> KPIResult:
        """从本地 CSV 聚合出 KPI；保留 question 参数以兼容现有 Workflow 接口。"""

        business_data = self._data_loader.load_kpi_data()
        return KPIResult(
            sales_amount_jpy=business_data.revenue_jpy,
            gross_margin_rate=business_data.gross_margin_rate,
            inventory_turnover=business_data.inventory_turnover,
            active_members=business_data.active_members,
            promotion_lift_rate=business_data.promotion_lift_rate,
            data_version=business_data.data_version,
            rule_version="kpi-file-v1",
        )
