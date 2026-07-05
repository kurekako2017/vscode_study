# 接口学习走读

这份文档是面向学习者的分接口学习文档，不是接口总表，也不是 Swagger 截图汇总。目标是把每个接口的作用、为什么先学、怎么在 Swagger 操作、输入输出、后台日志观察点、程序调用流程、对应测试和对应源码分开讲清楚。

## 先认识三个入口

### Swagger 是什么

Swagger 是 FastAPI 自动生成的 API 调试与验证工具。

- 它不是测试环境。
- 它不是正式 UI。
- 它是 API 调试与验证工具。
- 当前阶段主要用它验证后端骨架、接口合同和主链路。
- UI 完成以后，Swagger 通常仍然保留，因为联调和排错很快。
- Swagger 和 React 调用的是同一套 FastAPI API。

### ReDoc 是什么

ReDoc 更适合阅读接口结构、字段说明和响应模型。它偏“看文档”，不是偏“点接口”。

### OpenAPI JSON 是什么

OpenAPI JSON 是机器可读接口定义。它适合确认路径、Schema、字段是否真的注册到应用里。

## 企业项目验证体系

Swagger（FastAPI 自动生成的 API 调试与验证工具）

项目验证体系分四层：

| 层级 | 工具 | 目的 |
|---|---|---|
| 单元测试（Unit Test） | python -m unittest | 验证单个模块或类的逻辑是否正确 |
| 接口验证（API Verification） | Swagger UI (/docs) | 手工验证 API 请求、响应和业务流程 |
| 前后端集成测试（Integration Test） | React + FastAPI | 验证完整用户操作流程 |
| 端到端测试（E2E Test） | Playwright / Cypress | 模拟真实用户完成整个业务流程 |

补充说明：

- Swagger 不是测试环境。
- Swagger 不是正式 UI。
- Swagger 是 API 调试与验证工具。
- UI 完成以后 Swagger 通常仍然保留。
- Swagger 和 React 调用的是同一套 FastAPI API。
- 当前阶段主要用 Swagger 验证后端骨架。
- UI 完成后再做前后端 Integration Test。
- 发布前再考虑 E2E Test。

## 学习顺序

```text
GET /health
→ POST /api/tasks
→ GET /api/tasks/{task_id}
→ GET /api/tasks/{task_id}/events
→ GET /api/tasks/{task_id}/report
→ documents 系列
→ retrieval / internal-rag
→ approval / security / audit
```

## 01. GET /health：确认后端是否启动

### 接口作用

这个接口用来确认 FastAPI 应用是否真的启动成功，并返回当前服务的基础状态信息。

### 为什么先学习它

因为它没有业务前置条件，也不依赖任务、文档或审批数据。先把它跑通，才能确认后面的学习不是建立在错误环境上。

### Swagger 如何操作

1. 打开 `/docs`
2. 展开 `GET /health`
3. 点击 `Try it out`
4. 点击 `Execute`

### 输入（入力）

无。

### 预想结果（予想結果）

- HTTP `200`
- 返回 `status=ok`
- 返回 `service=retail-insight-ai`
- 返回 `provider=static`
- 返回非空 `request_id`

### 后台日志观察点

重点看是否出现健康检查请求日志，以及 `request_id` 是否已经进入结构化日志。

### 程序调用流程

```text
Swagger
→ FastAPI Router
→ Health Handler
→ Response
```

### 对应测试文件

`backend/tests/test_api.py`

### 对应源码

`backend/app/main.py`
`backend/app/api/health.py`
`backend/app/schemas/health_api.py`

### 成功后下一步

继续学习 `POST /api/tasks`，进入主业务链路。

## 02. POST /api/tasks：创建一个分析任务

### 接口作用

这个接口负责接收问题和模式，创建任务，并把后续执行交给任务服务和工作流处理。

### 为什么先学习它

因为任务是主链路入口。状态查询、SSE 事件、报告读取都依赖它返回的 `task_id`。

### Swagger 如何操作

1. 打开 `/docs`
2. 展开 `POST /api/tasks`
3. 点击 `Try it out`
4. 输入 `question` 和 `mode`
5. 点击 `Execute`

### 输入（入力）

- `question`
- `mode`

### 预想结果（予想結果）

- HTTP `202`
- 返回 `task_id`
- 返回 `status=queued`

### 后台日志观察点

重点看 `request_id`、`task_id`、`queued` 状态，以及后续是否有任务推进日志。

### 程序调用流程

```text
Swagger
→ FastAPI Router
→ Task API
→ TaskService
→ Workflow
→ Response
```

### 对应测试文件

`backend/tests/test_api.py`

### 对应源码

`backend/app/api/tasks.py`
`backend/app/services/task_service.py`
`backend/app/workflow/`
`backend/app/schemas/task_api.py`

### 成功后下一步

继续学习 `GET /api/tasks/{task_id}`，确认任务状态是否推进。

## 03. GET /api/tasks/{task_id}：查看任务状态

### 接口作用

这个接口负责按 `task_id` 读取任务快照，让你知道任务当前在 `queued`、`running`、`completed` 还是 `failed`。

### 为什么先学习它

创建完任务以后，先确认状态是否能被读取，比先看 SSE 更容易理解任务生命周期。

### Swagger 如何操作

1. 打开 `/docs`
2. 展开 `GET /api/tasks/{task_id}`
3. 点击 `Try it out`
4. 填入刚才拿到的 `task_id`
5. 点击 `Execute`

### 输入（入力）

- `task_id`

### 预想结果（予想結果）

- HTTP `200`
- 返回任务对象
- `status` 可能是 `queued`、`running`、`completed`、`failed`

### 后台日志观察点

重点看同一个 `task_id` 的状态推进，以及是否出现读取任务快照的日志。

### 程序调用流程

```text
Swagger
→ FastAPI Router
→ Task API
→ TaskService
→ Task Repository
→ Response
```

### 对应测试文件

`backend/tests/test_api.py`

### 对应源码

`backend/app/api/tasks.py`
`backend/app/services/task_service.py`

### 成功后下一步

继续学习 `GET /api/tasks/{task_id}/events`，观察实时事件流。

## 04. GET /api/tasks/{task_id}/events：订阅任务事件

### 接口作用

这个接口通过 `SSE` 推送任务过程中的状态事件，让你看到任务不是一下子完成，而是逐步推进。

### 为什么先学习它

因为它最能体现这个项目不是同步短请求，而是带进度推送的长任务链路。

### Swagger 如何操作

1. 打开 `/docs`
2. 展开 `GET /api/tasks/{task_id}/events`
3. 点击 `Try it out`
4. 填入 `task_id`
5. 点击 `Execute`

### 输入（入力）

- `task_id`

### 预想结果（予想結果）

- HTTP `200`
- 持续返回 `text/event-stream`
- 可看到 `status`、`done` 或 `error` 事件

### 后台日志观察点

重点看事件推送日志、事件名称、任务状态和连接生命周期。

### 程序调用流程

```text
Swagger / Client
→ FastAPI Router
→ SSE Endpoint
→ Event Publisher
→ Response Stream
```

### 对应测试文件

`backend/tests/test_api.py`

### 对应源码

`backend/app/api/tasks.py`
`backend/app/events/sse.py`
`backend/app/events/publisher.py`

### 成功后下一步

继续学习 `GET /api/tasks/{task_id}/report`，确认最终产物能否被读取。

## 05. GET /api/tasks/{task_id}/report：读取最终报告

### 接口作用

这个接口负责根据 `task_id` 读取最终生成的报告结果，通常是主任务链路的终点。

### 为什么先学习它

因为任务最终不是为了“状态变化”，而是为了“拿到报告”。所以要确认结果是否真实保存和可读取。

### Swagger 如何操作

1. 打开 `/docs`
2. 展开 `GET /api/tasks/{task_id}/report`
3. 点击 `Try it out`
4. 填入 `task_id`
5. 点击 `Execute`

### 输入（入力）

- `task_id`

### 预想结果（予想結果）

- HTTP `200`
- 返回 `status=generated`
- 返回 Markdown 报告内容

### 后台日志观察点

重点看报告生成完成日志、报告读取日志，以及是否存在 `report_not_found` 类失败线索。

### 程序调用流程

```text
Swagger
→ FastAPI Router
→ Task API
→ TaskService
→ Report Repository
→ Response
```

### 对应测试文件

`backend/tests/test_api.py`

### 对应源码

`backend/app/api/tasks.py`
`backend/app/services/task_service.py`
`backend/app/reports/generator.py`

### 成功后下一步

开始学习文档链路，从 `POST /api/v1/documents` 进入。

## 06. POST /api/v1/documents：上传文档

### 接口作用

这个接口负责接收上传文件和 `metadata`，创建一条新的文档记录，是文档处理链路的入口。

### 为什么先学习它

因为导入、切分、检索、Internal RAG 都依赖先有文档，上传是文档域最前面的入口。

### Swagger 如何操作

1. 打开 `/docs`
2. 展开 `POST /api/v1/documents`
3. 点击 `Try it out`
4. 选择文件并填写 `metadata`
5. 点击 `Execute`

### 输入（入力）

- `file`
- `metadata`

### 预想结果（予想結果）

- HTTP `201`
- 返回 `document_id`
- 返回上传后的文档状态

### 后台日志观察点

重点看文件名、checksum、去重判断、文档状态和 `document_id`。

### 程序调用流程

```text
Swagger
→ FastAPI Router
→ Documents API
→ DocumentUploadService
→ Document Repository
→ Response
```

### 对应测试文件

`backend/tests/test_document_upload_api.py`

### 对应源码

`backend/app/api/documents.py`
`backend/app/services/document_upload_service.py`

### 成功后下一步

继续学习 `GET /api/v1/documents`，确认上传结果是否真的可见。

## 07. GET /api/v1/documents：查看文档列表

### 接口作用

这个接口负责读取文档列表，并支持基础过滤，是理解仓库中有哪些文档的最直接入口。

### 为什么先学习它

因为它能立即验证上传是否落库，也能帮助你理解默认过滤逻辑，比如 archived 是否默认排除。

### Swagger 如何操作

1. 打开 `/docs`
2. 展开 `GET /api/v1/documents`
3. 点击 `Try it out`
4. 可选填写过滤参数
5. 点击 `Execute`

### 输入（入力）

- `status`
- `document_type`
- `language`
- `tag`
- `owner`

### 预想结果（予想結果）

- HTTP `200`
- 返回文档列表
- 默认不含 archived 文档

### 后台日志观察点

重点看过滤条件、命中文档数量，以及默认排除 archived 的行为。

### 程序调用流程

```text
Swagger
→ FastAPI Router
→ Documents API
→ DocumentReadService
→ Document Repository
→ Response
```

### 对应测试文件

`backend/tests/test_document_read_api.py`

### 对应源码

`backend/app/api/documents.py`
`backend/app/services/document_read_service.py`

### 成功后下一步

继续学习 `GET /api/v1/documents/{document_id}`。

## 08. GET /api/v1/documents/{document_id}：查看单个文档详情

### 接口作用

这个接口负责读取单个文档的完整详情，让你看到文档对象的关键字段和当前状态。

### 为什么先学习它

因为列表只告诉你“有这条数据”，详情接口才能让你理解领域对象长什么样。

### Swagger 如何操作

1. 打开 `/docs`
2. 展开 `GET /api/v1/documents/{document_id}`
3. 点击 `Try it out`
4. 填入 `document_id`
5. 点击 `Execute`

### 输入（入力）

- `document_id`

### 预想结果（予想結果）

- HTTP `200`
- 返回单个文档详情
- 不存在时返回 `document_not_found`

### 后台日志观察点

重点看文档命中日志、缺失日志和响应中字段是否齐全。

### 程序调用流程

```text
Swagger
→ FastAPI Router
→ Documents API
→ DocumentReadService
→ Document Repository
→ Response
```

### 对应测试文件

`backend/tests/test_document_read_api.py`

### 对应源码

`backend/app/api/documents.py`
`backend/app/services/document_read_service.py`

### 成功后下一步

继续学习 `DELETE /api/v1/documents/{document_id}`，理解归档语义。

## 09. DELETE /api/v1/documents/{document_id}：归档文档

### 接口作用

这个接口负责把文档归档，而不是物理删除。它体现的是“软删除、可追溯”的企业语义。

### 为什么先学习它

因为很多学习者会把删除理解成“直接没了”，但这里设计的是 archive 语义，适合企业审计和恢复场景。

### Swagger 如何操作

1. 打开 `/docs`
2. 展开 `DELETE /api/v1/documents/{document_id}`
3. 点击 `Try it out`
4. 填入 `document_id`
5. 点击 `Execute`

### 输入（入力）

- `document_id`

### 预想结果（予想結果）

- HTTP `200`
- 返回归档后的文档信息
- 列表接口默认不再显示该文档

### 后台日志观察点

重点看归档状态变化、归档前后列表差异、不可重复删除等边界。

### 程序调用流程

```text
Swagger
→ FastAPI Router
→ Document Archive API
→ DocumentArchiveService
→ Document Repository
→ Response
```

### 对应测试文件

`backend/tests/test_document_archive_api.py`

### 对应源码

`backend/app/api/documents.py`
`backend/app/services/document_archive_service.py`

### 成功后下一步

继续学习 `POST /api/v1/documents/{document_id}/import`。

## 10. POST /api/v1/documents/{document_id}/import：导入文档

### 接口作用

这个接口负责启动文档导入流程，把上传后的原始文件推进到可验证、可后续处理的状态。

### 为什么先学习它

因为文档上传完成并不等于可检索。导入阶段决定文件是否能被系统接受并进入后续处理。

### Swagger 如何操作

1. 打开 `/docs`
2. 展开 `POST /api/v1/documents/{document_id}/import`
3. 点击 `Try it out`
4. 填入 `document_id`
5. 点击 `Execute`

### 输入（入力）

- `document_id`
- 可选导入参数

### 预想结果（予想結果）

- HTTP `202` 或 `200`
- 返回导入结果
- 文档状态向 `validated` 等后续状态推进

### 后台日志观察点

重点看导入状态推进、失败原因、文档类型支持与否。

### 程序调用流程

```text
Swagger
→ FastAPI Router
→ Document Import API
→ DocumentImportService
→ Document Repository
→ Response
```

### 对应测试文件

`backend/tests/test_document_import_api.py`

### 对应源码

`backend/app/api/document_imports.py`
`backend/app/services/document_import_service.py`

### 成功后下一步

继续学习 `POST /api/v1/documents/{document_id}/chunks`。

## 11. POST /api/v1/documents/{document_id}/chunks：切分文档

### 接口作用

这个接口负责把已导入文档切成 chunk，为后续检索和 Internal RAG 提供最小可检索单元。

### 为什么先学习它

因为 Retrieval 不是直接读整篇文档，而是依赖 chunk。理解切分，就能理解后面的来源追踪和 citation。

### Swagger 如何操作

1. 打开 `/docs`
2. 展开 `POST /api/v1/documents/{document_id}/chunks`
3. 点击 `Try it out`
4. 填入 `document_id`
5. 点击 `Execute`

### 输入（入力）

- `document_id`
- 可选切分参数

### 预想结果（予想結果）

- HTTP `200`
- 返回 chunk 结果或 chunk 数量
- 每个 chunk 有稳定顺序和元数据

### 后台日志观察点

重点看 chunk 数量、`chunk_index`、切分策略和替换行为。

### 程序调用流程

```text
Swagger
→ FastAPI Router
→ Document Chunk API
→ DocumentChunkService
→ Chunk Repository
→ Response
```

### 对应测试文件

`backend/tests/test_document_chunk_api.py`

### 对应源码

`backend/app/api/document_chunks.py`
`backend/app/services/document_chunk_service.py`

### 成功后下一步

继续学习 `GET /api/v1/documents/{document_id}/chunks`。

## 12. GET /api/v1/documents/{document_id}/chunks：读取 chunk 列表

### 接口作用

这个接口负责把已经切好的 chunk 读出来，让你确认切分结果真的被保存并可再次读取。

### 为什么先学习它

因为“写入成功”和“可再次读取”是两件事。企业系统必须验证这两个动作都成立。

### Swagger 如何操作

1. 打开 `/docs`
2. 展开 `GET /api/v1/documents/{document_id}/chunks`
3. 点击 `Try it out`
4. 填入 `document_id`
5. 点击 `Execute`

### 输入（入力）

- `document_id`

### 预想结果（予想結果）

- HTTP `200`
- 返回 chunk 列表
- 列出 `chunk_id`、`chunk_index`、内容片段和元数据

### 后台日志观察点

重点看 chunk 读取数量、空结果情况、读取与写入是否一致。

### 程序调用流程

```text
Swagger
→ FastAPI Router
→ Document Chunk API
→ DocumentChunkService
→ Chunk Repository
→ Response
```

### 对应测试文件

`backend/tests/test_document_chunk_api.py`

### 对应源码

`backend/app/api/document_chunks.py`
`backend/app/services/document_chunk_service.py`

### 成功后下一步

继续学习 `POST /api/v1/document-retrieval/search`。

## 13. POST /api/v1/document-retrieval/search：检索文档片段

### 接口作用

这个接口负责基于 query 和过滤条件，从 chunk 集合里选出相关片段，是 Internal RAG 的上游输入。

### 为什么先学习它

因为答案不是“凭空生成”的。先看检索结果，才能理解后面的答案和 citation 从哪里来。

### Swagger 如何操作

1. 打开 `/docs`
2. 展开 `POST /api/v1/document-retrieval/search`
3. 点击 `Try it out`
4. 输入 `query` 和过滤条件
5. 点击 `Execute`

### 输入（入力）

- `query`
- `limit`
- `include_archived`
- `document_type`
- `language`
- `tags`

### 预想结果（予想結果）

- HTTP `200`
- 返回命中的 chunk 列表
- 每条结果带 `score`、来源和元数据

### 后台日志观察点

重点看 query、过滤条件、命中 chunk、archived 排除逻辑和排序结果。

### 程序调用流程

```text
Swagger
→ FastAPI Router
→ Document Retrieval API
→ DocumentRetrievalService
→ Retrieval Provider
→ Response
```

### 对应测试文件

`backend/tests/test_document_retrieval_api.py`

### 对应源码

`backend/app/api/document_retrieval.py`
`backend/app/services/document_retrieval_service.py`

### 成功后下一步

继续学习 `POST /api/v1/internal-rag/answer`。

## 14. POST /api/v1/internal-rag/answer：生成内部问答结果

### 接口作用

这个接口负责把检索结果组装成确定性答案，并附上 citation、confidence 和 warning。

### 为什么先学习它

因为它能体现“当前还没接真实 LLM，但已经具备可解释内部问答骨架”的设计思路。

### Swagger 如何操作

1. 打开 `/docs`
2. 展开 `POST /api/v1/internal-rag/answer`
3. 点击 `Try it out`
4. 输入 `question` 和检索参数
5. 点击 `Execute`

### 输入（入力）

- `question`
- `limit`
- `include_archived`
- `document_type`
- `language`
- `tags`
- `answer_mode`
- `require_citations`

### 预想结果（予想結果）

- HTTP `200`
- 返回 `answer`
- 返回 `citations`
- 返回 `confidence`
- 返回 `warnings`

### 后台日志观察点

重点看 retrieval 是否成功、citation 是否齐全、是否回退 deterministic 路径、warning 为何产生。

### 程序调用流程

```text
Swagger
→ FastAPI Router
→ Internal RAG API
→ InternalRAGService
→ Retrieval Provider
→ Answer Assembly
→ Response
```

### 对应测试文件

`backend/tests/test_internal_rag_api.py`
`backend/tests/test_internal_rag_evaluation.py`
`backend/tests/test_rag_answer_generator.py`

### 对应源码

`backend/app/api/internal_rag.py`
`backend/app/services/internal_rag_service.py`

### 成功后下一步

继续学习审批入口 `POST /api/v1/reports/{task_id}/submit-approval`。

## 15. POST /api/v1/reports/{task_id}/submit-approval：提交审批

### 接口作用

这个接口负责把某个任务产出的报告送入审批流，建立审批请求记录。

### 为什么先学习它

因为它是“分析结果进入治理流程”的边界，代表系统开始从“生成结果”走向“受控发布”。

### Swagger 如何操作

1. 打开 `/docs`
2. 展开 `POST /api/v1/reports/{task_id}/submit-approval`
3. 点击 `Try it out`
4. 填入 `task_id`
5. 点击 `Execute`

### 输入（入力）

- `task_id`

### 预想结果（予想結果）

- HTTP `200`
- 返回审批请求对象
- 返回 `approval_id` 或审批状态

### 后台日志观察点

重点看审批创建日志、RBAC 检查日志、关联报告版本信息。

### 程序调用流程

```text
Swagger
→ FastAPI Router
→ Approvals API
→ ApprovalService
→ Approval Repository
→ Response
```

### 对应测试文件

`backend/tests/test_approval_api.py`
`backend/tests/test_rbac_guard.py`

### 对应源码

`backend/app/api/approvals.py`
`backend/app/services/approval_service.py`

### 成功后下一步

继续学习 `GET /api/v1/approvals`。

## 16. GET /api/v1/approvals：查看审批列表

### 接口作用

这个接口负责按集合方式查看审批请求，是理解审批工作量和状态分布的入口。

### 为什么先学习它

因为先看列表再看详情，更容易建立“审批对象是独立资源”的概念。

### Swagger 如何操作

1. 打开 `/docs`
2. 展开 `GET /api/v1/approvals`
3. 点击 `Try it out`
4. 可选填写过滤条件
5. 点击 `Execute`

### 输入（入力）

- 可选过滤参数

### 预想结果（予想結果）

- HTTP `200`
- 返回审批列表
- 每条记录带基础状态和关联信息

### 后台日志观察点

重点看列表过滤、RBAC 检查、审批数量和状态分布。

### 程序调用流程

```text
Swagger
→ FastAPI Router
→ Approvals API
→ ApprovalService
→ Approval Repository
→ Response
```

### 对应测试文件

`backend/tests/test_approval_api.py`

### 对应源码

`backend/app/api/approvals.py`
`backend/app/services/approval_service.py`

### 成功后下一步

继续学习 `GET /api/v1/approvals/{approval_id}`。

## 17. GET /api/v1/approvals/{approval_id}：查看审批详情

### 接口作用

这个接口负责查看单个审批记录的完整信息，包括当前状态、动作历史和关联对象。

### 为什么先学习它

因为审批列表只解决“有哪些”，详情接口才真正解释“这张审批单现在处于什么阶段”。

### Swagger 如何操作

1. 打开 `/docs`
2. 展开 `GET /api/v1/approvals/{approval_id}`
3. 点击 `Try it out`
4. 填入 `approval_id`
5. 点击 `Execute`

### 输入（入力）

- `approval_id`

### 预想结果（予想結果）

- HTTP `200`
- 返回审批详情
- 返回状态、版本、事件或审批人信息

### 后台日志观察点

重点看详情读取、状态机位置、RBAC 检查和不存在时的错误分支。

### 程序调用流程

```text
Swagger
→ FastAPI Router
→ Approvals API
→ ApprovalService
→ Approval Repository
→ Response
```

### 对应测试文件

`backend/tests/test_approval_api.py`

### 对应源码

`backend/app/api/approvals.py`
`backend/app/services/approval_service.py`

### 成功后下一步

继续学习 `POST /api/v1/approvals/{approval_id}/approve`。

## 18. POST /api/v1/approvals/{approval_id}/approve：批准审批

### 接口作用

这个接口负责把审批记录推进到批准状态，是审批状态机里的正向动作。

### 为什么先学习它

因为它最能体现“状态推进 + 权限检查 + 审计记录”三件事是一起发生的。

### Swagger 如何操作

1. 打开 `/docs`
2. 展开 `POST /api/v1/approvals/{approval_id}/approve`
3. 点击 `Try it out`
4. 填入 `approval_id`
5. 点击 `Execute`

### 输入（入力）

- `approval_id`

### 预想结果（予想結果）

- HTTP `200`
- 返回 `approved`
- 返回更新后的审批状态

### 后台日志观察点

重点看 `approval.approve` 权限检查、审计写入、状态变化和版本边界。

### 程序调用流程

```text
Swagger
→ FastAPI Router
→ Approvals API
→ ApprovalService
→ Audit / Repository
→ Response
```

### 对应测试文件

`backend/tests/test_approval_api.py`
`backend/tests/test_rbac_guard.py`
`backend/tests/test_audit_middleware.py`

### 对应源码

`backend/app/api/approvals.py`
`backend/app/services/approval_service.py`
`backend/app/services/audit_service.py`

### 成功后下一步

继续学习 `POST /api/v1/approvals/{approval_id}/reject`。

## 19. POST /api/v1/approvals/{approval_id}/reject：拒绝审批

### 接口作用

这个接口负责把审批记录推进到拒绝状态，是审批状态机中的负向动作。

### 为什么先学习它

因为企业项目不能只验证 happy path，还要验证拒绝、回退和失败原因记录。

### Swagger 如何操作

1. 打开 `/docs`
2. 展开 `POST /api/v1/approvals/{approval_id}/reject`
3. 点击 `Try it out`
4. 填入 `approval_id`
5. 点击 `Execute`

### 输入（入力）

- `approval_id`

### 预想结果（予想結果）

- HTTP `200`
- 返回 `rejected`
- 返回更新后的审批状态

### 后台日志观察点

重点看拒绝动作、RBAC 检查、审计日志和拒绝后状态是否稳定。

### 程序调用流程

```text
Swagger
→ FastAPI Router
→ Approvals API
→ ApprovalService
→ Audit / Repository
→ Response
```

### 对应测试文件

`backend/tests/test_approval_api.py`
`backend/tests/test_rbac_guard.py`
`backend/tests/test_audit_middleware.py`

### 对应源码

`backend/app/api/approvals.py`
`backend/app/services/approval_service.py`
`backend/app/services/audit_service.py`

### 成功后下一步

进入安全读模型，从 `GET /api/v1/users/me` 开始。

## 20. GET /api/v1/users/me：查看当前用户

### 接口作用

这个接口负责返回当前用户占位主体，是未来真实认证接入前的最小读接口。

### 为什么先学习它

因为它能帮助你理解当前阶段没有真实登录，但已经为认证接入保留了边界。

### Swagger 如何操作

1. 打开 `/docs`
2. 展开 `GET /api/v1/users/me`
3. 点击 `Try it out`
4. 点击 `Execute`

### 输入（入力）

无。

### 预想结果（予想結果）

- HTTP `200`
- 返回当前用户对象
- 当前通常为 `user_id=system`

### 后台日志观察点

重点看 current user 解析日志、`request_id` 和安全读模型是否正常。

### 程序调用流程

```text
Swagger
→ FastAPI Router
→ Security API
→ SecurityService
→ Response
```

### 对应测试文件

`backend/tests/test_security_audit_api.py`

### 对应源码

`backend/app/api/security.py`
`backend/app/services/security_service.py`

### 成功后下一步

继续学习 `GET /api/v1/security/roles`。

## 21. GET /api/v1/security/roles：查看角色目录

### 接口作用

这个接口负责读取冻结的角色目录，帮助你理解 RBAC 里“角色”这一层的定义方式。

### 为什么先学习它

因为很多人先看权限名会混乱，先看角色再看权限更容易理解层级关系。

### Swagger 如何操作

1. 打开 `/docs`
2. 展开 `GET /api/v1/security/roles`
3. 点击 `Try it out`
4. 点击 `Execute`

### 输入（入力）

无。

### 预想结果（予想結果）

- HTTP `200`
- 返回角色列表
- 每个角色带名称和权限关系

### 后台日志观察点

重点看角色目录读取、静态目录初始化和响应结构是否稳定。

### 程序调用流程

```text
Swagger
→ FastAPI Router
→ Security API
→ SecurityService
→ Response
```

### 对应测试文件

`backend/tests/test_security_audit_api.py`

### 对应源码

`backend/app/api/security.py`
`backend/app/services/security_service.py`

### 成功后下一步

继续学习 `GET /api/v1/security/permissions`。

## 22. GET /api/v1/security/permissions：查看权限目录

### 接口作用

这个接口负责读取冻结的权限目录，用来说明当前系统的动作粒度和权限命名方式。

### 为什么先学习它

因为审批 RBAC 的具体动作最终都落在权限名上，这个接口是理解审批鉴权的基础。

### Swagger 如何操作

1. 打开 `/docs`
2. 展开 `GET /api/v1/security/permissions`
3. 点击 `Try it out`
4. 点击 `Execute`

### 输入（入力）

无。

### 预想结果（予想結果）

- HTTP `200`
- 返回权限列表
- 权限命名稳定且可读

### 后台日志观察点

重点看权限目录读取、权限数量和权限命名是否与审批动作一致。

### 程序调用流程

```text
Swagger
→ FastAPI Router
→ Security API
→ SecurityService
→ Response
```

### 对应测试文件

`backend/tests/test_security_audit_api.py`

### 对应源码

`backend/app/api/security.py`
`backend/app/services/security_service.py`

### 成功后下一步

继续学习 `GET /api/v1/audit-logs`。

## 23. GET /api/v1/audit-logs：查看审计日志

### 接口作用

这个接口负责读取 append-only 审计日志，帮助你确认关键动作是否留下了可追踪事实。

### 为什么先学习它

因为企业项目除了“功能能不能跑”，还要解释“谁做了什么、什么时候做的、为什么被允许或拒绝”。

### Swagger 如何操作

1. 打开 `/docs`
2. 展开 `GET /api/v1/audit-logs`
3. 点击 `Try it out`
4. 可选填写分页参数
5. 点击 `Execute`

### 输入（入力）

- 可选分页参数

### 预想结果（予想結果）

- HTTP `200`
- 返回审计日志列表
- 当前 `next_cursor` 可能为空

### 后台日志观察点

重点看 append-only 读取日志、审计事件名称、成功/失败事实是否都保留。

### 程序调用流程

```text
Swagger
→ FastAPI Router
→ Audit Logs API
→ AuditService
→ Audit Repository
→ Response
```

### 对应测试文件

`backend/tests/test_security_audit_api.py`
`backend/tests/test_audit_middleware.py`

### 对应源码

`backend/app/api/audit_logs.py`
`backend/app/services/audit_service.py`

### 成功后下一步

回到 `docs/TEST_CASES.md`，用测试文件反向验证这些接口和流程。

## 补充接口：POST /api/v1/reports/{task_id}/revise

这个接口属于审批链路里的“修订”动作。它不是本次要求的 23 个主学习接口之一，但属于现有审批能力的一部分，学习审批状态机时建议在看完 approve / reject 后再补看。它的代码入口在 `backend/app/api/approvals.py`，主要测试在 `backend/tests/test_approval_api.py`。
