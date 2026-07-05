# 程序运行流程学习文档

这份文档不是测试命令清单，而是“每个测试文件对应哪条程序流”的学习文档。目标是让你知道每个测试保护什么、怎么执行、怎么观察后台日志、怎么定位源码、为什么这样设计。

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

## Swagger 和 unittest 的区别

- `Swagger` 负责验证 `API`、`Workflow` 和业务链路是否真的能从接口走通。
- `unittest` 负责验证类、方法、边界和局部逻辑是否正确。
- `Swagger` 更像“从外到内”的业务验证。
- `unittest` 更像“从内到外”的代码验证。

```text
Swagger
↓
API
↓
Workflow
↓
Business

unittest
↓
Class
↓
Method
↓
Boundary
↓
Logic
```

## 测试文件学习表

| 测试文件 | 测试目的 | 对应 API | 对应源码 | 测试命令 | 输入（入力） | 预想输出（予想結果） | Swagger 如何操作 | 后台日志观察点 | 程序执行流程 | 为什么这样设计 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `backend/tests/test_api.py` | 验证任务主链路、SSE、报告和错误封装 | `POST /api/tasks`、`GET /api/tasks/{task_id}`、`GET /api/tasks/{task_id}/events`、`GET /api/tasks/{task_id}/report` | `backend/app/api/tasks.py`、`backend/app/services/task_service.py`、`backend/app/events/sse.py` | `python3 -m unittest tests.test_api -v` | 创建任务请求、状态查询、SSE 订阅、报告查询 | HTTP 202、状态流、SSE 事件、Markdown 报告 | 打开 Swagger，先创建任务，再复制 `task_id`，再订阅 events，最后读取 report | 看 `request_id`、`task_id`、`queued/running/completed/failed`、`done/error` | `Swagger -> API -> TaskService -> Workflow -> SSE -> Report` | 这是主链路，先稳住最能代表项目运行的路径 |
| `backend/tests/test_document_upload_api.py` | 验证上传、metadata、checksum、幂等 | `POST /api/v1/documents` | `backend/app/api/documents.py`、`backend/app/services/document_upload_service.py` | `python3 -m unittest tests.test_document_upload_api -v` | `file` + `metadata` | HTTP 201，返回 `document_id` | 打开 Swagger，展开 `POST /api/v1/documents`，选文件并执行 | 看上传成功、checksum、重复校验和状态变化 | `Swagger -> API -> UploadService -> DocumentRepository -> Response` | 上传是文档链路入口，后面的 import / chunk / retrieval 都依赖它 |
| `backend/tests/test_document_read_api.py` | 验证列表、详情、过滤 | `GET /api/v1/documents`、`GET /api/v1/documents/{document_id}` | `backend/app/api/documents.py`、`backend/app/services/document_read_service.py` | `python3 -m unittest tests.test_document_read_api -v` | 文档 ID、过滤参数 | 返回列表或详情，缺失时 `document_not_found` | Swagger 中先读列表，再填 `document_id` 看详情 | 看列表过滤、命中记录和缺失日志 | `Swagger -> API -> ReadService -> Repository -> Response` | 先验证读接口，最容易确认仓库状态和过滤逻辑 |
| `backend/tests/test_document_archive_api.py` | 验证软删除/归档语义 | `DELETE /api/v1/documents/{document_id}` | `backend/app/api/document_archive.py`、`backend/app/services/document_archive_service.py` | `python3 -m unittest tests.test_document_archive_api -v` | 文档 ID | 文档进入 archived，列表默认不显示 | Swagger 中执行 DELETE，再回列表确认不再展示 | 看归档日志和列表变化日志 | `Test Client -> API -> ArchiveService -> Repository -> archived` | 要区分“归档”和“物理删除”，保留可追溯性 |
| `backend/tests/test_document_import_api.py` | 验证导入流程和状态推进 | `POST /api/v1/documents/{document_id}/import` | `backend/app/api/document_imports.py`、`backend/app/services/document_import_service.py` | `python3 -m unittest tests.test_document_import_api -v` | 文档 ID、导入请求 | 返回导入结果，状态推进 | Swagger 中先确认文档存在，再执行 import | 看 import 状态、失败原因和文档状态变化 | `Swagger -> API -> ImportService -> Repository -> validated` | 导入是结构化处理起点，决定后续 chunk 能不能跑 |
| `backend/tests/test_document_chunk_api.py` | 验证切分和 chunk 读取 | `POST /api/v1/documents/{document_id}/chunks`、`GET /api/v1/documents/{document_id}/chunks` | `backend/app/api/document_chunks.py`、`backend/app/services/document_chunk_service.py` | `python3 -m unittest tests.test_document_chunk_api -v` | 文档 ID、切分参数 | 返回 chunk 列表和稳定元数据 | Swagger 中先切分，再读 chunks 校验 | 看 chunk 数量、chunk_index、切分策略 | `Swagger -> API -> ChunkService -> ChunkRepository -> Response` | Chunk 是 retrieval / RAG 的前置数据层 |
| `backend/tests/test_document_retrieval_api.py` | 验证关键字检索、过滤、archived 排除 | `POST /api/v1/document-retrieval/search` | `backend/app/api/document_retrieval.py`、`backend/app/services/document_retrieval_service.py` | `python3 -m unittest tests.test_document_retrieval_api -v` | `query` 和过滤条件 | 返回检索结果、分数、来源 | Swagger 中先写 query，再看返回的 chunks 和 score | 看 query、过滤条件和命中 chunk | `Swagger -> API -> RetrievalProvider -> ranked chunks -> Response` | 先保证检索稳定，RAG 才有可信前提 |
| `backend/tests/test_internal_rag_api.py` | 验证 deterministic RAG 组装 | `POST /api/v1/internal-rag/answer` | `backend/app/api/internal_rag.py`、`backend/app/services/internal_rag_service.py` | `python3 -m unittest tests.test_internal_rag_api -v` | 问题文本、检索参数 | 返回 `answer`、`citations`、`confidence`、`warnings` | Swagger 中先检索再生成回答，观察 citations | 看 answer 组装、citation、confidence、warning | `Swagger -> API -> Retrieval -> Answer assembly -> Response` | 证明项目能在不接真实 LLM 时完成可解释回答 |
| `backend/tests/test_internal_rag_evaluation.py` | 验证 citation quality 和 warning 评分 | `POST /api/v1/internal-rag/answer` | `backend/app/services/internal_rag_service.py` 及评估相关代码 | `python3 -m unittest tests.test_internal_rag_evaluation -v` | 不同质量的上下文和问句 | 返回评分和 warning | 不需要单独前端，Swagger 直接观察评分字段 | 看 evaluation 评分、citation 校验和 warning taxonomy | `Test Client -> internal_rag_service -> evaluation -> Response` | 让 RAG 不只是“能答”，还要“能解释为什么这样答” |
| `backend/tests/test_rag_answer_generator.py` | 验证 stub LLM provider 和 fallback | `POST /api/v1/internal-rag/answer` | `backend/app/agents/`、`backend/app/reports/`、`backend/app/workflow/` | `python3 -m unittest tests.test_rag_answer_generator -v` | provider 状态、answer 请求 | provider 可用时走 provider，失败时回退 deterministic answer | Swagger 中直接观察 answer 是否回退 | 看 provider 名称、fallback 分支和内部日志 | `Test Client -> RAGAnswerGenerator -> StubLLMProvider / fallback` | 先把未来 LLM 替换点固定住，保证当前默认路径稳定 |
| `backend/tests/test_approval_api.py` | 验证审批提交、列表、详情、批准、拒绝、修订 | `POST /api/v1/reports/{task_id}/submit-approval`、`GET /api/v1/approvals`、`GET /api/v1/approvals/{approval_id}`、`POST /api/v1/approvals/{approval_id}/approve`、`POST /api/v1/approvals/{approval_id}/reject`、`POST /api/v1/reports/{task_id}/revise` | `backend/app/api/approvals.py`、`backend/app/services/approval_service.py` | `python3 -m unittest tests.test_approval_api -v` | `task_id`、`approval_id`、审批动作 | 返回正确的状态流转和错误码 | Swagger 中先 submit，再看 list/detail，再做 approve/reject/revise | 看 RBAC、状态变更、审计和 revision 日志 | `Swagger -> API -> ApprovalService -> ApprovalRepository -> Response` | 审批链路是 report 之后的重要边界，必须独立验证 |
| `backend/tests/test_rbac_guard.py` | 验证 approval 相关 RBAC allow / deny | 审批相关 API 权限边界 | `backend/app/services/security_service.py`、`backend/app/api/approvals.py` | `python3 -m unittest tests.test_rbac_guard -v` | 不同权限主体和审批动作 | allow 正常通过，deny 返回 `permission_denied` | Swagger 中用不同身份或测试桩观察返回 | 看 permission check 和 denied audit fact | `Test Client -> SecurityService -> Approval endpoints -> Permission check` | 把权限规则单独测试，避免散落在接口里 |
| `backend/tests/test_audit_middleware.py` | 验证审批审计中间件的 success / deny / failure | 审批相关 API 的中间件边界 | `backend/app/events/`、`backend/app/api/`、`backend/app/services/audit_service.py` | `python3 -m unittest tests.test_audit_middleware -v` | 审批动作请求、异常路径请求 | 审计事实被记录，失败路径仍可追踪 | Swagger 触发审批，再检查 audit logs 或测试断言 | 看 append-only 写入、失败路径和日志事件 | `Test Client -> Middleware -> AuditService -> append-only audit log` | 审计必须 append-only，错误路径也不能丢事实 |
| `backend/tests/test_security_audit_api.py` | 验证 current user、roles、permissions、audit logs | `GET /api/v1/users/me`、`GET /api/v1/security/roles`、`GET /api/v1/security/permissions`、`GET /api/v1/audit-logs` | `backend/app/api/security.py`、`backend/app/api/audit_logs.py`、`backend/app/services/security_service.py`、`backend/app/services/audit_service.py` | `python3 -m unittest tests.test_security_audit_api -v` | 无或少量分页参数 | 返回 placeholder principal、冻结目录、审计列表 | Swagger 依次打开四个 GET，确认返回结构 | 看 current user、role catalog、permission catalog、audit list | `Swagger -> API -> SecurityService / AuditService -> Response` | 先固定安全读模型，未来真实认证才有替换基线 |
| `backend/tests/test_file_inputs.py` | 验证本地文件输入读取 | 内部数据加载边界 | `backend/app/data_loaders/`、`backend/app/kpi/`、`backend/app/agents/providers/` | `python3 -m unittest tests.test_file_inputs -v` | CSV、JSON、Markdown | 读取到稳定的本地数据结构 | 不需要 Swagger，直接看本地数据文件和测试断言 | 看文件读取、解析结果和数据完整性 | `unit -> data_loaders -> local files -> parsed data` | 本地静态数据是当前阶段可运行的基础 |
| `backend/tests/test_document_domain.py` | 验证文档领域模型和 InMemory 仓库规则 | 领域模型边界 | `backend/app/models/document.py`、`backend/app/repositories/interfaces/document_repository.py`、`backend/app/repositories/implementations/in_memory/document_repository.py` | `python3 -m unittest tests.test_document_domain -v` | 文档对象、元数据、状态变更请求 | 创建、状态迁移、去重、CRUD 规则正确 | 不需要 Swagger，先看领域对象再看测试 | 看状态迁移、checksum 重复检测和 CRUD 行为 | `unit -> document model -> document repository -> assertions` | 先把领域约束固定住，接口层才稳定 |
| `backend/tests/test_repositories.py` | 验证 Repository 接口边界 | 存储抽象边界 | `backend/app/repositories/interfaces/` | `python3 -m unittest tests.test_repositories -v` | 仓库实现对象 | 满足最小协议要求 | 不需要 Swagger，直接看接口定义和测试实现 | 看协议方法和抽象依赖 | `unit -> Protocol -> repository interface -> contract check` | Repository 模式的核心价值是解耦存储和业务 |
| `backend/tests/test_repository_backend_switch.py` | 验证 InMemory 默认和 PostgreSQL 开关 | 组合根和配置边界 | `backend/app/config/container.py`、`backend/app/db/connection.py` | `python3 -m unittest tests.test_repository_backend_switch -v` | 环境变量、backend 配置 | 默认仍用 InMemory，满足条件才走 PostgreSQL | 不需要 Swagger，查看配置和测试输出 | 看 backend 选择、环境变量和依赖注入 | `unit -> container.py -> backend switch -> repository backend selection` | 仓库切换必须显式，不破坏默认学习路径 |
| `backend/tests/test_postgres_repositories.py` | 验证 PostgreSQL 持久化冒烟测试 | 可选环境验证 | `backend/app/repositories/postgres/` 相关实现 | `python3 -m unittest tests.test_postgres_repositories -v` | `psycopg` + PostgreSQL 连接配置 | 环境满足时通过，缺少依赖时跳过 | 不需要 Swagger，先确认本机是否有 Docker / psycopg | 看连接、写入、读取和跳过原因 | `integration-like test -> postgres repository -> database roundtrip` | 证明仓库抽象能切到 PostgreSQL，但不影响默认本地运行 |
| `backend/tests/test_settings.py` | 验证环境变量和配置解析 | 启动配置边界 | `backend/app/config/`、`backend/app/main.py` | `python3 -m unittest tests.test_settings -v` | 环境变量和默认值 | settings 正确解析，默认值合理 | 不需要 Swagger，先看 env 和 settings | 看配置加载、默认值和错误提示 | `unit -> settings loader -> app config -> startup` | 启动配置是所有链路的前提，必须稳定 |

## 每个测试保护什么

- `backend/tests/test_api.py` 保护任务主链路、SSE 和报告，防止任务跑通后拿不到结果。
- `backend/tests/test_document_upload_api.py` 保护文档入口，防止上传、重复校验和幂等性失效。
- `backend/tests/test_document_read_api.py` 保护列表和详情，防止文档查询和过滤错误。
- `backend/tests/test_document_archive_api.py` 保护软删除语义，防止误做物理删除。
- `backend/tests/test_document_import_api.py` 保护导入状态机，防止未验证文档被继续处理。
- `backend/tests/test_document_chunk_api.py` 保护切分逻辑，防止 chunk 结果不稳定。
- `backend/tests/test_document_retrieval_api.py` 保护检索排序和过滤，防止检索到不该返回的数据。
- `backend/tests/test_internal_rag_api.py` 保护可解释答案，防止无依据回答。
- `backend/tests/test_internal_rag_evaluation.py` 保护 citation 质量，防止答案质量下降却没有告警。
- `backend/tests/test_rag_answer_generator.py` 保护未来 `LLM` 接缝，防止 provider 故障影响当前默认路径。
- `backend/tests/test_approval_api.py` 保护审批流程，防止状态机和修订逻辑出错。
- `backend/tests/test_rbac_guard.py` 保护审批权限，防止越权访问。
- `backend/tests/test_audit_middleware.py` 保护审计完整性，防止关键操作没有被记录。
- `backend/tests/test_security_audit_api.py` 保护安全读模型，防止 current user、roles、permissions 和 audit 视图失真。
- `backend/tests/test_file_inputs.py` 保护本地静态数据输入，防止基础样本文件读取失败。
- `backend/tests/test_document_domain.py` 保护文档领域规则，防止状态迁移和去重失控。
- `backend/tests/test_repositories.py` 保护 `Repository` 合同，防止存储抽象漂移。
- `backend/tests/test_repository_backend_switch.py` 保护默认后端切换边界，防止 InMemory 和 PostgreSQL 互相污染。
- `backend/tests/test_postgres_repositories.py` 保护可选 PostgreSQL 能力，防止未来迁移路径失真。
- `backend/tests/test_settings.py` 保护启动配置，防止环境变量解析错误。

## 每个测试保护的能力

- 任务主链路能力
- 文档上传和读取能力
- 文档归档和导入能力
- 文档切分和检索能力
- 无 `LLM` 的 `RAG` 能力
- 审批与修订能力
- 审批权限控制能力
- 审计追踪能力
- 安全读模型能力
- 本地静态数据能力
- 领域模型稳定性
- `Repository` 抽象能力
- InMemory / PostgreSQL 可切换能力
- 启动配置能力

## 学习日志

运行接口或测试以后，重点观察这些内容：

1. 后台应该出现哪些日志字段。
2. 程序经过哪些模块。
3. 哪些步骤是输入，哪些步骤是输出。
4. 下一步该读哪份源码和哪份学习文档。

学习路径固定为：

```text
Swagger
↓
Backend Log
↓
TEST_CASES
↓
Source Code
```

## 怎么继续学

1. 先看 `test_api.py` 和 `test_document_upload_api.py`，它们最接近真实用户路径。
2. 再看 document 系列，理解上传、读取、归档、导入、切分、检索的层次。
3. 再看 internal RAG 和 evaluation，理解 deterministic RAG 为什么可解释。
4. 最后看 approval、security、audit、rbac、logging，理解权限和观测边界。

## 分测试文件学习说明

### backend/tests/test_api.py

- 测试目的：验证任务主链路、SSE 和报告是否一起跑通。
- 对应 API：`POST /api/tasks`、`GET /api/tasks/{task_id}`、`GET /api/tasks/{task_id}/events`、`GET /api/tasks/{task_id}/report`
- 测试命令：`cd backend && python3 -m unittest tests.test_api -v`
- 输入（入力）：创建任务请求、任务 ID、SSE 订阅、报告查询
- 预想输出（予想結果）：HTTP 202、状态流、SSE 事件、Markdown 报告
- Swagger 对应操作：先创建任务，再复制 `task_id`，再看状态、事件和报告
- 后端程序流程：

```text
Swagger
→ API
→ TaskService
→ Workflow
→ SSE
→ Report
→ Response
```

- LearningLog / 后台日志观察点：`request_id`、`task_id`、`queued/running/completed/failed`、`done/error`
- 对应源码：`backend/app/api/tasks.py`、`backend/app/services/task_service.py`、`backend/app/events/sse.py`
- 为什么设计这个测试：这是主链路，必须先稳住最能代表项目运行的路径。

### backend/tests/test_document_upload_api.py

- 测试目的：验证文档上传能接收文件和 metadata，并生成 `document_id`。
- 对应 API：`POST /api/v1/documents`
- 测试命令：`cd backend && python3 -m unittest tests.test_document_upload_api -v`
- 输入（入力）：`file`、`metadata`
- 预想输出（予想結果）：HTTP 201、`document_id`、`status=uploaded`
- Swagger 对应操作：打开 `POST /api/v1/documents`，选择文件并执行
- 后端程序流程：

```text
Swagger
→ API
→ DocumentUploadService
→ InMemoryDocumentRepository
→ Response
```

- LearningLog / 后台日志观察点：上传成功日志、checksum、重复校验、状态变化
- 对应源码：`backend/app/api/documents.py`、`backend/app/services/document_upload_service.py`
- 为什么设计这个测试：上传是文档链路入口，后面的 import / chunk / retrieval 都依赖它。

### backend/tests/test_document_read_api.py

- 测试目的：验证文档列表和详情查询。
- 对应 API：`GET /api/v1/documents`、`GET /api/v1/documents/{document_id}`
- 测试命令：`cd backend && python3 -m unittest tests.test_document_read_api -v`
- 输入（入力）：文档 ID、过滤参数
- 预想输出（予想結果）：列表或详情返回正确；缺失时返回 `document_not_found`
- Swagger 对应操作：先读列表，再填 `document_id` 看详情
- 后端程序流程：

```text
Swagger
→ API
→ DocumentReadService
→ Repository
→ Response
```

- LearningLog / 后台日志观察点：列表过滤、命中记录、缺失日志
- 对应源码：`backend/app/api/documents.py`、`backend/app/services/document_read_service.py`
- 为什么设计这个测试：先验证读接口，最容易确认仓库状态和过滤逻辑。

### backend/tests/test_document_archive_api.py

- 测试目的：验证软删除/归档语义。
- 对应 API：`DELETE /api/v1/documents/{document_id}`
- 测试命令：`cd backend && python3 -m unittest tests.test_document_archive_api -v`
- 输入（入力）：文档 ID
- 预想输出（予想結果）：文档进入 archived，列表默认不显示
- Swagger 对应操作：执行 DELETE，再回列表确认
- 后端程序流程：

```text
Test Client / Swagger
→ API
→ DocumentArchiveService
→ Repository
→ archived
```

- LearningLog / 后台日志观察点：归档日志、列表变化日志
- 对应源码：`backend/app/api/document_archive.py`、`backend/app/services/document_archive_service.py`
- 为什么设计这个测试：要区分“归档”和“物理删除”，保留可追溯性。

### backend/tests/test_document_import_api.py

- 测试目的：验证导入流程和状态推进。
- 对应 API：`POST /api/v1/documents/{document_id}/import`
- 测试命令：`cd backend && python3 -m unittest tests.test_document_import_api -v`
- 输入（入力）：文档 ID、导入请求
- 预想输出（予想結果）：返回导入结果，状态推进
- Swagger 对应操作：先确认文档存在，再执行 import
- 后端程序流程：

```text
Swagger
→ API
→ DocumentImportService
→ Repository
→ validated
```

- LearningLog / 后台日志观察点：`import` 状态、失败原因、文档状态变化
- 对应源码：`backend/app/api/document_imports.py`、`backend/app/services/document_import_service.py`
- 为什么设计这个测试：导入是结构化处理起点，决定后续 chunk 能不能跑。

### backend/tests/test_document_chunk_api.py

- 测试目的：验证切分和 chunk 读取。
- 对应 API：`POST /api/v1/documents/{document_id}/chunks`、`GET /api/v1/documents/{document_id}/chunks`
- 测试命令：`cd backend && python3 -m unittest tests.test_document_chunk_api -v`
- 输入（入力）：文档 ID、切分参数
- 预想输出（予想結果）：chunk 列表和稳定元数据
- Swagger 对应操作：先切分，再读 chunks 校验
- 后端程序流程：

```text
Swagger
→ API
→ DocumentChunkService
→ ChunkRepository
→ Response
```

- LearningLog / 后台日志观察点：chunk 数量、`chunk_index`、切分策略
- 对应源码：`backend/app/api/document_chunks.py`、`backend/app/services/document_chunk_service.py`
- 为什么设计这个测试：Chunk 是 retrieval / RAG 的前置数据层。

### backend/tests/test_document_retrieval_api.py

- 测试目的：验证关键字检索、过滤和 archived 排除。
- 对应 API：`POST /api/v1/document-retrieval/search`
- 测试命令：`cd backend && python3 -m unittest tests.test_document_retrieval_api -v`
- 输入（入力）：`query` 和过滤条件
- 预想输出（予想結果）：检索结果、分数、来源
- Swagger 对应操作：写 query，再看返回的 chunks 和 score
- 后端程序流程：

```text
Swagger
→ API
→ RetrievalProvider
→ Ranked Chunks
→ Response
```

- LearningLog / 后台日志观察点：`query`、过滤条件、命中 chunk
- 对应源码：`backend/app/api/document_retrieval.py`、`backend/app/services/document_retrieval_service.py`
- 为什么设计这个测试：先保证检索稳定，RAG 才有可信前提。

### backend/tests/test_internal_rag_api.py

- 测试目的：验证 deterministic RAG 组装。
- 对应 API：`POST /api/v1/internal-rag/answer`
- 测试命令：`cd backend && python3 -m unittest tests.test_internal_rag_api -v`
- 输入（入力）：问题文本、检索参数
- 预想输出（予想結果）：`answer`、`citations`、`confidence`、`warnings`
- Swagger 对应操作：先检索再生成回答，观察 citations
- 后端程序流程：

```text
Swagger
→ API
→ Retrieval
→ Answer Assembly
→ Response
```

- LearningLog / 后台日志观察点：answer 组装、citation、confidence、warning
- 对应源码：`backend/app/api/internal_rag.py`、`backend/app/services/internal_rag_service.py`
- 为什么设计这个测试：证明项目能在不接真实 LLM 时完成可解释回答。

### backend/tests/test_internal_rag_evaluation.py

- 测试目的：验证 citation quality 和 warning 评分。
- 对应 API：`POST /api/v1/internal-rag/answer`
- 测试命令：`cd backend && python3 -m unittest tests.test_internal_rag_evaluation -v`
- 输入（入力）：不同质量的上下文和问句
- 预想输出（予想結果）：评分和 warning
- Swagger 对应操作：直接观察评分字段
- 后端程序流程：

```text
Test Client
→ internal_rag_service
→ evaluation
→ Response
```

- LearningLog / 后台日志观察点：evaluation 评分、citation 校验、warning taxonomy
- 对应源码：`backend/app/services/internal_rag_service.py`
- 为什么设计这个测试：让 RAG 不只是“能答”，还要“能解释为什么这样答”。

### backend/tests/test_rag_answer_generator.py

- 测试目的：验证 stub LLM provider 和 fallback。
- 对应 API：`POST /api/v1/internal-rag/answer`
- 测试命令：`cd backend && python3 -m unittest tests.test_rag_answer_generator -v`
- 输入（入力）：provider 状态、answer 请求
- 预想输出（予想結果）：provider 可用时走 provider，失败时回退 deterministic answer
- Swagger 对应操作：观察 answer 是否回退
- 后端程序流程：

```text
Test Client
→ RAGAnswerGenerator
→ StubLLMProvider / fallback
→ Response
```

- LearningLog / 后台日志观察点：provider 名称、fallback 分支、内部日志
- 对应源码：`backend/app/agents/`、`backend/app/reports/`、`backend/app/workflow/`
- 为什么设计这个测试：先把未来 LLM 替换点固定住，保证当前默认路径稳定。

### backend/tests/test_approval_api.py

- 测试目的：验证审批提交、列表、详情、批准、拒绝、修订。
- 对应 API：`POST /api/v1/reports/{task_id}/submit-approval`、`GET /api/v1/approvals`、`GET /api/v1/approvals/{approval_id}`、`POST /api/v1/approvals/{approval_id}/approve`、`POST /api/v1/approvals/{approval_id}/reject`、`POST /api/v1/reports/{task_id}/revise`
- 测试命令：`cd backend && python3 -m unittest tests.test_approval_api -v`
- 输入（入力）：`task_id`、`approval_id`、审批动作
- 预想输出（予想結果）：状态流转正确，错误码正确
- Swagger 对应操作：先 submit，再看 list/detail，再做 approve/reject/revise
- 后端程序流程：

```text
Swagger
→ API
→ ApprovalService
→ ApprovalRepository
→ Response
```

- LearningLog / 后台日志观察点：RBAC、状态变更、审计和 revision 日志
- 对应源码：`backend/app/api/approvals.py`、`backend/app/services/approval_service.py`
- 为什么设计这个测试：审批链路是 report 之后的重要边界，必须独立验证。

### backend/tests/test_rbac_guard.py

- 测试目的：验证 approval 相关 RBAC allow / deny。
- 对应 API：审批相关 API 权限边界
- 测试命令：`cd backend && python3 -m unittest tests.test_rbac_guard -v`
- 输入（入力）：不同权限主体和审批动作
- 预想输出（予想結果）：allow 正常通过，deny 返回 `permission_denied`
- Swagger 对应操作：用不同身份或测试桩观察返回
- 后端程序流程：

```text
Test Client
→ SecurityService
→ Approval endpoints
→ Permission check
→ allow / deny
```

- LearningLog / 后台日志观察点：permission check、denied audit fact
- 对应源码：`backend/app/services/security_service.py`、`backend/app/api/approvals.py`
- 为什么设计这个测试：把权限规则单独测试，避免散落在接口里。

### backend/tests/test_audit_middleware.py

- 测试目的：验证审批审计中间件的 success / deny / failure。
- 对应 API：审批相关 API 的中间件边界
- 测试命令：`cd backend && python3 -m unittest tests.test_audit_middleware -v`
- 输入（入力）：审批动作请求、异常路径请求
- 预想输出（予想結果）：审计事实被记录，失败路径仍可追踪
- Swagger 对应操作：触发审批，再检查 audit logs 或测试断言
- 后端程序流程：

```text
Test Client
→ Middleware
→ AuditService
→ Append-only Audit Log
→ Response
```

- LearningLog / 后台日志观察点：append-only 写入、失败路径、日志事件
- 对应源码：`backend/app/events/`、`backend/app/api/`、`backend/app/services/audit_service.py`
- 为什么设计这个测试：审计必须 append-only，错误路径也不能丢事实。

### backend/tests/test_security_audit_api.py

- 测试目的：验证 current user、roles、permissions、audit logs。
- 对应 API：`GET /api/v1/users/me`、`GET /api/v1/security/roles`、`GET /api/v1/security/permissions`、`GET /api/v1/audit-logs`
- 测试命令：`cd backend && python3 -m unittest tests.test_security_audit_api -v`
- 输入（入力）：无或少量分页参数
- 预想输出（予想結果）：placeholder principal、冻结目录、审计列表
- Swagger 对应操作：依次打开四个 GET，确认返回结构
- 后端程序流程：

```text
Swagger
→ API
→ SecurityService / AuditService
→ Response
```

- LearningLog / 后台日志观察点：current user、role catalog、permission catalog、audit list
- 对应源码：`backend/app/api/security.py`、`backend/app/api/audit_logs.py`、`backend/app/services/security_service.py`、`backend/app/services/audit_service.py`
- 为什么设计这个测试：先固定安全读模型，未来真实认证才有替换基线。

### backend/tests/test_file_inputs.py

- 测试目的：验证本地文件输入读取。
- 对应 API：无，属于内部数据加载边界
- 测试命令：`cd backend && python3 -m unittest tests.test_file_inputs -v`
- 输入（入力）：CSV、JSON、Markdown
- 预想输出（予想結果）：读取到稳定的本地数据结构
- Swagger 对应操作：不需要 Swagger
- 后端程序流程：

```text
unit
→ data_loaders
→ local files
→ parsed data
```

- LearningLog / 后台日志观察点：文件读取、解析结果、数据完整性
- 对应源码：`backend/app/data_loaders/`、`backend/app/kpi/`、`backend/app/agents/providers/`
- 为什么设计这个测试：本地静态数据是当前阶段可运行的基础。

### backend/tests/test_document_domain.py

- 测试目的：验证文档领域模型和 InMemory 仓库规则。
- 对应 API：无，属于领域模型边界
- 测试命令：`cd backend && python3 -m unittest tests.test_document_domain -v`
- 输入（入力）：文档对象、元数据、状态变更请求
- 预想输出（予想結果）：创建、状态迁移、去重、CRUD 规则正确
- Swagger 对应操作：不需要 Swagger
- 后端程序流程：

```text
unit
→ document model
→ document repository
→ assertions
```

- LearningLog / 后台日志观察点：状态迁移、checksum 重复检测、CRUD 行为
- 对应源码：`backend/app/models/document.py`、`backend/app/repositories/interfaces/document_repository.py`、`backend/app/repositories/implementations/in_memory/document_repository.py`
- 为什么设计这个测试：先把领域约束固定住，接口层才稳定。

### backend/tests/test_repositories.py

- 测试目的：验证 `Repository` 接口边界。
- 对应 API：无，属于存储抽象边界
- 测试命令：`cd backend && python3 -m unittest tests.test_repositories -v`
- 输入（入力）：仓库实现对象
- 预想输出（予想結果）：满足最小协议要求
- Swagger 对应操作：不需要 Swagger
- 后端程序流程：

```text
unit
→ Protocol
→ repository interface
→ contract check
```

- LearningLog / 后台日志观察点：协议方法、抽象依赖
- 对应源码：`backend/app/repositories/interfaces/`
- 为什么设计这个测试：`Repository` 模式的核心价值是解耦存储和业务。

### backend/tests/test_repository_backend_switch.py

- 测试目的：验证 InMemory 默认和 PostgreSQL 开关。
- 对应 API：无，属于组合根和配置边界
- 测试命令：`cd backend && python3 -m unittest tests.test_repository_backend_switch -v`
- 输入（入力）：环境变量、backend 配置
- 预想输出（予想結果）：默认仍用 InMemory，满足条件才走 PostgreSQL
- Swagger 对应操作：不需要 Swagger
- 后端程序流程：

```text
unit
→ container.py
→ backend switch
→ repository backend selection
```

- LearningLog / 后台日志观察点：backend 选择、环境变量、依赖注入
- 对应源码：`backend/app/config/container.py`、`backend/app/db/connection.py`
- 为什么设计这个测试：仓库切换必须显式，不破坏默认学习路径。

### backend/tests/test_postgres_repositories.py

- 测试目的：验证 PostgreSQL 持久化冒烟测试。
- 对应 API：无，属于可选环境验证
- 测试命令：`cd backend && python3 -m unittest tests.test_postgres_repositories -v`
- 输入（入力）：`psycopg` + PostgreSQL 连接配置
- 预想输出（予想結果）：环境满足时通过，缺少依赖时跳过
- Swagger 对应操作：不需要 Swagger
- 后端程序流程：

```text
integration-like test
→ postgres repository
→ database roundtrip
→ assertions
```

- LearningLog / 后台日志观察点：连接、写入、读取、跳过原因
- 对应源码：`backend/app/repositories/postgres/` 相关实现
- 为什么设计这个测试：证明仓库抽象能切到 PostgreSQL，但不影响默认本地运行。

### backend/tests/test_settings.py

- 测试目的：验证环境变量和配置解析。
- 对应 API：无，属于启动配置边界
- 测试命令：`cd backend && python3 -m unittest tests.test_settings -v`
- 输入（入力）：环境变量和默认值
- 预想输出（予想結果）：settings 正确解析，默认值合理
- Swagger 对应操作：不需要 Swagger
- 后端程序流程：

```text
unit
→ settings loader
→ app config
→ startup
```

- LearningLog / 后台日志观察点：配置加载、默认值、错误提示
- 对应源码：`backend/app/config/`、`backend/app/main.py`
- 为什么设计这个测试：启动配置是所有链路的前提，必须稳定。
