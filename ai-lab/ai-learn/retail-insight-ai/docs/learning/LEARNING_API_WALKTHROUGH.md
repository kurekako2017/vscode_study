# 接口学习走读

这份文档用于按 `总览 -> 详细` 的顺序学习 API。总览表负责快速定位，接口章节负责保留 Swagger 操作、输入、输出、后台 Log、源码位置、对应测试、下一步和程序调用流程。

## 先认识三个入口

| 工具         | 作用                                                               | 当前学习阶段怎么用                     |
| ------------ | ------------------------------------------------------------------ | -------------------------------------- |
| Swagger      | FastAPI 自动生成的 API 调试与验证工具，不是测试环境，也不是正式 UI | 手工执行接口，观察请求、响应和业务流程 |
| ReDoc        | 偏阅读体验的 API 文档                                              | 慢慢阅读字段、Schema 和响应模型        |
| OpenAPI JSON | 机器可读接口定义                                                   | 检查路径、Schema、字段是否真实注册     |

## 企业项目验证体系

| 层级                               | 工具                   | 目的                              |
| ---------------------------------- | ---------------------- | --------------------------------- |
| 单元测试（Unit Test）              | `python -m unittest` | 验证单个模块或类的逻辑是否正确    |
| 接口验证（API Verification）       | Swagger UI`/docs`    | 手工验证 API 请求、响应和业务流程 |
| 前后端集成测试（Integration Test） | React + FastAPI        | 验证完整用户操作流程              |
| 端到端测试（E2E Test）             | Playwright / Cypress   | 模拟真实用户完成整个业务流程      |

补充说明：Swagger 不是测试环境，Swagger 不是正式 UI，Swagger 是 API 调试与验证工具。UI 完成以后 Swagger 通常仍然保留，因为 React 和 Swagger 调用的是同一套 FastAPI API。当前阶段主要用 Swagger 验证后端骨架；UI 完成后再做前后端 Integration Test；发布前再考虑 E2E Test。

## 后台日志怎么观察

后台日志就是启动 FastAPI 的那个终端输出。

如果你是手动启动后端，通常会看到类似这样的命令：

```bash
cd backend
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

如果你是通过项目脚本启动，那么就观察那个显示 `uvicorn`、`FastAPI`、`SSE`、`request_id` 的 Terminal。也就是说，Backend Terminal Log 不是单独的新工具，而是后端进程正在运行时的控制台输出。

做 Swagger `Execute` 之后，不要只看一个地方，要同时看这三块：

1. `Swagger Response Body`
2. `Swagger Response Headers`
3. `Backend Terminal Log`

这三块是同一次请求的三个视角。

| 观察项               | 含义                                                  | 为什么要看               |
| -------------------- | ----------------------------------------------------- | ------------------------ |
| `request_id`       | 一次请求的追踪 ID                                     | 用来串联同一次请求的日志 |
| `HTTP method/path` | `GET` / `POST` 和 URL                             | 判断请求是否进入后端     |
| `status code`      | `200` / `201` / `400` / `404` / `500`       | 判断接口成功还是失败     |
| `event`            | 业务事件名称                                          | 判断程序执行到哪个阶段   |
| `task_id`          | 任务 ID                                               | 跟踪任务链路             |
| `document_id`      | 文档 ID                                               | 跟踪文档链路             |
| `status`           | `queued` / `running` / `completed` / `failed` | 判断业务状态变化         |
| `error_code`       | 错误码                                                | 定位失败原因             |
| `duration_ms`      | 耗时                                                  | 判断性能问题             |

学习时建议按这个顺序串起来看：

```text
阅读接口文档
↓
打开 Swagger
↓
Execute
↓
看 Response Body
↓
看 Response Headers
↓
看 Backend Terminal Log
↓
用 request_id / task_id / document_id 关联日志
↓
再去看源码 Router -> Service -> Repository
```

这里要特别记住两句话：

- Swagger 只告诉我们接口响应结果。
- Backend Log 能告诉我们请求是否真正进入后端，以及执行到了哪个业务阶段。

## Learning Trace（学习调用链日志）

Learning Trace 是一组可关闭的教学日志，用来把请求阶段、后台阶段和任务生命周期串成同一条学习链路。

什么时候开启：

- 只在你想学习“请求是怎么走到源码里”的时候开启。
- 正常使用、普通调试、日常运行都保持默认关闭。
- 默认配置是 `LEARNING_TRACE=false`，关闭时完全没有影响。

为什么存在：

- Swagger 只能告诉我们接口响应结果。
- Learning Trace 用来补上“请求在后端内部到底是怎么被业务步骤处理的”。
- 它特别适合初学者对照阅读 `Router -> Service -> Repository -> Workflow -> Report`，再理解任务为什么要先返回 `202`，后面又继续异步推进。

如何阅读：

```text
打开 Swagger
↓
Execute
↓
看 Response Body
↓
看 Response Headers
↓
看 Backend Terminal Log
↓
用 request_id / task_id / document_id 关联日志
↓
再看源码 Router -> Service -> Repository
```

和 Swagger 配合的方法：

- 先在 Swagger 里执行一次接口。
- 再回到后端终端看 Learning Trace。
- 用 `request_id` 串联同一次请求。
- `task_id` 适合任务链路，`document_id` 适合文档链路。
- 这套方法目前先覆盖 `GET /health`、`POST /api/tasks`、`GET /api/tasks/{task_id}`、`GET /api/tasks/{task_id}/events`。

开启步骤：

1. 打开项目根目录 `.env`
2. 增加或修改：

```env
LEARNING_TRACE=true
```

3. 重启后端：

```bash
cd backend
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

4. 打开 Swagger 执行 `GET /health`
5. 在后端 Terminal 中查找 `learning_trace` 或 `Router -> health() -> Response`

关闭步骤：

- 在项目根目录 `.env` 中把 `LEARNING_TRACE=false`
- 然后重启后端

排查说明：

- 如果只看到 `event=health_check`，而没有看到 `learning_trace`，通常表示：
  - `.env` 没有设置 `LEARNING_TRACE=true`
  - 或者后端没有重启
  - 或者当前启动命令没有读取项目根目录 `.env`

### Learning Trace Phase 2

> 这是旧版学习链路说明，当前实际输出以下面的 Phase 4 为准。

Phase 2 目标是把学习日志升级成更像企业项目的调用链视图。

默认仍然关闭：

```env
LEARNING_TRACE=false
```

开启后，在终端里可以看到类似这样的学习链路：

```text
HTTP Request
↓
Router
↓
Service
↓
Workflow
↓
Provider
↓
Repository
↓
Schema(Response Model)
↓
HTTP Response
```

这套日志用于学习程序调用流程，不会改变 Swagger、OpenAPI、API Response、SSE 或任何业务逻辑。

对 `POST /api/tasks` 来说，这条学习链路会在后台任务完成后统一打印完整 block，方便你按源码顺序把 main.py、API 路由、Service、Workflow、Provider、Repository 和 Response 串起来看。

每个节点的含义：

| 节点                       | 含义                                                  |
| -------------------------- | ----------------------------------------------------- |
| `HTTP Request`           | 一次 HTTP 请求进入后端                                |
| `Router`                 | FastAPI 路由函数，负责接收请求和调用 Service          |
| `Service`                | 业务编排层，负责调用 Workflow、Repository 或 Provider |
| `Workflow`               | 流程编排层，负责控制任务步骤顺序                      |
| `Provider`               | 数据或研究来源提供层                                  |
| `Repository`             | 数据读写层，负责保存或读取业务状态                    |
| `Schema(Response Model)` | 响应模型转换层，把领域对象转成 API JSON               |
| `HTTP Response`          | 响应离开后端，返回给 Swagger 或前端                   |

对于 `GET /health`，你会看到：

```text
backend/app/main.py
create_app()
（路由已注册）
↓
backend/app/api/health.py
router = APIRouter()
↓
@router.get("/health")
↓
health()
↓
backend/app/schemas/health.py
HealthResponse
↓
JSON
↓
HTTP Response
```

对于 `POST /api/tasks`，你会看到：

```text
backend/app/main.py
create_app()
（路由已注册）
↓
backend/app/api/tasks.py
router = APIRouter(prefix="/api/tasks")
↓
@router.post("")
↓
create_task()
↓
TaskService.create_task()
↓
Workflow
↓
Provider
↓
Repository
↓
Schema(Response Model)
↓
HTTP Response
```

如果只想关闭 Phase 2，仍然只需要把 `.env` 中的值改回：

```env
LEARNING_TRACE=false
```

然后重启后端即可。

### Learning Trace Phase 4

Phase 4 把学习 trace 升级成“业务调用链块”。它不是为了强调 HTTP，而是为了让初学者一眼看到请求阶段和后台阶段分别做了什么。

现在每个 block 都会显示：

- `request_id`
- `task_id`
- `Request Body`
- 请求阶段
- 后台阶段

`POST /api/tasks` 的输出示例：

```text
POST /api/tasks
request_id : ...
task_id    : ...
============================================================
Request Body
------------------------------------------------------------
question : 你好
mode     : hybrid
------------------------------------------------------------

============= Request =============
backend/app/main.py
create_app()
（路由已注册）
    ↓
backend/app/api/tasks.py
router = APIRouter(prefix="/api/tasks")
    ↓
@router.post("")
    ↓
create_task()
    ↓
backend/app/services/task_service.py
TaskService.create_task()
    ↓
backend/app/repositories/implementations/in_memory/task_repository.py
TaskRepository.create()
    ↓
backend/app/events/publisher.py
EventPublisher.publish(queued)
    ↓
BackgroundTasks.add_task()

HTTP 202 返回

============= Background =============
backend/app/services/task_service.py
TaskService.run_task()
    ↓
backend/app/repositories/implementations/in_memory/task_repository.py
TaskRepository.save(running)
    ↓
backend/app/events/publisher.py
EventPublisher.publish(running)
    ↓
backend/app/workflow/graph.py
AnalysisWorkflow.stream()
    ↓
Route
    ↓
KPI
    ↓
Research
    ↓
Report
    ↓
TaskRepository.save(completed)
    ↓
EventPublisher.publish(completed)
```

`GET /health` 也会走同一套 Source Chain 风格，只是链路更短，重点是先读 `main.py`、再读 `health.py`，最后读 `HealthResponse`。

# 后台日志观察（Backend Log Observation Guide）

企业开发调试接口时，后台日志不是只看有没有报错，而是按照固定顺序观察。

建议学习流程：

```text
Swagger Execute
↓
查看 request_id
↓
查看 Learning Trace
↓
查看业务事件（event）
↓
查看业务状态（status）
↓
查看 Response
↓
结束
```

统一观察时，重点不是“某一行日志长什么样”，而是“同一次请求在后端内部有没有按顺序走完整条业务链路”。

| 后台日志观察项                               | 为什么看                       | 正常意味着什么                           |
| -------------------------------------------- | ------------------------------ | ---------------------------------------- |
| `request_id`          | 关联一次完整请求             | 同一次请求所有日志拥有相同 `request_id` |
| `task_id`             | 关联任务生命周期             | 同一条任务链路都能串起来                |
| `Request Body`        | 观察用户输入                 | 先确认 `question`、`mode` 进入系统      |
| `Router`              | 是否进入路由层               | 请求已进入 API 入口                     |
| `Service`             | 是否进入业务层               | 开始执行业务编排                        |
| `Repository`          | 是否写入或读取状态           | 任务状态开始落库                        |
| `Workflow`            | 是否进入工作流               | 后台分析已经开始                        |
| `Provider`            | 是否调用研究来源             | 数据来源开始执行                        |
| `Report`              | 是否生成最终产物             | 报告已经合成                            |
| `event`               | 业务事件名称                 | 事件发布顺序正确                        |
| `status`              | 业务状态                     | `queued` / `running` / `completed`      |
| `duration_ms`         | 性能分析                     | 接口耗时可观察                          |
| `error_code`          | 是否异常                     | `null` 表示正常                         |

## 学习建议

第一次学习一个接口：

① Execute

② 看后台 Learning Trace

③ 先看 Request Body，再看 Router / Service / Repository

④ 看后台异步阶段的 Workflow / KPI / Research / Report

⑤ 看 event 和 status

⑥ 看 Response

⑩ 返回源码继续阅读

> 企业项目中，不建议只关注 Response。
>
> 更重要的是理解：
>
> HTTP Request
> ↓
> Router
> ↓
> Service
> ↓
> Workflow
> ↓
> Provider
> ↓
> Repository
> ↓
> Response Model
> ↓
> HTTP Response
>
> Learning Trace 正是为了帮助理解这一完整调用过程。

# 主链路接口总览

| 序号 | API                                                | 功能          | Swagger 操作                      | 输入                   | 返回                           | 对应测试                           | Service                                       | 下一步学习                                         |
| ---- | -------------------------------------------------- | ------------- | --------------------------------- | ---------------------- | ------------------------------ | ---------------------------------- | --------------------------------------------- | -------------------------------------------------- |
| 01   | `GET /health`                                    | 健康检查      | Execute                           | 无                     | `status=ok`                  | `test_api.py`                    | Health Handler                                | `POST /api/tasks`                                |
| 02   | `POST /api/tasks`                                | 创建分析任务  | 填 body 后 Execute                | `question`、`mode` | `task_id`、`status=queued` | `test_api.py`                    | `TaskService.create_task()`                 | `GET /api/tasks/{task_id}`                       |
| 03   | `GET /api/tasks/{task_id}`                       | 查询任务状态  | 填`task_id` 后 Execute          | `task_id`            | 任务状态                       | `test_api.py`                    | `TaskService.get_task()`                    | `GET /api/tasks/{task_id}/events`                |
| 04   | `GET /api/tasks/{task_id}/events`                | 订阅 SSE 事件 | 填`task_id` 后 Execute          | `task_id`            | `status/done/error` event    | `test_api.py`                    | `InMemoryEventRepository.list_after()`      | `GET /api/tasks/{task_id}/report`                |
| 05   | `GET /api/tasks/{task_id}/report`                | 读取报告      | 填`task_id` 后 Execute          | `task_id`            | Markdown 报告                  | `test_api.py`                    | `TaskService.get_report()`                  | `POST /api/v1/documents`                         |
| 06   | `POST /api/v1/documents`                         | 上传文档      | 选择 file、填 metadata 后 Execute | `file`、`metadata` | `document_id`                | `test_document_upload_api.py`    | `DocumentUploadService.upload_document()`   | `GET /api/v1/documents`                          |
| 07   | `GET /api/v1/documents`                          | 文档列表      | 可填过滤条件后 Execute            | 过滤参数               | 文档列表                       | `test_document_read_api.py`      | `DocumentReadService.list_documents()`      | `GET /api/v1/documents/{document_id}`            |
| 08   | `GET /api/v1/documents/{document_id}`            | 文档详情      | 填`document_id` 后 Execute      | `document_id`        | 文档详情                       | `test_document_read_api.py`      | `DocumentReadService.get_document()`        | `DELETE /api/v1/documents/{document_id}`         |
| 09   | `DELETE /api/v1/documents/{document_id}`         | 归档文档      | 填`document_id` 后 Execute      | `document_id`        | archived 文档                  | `test_document_archive_api.py`   | `DocumentArchiveService.archive_document()` | `POST /api/v1/documents/{document_id}/import`    |
| 10   | `POST /api/v1/documents/{document_id}/import`    | 导入文档      | 填`document_id` 后 Execute      | `document_id`        | import 结果                    | `test_document_import_api.py`    | `DocumentImportService.import_document()`   | `POST /api/v1/documents/{document_id}/chunks`    |
| 11   | `POST /api/v1/documents/{document_id}/chunks`    | 创建 chunk    | 填`document_id` 后 Execute      | `document_id`        | chunk 列表                     | `test_document_chunk_api.py`     | `DocumentChunkService.chunk_document()`     | `GET /api/v1/documents/{document_id}/chunks`     |
| 12   | `GET /api/v1/documents/{document_id}/chunks`     | 读取 chunk    | 填`document_id` 后 Execute      | `document_id`        | chunk 列表                     | `test_document_chunk_api.py`     | `DocumentChunkService.get_chunks()`         | `POST /api/v1/document-retrieval/search`         |
| 13   | `POST /api/v1/document-retrieval/search`         | 检索文档片段  | 填 query 后 Execute               | `query`、过滤条件    | ranked chunks                  | `test_document_retrieval_api.py` | `DocumentRetrievalService.search()`         | `POST /api/v1/internal-rag/answer`               |
| 14   | `POST /api/v1/internal-rag/answer`               | 内部 RAG 回答 | 填 question 后 Execute            | `question`、检索参数 | answer、citations              | `test_internal_rag_api.py`       | `InternalRagService.answer()`               | `POST /api/v1/reports/{task_id}/submit-approval` |
| 15   | `POST /api/v1/reports/{task_id}/submit-approval` | 提交审批      | 填`task_id` 后 Execute          | `task_id`            | approval request               | `test_approval_api.py`           | `ApprovalService.submit_approval()`         | `GET /api/v1/approvals`                          |
| 16   | `GET /api/v1/approvals`                          | 审批列表      | Execute                           | 可选过滤               | approval list                  | `test_approval_api.py`           | `ApprovalService.list_approvals()`          | `GET /api/v1/approvals/{approval_id}`            |
| 17   | `GET /api/v1/approvals/{approval_id}`            | 审批详情      | 填`approval_id` 后 Execute      | `approval_id`        | approval detail                | `test_approval_api.py`           | `ApprovalService.get_approval()`            | `POST /api/v1/approvals/{approval_id}/approve`   |
| 18   | `POST /api/v1/approvals/{approval_id}/approve`   | 批准审批      | 填`approval_id` 后 Execute      | `approval_id`        | `approved`                   | `test_approval_api.py`           | `ApprovalService.approve()`                 | `POST /api/v1/approvals/{approval_id}/reject`    |
| 19   | `POST /api/v1/approvals/{approval_id}/reject`    | 拒绝审批      | 填`approval_id` 后 Execute      | `approval_id`        | `rejected`                   | `test_approval_api.py`           | `ApprovalService.reject()`                  | `GET /api/v1/users/me`                           |
| 20   | `GET /api/v1/users/me`                           | 当前用户      | Execute                           | 无                     | `user_id=system`             | `test_security_audit_api.py`     | `SecurityService.get_current_user()`        | `GET /api/v1/security/roles`                     |
| 21   | `GET /api/v1/security/roles`                     | 角色目录      | Execute                           | 无                     | roles                          | `test_security_audit_api.py`     | `SecurityService.list_roles()`              | `GET /api/v1/security/permissions`               |
| 22   | `GET /api/v1/security/permissions`               | 权限目录      | Execute                           | 无                     | permissions                    | `test_security_audit_api.py`     | `SecurityService.list_permissions()`        | `GET /api/v1/audit-logs`                         |
| 23   | `GET /api/v1/audit-logs`                         | 审计日志      | Execute                           | 无                     | audit logs                     | `test_security_audit_api.py`     | `AuditService.list_audit_logs()`            | `docs/learning/TEST_CASES.md`                    |

## 01. GET /health

| 项目                 | 内容                                                                                                |
| -------------------- | --------------------------------------------------------------------------------------------------- |
| 接口作用             | 确认 FastAPI 是否启动，并返回基础服务状态                                                           |
| 为什么先学习         | 无业务依赖，适合作为学习入口                                                                        |
| Swagger 操作         | 打开`GET /health` → `Try it out` → `Execute`                                                |
| 输入（入力）         | 无                                                                                                  |
| 预想结果（予想結果） | HTTP`200`，`status=ok`，`service=retail-insight-ai`，`provider=static`，非空 `request_id` |
| 后台日志观察         | `request_id`、访问日志、健康检查请求是否进入应用                                                  |
| 对应测试             | `backend/tests/test_api.py`                                                                       |
| 对应源码             | `backend/app/main.py`、`backend/app/api/health.py`、`backend/app/schemas/health.py`           |
| 下一步               | `POST /api/tasks`                                                                                 |

### 程序调用流程

```text
Swagger UI
↓
backend/app/main.py
create_app()
（路由已注册）
↓
backend/app/api/health.py
router = APIRouter()
↓
@router.get("/health")
↓
health()
↓
backend/app/schemas/health.py
HealthResponse
↓
JSON
↓
HTTP Response
```

## 源码学习说明

### backend/app/main.py（项目启动入口）
作用：创建应用实例，并把路由和依赖接到同一个后端上。  
为什么现在学习：先知道请求从哪里进入项目，后面读接口才不会迷路。  
重点关注：
- `create_app()`
- `request_context()`

### backend/app/api/health.py（接口入口）
作用：接收 `GET /health`，返回最小可验证的状态结果。  
为什么现在学习：这是最短的入口，适合先建立 Router→Schema 的直觉。  
重点关注：
- `health()`
- `HealthResponse`

### backend/app/schemas/health.py（响应模型）
作用：固定健康检查返回字段，让接口输出稳定可读。  
为什么现在学习：先理解返回结构，再看更复杂的业务响应。  
重点关注：
- `HealthResponse`
- `status` / `service` / `provider` / `request_id`

再回到 `main.py`，理解 `include_router()` 如何把接口接入应用。

## 02. POST /api/tasks

| 项目                 | 内容                                                                                                                                              |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| 接口作用             | 创建任务，启动主业务链路                                                                                                                          |
| 为什么先学习         | 后续状态、SSE、报告都依赖 `task_id`                                                                                                              |
| Swagger 操作         | 打开 `POST /api/tasks` → `Try it out` → 输入 `question`、`mode` → `Execute`                                                           |
| 输入（入力）         | `question`、`mode`                                                                                                                            |
| 预想结果（予想結果） | HTTP `202`，返回 `task_id` 和 `status=queued`                                                                                                |
| 后台日志观察         | `request_id`、`task_id`、`Request Body`、`queued`、`running`、`completed`、`Route`、`KPI`、`Research`、`Report` |
| 对应测试             | `backend/tests/test_api.py`                                                                                                                     |
| 对应源码             | `backend/app/api/tasks.py`、`backend/app/services/task_service.py`、`backend/app/repositories/implementations/in_memory/task_repository.py`、`backend/app/workflow/graph.py`、`backend/app/kpi/workflow.py`、`backend/app/agents/providers/static_research.py`、`backend/app/reports/generator.py` |
| 下一步               | `GET /api/tasks/{task_id}`                                                                                                                      |

### Learning Trace

```text
POST /api/tasks
request_id : xxxx
task_id    : xxxx

Request Body
--------------------------
question : 你好
mode     : hybrid
--------------------------

============= Request =============
Router.create_task()
    ↓
TaskService.create_task()
    ↓
TaskRepository.create()
    ↓
EventPublisher.publish(queued)
    ↓
BackgroundTasks.add_task()

HTTP 202 返回

============= Background =============
TaskService.run_task()
    ↓
TaskRepository.save(running)
    ↓
EventPublisher.publish(running)
    ↓
AnalysisWorkflow.stream()
    ↓
Route
    ↓
KPI
    ↓
Research
    ↓
Report
    ↓
TaskRepository.save(completed)
    ↓
EventPublisher.publish(completed)
```

### 程序调用流程

```text
客户端（Swagger）
↓
POST /api/tasks
↓
backend/app/main.py
create_app()
（路由已注册）
↓
backend/app/api/tasks.py
router = APIRouter(prefix="/api/tasks")
↓
@router.post("")
↓
create_task()
↓
backend/app/services/task_service.py
TaskService.create_task()
↓
backend/app/repositories/implementations/in_memory/task_repository.py
TaskRepository.create()
↓
backend/app/events/publisher.py
EventPublisher.publish(queued)
↓
BackgroundTasks.add_task()
↓
HTTP 202 返回

==========================
后台异步开始
==========================

backend/app/services/task_service.py
TaskService.run_task()
↓
backend/app/repositories/implementations/in_memory/task_repository.py
TaskRepository.save(running)
↓
backend/app/events/publisher.py
EventPublisher.publish(running)
↓
backend/app/workflow/graph.py
AnalysisWorkflow.stream()
↓
Route
↓
KPI
↓
Research
↓
Report
↓
TaskRepository.save(completed)
↓
EventPublisher.publish(completed)
```

### 源码学习说明

### 主调用链（★★★★★）

### backend/app/api/tasks.py
职责：HTTP 入口，只负责 `create_task()`。  
重点函数：`create_task()`

### backend/app/services/task_service.py
职责：创建任务、串联后台任务执行。  
重点函数：`create_task()`、`run_task()`

### backend/app/repositories/implementations/in_memory/task_repository.py
职责：保存任务状态，承接 queued / running / completed。  
重点函数：`create()`、`save()`

### backend/app/workflow/graph.py
职责：后台 Workflow，推进 `Route -> KPI -> Research -> Report`。  
重点函数：`stream()`

### backend/app/kpi/workflow.py
职责：KPI Workflow。  
重点函数：`run()`

### backend/app/agents/providers/static_research.py
职责：Research。  
重点函数：`research()`

### backend/app/reports/generator.py
职责：生成最终 Report。  
重点函数：`generate()`

### 相关模块（了解即可）

### backend/app/events/publisher.py
说明：负责发布任务生命周期事件。供 SSE/Event Stream 使用。本章节不用深入阅读。  
建议在 `GET /api/tasks/{task_id}/events` 章节再学习。

## 03. GET /api/tasks/{task_id}

| 项目                 | 内容                                                                                                                                              |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| 接口作用             | 按`task_id` 查询任务状态                                                                                                                        |
| 为什么先学习         | 创建任务后先确认状态快照，比直接看 SSE 更容易理解生命周期                                                                                         |
| Swagger 操作         | 打开`GET /api/tasks/{task_id}` → `Try it out` → 填 `task_id` → `Execute`                                                               |
| 输入（入力）         | `task_id`                                                                                                                                       |
| 预想结果（予想結果） | HTTP`200`，返回 `queued/running/completed/failed` 等状态                                                                                      |
| 后台日志观察         | 同一个`task_id` 的状态读取和状态推进日志                                                                                                        |
| 对应测试             | `backend/tests/test_api.py`                                                                                                                     |
| 对应源码             | `backend/app/api/tasks.py`、`backend/app/services/task_service.py`、`backend/app/repositories/implementations/in_memory/task_repository.py` |
| 下一步               | `GET /api/tasks/{task_id}/events`                                                                                                               |

### 程序调用流程

```text
Swagger UI
↓
backend/app/api/tasks.py
get_task()
↓
backend/app/services/task_service.py
TaskService.get_task()
↓
backend/app/repositories/implementations/in_memory/task_repository.py
InMemoryTaskRepository.get()
↓
Response
```

## 源码学习说明

### backend/app/api/tasks.py（任务查询入口）
作用：接收按 `task_id` 读取状态的请求，并返回当前任务快照。  
为什么现在学习：创建任务后，最先要学会的是如何确认它现在跑到哪一步。  
重点关注：
- `get_task()`

### backend/app/services/task_service.py（任务状态读取）
作用：负责从任务仓库读取任务，并统一处理不存在等状态边界。  
为什么现在学习：这里能看清“查状态”和“跑任务”是两件分开的事。  
重点关注：
- `get_task()`

### backend/app/repositories/implementations/in_memory/task_repository.py（任务状态存储）
作用：按 `task_id` 返回当前任务事实对象。  
为什么现在学习：状态查询最终都会落到这里读取真实存储结果。  
重点关注：
- `get()`

## 04. GET /api/tasks/{task_id}/events

| 项目                 | 内容                                                                                                                                    |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| 接口作用             | 通过 SSE 订阅任务过程事件                                                                                                               |
| 为什么先学习         | 体现长任务不是同步短请求，而是有状态推进和实时事件                                                                                      |
| Swagger 操作         | 打开`GET /api/tasks/{task_id}/events` → `Try it out` → 填 `task_id` → `Execute`                                              |
| 输入（入力）         | `task_id`                                                                                                                             |
| 预想结果（予想結果） | HTTP`200`，返回 `text/event-stream`，包含 `status/done/error`                                                                     |
| 后台日志观察         | SSE 连接、事件名称、任务状态、断连或重连现象                                                                                            |
| 对应测试             | `backend/tests/test_api.py`                                                                                                           |
| 对应源码             | `backend/app/api/tasks.py`、`backend/app/events/sse.py`、`backend/app/repositories/implementations/in_memory/event_repository.py` |
| 下一步               | `GET /api/tasks/{task_id}/report`                                                                                                     |

### 程序调用流程

```text
Swagger UI / Browser
↓
backend/app/api/tasks.py
get_task_events()
↓
backend/app/events/sse.py
stream_events()
↓
backend/app/repositories/implementations/in_memory/event_repository.py
InMemoryEventRepository.list_after()
↓
Response Stream
```

## 源码学习说明

### backend/app/api/tasks.py（任务事件入口）
作用：暴露任务事件订阅接口，把同一个 `task_id` 交给 SSE 层继续处理。  
为什么现在学习：这里能看出任务接口不只负责创建，还负责实时观察过程。  
重点关注：
- `get_task_events()`

### backend/app/events/sse.py（SSE 输出）
作用：把事件仓库里的任务事件持续转换成 `text/event-stream` 响应。  
为什么现在学习：这是理解“前端为什么能边跑边看”的关键文件。  
重点关注：
- `stream_task_events()`

### backend/app/repositories/implementations/in_memory/event_repository.py（事件存储）
作用：按顺序保存并读取任务事件。  
为什么现在学习：SSE 不是直接读 Workflow，而是读这里已经落下来的事件事实。  
重点关注：
- `append()`
- `list_after()`

## 05. GET /api/tasks/{task_id}/report

| 项目                 | 内容                                                                                                                                                |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| 接口作用             | 读取任务最终生成的报告                                                                                                                              |
| 为什么先学习         | 主链路最终目标是拿到报告，而不是只看状态变化                                                                                                        |
| Swagger 操作         | 打开`GET /api/tasks/{task_id}/report` → `Try it out` → 填 `task_id` → `Execute`                                                          |
| 输入（入力）         | `task_id`                                                                                                                                         |
| 预想结果（予想結果） | HTTP`200`，返回 `status=generated` 和 Markdown 报告                                                                                             |
| 后台日志观察         | 报告保存、报告读取、`report_not_found` 失败线索                                                                                                   |
| 对应测试             | `backend/tests/test_api.py`                                                                                                                       |
| 对应源码             | `backend/app/api/tasks.py`、`backend/app/services/task_service.py`、`backend/app/repositories/implementations/in_memory/report_repository.py` |
| 下一步               | `POST /api/v1/documents`                                                                                                                          |

### 程序调用流程

```text
Swagger UI
↓
backend/app/api/tasks.py
get_report()
↓
backend/app/services/task_service.py
TaskService.get_report()
↓
backend/app/repositories/implementations/in_memory/report_repository.py
InMemoryReportRepository.get()
↓
Response
```

## 源码学习说明

### backend/app/api/tasks.py（报告读取入口）
作用：接收报告读取请求，并把 `task_id` 交给任务服务查询最终结果。  
为什么现在学习：任务链路走完以后，用户真正关心的是报告能不能拿到。  
重点关注：
- `get_report()`

### backend/app/services/task_service.py（报告读取服务）
作用：负责根据任务 ID 找到最终报告，并处理未生成的边界。  
为什么现在学习：这里能看懂“任务状态”和“任务产物”是分开保存的。  
重点关注：
- `get_report()`

### backend/app/repositories/implementations/in_memory/report_repository.py（报告存储）
作用：保存和读取任务报告正文。  
为什么现在学习：最终 Markdown 报告就是从这里被取出来返回给接口的。  
重点关注：
- `save()`
- `get()`

## 06. POST /api/v1/documents

| 项目                 | 内容                                                                                                                                                                 |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 接口作用             | 上传文件和 metadata，创建文档记录                                                                                                                                    |
| 为什么先学习         | 上传是 import、chunk、retrieval、internal RAG 的入口                                                                                                                 |
| Swagger 操作         | 打开`POST /api/v1/documents` → `Try it out` → 选择文件并填写 `metadata` → `Execute`                                                                            |
| 输入（入力）         | `file`、`metadata`                                                                                                                                                 |
| 预想结果（予想結果） | HTTP`201`，返回 `document_id`、文档状态、checksum、metadata                                                                                                       |
| 后台日志观察         | upload 开始、checksum、重复文件命中、metadata 校验结果                                                                                                              |
| 对应测试             | `backend/tests/test_document_upload_api.py`                                                                                                                         |
| 对应源码             | `backend/app/api/documents.py`、`backend/app/services/document_upload_service.py`、`backend/app/repositories/implementations/in_memory/document_repository.py` |
| 下一步               | `GET /api/v1/documents`                                                                                                                                           |

### 程序调用流程

```text
Swagger UI
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

## 源码学习说明

### backend/app/api/documents.py（文档上传入口）
作用：接收上传文件和 metadata，并把原始输入交给上传服务处理。  
为什么现在学习：Document 链路的第一步就是把事实先送进系统。  
重点关注：
- `upload_document()`

### backend/app/services/document_upload_service.py（文档上传服务）
作用：校验 metadata、生成 checksum、处理重复上传，再创建文档记录。  
为什么现在学习：上传不是简单存文件，这里决定文档能否进入后续流程。  
重点关注：
- `upload_document()`
- `_parse_metadata()`
- `_build_response()`

### backend/app/repositories/implementations/in_memory/document_repository.py（文档事实存储）
作用：保存上传后的文档事实对象。  
为什么现在学习：导入、切分、检索都会先依赖这里的文档记录。  
重点关注：
- `create()`
- `find_by_checksum()`

## 07. GET /api/v1/documents

| 项目                 | 内容                                                                                                                                                              |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 接口作用             | 查看文档列表                                                                                                                                                      |
| 为什么先学习         | 先看集合，最容易理解文档领域对象当前有哪些状态和过滤条件                                                                                                          |
| Swagger 操作         | 打开`GET /api/v1/documents` → `Try it out` → 可选填写过滤条件 → `Execute`                                                                                    |
| 输入（入力）         | `status`、`document_type`、`language`、`tag`、`owner`                                                                                                    |
| 预想结果（予想結果） | HTTP`200`，返回文档列表，默认不含 archived                                                                                                                       |
| 后台日志观察         | 过滤条件、命中文档数量、archived 默认排除行为                                                                                                                      |
| 对应测试             | `backend/tests/test_document_read_api.py`                                                                                                                        |
| 对应源码             | `backend/app/api/documents.py`、`backend/app/services/document_read_service.py`、`backend/app/repositories/implementations/in_memory/document_repository.py` |
| 下一步               | `GET /api/v1/documents/{document_id}`                                                                                                                            |

### 程序调用流程

```text
Swagger UI
↓
backend/app/api/documents.py
list_documents()
↓
backend/app/services/document_read_service.py
DocumentReadService.list_documents()
↓
backend/app/repositories/implementations/in_memory/document_repository.py
InMemoryDocumentRepository.list_all()
↓
Response
```

## 源码学习说明

### backend/app/api/documents.py（文档列表入口）
作用：接收过滤条件，并返回当前可见的文档集合。  
为什么现在学习：读集合最适合先认识文档模型里的状态和基础字段。  
重点关注：
- `list_documents()`

### backend/app/services/document_read_service.py（文档读取服务）
作用：负责过滤文档列表，并组装列表响应。  
为什么现在学习：这里能看出哪些筛选逻辑属于业务层，而不是 Router。  
重点关注：
- `list_documents()`
- `_matches()`

### backend/app/repositories/implementations/in_memory/document_repository.py（文档列表存储）
作用：返回当前仓库中的全部文档事实，供上层再做过滤。  
为什么现在学习：列表查询最终还是从同一份文档事实集合开始。  
重点关注：
- `list_all()`

## 08. GET /api/v1/documents/{document_id}

| 项目                 | 内容                                                                                                                                                               |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 接口作用             | 读取单个文档详情                                                                                                                                                   |
| 为什么先学习         | 详情接口能展示文档领域对象的完整字段和状态                                                                                                                         |
| Swagger 操作         | 打开`GET /api/v1/documents/{document_id}` → `Try it out` → 填 `document_id` → `Execute`                                                                 |
| 输入（入力）         | `document_id`                                                                                                                                                    |
| 预想结果（予想結果） | HTTP`200`，返回文档详情；不存在时返回 `document_not_found`                                                                                                     |
| 后台日志观察         | 文档命中、缺失日志、响应字段是否齐全                                                                                                                               |
| 对应测试             | `backend/tests/test_document_read_api.py`                                                                                                                        |
| 对应源码             | `backend/app/api/documents.py`、`backend/app/services/document_read_service.py`、`backend/app/repositories/implementations/in_memory/document_repository.py` |
| 下一步               | `DELETE /api/v1/documents/{document_id}`                                                                                                                         |

### 程序调用流程

```text
Swagger UI
↓
backend/app/api/documents.py
get_document()
↓
backend/app/services/document_read_service.py
DocumentReadService.get_document()
↓
backend/app/repositories/implementations/in_memory/document_repository.py
InMemoryDocumentRepository.get()
↓
Response
```

## 源码学习说明

### backend/app/api/documents.py（文档详情入口）
作用：接收 `document_id` 并发起单文档详情查询。  
为什么现在学习：看详情比看列表更容易理解一个 Document 实体完整长什么样。  
重点关注：
- `get_document()`

### backend/app/services/document_read_service.py（文档详情读取）
作用：负责读取单个文档，并处理不存在的情况。  
为什么现在学习：这里能帮助初学者看懂“列表查询”和“单体查询”的分工。  
重点关注：
- `get_document()`

### backend/app/repositories/implementations/in_memory/document_repository.py（文档详情存储）
作用：按 `document_id` 返回对应文档事实。  
为什么现在学习：详情接口最终就是从这里拿到真实文档对象。  
重点关注：
- `get()`

## 09. DELETE /api/v1/documents/{document_id}

| 项目                 | 内容                                                                                                                                                                  |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 接口作用             | 归档文档，不做物理删除                                                                                                                                                |
| 为什么先学习         | 理解 archive 语义、可追溯删除和企业审计边界                                                                                                                           |
| Swagger 操作         | 打开`DELETE /api/v1/documents/{document_id}` → `Try it out` → 填 `document_id` → `Execute`                                                                 |
| 输入（入力）         | `document_id`                                                                                                                                                       |
| 预想结果（予想結果） | HTTP`200`，文档进入 archived，列表默认不再显示                                                                                                                      |
| 后台日志观察         | 归档状态变化、列表变化、重复归档边界                                                                                                                                  |
| 对应测试             | `backend/tests/test_document_archive_api.py`                                                                                                                        |
| 对应源码             | `backend/app/api/documents.py`、`backend/app/services/document_archive_service.py`、`backend/app/repositories/implementations/in_memory/document_repository.py` |
| 下一步               | `POST /api/v1/documents/{document_id}/import`                                                                                                                       |

### 程序调用流程

```text
Swagger UI
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

## 源码学习说明

### backend/app/api/documents.py（文档归档入口）
作用：接收归档请求，把目标文档交给归档服务处理。  
为什么现在学习：这里能建立“删除并不一定是物理删除”的企业项目直觉。  
重点关注：
- `archive_document()`

### backend/app/services/document_archive_service.py（文档归档服务）
作用：把文档状态改成 archived，并发布对应领域事件。  
为什么现在学习：归档的重点不是删文件，而是稳定保存状态变化。  
重点关注：
- `archive_document()`

### backend/app/repositories/implementations/in_memory/document_repository.py（文档归档存储）
作用：持久化归档后的文档状态。  
为什么现在学习：归档动作最终还是通过更新文档事实来完成。  
重点关注：
- `update()`

## 10. POST /api/v1/documents/{document_id}/import

| 项目                 | 内容                                                                                                                                                                        |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 接口作用             | 启动文档导入流程，把上传文档推进到可处理状态                                                                                                                                |
| 为什么先学习         | 上传完成不代表可检索，导入决定文档是否能进入后续 pipeline                                                                                                                   |
| Swagger 操作         | 打开`POST /api/v1/documents/{document_id}/import` → `Try it out` → 填 `document_id` → `Execute`                                                                  |
| 输入（入力）         | `document_id`                                                                                                                                                             |
| 预想结果（予想結果） | 返回 import 结果，文档状态推进到 validated 等后续状态                                                                                                                       |
| 后台日志观察         | import 状态、失败原因、文档类型支持与否                                                                                                                                     |
| 对应测试             | `backend/tests/test_document_import_api.py`                                                                                                                               |
| 对应源码             | `backend/app/api/document_imports.py`、`backend/app/services/document_import_service.py`、`backend/app/repositories/implementations/in_memory/document_repository.py` |
| 下一步               | `POST /api/v1/documents/{document_id}/chunks`                                                                                                                             |

### 程序调用流程

```text
Swagger UI
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

## 源码学习说明

### backend/app/api/document_imports.py（文档导入入口）
作用：接收导入请求，并把指定文档推进到导入服务。  
为什么现在学习：导入是上传之后的独立一步，不要把两者看成同一件事。  
重点关注：
- `import_document()`
- `get_document_import()`

### backend/app/services/document_import_service.py（文档导入服务）
作用：校验文档状态和类型，再把文档推进到可切分的阶段。  
为什么现在学习：后续 chunk 和 retrieval 都只接受已经过导入校验的文档。  
重点关注：
- `import_document()`
- `get_import()`

### backend/app/repositories/implementations/in_memory/document_repository.py（文档导入存储）
作用：保存导入后的文档状态变化。  
为什么现在学习：导入结果不会凭空存在，最终还是落回文档事实本身。  
重点关注：
- `update()`
- `get()`

## 11. POST /api/v1/documents/{document_id}/chunks

| 项目                 | 内容                                                                                                                                                                            |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 接口作用             | 把 validated 文档切成 chunk                                                                                                                                                     |
| 为什么先学习         | chunk 是 retrieval 和 citation 的基础数据层                                                                                                                                     |
| Swagger 操作         | 打开`POST /api/v1/documents/{document_id}/chunks` → `Try it out` → 填 `document_id` → `Execute`                                                                      |
| 输入（入力）         | `document_id`                                                                                                                                                                 |
| 预想结果（予想結果） | HTTP`201`，返回 chunk 列表、chunk 数量和元数据                                                                                                                                |
| 后台日志观察         | chunk 数量、`chunk_index`、切分策略、replace 行为                                                                                                                             |
| 对应测试             | `backend/tests/test_document_chunk_api.py`                                                                                                                                    |
| 对应源码             | `backend/app/api/document_chunks.py`、`backend/app/services/document_chunk_service.py`、`backend/app/repositories/implementations/in_memory/document_chunk_repository.py` |
| 下一步               | `GET /api/v1/documents/{document_id}/chunks`                                                                                                                                  |

### 程序调用流程

```text
Swagger UI
↓
backend/app/api/document_chunks.py
chunk_document()
↓
backend/app/services/document_chunk_service.py
DocumentChunkService.chunk_document()
↓
backend/app/repositories/implementations/in_memory/document_chunk_repository.py
InMemoryDocumentChunkRepository.replace_for_document()
↓
Response
```

## 源码学习说明

### backend/app/api/document_chunks.py（切分入口）
作用：接收切分请求，并把目标文档交给 chunk 服务。  
为什么现在学习：chunk 是文档链路里第一次把正文改造成可检索结构。  
重点关注：
- `chunk_document()`

### backend/app/services/document_chunk_service.py（文档切分服务）
作用：读取文档、校验状态、构造 chunk，再替换当前版本切分结果。  
为什么现在学习：这里决定 chunk 长什么样，以及为什么会有版本语义。  
重点关注：
- `chunk_document()`
- `_build_chunks()`
- `_chunk_id()`

### backend/app/repositories/implementations/in_memory/document_chunk_repository.py（chunk 存储）
作用：按文档和版本保存切分结果。  
为什么现在学习：检索和 citation 依赖的不是原文，而是这里保存的 chunk 集。  
重点关注：
- `replace_for_document()`

## 12. GET /api/v1/documents/{document_id}/chunks

| 项目                 | 内容                                                                                                                                                                            |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 接口作用             | 读取当前版本 chunk 列表                                                                                                                                                         |
| 为什么先学习         | 验证切分结果不仅写入成功，而且可以再次读取                                                                                                                                      |
| Swagger 操作         | 打开`GET /api/v1/documents/{document_id}/chunks` → `Try it out` → 填 `document_id` → `Execute`                                                                       |
| 输入（入力）         | `document_id`                                                                                                                                                                 |
| 预想结果（予想結果） | HTTP`200`，返回 `chunk_id`、`chunk_index`、内容片段和元数据                                                                                                               |
| 后台日志观察         | chunk 读取数量、空结果、读取与写入是否一致                                                                                                                                      |
| 对应测试             | `backend/tests/test_document_chunk_api.py`                                                                                                                                    |
| 对应源码             | `backend/app/api/document_chunks.py`、`backend/app/services/document_chunk_service.py`、`backend/app/repositories/implementations/in_memory/document_chunk_repository.py` |
| 下一步               | `POST /api/v1/document-retrieval/search`                                                                                                                                      |

### 程序调用流程

```text
Swagger UI
↓
backend/app/api/document_chunks.py
get_document_chunks()
↓
backend/app/services/document_chunk_service.py
DocumentChunkService.get_chunks()
↓
backend/app/repositories/implementations/in_memory/document_chunk_repository.py
InMemoryDocumentChunkRepository.list_for_document()
↓
Response
```

## 源码学习说明

### backend/app/api/document_chunks.py（chunk 读取入口）
作用：接收 chunk 读取请求，并返回当前文档版本的切分结果。  
为什么现在学习：写入 chunk 以后，最好立刻看它是怎样被重新读出来的。  
重点关注：
- `get_document_chunks()`

### backend/app/services/document_chunk_service.py（chunk 读取服务）
作用：负责读取当前文档版本的 chunk 列表。  
为什么现在学习：这一步能帮助初学者理解“切分”和“读取切分结果”是分开的。  
重点关注：
- `get_chunks()`

### backend/app/repositories/implementations/in_memory/document_chunk_repository.py（chunk 读取存储）
作用：按文档和版本返回 chunk 列表。  
为什么现在学习：后续 retrieval 实际上就是在读取这里的结果。  
重点关注：
- `list_for_document()`

## 13. POST /api/v1/document-retrieval/search

| 项目                 | 内容                                                                                                                                                                            |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 接口作用             | 从 chunk 集合中检索相关片段                                                                                                                                                     |
| 为什么先学习         | answer 和 citation 必须建立在检索证据上                                                                                                                                         |
| Swagger 操作         | 打开`POST /api/v1/document-retrieval/search` → `Try it out` → 输入 `query` 和过滤条件 → `Execute`                                                                    |
| 输入（入力）         | `query`、`limit`、`include_archived`、`document_type`、`language`、`tags`                                                                                           |
| 预想结果（予想結果） | HTTP`200`，返回 ranked chunks、score、source、metadata                                                                                                                        |
| 后台日志观察         | query、过滤条件、命中 chunk、archived 排除、排序                                                                                                                                |
| 对应测试             | `backend/tests/test_document_retrieval_api.py`                                                                                                                                |
| 对应源码             | `backend/app/api/document_retrieval.py`、`backend/app/services/document_retrieval_service.py`、`backend/app/repositories/implementations/in_memory/document_retrieval.py` |
| 下一步               | `POST /api/v1/internal-rag/answer`                                                                                                                                            |

### 程序调用流程

```text
Swagger UI
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

## 源码学习说明

### backend/app/api/document_retrieval.py（检索入口）
作用：接收查询词和过滤条件，并把请求送进检索服务。  
为什么现在学习：RAG 不是直接回答问题，而是先从这里找证据。  
重点关注：
- `search_documents()`

### backend/app/services/document_retrieval_service.py（文档检索服务）
作用：整理检索请求边界，再把真正检索交给当前检索后端。  
为什么现在学习：这里是以后升级语义检索前最重要的服务边界。  
重点关注：
- `search()`
- `_normalize_query()`

### backend/app/repositories/implementations/in_memory/document_retrieval.py（当前检索后端）
作用：执行当前项目的 keyword-only 检索、过滤和排序。  
为什么现在学习：能直接看懂现阶段检索为什么是可运行但仍非语义化。  
重点关注：
- `search()`
- `_matches_document()`
- `_score_chunk()`

## 14. POST /api/v1/internal-rag/answer

| 项目                 | 内容                                                                                                                                          |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| 接口作用             | 基于检索结果生成确定性内部回答                                                                                                                |
| 为什么先学习         | 体现当前不接真实 LLM 也能做可解释 answer + citation                                                                                           |
| Swagger 操作         | 打开`POST /api/v1/internal-rag/answer` → `Try it out` → 输入 `question` 和检索参数 → `Execute`                                     |
| 输入（入力）         | `question`、`limit`、`include_archived`、`document_type`、`language`、`tags`、`answer_mode`、`require_citations`              |
| 预想结果（予想結果） | HTTP`200`，返回 `answer`、`citations`、`confidence`、`warnings`                                                                     |
| 后台日志观察         | retrieval 是否成功、citation 是否齐全、warning、deterministic fallback                                                                        |
| 对应测试             | `backend/tests/test_internal_rag_api.py`、`backend/tests/test_internal_rag_evaluation.py`、`backend/tests/test_rag_answer_generator.py` |
| 对应源码             | `backend/app/api/internal_rag.py`、`backend/app/services/internal_rag_service.py`、`backend/app/services/rag_answer_generator.py`       |
| 下一步               | `POST /api/v1/reports/{task_id}/submit-approval`                                                                                            |

### 程序调用流程

```text
Swagger UI
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

## 源码学习说明

### backend/app/api/internal_rag.py（内部回答入口）
作用：接收内部问答请求，并把问题和检索参数交给回答服务。  
为什么现在学习：这是 Retrieval 之后真正进入“生成回答”阶段的入口。  
重点关注：
- `answer_internal_rag()`

### backend/app/services/internal_rag_service.py（回答编排服务）
作用：先做检索，再校验结果，最后交给答案生成器组装输出。  
为什么现在学习：它说明当前项目的 RAG 仍然是“检索优先、回答随后”。  
重点关注：
- `answer()`
- `_request_summary()`

### backend/app/services/rag_answer_generator.py（答案生成器）
作用：把检索片段整理成 answer、citations 和 confidence。  
为什么现在学习：当前 no-LLM 模式下，回答是如何被确定性拼装出来的，都在这里。  
重点关注：
- `generate()`
- `_build_citations()`
- `_build_deterministic_result()`

## 15. POST /api/v1/reports/{task_id}/submit-approval

| 项目                 | 内容                                                                                                                                                          |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 接口作用             | 把任务报告提交到审批流                                                                                                                                        |
| 为什么先学习         | 这是分析结果进入治理流程的边界                                                                                                                                |
| Swagger 操作         | 打开`POST /api/v1/reports/{task_id}/submit-approval` → `Try it out` → 填 `task_id` → `Execute`                                                     |
| 输入（入力）         | `task_id`、可选 comment                                                                                                                                     |
| 预想结果（予想結果） | HTTP`200`，返回 approval request 和状态                                                                                                                     |
| 后台日志观察         | RBAC 检查、审批创建、报告版本快照、审计记录                                                                                                                   |
| 对应测试             | `backend/tests/test_approval_api.py`、`backend/tests/test_rbac_guard.py`                                                                                  |
| 对应源码             | `backend/app/api/approvals.py`、`backend/app/services/approval_service.py`、`backend/app/repositories/implementations/in_memory/approval_repository.py` |
| 下一步               | `GET /api/v1/approvals`                                                                                                                                     |

### 程序调用流程

```text
Swagger UI
↓
backend/app/api/approvals.py
submit_approval()
↓
backend/app/services/approval_service.py
ApprovalService.submit_approval()
↓
backend/app/repositories/implementations/in_memory/approval_repository.py
InMemoryApprovalRepository.save_approval_request()
↓
Response
```

## 源码学习说明

### backend/app/api/approvals.py（审批提交入口）
作用：接收报告提审请求，并把它交给审批服务创建审批记录。  
为什么现在学习：报告不是生成完就结束，企业流程往往从这里才进入治理阶段。  
重点关注：
- `submit_approval()`

### backend/app/services/approval_service.py（审批提交服务）
作用：冻结报告版本、创建审批请求，并记录审批起点。  
为什么现在学习：这一步最能体现“审批的是某个版本”，不是审批一段临时文本。  
重点关注：
- `submit_approval()`
- `_create_version_snapshot()`

### backend/app/repositories/implementations/in_memory/approval_repository.py（审批数据存储）
作用：保存审批请求和报告版本快照。  
为什么现在学习：审批资源能被后续查询、批准、拒绝，靠的就是这里先落事实。  
重点关注：
- `save_report_version()`
- `save_approval_request()`

## 16. GET /api/v1/approvals

| 项目                 | 内容                                                                                                                                                          |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 接口作用             | 查看审批列表                                                                                                                                                  |
| 为什么先学习         | 先看集合，再看单体详情，容易理解审批是独立资源                                                                                                                |
| Swagger 操作         | 打开`GET /api/v1/approvals` → `Try it out` → 可选过滤 → `Execute`                                                                                    |
| 输入（入力）         | 可选过滤条件                                                                                                                                                  |
| 预想结果（予想結果） | HTTP`200`，返回 approval list                                                                                                                               |
| 后台日志观察         | RBAC 检查、列表过滤、审批数量和状态分布                                                                                                                       |
| 对应测试             | `backend/tests/test_approval_api.py`                                                                                                                        |
| 对应源码             | `backend/app/api/approvals.py`、`backend/app/services/approval_service.py`、`backend/app/repositories/implementations/in_memory/approval_repository.py` |
| 下一步               | `GET /api/v1/approvals/{approval_id}`                                                                                                                       |

### 程序调用流程

```text
Swagger UI
↓
backend/app/api/approvals.py
list_approvals()
↓
backend/app/services/approval_service.py
ApprovalService.list_approvals()
↓
backend/app/repositories/implementations/in_memory/approval_repository.py
InMemoryApprovalRepository.list_approval_requests()
↓
Response
```

## 源码学习说明

### backend/app/api/approvals.py（审批列表入口）
作用：接收审批列表查询，并把过滤条件交给审批服务。  
为什么现在学习：先读集合，最容易建立当前系统里有哪些审批实例的直觉。  
重点关注：
- `list_approvals()`

### backend/app/services/approval_service.py（审批列表服务）
作用：负责整理查询条件，并返回审批列表结果。  
为什么现在学习：这里能看清审批资源是如何被当作独立业务对象读取的。  
重点关注：
- `list_approvals()`

### backend/app/repositories/implementations/in_memory/approval_repository.py（审批列表存储）
作用：返回当前保存的审批请求集合。  
为什么现在学习：审批列表最终来自这里，而不是实时重新计算。  
重点关注：
- `list_approval_requests()`

## 17. GET /api/v1/approvals/{approval_id}

| 项目                 | 内容                                                                                                                                                          |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 接口作用             | 查看单个审批详情                                                                                                                                              |
| 为什么先学习         | 详情接口能解释审批状态机当前位置                                                                                                                              |
| Swagger 操作         | 打开`GET /api/v1/approvals/{approval_id}` → `Try it out` → 填 `approval_id` → `Execute`                                                            |
| 输入（入力）         | `approval_id`                                                                                                                                               |
| 预想结果（予想結果） | HTTP`200`，返回审批状态、版本、事件或关联信息                                                                                                               |
| 后台日志观察         | RBAC 检查、状态读取、不存在时的错误分支                                                                                                                       |
| 对应测试             | `backend/tests/test_approval_api.py`                                                                                                                        |
| 对应源码             | `backend/app/api/approvals.py`、`backend/app/services/approval_service.py`、`backend/app/repositories/implementations/in_memory/approval_repository.py` |
| 下一步               | `POST /api/v1/approvals/{approval_id}/approve`                                                                                                              |

### 程序调用流程

```text
Swagger UI
↓
backend/app/api/approvals.py
get_approval()
↓
backend/app/services/approval_service.py
ApprovalService.get_approval()
↓
backend/app/repositories/implementations/in_memory/approval_repository.py
InMemoryApprovalRepository.get_approval_request()
↓
Response
```

## 源码学习说明

### backend/app/api/approvals.py（审批详情入口）
作用：接收 `approval_id`，查询单个审批实例的当前状态。  
为什么现在学习：当你已经看到审批列表，下一步自然是理解单个审批怎么看。  
重点关注：
- `get_approval()`

### backend/app/services/approval_service.py（审批详情服务）
作用：读取单个审批并处理不存在等错误边界。  
为什么现在学习：这里能直接看到审批状态机当前停在哪个状态。  
重点关注：
- `get_approval()`

### backend/app/repositories/implementations/in_memory/approval_repository.py（审批详情存储）
作用：按 `approval_id` 返回审批请求事实。  
为什么现在学习：详情读取最终就是从这里拿到唯一那条审批记录。  
重点关注：
- `get_approval_request()`

## 18. POST /api/v1/approvals/{approval_id}/approve

| 项目                 | 内容                                                                                                                      |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| 接口作用             | 批准审批请求                                                                                                              |
| 为什么先学习         | 正向审批动作同时体现状态推进、权限检查和审计                                                                              |
| Swagger 操作         | 打开`POST /api/v1/approvals/{approval_id}/approve` → `Try it out` → 填 `approval_id` → `Execute`               |
| 输入（入力）         | `approval_id`、可选 comment                                                                                             |
| 预想结果（予想結果） | HTTP`200`，审批状态变为 `approved`                                                                                    |
| 后台日志观察         | `approval.approve` 权限检查、审计写入、状态变化                                                                         |
| 对应测试             | `backend/tests/test_approval_api.py`、`backend/tests/test_rbac_guard.py`、`backend/tests/test_audit_middleware.py`  |
| 对应源码             | `backend/app/api/approvals.py`、`backend/app/services/approval_service.py`、`backend/app/services/audit_service.py` |
| 下一步               | `POST /api/v1/approvals/{approval_id}/reject`                                                                           |

### 程序调用流程

```text
Swagger UI
↓
backend/app/api/approvals.py
approve()
↓
backend/app/services/approval_service.py
ApprovalService.approve()
↓
backend/app/repositories/implementations/in_memory/approval_repository.py
InMemoryApprovalRepository.save_approval_request()
↓
backend/app/services/audit_service.py
AuditService.record_audit_log()
↓
Response
```

## 源码学习说明

### backend/app/api/approvals.py（批准入口）
作用：接收批准动作，并把审批决定交给审批服务与审计逻辑处理。  
为什么现在学习：这里最适合观察“业务动作 + 权限 + 审计”是如何一起出现的。  
重点关注：
- `approve()`
- `_run_audited_operation()`

### backend/app/services/approval_service.py（批准服务）
作用：推进审批状态到 `approved`，并记录对应审批事件。  
为什么现在学习：真正改变审批状态的地方在这里，不在 Router。  
重点关注：
- `approve()`
- `_record_event()`

### backend/app/services/audit_service.py（审批审计服务）
作用：把批准动作写成可追踪的审计记录。  
为什么现在学习：企业审批不仅要成功，还要能解释是谁批准了什么。  
重点关注：
- `record_audit_log()`

## 19. POST /api/v1/approvals/{approval_id}/reject

| 项目                 | 内容                                                                                                                      |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| 接口作用             | 拒绝审批请求                                                                                                              |
| 为什么先学习         | 企业项目必须验证拒绝、失败原因和负向状态                                                                                  |
| Swagger 操作         | 打开`POST /api/v1/approvals/{approval_id}/reject` → `Try it out` → 填 `approval_id` → `Execute`                |
| 输入（入力）         | `approval_id`、可选 reason                                                                                              |
| 预想结果（予想結果） | HTTP`200`，审批状态变为 `rejected`                                                                                    |
| 后台日志观察         | `approval.reject` 权限检查、拒绝动作、审计日志、状态稳定性                                                              |
| 对应测试             | `backend/tests/test_approval_api.py`、`backend/tests/test_rbac_guard.py`、`backend/tests/test_audit_middleware.py`  |
| 对应源码             | `backend/app/api/approvals.py`、`backend/app/services/approval_service.py`、`backend/app/services/audit_service.py` |
| 下一步               | `GET /api/v1/users/me`                                                                                                  |

### 程序调用流程

```text
Swagger UI
↓
backend/app/api/approvals.py
reject()
↓
backend/app/services/approval_service.py
ApprovalService.reject()
↓
backend/app/repositories/implementations/in_memory/approval_repository.py
InMemoryApprovalRepository.save_approval_request()
↓
backend/app/services/audit_service.py
AuditService.record_audit_log()
↓
Response
```

## 源码学习说明

### backend/app/api/approvals.py（拒绝入口）
作用：接收拒绝动作，并把理由和目标审批交给后续服务。  
为什么现在学习：批准路径看完以后，再看拒绝路径更容易理解状态机完整性。  
重点关注：
- `reject()`
- `_run_audited_operation()`

### backend/app/services/approval_service.py（拒绝服务）
作用：推进审批状态到 `rejected`，并记录拒绝事件。  
为什么现在学习：企业项目必须把负向结果也当成正式业务状态来处理。  
重点关注：
- `reject()`
- `_record_event()`

### backend/app/services/audit_service.py（拒绝审计服务）
作用：把拒绝动作写入审计日志。  
为什么现在学习：拒绝通常比批准更需要留下理由和追踪证据。  
重点关注：
- `record_audit_log()`

## 20. GET /api/v1/users/me

| 项目                 | 内容                                                                          |
| -------------------- | ----------------------------------------------------------------------------- |
| 接口作用             | 返回当前用户占位主体                                                          |
| 为什么先学习         | 理解当前没有真实登录，但保留了认证接入边界                                    |
| Swagger 操作         | 打开`GET /api/v1/users/me` → `Try it out` → `Execute`                 |
| 输入（入力）         | 无                                                                            |
| 预想结果（予想結果） | HTTP`200`，返回 `user_id=system` 等 current user 信息                     |
| 后台日志观察         | current user 解析、`request_id`、安全读模型是否正常                         |
| 对应测试             | `backend/tests/test_security_audit_api.py`                                  |
| 对应源码             | `backend/app/api/security.py`、`backend/app/services/security_service.py` |
| 下一步               | `GET /api/v1/security/roles`                                                |

### 程序调用流程

```text
Swagger UI
↓
backend/app/api/security.py
get_current_user()
↓
backend/app/services/security_service.py
SecurityService.get_current_user()
↓
Response
```

## 源码学习说明

### backend/app/api/security.py（当前用户入口）
作用：返回当前请求上下文里的占位用户信息。  
为什么现在学习：当前项目没有真实登录，但很多权限链路都要先经过这个边界。  
重点关注：
- `get_current_user()`

### backend/app/services/security_service.py（当前用户读模型）
作用：提供当前用户对象，供权限检查和安全接口读取。  
为什么现在学习：先理解占位用户从哪里来，后面读 RBAC 会更轻松。  
重点关注：
- `get_current_user()`

## 21. GET /api/v1/security/roles

| 项目                 | 内容                                                                          |
| -------------------- | ----------------------------------------------------------------------------- |
| 接口作用             | 读取冻结角色目录                                                              |
| 为什么先学习         | 先看角色，再看权限，更容易理解 RBAC 层级                                      |
| Swagger 操作         | 打开`GET /api/v1/security/roles` → `Try it out` → `Execute`           |
| 输入（入力）         | 无                                                                            |
| 预想结果（予想結果） | HTTP`200`，返回 roles                                                       |
| 后台日志观察         | role catalog 读取、静态目录初始化、响应结构                                   |
| 对应测试             | `backend/tests/test_security_audit_api.py`                                  |
| 对应源码             | `backend/app/api/security.py`、`backend/app/services/security_service.py` |
| 下一步               | `GET /api/v1/security/permissions`                                          |

### 程序调用流程

```text
Swagger UI
↓
backend/app/api/security.py
get_roles()
↓
backend/app/services/security_service.py
SecurityService.list_roles()
↓
Response
```

## 源码学习说明

### backend/app/api/security.py（角色目录入口）
作用：接收角色目录读取请求，并返回当前系统冻结的角色集合。  
为什么现在学习：先理解“有哪些角色”，后面看权限目录更自然。  
重点关注：
- `get_roles()`

### backend/app/services/security_service.py（角色目录服务）
作用：提供系统当前可用的角色定义。  
为什么现在学习：RBAC 的第一层就是角色目录，这里最适合建立基础概念。  
重点关注：
- `list_roles()`

## 22. GET /api/v1/security/permissions

| 项目                 | 内容                                                                          |
| -------------------- | ----------------------------------------------------------------------------- |
| 接口作用             | 读取冻结权限目录                                                              |
| 为什么先学习         | 审批 RBAC 的动作最终落在权限名上                                              |
| Swagger 操作         | 打开`GET /api/v1/security/permissions` → `Try it out` → `Execute`     |
| 输入（入力）         | 无                                                                            |
| 预想结果（予想結果） | HTTP`200`，返回 permissions                                                 |
| 后台日志观察         | permission catalog 读取、权限数量、命名是否与审批动作一致                     |
| 对应测试             | `backend/tests/test_security_audit_api.py`                                  |
| 对应源码             | `backend/app/api/security.py`、`backend/app/services/security_service.py` |
| 下一步               | `GET /api/v1/audit-logs`                                                    |

### 程序调用流程

```text
Swagger UI
↓
backend/app/api/security.py
get_permissions()
↓
backend/app/services/security_service.py
SecurityService.list_permissions()
↓
Response
```

## 源码学习说明

### backend/app/api/security.py（权限目录入口）
作用：接收权限目录读取请求，并返回当前系统暴露的权限名集合。  
为什么现在学习：审批动作最后会落到具体权限名，所以这里是 RBAC 的第二层。  
重点关注：
- `get_permissions()`

### backend/app/services/security_service.py（权限目录服务）
作用：提供权限目录，并承接后续权限判断逻辑。  
为什么现在学习：读完这个文件，后面看审批接口的权限检查会更顺。  
重点关注：
- `list_permissions()`
- `require_permission()`

## 23. GET /api/v1/audit-logs

| 项目                 | 内容                                                                                                                                                     |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 接口作用             | 读取 append-only 审计日志                                                                                                                                |
| 为什么先学习         | 企业项目要解释谁做了什么、什么时候做、为什么被允许或拒绝                                                                                                 |
| Swagger 操作         | 打开`GET /api/v1/audit-logs` → `Try it out` → `Execute`                                                                                          |
| 输入（入力）         | 无                                                                                                                                                       |
| 预想结果（予想結果） | HTTP`200`，返回 audit log list                                                                                                                         |
| 后台日志观察         | append-only 读取、审计事件名、成功/失败事实                                                                                                              |
| 对应测试             | `backend/tests/test_security_audit_api.py`、`backend/tests/test_audit_middleware.py`                                                                 |
| 对应源码             | `backend/app/api/audit_logs.py`、`backend/app/services/audit_service.py`、`backend/app/repositories/implementations/in_memory/audit_repository.py` |
| 下一步               | `docs/learning/TEST_CASES.md`                                                                                                                          |

### 程序调用流程

```text
Swagger UI
↓
backend/app/api/audit_logs.py
get_audit_logs()
↓
backend/app/services/audit_service.py
AuditService.list_audit_logs()
↓
backend/app/repositories/implementations/in_memory/audit_repository.py
InMemoryAuditRepository.list_all()
↓
Response
```

## 源码学习说明

### backend/app/api/audit_logs.py（审计日志入口）
作用：接收审计日志读取请求，并返回系统已记录的审计事实。  
为什么现在学习：所有安全和审批动作最后都能回到这里做事后追踪。  
重点关注：
- `get_audit_logs()`

### backend/app/services/audit_service.py（审计日志服务）
作用：提供审计记录写入和读取的统一边界。  
为什么现在学习：这里能帮助初学者区分“普通日志”和“审计事实”不是一回事。  
重点关注：
- `record_audit_log()`
- `list_audit_logs()`

### backend/app/repositories/implementations/in_memory/audit_repository.py（审计事实存储）
作用：以 append-only 方式保存并读取审计日志。  
为什么现在学习：审计可追溯的前提，就是底层不允许随意改写历史。  
重点关注：
- `append()`
- `list_all()`

## 补充接口：POST /api/v1/reports/{task_id}/revise

| 项目                 | 内容                                                                                             |
| -------------------- | ------------------------------------------------------------------------------------------------ |
| 接口作用             | 修订报告并形成新的审批相关版本语义                                                               |
| 为什么先学习         | 这是审批链路的补充动作，不属于本轮 23 个主学习接口，但属于现有 Approval 能力                     |
| Swagger 操作         | 打开`POST /api/v1/reports/{task_id}/revise` → `Try it out` → 填 `task_id` → `Execute` |
| 输入（入力）         | `task_id`、可选 revision reason                                                                |
| 预想结果（予想結果） | 返回 revision 结果                                                                               |
| 后台日志观察         | revision 日志、新快照记录、审批状态关系                                                          |
| 对应测试             | `backend/tests/test_approval_api.py`                                                           |
| 对应源码             | `backend/app/api/approvals.py`、`backend/app/services/approval_service.py`                   |
| 下一步               | 回看 approval 状态机                                                                             |

### 程序调用流程

```text
Swagger UI
↓
backend/app/api/approvals.py
revise()
↓
backend/app/services/approval_service.py
ApprovalService.revise()
↓
backend/app/repositories/implementations/in_memory/approval_repository.py
InMemoryApprovalRepository.save_report_version()
↓
Response
```

## 源码学习说明

### backend/app/api/approvals.py（报告修订入口）
作用：接收报告修订请求，并把修订动作交给审批服务生成新版本语义。  
为什么现在学习：这能补齐审批链路里“不是批准也不是拒绝”的第三种处理方式。  
重点关注：
- `revise()`

### backend/app/services/approval_service.py（报告修订服务）
作用：创建新的报告版本快照，并返回修订结果。  
为什么现在学习：它说明审批流里的修订本质上仍然是版本管理问题。  
重点关注：
- `revise()`
- `_create_version_snapshot()`
