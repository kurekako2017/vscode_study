"""LangGraph 共享状态合同。

文件职责：定义所有 Node 可以读取、以及通过增量 Patch 更新的字段。
谁调用它：Workflow Graph、Node、Service 和 Answer Generator。
输入：question_id、问题、request_id 与可选审批决定；输出：贯穿图执行的 TypedDict。
为什么需要这一层：显式 State 能让 Node 合同、条件路由和恢复输入可检查。
初学者重点：Node 不必返回完整 State，只返回自己新增或修改的字段。
日本现场面试：可说明 SQLite 保存长期事实，WorkflowState 是单次图执行的工作状态。
企业级替换：增加版本化状态、checkpoint 标识和迁移策略，避免无界保存敏感 Context。
"""

from __future__ import annotations

from typing import Literal, NotRequired, TypedDict


class WorkflowState(TypedDict):
    """LangGraph 节点共享状态；必填字段建立执行身份，可选字段由 Node 逐步产生。"""

    question_id: str
    question: str
    request_id: str
    approval_decision: NotRequired[Literal["approved", "rejected"] | None]
    risk_level: NotRequired[Literal["LOW", "HIGH"]]
    status: NotRequired[str]
    report: NotRequired[str]
