# 接口学习走读

这份文档按 Swagger 的实际接口顺序组织，目标是让初学者按“看接口 - 点 Swagger - 试请求 - 看源码”的顺序把主链路跑通。

## 启动前

```bash
cd backend
python3 -c "from app.main import app; print(app.title)"
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

三者用途：

- Swagger: 适合点开接口、填参数、直接执行。
- ReDoc: 适合阅读接口说明和结构化字段。
- OpenAPI JSON: 适合确认路由、schema、返回字段确实已注册。

## 学习方式

1. 先看表中的“接口作用”和“为什么先学”。
2. 再按“Swagger 操作”真的点一次。
3. 再对照“预期输出”和“常见失败”判断请求是否成功。
4. 最后去“对应源码位置”看实现。

## 主链路接口

| 接口 | 接口作用 | 为什么先学这个接口 | Swagger 哪里点 | 输入（入力） | 预期输出（预想结果） | 成功后下一步 | 常见失败 | 对应源码位置 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `GET /health` | 确认 FastAPI 进程活着，并返回 `request_id` | 没有业务前置条件，最适合先验证环境 | Swagger 展开 `GET /health`，直接 `Execute` | 无 | `status=ok`、`service=retail-insight-ai`、`provider=static`、`request_id` 非空 | 去看 `POST /api/tasks` | 404、`Connection refused`、后端未启动 | `backend/app/main.py`、`backend/app/api/health.py`、`backend/app/schemas/health_api.py` |
| `POST /api/tasks` | 创建任务，启动主业务链路 | 后续状态、SSE、报告都从这里开始 | Swagger 展开 `POST /api/tasks`，填 `question` 和 `mode`，点 `Execute` | JSON：`question`、`mode` | HTTP 202，返回 `task_id` 和 `status=queued` | 去看 `GET /api/tasks/{task_id}` | `VALIDATION_ERROR`、422、`mode` 写错 | `backend/app/api/tasks.py`、`backend/app/services/task_service.py`、`backend/app/schemas/task_api.py` |
| `GET /api/tasks/{task_id}` | 查询任务当前状态 | 先确认任务是否真的进入队列和运行态 | Swagger 填 `task_id`，直接查询 | 路径参数 `task_id` | 返回 `queued`、`running`、`completed` 或 `failed` | 去看 `GET /api/tasks/{task_id}/events` | `task_id` 不存在、404、后端重启导致内存丢失 | `backend/app/api/tasks.py`、`backend/app/services/task_service.py` |
| `GET /api/tasks/{task_id}/report` | 读取最终报告 | 任务结束后要确认结果真的保存了 | Swagger 填 `task_id`，执行 GET | 路径参数 `task_id` | 返回 `status=generated` 和 `markdown` 报告 | 去看 `POST /api/v1/documents` | `REPORT_NOT_FOUND`、任务还没 done | `backend/app/api/tasks.py`、`backend/app/services/task_service.py`、`backend/app/reports/generator.py` |
| `POST /api/v1/documents` | 上传文档，建立文档源数据 | 文档链路的入口 | Swagger 展开 `POST /api/v1/documents`，选择文件，填 `metadata`，点 `Execute` | `multipart/form-data`：`file` + `metadata` | HTTP 201，返回 `document_id` | 去看 `GET /api/v1/documents` | 文件空、metadata 违法、`document_type` 错误 | `backend/app/api/documents.py`、`backend/app/services/document_upload_service.py`、`backend/app/schemas/document_api.py` |
| `GET /api/v1/documents` | 查看文档列表 | 先确认上传结果是否入库 | Swagger 展开 `GET /api/v1/documents`，可填过滤条件 | 可选 `status`、`document_type`、`language`、`tag`、`owner` | 返回文档列表，默认不含 archived | 去看 `GET /api/v1/documents/{document_id}` | 查询条件不对、列表为空、文档未上传 | `backend/app/api/documents.py`、`backend/app/services/document_read_service.py` |
| `GET /api/v1/documents/{document_id}` | 查看单个文档详情 | 先看单体记录，最容易理解领域对象 | Swagger 填 `document_id` | 路径参数 `document_id` | 返回文档详情；不存在时返回 `document_not_found` | 去看 `DELETE /api/v1/documents/{document_id}` | `document_id` 不存在、输入写错 | `backend/app/api/documents.py`、`backend/app/services/document_read_service.py` |
| `DELETE /api/v1/documents/{document_id}` | 归档文档，不做物理删除 | 理解软删除和可追溯性 | Swagger 填 `document_id` 执行 DELETE | 路径参数 `document_id` | 文档进入 archived，列表默认不再显示 | 去看 `POST /api/v1/documents/{document_id}/import` | 文档不存在、已归档后重复操作 | `backend/app/api/document_archive.py`、`backend/app/services/document_archive_service.py` |
| `POST /api/v1/documents/{document_id}/import` | 启动导入流程 | 导入是切分和检索之前的准备步骤 | Swagger 填 `document_id` 执行 POST | 路径参数 `document_id`，可选配置 | 返回导入结果，文档状态推进 | 去看 `POST /api/v1/documents/{document_id}/chunks` | 文档未找到、类型不支持、状态不对 | `backend/app/api/document_imports.py`、`backend/app/services/document_import_service.py` |
| `POST /api/v1/documents/{document_id}/chunks` | 把文档切成 chunk | Chunk 是 retrieval / RAG 的基础 | Swagger 填 `document_id` 执行 POST | 路径参数 `document_id`，可选切分策略 | 返回 chunk 列表或切分结果 | 去看 `GET /api/v1/documents/{document_id}/chunks` | 文档没导入、文档已归档、格式不支持 | `backend/app/api/document_chunks.py`、`backend/app/services/document_chunk_service.py` |
| `GET /api/v1/documents/{document_id}/chunks` | 读取 chunk 列表 | 先确认切分结果真的入库 | Swagger 填 `document_id` 执行 GET | 路径参数 `document_id` | 返回 chunk 列表和 chunk 元数据 | 去看 `POST /api/v1/document-retrieval/search` | chunk 还没生成、`document_id` 错误 | `backend/app/api/document_chunks.py`、`backend/app/services/document_chunk_service.py` |
| `POST /api/v1/document-retrieval/search` | 在本地 chunk 上检索 | 这是 internal RAG 的输入 | Swagger 填 `query` 和过滤条件执行 POST | `query`、`limit`、`include_archived`、`document_type`、`language`、`tags` | 返回检索结果、分数、来源信息 | 去看 `POST /api/v1/internal-rag/answer` | query 为空、过滤条件过严、无匹配 | `backend/app/api/document_retrieval.py`、`backend/app/services/document_retrieval_service.py` |
| `POST /api/v1/internal-rag/answer` | 基于检索结果生成确定性答案 | 把检索和答案组装串起来 | Swagger 填 `question` 和检索参数执行 POST | `question`、`limit`、`include_archived`、`document_type`、`language`、`tags`、`answer_mode`、`require_citations` | 返回 `answer`、`citations`、`retrieval_mode`、`answer_mode`、`confidence`、`warnings` | 去看 `POST /api/v1/reports/{task_id}/submit-approval` | `insufficient_context`、`invalid_question`、`citation_required` | `backend/app/api/internal_rag.py`、`backend/app/services/internal_rag_service.py` |
| `POST /api/v1/reports/{task_id}/submit-approval` | 提交报告审批 | 把报告和审批边界连起来 | Swagger 填 `task_id` 执行 POST | 路径参数 `task_id` | 返回审批请求或审批编号 | 去看 `GET /api/v1/approvals` | `task_id` 无报告、权限不足 | `backend/app/api/approvals.py`、`backend/app/services/approval_service.py` |
| `GET /api/v1/approvals` | 查看审批列表 | 先看集合，再看详情 | Swagger 直接 GET，可填过滤条件 | 可选过滤条件 | 返回审批列表和分页信息 | 去看 `GET /api/v1/approvals/{approval_id}` | 列表为空、RBAC 拒绝 | `backend/app/api/approvals.py`、`backend/app/services/approval_service.py` |
| `GET /api/v1/approvals/{approval_id}` | 查看审批详情 | 最适合看状态流转 | Swagger 填 `approval_id` 执行 GET | 路径参数 `approval_id` | 返回审批状态、事件和关联信息 | 去看 `POST /api/v1/approvals/{approval_id}/approve` | `approval_id` 错误、权限不足 | `backend/app/api/approvals.py`、`backend/app/services/approval_service.py` |
| `POST /api/v1/approvals/{approval_id}/approve` | 批准审批 | 最典型的正向动作 | Swagger 填 `approval_id` 执行 POST | 路径参数 `approval_id` | 返回 `approved` | 去看 `POST /api/v1/approvals/{approval_id}/reject` | 权限不足、状态不允许 | `backend/app/api/approvals.py`、`backend/app/services/approval_service.py` |
| `POST /api/v1/approvals/{approval_id}/reject` | 拒绝审批 | 了解失败路径和原因记录 | Swagger 填 `approval_id` 执行 POST | 路径参数 `approval_id` | 返回 `rejected` | 去看 `GET /api/v1/users/me` | 权限不足、状态不允许 | `backend/app/api/approvals.py`、`backend/app/services/approval_service.py` |
| `GET /api/v1/users/me` | 查看当前用户占位主体 | 未来认证接缝的最小读接口 | Swagger 直接 GET | 无 | 返回 `user_id=system` 的 placeholder principal | 去看 `GET /api/v1/security/roles` | 后端没启动、接口 404 | `backend/app/api/security.py`、`backend/app/services/security_service.py` |
| `GET /api/v1/security/roles` | 查看冻结角色目录 | 先理解 RBAC 的角色层 | Swagger 直接 GET | 无 | 返回静态角色目录 | 去看 `GET /api/v1/security/permissions` | 角色目录为空、后端未加载 | `backend/app/api/security.py`、`backend/app/services/security_service.py` |
| `GET /api/v1/security/permissions` | 查看冻结权限目录 | 理解 RBAC 的动作粒度 | Swagger 直接 GET | 无 | 返回静态权限目录 | 去看 `GET /api/v1/audit-logs` | 权限目录为空、后端未加载 | `backend/app/api/security.py`、`backend/app/services/security_service.py` |
| `GET /api/v1/audit-logs` | 查看追加式审计记录 | 看谁做了什么是否被保存 | Swagger 直接 GET，可填分页参数 | 可选分页参数 | 返回审计记录列表，`next_cursor` 当前为 `null` | 回看 `docs/TEST_CASES.md` 和 `docs/INTERVIEW_GUIDE.md` | 没有审计数据、后端未启动 | `backend/app/api/audit_logs.py`、`backend/app/services/audit_service.py` |

## 怎么串起来

1. 先跑 `GET /health`。
2. 再跑 `POST /api/tasks`、`GET /api/tasks/{task_id}`、`GET /api/tasks/{task_id}/report`。
3. 再跑 documents、retrieval、internal RAG。
4. 最后再看 approval、security、audit。

