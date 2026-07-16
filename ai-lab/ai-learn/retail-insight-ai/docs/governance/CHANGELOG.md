# retail-insight-ai CHANGELOG

# CHANGELOG

## 2026-07-16 ERIP PostgreSQL Persistent Audit

- 新增 PostgreSQL-only `PersistentAuditService` 与 FastAPI yield Dependency；InMemory Audit 保持冻结且默认 backend 不变。
- AuditLog/API 增加 `occurred_at`、actor username/role、action、permission、HTTP method/path/status 等企业审计字段，同时保留旧字段兼容。
- Login 记录 `login.success/login.failure`；Bearer 401、Permission 403、Document、Retrieval、Analysis、Approval、Audit Read、Security Catalog 纳入统一持久审计。
- PostgreSQL Unit of Work 增加 nested savepoint；成功业务与审计原子提交，业务失败回滚自身写入后保留 failure event/audit，审计写失败不返回业务成功。
- Audit 查询支持 actor、action、resource、result、时间、request_id、limit/offset 和稳定倒序；Audit API 仍无修改或删除入口。
- 新增 `20260716_03_persistent_audit` migration：兼容旧 `failed`、增加 nullable 列与 4 个常用查询索引，不删除历史数据。
- 最终验证：InMemory 183（1 expected skip）、PostgreSQL 191（0 skip）、Frontend 47/47、production build、compileall、migration round-trip、diff-check 全绿。

## 2026-07-15 ERIP Enterprise RBAC Authorization

- 新增集中式 RBAC Contract：Role、Permission、Role Mapping、Authorization Result、Permission Checker、Permission Error 与 Forbidden Error。
- 新增 Permission Registry、Permission Resolver、Authorization Service 与 `require_permission()` FastAPI Dependency；JWT Payload 继续只承载身份，不写入 permission matrix。
- 冻结 admin / manager / employee 与 10 项能力权限；未知角色使用空权限集 fail-closed，不抛出 ValueError 或返回 500。
- Documents、Document Chunk/Import、Retrieval、Internal RAG、Tasks、Approval、Audit 与 Security Catalog 使用声明式 Permission Dependency；业务 Router/Service 不写 role if 判断。
- Health、Login、Swagger/OpenAPI 保持匿名，`GET /api/v1/users/me` 保持 authentication-only；受保护 API 继续使用 Swagger `BearerAuth`。
- 权限不足统一返回 403 `forbidden`，安全 detail 包含 `permission` 与 `role`，且不错误返回 401 或 `WWW-Authenticate`。
- 新增 12 个 RBAC 单元/API 测试并更新安全目录契约测试；InMemory 182 passed（skip 1）、PostgreSQL 187 passed（skip 0）、Frontend 47/47、build、compileall 全绿。
- 本轮未修改 JWT Contract、Repository、Alembic、Migration、schema、Embedding、pgvector、Retrieval/Reranker 实现、Frontend、README、Learning 或 handbook。

## 2026-07-15 ERIP Enterprise JWT Authentication

- 新增集中式 JWT Authentication Framework：Access Token、Token Payload、Current User、Authentication Error、JWT Config / Provider / Service / Dependency。
- 新增 `POST /api/v1/auth/login`，使用 passlib + bcrypt 校验 admin / manager / employee deterministic test users；密码只以 bcrypt hash 存储。
- JWT Payload 固定 `sub / user_id / username / role / iat / exp / jti`，默认 30 分钟、唯一 jti，不写入 permissions 或 permission matrix。
- Health、Login、Swagger/OpenAPI 保持匿名；其余业务 API 统一经 `get_current_user()` Bearer dependency 认证，Swagger 提供 `BearerAuth` Authorize。
- 缺失 Token、非法 Header、非法签名、非法 Payload、Token Expired 与 Login Failure 全部稳定返回 401，并保留 `WWW-Authenticate: Bearer`。
- 新增 16 个 Authentication / Settings 测试并为既有 API 回归注入真实测试 JWT；InMemory 170 passed（skip 1）、PostgreSQL 175 passed（skip 0）、Frontend 47/47、build、compileall 全绿。
- 本轮未实现 Refresh Token、用户数据库或 RBAC 扩展，未修改 Repository、Alembic、Migration、schema、Frontend、README、Learning 或 handbook。

## 2026-07-14 ERIP Enterprise Reranker

- 新增独立 Reranker contract、deterministic provider、集中配置与 service，使用关键词覆盖率、原 retrieval score、位置和 SHA-256 稳定排序。
- Internal RAG 现在按 `DocumentRetrievalService -> Top-N -> RerankerService -> Final Top-K` 编排；不修改 chunk 内容、retrieval score、Repository 或既有 API contract。
- disabled、provider 缺失或异常时保留 retrieval 顺序并返回正常结果，同时记录 reranker fallback 事件元数据。
- 新增 13 个 reranker/pipeline/fallback 测试；InMemory 154（skip 1）、PostgreSQL 159（skip 0）、Frontend 47/47、build、compileall 全绿。

## 2026-07-14 ERIP Embedding + Vector/Hybrid Retrieval

- 新增固定 384 维 Embedding Contract、显式 deterministic test provider 和统一输出验证，不调用外部 API。
- `DocumentChunkRepository` 双 backend 支持可空向量、更新、读取和 cosine 检索；API 不暴露原始 embedding。
- Document Retrieval 兼容默认 keyword，并新增 vector/hybrid、top_k、document filter、稳定 score 与 fallback。
- 新增 `20260714_02_chunk_embeddings` migration 和 cosine HNSW schema 基线，downgrade 不删除共享 vector extension。
- 默认 Baseline 全绿；真实 pgvector migration 因 PostgreSQL 16 系统未安装 extension 而阻塞，失败事务已完整回滚。

## 2026-07-14 ERIP Enterprise Phase 2B Baseline Gate + Repository Audit

- 重新执行 `./scripts/run_tests.sh`，确认 Backend tests、Frontend tests、Frontend build 与 Python compileall 可通过。
- 昨天记录的 4 个 Frontend timeout 用例本轮未复现稳定失败。
- 首次 Baseline 新观察到 `src/App.test.tsx` 中 `insufficient_context` 学习侧栏用例出现一次性 timeout；定向复跑和整份测试文件复跑通过，暂记为 flaky 风险观察，不修改生产代码。
- 审计 Repository 双后端边界：默认保持 `REPOSITORY_BACKEND=inmemory`，`postgres` 仅显式启用，连接失败不回退，Service 继续依赖接口，API 继续经 Service 访问仓储。
- 当前环境未设置 `DATABASE_URL`，真实 PostgreSQL integration suite 按设计安全跳过；本轮不宣称 PostgreSQL 重启持久化与持久化 Retrieval 已再次本机验证。

## 2026-07-12 Scenario01 Business Sample Data

- 新增 `docs/learning/sample-data/Scenario01_Sales_Decline/` 企业业务学习样本文档集。
- 统一关东地区饮料销售下降场景的销售、库存、促销、顾客、竞品、KPI、RAG、Analysis、Approval 与业务测试脚本口径。
- 仅补充学习资料，不修改 backend、frontend、API、Workflow 或业务逻辑。

## 2026-07-11 API Case Input and Learning Trace Alignment

- 对齐 `docs/learning/01_Foundation/LEARNING_API_WALKTHROUGH.md` 的 24 个 API Case 输入参数说明。
- 为 `GET /api/v1/documents` 补齐 Router、Service、Repository 的最小 Learning Trace。
- 未修改 API 业务逻辑、Schema、测试、Learning Trace 核心框架或 Repository 查询逻辑。

## 2026-07-09

### Documentation

Freeze LEARNING_API_WALKTHROUGH.md V1.0

完成：

- Learning Trace 统一
- Source Chain 统一
- Console Log 示例统一
- Execution Flow 统一
- Request / Background 学习模型统一

## 2026-07-08 ERIP Worldview Alignment

- 统一平台命名：`Enterprise Retail Intelligence Platform (ERIP)` 作为最终企业平台名称，`Retail Insight AI` 只作为 Current MVP / PoC / Early Prototype。
- `README.md`、`ROADMAP.md`、`TASK.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/architecture/ARCHITECTURE.md`、`docs/ai-agent-retail-handbook-v3/PROJECT_BIBLE.md` 已同步统一世界观。
- `docs/ai-agent-retail-handbook-v3/09_系统设计书.md`、`08_架构图册.md`、`10_Production_Roadmap.md`、`12_ADR.md`、`INTERVIEW_GUIDE.md` 已同步 `Current / Target / Planned` 标记与核心术语。
- 核心术语统一为 `Task API`、`TaskService`、`LangGraph Workflow`、`Fixed KPI Workflow`、`Research Agent`、`Report Generator`、`Repository Pattern`。
- 平台演进术语统一为 `SQLite(Current)`、`Docker(Current)`、`PostgreSQL(Target)`、`pgvector(Target)`、`Hybrid Retrieval(Target)`、`RBAC(Target)`、`Audit Log(Target)`、`OpenTelemetry(Target)`、`Redis(Target)`、`RabbitMQ(Target)`、`Kubernetes(Target)`。
- Documentation Only：未修改 backend、frontend、tests、scripts、API 行为或业务逻辑。

## 2026-07-07 Technical Architecture Handbook Alignment

- `docs/ai-agent-retail-handbook-v3/09_系统设计书.md` 新增 `7.0 Technical Architecture（技术架构总览）`，补齐 Technology Stack Overview、Layered Architecture、AI Framework Relationship、Retrieval Pipeline、Technology Evolution、Enterprise Deployment、Current vs Target Matrix。
- `docs/ai-agent-retail-handbook-v3/09_系统设计书.md` 将 Document Platform 主题统一收束为 `Appendix A Document Platform Design`，整理为 `A.1~A.6`，并同步更新目录、交叉引用与章节编号。
- `docs/ai-agent-retail-handbook-v3/08_架构图册.md` 追加 Technology Stack Architecture、AI Framework Relationship、Retrieval Pipeline、Technology Evolution、Enterprise Deployment Topology、Container Architecture、AI Component Architecture、Create Task End-to-End 八组 Mermaid 图，并在 RC 收口时把 `28 / 29 / 33 / 34` 调整为不同视角，避免重复维护同构 Mermaid。
- `docs/ai-agent-retail-handbook-v3/09_系统设计书.md` 在 RC 收口中统一 `Related ADR` 格式、补齐 `See Figure / See Chapter` 引用，并修复 Appendix A 与审计章节中的阶段口径和编号一致性问题。
- 统一术语为 `Keyword Retrieval (Current)`、`Hybrid Retrieval (Target)`、`Vector Database (Target)`、`Embedding (Planned)`、`LangGraph = Workflow Orchestration`、`LangChain = RAG Orchestration`、`Repository Pattern`、`Application Service`、`HTTP Boundary`。
- `docs/ai-agent-retail-handbook-v3/PROJECT_BIBLE.md` 与 `README.md` 已同步新的 Technology Stack 入口与统一口径，并明确 `09_系统设计书.md` Chapter `7.0` 与 `08_架构图册.md` Figure `28~35` 为技术演进唯一维护入口。
- Documentation Only：未修改 backend、frontend、tests、scripts、API 行为或业务逻辑。

## 2026-07-07 API Walkthrough Repair

- 修复 `docs/learning/LEARNING_API_WALKTHROUGH.md` 被截断的问题，恢复 `01~23` 全部接口章节和补充接口章节。
- 保持原有接口顺序、Swagger 操作、输入输出、后台日志和程序调用流程不变。
- 将错位的“源码学习说明”按接口归位，避免 Health 混入 Task、Document、Approval、Security、Audit 相关源码。
- 每个接口只保留一套源码学习说明，并限制为说明当前接口 `对应源码` 中的文件。
- Documentation Only：未修改 backend、frontend、tests、scripts、API 行为或业务逻辑。

## 2026-07-06 Learning Trace Phase 4

- Learning Trace 升级为源码一眼可读 block，按 `HTTP Request -> Router -> Controller File -> Controller Method -> Return -> Schema File -> Schema -> HTTP Response` 展示。
- `backend/app/core/learning_trace.py` 按文件切换自动补出 `Controller File`、`Entering File`、`Schema File`、`Schema`，便于直接对照源码阅读。
- `GET /health` 与 `POST /api/tasks` 的学习顺序同步到 `docs/learning/LEARNING_API_WALKTHROUGH.md`，健康检查 schema 文件名修正为 `backend/app/schemas/health.py`。
- `LEARNING_TRACE=false` 时仍然不会输出新增学习日志。
- 本次保持 API 行为、响应 JSON、Swagger/OpenAPI、SSE 和业务逻辑不变。

## 2026-07-06 Backend Startup Recovery

- 修复后端本地启动失败的根因：`python-multipart` 未声明且当前工作区没有可用 `.venv`。
- 在 `backend/requirements.txt` 中补充 `python-multipart==0.0.20`，并创建 `.venv` 重新安装 backend 依赖。
- 使用 `cd backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000` 成功启动后端。
- 验证 `/health`、`/docs`、`/redoc`、`/openapi.json` 均返回 200。
- 在 `docs/learning/RUNBOOK_LOCAL.md` 末尾追加 Appendix A / Appendix B，只追加不改写原文。

## 2026-07-05 Learning Trace Phase 3

- learning trace 从单行 JSON 改为终端可读 block，便于学习调用链。
- `POST /api/tasks` 的学习链路会在后台任务完成后统一打印完整 block。
- `LEARNING_TRACE=false` 时仍然不会输出任何学习 trace。
- `docs/learning/LEARNING_API_WALKTHROUGH.md` 补充了可读格式说明和节点含义。
- 本次仅优化学习 trace 的显示格式，不修改 API 行为、返回值、Swagger、OpenAPI、SSE 或业务逻辑。

## 2026-07-05 Learning Trace Phase 2

- 学习日志升级为 `HTTP Request -> Router -> Service -> Workflow -> Provider -> Repository -> Schema(Response Model) -> HTTP Response`。
- `GET /health` 与 `POST /api/tasks` 输出更细的学习节点，便于按 `node / class / method / file` 阅读源码调用链。
- `LEARNING_TRACE=false` 时仍然不产生新增学习日志。
- `docs/learning/LEARNING_API_WALKTHROUGH.md` 增加 `Learning Trace Phase 2`，说明默认关闭、如何开启和如何关闭。
- 本次只增强 Learning Trace，不修改 API 行为、返回值、Swagger、OpenAPI、SSE 或测试逻辑。

## 2026-07-05 Learning Trace Phase 1

- 新增可关闭的 Learning Trace，用于学习 `GET /health`、`POST /api/tasks`、`GET /api/tasks/{task_id}`、`GET /api/tasks/{task_id}/events` 的调用链。
- `LEARNING_TRACE=false` 时完全关闭，不影响 API 行为、返回值、Swagger 或业务逻辑。
- 新增 `backend/app/core/learning_trace.py`，统一提供 `trace_enter()`、`trace_step()`、`trace_exit()`。
- `docs/learning/LEARNING_API_WALKTHROUGH.md` 新增 `Learning Trace（学习调用链日志）` 章节，说明开启时机、存在原因、阅读方式和 Swagger 配合方法。
- `.env.example` 增加 `LEARNING_TRACE=false`。
- 本次只做 Documentation + Learning Trace，不修改测试逻辑，也不扩大到其他 API。

## 2026-07-05 Documentation Organization + AI Agent Guide 中文化 Sprint

- `docs/` 下活动 Markdown 已按职责移动到 `learning/`、`architecture/`、`contracts/`、`development/`、`database/`、`governance/`。
- `README.md` 已同步新目录结构、学习路线和全量 Markdown 文档导航。
- `docs/learning/LEARNING_API_WALKTHROUGH.md` 保留主链路接口总览、每个接口详细表和程序调用流程。
- `docs/learning/TEST_CASES.md` 保留测试总览、每个测试文件详细表和后端程序流程，并新增“保护的 Bug / 风险”列。
- `docs/architecture/AI_AGENT_DESIGN_GUIDE.md` 已中文化，日语为辅，覆盖 Workflow vs Agent、Tool、Repository、Provider、RAGAnswerGenerator、LLMProvider、Retrieval、Approval、RBAC / Audit 和未来模型 Provider 接入方式。
- `docs/development/MASTER_PROMPT.md` 已补充文档合并、唯一主文档、归档候选区、学习内容保护和语言规则。
- Documentation Only：未修改 backend、frontend、scripts、Python、React、API、测试实现或业务逻辑。

## 2026-07-05 Documentation Readability Optimization Sprint

- `docs/learning/LEARNING_API_WALKTHROUGH.md` 调整为 `主链路接口总览 -> 接口详细表 -> 程序调用流程`。
- `docs/learning/LEARNING_API_WALKTHROUGH.md` 所有主接口统一采用详细表格，保留 Swagger 操作、输入、输出、后台 Log、源码、测试和下一步。
- `docs/learning/LEARNING_API_WALKTHROUGH.md` 程序流程统一写文件路径、类名、方法名。
- `docs/learning/TEST_CASES.md` 调整为 `测试总览 -> 测试详细表 -> 后端程序流程`。
- `docs/learning/TEST_CASES.md` 所有测试文件统一采用详细表格，保留测试目的、API、Swagger 操作、命令、输入、输出、后台 Log、源码和为什么设计。
- `docs/learning/TEST_CASES.md` 后端程序流程统一写文件路径、类名、方法名。
- Documentation Only：未修改 backend、frontend、scripts、Python、React、API、测试实现或业务逻辑。

## 2026-07-05 Documentation Governance V2

- `README.md` 升级为唯一知识导航中心，补齐全部 59 个 Markdown 文档链接、知识地图、学习路线流程图、当前完成情况矩阵和企业项目验证体系。
- `README.md` 增加文档责任表，明确唯一职责、是否唯一、是否允许新增同类文档。
- `docs/learning/LEARNING_API_WALKTHROUGH.md` 增加接口学习总表，同时保留每个接口的作用、Swagger 操作、输入、输出、后台日志、程序流程、源码、测试和下一步。
- `docs/learning/TEST_CASES.md` 增加测试总览表，同时保留每个测试文件的测试目的、API、命令、输入、输出、Swagger 操作、后台日志、程序流程、源码和设计理由。
- `RUNBOOK_LOCAL.md` 的启动、Swagger、ReDoc、OpenAPI、验证、测试和排错内容已由 README、LEARNING、TEST、VERIFY 承接，文件移动到 `docs/_archive_candidate/RUNBOOK_LOCAL.md`。
- `STUDY_PLAN_DAY1_DAY3.md` 已由 README 学习路线、接口学习、测试学习和源码阅读文档承接，移动到 `docs/_archive_candidate/root/STUDY_PLAN_DAY1_DAY3.md`。
- handbook 侧 `TASK.md`、`ROADMAP.md` 已由根目录同名主文档承接，移动到 `docs/_archive_candidate/handbook-root/`。
- handbook/docs 技术规范镜像已由主项目 `docs/` 承接，移动到 `docs/_archive_candidate/handbook-docs/`。
- `docs/_archive_candidate/README.md` 补充归档规则、当前归档候选文件、移动原因、停止维护状态和未来删除条件。
- `docs/ai-agent-retail-handbook-v3/README.md` 调整为长期知识库入口，不重复维护主项目介绍；技术规范镜像统一说明为引用或镜像。
- `docs/development/MASTER_PROMPT.md` 增加 Documentation Governance 永久规则，禁止删除学习内容、程序流程、Swagger 操作、后台 Log、输入输出和源码位置。
- Documentation Only：未修改 backend、frontend、tests、scripts、Python、React。

## 2026-07-05 Documentation Restore + Safe Merge Sprint

- `README.md` 恢复树形目录结构图、文档导航中心和企业项目测试体系说明。
- `docs/learning/LEARNING_API_WALKTHROUGH.md` 恢复分接口学习章节，并补回每个接口的完整学习流程。
- `docs/learning/TEST_CASES.md` 恢复分测试文件学习章节，并补回每个测试文件的程序运行流程。
- `RUNBOOK_LOCAL.md`、`VERIFY_CHECKLIST.md`、`docs/development/MASTER_PROMPT.md` 补充文档规则和验证体系说明。
- `docs/ai-agent-retail-handbook-v3/README.md` 补充根目录与 `docs` 目录职责说明。
- 本次仅修改文档，不修改 backend、frontend、scripts、业务代码、测试代码。

## 2026-07-05 Documentation Recovery + Governance Sprint

- `README.md` 重新恢复为项目总入口，补齐项目一句话介绍、当前已实现能力、部分完成能力、未来规划、项目验证体系、目录树、文档导航中心、学习路线、测试路线、源码阅读路线、面试准备路线和文档治理规则。
- `docs/learning/LEARNING_API_WALKTHROUGH.md` 恢复为按接口逐节展开的学习文档，覆盖 `GET /health`、tasks、documents、retrieval、internal-rag、approvals、security、audit 等主接口，不再用总表承载主内容。
- `docs/learning/TEST_CASES.md` 恢复为按测试文件逐节展开的学习文档，覆盖重点测试目的、输入、预想输出、Swagger 对应操作、后端程序流程、源码和设计理由。
- `RUNBOOK_LOCAL.md` 和 `VERIFY_CHECKLIST.md` 补充 Swagger、ReDoc、OpenAPI JSON 的区别，以及 `unittest` 必须在 `backend/` 目录执行的规则。
- `docs/development/MASTER_PROMPT.md` 补充永久文档保护规则，明确不能把 `TEST_CASES.md` 压缩成命令列表，也不能把 `LEARNING_API_WALKTHROUGH.md` 压缩成接口表格。
- `docs/ai-agent-retail-handbook-v3/README.md` 明确 handbook 根目录负责学习/面试，handbook/docs 负责技术规范镜像和治理记录。
- 新增 `docs/_archive_candidate/README.md`，先登记疑似重复文档与主维护文件，不移动、不删除任何文档。
- `docs/governance/PROJECT_BACKLOG.md` 增加“文档治理清单”章节。
- 本次仅修改 Markdown 文档，不修改 backend/app、backend/tests、frontend、scripts、业务逻辑、API 行为、测试实现。

## 2026-07-05 文档重构 V1

- `README.md` 重写为项目门户，补齐项目概览、架构、目录、文档导航和验证系统。
- `RUNBOOK_LOCAL.md` 重写为启动与排错指南，补齐每条命令的原因、结果、失败和验证。
- `docs/learning/LEARNING_API_WALKTHROUGH.md` 重写为初学者学习文档，补齐 Swagger、当前学习阶段、通用时序模板和常见失败速查。
- `docs/learning/TEST_CASES.md` 重写为学习导向测试文档，补齐 `Swagger` 和 `unittest` 的区别、每个测试保护的 bug 和能力。
- `CODE_STUDY_GUIDE.md` 重写为固定阅读顺序，明确 `Swagger -> API -> Service -> Repository -> Domain -> Tests`。
- `docs/ai-agent-retail-handbook-v3/INTERVIEW_GUIDE.md` 继续保持企业 AI 后端项目面试稿定位，作为唯一面试文档入口。
- 本次仅修改文档，不修改 backend、frontend、scripts、业务逻辑或测试实现。

## 2026-07-05 文档重构 V3

- `README.md` 重写为唯一项目入口，补齐项目介绍、当前实现范围、目录说明和文档导航中心。
- `docs/learning/LEARNING_API_WALKTHROUGH.md` 重写为中文主导的接口学习走读，补齐 Swagger / ReDoc / OpenAPI JSON、后台日志观察点和学习日志。
- `docs/learning/TEST_CASES.md` 重写为程序运行流程学习文档，补齐程序流转、后台日志观察点和学习日志。
- `RUNBOOK_LOCAL.md` 重写为启动与排错指南，补齐为什么执行、命令、成功判断、失败现象和修复方法。
- `VERIFY_CHECKLIST.md` 重写为启动完成检查清单，补齐检查项、命令、预想结果、失败现象和参考文档。
- `CODE_STUDY_GUIDE.md` 重写为源码阅读指南，补齐为什么要 `Service`、`Repository`、`Provider`、`Workflow`。
- `docs/ai-agent-retail-handbook-v3/INTERVIEW_GUIDE.md` 重写为企业 AI 后端项目面试稿，补齐中文回答与日语回答。
- 删除并收敛旧面试文档引用，统一指向 handbook 唯一入口。
- 本次仅修改文档，不修改 backend、frontend、scripts、API 行为、业务逻辑、数据库或测试实现。

## 2026-07-05 Documentation Consolidation Sprint 2

- README 增加“文档导航中心”，把项目入口、本地排错、验证清单、源码阅读、接口学习、测试学习、面试讲解、架构、契约、错误码、数据库、AI 执行规则、编码规范、开发流程统一串联。
- README 增加初学者只读 5 个文档、面试准备 3 个文档、开发维护再看哪些文档、不要一开始看的文档，以及文档数量控制规则。
- `docs/learning/LEARNING_API_WALKTHROUGH.md` 改为主链路接口学习表，补齐 Swagger 操作、输入、预期输出、成功后下一步、常见失败和源码位置。
- `docs/learning/TEST_CASES.md` 改为测试文件学习表，补齐测试目的、后端流程、Swagger/前端流程和设计理由。
- `docs/ai-agent-retail-handbook-v3/INTERVIEW_GUIDE.md` 改为适合日本项目面试的中文主导讲解稿，并加入日语回答要点。
- `RUNBOOK_LOCAL.md` 明确项目根目录脚本和 backend 目录 uvicorn 的不同执行方式，并补上 Swagger / ReDoc / OpenAPI JSON 的用途。
- `VERIFY_CHECKLIST.md` 增加失败时先看哪个文档。
- `CODE_STUDY_GUIDE.md` 增加每章推荐阅读文件和下一步看哪里。
- `docs/development/MASTER_PROMPT.md` 增加文档数量控制规则。
- 本次仅修改文档，不修改 backend/app、backend/tests、frontend、scripts。

## 2026-07-05 Sprint R3.1 Documentation Quality Refactor

- 将 `README.md` 重写为中文入口，并新增“第一次启动项目”章节，逐步说明命令、作用、成功标志、失败现象和下一步操作。
- 将 `docs/learning/LEARNING_API_WALKTHROUGH.md` 重写为按接口顺序展开的中文学习走读，每个接口都补齐接口作用、学习原因、Swagger 位置、输入、预期输出、知识点和源码位置。
- 将 `docs/learning/TEST_CASES.md` 重写为按测试文件逐项说明的中文文档，补齐测试目的、对应 API、源码位置、运行命令、输入、预期输出和设计理由。
- 将 `RUNBOOK_LOCAL.md` 改为“启动与排错指南”，并用“问题 → 原因 → 解决方法”重新组织。
- 将 `VERIFY_CHECKLIST.md` 改为启动完成检查清单，明确每项如何验证成功。
- 将 `CODE_STUDY_GUIDE.md` 为每章补齐学习目标、推荐阅读时间、推荐顺序和看完应掌握的内容。
- 本次仅做文档质量重构，不修改 Python 代码、测试代码或接口。

## 2026-07-05 Sprint R3 Learning Guide + Test Case + Interview Docs Optimization

- 统一最短学习路径到 `README.md`、`docs/learning/LEARNING_API_WALKTHROUGH.md`、`CODE_STUDY_GUIDE.md`。
- 新增 `docs/learning/TEST_CASES.md` 和 `docs/ai-agent-retail-handbook-v3/INTERVIEW_GUIDE.md`，分别用于测试总览和面试讲解。
- 更新 `README.md`、`RUNBOOK_LOCAL.md`、`VERIFY_CHECKLIST.md`、`CODE_STUDY_GUIDE.md`、`TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`。
- 新文档保留 English / 中文（简体） / 日本語 三语摘要，不把未完成能力写成已完成。
- 本次不新增业务功能，不改 frontend，不接 PostgreSQL，不接真实 LLM，不接 JWT/OAuth，不接 pgvector/MCP。

## 2026-07-05 Sprint R2 Runnable Learning MVP Verification

- 验证 `from app.main import app; print(app.title)` 和 `app.openapi()` 可正常运行。
- 通过 ASGI 直接确认最小可运行路径：health、task、document、pipeline、approval、security、audit。
- 新增 `docs/learning/LEARNING_API_WALKTHROUGH.md`，把 runnable learning 路径收敛成最短学习顺序。
- 更新 `README.md`、`RUNBOOK_LOCAL.md`、`VERIFY_CHECKLIST.md`、`CODE_STUDY_GUIDE.md`、`TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`。
- 本次不新增功能，不改 frontend，不接 PostgreSQL，不接真实 LLM，不接 JWT/OAuth，不接 pgvector/MCP。

## 2026-07-05 Final Wrap-up Sprint: Project Consolidation and Verification

- 本次仅做收口整理和验证，不新增功能，不改 frontend，不接 PostgreSQL，不接真实 LLM，不接 JWT / OAuth。
- `python3 -m unittest discover -s tests -v` 通过，`115` 个测试运行，`1` 个 PostgreSQL 相关测试因当前环境缺少 `psycopg` 跳过。
- `python3 -m compileall app tests` 通过。
- 当前已完成能力、未完成能力和项目边界已整理为三语摘要，并同步到 handbook mirror。
- 当前完成能力包括：Document Upload / Read / Archive / Import / Chunk / Retrieval、Internal RAG without LLM、LLM Provider Stub Seam、Approval Workflow、Approval RBAC、Approval Audit Middleware、Security Domain、InMemory Audit Log。
- 当前未完成能力包括：frontend UI、PostgreSQL repository full migration、real authentication、JWT/OAuth、real LLM provider、pgvector、internet search、MCP、production deployment。

## 2026-07-05 Sprint 11.3 RBAC Enforcement for Approval APIs

- 在现有 `SecurityService` current-user seam 上，只对 approval APIs 强制 RBAC，不扩展到 document / retrieval / RAG / task APIs。
- `POST /api/v1/reports/{task_id}/submit-approval` 现在要求 `report.submit_approval`；`GET /api/v1/approvals`、`GET /api/v1/approvals/{approval_id}` 要求 `approval.review`；`approve`、`reject`、`revise` 分别要求 `approval.approve`、`approval.reject`、`approval.revise`。
- default system admin placeholder user 继续通过所有 approval permission checks。
- permission denied 会写入 append-only audit fact，并以 `permission_denied` 返回 403。
- 新增 backend tests 覆盖允许路径、拒绝路径与 denied audit logging。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/governance/DECISIONS.md`、`docs/architecture/ARCHITECTURE.md`、`docs/contracts/API_CONTRACT.md` 以及 handbook mirror。
- 本次不修改 frontend、scripts 或 approval response shape。

## 2026-07-05 Sprint 11.2 Security Domain + InMemory Audit MVP

- 新增 security domain models：`User`、`Organization`、`Department`、`Role`、`Permission`、`Policy`。
- 实现 `GET /api/v1/users/me`、`GET /api/v1/security/roles`、`GET /api/v1/security/permissions` 和 `GET /api/v1/audit-logs`。
- 新增 `AuditLog`、`AuditRepository`、`InMemoryAuditRepository` 和 `AuditService`，并把审计写入边界做成 append-only seam。
- current user 使用 `user_id="system"` 的 placeholder principal，roles 预置为 `admin`，permissions 预置为 frozen catalog。
- `audit.log.created` / `audit.log.failed` 作为结构化日志事件记录审计追加成功和失败。
- 新增 backend tests，覆盖系统用户、冻结目录、审计追加、审计只读读取和 append-only 语义。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/governance/DECISIONS.md`、`docs/architecture/ARCHITECTURE.md` 以及 handbook mirror。
- 本次仍不实现真实认证、JWT、OAuth、RBAC enforcement、PostgreSQL audit repository 或 frontend 变更。

## 2026-07-05 Sprint 11.1 Enterprise Security Foundation Contract Freeze

- 冻结企业安全基础合同，覆盖 user / organization / department / role / permission / policy 概念。
- 冻结 `GET /api/v1/users/me`、`GET /api/v1/security/roles`、`GET /api/v1/security/permissions`、`GET /api/v1/audit-logs` 的未来读接口边界。
- 冻结 RBAC approval-action matrix、audit log contract、operation log contract 和 future authentication relationship。
- 更新 `docs/contracts/API_CONTRACT.md`、`docs/contracts/EVENT_CONTRACT.md`、`docs/contracts/ERROR_CATALOG.md`、`docs/architecture/ARCHITECTURE.md`、`docs/database/DATABASE.md`、`TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/governance/DECISIONS.md` 以及 handbook mirror。
- 本次不修改 backend、frontend 或 scripts。

## 2026-07-05 Sprint 10.2 Approval API MVP Implementation

- 在 frozen approval contract 上实现 backend-only Approval API MVP。
- 新增 `POST /api/v1/reports/{task_id}/submit-approval`、`GET /api/v1/approvals`、`GET /api/v1/approvals/{approval_id}`、`POST /api/v1/approvals/{approval_id}/approve`、`POST /api/v1/approvals/{approval_id}/reject`、`POST /api/v1/reports/{task_id}/revise`。
- 新增 immutable `ReportVersion`、`ApprovalRequest`、`ApprovalEvent`、InMemory approval repository 和 approval service / router / tests。
- approval submitted / approved / rejected / revised / failed events 进入 backend event trail。
- 继续保持 report / retrieval / internal RAG response contract 不变。
- Approval API / Approval Events / Approval Errors / Approval Architecture sections were checked and supplemented with 中文（简体） / 日本語 summaries where they were still English-only.

## 2026-07-04 Sprint 10.1 follow-up Trilingual Documentation Rule Freeze

- 冻结文档语言政策：所有人类可读项目文档默认采用 English / 中文（简体） / 日本語 三语。
- 明确 English-only 仅允许用于 code identifiers、API paths、class names、environment variables、enum values、error codes 和 event names。
- 更新 `docs/development/MASTER_PROMPT.md`、`docs/development/CODING_STANDARD.md`、`docs/development/DEVELOPMENT_GUIDE.md`、`docs/contracts/API_CONTRACT.md`、`docs/contracts/EVENT_CONTRACT.md`、`docs/contracts/ERROR_CATALOG.md`、`docs/architecture/ARCHITECTURE.md`、`TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/governance/DECISIONS.md` 以及 handbook mirror。
- 本次仅冻结规则，不重写旧文档正文。

## 2026-07-04 Sprint 10.1 Approval Workflow Contract Freeze

- 冻结 Approval Workflow contract，覆盖 `submit-approval`、`approvals list/detail`、`approve`、`reject`、`revise` 的 API 边界。
- 冻结 approval state machine：`draft`、`pending_approval`、`approved`、`rejected`、`revised`、`published`、`archived`。
- 冻结 approval events：`approval.submitted`、`approval.approved`、`approval.rejected`、`approval.revised`、`approval.published`、`approval.failed`。
- 冻结 approval error catalog，并明确 report revision relationship、audit relationship、future RBAC relationship。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/contracts/API_CONTRACT.md`、`docs/contracts/EVENT_CONTRACT.md`、`docs/contracts/ERROR_CATALOG.md`、`docs/database/DATABASE.md`、`docs/architecture/ARCHITECTURE.md`、`docs/governance/DECISIONS.md` 以及 handbook mirror。
- 本次不修改 backend、frontend 或 scripts。

## 2026-07-04 Sprint 9.5 LLM Provider Seam Stub MVP

- 新增 `StubLLMProvider` 作为本地 provider stub，不访问 OpenAI、Azure 或任何外部 API。
- 新增 `RAGAnswerGenerator`，并通过 `LLM_PROVIDER=stub` / `INTERNAL_RAG_USE_LLM=false` 控制是否启用 model seam。
- provider failure、timeout、invalid output、missing citation 都回退到 deterministic extractive answer。
- 记录 `provider_name`、`prompt_tokens`、`completion_tokens`、`estimated_cost`、`latency_ms` 占位信息，仅用于内部事件/日志，不暴露到 API response。
- 新增 `backend/tests/test_rag_answer_generator.py`，并确认 backend full suite 与 compileall 已通过。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/governance/DECISIONS.md`、`docs/architecture/ARCHITECTURE.md` 以及 handbook mirror。
- 本次不修改 `/api/v1/internal-rag/answer` response contract，不修改 frontend。

## 2026-07-04 Sprint 9.4 LLM Provider Seam Contract Freeze

- 冻结未来 `LLMProvider` interface concept、`RAGAnswerGenerator` concept 以及 prompt input/output contract。
- 冻结 provider error model：`llm_provider_unavailable`、`llm_provider_timeout`、`llm_output_invalid`、`llm_citation_missing`、`llm_cost_limit_exceeded`。
- 明确当前默认仍是 deterministic extractive fallback，不调用 LLM、不调用外部 provider。
- 记录 token / cost / latency tracking placeholders，供未来模型接入时使用。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/governance/DECISIONS.md`、`docs/development/PROMPT_STANDARD.md`、`docs/architecture/AI_AGENT_DESIGN_GUIDE.md`、`docs/architecture/ARCHITECTURE.md`、`docs/contracts/ERROR_CATALOG.md` 以及 handbook mirror。
- 本次不修改 backend、frontend 或 scripts，且不改变 `/api/v1/internal-rag/answer` response。

## 2026-07-04 Sprint 9.3 Internal RAG Evaluation + Citation Quality MVP

- 新增 internal RAG evaluation service，用于计算 `coverage_score`、`citation_score`、`confidence` 和 warnings。
- 新增 citation quality checker，验证 `document_id` / `chunk_id` / excerpt grounding 关系，并生成 `low_context`、`missing_citation`、`weak_match` warnings。
- `POST /api/v1/internal-rag/answer` 仍保持 backward compatible，对外 response 未增加新字段。
- `extractive` / `summary` 两种 answer mode 继续不调用 LLM、embedding 或 pgvector。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/governance/DECISIONS.md`、`docs/architecture/ARCHITECTURE.md` 以及 handbook mirror。
- `python3 -m unittest discover -s tests -v` 与 `python3 -m compileall app tests` 已通过。

## 2026-07-04 Sprint 9.2 Internal RAG MVP without LLM

- 实现 `POST /api/v1/internal-rag/answer`，基于现有 `DocumentRetrievalProvider` 进行 deterministic answer assembly。
- `answer_mode=extractive` 直接组装 top retrieval excerpts，并为使用的每个 excerpt 返回 citation。
- `answer_mode=summary` 采用稳定的本地摘要规则，不调用 LLM、embedding 或 pgvector。
- `invalid_question`、`insufficient_context`、`citation_required`、`archived exclusion` 行为已由 backend tests 覆盖。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/governance/DECISIONS.md`、`docs/architecture/ARCHITECTURE.md` 以及 handbook mirror。
- `python3 -m unittest discover -s tests -v` 与 `python3 -m compileall app tests` 已通过。

## 2026-07-04 Sprint 9.1 Internal RAG Contract Freeze

- 冻结 `POST /api/v1/internal-rag/answer`，定义 question / limit / include_archived / document_type / language / tags / answer_mode / require_citations 请求合同。
- 冻结 internal RAG response contract，包含 `answer`、`citations[]`、`retrieval_mode`、`answer_mode`、`confidence`、`warnings[]`。
- 冻结 `internal_rag.started`、`internal_rag.retrieval_completed`、`internal_rag.answer_generated`、`internal_rag.failed` 事件语义。
- 在 `docs/architecture/ARCHITECTURE.md` 增加 Internal RAG Flow、Retrieval to Citation Flow、Future LLM Provider Flow、Future Approval Integration Flow。
- 在 `docs/development/PROMPT_STANDARD.md` 增加 Internal RAG prompt family，在 `docs/contracts/ERROR_CATALOG.md` 增加内部 RAG 错误码分组。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/governance/DECISIONS.md` 以及 handbook mirror。
- 本次不实现 RAG、LLM、embedding、pgvector、frontend，且不修改 retrieval API 行为。

## 2026-07-04 Sprint 8.3 Retrieval Repository Abstraction + Worktree Cleanup

- 将 `POST /api/v1/document-retrieval/search` 的实现边界从 raw chunk storage 下沉到 `DocumentRetrievalProvider`。
- 新增 `backend/app/repositories/interfaces/document_retrieval_provider.py` 与 `backend/app/repositories/implementations/in_memory/document_retrieval.py`，并保留当前 `InMemoryKeywordRetrieval` 作为唯一实现。
- `backend/app/services/document_retrieval_service.py` 现在只负责 API、事件和错误边界，不再直接依赖 chunk repository。
- 更新 `backend/app/config/container.py` 以在组合根中装配 retrieval provider。
- 更新 `docs/architecture/ARCHITECTURE.md`、`docs/governance/DECISIONS.md`、`TASK.md`、`docs/governance/PROJECT_BACKLOG.md`。
- 检查工作区后未发现额外 untracked chunk 文件，因此无需删除重复产物。
- 本次不改变 API response、不改变 scoring 行为、不引入 RAG、embedding、pgvector、frontend 或 PostgreSQL 搜索后端。

## 2026-07-04 Sprint 8.2 Document Retrieval API MVP Implementation

- 实现 `POST /api/v1/document-retrieval/search`，以 keyword-only 方式在现有 in-memory document chunks 上执行检索。
- 支持 `query`、`limit`、`include_archived`、`document_type`、`language`、`tags`，并返回 `document_id`、`chunk_id`、`chunk_index`、`content_excerpt`、`score`、`source`、`metadata`。
- 新增 `backend/app/api/document_retrieval.py`、`backend/app/services/document_retrieval_service.py`、`backend/app/schemas/document_retrieval_api.py` 与 `backend/tests/test_document_retrieval_api.py`。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/architecture/ARCHITECTURE.md`、`docs/governance/DECISIONS.md` 以及 handbook mirror。
- 本次仍不实现 LLM、RAG、embedding、pgvector、hybrid search、frontend 或 PostgreSQL document repository。

## 2026-07-04 Sprint 8.1 Document Retrieval Contract Freeze

- 冻结 `POST /api/v1/document-retrieval/search` 的请求、响应、状态码、错误码、检索事件与错误目录。
- 在 `docs/architecture/ARCHITECTURE.md` 增加 Document Retrieval Flow、Source Trace Flow 与 Future RAG Integration Flow。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/governance/DECISIONS.md` 以及 handbook mirror。
- 本次仍不实现 Retrieval API、RAG、embedding、pgvector、hybrid search 或 future approval flow。

## 2026-07-04 Sprint 7 Document Chunk Pipeline MVP

- 实现 `POST /api/v1/documents/{document_id}/chunks` 与 `GET /api/v1/documents/{document_id}/chunks`。
- Chunk pipeline 只接受 validated 文档，只支持 Markdown / Text，并采用 deterministic replace 规则。
- 新增 `backend/app/repositories/interfaces/document_chunk_repository.py`、`backend/app/repositories/implementations/in_memory/document_chunk_repository.py`、`backend/app/services/document_chunk_service.py`、`backend/app/api/document_chunks.py`、`backend/app/schemas/document_chunk_api.py` 与 `backend/tests/test_document_chunk_api.py`。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/contracts/API_CONTRACT.md`、`docs/contracts/EVENT_CONTRACT.md`、`docs/contracts/ERROR_CATALOG.md`、`docs/architecture/ARCHITECTURE.md`、`docs/governance/DECISIONS.md` 以及 handbook mirror。
- 本次仍不实现 frontend、RAG、embedding、pgvector、Approval API、PostgreSQL Document Repository、versions、search。

## 2026-07-04 Sprint 6 Document Import Pipeline MVP

- 实现 `POST /api/v1/documents/{document_id}/import` 与 `GET /api/v1/document-imports/{import_id}`。
- 导入流水线支持 pending / running / completed / failed 状态，成功导入会把文档状态推进到 `validated`。
- 对 Markdown / Text / CSV / JSON 允许导入，对 PDF / Word / Excel / Image 作为计划能力返回 `unsupported_document_type`。
- 新增 `backend/app/models/document_import.py`、`backend/app/services/document_import_service.py`、`backend/app/api/document_imports.py`、`backend/app/schemas/document_import_api.py` 与 `backend/tests/test_document_import_api.py`。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/contracts/API_CONTRACT.md`、`docs/contracts/EVENT_CONTRACT.md`、`docs/contracts/ERROR_CATALOG.md`、`docs/database/DATABASE.md`、`docs/architecture/ARCHITECTURE.md`、`docs/governance/DECISIONS.md` 以及 handbook mirror。
- 本次仍不实现 frontend、RAG、embedding、pgvector、Internet Search、Approval API、versions、chunks、PostgreSQL Document Repository。

## 2026-07-04 Sprint 5 Document Archive API MVP

- 实现 `DELETE /api/v1/documents/{document_id}` 的软删除归档语义，不做物理删除。
- archived 文档继续可由 `GET /api/v1/documents/{document_id}` 读取；列表默认排除 archived，并支持 `include_archived=true` 或 `status=archived`。
- 新增 `backend/app/services/document_archive_service.py` 与 `backend/tests/test_document_archive_api.py`，并调整文档领域删除行为为 archive / soft delete。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/contracts/API_CONTRACT.md`、`docs/contracts/EVENT_CONTRACT.md`、`docs/architecture/ARCHITECTURE.md`、`docs/governance/DECISIONS.md` 以及 handbook mirror。
- 本次仍不实现 frontend、RAG、chunking、pgvector、Approval API、versions、chunks、PostgreSQL Document Repository。

## 2026-07-04 Sprint 4 Document Read API MVP

- 实现 `GET /api/v1/documents` 与 `GET /api/v1/documents/{document_id}`。
- 支持 status / document_type / language / tag / owner 基础过滤，并在缺失文档时返回 `document_not_found`。
- 新增 `backend/app/services/document_read_service.py`、`backend/tests/test_document_read_api.py`，并复用现有 `InMemoryDocumentRepository`。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/architecture/ARCHITECTURE.md`、`docs/governance/CHANGELOG.md`、`docs/governance/DECISIONS.md` 以及 handbook mirror。
- 本次仍不实现 frontend、RAG、chunking、pgvector、Approval API、DELETE、versions、chunks、PostgreSQL Document Repository。

## 2026-07-04 Sprint 3 Document Upload API MVP Implementation

- 实现 `POST /api/v1/documents` 的同步 MVP。
- 支持 multipart/form-data、metadata JSON、title / description / owner / tags / language 校验、SHA-256 checksum、duplicate checksum detection 和 `Idempotency-Key`。
- 新增 `backend/app/api/documents.py`、`backend/app/services/document_upload_service.py`、`backend/app/schemas/document_api.py` 与 `backend/tests/test_document_upload_api.py`。
- 更新 `TASK.md`、`ROADMAP.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/contracts/API_CONTRACT.md`、`docs/contracts/EVENT_CONTRACT.md`、`docs/governance/CHANGELOG.md`、`docs/governance/DECISIONS.md` 以及 handbook mirror。
- 本次仍不实现 frontend、不实现 RAG、不实现 chunking、不实现 pgvector、不实现 Approval API。

## 2026-07-04 Sprint 2.5 Document Upload Workflow + Error Catalog + Upload Policy Freeze

- 冻结 Document Upload Workflow、Upload Session contract、Idempotency contract、Error Catalog 和 Upload Policy。
- 新增 `docs/contracts/ERROR_CATALOG.md` 与 `docs/contracts/UPLOAD_POLICY.md`。
- 更新 `docs/contracts/API_CONTRACT.md`、`docs/contracts/EVENT_CONTRACT.md`、`docs/architecture/ARCHITECTURE.md`、`docs/database/DATABASE.md`、`docs/governance/PROJECT_BACKLOG.md`、`TASK.md`、`ROADMAP.md`、`docs/governance/DECISIONS.md` 以及 handbook mirror。
- 本次仍不实现 Upload API，不修改 backend 业务代码，不修改 frontend。

## 2026-07-04 Sprint 2 Document Upload API Contract Freeze

- 冻结 Document Upload API contract，覆盖 `POST /api/v1/documents`、`GET /api/v1/documents`、`GET /api/v1/documents/{document_id}`、`GET /api/v1/documents/{document_id}/versions`、`GET /api/v1/documents/{document_id}/chunks`、`DELETE /api/v1/documents/{document_id}`。
- 冻结 Document Upload event contract，覆盖 `document.upload.started`、`document.upload.validated`、`document.upload.completed`、`document.upload.failed`、`document.version.created`、`document.validation.failed`。
- 更新 `docs/contracts/API_CONTRACT.md`、`docs/contracts/EVENT_CONTRACT.md`、`docs/architecture/ARCHITECTURE.md`、`docs/database/DATABASE.md`、`docs/governance/PROJECT_BACKLOG.md`、`TASK.md`、`ROADMAP.md`、`docs/governance/DECISIONS.md` 以及 handbook mirror。
- 本次仍只停留在 Document Domain Model，未实现 Upload API、未修改 backend 业务代码、未修改 frontend。

## 2026-07-04

- 完成 `Sprint 1: Phase 3.1 Document Domain Model`。
- 新增 `backend/app/models/document.py`，定义 Document、DocumentVersion、DocumentChunk placeholder、DocumentMetadata、DocumentSource、DocumentStatus、DocumentType、Language，并复用现有 ApprovalStatus 与 ImportBatch。
- 新增 `backend/app/repositories/interfaces/document_repository.py` 与 `backend/app/repositories/implementations/in_memory/document_repository.py`。
- 新增文档域单元测试，覆盖 Document creation、metadata validation、status transition、Repository CRUD、checksum duplicate detection。
- 更新 `docs/architecture/ARCHITECTURE.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/ROADMAP.md`、`docs/TASK.md`、`docs/governance/DECISIONS.md` 以及 handbook mirror。
- 本次未实现 Upload API、RAG、Chunk、pgvector、Internet Search 或 PostgreSQL Document Repository。

- 完成 `Epic 14: Engineering Standards (Final Freeze)` 文档冻结。
- Master Prompt Summary was added after Epic 14 final freeze.
- 新增 `docs/development/MASTER_PROMPT.md`，作为唯一 Master Prompt。
- 新增 `docs/development/CODING_STANDARD.md`、`docs/development/DEVELOPMENT_GUIDE.md`、`docs/architecture/AI_AGENT_DESIGN_GUIDE.md`。
- 新增 `docs/contracts/API_CONTRACT.md`、`docs/contracts/EVENT_CONTRACT.md`、`docs/development/PROMPT_STANDARD.md`。
- 在 `docs/ai-agent-retail-handbook-v3/docs/` 新增上述 7 份镜像文档。
- 更新 `ROADMAP.md`、`TASK.md`、`docs/governance/PROJECT_BACKLOG.md`、`docs/architecture/ARCHITECTURE.md`、`docs/governance/DECISIONS.md` 记录本次冻结。
- 扩展 `../doc-sync.manifest.json`，新增 `engineering-standards` 同步组。
- 本次未修改 `backend/`、`frontend/`、`scripts/`，未新增业务代码，未修改数据库 schema。

- 新增 `scripts/verify_postgres_phase2.sh`，统一 Phase 2 PostgreSQL 验证入口。
- 该脚本会先检查 `psycopg` 与 Docker，再决定自动启动 `postgres` 容器并执行 `tests.test_postgres_repositories`，或明确输出跳过原因与手动命令。
- 修正 `RUNBOOK_LOCAL.md` 中 PostgreSQL 示例账号口径，统一为 `retail_user / retail_password`。
- README、RUNBOOK、VERIFY_CHECKLIST、CODE_STUDY_GUIDE 补充 PostgreSQL 验证脚本说明。
- 尝试执行 `python3 ../scripts/sync_retail_handbook_docs.py` 刷新外部 handbook，同步因缺少同级 `ai-agent-retail-handbook-v3/README.md` 工作区文件而阻塞。
- 实现 Phase 2：PostgreSQL Persistence MVP 的代码基础。
- 新增 `backend/app/db/connection.py` 与 `backend/app/repositories/postgres/`。
- 新增 `backend/db/schema.sql`、`backend/db/init.sql`。
- 新增 `REPOSITORY_BACKEND=inmemory|postgres`，默认保持 `inmemory`。
- 新增 PostgreSQL 连接配置：
  `POSTGRES_HOST`、`POSTGRES_PORT`、`POSTGRES_DB`、`POSTGRES_USER`、`POSTGRES_PASSWORD`。
- 为 `tasks`、`task_events`、`reports`、`report_versions` 实现 PostgreSQL Repository。
- 为 `data_imports`、`import_errors`、`approval_requests`、`approval_events` 新增 schema 与基础模型预留。
- `reports` 表新增 `approval_status` 字段，当前值仍为 `generated`。
- `docker-compose.yml` 新增 PostgreSQL service。
- 新增 backend switch 测试与 PostgreSQL Repository 集成测试骨架。
- 同步更新 `docs/database/DATABASE.md`、`docs/architecture/ARCHITECTURE.md`、`docs/governance/DECISIONS.md` 以及 handbook 对应文档。
- 修正 Phase 2 状态口径为：
  `Code implemented`
  `InMemory path verified`
  `PostgreSQL schema implemented`
  `PostgreSQL repository tests prepared`
  `PostgreSQL real integration test pending`
  `Status: In Progress / Partially Verified`
- 明确当前环境缺少 Docker CLI、未安装 `psycopg` 到实际运行 venv，因此 PostgreSQL 集成测试被 skip。

- 新增 Phase 1.5：Data Contract Freeze + Approval State Machine Design。
- 新增 `docs/architecture/DATA_CONTRACTS.md`，冻结业务 CSV、Research JSON、Documents Markdown 契约。
- 新增 `docs/architecture/APPROVAL_WORKFLOW.md`，冻结 `generated / draft / pending_approval / approved / rejected / revised / published / archived` 状态机。
- 新增 `docs/database/DATABASE.md`，冻结 Phase 2 PostgreSQL 准备项：
  `data_imports`、`import_errors`、`reports`、`report_versions`、`approval_requests`、`approval_events`。
- 新增导入错误模型：
  `missing_file`、`invalid_header`、`invalid_type`、`empty_dataset`、`invalid_json`、`invalid_source`、`unsupported_encoding`。
- 完成 Phase 1 文件化输入实现。
- 新增 `backend/app/data_loaders/` 本地文件加载层。
- KPI 从 `backend/data/business/sales.csv`、`inventory.csv`、`members.csv`、`promotions.csv` 读取并计算。
- Research 从 `backend/data/research/market_trend_2026_06.json` 与 `competitor_summary_2026_06.json` 读取 summary / sources。
- 新增 `backend/data/documents/company_policy_sample.md`，作为后续文档上传与检索输入边界样例。
- Report API 新增 `status` 字段，当前值为 `generated`，并为后续 Approval Workflow 预留 `draft / pending_approval / approved / rejected / revised`。
- 新增文件输入测试、Research JSON 测试、hybrid 报告测试。
- 新增企业架构定位（Architecture Positioning）。
- 明确 `Retail Insight AI` 仍为当前项目名称和仓库名称。
- 明确 `Enterprise Retail Intelligence Platform (ERIP)` 为未来平台化目标，而非当前已实现平台。
- 新增 `Epic 0: Enterprise Platform Architecture Evolution`。
- 新增平台化架构原则：
  Platform First、Domain Driven、Provider Pattern、Repository Pattern、Workflow Driven、Configuration First、Test First、Documentation First、Backward Compatibility。
- 新增目标架构逻辑分层：
  Platform、Domain、Provider、Workflow、Repository、Approval、Documents、Search、Import、Audit、Database、Frontend。
- 新增 Phase 完成的 Definition of Done。
- 新增 `Epic 0` 的 Enterprise Architecture Freeze 设计内容：
  Architecture Freeze、Directory Refactor Design、Repository Abstraction Design、Provider Abstraction Design、Workflow Architecture、Document Pipeline、Business Data Pipeline、Approval Workflow、Database Target Design、Testing Matrix、Documentation Matrix、Epic 0 Deliverables。
- 新增 `Epic 12: Retrieval and RAG Platform`。
- 明确 RAG 包含结构化业务数据检索、社内文档检索、互联网检索，而不只限于社内文档。
- 新增检索层相关架构章节：
  Retrieval Layer Architecture、Business Retrieval Flow、Internal RAG Flow、Internet Search Flow、Context Merge Flow、Citation and Source Trace Flow、Future Hybrid Search Architecture。

## 2026-07-02

- 建立 retail-insight-ai 与 ai-agent-retail-handbook-v3 的跨项目文档同步机制。
- 新增 `../scripts/sync_retail_handbook_docs.py` 与 `../doc-sync.manifest.json`。
- 为 README、TASK、PROJECT_BACKLOG、CHANGELOG、RUNBOOK、CODE_STUDY_GUIDE、VERIFY_CHECKLIST、STUDY_PLAN、ARCHITECTURE 和 DECISIONS 建立同步块维护入口。

## 2026-06-29

- 创建项目永久任务清单机制。
- 更新项目 AGENTS.md。
- 建立开发前检查、开发后更新规则。
- 执行项目状态检查。
- 检查结果概要：五份治理文档完整，项目处于 Phase 2 开发准备阶段；当前仍是 Level 1 本地可运行实现，Document Upload、Chunk Pipeline、Embedding、Vector Search 与 Approval Agent 尚未实现。
- 风险概要：README 与 Backlog 的阶段描述尚未统一，CHANGELOG 尚未完整回溯既有功能，当前 WSL 环境无法使用 Docker CLI；`.env`、虚拟环境、依赖目录和构建产物已被 `.gitignore` 保护且未被 Git 跟踪。
- 升级到 AI-LAB Project Governance V2。
- 新增 `ROADMAP.md`、`docs/architecture/ARCHITECTURE.md` 和 `docs/governance/DECISIONS.md`。
- 更新 `AGENTS.md`，开发前增加 Roadmap、Backlog 和 TASK 强制读取顺序。
- 影响文件：AGENTS.md、TASK.md、ROADMAP.md、docs/governance/PROJECT_BACKLOG.md、docs/governance/CHANGELOG.md、docs/architecture/ARCHITECTURE.md、docs/governance/DECISIONS.md。

<!-- DOC-SYNC:START group=governance -->
## 文档同步块

- group: `governance`
- file: `retail-insight-ai/docs/governance/CHANGELOG.md`
- self_sha256: `cf9c2939e3369aa13c65a636fb64c44d56b672866b23771cf1dda5f1dbe755b3`
- peers:
- `retail-insight-ai/ROADMAP.md` | sha256=5bf39c8dbde1e5279088478951af2f3c02a4506bcbf3682403b3e45a02846cae | # retail-insight-ai Roadmap / 最后更新：2026-06-29 / ## 当前阶段 / 待根据项目现状确认。
- `retail-insight-ai/TASK.md` | sha256=83a6ef1d9395a1c0026514c5d8fab074fb8428781ab712ad25764c1c82decc05 | # retail-insight-ai 当前任务 / 最后更新：2026-07-02 / ## 当前阶段 / Phase 2: Internal Knowledge Approval Agent
- `retail-insight-ai/docs/governance/PROJECT_BACKLOG.md` | sha256=b1dd8a6cee6a7fc07965026b8aefe8c9c8f08669871abd5ce2b8eb3dc1d5d477 | # retail-insight-ai Project Backlog / 最后更新：2026-07-08 / ## 项目目标 / 构建 `Enterprise Retail Intelligence Platform (ERIP)` 的目标平台蓝图；当前仓库中的 `Retail Insight AI` 仅表示该目标平台的 Current MVP，包含：
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
