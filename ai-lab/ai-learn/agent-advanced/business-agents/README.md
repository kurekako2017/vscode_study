# 业务 Agent 作品集

这些项目是可离线演示的业务纵切片，统一复用 `shared/core.py` 的结构化结果、权限拒绝和审计事件。它们当前定位为“作品集 MVP”，不是生产系统。

| 项目 | 业务闭环 | 当前完成度 |
| --- | --- | --- |
| `japan_ses_sales_agent` | 案件条件 → 人员过滤/评分 → 提案审批 | B 可演示 |
| `interview_agent` | 回答 → STAR rubric 评分 → 追问 | B 可演示 |
| `mcp_office_agent` | 工具 allowlist → 检索/草稿 → 审批 | B 可演示 |
| `enterprise_customer_service_agent` | 租户校验 → 知识回答/引用 → 人工转接 | B 可演示 |
| `coding_github_agent` | diff 检查 → 风险分级 → review 草稿 | B 可演示 |

共同安全约束：不发送邮件、不修改 Office 文件、不 push/merge、不保存个人履历；所有副作用只生成 `proposal`/`draft` 并设置 `requires_approval=true`。

要提升为 A 级作品集，后续统一补 FastAPI/流式 UI、持久化、Docker、自动化测试、真实身份权限与部署说明。
