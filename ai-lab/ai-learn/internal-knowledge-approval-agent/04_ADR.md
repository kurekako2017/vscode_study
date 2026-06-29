# Architecture Decision Records

状态说明：`Accepted` 表示当前设计基线；后续若条件变化，以新 ADR 替代，不直接改写历史决策。

## 目录

- [ADR-001：为什么使用 RAG](#adr-001为什么使用-rag)
- [ADR-002：为什么需要 Approval Workflow](#adr-002为什么需要-approval-workflow)
- [ADR-003：为什么高风险问题不能直接回答](#adr-003为什么高风险问题不能直接回答)
- [ADR-004：为什么使用 LangGraph](#adr-004为什么使用-langgraph)
- [ADR-005：为什么使用 SSE](#adr-005为什么使用-sse)
- [ADR-006：为什么需要 Audit Log](#adr-006为什么需要-audit-log)
- [ADR-007：为什么需要 RBAC](#adr-007为什么需要-rbac)
- [ADR-008：为什么当前先用 SQLite](#adr-008为什么当前先用-sqlite)
- [ADR-009：为什么未来升级 VectorDB](#adr-009为什么未来升级-vectordb)
- [ADR-010：为什么需要 OpenSearch](#adr-010为什么需要-opensearch)
- [ADR-011：为什么 Retriever 和 Generator 分离](#adr-011为什么-retriever-和-generator-分离)
- [ADR-012：为什么需要 Rerank](#adr-012为什么需要-rerank)
- [ADR-013：为什么 Prompt 需要版本管理](#adr-013为什么-prompt-需要版本管理)
- [ADR-014：为什么需要人工审批](#adr-014为什么需要人工审批)
- [ADR-015：为什么需要 OpenTelemetry](#adr-015为什么需要-opentelemetry)
- [ADR 共通复核规则](#adr-共通复核规则)

## ADR-001：为什么使用 RAG

状态：Accepted

### Context

回答必须基于企业当前有效且用户有权访问的社内文書。仅依赖生成器内部知识无法证明依据，也无法及时反映内部规则改版。

### Decision

采用 RAG，将权限过滤、Retriever、Rerank、Evidence Gate、Context Builder 和 Citation Validator 组成受控检索链。正式回答必须携带可追踪 citation；证据不足时拒绝确定性回答或转人工。

### Alternative

- 只用关键词搜索并让用户自行阅读文档。
- 把所有文档直接放入超长上下文。
- 只依赖生成器已有知识。

### Tradeoff

RAG 增加文档治理、切块、索引、评价和权限同步复杂度。检索错误会传递到回答，因此需要独立质量指标。

### Impact

必须建立 document/version/chunk/citation 模型、离线检索集和索引更新流程。回答 API 需要返回引用与版本。

## ADR-002：为什么需要 Approval Workflow

状态：Accepted

### Context

契約、個人情報、セキュリティ、経費、法務和障害対応涉及明确组织责任。即使检索结果正确，适用条件和最终判断也可能需要负责人确认。

### Decision

将审批建模为可持久化、可中断、可恢复的 Workflow。高风险或不确定问题创建 approval，保存 checkpoint，等待承認、差戻し或却下。

### Alternative

- 通过邮件或聊天工具在系统外确认。
- 前端弹窗让任意用户点击确认。
- 所有问题均由人工回答。

### Tradeoff

审批降低直出速度，增加待办、超时、代理、升级和运营负荷，但能维持责任边界并提供审计证据。

### Impact

需要审批状态机、责任矩阵、SLA、幂等决定、草案版本绑定和恢复测试。

## ADR-003：为什么高风险问题不能直接回答

状态：Accepted

### Context

高风险回答错误可能导致合同、隐私、安全、财务或生产事故。生成结果的语言流畅度不能代表业务正确性或授权有效性。

### Decision

high/critical 风险禁止自动发布；medium 是否审批由策略定义；分类异常和证据冲突按高风险处理。critical 可直接阻断并升级，而不是仅进入普通队列。

### Alternative

- 在回答底部增加免责声明后直接发布。
- 只在低置信度时审批。
- 允许用户自行决定是否采纳。

### Tradeoff

保守策略提高误报和等待量，但显著降低高影响漏判。后续优化以分层规则和运营数据降低无效审批，而不是降低安全上限。

### Impact

风险分类必须独立、可解释、版本化，并以 high-risk recall 和漏判事件为核心指标。

## ADR-004：为什么使用 LangGraph

状态：Accepted

### Context

流程包含条件路由、节点失败、持久 checkpoint、人工等待和恢复。普通线性函数或仅在内存中的异步任务难以表达长时间审批状态。

### Decision

采用 LangGraph StateGraph 显式定义 State、Node、Edge、条件分支和 interrupt/resume。Task/Question 生命周期仍由 Application Service 持有。

### Alternative

- 手写大量 if/else 和状态迁移。
- 使用简单后台任务且把状态只保存在内存。
- 立即引入完整 BPM 平台。

### Tradeoff

LangGraph 引入框架学习、State schema 兼容和 checkpoint 运维要求。它不替代领域状态、权限或事务设计。

### Impact

需定义 State 版本、节点合同、超时重试、幂等副作用和 checkpoint 恢复测试；禁止把所有业务规则塞进图节点。

## ADR-005：为什么使用 SSE

状态：Accepted

### Context

检索、草案、审批和发布是异步过程，用户需要看到进度。主要通信方向是服务端向浏览器推送状态，不需要持续双向会话。

### Decision

采用 SSE 发布 `status`、`approval_required`、`approval_updated`、`done` 和 `error`。事件持久化并带 sequence，支持断线续传；正式回答通过 GET API 获取。

### Alternative

- 浏览器固定间隔轮询。
- WebSocket。
- 长轮询或同步等待完整结果。

### Tradeoff

SSE 单向且需要处理代理缓冲、连接上限、认证和重连。相比 WebSocket，协议和服务端状态更简单，符合当前通信模式。

### Impact

需要 EventRepository、Last-Event-ID/after 机制、keepalive、慢客户端策略和 SSE 集成测试。

## ADR-006：为什么需要 Audit Log

状态：Accepted

### Context

高风险回答需要事后证明提问者、证据、策略、草案版本、审批人和最终结果。普通应用日志可能被采样、轮转或缺少业务语义。

### Decision

建立独立 Audit Record 模型，采用追加写语义，记录 actor、role/scope、action、resource、workflow、版本、before/after hash 和 result。审计查询也被审计。

### Alternative

- 只保存应用日志。
- 只保存当前业务表状态。
- 只记录审批最终结果。

### Tradeoff

审计增加存储、权限、保留期和隐私治理成本。记录过多正文会扩大敏感面，因此采用引用与哈希最小化。

### Impact

业务事务必须可靠地产生审计事件；生产需评估 WORM、哈希链、受限账号和长期归档。

## ADR-007：为什么需要 RBAC

状态：Accepted

### Context

员工不能访问所有内部文档，审批者也只负责特定风险领域。仅登录不能满足动作和资源范围控制。

### Decision

采用 RBAC + resource scope。角色定义动作，scope 限定部门、文档等级和风险领域。生产身份来自 SSO；服务端构建 ActorContext，检索时强制 ACL。

### Alternative

- 所有登录用户共享权限。
- 仅在前端隐藏按钮和引用。
- 每个 API 内分别硬编码部门判断。

### Tradeoff

角色和 scope 组合增加策略管理复杂度，需要缓存失效、授权测试和职责分离管理。

### Impact

Repository 和 Retriever 接口必须接受授权 scope；所有受控动作需要 policy decision 和 audit。

## ADR-008：为什么当前先用 SQLite

状态：Accepted

### Context

下一阶段需要验证 Question、Workflow、Approval、Event 和 Audit 的持久化边界，但当前不需要多实例、高可用或外部数据库运维。

### Decision

使用 SQLite 作为单机本地基线，开启 foreign keys、WAL 和 busy timeout。业务层依赖 Repository 接口，避免绑定 SQLite SQL 细节。

### Alternative

- 只用内存字典。
- 立即引入 PostgreSQL。
- 为每类数据使用不同存储。

### Tradeoff

SQLite 部署简单且支持事务，但写并发、HA、多实例共享和运维能力有限。它不能代表生产数据库拓扑。

### Impact

Backend 初始只运行一个实例；设计 migration、事务和 Repository 契约，为 PostgreSQL 演进保留空间。

## ADR-009：为什么未来升级 VectorDB

状态：Accepted with Trigger

### Context

当前固定文档和关键词检索足以验证业务流程。随着语料规模、同义表达和语义查询增加，纯关键词召回可能不足。

### Decision

不在当前阶段接入 VectorDB。只有离线评价显示语义召回能显著改善目标查询，且 ACL、成本、数据驻留和运维条件满足时，才引入向量索引。

### Alternative

- 从第一天起仅使用向量检索。
- 永久只使用 SQLite LIKE/FTS。
- 由生成器扩写大量查询代替语义索引。

### Tradeoff

VectorDB 改善部分语义召回，但引入 embedding 版本、重建索引、过滤召回、容量和供应商治理问题。

### Impact

Retriever 接口必须隐藏存储实现；文档 chunk 保留可重建元数据；建立语义检索评价基线后再决策产品。

## ADR-010：为什么需要 OpenSearch

状态：Accepted with Trigger

### Context

企业文档包含规则编号、产品名、错误码和精确条款，词法检索不可被语义检索完全替代。日文分词、过滤和索引生命周期也需要成熟能力。

### Decision

生产候选采用 OpenSearch 处理 BM25、日文 analyzer、metadata/ACL filter 和索引运营，并与向量候选做混合检索。当前阶段不部署。

### Alternative

- 仅使用 VectorDB。
- 使用数据库全文索引承担所有规模。
- 自建搜索服务。

### Tradeoff

OpenSearch 运维和资源成本较高，需要 shard、mapping、alias、备份与升级治理。小规模下可能不经济。

### Impact

文档 schema 需支持词法与向量双索引；通过评价和容量触发迁移，不按技术偏好提前引入。

## ADR-011：为什么 Retriever 和 Generator 分离

状态：Accepted

### Context

检索负责“找什么证据”，生成负责“如何组织回答”。两者失败模式、权限、指标和替换频率不同。

### Decision

定义独立 Retriever、ContextBuilder、AnswerProvider 和 CitationValidator 合同。Generator 只能读取明确传入的 evidence，不能绕过 Retriever 访问文档库。

### Alternative

- 单一 Agent 同时搜索、选择和回答。
- Generator 自行调用任意搜索工具。
- 把完整索引查询细节暴露给前端。

### Tradeoff

分离增加接口和中间模型，但提高可测试性、权限控制、评价定位和 Provider 替换能力。

### Impact

建立 RetrievalCandidate、Evidence、Citation 和 DraftAnswer schema；分别测试检索质量与回答正确性。

## ADR-012：为什么需要 Rerank

状态：Accepted

### Context

Retriever 为提高召回会返回较多候选；直接把所有候选送入上下文会增加噪声、冲突和长度。首轮检索分数不一定反映最终问题相关性。

### Decision

在 Retrieve top_n 后执行独立 Rerank，当前用确定性规则综合关键词覆盖、版本有效性、文档类型和章节匹配，选择 top_k 证据。

### Alternative

- 直接使用 Retriever 排序。
- 扩大上下文纳入全部候选。
- 只保留最高分单一片段。

### Tradeoff

Rerank 增加延迟和配置，错误排序也可能降低召回。需要保留原始分数和重排分数用于诊断。

### Impact

建立 NDCG/MRR 评价、超时和降级策略；Reranker 不得改变 ACL 结果。

## ADR-013：为什么 Prompt 需要版本管理

状态：Accepted

### Context

即使当前使用固定回答模板，未来 Prompt/Template 的变化也会影响草案格式、引用和风险判断。没有版本无法复现历史结果。

### Decision

将 system instruction、answer template、risk template 作为版本化配置。每个 DraftAnswer 和 Audit Record 保存实际版本；发布前通过测试与评价门禁。

### Alternative

- 将 Prompt 字符串散落在代码中。
- 直接在线修改且不记录历史。
- 只依赖 Git commit 推断版本。

### Tradeoff

版本管理增加发布流程和兼容成本，但提供可复现、回滚、A/B 对比和审计基础。

### Impact

模板需要 schema、owner、review、effective time 和回归集；在途 Workflow 固定使用启动时版本。

## ADR-014：为什么需要人工审批

状态：Accepted

### Context

技术系统无法替代法务、安全、财务和事故负责人的组织授权。部分问题即使证据完整，也需要结合例外、时效和业务影响作判断。

### Decision

保留 human-in-the-loop。承認者看到问题、证据、草案、风险理由和版本差异后作决定。系统不把超时、无人处理或模型建议视为批准。

### Alternative

- 全自动发布。
- 所有回答都人工编写。
- 由提问者自行确认风险。

### Tradeoff

人工审批造成等待和队列，需要 SLA、代理、升级与负荷管理；但能将关键判断交给有授权和上下文的人。

### Impact

需要承認者 UI、待办查询、通知、理由必填规则、职责分离和审批质量指标。

## ADR-015：为什么需要 OpenTelemetry

状态：Accepted with Production Phase

### Context

完整请求跨越 API、Workflow、Retriever、数据库、SSE 和可能的 Worker。仅靠各服务日志难以定位延迟、重试和失败传播。

### Decision

生产阶段采用 OpenTelemetry 统一 trace、metric 和 log correlation。人工等待使用 trace link 或新 span 关联 workflow_id，不保持超长 span。

### Alternative

- 只写文本日志。
- 每个组件使用不同监控方案。
- 只监控主机 CPU 和内存。

### Tradeoff

Telemetry 增加埋点、采样、存储和敏感数据治理成本。过度高基数字段会造成费用和查询问题。

### Impact

定义稳定 span/metric 名称、采样策略、SLO、告警和数据脱敏。request_id、trace_id、workflow_id 需可关联但职责不同。

## ADR 共通复核规则

以下情况触发 ADR 复核：

- 文档规模、并发量或审批等待量超过当前基线。
- SSO、RBAC、数据驻留或法规要求变化。
- 检索评价显示现有 Retriever/Reranker 无法达到质量门槛。
- 单实例 SQLite 或进程内执行成为可用性瓶颈。
- 需要外部模型、工具调用或不可逆业务动作。
- 架构决策的前提不再成立，或实际运行数据与预期明显不符。

新决策以新的 ADR 编号记录，并标明 supersedes/superseded by，不删除原有 Context 和 Tradeoff。

