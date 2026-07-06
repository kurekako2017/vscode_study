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

Learning Trace 是一组可关闭的教学日志，用来把 Swagger、Router、Service、Repository 和 SSE 串成同一条学习链路。

什么时候开启：

- 只在你想学习“请求是怎么走到源码里”的时候开启。
- 正常使用、普通调试、日常运行都保持默认关闭。
- 默认配置是 `LEARNING_TRACE=false`，关闭时完全没有影响。

为什么存在：

- Swagger 只能告诉我们接口响应结果。
- Learning Trace 用来补上“请求在后端内部到底走到了哪里”。
- 它特别适合初学者对照阅读 `Router -> Service -> Repository`，再理解 SSE 这种长连接是怎么持续输出事件的。

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

对 `POST /api/tasks` 来说，这条学习链路会在后台任务完成后统一打印完整 block，方便你把 Router、Service、Workflow、Provider、Repository 和 Response 串起来看。

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
HTTP Request
↓
Router
↓
health()
↓
HealthResponse
↓
HTTP Response
```

对于 `POST /api/tasks`，你会看到：

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

如果只想关闭 Phase 2，仍然只需要把 `.env` 中的值改回：

```env
LEARNING_TRACE=false
```

然后重启后端即可。

### Learning Trace Phase 4

Phase 4 把学习 trace 升级成“源码一眼可读块”。它不是为了增加新业务节点，而是为了让日志顺着源码目录读就能定位到对应文件。

现在每个 frame 都会显示：

- `node`
- `class`
- `method`
- `file`

并且会按文件类型自动补出教学节点：

- `backend/app/api/**` -> `Controller File`
- `backend/app/schemas/**` -> `Schema File`
- 其他新 Python 文件 -> `Entering File`

这套输出和实际源码阅读顺序保持一致：

```text
LEARNING TRACE
GET /health
request_id: ...
============================================================
1. HTTP Request
   node  : HTTP Request
   class : FastAPI
   method: -
   file  : backend/app/main.py
↓
2. Router
   node  : Router
   class : health.py
   method: health()
   file  : backend/app/api/health.py
↓
3. Controller File
   node  : Entering File
   class : health.py
   method: health()
   file  : backend/app/api/health.py
↓
4. Controller Method
   node  : Controller Method
   class : health.py
   method: health()
   file  : backend/app/api/health.py
↓
5. Return
   node  : Schema(Response Model)
   class : HealthResponse
   method: model_construct()
   file  : backend/app/schemas/health.py
↓
6. Schema File
   node  : Entering Schema File
   class : HealthResponse
   method: model_construct()
   file  : backend/app/schemas/health.py
↓
7. Schema
   node  : Schema
   class : HealthResponse
   method: model_construct()
   file  : backend/app/schemas/health.py
↓
8. HTTP Response
   node  : HTTP Response
   class : FastAPI
   method: -
   file  : backend/app/main.py
============================================================
END TRACE
```

`POST /api/tasks` 的顺序同样遵守这个规则，只是后台任务会继续把 Service、Repository、Workflow、Provider、Report 的链路打印完，最后才收口到 `HTTP Response`：

```text
Swagger Execute
↓
HTTP Request
↓
Router
↓
Controller File
↓
Controller Method
↓
Entering File
↓
Service
↓
Entering File
↓
Repository
↓
Entering File
↓
Workflow
↓
Entering File
↓
Provider
↓
Entering File
↓
Repository
↓
Entering File
↓
Return
↓
Schema File
↓
Schema
↓
TaskCreateResponse
↓
后台任务继续打印
↓
Entering File
↓
Service
↓
Entering File
↓
Repository
↓
Repository
↓
Entering File
↓
Workflow
↓
Entering File
↓
Workflow
↓
Entering File
↓
Provider
↓
Entering File
↓
Provider
↓
Entering File
↓
Workflow
↓
Entering File
↓
Repository
↓
Entering File
↓
Repository
↓
HTTP Response
```

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

统一观察时，重点不是“某一行日志长什么样”，而是“同一次请求在后端内部有没有按顺序走完整条链路”。

| 后台日志观察项                               | 为什么看                       | 正常意味着什么                           |
| -------------------------------------------- | ------------------------------ | ---------------------------------------- |
| `request_id`                               | 关联一次完整请求               | 同一次请求所有日志拥有相同`request_id` |
| `learning_trace.enter`                     | 请求开始                       | Learning Trace 已开启                    |
| `HTTP Request`                             | 请求进入 FastAPI               | 请求成功进入应用                         |
| `Router`                                   | 是否进入 Router                | 路由匹配成功                             |
| `Controller File` / `Entering File`      | 是否进入控制器文件或业务文件   | 已进入对应 Python 文件                   |
| `Controller Method`                        | 是否进入控制器方法             | 路由方法已开始阅读                       |
| `Service`                                  | 是否进入业务层                 | 开始执行业务逻辑                         |
| `Workflow`                                 | 是否进入工作流                 | Workflow 正常执行（存在时）              |
| `Provider`                                 | 是否调用 Provider              | 数据来源开始执行（存在时）               |
| `Repository`                               | 是否访问 Repository            | 已进入数据访问层（存在时）               |
| `Schema File` / `Schema(Response Model)` | 是否进入返回模型文件并构造对象 | Response Model 创建成功                  |
| `HTTP Response`                            | 请求结束                       | 返回状态码正常                           |
| `learning_trace.exit`                      | Trace 结束                     | 整个调用链完成                           |
| `duration_ms`                              | 性能分析                       | 接口耗时                                 |
| `error_code`                               | 是否异常                       | `null` 表示正常                        |

## 学习建议

第一次学习一个接口：

① Execute

② 看 Swagger Response

③ 看后台 Learning Trace

④ 看 Router

⑤ 看 Service

⑥ 看 Workflow（如果有）

⑦ 看 Provider（如果有）

⑧ 看 Repository（如果有）

⑨ 看 Response Model

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
HTTP Request
↓
backend/app/api/health.py
Router
↓
Controller File
↓
Controller Method
↓
health()
↓
Return
↓
backend/app/schemas/health.py
Schema File
↓
Schema
↓
HealthResponse
↓
HTTP Response
```

## 02. POST /api/tasks

| 项目                 | 内容                                                                                                                                              |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| 接口作用             | 创建任务，启动主业务链路                                                                                                                          |
| 为什么先学习         | 后续状态、SSE、报告都依赖`task_id`                                                                                                              |
| Swagger 操作         | 打开`POST /api/tasks` → `Try it out` → 输入 `question`、`mode` → `Execute`                                                           |
| 输入（入力）         | `question`、`mode`                                                                                                                            |
| 预想结果（予想結果） | HTTP`202`，返回 `task_id` 和 `status=queued`                                                                                                |
| 后台日志观察         | `request_id`、`task_id`、`queued`、后续任务推进日志                                                                                         |
| 对应测试             | `backend/tests/test_api.py`                                                                                                                     |
| 对应源码             | `backend/app/api/tasks.py`、`backend/app/services/task_service.py`、`backend/app/repositories/implementations/in_memory/task_repository.py` |
| 下一步               | `GET /api/tasks/{task_id}`                                                                                                                      |

### 程序调用流程

```text
Swagger UI
↓
HTTP Request
↓
backend/app/api/tasks.py
Router
↓
Controller File
↓
Controller Method
↓
create_task()
↓
backend/app/services/task_service.py
Entering File
↓
Service
↓
TaskService.create_task()
↓
backend/app/repositories/implementations/in_memory/task_repository.py
Entering File
↓
Repository
↓
InMemoryTaskRepository.create()
↓
backend/app/workflow/graph.py
Entering File
↓
Workflow
↓
AnalysisWorkflow.stream()
↓
backend/app/kpi/workflow.py
Entering File
↓
backend/app/agents/providers/static_research.py
Entering File
↓
backend/app/reports/generator.py
Entering File
↓
backend/app/schemas/task_api.py
Return
↓
Schema File
↓
Schema
↓
TaskCreateResponse
↓
后台任务继续打印
↓
Entering File
↓
Service
↓
Entering File
↓
Repository
↓
Repository
↓
Entering File
↓
Workflow
↓
Entering File
↓
Workflow
↓
Entering File
↓
Provider
↓
Entering File
↓
Provider
↓
Entering File
↓
Workflow
↓
Entering File
↓
Repository
↓
Entering File
↓
Repository
↓
HTTP Response
```

## 03. GET /api/tasks/

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

## 04. GET /api/tasks//events

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

## 05. GET /api/tasks//report

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

## 06. POST /api/v1/documents

| 项目                 | 内容                                                                                                                                                                 |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 接口作用             | 上传文件和 metadata，创建文档记录                                                                                                                                    |
| 为什么先学习         | 上传是 import、chunk、retrieval、internal RAG 的入口                                                                                                                 |
| Swagger 操作         | 打开`POST /api/v1/documents` → `Try it out` → 选择文件并填写 `metadata` → `Execute`                                                                       |
| 输入（入力）         | `file`、`metadata`                                                                                                                                               |
| 预想结果（予想結果） | HTTP`201`，返回 `document_id` 和上传后状态                                                                                                                       |
| 后台日志观察         | 文件名、checksum、去重、状态变化、`document_id`                                                                                                                    |
| 对应测试             | `backend/tests/test_document_upload_api.py`                                                                                                                        |
| 对应源码             | `backend/app/api/documents.py`、`backend/app/services/document_upload_service.py`、`backend/app/repositories/implementations/in_memory/document_repository.py` |
| 下一步               | `GET /api/v1/documents`                                                                                                                                            |

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

## 07. GET /api/v1/documents

| 项目                 | 内容                                                                                                                                                               |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 接口作用             | 读取文档列表并支持基础过滤                                                                                                                                         |
| 为什么先学习         | 验证上传结果是否入库，理解默认过滤逻辑                                                                                                                             |
| Swagger 操作         | 打开`GET /api/v1/documents` → `Try it out` → 可选填写过滤条件 → `Execute`                                                                                 |
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
