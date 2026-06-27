# 10_Production_Roadmap

# 目录

- [1. Roadmap 原则](#1-roadmap-原则)
- [2. Level 1 Demo](#2-level-1-demo)
- [3. Level 2 Internal Tool](#3-level-2-internal-tool)
- [4. Level 3 Department System](#4-level-3-department-system)
- [5. Level 4 Enterprise System](#5-level-4-enterprise-system)
- [6. Level 5 SaaS Platform](#6-level-5-saas-platform)
- [7. 等级对照](#7-等级对照)
- [8. 未来两年升级路线图](#8-未来两年升级路线图)
- [9. 投资与决策门禁](#9-投资与决策门禁)

## 1. Roadmap 原则

Retail Insight AI 的升级以业务范围、风险和运维责任为门禁，不以引入组件数量作为完成标准。

- 当前实现能力：FastAPI、TaskService、LangGraph Workflow、Fixed KPI Workflow、Research Agent、SSE、Report Generator、SQLite、Docker。
- 正式运用优先级：身份与权限、审计、持久化、可观测性、备份恢复先于规模扩展。
- KPI 始终保持确定性；Agent 只处理调查型任务。
- 每一级必须满足上一等级的质量门禁，不能跨级跳过数据、权限或恢复能力。
- 成本同时包含基础设施、模型调用、开发、测试、安全、运维和业务确认。

## 2. Level 1 Demo

**目标范围**

验证从任务受理、KPI、Research、报告生成到 SSE 展示的端到端业务链路。

| 项目 | 内容 |
| --- | --- |
| 新增能力 | Task API、TaskService、LangGraph Workflow、Fixed KPI Workflow、Research Agent、SSE、Report Generator |
| 新增组件 | FastAPI、React、SQLite、Docker、本地文件数据 |
| 新增成本 | 开发环境、模型调用、基础测试与文档维护 |
| 新增风险 | 单实例状态、数据结构变化、模型输出不稳定、外部 Tool timeout |
| 新增开发量 | API、Workflow、KPI、Research、Report、Frontend 的纵向切片 |
| 新增运维量 | 启停、环境变量、基础日志、数据初始化 |

**完成门禁**

- 核心链路可重复运行。
- KPI 与 Research 边界明确。
- 正常、超时、输入错误、报告失败路径可确认。
- 不把当前能力描述为正式企业运用能力。

**不在本级范围**

多用户权限、分布式执行、高可用、正式 SLA、多租户和企业检索。

## 3. Level 2 Internal Tool

**目标范围**

向限定内部用户开放，替代部分经营会议前的手工整理工作。

| 项目 | 内容 |
| --- | --- |
| 新增能力 | 内部登录、基础角色、报告历史、数据导入校验、任务重试、基础 Audit Log |
| 新增组件 | PostgreSQL、内部 SSO 接入、集中日志、基础 OpenTelemetry、备份作业 |
| 新增成本 | 托管数据库、日志与 Trace 存储、身份接入、业务验收 |
| 新增风险 | 内部数据越权、错误 KPI 进入会议、报告版本不一致、备份不可恢复 |
| 新增开发量 | Repository 迁移、权限中间件、审计事件、迁移脚本、恢复验证 |
| 新增运维量 | 用户与权限维护、数据库备份、告警确认、月次数据导入确认 |

**完成门禁**

- PostgreSQL 迁移和 restore test 通过。
- 基础 RBAC 在 API、数据与报告层生效。
- task_id 与 trace_id 可完成障害调查。
- KPI 规则和报告模板版本可追踪。

**退出条件**

内部用户、任务量或部门数量超过单实例安全范围，进入 Level 3。

## 4. Level 3 Department System

**目标范围**

服务一个或多个业务部门，支持月次集中任务、稳定检索和部门级权限治理。

| 项目 | 内容 |
| --- | --- |
| 新增能力 | 部门 / 门店数据范围、异步队列、SSE 事件恢复、内部资料 RAG、人工审批 |
| 新增组件 | Redis、RabbitMQ、Worker Pool、OpenSearch、VectorDB、OpenTelemetry Collector |
| 新增成本 | Queue 与 Cache、搜索集群、向量存储、监控后端、容量测试 |
| 新增风险 | 消息重复、队列积压、缓存不一致、检索越权、索引过期 |
| 新增开发量 | 幂等、retry、DLQ、ACL Filter、Hybrid Search、Rerank、审批状态 |
| 新增运维量 | Queue / Redis / Search 监控、索引更新、DLQ 处置、权限复核 |

**完成门禁**

- API 与 Worker 解耦，重复消息不产生重复副作用。
- RabbitMQ 积压、Redis 故障和 Research timeout 有 Runbook。
- RAG 具备 ACL、增量更新和离线评价。
- 部门级 Audit Log 与审批记录完整。

**容量判断**

根据端到端完成时间、队列等待、数据库延迟、Research 成功率和成本决定扩展，不按 API QPS 单独判断。

## 5. Level 4 Enterprise System

**目标范围**

覆盖企业多部门、多门店的正式经营分析流程，满足安全、恢复、发布和运维责任要求。

| 项目 | 内容 |
| --- | --- |
| 新增能力 | 企业 SSO、完整 RBAC、审计治理、SLO、灾害恢复、版本化发布、成本治理 |
| 新增组件 | Kubernetes 或客户标准容器平台、Secrets Manager、完整 CI/CD、集中 Observability |
| 新增成本 | 高可用基础设施、安全审查、灾害恢复环境、24 小时告警与运维责任 |
| 新增风险 | 组织权限复杂化、跨版本 State 不兼容、发布故障、审计数据膨胀、供应方依赖 |
| 新增开发量 | 多环境配置、Canary / Rollback、State Migration、SLO、权限自动化测试 |
| 新增运维量 | On-call、容量规划、恢复演练、权限复核、成本优化、供应方管理 |

**完成门禁**

- SSO、RBAC、Audit Log 通过安全与业务验收。
- SLA / SLO、Error Budget 和告警责任人明确。
- Backup、Restore、Rollback、灾害恢复演练通过。
- Kubernetes 发布验证 Workflow State、checkpoint 和在途任务兼容。
- 关键操作具备人工审批与审计证据。

**企业治理**

Prompt、KPI、Report Template、模型、数据 Schema、Workflow State 和权限策略全部版本化并受变更流程控制。

## 6. Level 5 SaaS Platform

**目标范围**

在统一平台上为多个零售客户提供隔离、可计量、可配置的经营分析服务。

| 项目 | 内容 |
| --- | --- |
| 新增能力 | Multi Tenant、租户配置、租户级权限、用量计量、服务套餐、租户级 SLO |
| 新增组件 | Tenant Control Plane、租户配置库、用量与成本系统、租户隔离监控 |
| 新增成本 | 多租户安全、客户支持、计费与合同、跨区域运维、合规与数据治理 |
| 新增风险 | 跨租户数据泄露、噪声租户、配置爆炸、成本归属错误、区域合规差异 |
| 新增开发量 | tenant_id 全链路、配额、隔离测试、租户迁移、计量、客户运维入口 |
| 新增运维量 | 租户 onboarding、配额调整、租户告警、客户支持、容量与成本分摊 |

**完成门禁**

- API、Queue、DB、Redis、OpenSearch、VectorDB、Report、Audit 全链路租户隔离。
- 默认拒绝跨租户访问，运维特权有独立审批与审计。
- 单一租户故障、流量或成本不能无边界影响其他租户。
- 租户级备份、恢复、导出和删除流程可验证。

**Multi Agent 位置**

Multi Agent 仅作为租户内部 Research 能力演进，不作为 SaaS 化前提。是否启用由租户业务、权限和成本策略决定。

## 7. 等级对照

| 维度 | Level 1 | Level 2 | Level 3 | Level 4 | Level 5 |
| --- | --- | --- | --- | --- | --- |
| 用户范围 | 开发与 Review | 限定内部用户 | 业务部门 | 全企业 | 多客户 |
| 数据库 | SQLite | PostgreSQL | PostgreSQL + Redis | 高可用数据层 | 租户隔离数据层 |
| 执行方式 | 单进程 | 稳定后台任务 | RabbitMQ + Worker Pool | Kubernetes 扩展 | 租户级调度与配额 |
| 权限 | 边界预留 | 基础角色 | 部门 / 门店 Scope | 企业 SSO + RBAC | Tenant + RBAC + Scope |
| 审计 | 基础日志 | 基础 Audit Log | 完整业务审计 | 合规治理 | 租户级审计 |
| RAG | 边界验证 | 限定资料 | Hybrid Search + ACL | 企业知识治理 | 租户知识隔离 |
| 可观测性 | 基础日志 | Trace 基线 | 全链路 Trace / Metrics | SLO / Error Budget | 租户级 SLO 与成本 |
| 恢复 | 手工重跑 | Backup / Restore | Queue / Checkpoint 恢复 | DR / Rollback 演练 | 租户级恢复 |
| 发布 | Docker | 基础 CI/CD | 多服务发布 | Canary / Rollback | 租户兼容发布 |

## 8. 未来两年升级路线图

### Year 1 Q1：Current Baseline Hardening

- 固定 API、TaskService、Workflow、KPI、Research、Report 契约。
- 建立 KPI、Prompt、Template 和数据 Schema 版本。
- 补齐异常路径、幂等、日志关联和基础评价。
- 交付：Level 1 质量门禁通过。

### Year 1 Q2：Internal Tool Foundation

- SQLite 迁移 PostgreSQL。
- 接入内部身份，落地基础 RBAC 与 Audit Log。
- 建立 OpenTelemetry 基线和 Backup / Restore。
- 交付：限定内部用户可用的 Level 2。

### Year 1 Q3：Distributed Execution

- 引入 Redis、RabbitMQ、KPI / Research / Report Worker Pool。
- 完成 retry、DLQ、backpressure、graceful shutdown。
- 执行首轮端到端 Load Test 和故障演练。
- 交付：100～1000 任务规模的容量基线。

### Year 1 Q4：Department RAG and Approval

- 建设 OpenSearch、VectorDB、Hybrid Search、Rerank、ACL。
- 落地文档增量更新与检索评价。
- 增加管理层报告人工审批和 Audit Log。
- 交付：Level 3 部门系统。

### Year 2 Q1：Enterprise Security and SLO

- 完成企业 SSO、完整 RBAC、权限复核和 Secret 管理。
- 定义 SLA、SLO、Error Budget、告警与 Incident Runbook。
- 完成数据分类、审计保留和安全 Review。
- 交付：企业正式运用安全门禁。

### Year 2 Q2：Kubernetes and Release Governance

- 部署 API、SSE、Worker、Collector 到 Kubernetes 或客户标准平台。
- 落地 readiness、HPA、graceful shutdown、Canary、Rollback。
- 验证 Workflow State 与 checkpoint 跨版本兼容。
- 交付：可扩展与可回滚发布能力。

### Year 2 Q3：Disaster Recovery and Cost Governance

- 完成数据库、索引、报告和审计的灾害恢复演练。
- 建立模型、检索、Queue 和租户候选成本归属。
- 根据评价证据决定是否拆分 Multi Agent。
- 交付：Level 4 Enterprise System。

### Year 2 Q4：SaaS Readiness Decision

- 评估 tenant_id 全链路改造、隔离等级、合规和支持成本。
- 实现租户配置、配额、用量计量和隔离验证的最小闭环。
- 由业务、法务、安全和运维共同决定是否进入 Level 5。
- 交付：SaaS Go / No-Go 决策与下一周期投资计划。

## 9. 投资与决策门禁

| 决策 | 必须证据 | 禁止依据 |
| --- | --- | --- |
| 引入 Redis | 状态读取与 SSE 事件瓶颈 | “Redis 更快” |
| 引入 RabbitMQ | 队列等待、背压、故障恢复需求 | “异步系统都需要 Queue” |
| 引入 Kubernetes | 独立扩展、环境治理、发布需求 | “企业系统必须上 K8s” |
| 引入 VectorDB | 语义检索评价优于基线 | “RAG 必须有向量库” |
| 拆分 Multi Agent | 权限、上下文、扩展特性确实分离 | “Agent 越多越先进” |
| 进入 SaaS | 客户需求、隔离、计量、支持成本成立 | “单租户系统可以直接复用” |

Roadmap 每季度 Review 一次。任何升级项都必须明确 Owner、业务收益、成本、风险、完成条件和回退方案。
