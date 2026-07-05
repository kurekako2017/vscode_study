# 测试用例说明

这份文档不是测试结果汇总，而是“每个测试文件该怎么学”的说明。目标是让你知道每个测试保护哪条链路、输入怎么构造、预期怎么判断。

## 统一命令

```bash
cd backend
python3 -m unittest discover -s tests -v
python3 -m compileall app tests
```

如果只跑单个文件：

```bash
cd backend
python3 -m unittest tests.test_api -v
```

## 测试用例学习说明

| 测试文件 | 测试目的 | 对应 API | 对应源码位置 | 测试命令 | 输入（入力） | 预期输出（预想结果） | 后端流程说明 | 前端/Swagger 操作流程说明 | 为什么这样设计 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `backend/tests/test_api.py` | 验证任务主链路、SSE、报告和错误封装 | `POST /api/tasks`、`GET /api/tasks/{task_id}`、`GET /api/tasks/{task_id}/events`、`GET /api/tasks/{task_id}/report` | `backend/app/api/tasks.py`、`backend/app/services/task_service.py`、`backend/app/events/sse.py` | `python3 -m unittest tests.test_api -v` | 创建任务请求、状态查询、SSE 订阅、报告查询 | HTTP 202、状态流、SSE 事件、Markdown 报告 | `Test Client / Swagger` → `api/tasks.py` → `task_service.py` → `events/sse.py` → `report repository` | 打开 Swagger → 执行创建任务 → 复制 `task_id` → 订阅 events → 读取 report | 它是主链路，先稳住最能代表项目运行的路径 |
| `backend/tests/test_document_upload_api.py` | 验证上传、metadata、checksum、幂等 | `POST /api/v1/documents` | `backend/app/api/documents.py`、`backend/app/services/document_upload_service.py` | `python3 -m unittest tests.test_document_upload_api -v` | `file` + `metadata` | HTTP 201，返回 `document_id` | `Swagger / Test Client` → `api/documents.py` → `document_upload_service.py` → `InMemoryDocumentRepository` → 返回 `document_id` | 打开 Swagger → 展开 `POST /api/v1/documents` → `Try it out` → 选文件 → 填 metadata → `Execute` | 上传是文档链路入口，后面的 import / chunk / retrieval 都依赖它 |
| `backend/tests/test_document_read_api.py` | 验证列表、详情、过滤 | `GET /api/v1/documents`、`GET /api/v1/documents/{document_id}` | `backend/app/api/documents.py`、`backend/app/services/document_read_service.py` | `python3 -m unittest tests.test_document_read_api -v` | 文档 ID、过滤参数 | 返回列表或详情，缺失时 `document_not_found` | `Swagger / Test Client` → `api/documents.py` → `document_read_service.py` → `InMemoryDocumentRepository` | Swagger 中先读列表，再填 `document_id` 看详情 | 先验证读接口，最容易确认仓库状态和过滤逻辑 |
| `backend/tests/test_document_archive_api.py` | 验证软删除/归档语义 | `DELETE /api/v1/documents/{document_id}` | `backend/app/api/document_archive.py`、`backend/app/services/document_archive_service.py` | `python3 -m unittest tests.test_document_archive_api -v` | 文档 ID | 文档进入 archived，列表默认不显示 | `Test Client` → `api/document_archive.py` → `document_archive_service.py` → `InMemoryDocumentRepository` | Swagger 中执行 DELETE，再回列表确认不再展示 | 要区分“归档”和“物理删除”，保留可追溯性 |
| `backend/tests/test_document_import_api.py` | 验证导入流程和状态推进 | `POST /api/v1/documents/{document_id}/import` | `backend/app/api/document_imports.py`、`backend/app/services/document_import_service.py` | `python3 -m unittest tests.test_document_import_api -v` | 文档 ID、导入请求 | 返回导入结果，状态推进 | `Swagger / Test Client` → `api/document_imports.py` → `document_import_service.py` → `DocumentRepository` / `ImportRepository` | Swagger 中先确认文档存在，再执行 import | 导入是结构化处理起点，决定后续 chunk 能不能跑 |
| `backend/tests/test_document_chunk_api.py` | 验证切分和 chunk 读取 | `POST /api/v1/documents/{document_id}/chunks`、`GET /api/v1/documents/{document_id}/chunks` | `backend/app/api/document_chunks.py`、`backend/app/services/document_chunk_service.py` | `python3 -m unittest tests.test_document_chunk_api -v` | 文档 ID、切分参数 | 返回 chunk 列表和稳定元数据 | `Swagger / Test Client` → `api/document_chunks.py` → `document_chunk_service.py` → `DocumentChunkRepository` | Swagger 中先切分，再读 chunks 校验 | Chunk 是 retrieval / RAG 的前置数据层 |
| `backend/tests/test_document_retrieval_api.py` | 验证关键字检索、过滤、archived 排除 | `POST /api/v1/document-retrieval/search` | `backend/app/api/document_retrieval.py`、`backend/app/services/document_retrieval_service.py` | `python3 -m unittest tests.test_document_retrieval_api -v` | `query` 和过滤条件 | 返回检索结果、分数、来源 | `Swagger / Test Client` → `api/document_retrieval.py` → `document_retrieval_service.py` → `DocumentRetrievalProvider` | Swagger 中先写 query，再看返回的 chunks 和 score | 先保证检索稳定，RAG 才有可信前提 |
| `backend/tests/test_internal_rag_api.py` | 验证 deterministic RAG 组装 | `POST /api/v1/internal-rag/answer` | `backend/app/api/internal_rag.py`、`backend/app/services/internal_rag_service.py` | `python3 -m unittest tests.test_internal_rag_api -v` | 问题文本、检索参数 | 返回 `answer`、`citations`、`confidence`、`warnings` | `Swagger / Test Client` → `api/internal_rag.py` → `internal_rag_service.py` → `retrieval` → `answer assembly` | Swagger 中先检索再生成回答，观察 citations | 证明项目能在不接真实 LLM 时完成可解释回答 |
| `backend/tests/test_internal_rag_evaluation.py` | 验证 citation quality 和 warning 评分 | `POST /api/v1/internal-rag/answer` | `backend/app/services/internal_rag_service.py` 及评估相关代码 | `python3 -m unittest tests.test_internal_rag_evaluation -v` | 不同质量的上下文和问句 | 返回评分和 warning | `Test Client` → `internal_rag_service.py` → `evaluation` → `warning taxonomy` | 不需要单独前端，Swagger 直接观察评分字段 | 让 RAG 不只是“能答”，还要“能解释为什么这样答” |
| `backend/tests/test_rag_answer_generator.py` | 验证 stub LLM provider 和 fallback | `POST /api/v1/internal-rag/answer` | `backend/app/agents/`、`backend/app/reports/`、`backend/app/workflow/` | `python3 -m unittest tests.test_rag_answer_generator -v` | provider 状态、answer 请求 | provider 可用时走 provider，失败时回退 deterministic answer | `Test Client` → `RAGAnswerGenerator` → `StubLLMProvider` / fallback | Swagger 中不需要额外页面，直接观察 answer 是否回退 | 先把未来 LLM 替换点固定住，保证当前默认路径稳定 |
| `backend/tests/test_approval_api.py` | 验证审批提交、列表、详情、批准、拒绝、修订 | `POST /api/v1/reports/{task_id}/submit-approval`、`GET /api/v1/approvals`、`GET /api/v1/approvals/{approval_id}`、`POST /api/v1/approvals/{approval_id}/approve`、`POST /api/v1/approvals/{approval_id}/reject`、`POST /api/v1/reports/{task_id}/revise` | `backend/app/api/approvals.py`、`backend/app/services/approval_service.py` | `python3 -m unittest tests.test_approval_api -v` | `task_id`、`approval_id`、审批动作 | 返回正确的状态流转和错误码 | `Swagger / Test Client` → `api/approvals.py` → `approval_service.py` → `approval repository` | Swagger 中先 submit，再看 list/detail，再做 approve/reject/revise | 审批链路是 report 之后的重要边界，必须独立验证 |
| `backend/tests/test_rbac_guard.py` | 验证 approval 相关 RBAC allow / deny | 审批相关 API 权限边界 | `backend/app/services/security_service.py`、`backend/app/api/approvals.py` | `python3 -m unittest tests.test_rbac_guard -v` | 不同权限主体和审批动作 | allow 正常通过，deny 返回 `permission_denied` | `Test Client` → `security_service.py` → `approval endpoints` → `permission check` | Swagger 里用不同身份/测试桩观察返回 | 把权限规则单独测试，避免散落在接口里 |
| `backend/tests/test_audit_middleware.py` | 验证审批审计中间件的 success / deny / failure | 审批相关 API 的中间件边界 | `backend/app/events/`、`backend/app/api/`、`backend/app/services/audit_service.py` | `python3 -m unittest tests.test_audit_middleware -v` | 审批动作请求、异常路径请求 | 审计事实被记录，失败路径仍可追踪 | `Test Client` → `middleware` → `audit_service.py` → `append-only audit log` | Swagger 触发审批，再检查 audit logs 或测试断言 | 审计必须 append-only，错误路径也不能丢事实 |
| `backend/tests/test_security_audit_api.py` | 验证 current user、roles、permissions、audit logs | `GET /api/v1/users/me`、`GET /api/v1/security/roles`、`GET /api/v1/security/permissions`、`GET /api/v1/audit-logs` | `backend/app/api/security.py`、`backend/app/api/audit_logs.py`、`backend/app/services/security_service.py`、`backend/app/services/audit_service.py` | `python3 -m unittest tests.test_security_audit_api -v` | 无或少量分页参数 | 返回 placeholder principal、冻结目录、审计列表 | `Swagger / Test Client` → `security.py` / `audit_logs.py` → `security_service.py` / `audit_service.py` | Swagger 依次打开四个 GET，确认返回结构 | 先固定安全读模型，未来真实认证才有替换基线 |
| `backend/tests/test_file_inputs.py` | 验证本地文件输入读取 | 内部数据加载边界 | `backend/app/data_loaders/`、`backend/app/kpi/`、`backend/app/agents/providers/` | `python3 -m unittest tests.test_file_inputs -v` | CSV、JSON、Markdown | 读取到稳定的本地数据结构 | `Test Client / unit` → `data_loaders` → `local files` | 不需要 Swagger，直接看本地数据文件和测试断言 | 本地静态数据是当前阶段可运行的基础 |
| `backend/tests/test_document_domain.py` | 验证文档领域模型和 InMemory 仓库规则 | 领域模型边界 | `backend/app/models/document.py`、`backend/app/repositories/interfaces/document_repository.py`、`backend/app/repositories/implementations/in_memory/document_repository.py` | `python3 -m unittest tests.test_document_domain -v` | 文档对象、元数据、状态变更请求 | 创建、状态迁移、去重、CRUD 规则正确 | `unit` → `document model` → `document repository` | 不需要 Swagger，先看领域对象再看测试 | 先把领域约束固定住，接口层才稳定 |
| `backend/tests/test_repositories.py` | 验证 Repository 接口边界 | 存储抽象边界 | `backend/app/repositories/interfaces/` | `python3 -m unittest tests.test_repositories -v` | 仓库实现对象 | 满足最小协议要求 | `unit` → `Protocol` → `repository interface` | 不需要 Swagger，直接看接口定义和测试实现 | Repository 模式的核心价值是解耦存储和业务 |
| `backend/tests/test_repository_backend_switch.py` | 验证 InMemory 默认和 PostgreSQL 开关 | 组合根与配置边界 | `backend/app/config/container.py`、`backend/app/db/connection.py` | `python3 -m unittest tests.test_repository_backend_switch -v` | 环境变量、backend 配置 | 默认仍用 InMemory，满足条件才走 PostgreSQL | `unit` → `container.py` → `backend switch` → `repository backend selection` | 不需要 Swagger，查看配置和测试输出 | 仓库切换必须显式，不破坏默认学习路径 |
| `backend/tests/test_postgres_repositories.py` | 验证 PostgreSQL 持久化冒烟测试 | 可选环境验证 | `backend/app/repositories/postgres/` 相关实现 | `python3 -m unittest tests.test_postgres_repositories -v` | `psycopg` + PostgreSQL 连接配置 | 环境满足时通过，缺少依赖时跳过 | `integration-like test` → `postgres repository` → `database roundtrip` | 不需要 Swagger，先确认本机是否有 Docker / psycopg | 证明仓库抽象能切到 PostgreSQL，但不影响默认本地运行 |
| `backend/tests/test_settings.py` | 验证环境变量和配置解析 | 启动配置边界 | `backend/app/config/`、`backend/app/main.py` | `python3 -m unittest tests.test_settings -v` | 环境变量和默认值 | settings 正确解析，默认值合理 | `unit` → `settings loader` → `app config` | 不需要 Swagger，先看 env 和 settings | 启动配置是所有链路的前提，必须稳定 |

## 如何学习这些测试

1. 先看 `test_api.py` 和 `test_document_upload_api.py`，它们最接近真实用户路径。
2. 再看 document 系列，理解上传、读取、归档、导入、切分、检索的层次。
3. 再看 internal RAG 和 evaluation，理解 deterministic RAG 为什么可解释。
4. 最后看 approval、security、audit、rbac、logging，理解权限和观测边界。

