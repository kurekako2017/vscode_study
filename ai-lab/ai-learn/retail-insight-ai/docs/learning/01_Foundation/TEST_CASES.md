# 测试用例学习文档

这份文档用于按 `测试总览表 -> 测试详细表 -> 后端程序流程` 的顺序学习测试。表格负责导航，章节负责学习；所有测试命令、输入、输出、Swagger 操作、后台 Log、源码位置和设计理由都保留。

## 先理解 Swagger 和 unittest

| 项目 | 内容 |
|---|---|
| Swagger | FastAPI 自动生成的 API 调试与验证工具，不是测试环境，也不是正式 UI |
| unittest | 验证单个模块、类、方法、边界和局部逻辑 |
| V1.0 当前验收 | Swagger 用于手工 API 调试；unittest / vitest / Stub E2E / Compose 用于回归与交付验收 |
| 历史阶段记录 | 早期曾写「先用 Swagger 验证后端骨架，再用 unittest」——该句保留为学习史，**不是** V1.0 唯一路径 |
| 执行目录 | 测试命令默认在 `backend/` 目录执行 |
| 常见错误 | `ModuleNotFoundError: No module named tests` 通常说明执行目录错了 |
| 正式前端导航 | `学习总览 → 文書管理 → RAG検索 → 分析依頼 → 承認管理`（与 `App.tsx` 一致） |

## 企业项目验证体系

| 层级 | 工具 | 目的 |
|---|---|---|
| 单元测试（Unit Test） | `python -m unittest` | 验证单个模块或类的逻辑是否正确 |
| 接口验证（API Verification） | Swagger UI `/docs` | 手工验证 API 请求、响应和业务流程 |
| 前后端集成测试（Integration Test） | React + FastAPI | 验证完整用户操作流程 |
| 端到端测试（E2E Test） | Playwright / Cypress | 模拟真实用户完成整个业务流程 |

V1.0 补充（不删除上表）：

| 层级 | 当前仓库入口 | 目的 |
|---|---|---|
| Stub API E2E | `./scripts/run_api_e2e.sh` / `tests.test_e2e_api_stub_flow` | 企业业务链 HTTP 验收，默认零真实 LLM |
| Compose 验收 | `compose_up` + `compose_verify` | 容器健康、迁移、SPA 路由 |
| Frontend Vitest | `cd frontend && npm test` | UI / Auth / RBAC / Lifecycle / Learning Dashboard |
| 业务样例数据 | `docs/learning/sample-data/Scenario01_Sales_Decline/` | 人工业务数据验证 |

V1.0 自动化数量基线（与 `RUNBOOK_LOCAL.md` Appendix N 一致）：

| Suite | 基线 |
|---|---|
| Backend PostgreSQL | 281 tests，2 skipped（real smoke 默认 skip） |
| Backend InMemory | 270 tests，52 skipped |
| Frontend | 113 / 113 |
| Production build / compileall / diff-check | 通过 |

# 测试总览

| 序号 | 测试文件 | 对应API | 保护能力 | 保护的 Bug / 风险 | 命令 | 对应Service | 状态 |
|---|---|---|---|---|---|---|---|
| 01 | `test_api.py` | tasks / events / report | 任务主链路、SSE、报告 | 防止主链路返回 500、防止 SSE done/error 丢失、防止报告读取不稳定 | `python -m unittest tests.test_api -v` | `TaskService` | 主路径 |
| 02 | `test_document_upload_api.py` | `POST /api/v1/documents` | 上传、metadata、checksum | 防止上传入口破坏、防止 checksum 去重失效、防止 metadata 解析错误 | `python -m unittest tests.test_document_upload_api -v` | `DocumentUploadService` | 主路径 |
| 03 | `test_document_read_api.py` | documents list / detail | 列表、详情、过滤 | 防止 `document_not_found` 不稳定、防止过滤条件失效、防止详情字段缺失 | `python -m unittest tests.test_document_read_api -v` | `DocumentReadService` | 主路径 |
| 04 | `test_document_archive_api.py` | `DELETE /api/v1/documents/{document_id}` | archive 语义 | 防止误做 hard delete、防止 archived 文档仍出现在默认列表 | `python -m unittest tests.test_document_archive_api -v` | `DocumentArchiveService` | 主路径 |
| 05 | `test_document_import_api.py` | document import | 导入流程和状态推进 | 防止未导入文档进入 chunk、防止非法状态继续推进 | `python -m unittest tests.test_document_import_api -v` | `DocumentImportService` | 主路径 |
| 06 | `test_document_chunk_api.py` | document chunks | 切分和 chunk 读取 | 防止 chunk 顺序错乱、防止重复切分残留旧 chunk、防止空内容切分异常 | `python -m unittest tests.test_document_chunk_api -v` | `DocumentChunkService` | 主路径 |
| 07 | `test_document_retrieval_api.py` | retrieval search | 检索、过滤、排序 | 防止检索排序不稳定、防止 source trace 丢失、防止过滤条件越界 | `python -m unittest tests.test_document_retrieval_api -v` | `DocumentRetrievalService` | 主路径 |
| 08 | `test_internal_rag_api.py` | internal-rag answer | deterministic RAG 主路径 | 防止 RAG answer 返回空、防止 citations 丢失、防止无 LLM 默认路径破坏 | `python -m unittest tests.test_internal_rag_api -v` | `InternalRagService` | 主路径 |
| 09 | `test_internal_rag_evaluation.py` | internal-rag answer | citation 和 warning 质量 | 防止 citation 质量退化、防止 warning 规则失效、防止低证据答案被误判成功 | `python -m unittest tests.test_internal_rag_evaluation -v` | `InternalRagEvaluationService` | 质量路径 |
| 10 | `test_rag_answer_generator.py` | internal-rag answer | provider 与 fallback | 防止 LLMProvider 失败时没有 fallback、防止 citation-safe contract 被破坏 | `python -m unittest tests.test_rag_answer_generator -v` | `RAGAnswerGenerator` | fallback 路径 |
| 11 | `test_approval_api.py` | approval APIs | 审批状态机 | 防止审批状态跳转错误、防止 approve/reject 后状态不一致 | `python -m unittest tests.test_approval_api -v` | `ApprovalService` | 主路径 |
| 12 | `test_rbac_guard.py` | approval APIs | RBAC allow / deny | 防止审批越权、防止角色权限判断反转、防止默认放行 | `python -m unittest tests.test_rbac_guard -v` | `SecurityService` | 权限路径 |
| 13 | `test_audit_middleware.py` | approval / audit | 审计事实记录 | 防止审计日志缺 request_id / actor / action、防止失败请求无记录 | `python -m unittest tests.test_audit_middleware -v` | `AuditMiddleware` / `AuditService` | 审计路径 |
| 14 | `test_security_audit_api.py` | users / roles / permissions / audit | 安全读模型 | 防止用户、角色、权限和 audit logs 读模型字段漂移 | `python -m unittest tests.test_security_audit_api -v` | `SecurityService` / `AuditService` | 主路径 |
| 15 | `test_file_inputs.py` | 无公开 API | 本地文件输入 | 防止样例文件路径变化后读取失败、防止编码和空文件边界破坏 | `python -m unittest tests.test_file_inputs -v` | 文件读取逻辑 | 单元路径 |
| 16 | `test_document_domain.py` | documents 间接对应 | 领域模型规则 | 防止 Document 状态、metadata、checksum 等领域规则退化 | `python -m unittest tests.test_document_domain -v` | Domain Logic | 领域路径 |
| 17 | `test_repositories.py` | 无公开 API | Repository 合同 | 防止 Repository interface 与 InMemory 实现不一致 | `python -m unittest tests.test_repositories -v` | 无 | 合同路径 |
| 18 | `test_settings.py` | 全局间接影响 | 配置解析 | 防止环境变量解析错误、防止默认配置影响本地学习路径 | `python -m unittest tests.test_settings -v` | Settings | 配置路径 |
| 19 | `test_repository_backend_switch.py` | 全局间接影响 | 仓库后端切换 | 防止切换错误破坏 InMemory 默认学习路径 | `python -m unittest tests.test_repository_backend_switch -v` | Container / Config | 配置路径 |
| 20 | `test_postgres_repositories.py` | 全局间接影响 | PostgreSQL 合同路径 | 防止 PostgreSQL repository contract 与 InMemory 合同分叉；**V1.0 正式验收含 PG 全量 suite** | `python -m unittest tests.test_postgres_repositories -v` | Repository Layer | 主验收路径（需 DATABASE_URL） |
| 21 | `test_logging.py` | 全局间接影响 | 结构化日志 | 防止日志缺少 request_id / task_id / error_code、防止敏感信息输出 | `python -m unittest tests.test_logging -v` | logging helpers | 观测路径 |
| 22 | `test_authentication.py` | login / users/me / JWT | JWT 签发、解析、时钟偏差 leeway | 防止签名错误被放行、防止时钟回拨导致随机 401、防止 jti 合同漂移 | `python -m unittest tests.test_authentication -v` | `JWTService` / `AuthenticationService` | 安全路径 |
| 23 | `test_authorization.py` | 受保护 API | RBAC Permission | 防止角色越权、防止未知角色 fail-open | `python -m unittest tests.test_authorization -v` | `AuthorizationService` | 权限路径 |
| 24 | `test_ai_analysis_api.py` | `POST /api/v1/ai-analysis` | low_cost 分析、幂等、额度、Evidence Gate | 防止无确认调用、防止幂等双计费、防止证据门禁失效 | `python -m unittest tests.test_ai_analysis_api -v` | `AIAnalysisService` / LLM Gateway | 主路径 |
| 25 | `test_executive_report_api.py` | `POST /api/v1/executive-reports` | high_quality 报告、审批入口 | 防止报告路由进 low_cost、防止自动 submit approval、防止额度串台 | `python -m unittest tests.test_executive_report_api -v` | `ExecutiveReportService` | 主路径 |
| 26 | `test_provider_fallback_chain.py` | LLM Gateway 间接 | Fallback Chain 顺序与熔断 | 防止顺序乱序、防止熔断后仍计费、防止跨 tier 串模型 | `python -m unittest tests.test_provider_fallback_chain -v` | ProviderChain | 韧性路径 |
| 27 | `test_e2e_api_stub_flow.py` | 企业业务链多 API | Stub 端到端 | 防止 Compose/API 链路上权限与文档流断裂 | `python -m unittest tests.test_e2e_api_stub_flow -v` 或 `./scripts/run_api_e2e.sh` | 多 Service | E2E 路径 |
| 28 | `test_openrouter_real_smoke.py` | 真实 OpenRouter（opt-in） | 真网 smoke | 防止默认 suite 产生费用；仅 `RUN_REAL_LLM_SMOKE=1` 时执行 | 默认 **skip** | OpenRouter Provider | 可选路径 |

说明：序号 01～21 为历史学习总览，**全部保留**。22～28 为 V1.0 增量登记；仓库中还有 `test_vector_retrieval.py`、`test_embedding_factory.py` 等文件，可按同样表格模板继续追加，不在此删除旧章。

## backend/tests/test_api.py

| 项目 | 内容 |
|---|---|
| 测试目的 | 验证任务主链路、SSE 事件和报告读取是否一起跑通 |
| 对应API | `POST /api/tasks`、`GET /api/tasks/{task_id}`、`GET /api/tasks/{task_id}/events`、`GET /api/tasks/{task_id}/report` |
| 测试命令 | `cd backend && python -m unittest tests.test_api -v` |
| 输入（入力） | 创建任务请求、`task_id`、状态查询、SSE 订阅、报告查询 |
| 预想输出（予想結果） | HTTP `202`、状态流、SSE 事件、Markdown 报告 |
| Swagger对应操作 | 创建任务 → 复制 `task_id` → 查询状态 → 订阅 events → 读取 report |
| 后台观察 | `request_id`、`task_id`、`queued/running/completed/failed`、`done/error` |
| 对应源码 | `backend/app/api/tasks.py`、`backend/app/services/task_service.py`、`backend/app/events/sse.py` |
| 为什么设计 | 主链路最能代表项目是否真的可运行，必须优先保护 |

### 后端程序流程

```text
TestClient
↓
backend/app/api/tasks.py
create_task() / get_task() / get_task_events() / get_report()
↓
backend/app/services/task_service.py
TaskService.create_task() / get_task() / get_report()
↓
backend/app/repositories/implementations/in_memory/task_repository.py
InMemoryTaskRepository.create() / get()
↓
backend/app/repositories/implementations/in_memory/report_repository.py
InMemoryReportRepository.get()
↓
Response
```

## backend/tests/test_document_upload_api.py

| 项目 | 内容 |
|---|---|
| 测试目的 | 验证上传流程、metadata 解析、checksum 去重和文档创建 |
| 对应API | `POST /api/v1/documents` |
| 测试命令 | `cd backend && python -m unittest tests.test_document_upload_api -v` |
| 输入（入力） | `file`、`metadata`、重复文件 |
| 预想输出（予想結果） | HTTP `201`，返回 `document_id`、上传状态；异常输入返回稳定错误 |
| Swagger对应操作 | 打开 `POST /api/v1/documents` → 选择文件 → 填 metadata → Execute |
| 后台观察 | checksum、`document_id`、上传状态、重复校验 |
| 对应源码 | `backend/app/api/documents.py`、`backend/app/services/document_upload_service.py` |
| 为什么设计 | Upload 是整个 Document Pipeline 入口，后续 import、chunk、retrieval 都依赖它 |

### 后端程序流程

```text
TestClient
↓
backend/app/api/documents.py
upload_document()
↓
backend/app/services/document_upload_service.py
DocumentUploadService.upload_document()
↓
backend/app/repositories/implementations/in_memory/document_repository.py
InMemoryDocumentRepository.create()
↓
Response
```

## backend/tests/test_document_read_api.py

| 项目 | 内容 |
|---|---|
| 测试目的 | 验证文档列表、详情、过滤和不存在文档的错误返回 |
| 对应API | `GET /api/v1/documents`、`GET /api/v1/documents/{document_id}` |
| 测试命令 | `cd backend && python -m unittest tests.test_document_read_api -v` |
| 输入（入力） | `document_id`、`status`、`document_type`、`language`、`tag`、`owner` |
| 预想输出（予想結果） | 返回文档列表或详情；缺失时返回 `document_not_found` |
| Swagger对应操作 | 先查列表，再复制 `document_id` 查询详情 |
| 后台观察 | 过滤条件、命中文档、缺失日志 |
| 对应源码 | `backend/app/api/documents.py`、`backend/app/services/document_read_service.py` |
| 为什么设计 | 读接口最容易暴露仓库状态和过滤逻辑问题，必须独立验证 |

### 后端程序流程

```text
TestClient
↓
backend/app/api/documents.py
list_documents() / get_document()
↓
backend/app/services/document_read_service.py
DocumentReadService.list_documents() / get_document()
↓
backend/app/repositories/implementations/in_memory/document_repository.py
InMemoryDocumentRepository.list_all() / get()
↓
Response
```

## backend/tests/test_document_archive_api.py

| 项目 | 内容 |
|---|---|
| 测试目的 | 验证归档语义，确认不是物理删除 |
| 对应API | `DELETE /api/v1/documents/{document_id}` |
| 测试命令 | `cd backend && python -m unittest tests.test_document_archive_api -v` |
| 输入（入力） | `document_id` |
| 预想输出（予想結果） | 文档进入 archived，列表默认不显示，详情按语义仍可追踪 |
| Swagger对应操作 | 执行 DELETE → 再查列表和详情观察差异 |
| 后台观察 | archive 状态变化、列表过滤、重复归档边界 |
| 对应源码 | `backend/app/api/documents.py`、`backend/app/services/document_archive_service.py` |
| 为什么设计 | 企业系统需要可追溯删除，防止误实现成 hard delete |

### 后端程序流程

```text
TestClient
↓
backend/app/api/documents.py
archive_document()
↓
backend/app/services/document_archive_service.py
DocumentArchiveService.archive_document()
↓
backend/app/repositories/implementations/in_memory/document_repository.py
InMemoryDocumentRepository.update()
↓
Response
```

## backend/tests/test_document_import_api.py

| 项目 | 内容 |
|---|---|
| 测试目的 | 验证导入流程和状态推进 |
| 对应API | `POST /api/v1/documents/{document_id}/import` |
| 测试命令 | `cd backend && python -m unittest tests.test_document_import_api -v` |
| 输入（入力） | `document_id`、导入请求 |
| 预想输出（予想結果） | 导入成功推进状态；不支持类型或错误状态被拒绝 |
| Swagger对应操作 | 确认文档存在 → 执行 import → 观察返回和状态 |
| 后台观察 | import 状态、失败原因、类型限制、validated 语义 |
| 对应源码 | `backend/app/api/document_imports.py`、`backend/app/services/document_import_service.py` |
| 为什么设计 | Import 是 chunk 和 retrieval 的前置门槛，不稳定会让后续问题难定位 |

### 后端程序流程

```text
TestClient
↓
backend/app/api/document_imports.py
import_document()
↓
backend/app/services/document_import_service.py
DocumentImportService.import_document()
↓
backend/app/repositories/implementations/in_memory/document_repository.py
InMemoryDocumentRepository.update()
↓
Response
```

## backend/tests/test_document_chunk_api.py

| 项目 | 内容 |
|---|---|
| 测试目的 | 验证文档切分和 chunk 读取 |
| 对应API | `POST /api/v1/documents/{document_id}/chunks`、`GET /api/v1/documents/{document_id}/chunks` |
| 测试命令 | `cd backend && python -m unittest tests.test_document_chunk_api -v` |
| 输入（入力） | `document_id`、切分参数 |
| 预想输出（予想結果） | chunk 数量、顺序、元数据稳定，可重复读取 |
| Swagger对应操作 | 先执行 chunk，再读取 chunks |
| 后台观察 | `chunk_index`、chunk 数量、切分策略、replace 行为 |
| 对应源码 | `backend/app/api/document_chunks.py`、`backend/app/services/document_chunk_service.py` |
| 为什么设计 | Chunk 是 retrieval 和 RAG 的基础数据层 |

### 后端程序流程

```text
TestClient
↓
backend/app/api/document_chunks.py
chunk_document() / get_document_chunks()
↓
backend/app/services/document_chunk_service.py
DocumentChunkService.chunk_document() / get_chunks()
↓
backend/app/repositories/implementations/in_memory/document_chunk_repository.py
InMemoryDocumentChunkRepository.replace_for_document() / list_for_document()
↓
Response
```

## backend/tests/test_document_retrieval_api.py

| 项目 | 内容 |
|---|---|
| 测试目的 | 验证关键字检索、过滤、排序和 archived 排除 |
| 对应API | `POST /api/v1/document-retrieval/search` |
| 测试命令 | `cd backend && python -m unittest tests.test_document_retrieval_api -v` |
| 输入（入力） | `query`、`limit`、`include_archived`、`document_type`、`language`、`tags` |
| 预想输出（予想結果） | 返回 ranked chunks、score、source、metadata |
| Swagger对应操作 | 输入 query 和过滤条件，观察 chunks、score、source |
| 后台观察 | query、过滤条件、命中 chunk、排序、archived 过滤 |
| 对应源码 | `backend/app/api/document_retrieval.py`、`backend/app/services/document_retrieval_service.py` |
| 为什么设计 | Retrieval 是 Internal RAG 的上游，检索不可靠则答案不可信 |

### 后端程序流程

```text
TestClient
↓
backend/app/api/document_retrieval.py
search_documents()
↓
backend/app/services/document_retrieval_service.py
DocumentRetrievalService.search()
↓
backend/app/repositories/implementations/in_memory/document_retrieval.py
InMemoryKeywordRetrieval.search()
↓
Response
```

## backend/tests/test_internal_rag_api.py

| 项目 | 内容 |
|---|---|
| 测试目的 | 验证 deterministic Internal RAG 主回答能力和 citation 返回结构 |
| 对应API | `POST /api/v1/internal-rag/answer` |
| 测试命令 | `cd backend && python -m unittest tests.test_internal_rag_api -v` |
| 输入（入力） | `question`、检索参数、`answer_mode`、`require_citations` |
| 预想输出（予想結果） | `answer`、`citations`、`confidence`、`warnings` |
| Swagger对应操作 | 执行 Internal RAG 接口，观察 answer、citation、warning |
| 后台观察 | citation 完整性、confidence、warning、上下文不足错误 |
| 对应源码 | `backend/app/api/internal_rag.py`、`backend/app/services/internal_rag_service.py` |
| 为什么设计 | 保护无真实 LLM 时仍能给出可解释回答的核心能力 |

### 后端程序流程

```text
TestClient
↓
backend/app/api/internal_rag.py
answer_internal_rag()
↓
backend/app/services/internal_rag_service.py
InternalRagService.answer()
↓
backend/app/repositories/implementations/in_memory/document_retrieval.py
InMemoryKeywordRetrieval.search()
↓
backend/app/services/rag_answer_generator.py
RAGAnswerGenerator.generate()
↓
Response
```

## backend/tests/test_internal_rag_evaluation.py

| 项目 | 内容 |
|---|---|
| 测试目的 | 验证 citation 质量评估、warning taxonomy 和回答质量信号 |
| 对应API | `POST /api/v1/internal-rag/answer` |
| 测试命令 | `cd backend && python -m unittest tests.test_internal_rag_evaluation -v` |
| 输入（入力） | 不同质量上下文、不同问句、不同 citation 覆盖度 |
| 预想输出（予想結果） | 返回预期评分、warning 和 confidence，不把低质量回答伪装成高置信度 |
| Swagger对应操作 | 构造弱上下文问题，观察 `warnings` 和 `confidence` |
| 后台观察 | `coverage_score`、`citation_score`、`confidence`、`warnings` |
| 对应源码 | `backend/app/services/internal_rag_evaluation_service.py`、`backend/app/services/internal_rag_service.py` |
| 为什么设计 | 企业 RAG 不只验证能答，还要验证答案是否有根据 |

### 后端程序流程

```text
TestClient
↓
backend/app/api/internal_rag.py
answer_internal_rag()
↓
backend/app/services/internal_rag_service.py
InternalRagService.answer()
↓
backend/app/services/internal_rag_evaluation_service.py
InternalRagEvaluationService.evaluate()
↓
Response
```

## backend/tests/test_rag_answer_generator.py

| 项目 | 内容 |
|---|---|
| 测试目的 | 验证 `StubLLMProvider` 接入位置和 provider 失败时 deterministic fallback |
| 对应API | `POST /api/v1/internal-rag/answer` |
| 测试命令 | `cd backend && python -m unittest tests.test_rag_answer_generator -v` |
| 输入（入力） | provider 开关、问题请求、失败和超时场景 |
| 预想输出（予想結果） | provider 可用时走 provider，失败时回退 deterministic answer |
| Swagger对应操作 | 通常以测试为主；启用相关配置后可通过 Internal RAG 观察 fallback |
| 后台观察 | provider 名称、fallback 分支、内部日志 |
| 对应源码 | `backend/app/services/rag_answer_generator.py`、`backend/app/services/internal_rag_service.py` |
| 为什么设计 | 未来接真实模型时，当前本地路径仍要稳定 |

### 后端程序流程

```text
TestClient
↓
backend/app/services/rag_answer_generator.py
RAGAnswerGenerator.generate()
↓
backend/app/services/rag_answer_generator.py
RAGAnswerGenerator._fallback()
↓
Response
```

## backend/tests/test_approval_api.py

| 项目 | 内容 |
|---|---|
| 测试目的 | 验证审批提交、列表、详情、批准、拒绝、修订状态机 |
| 对应API | `POST /api/v1/reports/{task_id}/submit-approval`、`GET /api/v1/approvals`、`GET /api/v1/approvals/{approval_id}`、`POST /approve`、`POST /reject`、`POST /revise` |
| 测试命令 | `cd backend && python -m unittest tests.test_approval_api -v` |
| 输入（入力） | `task_id`、`approval_id`、审批动作请求 |
| 预想输出（予想結果） | 状态按规则推进，非法转换被拒绝，修订形成新版本边界 |
| Swagger对应操作 | submit → list/detail → approve/reject/revise |
| 后台观察 | 状态机、approval id、修订版本、失败错误码 |
| 对应源码 | `backend/app/api/approvals.py`、`backend/app/services/approval_service.py` |
| 为什么设计 | 审批是报告发布治理边界，不能和普通 CRUD 混在一起验证 |

### 后端程序流程

```text
TestClient
↓
backend/app/api/approvals.py
submit_approval() / list_approvals() / get_approval() / approve() / reject() / revise()
↓
backend/app/services/approval_service.py
ApprovalService.submit_approval() / list_approvals() / get_approval() / approve() / reject() / revise()
↓
backend/app/repositories/implementations/in_memory/approval_repository.py
InMemoryApprovalRepository.save_approval_request() / get_approval_request() / list_approval_requests()
↓
Response
```

## backend/tests/test_rbac_guard.py

| 项目 | 内容 |
|---|---|
| 测试目的 | 验证 approval APIs 的 RBAC allow / deny |
| 对应API | approval 相关 API |
| 测试命令 | `cd backend && python -m unittest tests.test_rbac_guard -v` |
| 输入（入力） | 不同权限主体、不同审批动作、拒绝场景 |
| 预想输出（予想結果） | 有权限通过；无权限返回 `permission_denied` 并记录拒绝事实 |
| Swagger对应操作 | 结合审批 API 理解权限边界；主要以测试桩验证 |
| 后台观察 | permission name、deny 日志、audit fact |
| 对应源码 | `backend/app/api/approvals.py`、`backend/app/services/security_service.py` |
| 为什么设计 | 防止越权问题藏在业务 happy path 里 |

### 后端程序流程

```text
TestClient
↓
backend/app/api/approvals.py
approval endpoint
↓
backend/app/services/security_service.py
SecurityService.require_permission()
↓
backend/app/services/audit_service.py
AuditService.record_audit_log()
↓
Response
```

## backend/tests/test_audit_middleware.py

| 项目 | 内容 |
|---|---|
| 测试目的 | 验证审批相关动作的审计中间件和 append-only 事实记录 |
| 对应API | approval APIs、`GET /api/v1/audit-logs` |
| 测试命令 | `cd backend && python -m unittest tests.test_audit_middleware -v` |
| 输入（入力） | 审批动作请求、失败请求、拒绝请求 |
| 预想输出（予想結果） | 成功、拒绝、失败路径都留下审计事实 |
| Swagger对应操作 | 先执行审批动作，再执行 `GET /api/v1/audit-logs` |
| 后台观察 | 审计事件名、append-only 语义、失败路径是否记录 |
| 对应源码 | `backend/app/services/audit_middleware.py`、`backend/app/services/audit_service.py`、`backend/app/api/audit_logs.py` |
| 为什么设计 | 企业系统失败也必须可追踪，不能只记录成功 |

### 后端程序流程

```text
TestClient
↓
backend/app/services/audit_middleware.py
AuditMiddleware.run()
↓
backend/app/services/audit_service.py
AuditService.record_audit_log()
↓
backend/app/repositories/implementations/in_memory/audit_repository.py
InMemoryAuditRepository.append()
↓
Response
```

## backend/tests/test_security_audit_api.py

| 项目 | 内容 |
|---|---|
| 测试目的 | 验证 current user、roles、permissions、audit logs 读取能力 |
| 对应API | `GET /api/v1/users/me`、`GET /api/v1/security/roles`、`GET /api/v1/security/permissions`、`GET /api/v1/audit-logs` |
| 测试命令 | `cd backend && python -m unittest tests.test_security_audit_api -v` |
| 输入（入力） | 无或少量分页参数 |
| 预想输出（予想結果） | 返回 `system` 占位主体、冻结角色目录、冻结权限目录、审计日志列表 |
| Swagger对应操作 | 依次执行四个 GET 接口 |
| 后台观察 | `user_id`、role catalog、permission catalog、audit list |
| 对应源码 | `backend/app/api/security.py`、`backend/app/api/audit_logs.py`、`backend/app/services/security_service.py`、`backend/app/services/audit_service.py` |
| 为什么设计 | 安全读模型是未来真实认证和完整审计接入的最小基线 |

### 后端程序流程

```text
TestClient
↓
backend/app/api/security.py
get_current_user() / get_roles() / get_permissions()
↓
backend/app/services/security_service.py
SecurityService.get_current_user() / list_roles() / list_permissions()
↓
backend/app/api/audit_logs.py
get_audit_logs()
↓
backend/app/services/audit_service.py
AuditService.list_audit_logs()
↓
Response
```

## backend/tests/test_file_inputs.py

| 项目 | 内容 |
|---|---|
| 测试目的 | 验证本地静态输入文件读取和解析边界 |
| 对应API | 无公开 API |
| 测试命令 | `cd backend && python -m unittest tests.test_file_inputs -v` |
| 输入（入力） | CSV、JSON、Markdown 等本地样本文件 |
| 预想输出（予想結果） | 文件能稳定读取，解析结果符合预期 |
| Swagger对应操作 | 无直接 Swagger 操作，可通过文档上传和任务链路间接理解 |
| 后台观察 | 文件路径、解析结果、异常输入处理 |
| 对应源码 | 本地数据加载相关模块和 `backend/data/` 样本文件 |
| 为什么设计 | 当前阶段很多能力依赖本地静态数据，底层输入不稳会影响学习路径 |

### 后端程序流程

```text
TestClient / unittest
↓
backend/data/
local sample files
↓
file reader / parser
↓
Assertion
```

## backend/tests/test_document_domain.py

| 项目 | 内容 |
|---|---|
| 测试目的 | 验证文档领域模型、状态迁移和仓库语义 |
| 对应API | documents 系列 API 间接对应 |
| 测试命令 | `cd backend && python -m unittest tests.test_document_domain -v` |
| 输入（入力） | 文档对象、metadata、状态变化请求、重复内容 |
| 预想输出（予想結果） | 状态迁移、去重规则和领域约束符合预期 |
| Swagger对应操作 | 可通过上传、读取、归档接口间接观察 |
| 后台观察 | 状态机、checksum、archive 规则 |
| 对应源码 | `backend/app/models/document.py`、`backend/app/repositories/implementations/in_memory/document_repository.py` |
| 为什么设计 | 领域规则错了，所有上层 API 都会跟着错 |

### 后端程序流程

```text
unittest
↓
backend/app/models/document.py
Document / DocumentStatus
↓
backend/app/repositories/implementations/in_memory/document_repository.py
InMemoryDocumentRepository.create() / update() / find_by_checksum()
↓
Assertion
```

## backend/tests/test_repositories.py

| 项目 | 内容 |
|---|---|
| 测试目的 | 验证 Repository 抽象边界 |
| 对应API | 无公开 API |
| 测试命令 | `cd backend && python -m unittest tests.test_repositories -v` |
| 输入（入力） | Repository interface 和实现对象 |
| 预想输出（予想結果） | 仓库协议满足最小能力要求 |
| Swagger对应操作 | 无直接 Swagger 操作 |
| 后台观察 | 接口命名、能力边界、实现一致性 |
| 对应源码 | `backend/app/repositories/interfaces/` |
| 为什么设计 | Repository 抽象是未来切换 PostgreSQL 的前提 |

### 后端程序流程

```text
unittest
↓
backend/app/repositories/interfaces/
Repository Protocol
↓
backend/app/repositories/implementations/in_memory/
Repository Implementation
↓
Assertion
```

## backend/tests/test_settings.py

| 项目 | 内容 |
|---|---|
| 测试目的 | 验证环境变量和应用配置解析 |
| 对应API | 全部 API 间接受影响 |
| 测试命令 | `cd backend && python -m unittest tests.test_settings -v` |
| 输入（入力） | 环境变量、默认配置、覆盖场景 |
| 预想输出（予想結果） | 配置正确解析，默认值稳定，不合法配置可识别 |
| Swagger对应操作 | 可通过 `/health` 间接确认应用是否启动 |
| 后台观察 | 默认值、环境变量覆盖、启动前失败 |
| 对应源码 | `backend/app/config/settings.py` |
| 为什么设计 | 配置错误会让所有能力表现为启动或运行异常 |

### 后端程序流程

```text
unittest
↓
backend/app/config/settings.py
Settings
↓
backend/app/config/container.py
build_container()
↓
Assertion
```

## backend/tests/test_repository_backend_switch.py

| 项目 | 内容 |
|---|---|
| 测试目的 | 验证 InMemory 与 PostgreSQL 仓库切换边界 |
| 对应API | 全部依赖 Repository 的 API 间接受影响 |
| 测试命令 | `cd backend && python -m unittest tests.test_repository_backend_switch -v` |
| 输入（入力） | 后端配置开关、环境变量、依赖注入条件 |
| 预想输出（予想結果） | 默认走 InMemory；满足条件时才切 PostgreSQL |
| Swagger对应操作 | 通常不直接用 Swagger 复现，可结合 `/health` 和主链路理解 |
| 后台观察 | backend 选择、环境变量、依赖注入 |
| 对应源码 | `backend/app/config/container.py`、`backend/app/config/settings.py` |
| 为什么设计 | 防止未来引入 PostgreSQL 后破坏默认学习路径 |

### 后端程序流程

```text
unittest
↓
backend/app/config/settings.py
Settings
↓
backend/app/config/container.py
build_container()
↓
backend/app/repositories/implementations/in_memory/
or backend/app/repositories/postgres/
↓
Assertion
```

## backend/tests/test_postgres_repositories.py

| 项目 | 内容 |
|---|---|
| 测试目的 | 验证 PostgreSQL 仓库实现合同（V1.0 正式验收路径之一；InMemory 仍为默认学习路径） |
| 对应API | documents、tasks、approval 等依赖仓库能力间接受影响 |
| 测试命令 | `cd backend && python -m unittest tests.test_postgres_repositories -v` |
| 输入（入力） | PostgreSQL 连接配置、数据库环境、`psycopg` 依赖 |
| 预想输出（予想結果） | 环境满足时通过；缺依赖时明确跳过 |
| Swagger对应操作 | 不建议直接用 Swagger 验证，先确认底层 roundtrip |
| 后台观察 | 连接、写入、读取、skip 原因 |
| 对应源码 | `backend/app/repositories/postgres/` |
| 为什么设计 | 证明 PostgreSQL 与 InMemory 合同一致；V1.0 交付以 PG 全量 + InMemory 回归双轨验收，默认本地学习仍可不启 PG |

### 后端程序流程

```text
unittest
↓
backend/app/repositories/postgres/
PostgresTaskRepository / PostgresReportRepository / PostgresEventRepository
↓
PostgreSQL roundtrip
↓
Assertion
```

## backend/tests/test_logging.py

| 项目 | 内容 |
|---|---|
| 测试目的 | 验证结构化日志和 request_id 等观测字段 |
| 对应API | 全部 API 间接受影响 |
| 测试命令 | `cd backend && python -m unittest tests.test_logging -v` |
| 输入（入力） | 日志事件、request_id、结构化字段 |
| 预想输出（予想結果） | 日志字段稳定输出，不泄露敏感信息 |
| Swagger对应操作 | 执行任意主链路 API，观察后端日志 |
| 后台观察 | `timestamp`、`level`、`service`、`request_id`、`task_id`、`event`、`status`、`error_code`、`duration_ms` |
| 对应源码 | `backend/app/observability/logging.py` |
| 为什么设计 | 企业项目必须能排查问题，日志字段不能漂移 |

### 后端程序流程

```text
unittest
↓
backend/app/observability/logging.py
log_event()
↓
structured log output
↓
Assertion
```

## backend/tests/test_authentication.py（V1.0 增量）

| 项目 | 内容 |
|---|---|
| 测试目的 | 验证 JWT 生成/解析、唯一 jti、过期与伪造失败、以及 **时钟回拨 leeway** |
| 对应API | `POST /api/v1/auth/login`、`GET /api/v1/users/me`、受保护 API 的 Bearer 依赖 |
| 测试命令 | `cd backend && python -m unittest tests.test_authentication -v` |
| 输入（入力） | 合法用户密码、伪造签名 Token、过期 Token、iat 略超前的 Token |
| 预想输出（予想結果） | 合法 Token 通过；伪造/过期 401；iat 超前 2s 在默认 leeway 内可通过；leeway=0 时 immature 仍 401 |
| Swagger对应操作 | Authorize → login → 带 Bearer 调 `/api/v1/users/me` |
| 后台观察 | 不打印完整 Token；错误 reason 可为 `invalid_token` / `token_expired` |
| 对应源码 | `backend/app/security/jwt_service.py`、`jwt_provider.py`、`config.py`、`dependencies.py` |
| 为什么设计 | V1.0 曾出现 PG 全量 suite 随机 401：主机时钟回拨使 iat 落在未来；必须用回归锁住 leeway 行为且不放宽签名校验 |
| 保护的 Bug / 风险 | 随机 401、jti 重复假设、过期被误判为成功、伪造签名被接受 |

### 后端程序流程

```text
unittest / HTTPBearer
↓
backend/app/security/dependencies.py
get_current_user()
↓
backend/app/security/jwt_service.py
JWTService.parse_token() / get_current_user()
↓
backend/app/security/jwt_provider.py
PyJWTProvider.decode(leeway=JWTConfig.leeway_seconds)
↓
TokenPayload / CurrentUser
↓
Assertion
```

## backend/tests/test_ai_analysis_api.py（V1.0 增量）

| 项目 | 内容 |
|---|---|
| 测试目的 | 验证显式 AI 分析入口、low_cost 路由、幂等、Evidence Gate、缺 Bearer/缺幂等键 |
| 对应API | `POST /api/v1/ai-analysis` |
| 测试命令 | `cd backend && REPOSITORY_BACKEND=postgres DATABASE_URL=... python -m unittest tests.test_ai_analysis_api -v`（PostgreSQL-only 集成） |
| 输入（入力） | 已 chunk 证据、`confirmed=true`、Idempotency-Key |
| 预想输出（予想結果） | `provider` 以 stub-low-cost 开头；`route_tier=low_cost`；usage/cost 可解析；重复 key 不双计费 |
| Swagger对应操作 | 先完成文档 Upload→Import→Chunk→Retrieval，再调 ai-analysis（需 Bearer） |
| 后台观察 | `llm_usage_ledger` 成功行、audit `analysis.execute.*` |
| 对应源码 | `backend/app/api/` AI 分析路由、`services` 中分析服务、LLM Gateway |
| 为什么设计 | 成本治理要求「唯一显式入口 + 证据门禁 + 幂等」 |

### 后端程序流程

```text
TestClient + Bearer
↓
POST /api/v1/ai-analysis
↓
Evidence Gate + Idempotency
↓
LLMGatewayService（low_cost / stub）
↓
llm_usage_ledger 结算 + audit
↓
Assertion
```

## backend/tests/test_executive_report_api.py（V1.0 增量）

| 项目 | 内容 |
|---|---|
| 测试目的 | 验证 high_quality 董事会报告、与 low_cost 额度分离、不自动 submit approval |
| 对应API | `POST /api/v1/executive-reports`、`POST /api/v1/reports/{task_id}/submit-approval` |
| 测试命令 | `cd backend && REPOSITORY_BACKEND=postgres ... python -m unittest tests.test_executive_report_api -v` |
| 输入（入力） | 已成功的 `ai_analysis_id`、`confirmed=true`、Idempotency-Key |
| 预想输出（予想結果） | `route_tier=high_quality`；`provider` 以 stub-high-quality 开头；报告 GENERATED；需显式 submit 才进审批 |
| Swagger对应操作 | ai-analysis 成功 → executive-reports → submit-approval → manager approve |
| 后台观察 | ledger 中 `operation=executive_report`、report_version_id |
| 对应源码 | Executive report API/Service、Approval 入口 |
| 为什么设计 | 高成本路由与审批门禁必须可测、可回归 |

### 后端程序流程

```text
已成功 analysis_id
↓
POST /api/v1/executive-reports
↓
LLMGatewayService（high_quality / stub）
↓
Report + ReportVersion
↓
（可选）submit-approval → Approval 状态机
↓
Assertion
```

## backend/tests/test_e2e_api_stub_flow.py（V1.0 增量）

| 项目 | 内容 |
|---|---|
| 测试目的 | 一条 Stub 企业链：登录 → 文档 → 检索 → 分析 → 报告 → 审批 → 审计 |
| 对应API | auth / documents / retrieval / ai-analysis / executive-reports / approvals / audit-logs |
| 测试命令 | 进程内：`REPOSITORY_BACKEND=postgres` 下 `python -m unittest tests.test_e2e_api_stub_flow -v`；对 Compose：`./scripts/run_api_e2e.sh`（`E2E_BASE_URL=http://127.0.0.1:8000`） |
| 输入（入力） | 测试用户 admin/manager/employee；受控销售证据 Markdown |
| 预想输出（予想結果） | employee 不可 approve（403）；manager 可 approve；ledger 仅 stub；普通 retrieval 不强制真实 Provider |
| Swagger对应操作 | 可按同一顺序手工点一遍，但自动化以脚本为准 |
| 后台观察 | 禁止打印 Token/Key；health 响应无 secret 字段 |
| 对应源码 | 多 API + 多 Service；脚本 `scripts/run_api_e2e.sh` |
| 为什么设计 | Compose 交付必须有一条「零费用」业务验收链 |

### 后端程序流程

```text
（可选）Compose Backend :8000
↓
HTTP 登录三角色
↓
Upload → Import → Chunk → Retrieval
↓
AI Analysis（stub-low-cost）
↓
Executive Report（stub-high-quality）
↓
submit-approval → employee 403 → manager 200
↓
audit-logs / usage ledger 断言
↓
OK
```

## backend/tests/test_provider_fallback_chain.py（V1.0 增量）

| 项目 | 内容 |
|---|---|
| 测试目的 | 固定 Provider 顺序、失败切换、熔断、配额停止、low/high 模型不交叉 |
| 对应API | 间接触发（Gateway）；默认 suite 用 MockTransport，不访问公网 |
| 测试命令 | `cd backend && python -m unittest tests.test_provider_fallback_chain -v` |
| 输入（入力） | 可控 Mock 失败/429/超时、电路状态 |
| 预想输出（予想結果） | OpenRouter→NVIDIA→Gemini→Local Qwen 顺序；成功即停；open 状态跳过不收费 |
| Swagger对应操作 | 默认不在 Swagger 演示真实 fallback；学习时看单测更安全 |
| 后台观察 | attempt ledger / circuit state（PostgreSQL 共享状态场景） |
| 对应源码 | Provider chain、gateway、migration `20260717_07_fallback_chain` |
| 为什么设计 | 韧性链必须可测且默认零费用 |

### 后端程序流程

```text
unittest MockTransport
↓
ProviderChain.execute()
↓
attempt 记录 / circuit
↓
选中 provider+model 回填
↓
Assertion（无真实外呼）
```

# V1.0 业务数据验证与验收

本章是 **业务数据 / 人工验收** 补充，不删除上文任何测试文件章节。

## 业务主链（最终交付口径）

```text
文書管理
→ RAG検索
→ 分析依頼
→ 承認管理
→ 最终审计报告
```

对应前端页面（登录后）：

| 步骤 | 页面 | 自动化对照 |
|---|---|---|
| 文書管理 | `/documents` | document upload/import/chunk 测试 + E2E |
| RAG検索 | `/rag` | retrieval / internal-rag / frontend RagPage 测试 |
| 分析依頼 | `/analysis`（正式导航「分析依頼」；RAG 页另有 AI 分析入口） | `test_ai_analysis_api` + `test_api` 任务主链路 |
| 承認管理 | `/approval` | approval / rbac / E2E manager approve |
| 审计报告 | Approval 详情 + Audit / 报告版本 | audit 测试 + executive report |

## 推荐样例数据

目录：

```text
docs/learning/sample-data/Scenario01_Sales_Decline/
```

| 文件 | 用途 |
|---|---|
| `01_関東地域飲料売上分析.md` ～ `06_KPI月次報告.md` | 上传/Import/Chunk 用业务正文 |
| `07_RAG質問集.md` | RAG 查询输入 |
| `08_分析依頼入力例.md` | Analysis / AI 分析问题示例 |
| `09_承認コメント例.md` | 审批意见示例 |
| `10_業務テストシナリオ.md` | 逐步人工验收剧本 |

人工验收时请同时遵守：

- 默认 `LLM_PROVIDER_MODE=stub`（零真实费用）
- 不在日志/截图中暴露 Token、密码、API Key
- Compose 验收不要 `docker compose down -v`

## 自动化验收命令清单（两列）

| 真实模型 / 真实服务 | 纯本地 / Stub / 本地 Provider |
|---|---|
| 不适用（默认验收不调用真实 LLM） | `cd backend && python3 -m unittest discover -s tests -v`（InMemory 默认） |
| 仅当显式 `RUN_REAL_LLM_SMOKE=1` 且配置真实 Key 时 | `REPOSITORY_BACKEND=postgres DATABASE_URL=... python3 -m unittest discover -s tests -v` |
| 真实 OpenRouter smoke（默认 skip） | `./scripts/run_tests.sh`（Backend + Frontend + build + compileall） |
| — | `cd frontend && npm test` 与 `npm run build` |
| — | `./scripts/compose_up.sh` → `./scripts/compose_verify.sh` → `./scripts/run_api_e2e.sh` → `./scripts/compose_down.sh` |

## 通过标准（V1.0）

Backend：

- PostgreSQL：**281** tests，**2** skipped；建议完整 suite 连续多次无随机失败
- InMemory：**270** tests，**52** skipped
- Alembic head：`20260717_07_fallback_chain`
- compileall / `git diff --check`：通过

Frontend：

- **113 / 113** tests
- production build 通过

Docker（daemon 可用时）：

- compose build/up/health/verify/e2e/down（无 `-v`）通过
- 默认 stub，零真实 LLM 费用

业务：

- 人工可按 Scenario01 走通「文書→RAG→分析→承認→审计报告」
- Stub E2E 覆盖三角色与审批 403/成功路径

## 与启动手册的交叉引用

- 启动与排错：`docs/learning/01_Foundation/RUNBOOK_LOCAL.md`
- 启动完成检查清单：项目根目录 `VERIFY_CHECKLIST.md`
- Compose 步骤：RUNBOOK Appendix M
- 数字基线：RUNBOOK Appendix N
