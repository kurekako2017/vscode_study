# 12_ADR

# 目录

- [ADR-001 使用 Task API](#adr-001-使用-task-api)
- [ADR-002 引入 TaskService](#adr-002-引入-taskservice)
- [ADR-003 使用 LangGraph Workflow](#adr-003-使用-langgraph-workflow)
- [ADR-004 KPI 不使用 Agent](#adr-004-kpi-不使用-agent)
- [ADR-005 Research Agent 独立](#adr-005-research-agent-独立)
- [ADR-006 使用 SSE](#adr-006-使用-sse)
- [ADR-007 企业数据迁移 PostgreSQL](#adr-007-企业数据迁移-postgresql)
- [ADR-008 Redis 只保存热状态](#adr-008-redis-只保存热状态)
- [ADR-009 RabbitMQ 承接后台任务](#adr-009-rabbitmq-承接后台任务)
- [ADR-010 使用 OpenTelemetry](#adr-010-使用-opentelemetry)
- [ADR-011 服务端实施 RBAC](#adr-011-服务端实施-rbac)
- [ADR-012 Audit Log 独立治理](#adr-012-audit-log-独立治理)
- [ADR-013 使用 Docker 标准化环境](#adr-013-使用-docker-标准化环境)
- [ADR-014 满足条件后使用 Kubernetes](#adr-014-满足条件后使用-kubernetes)
- [ADR-015 RAG 使用 Hybrid Search 与 Rerank](#adr-015-rag-使用-hybrid-search-与-rerank)
- [ADR-016 OpenSearch 与 VectorDB 并存](#adr-016-opensearch-与-vectordb-并存)
- [ADR-017 Repository 隔离持久化实现](#adr-017-repository-隔离持久化实现)
- [ADR-018 使用结构化日志和关联 ID](#adr-018-使用结构化日志和关联-id)
- [ADR-019 Checkpoint 持久化并版本化](#adr-019-checkpoint-持久化并版本化)
- [ADR-020 高影响报告引入人工审批](#adr-020-高影响报告引入人工审批)
- [ADR-021 Multi Agent 按条件启用](#adr-021-multi-agent-按条件启用)
- [ADR-022 使用 Model Router 管理模型路径](#adr-022-使用-model-router-管理模型路径)
- [ADR-023 Multi Tenant 延后到 SaaS 阶段](#adr-023-multi-tenant-延后到-saas-阶段)
- [ADR-024 CI/CD 必须支持渐进发布与回滚](#adr-024-cicd-必须支持渐进发布与回滚)

ADR 状态说明：Accepted 表示当前架构决策；Planned 表示企业化目标，只有完成对应验收条件后才转为 Accepted。

## ADR-001 使用 Task API

**状态：Accepted**

**Context**

经营分析包含 KPI、Research 和报告生成，执行时间不稳定，同步请求容易 timeout、重复提交且无法展示进度。

**Decision**

创建任务立即返回 task_id，执行、状态查询、事件订阅和报告读取使用独立边界。

**Alternative**

- 同步 API 等待完整报告。
- 增大网关与客户端 timeout。

**Tradeoff**

增加状态机、幂等、结果保存和过期清理责任。

**Impact**

API 契约必须区分 accepted、running、completed、failed；所有后续数据通过 task_id 关联。

## ADR-002 引入 TaskService

**状态：Accepted**

**Context**

API、Workflow、SSE、Repository 均需要更新任务生命周期，若分散实现会产生状态冲突。

**Decision**

TaskService 统一负责创建、状态迁移、Workflow 启动、事件发布、结果保存和失败收口。

**Alternative**

- API Route 直接编排。
- LangGraph 同时管理 HTTP 外层生命周期。

**Tradeoff**

TaskService 有膨胀风险，需要持续限制其业务知识。

**Impact**

API 和 Worker 只能通过 TaskService 执行任务用例；KPI、Research、Report 内部逻辑不得进入 TaskService。

## ADR-003 使用 LangGraph Workflow

**状态：Accepted**

**Context**

系统需要 State、Node、条件路由、部分失败、checkpoint 与恢复，普通嵌套函数难以持续 Review。

**Decision**

使用 LangGraph Workflow 表达 route、KPI、research、report 及其 Edge。

**Alternative**

- 普通 Python 顺序函数。
- 只用消息队列串联函数。

**Tradeoff**

引入框架依赖、State 治理、checkpoint 兼容和图复杂度。

**Impact**

每个 Node 必须定义输入、输出、错误和终止路径；框架类型不得泄露到 API 与 Domain 契约。

## ADR-004 KPI 不使用 Agent

**状态：Accepted**

**Context**

KPI 直接用于经营判断，要求固定口径、可复算和可审计。

**Decision**

销售、库存、商品、会员和促销 KPI 使用 Fixed KPI Workflow；LLM 只解释结构化结果。

**Alternative**

- Agent 自主选择计算步骤。
- LLM 生成查询或计算结果后直接进入报告。

**Tradeoff**

新增 KPI 需要正式定义、实现、测试和版本变更。

**Impact**

KPI 模块不得依赖 Agent 或模型；结果必须携带规则、数据期间和来源版本。

## ADR-005 Research Agent 独立

**状态：Accepted**

**Context**

市场、竞品和内部资料调查的来源、权限、timeout 与失败特征不同于 KPI。

**Decision**

Research Agent 独立管理 Tool 选择、调查、来源、摘要、风险和降级状态。

**Alternative**

- 把 Research 作为 KPI 内部步骤。
- 不提供市场和竞品调查。

**Tradeoff**

需要额外 Tool 契约、权限过滤、timeout、评价和来源治理。

**Impact**

Research 失败允许保留 KPI 并生成带缺失说明的报告；Agent 不得修改 KPI。

## ADR-006 使用 SSE

**状态：Accepted**

**Context**

用户需要看到长任务进度，当前交互主要是服务端到浏览器的单向通知。

**Decision**

使用 SSE 发送 started、status、error、done，状态 API 保存最终事实。

**Alternative**

- 客户端定时轮询。
- 全面使用 WebSocket。

**Tradeoff**

需要处理重连、事件顺序、代理缓冲、连接容量和多实例分发。

**Impact**

SSE 连接中断不能取消任务；done 只表示成功，error 表示失败终止。

## ADR-007 企业数据迁移 PostgreSQL

**状态：Planned**

**Context**

SQLite / CSV 适合当前数据模型确认，但不满足多用户并发、备份、权限和多实例一致性。

**Decision**

企业运用以 PostgreSQL 保存业务数据、任务、报告和审计事实。

**Alternative**

- 长期使用 SQLite。
- 每个模块自行选择数据库。

**Tradeoff**

增加迁移、Schema、事务、连接池、备份和运维责任。

**Impact**

迁移前固定 Repository，执行数据校验、restore test 和 rollback；业务代码不得依赖 SQLite 特性。

## ADR-008 Redis 只保存热状态

**状态：Planned**

**Context**

多 API 与 SSE 实例需要共享高频状态和短期事件，但这些数据必须可恢复。

**Decision**

Redis 保存热状态、SSE 事件、短期缓存和必要的分布式协调；PostgreSQL 保存事实。

**Alternative**

- 所有读取直接访问 PostgreSQL。
- 把 Redis 作为任务唯一存储。

**Tradeoff**

增加缓存一致性、TTL、内存容量和高可用治理。

**Impact**

Redis 故障时状态 API 回退 PostgreSQL；任何不能重建的关键数据不得只存在 Redis。

## ADR-009 RabbitMQ 承接后台任务

**状态：Planned**

**Context**

单进程执行无法稳定处理任务突增、进程重启、重试和不同负载隔离。

**Decision**

TaskService 投递任务到 RabbitMQ，KPI、Research、Report 使用独立 Worker Pool。

**Alternative**

- API 进程直接执行。
- 仅增加更多 API 实例。

**Tradeoff**

引入消息重复、乱序、积压、DLQ、消费者治理和运维成本。

**Impact**

消费者必须幂等；重试按错误类型限制；超过上限进入 DLQ 并由受控流程处置。

## ADR-010 使用 OpenTelemetry

**状态：Planned**

**Context**

异步任务横跨 API、TaskService、Queue、Node、Tool、DB 和 Report，单独日志无法快速定位延迟与失败。

**Decision**

使用 OpenTelemetry 统一 Trace、Metrics、Logs 关联，trace context 与 task_id 一起跨异步边界传递。

**Alternative**

- 只使用文本日志。
- 各服务使用不一致的观测方案。

**Tradeoff**

增加采集、存储、采样、成本和敏感字段治理。

**Impact**

每个关键 Node 与外部依赖定义 Span；禁止采集 Prompt、会员数据和内部资料正文。

## ADR-011 服务端实施 RBAC

**状态：Planned**

**Context**

经营层、部门和门店的数据范围不同，前端显示控制不能阻止直接 API 访问。

**Decision**

在 API、Service、Repository、Search 与 Report 边界同时执行 role + data scope 授权，默认拒绝。

**Alternative**

- 仅前端隐藏功能。
- 只在 API 入口检查角色。

**Tradeoff**

权限传播、组织变更、测试矩阵和运维管理复杂度上升。

**Impact**

所有业务查询携带 tenant / department / store scope；权限变更与拒绝事件进入 Audit Log。

## ADR-012 Audit Log 独立治理

**状态：Planned**

**Context**

管理层报告、内部资料和会员数据访问需要追踪谁在何时对什么执行了什么操作。

**Decision**

Audit Log 与应用日志分离，独立管理字段、访问权限、保留期限和完整性。

**Alternative**

- 使用普通应用日志替代审计。
- 保存完整 Prompt 与业务正文便于调查。

**Tradeoff**

增加存储、查询、归档和合规治理成本。

**Impact**

审计只保存必要标识和结果；高风险操作的审计写入失败时默认失败关闭。

## ADR-013 使用 Docker 标准化环境

**状态：Accepted**

**Context**

开发、测试、Review 和部署准备需要一致的依赖与启动条件。

**Decision**

使用 Docker 构建 Backend 与 Frontend 运行环境，配置和 Secret 外部化。

**Alternative**

- 依赖开发者本地环境。
- 每个环境使用不同安装手册。

**Tradeoff**

增加镜像构建、漏洞扫描、版本和容器调试责任。

**Impact**

镜像必须非 root、可扫描、可追踪；日志输出 stdout，并提供 health check 与 graceful shutdown。

## ADR-014 满足条件后使用 Kubernetes

**状态：Planned**

**Context**

API、SSE、KPI、Research 和 Report 的扩展特性不同，但过早使用 Kubernetes 会增加运维成本。

**Decision**

在独立扩展、多环境治理和发布需求经容量证据确认后，使用 Kubernetes 或客户标准容器平台。

**Alternative**

- 从初期直接 Kubernetes 化。
- 永久使用单机 Docker Compose。

**Tradeoff**

获得扩展与发布能力，同时承担集群、网络、Secret、观测和恢复复杂度。

**Impact**

上线前验证 readiness、graceful shutdown、State / checkpoint 兼容、Canary 和 rollback。

## ADR-015 RAG 使用 Hybrid Search 与 Rerank

**状态：Planned**

**Context**

商品代码和固有名词需要关键词精确性，抽象业务问题需要语义召回，仅单一检索方式不足。

**Decision**

使用关键词检索与向量检索组成 Hybrid Search，再以 Rerank 选择 Top-K Evidence。

**Alternative**

- 仅关键词检索。
- 仅向量检索。

**Tradeoff**

增加索引、延迟、分数融合、评价和运维复杂度。

**Impact**

必须建立 recall@k、MRR、引用正确性、groundedness、无结果率和延迟基线。

## ADR-016 OpenSearch 与 VectorDB 并存

**状态：Planned**

**Context**

Retail Insight AI 同时需要结构条件、全文搜索和语义搜索。

**Decision**

OpenSearch 承接关键词与条件检索，VectorDB 承接语义检索；两者都执行 Metadata / ACL Filter。

**Alternative**

- 用单一搜索引擎承担全部场景。
- 把所有业务表无差别向量化。

**Tradeoff**

增加双索引同步、删除、权限一致性和故障治理。

**Impact**

原始文档保持唯一来源；索引必须支持增量更新、删除传播和版本追踪。

## ADR-017 Repository 隔离持久化实现

**状态：Accepted**

**Context**

当前 SQLite 将迁移 PostgreSQL，并增加 Redis 与 Search，业务层不能绑定具体驱动。

**Decision**

Service、KPI、Workflow 依赖 Repository Interface，实现放在基础设施边界。

**Alternative**

- 业务模块直接执行 SQL。
- 使用全局通用数据库对象。

**Tradeoff**

增加接口、映射和 Contract Test，但降低迁移影响。

**Impact**

Repository 返回 Domain Model，不暴露 ORM / Driver 类型；Implementation 不能反向定义业务语义。

## ADR-018 使用结构化日志和关联 ID

**状态：Accepted**

**Context**

任务跨多个组件执行，纯文本异常无法从入口追到失败 Node。

**Decision**

所有日志结构化记录 request_id、task_id、trace_id、service、workflow_node、event、duration 和 error_code。

**Alternative**

- 各模块自由输出文本日志。
- 记录完整输入输出便于调试。

**Tradeoff**

需要字段标准、日志治理、脱敏和存储成本控制。

**Impact**

关联 ID 在边界生成并传递；禁止记录 Secret、会员数据、完整 Prompt 和内部资料正文。

## ADR-019 Checkpoint 持久化并版本化

**状态：Planned**

**Context**

内存 checkpoint 无法支持进程重启、跨版本恢复和长任务发布。

**Decision**

将 checkpoint 持久化，并保存 task_id、Workflow 版本和 State Schema 版本。

**Alternative**

- 失败后始终从头执行。
- checkpoint 只保存在 Worker 内存。

**Tradeoff**

增加状态迁移、清理、兼容、敏感字段和存储治理。

**Impact**

发布前必须验证旧 checkpoint 恢复；副作用 Node 使用幂等记录避免重复执行。

## ADR-020 高影响报告引入人工审批

**状态：Planned**

**Context**

管理层报告可能影响经营决策，Research 来源不足或报告版本变化时需要明确责任人确认。

**Decision**

Report Generator 后进入 approval interrupt，由授权人员批准、退回或要求补充。

**Alternative**

- 所有报告生成后自动交付。
- 审批完全在线下完成且不记录。

**Tradeoff**

增加等待时间、审批权限、代理审批、超时和版本竞争处理。

**Impact**

审批绑定不可变 report_id 与版本；决定、理由和操作者进入 Audit Log。

## ADR-021 Multi Agent 按条件启用

**状态：Planned**

**Context**

当前单一 Research Agent 能覆盖调查；无理由拆分会增加延迟、成本和消息复杂度。

**Decision**

只有市场、竞品、内部资料在职责、权限、上下文或扩展特性上明确分离时，才引入 Supervisor 与专用 Agent。

**Alternative**

- 从初期构建多个 Agent。
- 永久维持单一 Agent。

**Tradeoff**

Multi Agent 提升隔离与独立扩展，同时增加协调、冲突、预算和终止治理。

**Impact**

拆分前必须提交评价证据；Fixed KPI Workflow 永远不进入 Agent 自主协商。

## ADR-022 使用 Model Router 管理模型路径

**状态：Planned**

**Context**

Research、摘要和管理层报告对质量、延迟、成本与数据敏感度要求不同，单一模型形成供应方依赖。

**Decision**

通过 Model Router 按任务类型、数据等级、质量门槛和健康状态选择已验证模型。

**Alternative**

- 所有任务固定单一模型。
- 每个模块自行选择模型。

**Tradeoff**

增加输出差异、评价矩阵、fallback、成本和版本治理。

**Impact**

每个任务记录模型与版本；fallback 必须通过相同质量与安全基线，不能只按价格路由。

## ADR-023 Multi Tenant 延后到 SaaS 阶段

**状态：Planned**

**Context**

当前目标是单一零售企业内部系统，提前引入租户控制会增加所有数据与运维路径复杂度。

**Decision**

Level 4 前以组织、部门、门店 Scope 为主；只有 SaaS 商业决策成立后实施 tenant_id 全链路隔离。

**Alternative**

- 从初期实现 Multi Tenant。
- 每个客户永久部署独立系统。

**Tradeoff**

延后降低当前复杂度，但未来改造需要覆盖 API、Queue、DB、Cache、Search、Report、Audit。

**Impact**

现有契约预留组织边界但不宣称多租户；SaaS 前必须完成隔离测试、配额、计量和租户恢复。

## ADR-024 CI/CD 必须支持渐进发布与回滚

**状态：Planned**

**Context**

应用、Workflow State、Prompt、KPI、Template 和 DB Schema 同时版本化，简单滚动部署可能破坏在途任务。

**Decision**

CI/CD 执行测试、架构规则、镜像扫描、Migration 验证、Canary 和 rollback；发布绑定版本矩阵。

**Alternative**

- 人工构建并直接覆盖部署。
- 只检查 API health 即判定发布成功。

**Tradeoff**

增加流水线、测试环境、发布时间和维护成本。

**Impact**

发布成功条件包含任务恢复、SSE、权限、报告质量和观测指标；失败时回滚应用、数据兼容层和流量。
