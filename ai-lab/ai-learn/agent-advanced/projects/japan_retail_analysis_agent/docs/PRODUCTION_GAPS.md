# Production Gaps

本项目已经是“电商问数 + 深度研搜”的前后台分离缩小版工程，但仍不是可直接上线的生产系统。下面按日本现场常见审查点标记未完成部分。

## 状态标记

| 标记 | 含义 |
| --- | --- |
| `DONE` | 已有可运行实现 |
| `PARTIAL` | 有教学/骨架实现，但不满足生产要求 |
| `TODO` | 尚未实现 |

## 未完成清单

| 领域 | 状态 | 当前实现 | 生产要求 | 建议落点 |
| --- | --- | --- | --- | --- |
| 认证 Authentication | `TODO` | 无登录，无用户身份 | OIDC/SAML/SSO、JWT/session、用户上下文 | `interfaces/http/middleware/`, `core/security.py` |
| 授权 Authorization | `TODO` | 无角色权限 | RBAC/ABAC、租户隔离、工具级权限 | `application/policies/`, `infrastructure/repositories/` |
| 多租户 Tenant Isolation | `TODO` | task 无 tenant_id | tenant_id 贯穿 task、checkpoint、data access | `models.py`, `TaskRepository`, API schema |
| SQL AST 安全 | `PARTIAL` | SELECT-only 字符串 guard | SQL parser/AST、表/字段白名单、成本限制 | `data/sql_guard.py` |
| 行列级权限 | `TODO` | 无行级/列级过滤 | 按用户、部门、门店限制数据范围 | `workflows/business.py`, `data/warehouse.py` |
| PII masking | `TODO` | 样本数据无个人信息 | 个人信息字段脱敏、访问审计 | `reporting/composer.py`, `data/` |
| 真实 DWH 接入 | `PARTIAL` | CSV + SQLite in-memory | PostgreSQL/MySQL/DWH 只读账号、连接池、超时 | `data/warehouse.py` |
| 企业搜索接入 | `PARTIAL` | 本地 Markdown 工具 | 企业许可搜索、SharePoint、Confluence、社内 Wiki | `research/tools.py` |
| LLM planning | `PARTIAL` | 规则式 planner | 模型工具调用、预算限制、prompt injection 防御 | `research/agent.py` |
| HITL interrupt/resume | `PARTIAL` | 报告中记录人工确认事项 | LangGraph interrupt/resume、审批 API、审批 UI | `orchestration/orchestrator.py`, `interfaces/http/routers/` |
| Durable queue | `TODO` | `asyncio.create_task` | Celery/RQ/Arq/Cloud Tasks 等持久队列 | `application/task_service.py` |
| Checkpoint 恢复 | `PARTIAL` | LangGraph SqliteSaver 保存 checkpoint | 失败后 resume、任务重启恢复、幂等重放 | `orchestration/orchestrator.py` |
| 审计落库 | `PARTIAL` | task events SQLite | 审计字段标准化、操作者、IP、request id、保留期限 | `checkpoint/store.py` |
| OpenTelemetry | `TODO` | 基础日志 + in-memory metrics | trace/span、metrics、log correlation | `infrastructure/observability/` |
| Prometheus metrics | `TODO` | `/api/metrics` 返回内存计数 | Prometheus format、Grafana dashboard、告警 | `interfaces/http/routers/health.py` |
| 评估集 Evaluation | `TODO` | 仅 unittest/smoke | NL2SQL golden set、报告引用正确率、回归阈值 | `eval/` 或 `tests/evaluation/` |
| Prompt injection 防御 | `TODO` | 无恶意文档测试 | 外部/内部来源隔离、引用验证、工具边界 | `research/tools.py`, `tests/` |
| API 错误标准化 | `PARTIAL` | 有 `core/errors.py` 骨架 | exception handler、错误码、request id | `api/app.py`, `core/errors.py` |
| CI/CD | `TODO` | 无 GitHub Actions | test/build/lint/container scan/deploy pipeline | `.github/workflows/` |
| Migration | `TODO` | SQLite 自动建表 | Alembic 或 migration 管理 | `infrastructure/db/` |
| Load test | `TODO` | 无负载测试 | k6/Locust、并发任务、SSE/WS 压测 | `tests/load/` |
| Secrets 管理 | `TODO` | `.env.example` | AWS Secrets Manager、Vault、KMS、环境分离 | `core/config.py`, deployment |
| Frontend auth/error UX | `TODO` | 无登录，错误处理简单 | 登录态、权限错误、重试、反馈按钮 | `frontend/src/` |

## P0 优先补齐项

1. 认证授权、tenant_id、角色权限。
2. SQL AST parser、表/字段白名单、查询超时和最大返回行数。
3. LangGraph interrupt/resume 审批 API 和前端审批 UI。
4. 企业搜索/社内 Wiki 工具接入与来源可信度标记。
5. 评估集：经营问数 expected SQL/result，研究报告引用正确率。

## 面试时的准确表述

可以说：

> 这个项目已经具备前后台分离、FastAPI、SSE/WebSocket、LangGraph checkpoint、固定问数工作流、研究 Agent 和报告交付，是两个案例的生产风格缩小版。

不应该说：

> 这个项目已经可以直接上线到日本企业生产环境。

更准确的说法是：

> 它是生产框架骨架和作品集项目。若进入真实现场，需要按 `PRODUCTION_GAPS.md` 补齐认证授权、权限隔离、SQL 安全、审计、评估、观测、CI/CD 和外部系统接入。
