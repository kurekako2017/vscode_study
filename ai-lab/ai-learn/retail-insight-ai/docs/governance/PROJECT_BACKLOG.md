# retail-insight-ai Project Backlog

## 2026-07-17 Completed: V1.0 部署指南文档

- [x] 新增 `docs/development/DEPLOYMENT_GUIDE.md`
- [x] 区分：无 Docker 本地开发 / Compose 验收演示 / 生产硬化差距
- [x] 服务名 `postgres|backend|frontend`、volume `erip_postgres_data`、默认用户 `erip_app`、库 `erip`
- [x] 脚本：`compose_up/down/verify`、`start_backend/frontend`、`seed_scenario01`、`check_env`、`run_tests`
- [x] README + CHANGELOG 登记

最后更新：2026-07-17

## 2026-07-17 Completed: AI Runtime 持久化 + 页面衔接

- [x] Migration `20260717_08_ai_runtime`：`ai_runtime_settings` 单例（mode/kill_switch/version/actor；无 Secret）
- [x] `AiRuntimeService` + `GET/PATCH /api/v1/admin/ai-runtime`（乐观锁、二次确认、readiness fail-closed）
- [x] 启动恢复 effective_mode；Kill Switch 强制 stub；Persistent Audit `ai_runtime.*`
- [x] Frontend AdminLlmPage 接新合同；InMemory 503 fail-closed
- [x] Document 列表 `chunk_count/searchable/archived` + 跳转 RAG document_id
- [x] RAG 自动 document_id 过滤；报告→提交审批 handoff；Approval query `approval_id`
- [x] `scripts/seed_scenario01.sh`
- [x] 测试修复：Alembic head 列表；RagPage 多匹配；InMemory fail-closed 独立用例
- [x] handbook / VERIFY / FRONTEND 学习指南导航标签对齐
- [x] Compose rebuild healthy；head 08；Volume 保留；live AI Runtime stub

验证：Frontend **115/115**；InMemory Backend **280**（59 skip）；AI Runtime PG **8/8**；production build OK。全量 PG suite 见本轮 CHANGELOG 记录。

未做：真实 LLM、git commit、`docker compose down -v`。

最后更新：2026-07-17

## 2026-07-17 Completed: ERIP V1.0 页面可用性与 AI 管理

- [x] 审计并确认 `LLM_PROVIDER_MODE` 枚举：`stub` | `openrouter` | `fallback_chain`
- [x] Backend：`GET /api/v1/reports` 报告目录；`GET/PUT /api/v1/admin/llm/runtime`
- [x] ReportRepository.list_recent（interface / inmemory / postgres）
- [x] Frontend：导航 RAG/AI分析、KPI任务分析、AI管理；AdminLlmPage
- [x] ApprovalPage 报告下拉（无手抄 task_id）
- [x] DocumentsPage 就绪状态与 PG content 存储说明
- [x] RagPage Provider/Model/Route/Token/Cost/Status 展示
- [x] RUNBOOK：账号、8080/5173、Scenario01 导入、存储、LLM 成本风险
- [x] Frontend 113/113；Backend admin/catalog 测试；Compose rebuild；stub only
- [x] 禁止：真实 LLM、volume 删除、git commit、旧 Migration 改动

完成记录：PostgreSQL 数据与 `erip_postgres_data` Volume 保留；live health 200、llm_runtime=stub、reports total≥4、documents 仍在。

已知后续（非阻断）：

- [x] handbook 面试材料中「RAG検索/分析依頼」旧导航标签可增量对齐
- [x] VERIFY_CHECKLIST / README 若仍写旧入口可增量指针

最后更新：2026-07-17

## 2026-07-17 Completed: ERIP V1.0 第三批项目文档同步

- [x] 根入口 README / ROADMAP / TASK 与 V1.0 事实对齐
- [x] ARCHITECTURE / APPROVAL_WORKFLOW / DATA_CONTRACTS / AI_AGENT_DESIGN_GUIDE 增量校正
- [x] 学习文档 Foundation + Frontend 入口增量
- [x] PROJECT_BIBLE / handbook 01·06·08·09·11·README 增量
- [x] 冻结第一批启动验收文档与第二批面试材料
- [x] CHANGELOG 登记
- [x] 运行环境检测与页面可用性（见上节）

完成记录：第三批为文档；页面可用性批为代码+测试+RUNBOOK。

最后更新：2026-07-17



## 2026-07-17 Completed: Docker/Compose + Stub E2E 文件与本地验证

- [x] Compose 服务：postgres(pgvector) / backend / frontend
- [x] Alembic 启动链与 healthcheck
- [x] dockerignore 证明 `.env` 不进构建上下文
- [x] Stub API E2E 业务主链
- [x] Lifecycle 关键补测
- [x] Docker Desktop daemon 启动后执行 image build / compose up / 重启持久化
- [x] Backend 镜像补拷 `data/`（KPI/Research 静态样例），避免 Compose Task 因缺 CSV 失败

完成记录：PG 278（含 E2E，2 smoke skip）、Frontend 113、build 通过；本轮 Compose 健康验收 + AI Runtime migration + 全量 PG 291/2skip。

最后更新：2026-07-17

## 2026-07-17 Completed: React Lifecycle Live Status

- [x] 集中式 Learning Trace（ring buffer + sessionStorage 安全摘要）
- [x] LifecycleProbe 显式 mount/update/unmount（不解析 Fiber）
- [x] 刷新识别 page_reload；路由 leave/enter
- [x] Learning Dashboard 固定栏目：路由/页面/Live Status/组件树/Hook/Props/事件/State/流程/监视器/源码/测试/调用/StrictMode/教学
- [x] 脱敏与 Frontend 回归

完成记录：Frontend 105/105（原 100 + 新增 lifecycle/sanitize）；production build 通过；未改 Backend。

最后更新：2026-07-17

## 2026-07-17 Completed: Provider Fallback Chain（NVIDIA / Gemini / Local Qwen）

- [x] 固定串行 Chain：OpenRouter → NVIDIA → Gemini → Local Qwen
- [x] Provider Mode：`stub` / `fallback_chain` / `openrouter`（单 Provider 兼容）
- [x] 每 Provider low_cost/high_quality 模型、价格、timeout、enabled fail-closed
- [x] Attempt Ledger（`llm_provider_attempts`）与 Usage 汇总
- [x] Circuit Breaker closed/open/half_open（PostgreSQL 共享状态表）
- [x] Backend 响应：provider/model/route_tier/fallback/attempt/token/cost
- [x] Frontend 显示实际服务/模型/fallback/尝试摘要/Token/Cost
- [x] Migration `20260717_07_fallback_chain`
- [x] 默认零外网；真实 smoke 未执行

完成记录：InMemory Backend 266 tests（51 skipped）、Frontend 100/100、production build、compileall、diff-check 通过。PostgreSQL 本环境不可用，未跑全量 PG 与 migration round-trip。

最后更新：2026-07-17

## 2026-07-17 Completed: OpenRouter Real LLM Provider

- [x] 默认 `LLM_PROVIDER_MODE=stub`；`openrouter` 模式 fail-closed 校验 Key/模型
- [x] 单一 `OpenRouterLLMProvider` 经 Gateway + Model Router 双路由
- [x] Prompt Builder、JSON 校验、usage_source、重试与错误码映射
- [x] MockTransport 单元/集成测试；真实 smoke 仅 opt-in 且默认 skip
- [x] 前端最小展示 Provider/Model/Token/Cost；不暴露 Key

完成记录：不绕过 Gateway/Evidence/Quota/Idempotency/Ledger/Audit；无 Migration；OPENROUTER_API_KEY 未设置时真实 smoke 未执行。

最后更新：2026-07-17

## 2026-07-17 Completed: low_cost / high_quality 双路由

- [x] 统一 LLM Gateway，业务服务不再直接调用 Provider
- [x] Operation Policy + Model Router 集中路由 ai_analysis / executive_report
- [x] 按 route_tier 分离额度桶与 policy/price snapshot
- [x] Executive Report API、门禁、Report/ReportVersion、不自动 Approval
- [x] 前端 AI分析 + 生成取締役会報告 双按钮流程
- [x] Migration `20260717_06_dual_route_llm` 与全量验证

完成记录：PostgreSQL 239 passed；InMemory 182 + 46 skip（含 PostgreSQL-only）；Frontend 95/95；build/compileall/migration/diff-check 通过。仍只使用 Stub，未接真实模型。

最后更新：2026-07-17

## 2026-07-17 Completed: LLM 企业级成本可控边界

- [x] 封死普通 Internal RAG 的隐式 Provider 调用
- [x] 完成 PostgreSQL Ledger / Quota / Idempotency / Result 事实
- [x] 完成显式 AI Analysis API、Evidence Gate、Stub 与 Persistent Audit
- [x] 完成 RAG 页唯一显式入口与回归验证

已发现问题：`INTERNAL_RAG_USE_LLM=true` 可让普通 RAG 路由调用 Provider；现有 Provider Usage 使用 float，且没有额度、幂等与持久 Ledger。

完成记录：已以 Decimal 价格快照、PostgreSQL 唯一约束/行锁、短事务预占/结算、安全 Evidence ref 和唯一显式前端按钮关闭上述问题。

最后更新：2026-07-17

## 2026-07-17 Frontend Enterprise Authentication + RBAC

- [x] 建立 sessionStorage Access Token、JWT 身份校验、`/users/me` 恢复与集中 AuthContext
- [x] 让统一 fetch API Client 自动注入 Bearer，并集中处理 401、403 与并发失效
- [x] 建立 Login、URL 路由、ProtectedRoute、原目标回跳与登出链
- [x] 按冻结 Permission Registry 控制导航、页面入口与业务按钮，未知角色 fail-closed
- [x] 保持 Approval 状态机、后端 RBAC、JWT Payload、Schema、Migration 与 InMemory 不变
- [x] 补齐 Frontend 认证、请求链、路由和权限测试并完成全量回归

### 实施前审计

- 当前 Frontend 没有 Login、AuthContext、URL Router 或 ProtectedRoute，页面只由 `App` 内部 tab state 切换。
- 当前统一使用 `fetch`，但没有 Bearer 注入与 401/403 会话处理；页面无需引入第二套 HTTP Client。
- 当前导航和 Approval/Document/RAG 操作按页面状态静态展示，没有复用后端冻结 Permission Registry。
- 原生 `EventSource` 不能携带 Authorization Header，生产 SSE 请求链需要改为带 Bearer 的 fetch stream。
- 后端现有 Login、CurrentUser 与冻结 RBAC 合同足够，本轮不需要修改后端。

### 完成记录

- 2026-07-17：Login → JWT → `/users/me` → AuthContext → ProtectedRoute 已接通；Access Token 只保存于 sessionStorage。
- 2026-07-17：统一 fetch Client 为受保护 JSON API 和 SSE fetch stream 注入 Bearer；Login/Health 保持匿名。
- 2026-07-17：并发 401 只触发一次清会话/跳转；403 保持当前用户和页面状态并显示无权提示。
- 2026-07-17：admin / manager / employee 前端权限镜像与冻结 Backend Registry 一致，未知角色为空权限集。
- 2026-07-17：Approval 正常 approve/reject 只由 `approval.review` 控制；submit-only owner 通过 Approval ID 请求自己的详情。
- 2026-07-17：Frontend 77/77（原 47 + 新增 30）、InMemory 183（1 skip）、PostgreSQL 194、build、compileall、diff-check 全绿。

## 2026-07-17 Enterprise Approval RBAC Boundary Correction

- [x] 将正常 approve/reject 从 `approval.admin` 修正为 `approval.review`
- [x] 保持 Approval list 为 `approval.review`，detail 改为 reviewer 或 submitter owner
- [x] 保持 `approval.admin` 只承担跨所有者管理能力，不修改冻结角色映射
- [x] 验证 manager/admin、employee owner、非 owner、未知角色与 403 Persistent Audit
- [x] 完成 PostgreSQL、InMemory、Frontend、build、compileall、diff-check 全量验证

### 审计发现

- 新 Enterprise Approval Router 与 Service 把正常 approve/reject 绑定到了 `approval.admin`，权限层级过高。
- detail 仅绑定 `approval.review`，导致只有 `approval.submit` 的 employee owner 无法读取自己的当前状态与 History。
- 冻结注册表中 manager 同时拥有 `approval.review` 与 `approval.admin`，因此旧测试只验证“manager 能执行”，没有验证 endpoint 实际依赖的是哪项权限。
- 注册表描述仍把批准/拒绝写在 `approval.admin` 下；本轮按要求只报告，不修改冻结 Registry 或角色映射。

### 完成记录

- 2026-07-17：正常 approve/reject 的 API Dependency、Persistent Audit permission 与 Service 防御校验统一为 `approval.review`。
- 2026-07-17：detail 使用 reviewer-or-owner 策略；owner 通过 `approval.submit + requested_by` 读取自己的当前状态与 History，list 仍只允许 reviewer。
- 2026-07-17：新增 review-only manager PostgreSQL 测试，显式拒绝 `approval.admin` 后 approve/reject 仍成功。
- 2026-07-17：403 继续只写一条 `authorization.denied`，正常 approval Audit 每个 request_id 只写一条。
- 2026-07-17：InMemory 183（1 skip）、PostgreSQL 194（0 skip）、Frontend 47/47、build、compileall、diff-check 全绿。

## 2026-07-17 ERIP Enterprise Approval Workflow

- [x] 冻结 InMemory Approval，只保持现有回归，不补齐 PostgreSQL 企业审批对等能力
- [x] 让 PostgreSQL Approval 使用 JWT CurrentUser 作为 submitter、reviewer 和 revision actor
- [x] 补齐 rejected → revised → resubmitted → pending_approval 主链与非法转换 409
- [x] 扩展现有 approval_events 为 append-only Approval History，并在详情返回稳定排序历史
- [x] 使用 PostgreSQL 行锁与 partial unique index 防止重复 pending 和并发决策覆盖
- [x] 集中实现 submitter ownership / approval.admin 管理策略，不修改冻结权限矩阵
- [x] 复用既有 Persistent Audit granular actions，不修改 Audit Schema 或基础设施
- [x] 完成 PostgreSQL、InMemory、Frontend、build、compileall、migration round-trip 与 diff-check

### 审计发现

- 当前 actor 仍硬编码为 `system`，Approval Service 未接收 JWT CurrentUser。
- 当前 revise 创建新版本，但没有显式 resubmit API；详情也不返回业务审批历史。
- approve/reject 已有行锁基础，submit 尚缺报告级锁和单一 pending 数据库约束。
- 现有 `approval_events` 可直接扩展为业务历史，无需用 Persistent Audit 代替。

### 完成记录

- 2026-07-17：PostgreSQL 状态机固定为 `generated -> pending_approval -> approved` 或 `pending_approval -> rejected -> revised -> pending_approval`；重复/越级转换返回 409。
- 2026-07-17：初次提交者成为该审批链 owner；后续 revise/resubmit 仅 owner 或拥有 `approval.admin` 的用户可执行，未知角色继续 fail-closed。
- 2026-07-17：revise 生成新 `ReportVersion`，resubmit 复用最新版本；Approval History 与 Persistent Audit 分别保存业务轨迹和安全审计事实。
- 2026-07-17：report/approval 行锁、单任务单 pending partial unique index、同事务 history/audit 写入共同保证并发、幂等和失败回滚。
- 2026-07-17：migration 往返通过；InMemory 183（1 skip）、PostgreSQL 193（0 skip）、Frontend 47/47、build、compileall、diff-check 全绿。
- 2026-07-17：PostgreSQL 首轮全量观察到一次未涉及改动的既有 Internal RAG 用例瞬时 401；定向复跑及最终全量均通过，未修改 RAG 模块。

## 2026-07-16 ERIP PostgreSQL Persistent Audit

- [x] 审计现有 Audit domain、Repository、Service、Router、PostgreSQL schema、写入路径和测试缺口
- [x] 冻结 InMemory Audit，只保持既有回归，不补齐 PostgreSQL 企业审计对等能力
- [x] 扩展 PostgreSQL append-only Audit schema、兼容旧记录并增加必要索引
- [x] 覆盖 login、authorization、document、retrieval、analysis、approval、audit、security 关键事件
- [x] 保证 actor 身份来自 JWT CurrentUser，敏感凭证和文档/RAG 正文不进入 Audit Log
- [x] 补齐 PostgreSQL 过滤、时间范围、分页和稳定倒序查询
- [x] 验证持久化、连接/应用重建、success/failure/denied、403、去重与只读 API
- [x] 完成 PostgreSQL、InMemory、Frontend、build、compileall、diff-check 全量验证

### 完成记录

- 2026-07-16：成功业务与 Persistent Audit 在同一 PostgreSQL 请求事务提交；Service 嵌套事务使用 savepoint。
- 2026-07-16：业务失败先回滚自身 savepoint，再提交必要 failure event 与 failure audit；审计写入失败会使请求失败并回滚成功业务。
- 2026-07-16：Audit API 保持只读，employee 和无 `audit.read` 权限角色继续返回 403；manager/admin 按冻结矩阵读取。
- 2026-07-16：Migration downgrade/re-upgrade 往返通过；InMemory 183（1 skip）、PostgreSQL 191（0 skip）、Frontend 47/47、build、compileall、diff-check 全绿。

## 2026-07-15 ERIP Enterprise RBAC Authorization

- [x] 审计 JWT / CurrentUser、API Route、旧审批域 RBAC 与测试，保留冻结 Authentication Contract
- [x] 建立 Role、Permission、Role Mapping、Authorization Result、Permission Checker 与 403 Error Contract
- [x] 建立集中 Permission Registry、Permission Resolver、Authorization Service 和 `require_permission()` Dependency
- [x] 冻结 admin / manager / employee 三角色与 10 项 API 能力权限，JWT 不携带 permissions
- [x] Documents、Retrieval、Internal RAG、Tasks、Approval、Audit、Security Catalog 全部通过声明式 Dependency 授权
- [x] Health、Login、Swagger/OpenAPI 保持匿名，Current User 接口保持 authentication-only
- [x] 统一权限不足与未知角色的 403 fail-closed 响应和安全结构化日志
- [x] 覆盖 Role Mapping、Resolver、Checker、Dependency、403、Documents、Retrieval、Approval、Audit、Security、匿名入口与 Swagger
- [x] 双 backend 回归完成：InMemory 182（skip 1）、PostgreSQL 187（skip 0）、Frontend 47/47、build、compileall

### 完成记录

- 2026-07-15：授权链固定为 `JWT -> CurrentUser -> Permission Dependency -> AuthorizationService -> API`；业务 Service 不解析 Token、不判断 role。
- 2026-07-15：admin 拥有当前全部权限；manager 不含 `security.manage`；employee 不含 archive/review/admin/audit/security 权限。
- 2026-07-15：权限不足返回 403 `forbidden`，detail 固定包含 `permission` 与 `role`，不携带 `WWW-Authenticate`。
- 2026-07-15：既有审批域 RBAC/审计兼容层保持不变，新 JWT-RBAC 在进入该业务链之前统一授权。
- 2026-07-15：首次 PostgreSQL Baseline 被沙箱阻止本机 socket 访问；授权后按指定命令完整重跑通过，0 skipped。

### 后续 Authorization Hardening（不属于本轮）

- [ ] 将静态 Role Mapping 替换为可治理 Policy Store 或外部 Policy Engine
- [ ] 增加 organization / tenant / resource ownership 等上下文授权，不写入 JWT permission 列表
- [ ] 在未来独立阶段收敛旧审批域 permission 名称与平台 Permission Registry

## 2026-07-15 ERIP Enterprise JWT Authentication

- [x] 审计现有 API / config / services / tests，确认无 JWT、Login、Bearer 或 Token 解析实现
- [x] 冻结 `sub / user_id / username / role / iat / exp / jti` JWT Payload，不写入 permissions
- [x] 建立集中 JWT Config、JWT Provider、JWT Service、Authentication Service 与 CurrentUser Dependency
- [x] 使用 passlib + bcrypt 与预生成 hash 提供 admin / manager / employee deterministic test users
- [x] 建立匿名 Login/Health 边界和统一受保护业务 API Bearer dependency
- [x] 建立 401 Authentication Error / Unauthorized / Token Expired fallback 与安全结构化日志
- [x] 覆盖 password、JWT、expired、invalid signature、missing token、current user、login、protected API、Bearer、Swagger
- [x] 双 backend 回归完成：InMemory 170（skip 1）、PostgreSQL 175（skip 0）、Frontend 47/47、build、compileall

### 完成记录

- 2026-07-15：`POST /api/v1/auth/login` 与 Swagger `BearerAuth` 已落地；Access Token 默认有效期为配置化 30 分钟。
- 2026-07-15：本地默认 JWT secret 仅允许 local/development/test；staging/production 未覆盖时配置校验直接失败。
- 2026-07-15：认证后的 Current User 只暴露 `user_id / username / role`；本轮未把权限判断写入 JWT，也未修改既有 RBAC。
- 2026-07-15：首次 PostgreSQL Baseline 被沙箱阻止本机 socket 访问；授权本机数据库访问后完整重跑通过，0 skipped。

### 后续 Authentication Hardening（不属于本轮）

- [ ] 未来用企业 User Store / IdP 替换 DeterministicTestUserProvider
- [ ] 未来单独设计 Refresh Token、撤销、密钥轮换与多实例 Token 生命周期治理

## 2026-07-14 ERIP Enterprise Reranker

- [x] 冻结独立 reranker contract：query + retrieved chunks -> reranked chunks
- [x] 保留原 chunk content、retrieval score 与 document metadata，独立输出 rerank_score、reason 与 metadata
- [x] 建立 deterministic provider、集中配置、Top-N/Top-K 和稳定 SHA-256 tie-break
- [x] Internal RAG 按 `DocumentRetrievalService -> RerankerService` 编排，Repository 与 retrieval API 不承载 rerank
- [x] disabled、provider 缺失或异常时保留原 retrieval 顺序，不返回 500、不回退 backend
- [x] 双 backend 回归完成：InMemory 154（skip 1）、PostgreSQL 159（skip 0）、Frontend 47/47、build、compileall

### 完成记录

- 2026-07-14：新增 10 个 reranker 单元测试和 3 个 Internal RAG pipeline/fallback API 测试。
- 2026-07-14：完整 Baseline 中观察到既有 Frontend Vitest timeout 随机落在不同用例；独立复跑与最终两轮完整 Baseline 均为 47/47，未修改 Frontend。

## 2026-07-14 ERIP Embedding + pgvector + Vector/Hybrid Retrieval

- [x] 建立固定 384 维 Embedding Contract 与基于 SHA-256 的 deterministic test provider
- [x] 校验空文本、空批次、错误维度、NaN/Infinity 和 Provider 异常
- [x] 扩展同一 Chunk Repository Contract，支持 NULL、写入、更新、读取与 cosine 检索
- [x] 保持默认 `REPOSITORY_BACKEND=inmemory` 与默认 keyword contract，新增 vector/hybrid mode
- [x] Hybrid 完成两路分数归一化、集中权重、chunk_id 去重、稳定 tie-break 与无向量 fallback
- [x] 新增 `20260714_02_chunk_embeddings`：vector extension、`vector(384)`、cosine HNSW；downgrade 保留共享 extension
- [x] 默认完整 Baseline 通过：Backend 140（skip 1）、Frontend 47/47、build、compileall
- [ ] 安装 `postgresql-16-pgvector` 后完成真实 migration 往返与 PostgreSQL skipped=0 回归

### 阻塞记录

- `pg_available_extensions` 中没有 `vector`；`alembic upgrade head` 在 `CREATE EXTENSION` 明确失败并完整回滚。
- 安装后的唯一继续动作：`sudo apt-get update && sudo apt-get install -y postgresql-16-pgvector`，然后只对 `erip_integration_test` 执行 migration 与 PostgreSQL Baseline。

## 2026-07-14 ERIP Enterprise Phase 2B Baseline Gate + Repository Audit

- [x] 检查 Git 工作区状态，确认本轮开始前无未提交修改
- [x] 重新执行统一 Baseline：Backend tests、Frontend tests、Frontend build、Python compileall
- [x] 复核昨天的 4 个 Frontend 超时用例，本轮未复现稳定失败
- [x] 审计 InMemory / PostgreSQL Repository Contract、组合根切换和 Service / API 分层边界
- [x] 明确记录 PostgreSQL integration suite 在无 `DATABASE_URL` 环境下的安全跳过结论
- [x] 记录新发现问题：`src/App.test.tsx` 存在一次性 flaky timeout 迹象，当前未确认真实功能缺陷

### 完成记录

- 2026-07-14：`git status --short`、`git diff --stat` 均为空，分支为 `main`。
- 2026-07-14：第二次执行 `./scripts/run_tests.sh` 全绿；Backend 125 passed（PostgreSQL suite skipped=1）、Frontend 47 passed、Frontend build passed、Python compileall passed。
- 2026-07-14：昨天记录的 4 个 Frontend 超时用例
  `App navigation > uses the document-first enterprise navigation order`
  `ApprovalPage > submits approval successfully and refreshes list plus detail`
  `DocumentsPage > shows empty state when there are no documents`
  `RagPage > shows empty retrieval state from backend`
  本轮完整 Baseline 中均通过，未稳定复现。
- 2026-07-14：本轮新增观察到 `App navigation > explains insufficient_context as a backend evidence result in the learning sidebar` 首次 Baseline 运行出现 1 次 5000ms timeout；单测定向复跑与整份 `src/App.test.tsx` 复跑均通过，当前判断更接近 flaky timeout，而非真实页面功能错误。
- 2026-07-14：真实 PostgreSQL 契约测试 `backend/tests/test_postgres_repositories.py` 因未设置 `DATABASE_URL` 按设计安全跳过；本轮不能宣称 PostgreSQL 重启持久化、事务回滚与 Retrieval 持久化读取已在本机再次执行验证。
- 2026-07-14：当前自动化覆盖已明确保护默认 `REPOSITORY_BACKEND=inmemory`、`REPOSITORY_BACKEND=postgres` 显式启用、连接失败不回退、Repository Bundle 不混用、Service 依赖接口、API 经 Service 访问仓储等架构边界。

### 新发现任务

- [ ] 在具备脱敏 `DATABASE_URL` 的环境中重新执行 `backend/tests/test_postgres_repositories.py`，补做 PostgreSQL 重启持久化、事务回滚和持久化 Chunk 读取验证
- [ ] 继续观察 `frontend/src/App.test.tsx` 的 `insufficient_context` 学习侧栏用例，若再次出现超时，再定向排查异步等待或测试隔离问题
- [ ] 修复 `../doc-sync.manifest.json` 中失效的 handbook 路径映射；当前 `python3 scripts/sync_retail_handbook_docs.py` 会因缺失 `ai-agent-retail-handbook-v3/README.md` 而失败

## 2026-07-13 ERIP Enterprise Phase 2A

- [x] 新增统一临时 PostgreSQL 环境与测试入口的 `scripts/dev_postgres.sh`
- [x] 建立 Alembic 空基线，保留 `schema.sql` 且不生成或执行 migration
- [x] 建立 Embedding Interface、Configuration、Provider 与 Factory，默认禁用执行
- [x] 验证 Backend、InMemory 与 PostgreSQL 既有行为不回归

### 完成记录

- 2026-07-13：Phase 2A 验证完成；未生成 migration、未升级数据库、未生成向量、未访问模型 API。

## 2026-07-13 ERIP Phase 1 Complete PostgreSQL Persistence Bundle

- [x] PostgreSQL 完整覆盖 Task、Report、Event、Document、Chunk、Import、Approval、Audit 与 Upload Session
- [x] PostgreSQL 模式禁止混入 InMemory Repository，连接失败不静默回退
- [x] Task completion、Approval、Document Upload 接入共享事务边界
- [x] InMemory/API/Frontend/Build/compileall 全量验证通过
- [x] 使用隔离的 `DATABASE_URL` 执行真实 PostgreSQL integration suite

### 完成记录

- 2026-07-13：完成 ERIP Phase 1 PostgreSQL Persistence Bundle；未接入 SQLite、Alembic、Docker、pgvector、Embedding 或 LLM。
- 2026-07-13：真实 PostgreSQL Repository、事务回滚与重启持久化验证通过。

## 2026-07-12 Scenario01 Business Sample Data

- [x] 为 ERIP 新增 `docs/learning/sample-data/Scenario01_Sales_Decline/` 企业业务学习样本文档
- [x] 统一 2026 年 6 月关东饮料销售下降场景的销售、库存、促销、顾客、竞品、KPI、RAG、Analysis、Approval 与测试脚本口径
- [x] 保持 Scenario01 背景一致，不扩展 Scenario02
- [x] 完成记录：样本文档可直接用于 Documents 上传、RAG 检索、Analysis 输入、Approval 学习和业务流程测试

## 2026-07-11 API Case Input and Learning Trace Alignment

- [x] 核对学习文档中的 23 个主 Case 与 1 个补充 Case
- [x] 同步 API Case 的 Path / Query / Header / Body / Form / File 输入说明、默认值和约束
- [x] 修正 `GET /api/v1/documents` 的 include_archived、limit、cursor 以及真实 Learning Trace
- [x] 在 `documents.py` 与 `document_read_service.py` 补充 Router / Service / Repository 学习节点
- [x] 保持 API 行为、Repository 查询逻辑、Schema、测试和 Learning Trace 核心框架不变

### 完成记录

- 2026-07-11：完成 API Case 输入参数和文档列表 Learning Trace 对齐；保留工作区中已有的上传相关用户修改。

## 2026-07-08 Learning Request Body Trace

- [x] 在 `TaskService.create_task()` 追加学习日志，终端可直接看到 `request.question`、`request.mode` 和 `task_id`
- [x] 保持 API response、Workflow、Repository 和测试逻辑不变
- [x] 同步更新 `README.md`、`docs/learning/LEARNING_API_WALKTHROUGH.md`、`docs/learning/RUNBOOK_LOCAL.md`、`docs/learning/CODE_STUDY_GUIDE.md` 和 `VERIFY_CHECKLIST.md`
- [x] 完成后验证 `POST /api/tasks` 的终端输出能明确看到 `question: 你好`

### 完成记录

- 2026-07-08：新增学习请求体日志，帮助新手在终端直接确认 `question` 和 `mode` 已进入 `TaskService.create_task()`，未改变 API response、Workflow、Repository 或测试逻辑。

## 2026-07-08 ERIP Worldview Alignment

- [x] 统一项目文档世界观：`Retail Insight AI` 只表示 Current MVP / PoC / Early Prototype
- [x] 统一平台目标命名：`Enterprise Retail Intelligence Platform (ERIP)` 只表示 Target 企业平台
- [x] 统一 `Current / Target / Planned` 标记，禁止把未来能力写成已实现
- [x] 统一术语：`Task API`、`TaskService`、`LangGraph Workflow`、`Fixed KPI Workflow`、`Research Agent`、`Report Generator`、`Repository Pattern`
- [x] 统一平台演进术语：`SQLite(Current)`、`PostgreSQL(Target)`、`pgvector(Target)`、`Hybrid Retrieval(Target)`、`RBAC(Target)`、`Audit Log(Target)`、`OpenTelemetry(Target)`、`Redis(Target)`、`RabbitMQ(Target)`、`Docker(Current)`、`Kubernetes(Target)`
- [x] 逐份检查 Mermaid、Architecture、目录树、API 示例、ADR、Interview Answer、Roadmap 和 handbook 是否保持同一世界观
- [x] Documentation Only：只做术语统一、命名统一、Current/Target/Planned 标记统一，不重写、不扩写、不删章节
- [x] 完成记录：已统一 README、治理文档、架构文档、handbook 总规则、系统设计书、架构图册、生产路线图和面试主文档的 ERIP 世界观

## 2026-07-07 Technical Architecture Handbook Alignment

- [x] `docs/ai-agent-retail-handbook-v3/09_系统设计书.md` 新增 `7.0 Technical Architecture（技术架构总览）`
- [x] `docs/ai-agent-retail-handbook-v3/08_架构图册.md` 追加 Technology Stack Architecture / AI Framework Relationship / Retrieval Pipeline / Technology Evolution Mermaid 图
- [x] 统一 `Keyword Retrieval (Current)`、`Hybrid Retrieval (Target)`、`Vector Database (Target)`、`LangGraph = Workflow Orchestration`、`LangChain = RAG Orchestration`
- [x] 同步 `PROJECT_BIBLE.md` 与 `README.md` 的术语和导航入口
- [x] Documentation Only：未修改 backend、frontend、tests、scripts、API 行为或业务逻辑

## 2026-07-07 API Walkthrough Repair

- [x] 修复 `docs/learning/LEARNING_API_WALKTHROUGH.md` 被截断的问题，恢复 `01~23` 全部接口章节和补充接口章节
- [x] 保持原有接口顺序、Swagger 操作、输入输出、后台日志、程序调用流程不变
- [x] 将错位的“源码学习说明”按接口归位，避免 Health 章节混入 Task / Document / Approval / Security / Audit 内容
- [x] 每个接口仅保留一套源码学习说明，并且只说明该接口 `对应源码` 中的文件
- [x] Documentation Only：未修改 backend、frontend、tests、scripts、API 行为或业务逻辑

## 项目目标

构建 `Enterprise Retail Intelligence Platform (ERIP)` 的目标平台蓝图；当前仓库中的 `Retail Insight AI` 仅表示该目标平台的 Current MVP，包含：

- RAG 知识库检索
- Internal Knowledge Approval Agent
- 多 Agent 协作
- MCP 集成
- 企业权限控制
- AI 分析报告生成

## 2026-07-06 Backend Startup Recovery

- [x] 修复 `backend` 本地启动失败问题，补齐 `python-multipart` 依赖声明和安装步骤
- [x] 用新建 `.venv` 重新安装 backend 依赖，并验证 `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000`
- [x] 确认 `/health`、`/docs`、`/redoc`、`/openapi.json` 可访问
- [x] 在 `docs/learning/RUNBOOK_LOCAL.md` 末尾追加初学者启动顺序与常见错误修复
- [x] 保留原文，不重排、不删除 RUNBOOK_LOCAL 既有内容

## 2026-07-06 Learning Trace Phase 4

- [x] Learning Trace 升级为企业级、源码一眼可读 block，按 `HTTP Request -> Router -> Controller File -> Controller Method -> Return -> Schema File -> Schema -> HTTP Response` 展示
- [x] `backend/app/core/learning_trace.py` 支持按文件切换自动补出 `Controller File`、`Entering File`、`Schema File`、`Schema`
- [x] `GET /health` 与 `POST /api/tasks` 的学习顺序和实际 trace 输出保持一致
- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 同步更新程序调用流程，并修正健康检查 schema 文件名为真实路径 `backend/app/schemas/health.py`
- [x] `LEARNING_TRACE=false` 时仍然不输出新增学习日志
- [x] 本次保持 API 行为、响应 JSON、Swagger/OpenAPI、SSE、Router/Service/Workflow/Provider/Repository 逻辑不变

## 每次工作开始前必须检查

- [ ] 阅读 AGENTS.md
- [ ] 阅读 docs/governance/PROJECT_BACKLOG.md
- [ ] 阅读 TASK.md（如果存在）
- [ ] 检查未完成任务
- [ ] 检查技术债
- [ ] 确认本次要继续的最高优先级任务

## 每次工作完成后必须更新

- [ ] 更新任务状态
- [ ] 将完成项从 [ ] 改为 [x]
- [ ] 更新最后更新时间
- [ ] 追加完成记录
- [ ] 如果发现新任务，追加到 Backlog

## 当前阶段

Documentation Organization + AI Agent Guide 中文化 Sprint

状态：已完成

### Learning Trace Phase 1 结果

- [x] 新增可关闭的 Learning Trace，统一输出学习调用链日志
- [x] 仅覆盖 `GET /health`、`POST /api/tasks`、`GET /api/tasks/{task_id}`、`GET /api/tasks/{task_id}/events`
- [x] `.env.example` 增加 `LEARNING_TRACE=false`
- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 增加 `Learning Trace（学习调用链日志）` 章节
- [x] 保持 API 行为、返回值、Swagger、业务逻辑、测试逻辑不变
- [x] 完成记录：`LEARNING_TRACE=false` 时完全无影响，开启后只输出学习调用链日志，不扩展到其他 API。

### Learning Trace Phase 2

- [x] 学习日志升级为 `HTTP Request -> Router -> Service -> Workflow -> Provider -> Repository -> Schema(Response Model) -> HTTP Response`
- [x] `GET /health` 与 `POST /api/tasks` 补齐更细的学习节点
- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 增加 `Learning Trace Phase 2`
- [x] 默认仍然关闭，`LEARNING_TRACE=false` 时不产生新增学习日志
- [x] 保持 API 行为、返回值、Swagger、OpenAPI、SSE、业务逻辑不变

### Learning Trace Phase 3

- [x] learning trace 由单行 JSON 改为终端可读 block
- [x] `POST /api/tasks` 学习链路支持后台任务完成后统一打印
- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 补充可读格式说明
- [x] `LEARNING_TRACE=false` 时仍然不输出任何学习 trace
- [x] 保持 API 行为、返回值、Swagger、OpenAPI、SSE、业务逻辑不变

### Documentation Organization + AI Agent Guide 中文化 Sprint

- [x] `docs/` 下活动 Markdown 已移动到职责子目录：`learning`、`architecture`、`contracts`、`development`、`database`、`governance`
- [x] `README.md` 已同步新路径、文档树、学习路线和全量 Markdown 导航
- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 保留所有接口、Swagger 操作、输入、预想结果、后台日志、源码、测试、下一步和程序调用流程
- [x] `docs/learning/TEST_CASES.md` 保留所有测试文件详细表和后端程序流程，并在测试总览增加“保护的 Bug / 风险”
- [x] `docs/architecture/AI_AGENT_DESIGN_GUIDE.md` 已中文化，日语为辅，英文仅保留技术名词和代码标识符
- [x] `docs/development/MASTER_PROMPT.md` 增加文档合并、唯一主文档、archive、学习内容保护和语言规则
- [x] Documentation Only：未修改 backend、frontend、scripts、Python、React、API、测试实现、业务逻辑

### Documentation Readability Optimization Sprint

- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 调整为 `主链路接口总览 -> 接口详细表 -> 程序调用流程`
- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 所有主接口均保留 Swagger 操作、输入、输出、后台 Log、源码、测试、下一步
- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 程序流程统一写文件路径、类名、方法名
- [x] `docs/learning/TEST_CASES.md` 调整为 `测试总览 -> 测试详细表 -> 后端程序流程`
- [x] `docs/learning/TEST_CASES.md` 所有测试文件均保留测试目的、API、Swagger 操作、命令、输入、输出、后台 Log、源码、为什么设计
- [x] `docs/learning/TEST_CASES.md` 后端程序流程统一写文件路径、类名、方法名
- [x] Documentation Only：未修改 backend、frontend、scripts、Python、React、API、测试实现、业务逻辑

### Documentation Governance V2

- [x] README 成为唯一知识导航中心，并链接当前仓库全部 59 个 Markdown 文件
- [x] README 补齐知识地图、学习路线流程图、当前完成情况矩阵和四层企业验证体系
- [x] README 增加文档责任表，明确唯一职责和禁止新增同类文档
- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 增加接口学习总表，保留所有接口完整学习章节
- [x] `docs/learning/TEST_CASES.md` 增加测试总览表，保留所有测试文件完整学习章节
- [x] `RUNBOOK_LOCAL.md` 已移动到 `docs/_archive_candidate/RUNBOOK_LOCAL.md`
- [x] handbook/docs 技术规范镜像已移动到 `docs/_archive_candidate/handbook-docs/`
- [x] handbook TASK / ROADMAP 镜像已移动到 `docs/_archive_candidate/handbook-root/`
- [x] `STUDY_PLAN_DAY1_DAY3.md` 已移动到 `docs/_archive_candidate/root/`
- [x] `docs/_archive_candidate/README.md` 明确归档规则、移动原因、停止维护状态和未来删除条件
- [x] `docs/ai-agent-retail-handbook-v3/README.md` 调整为长期知识库入口，主项目介绍统一指向根 README
- [x] `docs/development/MASTER_PROMPT.md` 增加 Documentation Governance 永久规则
- [x] Documentation Only：未修改 backend、frontend、tests、scripts、Python、React

### Documentation Recovery + Governance Sprint

- [x] 重新盘点仓库 Markdown 文档，补充“文档治理清单”
- [x] 恢复 `README.md` 为项目总入口，补齐目录树、导航中心、学习/测试/源码/面试路线
- [x] 恢复 `docs/learning/LEARNING_API_WALKTHROUGH.md` 为分接口学习文档，不再用总表承载主内容
- [x] 恢复 `docs/learning/TEST_CASES.md` 为分测试文件学习文档，不再退化为命令列表
- [x] 补充 `RUNBOOK_LOCAL.md`、`VERIFY_CHECKLIST.md` 的 Swagger / ReDoc / OpenAPI JSON 与 unittest 规则
- [x] 补充 `docs/development/MASTER_PROMPT.md` 的永久文档保护规则
- [x] 补充 `docs/ai-agent-retail-handbook-v3/README.md` 的 handbook 根目录与 handbook/docs 职责边界
- [x] 新增 `docs/_archive_candidate/README.md`，先记录疑似重复文档，不移动、不删除
- [x] 本次只修改 Markdown 文档，不修改 backend/app、backend/tests、frontend、scripts、业务逻辑、API 行为、测试实现

## 文档治理清单

| 文件路径 | 文档用途 | 是否主维护文档 | 是否疑似重复 | 如果重复，建议合并到哪个文件 | 是否建议进入 docs/_archive_candidate/ | 是否需要人工确认 |
|---|---|---|---|---|---|---|
| `README.md` | 项目总入口、导航中心、学习和治理入口 | 是 | 是 | 主文件；与 `docs/ai-agent-retail-handbook-v3/README.md` 分工保留 | 否 | 否 |
| `docs/ai-agent-retail-handbook-v3/README.md` | handbook 学习与面试入口 | 是 | 是 | 主文件；保留 handbook 定位，不合并回根 README | 否 | 否 |
| `TASK.md` | 当前工作结果与阶段记录 | 是 | 是 | 主文件；与 handbook `TASK.md` 保持镜像但不互删 | 否 | 是 |
| `docs/ai-agent-retail-handbook-v3/TASK.md` | handbook 侧任务镜像 | 否 | 是 | 根目录 `TASK.md` | 是 | 是 |
| `ROADMAP.md` | 当前项目阶段路线图 | 是 | 是 | 主文件；与 handbook `ROADMAP.md` 分工保留 | 否 | 是 |
| `docs/ai-agent-retail-handbook-v3/ROADMAP.md` | handbook 侧路线图镜像 | 否 | 是 | 根目录 `ROADMAP.md` | 是 | 是 |
| `docs/governance/PROJECT_BACKLOG.md` | 当前项目 backlog、技术债、治理清单 | 是 | 是 | 主文件；与 handbook mirror 同步但不互删 | 否 | 否 |
| `docs/ai-agent-retail-handbook-v3/docs/governance/PROJECT_BACKLOG.md` | handbook 侧 backlog 镜像 | 否 | 是 | `docs/governance/PROJECT_BACKLOG.md` | 是 | 是 |
| `docs/governance/CHANGELOG.md` | 主项目变更历史 | 是 | 是 | 主文件；与 handbook mirror 同步 | 否 | 否 |
| `docs/ai-agent-retail-handbook-v3/docs/governance/CHANGELOG.md` | handbook 侧变更镜像 | 否 | 是 | `docs/governance/CHANGELOG.md` | 是 | 是 |
| `docs/architecture/ARCHITECTURE.md` | 架构说明与边界 | 是 | 是 | 主文件；与 handbook mirror 同步 | 否 | 否 |
| `docs/ai-agent-retail-handbook-v3/docs/architecture/ARCHITECTURE.md` | handbook 架构镜像 | 否 | 是 | `docs/architecture/ARCHITECTURE.md` | 是 | 是 |
| `docs/contracts/API_CONTRACT.md` | API 合同主文件 | 是 | 是 | 主文件；与 handbook mirror 同步 | 否 | 否 |
| `docs/ai-agent-retail-handbook-v3/docs/contracts/API_CONTRACT.md` | handbook API 合同镜像 | 否 | 是 | `docs/contracts/API_CONTRACT.md` | 是 | 是 |
| `docs/contracts/EVENT_CONTRACT.md` | SSE / 事件合同主文件 | 是 | 是 | 主文件；与 handbook mirror 同步 | 否 | 否 |
| `docs/ai-agent-retail-handbook-v3/docs/contracts/EVENT_CONTRACT.md` | handbook 事件合同镜像 | 否 | 是 | `docs/contracts/EVENT_CONTRACT.md` | 是 | 是 |
| `docs/contracts/ERROR_CATALOG.md` | 错误码主文件 | 是 | 是 | 主文件；与 handbook mirror 同步 | 否 | 否 |
| `docs/ai-agent-retail-handbook-v3/docs/contracts/ERROR_CATALOG.md` | handbook 错误码镜像 | 否 | 是 | `docs/contracts/ERROR_CATALOG.md` | 是 | 是 |
| `docs/learning/LEARNING_API_WALKTHROUGH.md` | 分接口学习主文件 | 是 | 是 | 主文件；handbook 仅引用学习路线，不替代此文档 | 否 | 否 |
| `docs/ai-agent-retail-handbook-v3/06_学习路线.md` | handbook 学习路径文档 | 否 | 是 | 不直接合并；保持入口级路线，引用 `docs/learning/LEARNING_API_WALKTHROUGH.md` | 否 | 是 |
| `docs/learning/TEST_CASES.md` | 分测试文件学习主文件 | 是 | 是 | 主文件；handbook 相关章节只引用，不替代 | 否 | 否 |
| `docs/ai-agent-retail-handbook-v3/07_面试口头训练.md` | 面试口头训练 | 否 | 是 | 不合并；只保留面试训练定位 | 否 | 是 |
| `docs/ai-agent-retail-handbook-v3/11_Project_Structure.md` | handbook 项目结构与测试结构说明 | 否 | 是 | 不合并；保留 handbook 结构视角，并引用 `docs/learning/TEST_CASES.md` | 否 | 是 |
| `CODE_STUDY_GUIDE.md` | 源码阅读路线主文件 | 是 | 是 | 主文件；handbook 结构/学习路线文档只补充，不替代 | 否 | 否 |
| `docs/ai-agent-retail-handbook-v3/11_Project_Structure.md` | handbook 项目结构学习文档 | 否 | 是 | `CODE_STUDY_GUIDE.md` 提供源码阅读入口 | 否 | 是 |
| `docs/_archive_candidate/RUNBOOK_LOCAL.md` | 已停止主维护的旧启动与排错文档 | 否 | 是 | `README.md`、`docs/learning/LEARNING_API_WALKTHROUGH.md`、`docs/learning/TEST_CASES.md`、`VERIFY_CHECKLIST.md` | 已进入 | 是 |
| `docs/_archive_candidate/root/STUDY_PLAN_DAY1_DAY3.md` | 已停止主维护的旧三日学习计划 | 否 | 是 | `README.md`、`docs/learning/LEARNING_API_WALKTHROUGH.md`、`docs/learning/TEST_CASES.md`、`CODE_STUDY_GUIDE.md` | 已进入 | 是 |
| `docs/_archive_candidate/handbook-root/TASK.md` | 已停止主维护的 handbook 任务镜像 | 否 | 是 | `TASK.md` | 已进入 | 是 |
| `docs/_archive_candidate/handbook-root/ROADMAP.md` | 已停止主维护的 handbook 路线图镜像 | 否 | 是 | `ROADMAP.md` | 已进入 | 是 |
| `docs/_archive_candidate/handbook-docs/*.md` | 已停止主维护的 handbook 技术规范镜像 | 否 | 是 | 主项目 `docs/` 同名文档 | 已进入 | 是 |
| `VERIFY_CHECKLIST.md` | 验证清单主文件 | 是 | 否 | 无 | 否 | 否 |
| `docs/development/MASTER_PROMPT.md` | 文档与工程治理总规则 | 是 | 是 | 主文件；handbook 侧为镜像 | 否 | 否 |

### Documentation Restore + Safe Merge Sprint

- [x] 恢复 README 树形目录图、文档导航和企业项目测试体系说明
- [x] 恢复 `docs/learning/LEARNING_API_WALKTHROUGH.md` 的分接口学习章节
- [x] 恢复 `docs/learning/TEST_CASES.md` 的分测试文件流程章节
- [x] 补充 `RUNBOOK_LOCAL.md`、`VERIFY_CHECKLIST.md`、`docs/development/MASTER_PROMPT.md` 的文档规则
- [x] 补充 `docs/ai-agent-retail-handbook-v3/README.md` 的根目录与 `docs` 目录职责说明
- [x] 同步 handbook 镜像侧治理文档
- [x] 本次只改文档，不改 backend、frontend、scripts、业务代码、测试代码

### 文档重构 V1

- [x] `README.md` 已重写为项目门户，补齐项目概览、架构、目录、文档导航和验证系统
- [x] `RUNBOOK_LOCAL.md` 已重写为启动与排错指南，补齐每条命令的原因、结果、失败和验证
- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 已重写为初学者学习文档，补齐 Swagger、当前学习阶段和时序模板
- [x] `docs/learning/TEST_CASES.md` 已重写为学习导向测试文档，补齐 Swagger / unittest 区别、测试保护的 bug 和能力
- [x] `CODE_STUDY_GUIDE.md` 已重写为固定阅读顺序，明确 `Swagger -> API -> Service -> Repository -> Domain -> Tests`
- [x] `docs/ai-agent-retail-handbook-v3/INTERVIEW_GUIDE.md` 继续作为唯一面试文档入口
- [x] 本次仅修改文档，不修改 backend、frontend、scripts、业务逻辑或测试实现

### 文档重构 V3

- [x] `README.md` 已重写为唯一入口，并补齐项目介绍、当前实现范围、目录说明和文档导航中心
- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 已重写为中文主导的接口学习走读，并补齐 Swagger / ReDoc / OpenAPI JSON 说明
- [x] `docs/learning/TEST_CASES.md` 已重写为程序运行流程学习文档，并补齐程序流转和学习日志
- [x] `RUNBOOK_LOCAL.md`、`VERIFY_CHECKLIST.md`、`CODE_STUDY_GUIDE.md` 已重写为面向新手的启动、验证和源码阅读指南
- [x] `docs/ai-agent-retail-handbook-v3/INTERVIEW_GUIDE.md` 已重写为企业 AI 后端项目面试稿
- [x] 仅修改文档，不修改 backend、frontend、scripts、API 行为、业务逻辑、数据库或测试实现
- [x] 删除并收敛旧面试文档引用，统一指向 handbook 唯一入口

### Documentation Consolidation Sprint 2

- [x] README 增加文档导航中心、初学者/面试/开发维护阅读分组和文档数量控制规则
- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 改为主链路接口学习表，补齐下一步和常见失败
- [x] `docs/learning/TEST_CASES.md` 改为测试文件学习表，补齐后端流程和 Swagger/前端流程
- [x] `docs/ai-agent-retail-handbook-v3/INTERVIEW_GUIDE.md` 改为中文主导、日语辅助的日本项目面试稿
- [x] `RUNBOOK_LOCAL.md` 补齐项目根目录脚本与 backend 目录 uvicorn 的区分，以及 Swagger / ReDoc / OpenAPI JSON 用法
- [x] `VERIFY_CHECKLIST.md` 增加失败时先看哪个文档
- [x] `CODE_STUDY_GUIDE.md` 补齐推荐阅读文件和下一步看哪里
- [x] `docs/development/MASTER_PROMPT.md` 增加文档数量控制规则
- [x] 本次仅修改文档，不修改 backend/app、backend/tests、frontend、scripts

### Sprint R3.1: Documentation Quality Refactor

- [x] `README.md` 改为中文入口，并新增“第一次启动项目”章节
- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 按接口顺序重写为中文学习走读
- [x] `docs/learning/TEST_CASES.md` 按测试文件逐个补齐测试目的、对应 API、源码位置、运行命令、输入、预期输出和设计理由
- [x] `RUNBOOK_LOCAL.md` 改写为“启动与排错指南”，使用“问题 → 原因 → 解决方法”组织内容
- [x] `VERIFY_CHECKLIST.md` 改写为启动完成检查清单，并明确每项如何验证成功
- [x] `CODE_STUDY_GUIDE.md` 为每章补齐学习目标、推荐阅读时间、推荐顺序和掌握目标
- [x] 本次仅做文档优化，不修改 Python 代码、测试代码或接口

### Sprint R3: Learning Guide + Test Case + Interview Docs Optimization

- [x] 最短学习路径已收敛到 `README.md` / `docs/learning/LEARNING_API_WALKTHROUGH.md` / `CODE_STUDY_GUIDE.md`
- [x] `README.md` / `RUNBOOK_LOCAL.md` / `VERIFY_CHECKLIST.md` 已补齐启动命令、Swagger 地址、最小验证命令和常见失败原因
- [x] 新增 `docs/learning/TEST_CASES.md`，整理 backend tests 现状、核心路径和 PostgreSQL 相关测试
- [x] 新增 `docs/ai-agent-retail-handbook-v3/INTERVIEW_GUIDE.md`，整理项目背景、架构、职责和面试回答要点
- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 已补充最短路径、文档职责与三语言摘要
- [x] backend tests 与 compileall 继续作为收口检查

### Sprint R2: Runnable Learning MVP Verification

- [x] backend import 验证通过
- [x] OpenAPI / Swagger 验证通过
- [x] 最小可运行路径通过 ASGI 验证
- [x] 新增 `docs/learning/LEARNING_API_WALKTHROUGH.md`
- [x] 更新 README / RUNBOOK / VERIFY / CODE_STUDY / TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG
- [x] 不新增功能，不改 frontend，不接 PostgreSQL，不接真实 LLM，不接 JWT/OAuth，不接 pgvector/MCP

### Final Wrap-up Sprint: Project Consolidation and Verification

- [x] 完成收口整理，不新增功能，不改 frontend，不接 PostgreSQL，不接真实 LLM，不接 JWT / OAuth
- [x] 后端单测与编译检查已通过
- [x] 当前已完成能力、未完成能力和项目边界已用三语摘要记录
- [x] handbook mirror 已同步

### 能力边界

- 英文术语：Document Upload, Document Read, Document Archive, Document Import, Document Chunk, Document Retrieval, Internal RAG without LLM, LLM Provider Stub Seam, Approval Workflow, RBAC for Approval APIs, Approval Audit Middleware, Security Domain, InMemory Audit Log
- 中文（简体）：文档上传、文档读取、文档归档、文档导入、文档切分、文档检索、无 LLM 的内部 RAG、LLM Provider Stub 接缝、审批工作流、审批 API 的 RBAC、审批审计中间件、安全域、InMemory 审计日志
- 日本語：ドキュメントアップロード、ドキュメント読取、ドキュメントアーカイブ、ドキュメントインポート、ドキュメントチャンク、ドキュメント検索、LLM なしの内部 RAG、LLM Provider Stub の接続点、承認ワークフロー、承認 API の RBAC、承認監査ミドルウェア、セキュリティドメイン、InMemory 監査ログ

### 未完成能力

- 英文术语：frontend UI, PostgreSQL repository full migration, real authentication, JWT/OAuth, real LLM provider, pgvector, internet search, MCP, production deployment
- 中文（简体）：前端 UI、PostgreSQL 仓库全面迁移、真实认证、JWT/OAuth、真实 LLM 提供方、pgvector、互联网搜索、MCP、生产部署
- 日本語：frontend UI、PostgreSQL リポジトリの完全移行、実認証、JWT/OAuth、実 LLM provider、pgvector、インターネット検索、MCP、本番デプロイ

### Sprint 11.3: RBAC Enforcement for Approval APIs

- [x] submit-approval / approvals list-detail / approve / reject / revise enforce RBAC via current user seam
- [x] default system admin placeholder user passes all approval checks
- [x] denied approval access writes append-only audit facts
- [x] backend tests added for allow / deny paths and denied audit logging
- [x] docs / roadmap / task / changelog / decisions / architecture / handbook mirror synchronized
- [x] backend / frontend / scripts boundary unchanged
- [x] Human-readable documentation is trilingual: English / 中文（简体） / 日本語

### Sprint 11.2: Security Domain + InMemory Audit MVP

- [x] user / organization / department / role / permission / policy domain models added
- [x] GET /api/v1/users/me implemented with system placeholder principal
- [x] GET /api/v1/security/roles implemented with frozen static role catalog
- [x] GET /api/v1/security/permissions implemented with frozen static permission catalog
- [x] append-only AuditLog model added
- [x] InMemoryAuditRepository added
- [x] GET /api/v1/audit-logs implemented
- [x] audit.log.created / audit.log.failed structured logging recorded on append success/failure
- [x] backend tests added for security read APIs and audit append-only behavior
- [x] backend compileall and unittest discover passed
- [x] docs / roadmap / task / changelog / decisions / architecture updated
- [x] handbook mirror synchronized
- [x] backend / frontend / scripts boundary unchanged
- [x] Human-readable documentation is trilingual: English / 中文（简体） / 日本語

### Sprint 11.1: Enterprise Security Foundation Contract Freeze

- [x] user / organization / department / role / permission / policy concepts frozen
- [x] GET /api/v1/users/me contract frozen
- [x] GET /api/v1/security/roles contract frozen
- [x] GET /api/v1/security/permissions contract frozen
- [x] GET /api/v1/audit-logs contract frozen
- [x] RBAC approval-action matrix frozen
- [x] audit log contract and operation log contract frozen
- [x] future authentication relationship documented
- [x] docs and handbook mirror synchronized
- [x] backend / frontend / scripts boundary unchanged
- [x] Human-readable documentation is trilingual: English / 中文（简体） / 日本語

### Sprint 10.2: Approval API MVP Implementation

- [x] POST /api/v1/reports/{task_id}/submit-approval implemented
- [x] GET /api/v1/approvals implemented
- [x] GET /api/v1/approvals/{approval_id} implemented
- [x] POST /api/v1/approvals/{approval_id}/approve implemented
- [x] POST /api/v1/approvals/{approval_id}/reject implemented
- [x] POST /api/v1/reports/{task_id}/revise implemented
- [x] immutable report version snapshot model added
- [x] ApprovalRequest / ApprovalEvent domain models added
- [x] InMemory approval repository added
- [x] approval events emitted and backend tests added
- [x] docs and handbook mirror synchronized
- [x] backend / frontend / scripts boundary unchanged
- [x] Human-readable documentation is trilingual: English / 中文（简体） / 日本語

### Sprint 10.1: Approval Workflow Contract Freeze

- [x] approval domain model frozen
- [x] approval API contract frozen
- [x] approval event contract frozen
- [x] approval error catalog frozen
- [x] approval state transition rules frozen
- [x] report revision relationship / audit relationship / future RBAC relationship documented
- [x] docs and handbook mirror synchronized
- [x] backend / frontend / scripts boundary unchanged
- [x] Human-readable documentation is trilingual: English / 中文（简体） / 日本語

### Sprint 9.5: LLM Provider Seam Stub MVP

- [x] `StubLLMProvider` added as the local no-external-API provider implementation
- [x] `RAGAnswerGenerator` now routes through an optional provider seam
- [x] `LLM_PROVIDER=stub` and `INTERNAL_RAG_USE_LLM=false` defaults added
- [x] provider failure / timeout / invalid output fallback to deterministic answer
- [x] usage / cost / latency placeholder model recorded internally
- [x] default deterministic path remains unchanged
- [x] backend tests added for default path, stub path, fallback, invalid output, and usage placeholders
- [x] backend full suite and compileall pass
- [x] TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS / handbook mirror synchronized
- [x] backend / frontend / scripts boundary unchanged

### Sprint 9.4: LLM Provider Seam Contract Freeze

- [x] `LLMProvider` interface concept frozen
- [x] `RAGAnswerGenerator` concept frozen
- [x] prompt input/output contract frozen for future model-backed answers
- [x] provider error model frozen for unavailable / timeout / invalid output / citation missing / cost limit cases
- [x] deterministic extractive fallback remains the current default
- [x] token / cost / latency tracking placeholders documented
- [x] `docs/development/PROMPT_STANDARD.md` / `docs/architecture/AI_AGENT_DESIGN_GUIDE.md` / `docs/architecture/ARCHITECTURE.md` / `docs/contracts/ERROR_CATALOG.md` updated
- [x] TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS / handbook mirror synchronized
- [x] backend / frontend / scripts left untouched

## Epic 0: Enterprise Platform Architecture Evolution

### Current State

当前项目名称保持为 `Retail Insight AI`，它是 `Enterprise Retail Intelligence Platform (ERIP)` 的 Current MVP；项目仍是零售分析领域参考实现，平台级抽象尚未冻结。

### Target State

未来目标平台名称：

`Enterprise Retail Intelligence Platform (ERIP)`

ERIP 仅表示目标平台架构，不表示当前项目、当前部署或当前目录已经完成平台化。

### Planned Tasks

- [x] Sprint 10.2 Approval API MVP Implementation
- [x] Sprint 10.1 Approval Workflow Contract Freeze
- [ ] Human-readable documentation is trilingual: English / 中文（简体） / 日本語
- [ ] Architecture Freeze
- [ ] Directory Refactor
- [ ] Repository Abstraction
- [ ] Workflow Abstraction
- [ ] Provider Abstraction
- [ ] Documentation Standard
- [ ] Testing Standard

### Epic 14: Engineering Standards (Final Freeze)

- [x] 冻结唯一 Master Prompt
- [x] 冻结 API Contract
- [x] 冻结 SSE Event Contract
- [x] 冻结 Prompt Standard
- [x] 冻结 Coding Standard
- [x] 冻结 Development Guide
- [x] 冻结 AI Agent Design Guide
- [x] 建立 handbook 镜像文档
- [x] 扩展文档同步清单
- [ ] 后续 Phase 在新增能力时按冻结文档执行一致性审查
- [ ] Human-readable documentation is trilingual: English / 中文（简体） / 日本語

### Epic 0 Deliverables

- [ ] Architecture Freeze
- [ ] Directory Freeze
- [ ] Repository Freeze
- [ ] Provider Freeze
- [ ] Workflow Freeze
- [ ] Database Freeze
- [ ] Testing Freeze
- [ ] Documentation Freeze

### Sprint 1: Phase 3.1 Document Domain Model

- [x] Document / DocumentVersion / DocumentChunk placeholder / DocumentMetadata / DocumentSource
- [x] DocumentStatus / DocumentType / Language / ApprovalStatus reuse
- [x] DocumentRepository Interface
- [x] InMemoryDocumentRepository
- [x] Document creation / metadata validation / status transition / CRUD / checksum duplicate tests
- [x] Architecture / Roadmap / TASK / CHANGELOG / DECISIONS / handbook mirror sync
- [ ] Document Upload API design only, no implementation yet
- [ ] PostgreSQL Document Repository design only, no implementation yet
- [ ] RAG pipeline design based on the frozen document domain model

## 工作区规则继承

本项目继承 ai-lab 全局项目管理规则。

每次开发前必须检查：

- AGENTS.md
- docs/governance/PROJECT_BACKLOG.md
- TASK.md

每次开发后必须更新：

- docs/governance/PROJECT_BACKLOG.md
- TASK.md
- docs/governance/CHANGELOG.md

### Sprint 4: Document Read API MVP

- [x] GET /api/v1/documents implemented
- [x] GET /api/v1/documents/{document_id} implemented
- [x] basic list filters implemented for status / document_type / language / tag / owner
- [x] document_not_found 404 behavior implemented for missing documents
- [x] backend tests added for empty list, upload then list, upload then get, missing document, and filters
- [x] existing upload tests still pass
- [x] Architecture / Task / Roadmap / Backlog / Changelog / Decisions / handbook mirror sync
- [ ] PostgreSQL Document Repository remains design-only
- [ ] DELETE / versions / chunks remain frozen for later phases

### Sprint 5: Document Archive API MVP

- [x] DELETE /api/v1/documents/{document_id} implemented as archive / soft delete
- [x] archived documents remain readable by GET /api/v1/documents/{document_id}
- [x] list default excludes archived unless include_archived=true or status=archived
- [x] backend tests added for archive success, archive missing, archive idempotency, and archived list visibility
- [x] existing upload/read tests still pass
- [x] Architecture / Task / Roadmap / Backlog / Changelog / Decisions / handbook mirror sync
- [ ] PostgreSQL Document Repository remains design-only
- [ ] versions / chunks remain frozen for later phases

### Sprint 6: Document Import Pipeline MVP

- [x] POST /api/v1/documents/{document_id}/import implemented
- [x] GET /api/v1/document-imports/{import_id} implemented
- [x] import status transitions pending / running / completed / failed implemented
- [x] successful import marks document as validated
- [x] backend tests added for markdown/text success, unsupported PDF failure, missing document, archived document, deterministic repeat, status read, and event recording
- [x] existing upload/read/archive tests still pass
- [x] Architecture / Task / Roadmap / Backlog / Changelog / Decisions / handbook mirror sync
- [ ] PostgreSQL Document Repository remains design-only
- [ ] versions / chunks / RAG / embedding / pgvector remain frozen for later phases

### Sprint 7: Document Chunk Pipeline MVP

- [x] POST /api/v1/documents/{document_id}/chunks implemented
- [x] GET /api/v1/documents/{document_id}/chunks implemented
- [x] chunk pipeline requires validated documents and rejects archived / unvalidated / unsupported types
- [x] deterministic replace rule implemented for repeated chunking
- [x] backend tests added for markdown/text success, pre-import rejection, archived rejection, unsupported PDF rejection, stored chunk reads, deterministic repeat, and event recording
- [x] existing upload/read/archive/import tests still pass
- [x] Architecture / Task / Roadmap / Backlog / Changelog / Decisions / handbook mirror sync
- [ ] PostgreSQL Document Repository remains design-only
- [ ] versions / RAG / embedding / pgvector / Approval API remain frozen for later phases

### Sprint 8.1: Document Retrieval Contract Freeze

- [x] POST /api/v1/document-retrieval/search contract frozen
- [x] document.retrieval.started / completed / failed contract frozen
- [x] invalid_query / retrieval_unavailable / repository_error frozen in Error Catalog
- [x] Document Retrieval Flow / Source Trace Flow / Future RAG Integration Flow added to Architecture
- [x] TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS / handbook mirror sync
- [ ] Retrieval implementation remains pending
- [ ] RAG / embedding / pgvector / hybrid search remain frozen for later phases

### Sprint 8.2: Document Retrieval API MVP Implementation

- [x] POST /api/v1/document-retrieval/search implemented
- [x] keyword-only search over existing in-memory document chunks implemented
- [x] empty query returns invalid_query
- [x] archived documents are excluded unless include_archived=true
- [x] deterministic score ordering implemented
- [x] retrieval events started / completed / failed emitted
- [x] backend tests added for success, no match, empty query, archived exclusion, include_archived, and deterministic ordering
- [x] existing upload/read/archive/import/chunk tests still pass
- [x] Architecture / Task / Roadmap / Backlog / Changelog / Decisions / handbook mirror sync
- [x] frozen contract remains unchanged

### Sprint 8.3: Retrieval Repository Abstraction + Worktree Cleanup

- [x] `DocumentRetrievalService` depends on `DocumentRetrievalProvider`
- [x] `InMemoryKeywordRetrieval` keeps current keyword scoring and ordering behavior
- [x] POST /api/v1/document-retrieval/search response shape unchanged
- [x] `git status` confirmed no untracked chunk files
- [x] current retrieval boundary documented in Architecture / Decisions / Changelog / Task
- [x] existing retrieval tests remain expected to pass after abstraction change
- [ ] future PostgreSQL full-text / hybrid search backend remains to be planned

### Sprint 9.1: Internal RAG Contract Freeze

- [x] `POST /api/v1/internal-rag/answer` contract frozen
- [x] `internal_rag.started` / `internal_rag.retrieval_completed` / `internal_rag.answer_generated` / `internal_rag.failed` frozen
- [x] `invalid_question` / `retrieval_unavailable` / `insufficient_context` / `citation_required` / `provider_timeout` / `repository_error` frozen
- [x] Internal RAG Flow / Retrieval to Citation Flow / Future LLM Provider Flow / Future Approval Integration Flow added to Architecture
- [x] Prompt Standard updated with Internal RAG prompt family
- [x] TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS / handbook mirror updated
- [x] retrieval API behavior unchanged

### Sprint 9.3: Internal RAG Evaluation + Citation Quality MVP

- [x] citation quality checker validates document_id / chunk_id / grounded excerpt
- [x] internal RAG evaluation service computes coverage_score / citation_score / confidence / warnings
- [x] low_context / missing_citation / weak_match warnings are generated internally
- [x] extractive answer has citation_score=1.0 on grounded paths
- [x] summary mode still returns citations
- [x] archived filtering and retrieval API behavior remain unchanged
- [x] backend tests added for evaluation scores, missing citation warning, weak_match, and low_context
- [x] existing retrieval and internal RAG tests still pass
- [x] backend full test suite and compileall pass
- [x] TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS / handbook mirror synchronized
- [x] retrieval API behavior remains unchanged

### Sprint 9.2: Internal RAG MVP without LLM

- [x] `POST /api/v1/internal-rag/answer` implemented on top of `DocumentRetrievalProvider`
- [x] extractive answer assembly uses top retrieval excerpts
- [x] summary mode stays deterministic and does not call an LLM
- [x] citations are returned for every excerpt used in the answer
- [x] `invalid_question` / `insufficient_context` / `citation_required` behavior covered by backend tests
- [x] archived documents are excluded unless `include_archived=true`
- [x] existing retrieval tests still pass
- [x] backend full test suite and compileall pass
- [x] TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS / handbook mirror synchronized
- [x] retrieval API behavior remains unchanged

## 当前近期优先级

### Enterprise Priority

- [x] Sprint 9.5 LLM Provider Seam Stub MVP
- [x] Sprint 9.4 LLM Provider Seam Contract Freeze
- [x] Sprint 9.3 Internal RAG Evaluation + Citation Quality MVP
- [x] Sprint 9.2 Internal RAG MVP without LLM
- [x] Sprint 9.1 Internal RAG Contract Freeze
- [x] Sprint 8.3 Retrieval Repository Abstraction + Worktree Cleanup
- [x] Sprint 8.2 Document Retrieval API MVP Implementation
- [x] Sprint 8.1 Document Retrieval Contract Freeze
- [ ] 第一优先级：文件化输入（CSV / JSON / Markdown）+ PostgreSQL 持久化基础
- [ ] 明确文件输入目录结构、样例数据规范、版本字段与加载边界
- [ ] 明确 PostgreSQL 持久化表结构、迁移方案与 Repository 替换策略
- [ ] 明确本地最小可行运行方案，不依赖真实外部服务
- [ ] 明确 Phase 完成后的 handbook 文档同步清单与验收标准
- [ ] 明确 Retail Insight AI 与 ERIP 的 Current / Target / Planned 定位边界
- [ ] 明确 Retrieval and RAG Platform 的横向能力边界

### P0

- [ ] 确认项目目录结构
- [ ] 确认 Docker 环境
- [ ] 确认 .gitignore 敏感文件保护
- [ ] 确认 Document Upload 流程

### P1

- [ ] Chunk Strategy 设计
- [ ] Chunk Size 配置化
- [ ] Overlap 配置化
- [ ] Chunk 可视化调试页面

### P2

- [ ] Embedding Pipeline
- [ ] Vector Search
- [ ] Approval Agent

说明：

- Embedding Pipeline / Vector Search 的详细拆解已并入 `Epic 13: Semantic RAG / Vector Retrieval Upgrade`，这里保留为当前优先级视图，不再单独拆出新的平行任务池。

## Backlog

### Epic 1: 项目基础架构

- [ ] 确认 monorepo 结构
- [ ] 确认 frontend/backend 目录
- [ ] 确认 Docker 环境
- [ ] 确认 .gitignore 是否保护敏感文件

### Epic 2: Internal Knowledge Approval Agent

- [ ] Document Upload 流程确认
- [ ] Chunk Strategy 设计
- [ ] Chunk Size 配置化
- [ ] Overlap 配置化
- [ ] Chunk 可视化调试页面
- [ ] Chunk 单元测试
- [ ] Embedding Service 设计
- [ ] Vector Search 设计
- [ ] Approval Agent 设计
- [ ] 审批日志设计

### Epic 3: RAG Platform

- [ ] Query Rewrite
- [ ] Hybrid Search
- [ ] Rerank
- [ ] Context Builder
- [ ] Citation 支持

### Epic 4: Multi-Agent

- [ ] Research Agent
- [ ] Knowledge Agent
- [ ] Approval Agent
- [ ] Report Agent
- [ ] Supervisor Agent

### Epic 5: MCP Integration

- [ ] MCP Server
- [ ] MCP Client
- [ ] Tool Registry
- [ ] Permission Layer

### Epic 6: Enterprise Security

- [x] Enterprise Security Foundation Contract Freeze
- [ ] RBAC
- [ ] JWT
- [ ] Audit Log
- [ ] Tenant Isolation

### Epic 7: Observability

- [ ] LangSmith / Langfuse 调研
- [ ] OpenTelemetry
- [ ] Metrics Dashboard
- [ ] Cost Tracking

### Epic 8: Enterprise Delivery Plan

- [x] Phase 1 文件化输入基础
- [x] Phase 1.5 Data Contract Freeze + Approval State Machine Design
- [x] Phase 1.6 Enterprise Security Foundation Contract Freeze
- [ ] Phase 2 PostgreSQL 持久化基础
- [ ] Phase 3 社内文档上传与入库
- [ ] Phase 4 切分与检索基础
- [ ] Phase 5 审批 Workflow
- [ ] Phase 6 互联网检索能力
- [ ] Phase 7 LangChain + LangGraph 工作流整合
- [ ] Phase 8 测试体系与流程图文档

### Epic 12: Retrieval and RAG Platform

说明：

当前将 Epic 12 作为横向平台能力，不表示当前已经实现完整 RAG 平台。

- [ ] Business Data Retrieval
- [ ] SQL-based structured retrieval
- [ ] Internal Document Retrieval
- [ ] Internal RAG MVP
- [ ] Document chunk retrieval
- [ ] PostgreSQL keyword search
- [ ] PostgreSQL full-text search planning
- [ ] pgvector planning
- [ ] Hybrid search planning
- [ ] Internet Search Retrieval
- [ ] Retrieval provider interface
- [ ] Context merge strategy
- [ ] Source citation model
- [ ] Reference tracking
- [ ] Hallucination risk control
- [ ] Retrieval evaluation
- [ ] Handbook 文档已同步

### Epic 13: Semantic RAG / Vector Retrieval Upgrade

说明：

Epic 13 负责把语义检索、向量库、LangChain 编排与评估体系收束到一个可执行主线，避免与 Epic 12 / Epic 3 重复。

#### Current State

- 当前 Document Upload / Import / Chunk 已有基础能力。
- 当前检索以 Keyword Retrieval 为主。
- 当前 Repository 默认 InMemory。
- 当前没有真正 Embedding。
- 当前没有真正 Vector Database。
- 当前没有 LangChain RAG 编排。

#### Target State

- 支持 Embedding。
- 支持 Vector Database。
- 支持 Hybrid Search（Keyword + Vector）。
- 支持 LangChain Retriever / Chain 编排。
- 支持 Rerank。
- 支持 Citation。
- 支持 Retrieval Evaluation。
- 支持 PostgreSQL + pgvector 企业化演进。

#### Planned Tasks

- [ ] 设计 Embedding Provider 接口
  - [ ] OpenAI Embedding
  - [ ] Gemini Embedding
  - [ ] BGE / 本地 Embedding
  - [ ] Provider fallback
  - [ ] 配置项通过 `.env` 控制
- [ ] 设计 Vector Store 接口
  - [ ] pgvector 优先
  - [ ] Qdrant / Milvus 作为未来扩展
  - [ ] 业务代码不直接绑定具体向量库
- [ ] 引入 LangChain
  - [ ] 仅用于 RAG 编排
  - [ ] 不替代 LangGraph
  - [ ] 定义 LangChain 与 TaskService / LangGraph 的边界
  - [ ] 定义 Retriever、Prompt、Context Builder 的职责
- [ ] Document Chunk Metadata 升级
  - [ ] `document_id`
  - [ ] `chunk_id`
  - [ ] `version`
  - [ ] `section`
  - [ ] `language`
  - [ ] `document_type`
  - [ ] `owner`
  - [ ] `tags`
  - [ ] `created_at`
  - [ ] `checksum`
  - [ ] `acl_scope`
- [ ] Embedding Pipeline
  - [ ] chunk -> embedding
  - [ ] embedding cache
  - [ ] re-embedding policy
  - [ ] document update 后重建 embedding
  - [ ] archived document 的向量处理策略
- [ ] Hybrid Retrieval
  - [ ] Keyword Search
  - [ ] Vector Search
  - [ ] Metadata Filter
  - [ ] ACL Filter
  - [ ] Score Merge
  - [ ] Top-K
- [ ] Rerank
  - [ ] Cross Encoder / LLM rerank 作为未来目标
  - [ ] 当前先设计接口和测试边界
- [ ] Citation / Source Trace
  - [ ] answer 必须引用 `document_id` / `chunk_id` / `version`
  - [ ] 报告中保留 source trace
  - [ ] 与 Audit Log 未来集成
- [ ] Retrieval Evaluation
  - [ ] `recall@k`
  - [ ] `MRR`
  - [ ] groundedness
  - [ ] citation accuracy
  - [ ] no-result rate
  - [ ] latency
- [ ] Tests
  - [ ] unit test
  - [ ] retrieval test
  - [ ] embedding mock test
  - [ ] vector store contract test
  - [ ] LangChain integration boundary test
- [ ] Documentation
  - [ ] 更新 `09_系统设计书.md`
  - [ ] 更新 `08_架构图册.md`
  - [ ] 更新 `LEARNING_API_WALKTHROUGH.md`
  - [ ] 更新 `DATABASE.md`，如涉及 pgvector schema
  - [ ] 更新 `README.md` 的能力矩阵，标记为 Planned

#### Design Notes

- Keyword Retrieval 偏向词面匹配与既有 chunk 命中，适合当前本地学习版和快速回归；Semantic Retrieval 通过 embedding 捕获语义相似、同义表达和改写问题。
- LangChain 只作为 RAG 编排层，用来组织 Retriever、Prompt 和 Context Builder，不接管 Workflow 状态机。
- LangGraph 继续负责 Workflow / State Machine，因为它更适合表达任务流转、重试、分支与状态持久化。
- pgvector 是第一优先，因为它最贴近当前 PostgreSQL-first 演进路径，能把向量、元数据和业务事实放在同一套数据库治理中；后续再通过同一 Vector Store 接口扩展到 Qdrant / Milvus。

## Phase 1 到 Phase 8 详细计划

### Phase 1.5: Data Contract Freeze + Approval State Machine Design

- 状态：已完成文档冻结。
- 本次完成：
  - [x] 冻结业务 CSV 字段契约
  - [x] 冻结 Research JSON 字段契约
  - [x] 冻结 Documents Markdown 当前边界与未来导入规则
  - [x] 冻结导入错误模型
  - [x] 冻结 Approval State Machine
  - [x] 冻结 Phase 2 PostgreSQL 准备项
- 后续待办：
  - [ ] 将导入错误模型映射到真实 Repository
  - [ ] 将审批状态机映射到真实 API / Repository / Event
  - [ ] 将数据契约映射到 PostgreSQL schema version 策略

### Sprint 2: Document Upload API Contract Freeze

- 状态：已完成文档冻结。
- 本次完成：
  - [x] 冻结 `POST /api/v1/documents`、`GET /api/v1/documents`、`GET /api/v1/documents/{document_id}`、`GET /api/v1/documents/{document_id}/versions`、`GET /api/v1/documents/{document_id}/chunks`、`DELETE /api/v1/documents/{document_id}`
  - [x] 冻结 `document.upload.started`、`document.upload.validated`、`document.upload.completed`、`document.upload.failed`、`document.version.created`、`document.validation.failed`
  - [x] 冻结 Document Upload Validation Flow 与 Future Approval Integration Flow
  - [x] 同步 `TASK.md`、`ROADMAP.md`、`docs/architecture/ARCHITECTURE.md`、`docs/database/DATABASE.md`、`docs/governance/CHANGELOG.md`、`docs/governance/DECISIONS.md` 以及 handbook mirror
- 后续待办：
  - [ ] 实现 Upload API
  - [ ] 实现 Document Upload persistence
  - [ ] 补齐 Upload API integration tests

### Sprint 2.5: Document Upload Workflow + Error Catalog + Upload Policy Freeze

- 状态：已完成文档冻结。
- 本次完成：
  - [x] 冻结 Document Upload Workflow
  - [x] 冻结 Upload Session contract
  - [x] 冻结 Idempotency contract
  - [x] 新增 `docs/contracts/ERROR_CATALOG.md`
  - [x] 新增 `docs/contracts/UPLOAD_POLICY.md`
  - [x] 同步 `TASK.md`、`ROADMAP.md`、`docs/architecture/ARCHITECTURE.md`、`docs/database/DATABASE.md`、`docs/governance/CHANGELOG.md`、`docs/governance/DECISIONS.md` 以及 handbook mirror
- 后续待办：
  - [ ] 实现 Upload API
  - [ ] 实现 Upload Session persistence
  - [ ] 实现 Upload API integration tests

### Sprint 3: Document Upload API MVP

- 状态：已实现并待验证。
- 本次完成：
  - [x] 实现 `POST /api/v1/documents`
  - [x] 实现 multipart/form-data 请求处理
  - [x] 实现 title / description / owner / tags / language 校验
  - [x] 实现 SHA-256 checksum、duplicate checksum detection、Idempotency-Key 处理
  - [x] 实现 `DocumentUploadSession` 成功响应
  - [x] 实现 upload 事件发布到现有 event repository
  - [x] 新增 backend 单元测试覆盖成功、空文件、类型不支持、缺少标题、重复 checksum、幂等重放与幂等冲突
  - [x] 同步 `TASK.md`、`ROADMAP.md`、`docs/architecture/ARCHITECTURE.md`、`docs/contracts/API_CONTRACT.md`、`docs/contracts/EVENT_CONTRACT.md`、`docs/governance/CHANGELOG.md`、`docs/governance/DECISIONS.md` 以及 handbook mirror
- 后续待办：
  - [ ] 实现 GET / DELETE / versions / chunks 只读接口
  - [ ] 保持 PostgreSQL Document Repository 仅设计不实现
  - [ ] 补齐 Upload API integration tests 的真实联调验证

### Sprint 4: Document Read API MVP

- 状态：已实现并待验证。
- 本次完成：
  - [x] 实现 `GET /api/v1/documents`
  - [x] 实现 `GET /api/v1/documents/{document_id}`
  - [x] 实现 status / document_type / language / tag / owner 过滤
  - [x] 实现 `document_not_found` 404 行为
  - [x] 新增 backend 单元测试覆盖空列表、上传后列表、上传后读取、缺失文档和过滤条件
  - [x] existing upload tests still pass
  - [x] 同步 `TASK.md`、`ROADMAP.md`、`docs/architecture/ARCHITECTURE.md`、`docs/governance/CHANGELOG.md`、`docs/governance/DECISIONS.md` 以及 handbook mirror
- 后续待办：
  - [ ] `DELETE`、`versions`、`chunks` 接口仍冻结未实现
  - [ ] PostgreSQL Document Repository 仍保持设计不实现

### Phase 2: PostgreSQL Persistence MVP

- 状态：In Progress / Partially Verified。
- 本次完成：
  - [x] Code implemented
  - [x] InMemory path verified
  - [x] PostgreSQL schema implemented
  - [x] PostgreSQL repository tests prepared
  - [x] PostgreSQL verification script added
  - [x] 新增 `REPOSITORY_BACKEND=inmemory|postgres` 配置开关，默认仍为 `inmemory`
  - [x] 新增 PostgreSQL 连接工厂与 UTC 会话设置
  - [x] 新增 `tasks`、`task_events`、`reports`、`report_versions` 表
  - [x] 新增 `data_imports`、`import_errors` schema 预留
  - [x] 新增 `approval_requests`、`approval_events` schema 预留
  - [x] 新增 PostgreSQL Repository 与 backend switch 测试
  - [x] 新增 `scripts/verify_postgres_phase2.sh`，统一输出依赖检查、跳过原因与手动验证命令
  - [x] 同步主项目与 handbook 文档
- 后续待办：
  - [ ] PostgreSQL real integration test pending
  - [ ] 在具备 PostgreSQL 环境后执行真实集成测试
  - [x] 记录当前环境缺少 Docker CLI、未安装 `psycopg` 到实际运行 venv、测试被 skip 的验证边界
  - [ ] 在具备同级 `ai-agent-retail-handbook-v3/` 工作区后执行 `python3 ../scripts/sync_retail_handbook_docs.py`
  - [ ] 实现 data imports / import errors Repository
  - [ ] 将 reports approval status 接入真实审批状态流转
  - [ ] 为 Phase 3 文档入库与 Phase 5 审批 API 复用当前 schema

## Handbook 同步治理规则

- 每个 Phase 完成后，必须同步更新 `docs/ai-agent-retail-handbook-v3/` 对应文档。
- handbook 同步最小集合：
  `TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/architecture/ARCHITECTURE.md`、`docs/governance/CHANGELOG.md`、`docs/governance/DECISIONS.md`。
- 若变更涉及测试、流程、系统设计、生产路线图，还必须同步检查并更新：
  `08_架构图册.md`、`09_系统设计书.md`、`10_Production_Roadmap.md`。
- 未同步 handbook 文档的 Phase 不得从 `[ ]` 改为 `[x]`。
- 所有功能变更必须追加到 handbook 侧：
  `docs/ai-agent-retail-handbook-v3/docs/governance/CHANGELOG.md`
  `docs/ai-agent-retail-handbook-v3/docs/governance/DECISIONS.md`

## 本次完成记录

### 2026-07-04

- 完成 Epic 14：Engineering Standards（Final Freeze）文档冻结。
- 新增 Master Prompt、API / Event Contract、Prompt Standard、Coding Standard、Development Guide、AI Agent Design Guide。
- 在 `docs/ai-agent-retail-handbook-v3/docs/` 建立对应镜像。
- 将 `../doc-sync.manifest.json` 扩展为包含 `engineering-standards` 同步组。
- 未修改 `backend/`、`frontend/`、`scripts/`。

### 2026-07-04 Sprint 1 Phase 3.1 Document Domain Model

- [x] 完成文档域模型、仓储接口、InMemory 仓储、验证与单元测试
- [x] 完成主项目与 handbook 的架构、路线图、任务、Backlog、Changelog、决策同步
- [ ] Upload API / RAG / pgvector / PostgreSQL Repository 留待后续 Sprint

### 2026-07-04 Sprint 8.1 Document Retrieval Contract Freeze

- [x] 冻结 `POST /api/v1/document-retrieval/search`
- [x] 冻结 `document.retrieval.started`、`document.retrieval.completed`、`document.retrieval.failed`
- [x] 冻结 `invalid_query`、`retrieval_unavailable`、`repository_error`
- [x] 新增 Document Retrieval Flow、Source Trace Flow、Future RAG Integration Flow
- [x] 完成主项目与 handbook 的任务、路线图、Backlog、Changelog、决策同步
- [ ] Retrieval implementation / RAG / embedding / pgvector / hybrid search 留待后续 Sprint

### 2026-07-04 Sprint 8.2 Document Retrieval API MVP Implementation

- [x] 实现 `POST /api/v1/document-retrieval/search`
- [x] 仅对现有 in-memory document chunks 做 keyword search
- [x] 实现 empty query / no match / archived exclusion / include_archived / deterministic ordering 测试
- [x] 保持 frozen contract 不变
- [x] 完成主项目与 handbook 的任务、路线图、Backlog、Changelog、决策同步

### 2026-07-04 Sprint 8.3 Retrieval Repository Abstraction + Worktree Cleanup

- [x] 将 `DocumentRetrievalService` 从 raw chunk storage 解耦到 `DocumentRetrievalProvider`
- [x] 保持 `InMemoryKeywordRetrieval` 的 keyword-only scoring / sorting 行为不变
- [x] 确认工作区没有额外 untracked chunk 文件
- [x] 更新主项目的 Architecture、DECISIONS、CHANGELOG、TASK、Backlog
- [ ] handbook mirror 自动同步被阻塞：`../scripts/sync_retail_handbook_docs.py` 需要缺失的 `ai-agent-retail-handbook-v3/README.md`

### 2026-07-04 Sprint 9.1 Internal RAG Contract Freeze

- [x] 冻结 `POST /api/v1/internal-rag/answer`
- [x] 冻结 `internal_rag.started`、`internal_rag.retrieval_completed`、`internal_rag.answer_generated`、`internal_rag.failed`
- [x] 冻结 `invalid_question`、`retrieval_unavailable`、`insufficient_context`、`citation_required`、`provider_timeout`、`repository_error`
- [x] 新增 Internal RAG Flow、Retrieval to Citation Flow、Future LLM Provider Flow、Future Approval Integration Flow
- [x] 完成主项目与 handbook 的任务、路线图、Backlog、Changelog、决策同步
- [x] 仅冻结 contract，不实现 RAG、embedding、pgvector、frontend

## Architecture Principles

- Platform First
- Domain Driven
- Provider Pattern
- Repository Pattern
- Workflow Driven
- Configuration First
- Test First
- Documentation First
- Backward Compatibility

## Target Architecture

### Current State

当前仓库未完全按平台化逻辑分层。

### Target State

未来目标逻辑分层：

```text
Platform
Domain
Provider
Workflow
Repository
Approval
Documents
Search
Import
Audit
Database
Frontend
```

### Planned

该结构用于 ERIP 目标架构规划，当前尚未全部实现。

## Epic 12 Positioning

### Current State

当前 RAG 尚未形成统一 Retrieval Layer。

### Target State

未来 RAG 范围明确包括：

- 结构化业务数据检索
- 社内文档检索
- 互联网检索
- 上下文合并
- 引用与来源追踪
- 幻觉风险控制
- 检索评估

### Planned

Epic 12 作为横向平台能力推进，而不是单一文档 RAG 能力。

## Definition of Done

任何一个 Phase 完成，必须同时满足：

- [ ] Code
- [ ] Unit Test
- [ ] Integration Test
- [ ] Frontend Test
- [ ] Handbook
- [ ] Changelog
- [ ] Decision Record
- [ ] Architecture Update
- [ ] Mermaid Diagram Update
- [ ] Task Update

## 测试文档规则

- 每个测试用例必须包含：
  - 用例目标
  - 前端操作流程
  - 后端处理流程
  - 数据输入来源
  - 预期输出
  - 验收标准
  - Mermaid 前端流程图
  - Mermaid 后端流程图

## 架构文档最小章节

- 前端流程图
- 后端流程图
- 数据流图
- 数据库 ER 图
- LangGraph workflow 图
- Retrieval Layer Architecture
- Business Retrieval Flow
- Internal RAG Flow
- Internet Search Flow
- Context Merge Flow
- Citation and Source Trace Flow
- Future Hybrid Search Architecture
- 文档检索流程图
- 审批 workflow 图
- 互联网检索流程图

### Phase 1: 文件化输入基础

- 状态：已完成第一轮实现，保持本地可运行。
- 本次完成：
  - [x] KPI 从 `backend/data/business/*.csv` 读取并计算
  - [x] Research 从 `backend/data/research/*.json` 读取 summary / sources
  - [x] 新增 `backend/data/documents/` Markdown 输入目录
  - [x] Report 增加 `generated` 状态，预留后续 Approval Workflow
  - [x] 新增文件输入测试与 hybrid 报告测试
- 后续待办：
  - [ ] 将 CSV / JSON 文件版本规则固化到导入规范
  - [ ] 将 `generated` 向 `draft / pending_approval / approved / rejected / revised` 扩展
  - [ ] 为 PostgreSQL 导入和持久化设计映射表结构

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  建立 CSV / JSON / Markdown 输入通路，替代 KPI、Research 和知识文档中的写死数据。
- 修改范围：
  数据目录规范、文件加载层、Provider 输入边界、示例数据、README / RUNBOOK / VERIFY 文档。
- 验收标准：
  任务执行可读取文件数据；移除关键运行路径中的硬编码示例值；本地仍可直接启动。
- 测试方法：
  文件加载单元测试、任务 API 集成测试、缺失文件与非法格式测试、手工验证报告来源。
- 风险：
  数据文件格式不一致、编码问题、样例数据与业务模型字段不匹配。

### Phase 2: PostgreSQL 持久化基础

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  为任务、事件、报告与导入记录提供可持久化数据库基础，并支持后续审批与检索扩展。
- 修改范围：
  PostgreSQL Repository、连接配置、迁移文件、表结构、运行脚本、部署文档。
- 验收标准：
  任务、事件、报告写入 PostgreSQL；进程重启后数据保留；接口合同保持稳定。
- 测试方法：
  Repository 测试、数据库集成测试、迁移测试、任务执行后持久化验证。
- 风险：
  本地数据库准备复杂、Schema 调整频繁、事务边界设计不足。

### Phase 3: 社内文档上传与入库

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  支持上传社内文档，并为每份文档建立版本、来源和审计信息。
- 修改范围：
  Upload API、文档元数据、文件存储策略、前端上传页面、错误处理与日志。
- 验收标准：
  支持上传受控格式文档；文档可登记并查询元数据；失败路径可追踪。
- 测试方法：
  上传接口测试、前端交互测试、重复文件测试、非法格式测试。
- 风险：
  敏感文档处理、文件大小限制、存储策略和权限设计不充分。

### Phase 4: 切分与检索基础

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  实现文档切分、片段入库、基础检索与引用输出，为 Approval Agent 和知识问答提供上下文。
- 修改范围：
  Chunk Pipeline、Retriever 抽象、片段存储、引用格式、Architecture 文档。
- 验收标准：
  上传文档可切分；查询时可返回 Top-K 片段和来源；检索结果可进入报告或审批上下文。
- 测试方法：
  Chunk 单元测试、检索回归测试、来源引用测试、端到端手工验证。
- 风险：
  Chunk 策略不稳定、检索质量不够、文档版本与索引版本失配。

### Phase 5: 审批 Workflow

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  建立可追踪的人工审批流程，支持提交、待审批、批准、拒绝和审计留痕。
- 修改范围：
  LangGraph 状态机、审批 API、审批日志表、前端审批界面、异常恢复逻辑。
- 验收标准：
  审批任务可稳定流转；日志完整；拒绝与重试路径可验证。
- 测试方法：
  状态迁移测试、审批接口测试、前端流程测试、失败恢复测试。
- 风险：
  状态管理复杂、幂等处理不足、人工操作与自动化边界不清。

### Phase 6: 互联网检索能力

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  在可控策略下引入互联网检索，为外部市场与竞品信息提供补充证据。
- 修改范围：
  Search Provider 抽象、可信来源规则、审计字段、降级策略、配置开关。
- 验收标准：
  可按配置启停互联网检索；结果保留来源；网络失败时主流程可降级。
- 测试方法：
  Provider 合同测试、失败降级测试、来源校验测试、人工抽样验证。
- 风险：
  外部数据质量、网络波动、成本与时效不可控。

### Phase 7: LangChain + LangGraph 工作流整合

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  把 LangChain 组件能力与 LangGraph 状态编排整合，形成清晰的 Tool / Retriever / Prompt / Workflow 分层。
- 修改范围：
  Workflow 组装层、Tool 适配层、Prompt 管理、Retriever 接口、架构文档和 ADR。
- 验收标准：
  组件职责清晰；核心状态流仍由 LangGraph 控制；新增组件不破坏现有 API。
- 测试方法：
  集成测试、Tool 调用测试、Prompt 回归测试、异常回退测试。
- 风险：
  框架职责重叠、抽象过度、调试成本上升。

### Phase 8: 测试体系与流程图文档

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  建立完整测试用例、测试方法、前后台流程图、系统架构图和学习文档同步机制。
- 修改范围：
  Backend / Frontend 测试、验证清单、流程图、`docs/architecture/ARCHITECTURE.md`、README、RUNBOOK。
- 验收标准：
  核心链路具备单元、集成、端到端验证；文档图示完整且与实现一致。
- 测试方法：
  执行自动化测试脚本、人工验收清单、文档对照审计。
- 风险：
  文档和实现不同步、测试成本过高、覆盖率高但有效性不足。

## Technical Debt

### High

- [ ] Chunk Strategy 统一
- [ ] Embedding 抽象层
- [ ] Prompt 版本管理
- [ ] 文件化输入契约未定义
- [ ] PostgreSQL Schema 与 Repository 边界未定义
- [ ] handbook 同步治理未形成关闭条件

### Medium

- [ ] API 统一返回格式
- [ ] 前端错误处理统一
- [ ] 初级学者友好注释补充
- [ ] Upload / Chunk / Retriever 流程图缺失
- [ ] 测试分层与测试数据策略未成体系
- [ ] handbook 测试模板与架构模板仍需补齐

### Low

- [ ] 文档补充
- [ ] 示例数据补充

## Known Issues

### BUG-001

描述：
Chunk 切分后显示效果需要确认。

状态：
Open

## Completion Log

### 2026-06-29

- 创建 PROJECT_BACKLOG.md
- 建立永久任务清单机制
- 在 AGENTS.md 追加中文“项目永久任务清单规则”，统一所有 AI 开发工具的开工与完工流程
- 建立 AI-LAB 全局规则、项目规则、Backlog、TASK 和 CHANGELOG 两层治理链路
### 2026-06-29 Governance V2

- [x] 升级到 AI-LAB Project Governance V2
- [x] 建立 Roadmap、Architecture 和 ADR 文档
- [ ] 根据真实代码和项目状态细化 Roadmap 与 Architecture

### 2026-07-02 文档同步器

- [x] 建立 retail-insight-ai 与 ai-agent-retail-handbook-v3 的文档同步映射
- [x] 新增跨项目文档同步脚本 `../../scripts/sync_retail_handbook_docs.py`
- [x] 新增同步清单 `../../doc-sync.manifest.json`

### 2026-07-04 Enterprise Planning

- [x] 将企业化改造需求纳入 TASK / Backlog / Roadmap
- [x] 新增 Phase 1 到 Phase 8 实施计划
- [x] 明确第一优先级为“文件化输入 + PostgreSQL 持久化基础”
- [x] 补充 Upload、检索、审批、互联网检索、LangChain + LangGraph、测试与架构文档任务

### 2026-07-04 Handbook Sync Governance

- [x] 新增 Phase 完成后的 handbook 同步规则
- [x] 新增测试用例强制模板规则
- [x] 新增架构文档必备图示清单
- [x] 新增 handbook CHANGELOG 与 DECISIONS 强制同步规则

### 2026-07-04 Epic 12 Retrieval and RAG Platform

- [x] 新增 Epic 12: Retrieval and RAG Platform

### 2026-07-04 Phase 1 文件化输入实现

- [x] KPI 硬编码数值迁移到 `backend/data/business/*.csv`
- [x] Research 硬编码摘要和来源迁移到 `backend/data/research/*.json`
- [x] 新增 `backend/data/documents/company_policy_sample.md`
- [x] 新增文件输入测试、Research JSON 测试、hybrid 报告测试
- [x] 报告模型预留 `generated / draft / pending_approval / approved / rejected / revised`

### 2026-07-04 Phase 1.5 Contract Freeze and Approval Design

- [x] 新增 `docs/architecture/DATA_CONTRACTS.md`
- [x] 新增 `docs/architecture/APPROVAL_WORKFLOW.md`
- [x] 新增 `docs/database/DATABASE.md`
- [x] 冻结导入错误模型
- [x] 冻结 Approval State Machine
- [x] 冻结 Phase 2 PostgreSQL 准备项
- [x] 明确 RAG 不只包括社内文档，还包括结构化业务数据检索和互联网检索
- [x] 新增 Retrieval Layer 相关架构章节与图示要求

<!-- DOC-SYNC:START group=governance -->
## 文档同步块

- group: `governance`
- file: `retail-insight-ai/docs/governance/PROJECT_BACKLOG.md`
- self_sha256: `611bb721ffe36ce4c3c4c1be6b82709516c6a46118beda941a0e7cf442e394ed`
- peers:
- `retail-insight-ai/ROADMAP.md` | sha256=3c656b952e6f27c3769dfacedbb7f097aba52bf1e7af1977d6e11cbf0b90aa0a | # retail-insight-ai Roadmap / 最后更新：2026-07-07 / ## 当前阶段 / 待根据项目现状确认。
- `retail-insight-ai/TASK.md` | sha256=d5cedb3877a8682b35aac0736259b9359bc3cad610d405249b565f64c9b589f7 | # retail-insight-ai 当前任务 / 最后更新：2026-07-07 / ## 当前阶段 / Phase 2: Internal Knowledge Approval Agent
- `retail-insight-ai/docs/governance/CHANGELOG.md` | sha256=cf9c2939e3369aa13c65a636fb64c44d56b672866b23771cf1dda5f1dbe755b3 | # retail-insight-ai CHANGELOG / ## 2026-07-02 / - 建立 retail-insight-ai 与 ai-agent-retail-handbook-v3 的跨项目文档同步机制。 / - 新增 `../scripts/sync_retail_handbook_docs.py` 与 `../doc-sync.manifest.json`。
- `ai-agent-retail-handbook-v3/ROADMAP.md` | sha256=8bea54fca33668303cb3ebc6a86e9fb359d814605450746eb7575075bc4600cf | # ai-agent-retail-handbook-v3 Roadmap / 最后更新：2026-06-29 / ## 当前阶段 / 待根据项目现状确认。
- `ai-agent-retail-handbook-v3/TASK.md` | sha256=8375c8be41775af3f492dbc66e69653096db6bcdc4838d411eacf72cd81d5c82 | # 当前任务 / 最后更新：2026-07-02 / ## 当前阶段 / 待确认
- `ai-agent-retail-handbook-v3/docs/governance/PROJECT_BACKLOG.md` | sha256=4b25c1fa793fa7ce50f3cc87341c8136603a8fc0eeae44e3b57dfcfd17f4dfc7 | # 项目总待办清单 / 最后更新：2026-07-02 / ## 项目目标 / 待确认
- `ai-agent-retail-handbook-v3/docs/governance/CHANGELOG.md` | sha256=db921303a94dca1268fc38339f4c13606461269c65ca79c1de024cc1d36601c3 | # CHANGELOG / ## 2026-07-02 / - 建立 ai-agent-retail-handbook-v3 与 retail-insight-ai 的跨项目文档同步机制。 / - 新增 `../scripts/sync_retail_handbook_docs.py` 与 `../doc-sync.manifest.json`。
- `ai-agent-retail-handbook-v3/10_Production_Roadmap.md` | sha256=d904e6883e84c4bb5adda4d7adab4499e1e0f6f5e52bf97f46ecd7150271e64e | # 10_Production_Roadmap / # 目录 / - [1. Roadmap 原则](#1-roadmap-原则) / - [2. Level 1 Demo](#2-level-1-demo)

说明：
- 这个块由 `scripts/sync_retail_handbook_docs.py` 自动维护。
- 只同步这个块，不覆盖各自正文。
- 任一组内文档正文变化时，整组文档的同步块都会一起刷新。
<!-- DOC-SYNC:END group=governance -->
