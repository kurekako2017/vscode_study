# Retail Insight AI 当前实现审计

审计日期：2026-07-12

## 1. 审计范围与方法

本次只做源码、配置、测试、前端、数据库、Workflow 和文档的一致性盘点，不开发新功能、不接入真实 LLM、不修改业务逻辑。

检查范围：

- `backend/app/api/`、`services/`、`workflow/`、`agents/`、`kpi/`、`repositories/`、`schemas/`
- `frontend/src/`
- `backend/db/`、`docker-compose.yml`、两个 Dockerfile
- `backend/tests/`、`frontend/src/*.test.tsx`、`frontend/src/*.test.ts`
- `docs/learning/01_Foundation/LEARNING_API_WALKTHROUGH.md`、架构/数据库/治理文档

分类含义：

| 分类 | 含义 |
|---|---|
| `COMPLETED` | 当前代码可运行，存在直接测试或可验证实现 |
| `PARTIAL` | 主链路可运行，但仍有明确范围、实现或生产能力缺口 |
| `SKELETON` | 有接口、模型或接缝，但核心能力仍是占位/最小实现 |
| `DOC_ONLY` | 文档描述存在，源码没有对应可运行实现 |
| `MISSING` | 当前源码没有该能力 |
| `BLOCKED` | 受外部环境、依赖或未完成基础设施阻塞 |

## 2. 验证结果摘要

| 检查项 | 结果 | 证据 |
|---|---|---|
| Backend tests | `COMPLETED` | `./scripts/run_tests.sh`：115 tests passed，1 skipped |
| Frontend tests | `COMPLETED` | Vitest：2 files，5 tests passed |
| Frontend build | `COMPLETED` | TypeScript checks 与 Vite production build 通过 |
| Python compileall | `COMPLETED` | `backend/app` 与 `backend/tests` compileall 通过 |
| PostgreSQL integration | `BLOCKED` | PostgreSQL 不可达，`test_postgres_repositories` skipped |
| Docker build/runtime | `PARTIAL` | Compose 与 Dockerfiles 存在；本轮未执行 Docker Build，不能宣称运行验证完成 |
| 业务源码变更 | `COMPLETED` | 本轮未修改业务代码、测试或前端 |

## 3. 总体完成度

按“当前可运行本地 MVP”口径，项目主链路完成度约为 **65%**；按目标 ERIP 企业平台口径，完成度约为 **35%**。

这个数字不是代码行数比例，而是对 API 可运行性、测试保护、数据持久化、AI/RAG、审批、前端和部署边界的综合估计。当前最准确的描述是：

> Retail Insight AI 已完成 Local Static Provider + InMemory Repository + FastAPI + React + SSE 的学习型 MVP；尚未完成企业级 PostgreSQL/pgvector、真实 LLM、生产安全、可观测性和容器运行闭环。

## 4. 能力实现矩阵

### 4.1 Backend/API

| 能力 | 状态 | 事实与证据 |
|---|---|---|
| FastAPI 应用启动与路由注册 | `COMPLETED` | `backend/app/main.py` 使用 `create_app()` 注册 Health、Tasks、Documents、RAG、Approval、Security、Audit 等 Router |
| Health API | `COMPLETED` | `/health` 有响应模型、request_id、static provider 信息和测试 |
| Task API | `COMPLETED` | 创建、状态、报告、SSE 事件均有实现和测试；创建返回 HTTP 202 |
| 统一错误 Envelope | `COMPLETED` | `errors/handlers.py`、错误码和 API 测试覆盖 404/409/422/403 等主要路径 |
| Structured Logging | `PARTIAL` | `log_event()` 已覆盖多条业务路径；并非所有 API 都有独立事件，部分接口只有 Response/Trace |
| Learning Trace | `PARTIAL` | Health、Tasks 和近期 Document 接口已有详细 Trace；其他 Retrieval、RAG、Approval、Security、Audit API 仍未全量展开 |
| Document Upload/Read/Archive/Import/Chunk | `COMPLETED` | Router、Service、InMemory Repository、状态/异常分支和测试均存在；能力是本地同步 MVP |
| API Contract 与 OpenAPI | `PARTIAL` | FastAPI schema 可生成 OpenAPI；学习文档部分 Execution Flow 与最新源码仍需持续同步 |

### 4.2 Frontend

| 能力 | 状态 | 事实与证据 |
|---|---|---|
| React/Vite 页面 | `COMPLETED` | `frontend/src/App.tsx` 提供任务输入、模式选择、状态时间线、错误区域和报告区域 |
| 创建 Task | `COMPLETED` | `frontend/src/api.ts:createTask()` 调用 `/api/tasks` |
| SSE 订阅 | `COMPLETED` | `subscribeToTask()` 使用 `EventSource`，处理 status/done/error 与连接关闭 |
| 报告读取 | `COMPLETED` | done 后调用 `getReport()`，页面展示 Markdown 原文 |
| Document/RAG/Approval 管理页面 | `MISSING` | 当前 React 页面只覆盖 Task → SSE → Report 主链路 |
| 前端认证/RBAC | `MISSING` | 没有真实登录、Token、用户切换或权限管理 UI |
| 前端生产部署 | `PARTIAL` | 有 Nginx production image 和 build；本轮未完成容器运行验证 |

### 4.3 Workflow / Agent / KPI

| 能力 | 状态 | 事实与证据 |
|---|---|---|
| LangGraph Workflow | `COMPLETED` | `backend/app/workflow/graph.py` 使用 StateGraph/astream，存在 route、kpi、research、report 节点 |
| Task Background 执行 | `COMPLETED` | `BackgroundTasks.add_task(service.run_task, task_id)`；TaskService 负责状态和事件推进 |
| mode 分支 | `COMPLETED` | `hybrid`、`kpi`、`research` 在 Workflow route 中选择对应节点 |
| Fixed KPI Workflow | `COMPLETED` | `backend/app/kpi/workflow.py` 有确定性 KPI 计算与测试保护 |
| Static Research Provider | `COMPLETED` | `backend/app/agents/providers/static_research.py` 读取本地静态研究数据 |
| Multi-Agent 协作 | `SKELETON` | 存在 ResearchAgent/Provider 等边界，但不是生产级多 Agent 协作、规划或工具编排系统 |
| Real-time workflow observability | `PARTIAL` | SSE 和事件已实现；Tracing/metrics/OpenTelemetry 未接入 |

### 4.4 RAG / AI

| 能力 | 状态 | 事实与证据 |
|---|---|---|
| Document Retrieval API | `COMPLETED` | Keyword-only 检索、过滤、排序、chunk 来源响应和测试存在 |
| Internal RAG Answer API | `COMPLETED` | 检索 → citation → deterministic answer → evaluation/warnings 有实现和测试 |
| Citation/Confidence/Evaluation | `COMPLETED` | `RAGAnswerGenerator` 与 `InternalRagEvaluationService` 提供当前无 LLM 的可解释结果 |
| Real LLM | `MISSING` | Settings 仅允许 `llm_provider="stub"`；未接 OpenAI 或其他真实模型 |
| Embedding | `MISSING` | 未发现 embedding provider/pipeline |
| Vector Search | `MISSING` | 未发现 pgvector、向量索引或相似度查询实现 |
| Hybrid Retrieval | `DOC_ONLY` | 文档/路线图描述 Target 能力；当前源码实际是 keyword retrieval |
| Reranking/Context Compression | `MISSING` | 当前没有 reranker 或 contextual compression pipeline |

### 4.5 Approval Workflow / Security

| 能力 | 状态 | 事实与证据 |
|---|---|---|
| Submit/List/Get Approval | `COMPLETED` | Approval API、Service、InMemory approval repository 和测试存在 |
| Approve/Reject/Revise 状态机 | `COMPLETED` | ApprovalService 有状态校验、版本快照、决策和失败事件；测试覆盖主要路径 |
| Audit Middleware | `COMPLETED` | 审批操作经过审计执行边界，拒绝和失败事实可写入 InMemory audit repository |
| RBAC seam | `PARTIAL` | permission/role 检查和 system placeholder user 可运行；没有真实认证身份来源 |
| Real authentication | `MISSING` | 当前没有 JWT/OAuth/session/外部 IdP |
| Durable audit storage | `SKELETON` | 当前是 InMemory append-only audit log，不是生产持久化审计库 |
| Approval UI | `MISSING` | 前端没有审批列表、审批详情、批准/拒绝/修订页面 |

### 4.6 PostgreSQL / Persistence

| 能力 | 状态 | 事实与证据 |
|---|---|---|
| InMemory Repository backend | `COMPLETED` | 当前默认配置 `repository_backend=inmemory`，Task/Report/Event/Document/Chunk/Approval 等本地实现可运行 |
| Repository interface boundary | `COMPLETED` | `repositories/interfaces/` 定义协议，测试保护 Service 不直接依赖部分实现 |
| PostgreSQL connection/config | `PARTIAL` | `db/connection.py` 与 settings/container 支持 PostgreSQL 配置 |
| PostgreSQL Task Repository | `PARTIAL` | `repositories/postgres/task_repository.py` 存在并有边界测试 |
| PostgreSQL Report Repository | `PARTIAL` | `repositories/postgres/report_repository.py` 存在 |
| PostgreSQL Event Repository | `PARTIAL` | `repositories/postgres/event_repository.py` 存在 |
| PostgreSQL Document/Chunk/Approval/Audit | `MISSING` | Container 仍使用 InMemory 实现，未形成完整 PostgreSQL 替换闭环 |
| PostgreSQL integration runtime | `BLOCKED` | 本轮环境 PostgreSQL 不可达，集成测试跳过 |
| Migration lifecycle | `SKELETON` | 有 `backend/db/schema.sql` / `init.sql`，但未发现完整版本化 migration workflow |

### 4.7 pgvector / Docker / Production

| 能力 | 状态 | 事实与证据 |
|---|---|---|
| pgvector | `MISSING` | requirements、schema、repository 和 container 中均未发现 pgvector 实现 |
| Docker Compose topology | `PARTIAL` | `docker-compose.yml` 定义 backend、frontend、postgres 和 volume |
| Backend Docker image | `COMPLETED` | `backend/Dockerfile` 可构建 uvicorn image，未在本轮实际 build |
| Frontend Docker image | `COMPLETED` | `frontend/Dockerfile` 使用 Node build + Nginx runtime，未在本轮实际 build |
| Docker end-to-end runtime | `BLOCKED` | 本轮未执行 Docker Build/Compose；不能证明三服务实际连通 |
| Redis/RabbitMQ | `MISSING` | 未接入 |
| Kubernetes | `DOC_ONLY` | 仅在 Target/路线图文档中出现 |
| OpenTelemetry/metrics | `MISSING` | 当前只有结构化日志和本地 Learning Trace |

## 5. 测试覆盖盘点

### 已覆盖

- Task API、Background Workflow、SSE、报告读取
- Document Upload、Read、Archive、Import、Chunk、Retrieval
- Internal RAG、Answer Generator、Evaluation
- Approval API、RBAC Guard、Audit Middleware、安全目录
- Repository boundary、backend switch、settings、structured logging
- Frontend API client 和主页面渲染/交互

### 覆盖边界

- PostgreSQL integration test 在本轮因数据库不可达而跳过，不等同于 PostgreSQL 通过。
- Docker build、Compose 启动、frontend/backend/proxy 联调未在本轮执行。
- 前端只验证 Task/SSE/Report；Document、RAG、Approval 没有页面级测试，因为没有对应 UI。
- 真实 LLM、embedding、vector search、external auth 没有测试，因为源码没有这些实现。
- Learning Trace 全量一致性尚未形成自动化契约测试；目前主要依赖接口测试输出和文档人工比对。

## 6. 文档与源码一致性

| 主题 | 状态 | 审计结论 |
|---|---|---|
| Current MVP / Target ERIP 边界 | `PARTIAL` | 主文档已多次声明 Current/Target；仍需持续防止 Target 能力被描述为已完成 |
| API 输入参数 | `PARTIAL` | 近期已修正主要 Document Case；全量文档仍有旧的简化 Execution Flow |
| Learning Trace | `PARTIAL` | 代码已逐步补齐 Document/Import/Chunk；文档和其他 API 尚未完全同步 |
| 05 /report 标准模板 | `COMPLETED` | 当前保留为详细树形模板，后续同步不得破坏 |
| PostgreSQL/pgvector/RAG 目标能力 | `PARTIAL` | 文档通常标注 Target/Planned，但应继续核对所有旧章节和 handbook 镜像 |

## 7. P0 阻塞项

1. **PostgreSQL 可运行验证缺失**：当前集成测试因 PostgreSQL 不可达而跳过；在此之前不能宣称 PostgreSQL backend 完成。
2. **Document/Chunk/Approval/Audit 尚未具备 PostgreSQL 实现**：切换 `repository_backend=postgres` 不能覆盖完整业务域。
3. **真实身份认证缺失**：Approval/RBAC 当前基于 system placeholder user，无法作为生产权限边界。
4. **生产 RAG 能力缺失**：没有 embedding、pgvector、hybrid retrieval、reranker 和真实 LLM。
5. **Docker 端到端未验证**：Compose 拓扑存在，但 backend、frontend、PostgreSQL 的实际容器连通性尚未证明。
6. **Learning Trace/文档全量同步未完成**：当前只完成部分接口，不能将所有 API 的学习链路视为一致。

## 8. 推荐下一阶段开发顺序

1. 修复本地 PostgreSQL 可运行环境，并完成 Task/Report/Event 的真实 integration test。
2. 设计并实现 Document/Chunk/Approval/Audit 的 PostgreSQL Repository 与 migration 版本管理。
3. 将认证身份接入 Security/RBAC，补齐真实用户、权限和审计关联。
4. 在不改变当前 Retrieval Contract 的前提下增加 embedding pipeline 与 pgvector index。
5. 增加 hybrid retrieval、reranking 和离线评测集；保留 deterministic fallback。
6. 在明确 provider seam 和安全策略后接入真实 LLM，不提前绕过当前 static/stub 边界。
7. 补齐 Document/RAG/Approval 前端页面和对应测试。
8. 执行 Docker Compose 端到端验证，再考虑 Redis/RabbitMQ/OpenTelemetry/Kubernetes。
9. 最后统一全量 API Learning Trace、Execution Flow、Log Check 和自动化文档一致性测试。

## 9. 审计结论

当前项目适合作为可运行、可学习、可面试讲解的日本现场 AI Agent MVP；不应被描述为已经完成的企业级 ERIP 平台。最可靠的当前能力是：本地静态数据、确定性 KPI、静态 Research、无真实 LLM 的 Internal RAG、InMemory 持久化、Task Workflow、SSE、基础 Approval/RBAC/Audit 边界和 React Task 页面。

本轮未修改业务代码、测试、前端、数据库脚本或既有文档；仅新增本审计文档。
