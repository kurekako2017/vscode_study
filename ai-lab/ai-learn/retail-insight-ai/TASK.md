# retail-insight-ai 当前任务

最后更新：2026-07-17

## 2026-07-17 Frontend Enterprise Authentication + RBAC

- [ ] Access Token 只保存于 sessionStorage，刷新时经 JWT 基础校验与 `/api/v1/users/me` 恢复身份
- [ ] AuthContext 集中提供当前用户、认证状态、登录、登出与 permission helper
- [ ] fetch API Client 自动注入 Bearer；Login/Health 保持匿名；401 清会话，403 保持会话
- [ ] Login、ProtectedRoute、原目标回跳和未知角色 fail-closed 落地
- [ ] 导航、Documents、RAG、Analysis、Approval 按冻结权限控制可见性与操作
- [ ] 不修改后端 Registry、JWT Payload、Approval 状态机、Schema、Migration 或 InMemory
- [ ] 完成 Frontend、双 Backend、build、compileall 与 diff-check 验证

## 2026-07-17 Enterprise Approval RBAC Boundary Correction

- [x] 正常 approve/reject 在 Router、Persistent Audit 和 Service 防御校验中统一改用 `approval.review`
- [x] Approval list 保持 `approval.review`；detail 支持 reviewer 或 `approval.submit` submitter owner
- [x] employee 非 owner、employee approve/reject、未知角色继续返回 403 并写单条 `authorization.denied`
- [x] admin 继续按冻结 Registry 同时拥有 `approval.review` 与 `approval.admin`，未修改角色权限矩阵
- [x] InMemory、状态机、Schema、Migration、Persistent Audit 基础设施和 Frontend 保持不变
- [x] 最终验证：InMemory 183（1 expected skip）、PostgreSQL 194（0 skip）、Frontend 47/47、build、compileall、diff-check

## 2026-07-17 ERIP Enterprise Approval Workflow

- [x] InMemory Approval 进入冻结维护状态；默认 `REPOSITORY_BACKEND=inmemory` 与原有测试保持可用
- [x] PostgreSQL Approval 使用 JWT `CurrentUser` 记录 submitter、reviewer 与 revision actor，忽略客户端自报身份
- [x] 状态机补齐 `rejected -> revised -> resubmitted -> pending_approval`，非法转换统一返回 409
- [x] `approval_events` 扩展为 append-only Approval History，详情接口按发生时间和主键稳定返回完整任务历史
- [x] `ReportVersion` 保持不可变；revise 创建新版本，resubmit 复用最新 revised 版本
- [x] PostgreSQL 使用 report/approval 行锁与单任务单 pending partial unique index 防止并发覆盖和重复待审
- [x] revision ownership 集中为原 submitter 或拥有 `approval.admin` 的用户，不修改冻结角色权限矩阵
- [x] 复用既有 Persistent Audit，覆盖 submitted/rejected/revised/resubmitted/approved 的 success/failure/denied
- [x] 新增 `20260717_04_enterprise_approval` migration，并完成 upgrade/downgrade/re-upgrade
- [x] 最终验证：InMemory 183（1 expected skip）、PostgreSQL 193（0 skip）、Frontend 47/47、build、compileall、migration、diff-check
- 完成记录：本轮未扩展 InMemory Repository、Persistent Audit Schema、JWT Payload、角色权限矩阵或 Frontend 登录/RBAC 界面。

## 2026-07-16 ERIP PostgreSQL Persistent Audit

- [x] InMemory Audit 进入冻结维护状态；默认 `REPOSITORY_BACKEND=inmemory` 与原有测试保持可用
- [x] PostgreSQL AuditLog 补齐 actor username/role、permission、HTTP method/path/status 和 failure 统一结果
- [x] 新增 PostgreSQL-only PersistentAuditService 与 FastAPI yield Dependency，集中处理 success/failure
- [x] JWT Dependency 记录 401，Permission Dependency 记录 `authorization.denied`，actor 只来自 CurrentUser
- [x] Approval PostgreSQL 旧审计写入关闭，避免同一动作被旧 Middleware 与新 Dependency 重复记录
- [x] PostgreSQL nested Unit of Work 使用 savepoint，成功业务与 Audit 原子提交，失败业务回滚后保留 failure event/audit
- [x] Audit API 补齐过滤、时间范围校验、limit/offset 分页和 `created_at DESC, id DESC` 稳定排序
- [x] 新增 `20260716_03_persistent_audit` migration，旧 `failed` 兼容升级为 `failure`，新增必要索引
- [x] 验证 login、authentication、authorization、document、retrieval、analysis、approval、audit、security 事件
- [x] 最终验证：InMemory 183（1 expected skip）、PostgreSQL 191（0 skip）、Frontend 47/47、build、compileall、diff-check
- 完成记录：本轮未修改 InMemory Repository 实现、默认 backend、冻结角色权限矩阵、JWT permissions、Frontend、README、学习文档或面试文档。

## 2026-07-15 ERIP Enterprise RBAC Authorization

- [x] 建立 `JWT -> CurrentUser -> RBAC -> Business API` 授权链，不修改 JWT Payload
- [x] 集中定义 admin / manager / employee、10 项 Permission、Role Mapping、Authorization Result 与 Permission Checker
- [x] 在 `backend/app/security/` 建立 Permission Registry、Resolver、Authorization Service 与 Permission Dependency
- [x] 所有授权 API 只声明 `Depends(require_permission(...))`，不在 Router/Service 散落 role 判断
- [x] Documents、Retrieval、Internal RAG、Tasks、Approval、Audit 与 Security Catalog 已挂载明确权限
- [x] Health、Login、Swagger/OpenAPI 保持匿名；`users/me` 只要求认证
- [x] 权限不足和未知角色 fail-closed，统一返回 403 `forbidden`、`permission`、`role`，不返回 401/500
- [x] Swagger 保留 `BearerAuth`，Permission Dependency 复用同一 CurrentUser 认证链
- [x] 新增 12 个 RBAC 测试；完整回归：InMemory Backend 182 passed / 1 expected skip；PostgreSQL Backend 187 passed / 0 skipped；Frontend 47/47；build、compileall 通过
- 完成记录：本轮未修改 JWT Contract、Repository、Alembic、Migration、schema、Embedding、pgvector、Retrieval/Reranker 实现、Frontend、README、Learning 或 handbook。

## 2026-07-15 ERIP Enterprise JWT Authentication

- [x] 建立 Access Token、Token Payload、Current User 与 Authentication Error 统一合同
- [x] 在 `backend/app/security/` 集中实现 JWT Config、Provider、Service、Password、Login 与 CurrentUser Dependency
- [x] 使用 passlib + bcrypt 校验 admin / manager / employee 三个 deterministic test users，不保存明文密码
- [x] `POST /api/v1/auth/login` 签发默认 30 分钟 HS256 Access Token，不实现 Refresh Token
- [x] 除 Health、Login、Swagger/OpenAPI 外，所有现有业务 API 统一要求 Bearer JWT
- [x] Swagger OpenAPI 生成 `BearerAuth`，受保护 API 可通过 Authorize 测试
- [x] 缺失、非法签名、非法 payload、过期 Token 和登录失败统一返回 401，不返回 500
- [x] 保持既有 RBAC permission catalog、permission matrix 与 approval authorization 判定不变
- [x] 完整回归：InMemory Backend 170 passed / 1 expected skip；PostgreSQL Backend 175 passed / 0 skipped；Frontend 47/47；build、compileall 通过
- 完成记录：本轮只实现 Authentication；未进入 Refresh Token、用户数据库、RBAC 扩展、Frontend、Repository、Migration、README、Learning 或 handbook。

## 2026-07-14 ERIP Enterprise Reranker

- [x] 建立独立 `RerankerProvider` / `RerankerService`，Repository 继续只负责候选召回
- [x] 建立可配置 Top-N（默认 20）与 Final Top-K，并保持既有 Internal RAG API contract
- [x] 完成基于关键词覆盖率、retrieval score、位置与 SHA-256 tie-break 的 deterministic reranker
- [x] 完成 disabled、missing provider、provider exception 的无损 retrieval-order fallback
- [x] 完成 InMemory 154 tests（skip 1）与 PostgreSQL 159 tests（skip 0）完整回归
- 完成记录：Frontend 47/47、production build、compileall 全绿；未修改 Repository、Migration、Schema、Frontend、README、learning 或 handbook。

## 2026-07-14 ERIP Embedding + Vector/Hybrid Retrieval

- [x] 完成固定 384 维 Embedding Contract、deterministic test provider 与输入输出校验
- [x] 完成 Chunk embedding 的 InMemory/PostgreSQL 持久化合同与 cosine 查询
- [x] 完成兼容默认 keyword 的 vector/hybrid retrieval、过滤、融合、去重和 fallback
- [x] 新增独立 `20260714_02_chunk_embeddings` revision，不修改 Initial Revision 文件
- [x] 默认 InMemory Baseline：Backend 140 tests（PostgreSQL suite 预期 skip 1）、Frontend 47/47、build、compileall 全绿
- [ ] 安装 PostgreSQL 16 pgvector 系统包后执行 upgrade/downgrade/re-upgrade 与 PostgreSQL 完整回归
- 阻塞记录：本机缺少 `/usr/share/postgresql/16/extension/vector.control`；migration 已事务回滚，测试库仍为 `20260714_01_initial_schema`，未残留 extension 或 embedding 列。

## 2026-07-14 ERIP Enterprise Phase 2B Baseline Gate + Repository Audit

- [x] 检查 Git 工作区状态并确认未覆盖用户修改
- [x] 重新执行统一 Baseline，确认 Backend / Frontend / Build / compileall 当前可通过
- [x] 复核昨天记录的 4 个 Frontend timeout，用现有完整 Baseline 未再次复现
- [x] 审计 Repository 双后端切换、Contract 对齐、Service 依赖接口和 API 分层边界
- [x] 明确记录 PostgreSQL integration suite 在无 `DATABASE_URL` 环境下按设计跳过
- 完成记录：首次 Baseline 出现 `src/App.test.tsx` 的 `insufficient_context` 学习侧栏用例 1 次 timeout；定向复跑和整份 `App.test.tsx` 复跑通过，第二次 `./scripts/run_tests.sh` 全绿。Backend 125 tests passed（skipped=1 for PostgreSQL suite）、Frontend 47 passed、Frontend build passed、Python compileall passed。昨天的 4 个 Frontend timeout 本轮均未复现。当前环境未设置 `DATABASE_URL`，因此真实 PostgreSQL 契约测试未执行，只能确认其跳过机制安全有效。

## 2026-07-13 ERIP Enterprise Phase 2A

- [x] 新增无密码、无建库、无 schema 修改的 PostgreSQL 开发验证脚本
- [x] 建立不含迁移版本、不会升级数据库的 Alembic Baseline
- [x] 建立默认关闭且不生成向量、不访问外部 API 的 Embedding Foundation
- [x] 完成 Backend、Alembic、Embedding、InMemory 与 PostgreSQL 回归
- 完成记录：Backend 125 tests（默认模式 PostgreSQL suite 跳过）、定向 10 tests、InMemory 14 tests、PostgreSQL 4 tests 与 compileall 均通过。

## 2026-07-13 ERIP Phase 1 Complete PostgreSQL Persistence Bundle

- [x] 保持默认 InMemory，并补齐可显式启用的完整 PostgreSQL Repository Bundle
- [x] 完成通用事件流、Approval 唯一版本事实源、核心 Unit of Work 与双后端契约测试
- [x] 全量验证与真实 PostgreSQL Integration Tests 均通过

## 2026-07-12 Scenario01 Business Sample Data

- [x] 生成 `docs/learning/sample-data/Scenario01_Sales_Decline/` 的 10 份企业业务学习文档
- [x] 统一关东地区饮料销售下降的业务背景、数值口径和后续学习用途
- [x] 保持 Scenario01 单一背景，不新增 Scenario02 或其他散乱主题
- [x] 完成记录：这批文档用于 Documents、RAG、Analysis、Approval 与业务测试学习

## 2026-07-11 API Case 输入参数与 Learning Trace 对齐

- [x] 核对 `docs/learning/01_Foundation/LEARNING_API_WALKTHROUGH.md` 的 24 个 API Case
- [x] 按 Router 签名补齐 Path、Query、Header、Body、Form、File、默认值和约束
- [x] 修正 `GET /api/v1/documents` 的文档列表输入、日志观察和执行链路
- [x] 为文档列表 Router / Service 补充最小 Learning Trace，不改变业务逻辑
- [x] 仅保留真实源码中的方法与 Repository 调用，不虚构 Structured Log

## 2026-07-08 Learning Request Body Trace

- [x] 在 `TaskService.create_task()` 追加学习日志，终端可直接看到 `request.question`、`request.mode` 和 `task_id`
- [x] 保持 API response、Workflow、Repository 和测试逻辑不变
- [x] 同步更新 `README.md`、`docs/learning/LEARNING_API_WALKTHROUGH.md`、`docs/learning/RUNBOOK_LOCAL.md`、`docs/learning/CODE_STUDY_GUIDE.md` 和 `VERIFY_CHECKLIST.md`
- [x] 完成后验证 `POST /api/tasks` 的终端输出能明确看到 `question: 你好`

## 2026-07-08 ERIP Worldview Alignment

- [x] 统一 `README.md`、`ROADMAP.md`、`TASK.md`、`ARCHITECTURE.md`、`PROJECT_BIBLE.md` 等主文档中的平台名称
- [x] 统一 `Retail Insight AI = Current MVP / PoC / Early Prototype`
- [x] 统一 `Enterprise Retail Intelligence Platform (ERIP) = Target 企业平台`
- [x] 统一 `Task API`、`TaskService`、`LangGraph Workflow`、`Fixed KPI Workflow`、`Research Agent`、`Report Generator`、`Repository Pattern`
- [x] 统一 `Current / Target / Planned` 标记，禁止把未来能力写成已实现
- [x] 完成记录：治理文档、架构文档、handbook 总规则、系统设计书、架构图册、生产路线图和面试总稿已统一到 ERIP 世界观

## 2026-07-07 Technical Architecture Handbook Alignment

- [x] 为 `docs/ai-agent-retail-handbook-v3/09_系统设计书.md` 新增 `7.0 Technical Architecture（技术架构总览）`
- [x] 为 `docs/ai-agent-retail-handbook-v3/08_架构图册.md` 追加 Technology Stack Architecture / AI Framework Relationship / Retrieval Pipeline / Technology Evolution Mermaid 图
- [x] 统一 `Keyword Retrieval (Current)`、`Hybrid Retrieval (Target)`、`Vector Database (Target)`、`LangGraph = Workflow Orchestration`、`LangChain = RAG Orchestration`
- [x] 同步 `PROJECT_BIBLE.md`、`README.md`、`docs/governance/CHANGELOG.md`
- [x] 本次仅修改 Markdown 文档，不修改 backend、frontend、tests、scripts 或系统行为

## 2026-07-07 API Walkthrough Repair

- [x] 修复 `docs/learning/LEARNING_API_WALKTHROUGH.md` 的接口章节截断与错位问题
- [x] 恢复 `01~23` 接口章节与补充接口章节，保持原学习路线不变
- [x] 将“源码学习说明”拆回各自接口下，避免跨章节混放源码说明
- [x] 保持 Swagger 操作、输入输出、后台日志、程序调用流程原结构不变
- [x] 本次仅修正文档，不修改 backend、frontend、tests、scripts 或 API 行为

## 当前阶段

Documentation Organization + AI Agent Guide 中文化 Sprint

状态：已完成

### 2026-07-06 Backend Startup Recovery

- [x] 修复后端本地启动失败的根因：`python-multipart` 未声明且当前环境未安装
- [x] 在 `backend/requirements.txt` 中补充 `python-multipart==0.0.20`
- [x] 创建并激活 `.venv`，升级 `pip`，重新安装 backend 依赖
- [x] 从 `backend` 目录执行 `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000` 验证启动成功
- [x] 验证 `/health`、`/docs`、`/redoc`、`/openapi.json` 均返回 200
- [x] 只在 `docs/learning/RUNBOOK_LOCAL.md` 末尾追加 Appendix A / Appendix B，不删除原文
- [x] 补充启动、验证与常见错误排错步骤，便于初学者复现

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

### Learning Trace Phase 4

- [x] Learning Trace 升级为企业级、源码一眼可读 block，按 `HTTP Request -> Router -> Controller File -> Controller Method -> Return -> Schema File -> Schema -> HTTP Response` 展示
- [x] `backend/app/core/learning_trace.py` 支持按文件切换自动补出 `Controller File`、`Entering File`、`Schema File`、`Schema`
- [x] `GET /health` 与 `POST /api/tasks` 的学习顺序和实际 trace 输出保持一致
- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 同步更新程序调用流程，并修正健康检查 schema 文件名为真实路径 `backend/app/schemas/health.py`
- [x] `LEARNING_TRACE=false` 时仍然不输出新增学习 trace
- [x] 保持 API 行为、返回值、Swagger、OpenAPI、SSE、业务逻辑不变

### Documentation Organization + AI Agent Guide 中文化 Sprint 结果

- [x] `docs/` 活动 Markdown 已按 `learning`、`architecture`、`contracts`、`development`、`database`、`governance` 分层管理
- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 保留主链路接口总览、接口详细表和程序调用流程
- [x] `docs/learning/TEST_CASES.md` 保留测试总览、测试详细表和后端程序流程，并新增“保护的 Bug / 风险”列
- [x] `docs/architecture/AI_AGENT_DESIGN_GUIDE.md` 已调整为中文为主、日语为辅，覆盖 Workflow、Agent、Tool、Repository、Provider、RAG、Approval、RBAC、Audit
- [x] `README.md` 已同步新目录结构和所有 Markdown 链接
- [x] `docs/development/MASTER_PROMPT.md` 已补充文档合并、唯一主文档、归档和语言规则
- [x] Documentation Only：未修改 backend、frontend、scripts、Python、React、API、测试实现或业务逻辑

### Documentation Readability Optimization Sprint 结果

- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 调整为 `主链路接口总览 -> 接口详细表 -> 程序调用流程`
- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 的所有主接口均采用统一详细表格
- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 的程序流程统一补充文件路径、类名、方法名
- [x] `docs/learning/TEST_CASES.md` 调整为 `测试总览 -> 测试详细表 -> 后端程序流程`
- [x] `docs/learning/TEST_CASES.md` 的所有测试文件均采用统一详细表格
- [x] `docs/learning/TEST_CASES.md` 的后端程序流程统一补充文件路径、类名、方法名
- [x] 本次仅修改 Markdown 文档，不修改 backend、frontend、scripts、Python、React、API、测试实现或业务逻辑

### Documentation Governance V2 结果

- [x] README 升级为唯一知识导航中心，补齐全部 Markdown 文档链接
- [x] README 增加知识地图、学习路线流程图、当前完成情况矩阵和企业项目验证体系
- [x] README 增加文档责任表，明确唯一职责和禁止新增同类文档
- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 增加接口学习总表，并保留每个接口的完整章节
- [x] `docs/learning/TEST_CASES.md` 增加测试总览表，并保留每个测试文件的完整章节
- [x] `RUNBOOK_LOCAL.md` 内容已由 README、LEARNING、TEST、VERIFY 承接，移动到 `docs/_archive_candidate/RUNBOOK_LOCAL.md`
- [x] handbook/docs 技术规范镜像已移动到 `docs/_archive_candidate/handbook-docs/`
- [x] handbook TASK / ROADMAP 镜像已移动到 `docs/_archive_candidate/handbook-root/`
- [x] `STUDY_PLAN_DAY1_DAY3.md` 已移动到 `docs/_archive_candidate/root/`
- [x] `docs/_archive_candidate/README.md` 更新归档规则、当前归档候选文件和未来删除条件
- [x] `docs/ai-agent-retail-handbook-v3/README.md` 调整为长期知识库入口，不重复维护主项目介绍
- [x] `docs/development/MASTER_PROMPT.md` 增加 Documentation Governance 永久规则
- [x] Documentation Only：未修改 backend、frontend、tests、scripts、Python、React

### Documentation Recovery + Governance Sprint 结果

- [x] 先盘点仓库 Markdown 文档，再开始修改
- [x] `README.md` 恢复为项目总入口，并补齐目录树、文档导航中心、学习路线、测试路线、源码阅读路线、面试准备路线、文档治理规则
- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 恢复为分接口学习文档，23 个主接口分别独立成节
- [x] `docs/learning/TEST_CASES.md` 恢复为分测试文件学习文档，重点测试文件分别独立成节
- [x] `RUNBOOK_LOCAL.md`、`VERIFY_CHECKLIST.md` 补充 Swagger / ReDoc / OpenAPI JSON 与 backend 目录执行 unittest 规则
- [x] `docs/development/MASTER_PROMPT.md` 补充永久文档保护规则
- [x] `docs/ai-agent-retail-handbook-v3/README.md` 明确 handbook 根目录与 handbook/docs 的职责边界
- [x] 新增 `docs/_archive_candidate/README.md` 记录疑似重复文档清单
- [x] `docs/governance/PROJECT_BACKLOG.md` 增加“文档治理清单”
- [x] 本次仅修改 Markdown 文档，不修改 backend、frontend、scripts、业务代码、测试代码

### Documentation Restore + Safe Merge Sprint 结果

- [x] 恢复 README 的树形目录结构图和文档导航中心，保留原有目录说明与验证系统
- [x] 将 `docs/learning/LEARNING_API_WALKTHROUGH.md` 恢复为分接口学习说明，补回每个接口的完整学习路径
- [x] 将 `docs/learning/TEST_CASES.md` 恢复为程序运行流程学习文档，补回每个测试文件的完整流程说明
- [x] 补充 `RUNBOOK_LOCAL.md`、`VERIFY_CHECKLIST.md`、`docs/development/MASTER_PROMPT.md` 的企业项目测试体系和文档规则说明
- [x] 补充 `docs/ai-agent-retail-handbook-v3/README.md` 的根目录与 `docs` 目录职责说明
- [x] 同步更新 handbook 镜像侧 `MASTER_PROMPT` 规则说明
- [x] 本次仅修改文档，不修改 backend、frontend、scripts、业务代码、测试代码

### 文档重构 V3 结果

- [x] README 重写为项目门户，并补齐项目概览、架构、目录、文档导航和验证系统
- [x] `RUNBOOK_LOCAL.md` 重写为启动与排错指南，补齐每条命令的原因、结果、失败和验证
- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 重写为初学者学习文档，补齐 Swagger、当前学习阶段和时序模板
- [x] `docs/learning/TEST_CASES.md` 重写为学习导向测试文档，补齐 Swagger / unittest 区别、测试保护的 bug 和能力
- [x] `CODE_STUDY_GUIDE.md` 重写为固定阅读顺序，明确 `Swagger -> API -> Service -> Repository -> Domain -> Tests`
- [x] `docs/ai-agent-retail-handbook-v3/INTERVIEW_GUIDE.md` 保持企业 AI 后端项目面试稿定位，继续作为唯一面试文档入口
- [x] 本次仅修改文档，不修改 backend、frontend、scripts、业务逻辑或测试实现

### 文档重构 V1 结果

- [x] `README.md` 重写为唯一项目入口，补齐项目介绍、当前实现范围、目录说明、文档导航中心和文档原则
- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 重写为中文主导的接口学习走读，补齐 Swagger / ReDoc / OpenAPI JSON、后台日志观察点和学习日志
- [x] `docs/learning/TEST_CASES.md` 重写为程序运行流程学习文档，补齐测试目的、程序流转、后台日志观察点和学习日志
- [x] `RUNBOOK_LOCAL.md` 重写为启动与排错指南，补齐为什么执行、成功判断、失败原因和解决方法
- [x] `VERIFY_CHECKLIST.md` 重写为启动完成检查清单，补齐检查项、执行命令、预想结果、失败现象和对应文档
- [x] `CODE_STUDY_GUIDE.md` 重写为源码阅读指南，补齐为什么要 `Service`、`Repository`、`Provider`、`Workflow`
- [x] `docs/ai-agent-retail-handbook-v3/INTERVIEW_GUIDE.md` 重写为企业 AI 后端项目面试稿，补齐中文回答与日语回答
- [x] 仅修改文档，不修改 backend、frontend、scripts、API 行为、业务逻辑、数据库或测试实现
- [x] 删除并收敛旧面试文档引用，统一指向 handbook 唯一入口

### Documentation Consolidation Sprint 2 Result

- [x] README 增加文档导航中心、初学者/面试/开发维护阅读分组和文档数量控制规则
- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 改为主链路接口学习表，补齐下一步和常见失败
- [x] `docs/learning/TEST_CASES.md` 改为测试文件学习表，补齐后端流程和 Swagger/前端流程
- [x] `docs/ai-agent-retail-handbook-v3/INTERVIEW_GUIDE.md` 改为中文主导、日语辅助的日本项目面试稿
- [x] `RUNBOOK_LOCAL.md` 补齐项目根目录脚本与 backend 目录 uvicorn 的区分，以及 Swagger / ReDoc / OpenAPI JSON 用法
- [x] `VERIFY_CHECKLIST.md` 增加失败时先看哪个文档
- [x] `CODE_STUDY_GUIDE.md` 补齐推荐阅读文件和下一步看哪里
- [x] `docs/development/MASTER_PROMPT.md` 增加文档数量控制规则
- [x] 本次仅修改文档，不修改 backend/app、backend/tests、frontend、scripts

### Sprint R3.1 Result

- [x] `README.md` 改为中文入口，并新增“第一次启动项目”章节
- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 按接口顺序重写为中文学习走读
- [x] `docs/learning/TEST_CASES.md` 按测试文件逐个补齐测试目的、对应 API、源码位置、运行命令、输入、预期输出和设计理由
- [x] `RUNBOOK_LOCAL.md` 改写为“启动与排错指南”，使用“问题 → 原因 → 解决方法”组织内容
- [x] `VERIFY_CHECKLIST.md` 改写为启动完成检查清单，并明确每项如何验证成功
- [x] `CODE_STUDY_GUIDE.md` 为每章补齐学习目标、推荐阅读时间、推荐顺序和掌握目标
- [x] 本次仅做文档优化，不修改 Python 代码、测试代码或接口

### Sprint R3 Result

- [x] 最短学习路径已收敛到 `README.md` / `docs/learning/LEARNING_API_WALKTHROUGH.md` / `CODE_STUDY_GUIDE.md`
- [x] `README.md` / `RUNBOOK_LOCAL.md` / `VERIFY_CHECKLIST.md` 已补齐启动命令、Swagger 地址、最小验证命令和常见失败原因
- [x] 新增 `docs/learning/TEST_CASES.md`，整理 backend tests 现状、核心路径和 PostgreSQL 相关测试
- [x] 新增 `docs/ai-agent-retail-handbook-v3/INTERVIEW_GUIDE.md`，整理项目背景、架构、职责和面试回答要点
- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 已补充最短路径、文档职责与三语言摘要
- [x] backend tests 与 compileall 验证将继续作为本 sprint 的收口检查

### Future Sprint Checklist

- [x] Human-readable documentation is trilingual: English / 中文（简体） / 日本語

## 当前最高优先级任务

### Sprint R3 Result

- [x] 最短学习路径已收敛到 `README.md` / `docs/learning/LEARNING_API_WALKTHROUGH.md` / `CODE_STUDY_GUIDE.md`
- [x] `README.md` / `RUNBOOK_LOCAL.md` / `VERIFY_CHECKLIST.md` 已补齐启动命令、Swagger 地址、最小验证命令和常见失败原因
- [x] 新增 `docs/learning/TEST_CASES.md`，整理 backend tests 现状、核心路径和 PostgreSQL 相关测试
- [x] 新增 `docs/ai-agent-retail-handbook-v3/INTERVIEW_GUIDE.md`，整理项目背景、架构、职责和面试回答要点
- [x] `docs/learning/LEARNING_API_WALKTHROUGH.md` 已补充最短路径、文档职责与三语言摘要
- [x] backend tests 与 compileall 验证将继续作为本 sprint 的收口检查

### Verification Boundary

- 当前只做文档优化和学习路径整理，不新增业务功能，不改 frontend，不接 PostgreSQL，不接真实 LLM，不接 JWT/OAuth，不接 pgvector/MCP。
- 不伪造 PostgreSQL、真实 LLM、JWT/OAuth、MCP 或 frontend 已完成。
- 需要代码级变更时，必须进入新的实现 sprint。

### Sprint Result

- [x] 已完成收口整理，不新增功能，不改 frontend，不接 PostgreSQL，不接真实 LLM，不接 JWT / OAuth
- [x] 后端验证通过：`python3 -m unittest discover -s tests -v`
- [x] 后端编译检查通过：`python3 -m compileall app tests`
- [x] 当前已完成能力、未完成能力和项目边界已整理为三语摘要
- [x] handbook mirror 已同步

- [x] approval APIs now enforce RBAC with the existing current-user seam
- [x] default system admin placeholder user passes all approval checks
- [x] denied approval access writes append-only audit facts
- [x] backend tests added for submit / review / approve / reject / revise deny paths
- [x] docs updated: API_CONTRACT / ARCHITECTURE / TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS / handbook mirror
- [x] backend / frontend / scripts boundary unchanged
- [x] Human-readable documentation is trilingual: English / 中文（简体） / 日本語

### 已完成能力

- 英文术语：Document Upload, Document Read, Document Archive, Document Import, Document Chunk, Document Retrieval, Internal RAG without LLM, LLM Provider Stub Seam, Approval Workflow, RBAC for Approval APIs, Approval Audit Middleware, Security Domain, InMemory Audit Log
- 中文（简体）：文档上传、文档读取、文档归档、文档导入、文档切分、文档检索、无 LLM 的内部 RAG、LLM Provider Stub 接缝、审批工作流、审批 API 的 RBAC、审批审计中间件、安全域、InMemory 审计日志
- 日本語：ドキュメントアップロード、ドキュメント読取、ドキュメントアーカイブ、ドキュメントインポート、ドキュメントチャンク、ドキュメント検索、LLM なしの内部 RAG、LLM Provider Stub の接続点、承認ワークフロー、承認 API の RBAC、承認監査ミドルウェア、セキュリティドメイン、InMemory 監査ログ

### 未完成能力

- 英文术语：frontend UI, PostgreSQL repository full migration, real authentication, JWT/OAuth, real LLM provider, pgvector, internet search, MCP, production deployment
- 中文（简体）：前端 UI、PostgreSQL 仓库全面迁移、真实认证、JWT/OAuth、真实 LLM 提供方、pgvector、互联网搜索、MCP、生产部署
- 日本語：frontend UI、PostgreSQL リポジトリの完全移行、実認証、JWT/OAuth、実 LLM provider、pgvector、インターネット検索、MCP、本番デプロイ

### Validation

- Backend unit tests: `python3 -m unittest discover -s tests -v` -> passed, `115` tests run, `1` skipped because `psycopg` is not installed in the current environment
- Backend compile check: `python3 -m compileall app tests` -> passed

### Next Focus

- Keep the current scope frozen until frontend, PostgreSQL, real auth, and real LLM are intentionally scheduled
- Use the current backend as the stable interview and learning baseline

## 后续优先级：面试线与项目线并行

### P0：企业项目面试核心文档

- [ ] 重构 01_日本AI项目介绍.md，按当前代码与企业架构抽象重写，避免写死临时实现。
- [ ] 重构 02_日本AI项目讲解.md，去除重复项目介绍，改成问题、回答、源码、TL追问、Production回答结构。
- [ ] 重构 03_AI核心知识.md，所有知识点必须绑定 Retail Insight AI 当前代码。
- [ ] 重构 04_日本现场开发.md，对应日本现场开发流程、設計、Review、测试、保守改修。
- [ ] 重构 05_TL代码审查.md，改成真实项目 Review Checklist。

说明：

- 优先服务日本企业面试。
- 企业架构抽象优先，不要绑定临时实现。

### P0.5：企业项目讲解能力

- [ ] 维护 `INTERVIEW_GUIDE.md` 过渡内容，统一承接项目讲解材料。
- [ ] 维护 `PROJECT_BIBLE.md` 作为唯一入口，保证总览不分散。
- [ ] 维护 Learning Trace，用于讲解调用链和源码流转。
- [ ] 维护 Swagger Walkthrough，用于讲解接口输入输出。
- [ ] 维护后台日志观察，用于讲解运行过程与问题定位。

说明：

- 帮助建立项目讲解能力。
- 帮助建立源码讲解能力。
- 帮助建立接口讲解能力。
- 帮助建立调用链讲解能力。
- 帮助建立 TL 深问能力。

### P1：学习平台继续完善

- [ ] 继续维护 Learning Trace、Swagger 学习、后台日志观察、memo 文档。
- [ ] 后续优化 Learning Trace 日志显示：module、function、endpoint、class、method、file 更清晰。

## V2.0 Handbook 命名统一计划（最终阶段）

当前 Handbook 经过长期演进，存在中英文混用、命名风格不一致、职责边界逐渐变化的问题。

V2.0 收尾阶段统一执行一次文档命名整理。

当前阶段仅记录规划，不修改任何文件。

### 统一原则

- 全部采用数字编号命名。
- 文件名保持简洁。
- 文档标题继续保持 English / 日本語 / 中文三语言。
- 一个文档只负责一个职责（Single Responsibility）。
- 文件名不再混用 GUIDE、BIBLE、ROADMAP 等不同风格。
- PROJECT_BIBLE.md 继续作为唯一入口文档。
- 所有引用统一更新，避免失效链接。
- INTERVIEW_GUIDE.md 作为过渡文档，最终合并或重命名到 `02_项目讲解.md`。
- README.md 保留英文名称，不参与统一命名。
- AGENTS.md 保留英文名称，不参与统一命名。
- PROJECT_BIBLE.md 保留英文名称，不参与统一命名。
- SSOT 原则：所有面试内容最终只保留一份唯一事实来源。
- 最终统一修改引用和目录。
- 最终统一改名。
- 等代码稳定后一次完成。

### 建议最终命名

- `01_项目介绍.md`
- `02_项目讲解.md`
- `03_核心知识.md`
- `04_现场开发.md`
- `05_代码审查.md`
- `06_学习路线.md`
- `07_面试问答.md`
- `08_架构图册.md`
- `09_系统设计.md`
- `10_开发路线图.md`
- `11_项目结构.md`
- `12_架构决策.md`

### 特殊文档

- `PROJECT_BIBLE.md`
- `README.md`
- `AGENTS.md`

继续保留英文名称，不参与统一命名。

### 执行时机

满足以下条件后统一执行：

- 核心代码基本稳定。
- 面试文档完成。
- 架构图完成。
- Handbook V2.0 定稿。
- 一次性修改所有引用、目录、README、PROJECT_BIBLE。

### 注意事项

- 当前阶段禁止提前改名。
- 所有改名统一放到 Handbook V2.0 收尾阶段一次完成，避免多次修改引用关系。

### P2：项目工程文档，随代码稳定后再做

- [ ] 重新校准 08_架构图册.md。
- [ ] 重新校准 09_系统设计.md。
- [ ] 重新校准 11_项目结构.md。
- [ ] 重新校准 12_架构决策.md。

### P3：最终整合

- [ ] 最后整理 PROJECT_BIBLE.md，作为唯一总入口。
- [ ] 新增或重构 AI Interview Notes（日本AI项目讲解手册），格式为：Question / 回答 / 源码 / 架构图 / Learning Trace / TL追问 / Production回答。

原则：

- 当前阶段先服务面试，不等代码100%完成。
- 面试文档使用企业架构抽象，不绑定临时实现细节。
- 后续代码仍可能持续演进。
- 因此：
- Learning 文档可以持续更新。
- 面试文档保持企业抽象。
- 工程设计文档等待代码稳定后统一校准。
- 最终在 Final Freeze Sprint 完成全项目统一收口。
- 工程文档等代码更稳定后再严格同步。
- 不修改任何代码。
- 不修改其它文档。
- git diff --check 通过。

## Final Freeze Sprint（最终收尾）

这是整个项目最终收尾阶段。

包括：

- Code Freeze
- Documentation Freeze
- Handbook Freeze
- README 最终整理
- PROJECT_BIBLE 最终整理
- Handbook 全部统一命名
- 所有引用统一更新
- Mermaid 图统一
- 架构图统一
- 截图统一
- Learning Trace 最终校准
- Interview 文档最终校准
- Release v2.0

说明：

- 所有统一改名、统一引用、统一目录，都放到这一阶段执行。
- 不要提前改名。


## 历史完成项

### Boundary

- 当前实现只在 approval APIs 上做 RBAC，不扩展到 document / retrieval / RAG / task APIs。
- 当前 current user seam 仍是 placeholder principal，不接真实认证、JWT、OAuth 或外部身份提供器。
- 不改变现有 approval response contract。

### Sprint Result

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
- [x] docs updated: ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS / ARCHITECTURE / handbook mirror
- [x] backend / frontend / scripts boundary unchanged
- [x] Human-readable documentation is trilingual: English / 中文（简体） / 日本語

### Sprint 11.1: Enterprise Security Foundation Contract Freeze

- [x] user / organization / department / role / permission / policy concepts frozen
- [x] GET /api/v1/users/me, GET /api/v1/security/roles, GET /api/v1/security/permissions, GET /api/v1/audit-logs contract frozen
- [x] RBAC approval-action matrix frozen
- [x] audit log contract and operation log contract frozen
- [x] future authentication relationship documented
- [x] docs updated: API_CONTRACT / EVENT_CONTRACT / ERROR_CATALOG / ARCHITECTURE / DATABASE / TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS / handbook mirror
- [x] backend / frontend / scripts untouched

### Boundary

- 当前实现已从 docs contract freeze 进入 backend MVP，但仍不接真实认证、JWT、OAuth 或外部身份提供器。
- 当前 security foundation 仍只是未来 RBAC / audit 的契约边界，不代表已实现真实身份系统。
- 不改变现有 document retrieval、internal RAG 或 approval API response contract。

## Sprint 10.2: Approval API MVP Implementation

### Sprint Result

- [x] POST /api/v1/reports/{task_id}/submit-approval implemented
- [x] GET /api/v1/approvals implemented
- [x] GET /api/v1/approvals/{approval_id} implemented
- [x] POST /api/v1/approvals/{approval_id}/approve implemented
- [x] POST /api/v1/approvals/{approval_id}/reject implemented
- [x] POST /api/v1/reports/{task_id}/revise implemented
- [x] immutable report version snapshot model added
- [x] ApprovalRequest / ApprovalEvent domain models added
- [x] InMemory approval repository added
- [x] approval submitted / approved / rejected / revised / failed events emitted
- [x] approval API tests added for success and error paths
- [x] backend full suite and compileall pending verification

### Boundary

- 当前实现仍只在 backend 生效，不修改 frontend 或 scripts。
- 当前 approval workflow 依赖 frozen contract，但已进入 MVP implementation。
- 不改变现有 report / retrieval / internal RAG response contract。

## Sprint 10.1: Approval Workflow Contract Freeze

### Sprint Result

- [x] approval domain model frozen
- [x] approval API contract frozen
- [x] approval event contract frozen
- [x] approval error catalog frozen
- [x] approval state transition rules frozen
- [x] report revision relationship / audit relationship / future RBAC relationship documented
- [x] docs updated: API_CONTRACT / EVENT_CONTRACT / ERROR_CATALOG / ARCHITECTURE / DATABASE / TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS / handbook mirror
- [x] backend / frontend / scripts untouched

### Current State

- Approval workflow is contract-only.
- Report revisions remain immutable snapshots.

### Target State

- Future Approval API can be implemented without changing report / retrieval / internal RAG boundary.

### Planned

- Keep this phase doc-only.
- Implementation must wait for a later backend sprint.

## Sprint 9.5: LLM Provider Seam Stub MVP

### Current State

- Internal RAG 仍然默认走 deterministic extractive path。
- `StubLLMProvider` 已接入 `RAGAnswerGenerator`，但只有在 `INTERNAL_RAG_USE_LLM=true` 时才会使用。

### Target State

- 未来真实 LLM provider 可以替换 stub provider，而不改变 API contract 或 retrieval boundary。

### Planned

- 继续保持 deterministic fallback 为默认路径。
- 未来若接入真实 provider，只允许替换 provider 实现，不允许改动 internal RAG response contract。

## Sprint 9.4: LLM Provider Seam Contract Freeze

### Sprint Result

- [x] LLMProvider interface concept frozen as the future model integration seam
- [x] RAGAnswerGenerator concept frozen as the answer assembly boundary
- [x] prompt input/output contract frozen for optional LLM-driven answer generation
- [x] provider error model frozen for unavailable / timeout / invalid output / missing citation / cost limit cases
- [x] deterministic extractive fallback preserved as the current default behavior
- [x] token / cost / latency tracking placeholders documented for future providers
- [x] ARCHITECTURE / PROMPT_STANDARD / AI_AGENT_DESIGN_GUIDE / ERROR_CATALOG updated
- [x] TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS / handbook mirror synchronized

### Boundary

- 当前行为仍然是 deterministic internal RAG，不调用 LLM、不调用外部 provider。
- 不修改 backend、frontend 或 scripts。
- 不改变 `POST /api/v1/internal-rag/answer` 的 response 结构。

## Sprint 9.4: LLM Provider Seam Contract Freeze

### Current State

Internal RAG 已完成 deterministic answer assembly，当前只冻结未来 LLM provider 的接入边界。

### Target State

未来可以把 `LLMProvider` 接到 `RAGAnswerGenerator` 后面，而不改变 retrieval contract、citation contract 或 API response。

### Planned

- 继续保持当前 no-LLM 行为作为默认路径。
- 未来若接入模型，只允许替换 answer generation seam，不允许回写 retrieval provider boundary。

## Sprint 9.3: Internal RAG Evaluation + Citation Quality MVP
- [x] citation quality checker validates document_id / chunk_id / grounded excerpt
- [x] internal RAG evaluation service computes coverage_score / citation_score / confidence / warnings
- [x] low_context / missing_citation / weak_match warnings are generated internally
- [x] extractive answer has citation_score=1.0 on grounded paths
- [x] summary mode still returns citations
- [x] archived filtering and retrieval API behavior remain unchanged
- [x] backend tests added for evaluation scores, missing citation warning, weak_match, and low_context
- [x] existing retrieval and internal RAG tests still pass
- [x] TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS / handbook mirror synchronized

### Boundary

- 当前实现已包含 Internal RAG Evaluation MVP，评估层仍是 deterministic，不调用 LLM。
- 不实现 frontend、不实现 embedding、不实现 pgvector、不实现真实 LLM provider、不实现 PostgreSQL retrieval backend。
- 继续保持 `/api/v1/document-retrieval/search` contract、scoring 和 response shape 不变。

## Sprint 9.3: Internal RAG Evaluation + Citation Quality MVP

### Current State

Internal RAG 已具备 deterministic answer assembly 和内部 evaluation / citation quality checking。

### Target State

未来若接入 LLM provider，仍要复用当前 evaluation contract、citation quality checker 和 warning taxonomy。

### Planned

- 继续保持 `/api/v1/internal-rag/answer` 对外 response backward compatible。
- 未来评估规则可扩展，但不能破坏 current warning taxonomy 和 retrieval boundary。

## Sprint 9.2: Internal RAG MVP without LLM

### Sprint Result

- [x] POST /api/v1/internal-rag/answer implemented
- [x] InternalRagService added on top of DocumentRetrievalProvider
- [x] extractive answer assembly uses top retrieval excerpts
- [x] summary mode is deterministic and does not call an LLM
- [x] citation validation returns grounded citations for each used excerpt
- [x] invalid_question / insufficient_context / citation_required behavior covered
- [x] archived documents are excluded unless include_archived=true
- [x] backend tests added for extractive success, summary determinism, no context, empty question, citations, and archived exclusion
- [x] existing retrieval tests still pass
- [x] TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS / handbook mirror synchronized
- [x] retrieval API behavior remains unchanged

## Sprint 8.3: Retrieval Repository Abstraction + Worktree Cleanup

### Current State

Document Retrieval service 已改为依赖 `DocumentRetrievalProvider`，不再直接依赖 raw chunk storage。

### Target State

Internal Document Retrieval 继续保持 keyword-only 行为，但检索后端边界已经独立出来，后续可替换成 PostgreSQL full-text 或其他 provider。

### Planned

- 保持 `POST /api/v1/document-retrieval/search` contract 不变。
- 保持 scoring / sorting / response shape 不变。
- 继续不实现 RAG、embedding、pgvector、frontend。

## Sprint 9.1: Internal RAG Contract Freeze

### Sprint Result

- [x] `POST /api/v1/internal-rag/answer` contract frozen
- [x] internal_rag.started / retrieval_completed / answer_generated / failed frozen
- [x] invalid_question / retrieval_unavailable / insufficient_context / citation_required / provider_timeout / repository_error frozen
- [x] Internal RAG Flow / Retrieval to Citation Flow / Future LLM Provider Flow / Future Approval Integration Flow added to Architecture
- [x] Prompt Standard updated with Internal RAG prompt family
- [x] TASK / ROADMAP / PROJECT_BACKLOG / CHANGELOG / DECISIONS / handbook mirror updated
- [x] retrieval API behavior unchanged

### Boundary

- 只冻结 Internal RAG contract，不实现 RAG。
- 不调用 LLM、不实现 embedding、不实现 pgvector、不实现 frontend。
- 继续保持 retrieval API 行为、评分和返回结构不变。

### Current State

Internal RAG 只是基于 Document Retrieval Provider 的上层 contract，没有实际回答引擎。

### Target State

未来 Internal RAG 将成为 retrieval 之后、approval 之前的稳定 grounded answer boundary。

### Planned

- 继续保持 `/api/v1/internal-rag/answer` 与 `/api/v1/document-retrieval/search` 分离。
- 未来 summary mode 可接入可替换 LLM provider，但不得破坏 contract。

## Sprint 8.2: Document Retrieval API MVP Implementation

### Current State

Document Retrieval API 已实现，且严格遵守 Sprint 8.1 冻结 contract。

### Target State

Internal Document Retrieval 成为 chunk 与 future RAG 之间的稳定只读边界。

### Planned

- 后续可在不破坏 contract 的前提下引入 PostgreSQL full-text / hybrid search。
- 继续保持 Retrieval 仅为只读边界，不接入 LLM answer generation。

## Epic 14: Engineering Standards（Final Freeze）

- [x] 新增 `docs/development/MASTER_PROMPT.md`
- [x] 新增 `docs/development/CODING_STANDARD.md`
- [x] 新增 `docs/development/DEVELOPMENT_GUIDE.md`
- [x] 新增 `docs/architecture/AI_AGENT_DESIGN_GUIDE.md`
- [x] 新增 `docs/contracts/API_CONTRACT.md`
- [x] 新增 `docs/contracts/EVENT_CONTRACT.md`
- [x] 新增 `docs/development/PROMPT_STANDARD.md`
- [x] 在 `docs/ai-agent-retail-handbook-v3/docs/` 建立 handbook 镜像
- [x] 扩展 `../doc-sync.manifest.json` 以纳入 Engineering Standards 同步组
- [x] 冻结 Architecture / Workflow / Contract / Development Standard 文档入口

当前边界：

- 本次不修改 `backend/`
- 本次不修改 `frontend/`
- 本次不修改 `scripts/`
- 本次不新增业务代码
- 本次不修改数据库 schema

下一任务：

- 在 contract 不变前提下，评估 retrieval ranking 的可解释性、filter coverage 和 future search backend 替换点。

## Epic 0: Enterprise Platform Architecture Evolution

### Current State

当前项目名称保持为 `Retail Insight AI`，它是 `Enterprise Retail Intelligence Platform (ERIP)` 的 Current MVP；当前仓库仍是零售分析 Domain 的参考实现，尚未演进成完整企业平台。

### Target State

未来目标是演进到：

`Enterprise Retail Intelligence Platform (ERIP)`

但当前不得把项目描述为 ERIP 已存在或已实现；ERIP 只能作为 Target 企业平台来表达。

### Planned

- [ ] Architecture Freeze
- [ ] Directory Refactor
- [ ] Repository Abstraction
- [ ] Workflow Abstraction
- [ ] Provider Abstraction
- [ ] Documentation Standard
- [ ] Testing Standard

## Epic 0 Deliverables

- [ ] Architecture Freeze
- [ ] Directory Freeze
- [ ] Repository Freeze
- [ ] Provider Freeze
- [ ] Workflow Freeze
- [ ] Database Freeze
- [ ] Testing Freeze
- [ ] Documentation Freeze

## Epic 12: Retrieval and RAG Platform

### Current State

当前项目尚未实现完整 Retrieval Layer。

当前只存在零售分析主链路中的简化 KPI / Research 路径，不代表已经具备完整 RAG 平台能力。

### Target State

未来 Retrieval and RAG Platform 不只包括社内文档 RAG，还包括：

- 结构化业务数据检索
- 社内文档检索
- 互联网检索
- 多来源上下文合并
- 引用与来源追踪
- 幻觉风险控制
- 检索效果评估

### Planned

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

当前仓库仍以现有 `backend/`、`frontend/`、`docs/` 为主，不代表平台目标结构已全部落地。

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

上述结构是 ERIP 目标架构视图，当前尚未全部实现。

### P0

- [ ] 确认项目目录结构
- [ ] 确认 Docker 环境
- [ ] 确认 .gitignore 是否保护敏感文件
- [ ] 确认 Document Upload 流程

## Phase 1 到 Phase 8 实施计划

## Definition of Done

以后任何一个 Phase 完成必须同时满足：

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

只要任一项未完成，对应 Phase 不能标记为完成。

## Handbook 同步规则

- 每个 Phase 完成后，必须同步更新 `docs/ai-agent-retail-handbook-v3/` 下对应文档。
- Handbook 同步至少覆盖：
  `TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/architecture/ARCHITECTURE.md`、`docs/governance/CHANGELOG.md`、`docs/governance/DECISIONS.md`。
- 如果本次变更涉及测试、流程、架构、运行方式，还必须同步检查并更新：
  `08_架构图册.md`、`09_系统设计书.md`、`10_Production_Roadmap.md`。
- 未完成 Handbook 同步，不得将对应 Phase 标记为完成。
- 所有核心架构图必须三语言维护：
  English、中文（简体）、日本語。

## 测试用例文档规则

- 每个测试用例必须包含：
  - 用例目标
  - 前端操作流程
  - 后端处理流程
  - 数据输入来源
  - 预期输出
  - 验收标准
  - Mermaid 前端流程图
  - Mermaid 后端流程图

## 架构文档规则

- 架构文档必须包含：
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

- [x] 是否完成
- [x] Handbook 文档已同步
- 目标：
  建立本地可运行的文件化输入基础，支持 CSV / JSON / Markdown 作为业务数据、Research 数据和文档数据的输入来源。
- 修改范围：
  `backend/app/` 数据加载层、Provider 组合方式、示例数据目录约定、README / RUNBOOK / VERIFY 文档，并为后续 Approval Workflow 预留报告状态边界。
- 验收标准：
  Backend 可以从约定目录读取 CSV / JSON / Markdown；KPI 与 Research 不再依赖写死示例值；本地运行无需真实数据库和外网；Report 当前仍直接生成，但状态模型已预留后续审批流扩展。
- 测试方法：
  运行文件加载单元测试；执行本地 API 创建任务；验证 hybrid 报告内容来自文件输入；验证缺失文件时返回标准错误；记录后续 Approval Workflow 测试预留项。
- 风险：
  文件格式不统一、编码问题、版本命名混乱、示例数据与代码契约不一致。

### Phase 1.5: Data Contract Freeze + Approval State Machine Design

- [x] 是否完成
- [x] Handbook 文档已同步
- 目标：
  固化 Phase 1 文件输入契约、导入错误模型和 Report / Approval 状态机，为 Phase 2 PostgreSQL 持久化与后续承認ワークフロー提供唯一设计依据。
- 修改范围：
  `docs/architecture/DATA_CONTRACTS.md`、`docs/architecture/APPROVAL_WORKFLOW.md`、`docs/database/DATABASE.md` 以及治理文档、架构文档、handbook 同步文档。
- 验收标准：
  业务 CSV、Research JSON、Documents Markdown 契约冻结；导入错误模型冻结；审批状态机冻结；Phase 2 表设计准备项冻结。
- 测试方法：
  文档审计；对照 Phase 1 已落地文件输入实现；确认状态机、Mermaid 图和 PostgreSQL 准备项已同步到主项目与 handbook。
- 风险：
  文档与代码未来漂移、审批状态与任务状态语义混淆、导入错误模型与实现不一致。

### Phase 2: PostgreSQL 持久化基础

- [ ] 是否完成
- [x] Handbook 文档已同步
- 当前状态：
  `Code implemented`
  `InMemory path verified`
  `PostgreSQL schema implemented`
  `PostgreSQL repository tests prepared`
  `PostgreSQL verification script added`
  `PostgreSQL real integration test pending`
  `Status: In Progress / Partially Verified`
- 目标：
  为 Task、Event、Report 和后续导入记录建立 PostgreSQL 持久化基础，同时保留本地可切换运行能力。
- 修改范围：
  `backend/app/config/`、`backend/app/db/`、`backend/app/repositories/`、`backend/app/models/`、`backend/tests/`、`backend/db/`、`.env.example`、`docker-compose.yml`、治理文档与 handbook。
- 验收标准：
  `REPOSITORY_BACKEND` 支持 `inmemory / postgres`；默认仍为 `inmemory`；Task / Event / Report 具备 PostgreSQL Repository；`data_imports`、`import_errors`、`approval_requests`、`approval_events` 完成 schema 与基础模型预留；当前 `reports.approval_status` 仍写入 `generated`。
- 测试方法：
  InMemory 全量回归；Repository backend switch 单元测试；PostgreSQL Repository 集成测试覆盖 create task、append event、save report、get report；当前环境缺少 `psycopg` / Docker 时记录跳过原因并提供手动命令。
- 当前未验证原因：
  当前环境缺少 Docker CLI；当前环境未安装 `psycopg` 到实际运行 venv；PostgreSQL 集成测试当前被 skip。已新增 `./scripts/verify_postgres_phase2.sh` 统一输出跳过原因与手动验证命令。外部 handbook 同步脚本因缺少同级 `../ai-agent-retail-handbook-v3/` 工作区而未执行。
- 下一步验证命令：
  `./scripts/verify_postgres_phase2.sh`
  或手工执行：
  `docker compose up -d postgres`
  `cd backend`
  `source .venv/bin/activate`
  `pip install -r requirements.txt`
  `REPOSITORY_BACKEND=postgres python -m unittest tests.test_postgres_repositories -v`
- 风险：
  本地环境数据库依赖增加、Schema 演进成本、连接池与事务边界设计不当、未完成真实 PostgreSQL 联调前不可宣称 Phase 2 全部关闭。

### Phase 3: 社内文档上传与入库

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  支持社内文档上传、元数据登记、原文保存和可追踪的数据版本管理。
- 修改范围：
  上传 API、文件存储路径、文档元数据表、前端上传入口、审计字段、运行手册。
- 验收标准：
  可上传受支持格式文档；系统记录上传者、时间、文件名、版本；上传失败有标准错误与日志。
- 测试方法：
  API 上传测试、非法文件测试、重复上传测试、前端上传流程测试、文档元数据查询测试。
- 风险：
  文件大小限制、编码与格式兼容、权限边界、敏感文档泄露风险。

### Phase 4: 切分与检索基础

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  建立文档切分、索引登记、基础检索和来源引用能力，为知识库问答与审批提供证据链。
- 修改范围：
  Chunk Pipeline、Chunk 配置、Retriever 抽象、引用格式、评估样例、Architecture 文档。
- 验收标准：
  文档可切分并入库；可根据查询返回 Top-K 片段与来源；报告可展示引用来源。
- 测试方法：
  Chunk 单元测试、检索召回测试、固定问答样例测试、来源引用验证。
- 风险：
  Chunk 策略不稳定、召回质量差、索引与原文版本不一致。

### Phase 5: 审批 Workflow

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  建立可审计的审批 Workflow，支持人工确认、状态流转、审批日志和失败恢复。
- 修改范围：
  LangGraph State / Node / Edge、审批表结构、审批 API、前端审批页面、日志与审计文档。
- 验收标准：
  审批任务可进入待审批、已批准、已拒绝状态；状态流转可追踪；不可逆动作有人工确认。
- 测试方法：
  Workflow 状态迁移测试、审批 API 测试、前端审批流程测试、异常恢复测试。
- 风险：
  状态机复杂度上升、幂等性不足、人工操作与自动执行边界不清。

### Phase 6: 互联网检索能力

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  在受控边界内引入互联网检索能力，用于市场趋势、竞品与外部公开信息补充。
- 修改范围：
  Search Provider 抽象、结果清洗、来源可信度规则、超时与重试、开关配置、审计说明。
- 验收标准：
  可按配置启用或禁用互联网检索；结果包含来源；外网失败时系统能降级而非整体崩溃。
- 测试方法：
  Provider 合同测试、失败降级测试、来源格式测试、手工验证检索结果与报告引用。
- 风险：
  外部信息时效与准确性风险、引用不可控、网络超时与成本不可预测。

### Phase 7: LangChain + LangGraph 工作流整合

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  在保持现有 LangGraph 可控状态编排的前提下，引入 LangChain 组件化能力，统一 Tool、Prompt、Retriever 和 Chain 边界。
- 修改范围：
  Workflow 编排层、Tool / Retriever 适配层、Prompt 管理、Chain 组合、架构文档与 ADR。
- 验收标准：
  LangChain 组件与 LangGraph Workflow 边界清晰；核心流程仍由 LangGraph 状态机控制；组件可替换。
- 测试方法：
  Workflow 集成测试、Tool 调用测试、Prompt 回归测试、故障回退测试。
- 风险：
  双框架职责重叠、抽象层过多、调试成本上升。

### Phase 8: 测试体系与流程图文档

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 目标：
  建立完整测试用例、测试方法、前后台程序流程图和架构文档，使项目达到可交接和可审计水平。
- 修改范围：
  Backend tests、Frontend tests、集成测试、验证清单、`docs/architecture/ARCHITECTURE.md`、`README.md`、`VERIFY_CHECKLIST.md`。
- 验收标准：
  核心流程覆盖单元、集成、端到端验证；架构图、数据流图、审批流图、上传与检索流程图齐全且与代码一致。
- 测试方法：
  执行 `./scripts/run_tests.sh`、补充人工验证步骤、按文档逐项验收。
- 风险：
  文档与实现脱节、测试过慢、样例数据不足导致覆盖失真。

### Epic: Semantic RAG / Vector Retrieval Upgrade

- [ ] 是否完成
- [ ] Handbook 文档已同步
- 状态：Planned / Future / Target

#### Current State

- 当前 Document Upload / Import / Chunk 已有基础能力。
- 当前检索以 Keyword Retrieval 为主，仍然依赖词面匹配与已有 chunk 结果排序。
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

#### Tasks

1. 设计 Embedding Provider 接口
   - [ ] OpenAI Embedding
   - [ ] Gemini Embedding
   - [ ] BGE / 本地 Embedding
   - [ ] Provider fallback
   - [ ] 配置项通过 `.env` 控制
2. 设计 Vector Store 接口
   - [ ] pgvector 优先
   - [ ] Qdrant / Milvus 作为未来扩展
   - [ ] 不要直接把业务代码绑定到具体向量库
3. 引入 LangChain
   - [ ] 仅用于 RAG 编排
   - [ ] 不替代 LangGraph
   - [ ] 定义 LangChain 与 TaskService / LangGraph 的边界
   - [ ] 定义 Retriever、Prompt、Context Builder 的职责
4. Document Chunk Metadata 升级
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
5. Embedding Pipeline
   - [ ] chunk -> embedding
   - [ ] embedding cache
   - [ ] re-embedding policy
   - [ ] document update 后重建 embedding
   - [ ] archived document 的向量处理策略
6. Hybrid Retrieval
   - [ ] Keyword Search
   - [ ] Vector Search
   - [ ] Metadata Filter
   - [ ] ACL Filter
   - [ ] Score Merge
   - [ ] Top-K
7. Rerank
   - [ ] Cross Encoder / LLM rerank 作为未来目标
   - [ ] 当前先设计接口和测试边界
8. Citation / Source Trace
   - [ ] answer 必须引用 `document_id` / `chunk_id` / `version`
   - [ ] 报告中保留 source trace
   - [ ] 与 Audit Log 未来集成
9. Retrieval Evaluation
   - [ ] `recall@k`
   - [ ] `MRR`
   - [ ] groundedness
   - [ ] citation accuracy
   - [ ] no-result rate
   - [ ] latency
10. Tests
   - [ ] unit test
   - [ ] retrieval test
   - [ ] embedding mock test
   - [ ] vector store contract test
   - [ ] LangChain integration boundary test
11. Documentation
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

## 本次工作完成标准

- [x] PROJECT_BACKLOG.md 已更新
- [x] TASK.md 已更新
- [x] CHANGELOG.md 已更新
- [x] AGENTS.md 规则未被破坏

## 下一步建议

优先进入 Phase 2 设计与最小实现：基于已冻结的 `DATA_CONTRACTS`、`APPROVAL_WORKFLOW`、`DATABASE` 文档，为 Task / Report / Event / Import / Approval 建立 PostgreSQL Repository 边界。
## Governance V2 升级记录

- [x] 创建 `ROADMAP.md`
- [x] 创建 `docs/architecture/ARCHITECTURE.md`
- [x] 创建 `docs/governance/DECISIONS.md`
- [x] 更新项目 `AGENTS.md` 的开发前读取顺序
- [ ] 根据项目实际状态完善 Roadmap 与 Architecture

## 2026-07-02 文档同步器

- [x] 建立 retail-insight-ai 与 ai-agent-retail-handbook-v3 的文档同步映射
- [x] 新增跨项目文档同步脚本 `../scripts/sync_retail_handbook_docs.py`
- [x] 新增同步清单 `../doc-sync.manifest.json`

<!-- DOC-SYNC:START group=governance -->
## 文档同步块

- group: `governance`
- file: `retail-insight-ai/TASK.md`
- self_sha256: `d5cedb3877a8682b35aac0736259b9359bc3cad610d405249b565f64c9b589f7`
- peers:
- `retail-insight-ai/ROADMAP.md` | sha256=3c656b952e6f27c3769dfacedbb7f097aba52bf1e7af1977d6e11cbf0b90aa0a | # retail-insight-ai Roadmap / 最后更新：2026-07-07 / ## 当前阶段 / 待根据项目现状确认。
- `retail-insight-ai/docs/governance/PROJECT_BACKLOG.md` | sha256=611bb721ffe36ce4c3c4c1be6b82709516c6a46118beda941a0e7cf442e394ed | # retail-insight-ai Project Backlog / 最后更新：2026-07-08 / ## 项目目标 / 构建 `Enterprise Retail Intelligence Platform (ERIP)` 的目标平台蓝图；当前仓库中的 `Retail Insight AI` 仅表示该目标平台的 Current MVP，包含：
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
