"""本地文件数据加载模块。

文件职责：
- 为 KPI Workflow 和 StaticResearchProvider 提供统一的本地文件读取入口。
- 当前由组合根 `backend/app/config/container.py` 注入。
- 当前只依赖 Python 标准库，后续可替换为数据库或检索实现。

输入：
- `backend/data/business/*.csv`
- `backend/data/research/*.json`

输出：
- 业务 KPI 聚合结果
- Research 摘要与来源列表

为什么需要这一层：
- 把“文件怎么读”从 KPI / Research 业务逻辑里拆出去，后续接 PostgreSQL、
  Approval Workflow、RAG 时不需要重写核心流程。

日本现场面试怎么讲：
- 这是典型的 Provider / Data Source 抽象预留。当前用本地文件保证可运行，
  未来企业项目可替换成 Repository、Search Provider 或 ETL Import。
"""

from app.data_loaders.local_files import (
    BusinessKPIData,
    LocalBusinessDataLoader,
    LocalResearchDataLoader,
    ResearchDataset,
)

__all__ = [
    "BusinessKPIData",
    "LocalBusinessDataLoader",
    "LocalResearchDataLoader",
    "ResearchDataset",
]
