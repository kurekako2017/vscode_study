# LEARNING API WALKTHROUGH

This document is the runnable learning path for Sprint R3.
English summary: start the backend, verify Swagger, then walk through the smallest working API surfaces in the same order the project explains them.
中文（简体）摘要：先启动后端，再确认 Swagger，然后按最小可运行路径学习各个 API。
日本語要約：まず backend を起動し、Swagger を確認してから、最小可動パスで各 API を学びます。

## Shortest Path / 最短路径 / 最短経路

| Order | Read this first | Problem it solves | 不建议一开始看的内容 |
| --- | --- | --- | --- |
| 1 | `README.md` | Find the project purpose, current boundary, and where to start | Full backlog history, handbook mirror appendices |
| 2 | `docs/LEARNING_API_WALKTHROUGH.md` | Learn how to start and verify the runnable MVP | Deep architecture diagrams and future platform plans |
| 3 | `CODE_STUDY_GUIDE.md` | Learn the code reading order and the runtime call chain | Frontend deep dive before understanding backend flow |
| 4 | `docs/TEST_CASES.md` | See which tests exist and what they protect | Reading every test body before knowing the file map |
| 5 | `docs/INTERVIEW_GUIDE.md` | Learn how to explain the project in interviews | Memorizing answers before understanding the system shape |

English: start with `README.md`, then `LEARNING_API_WALKTHROUGH.md`, then `CODE_STUDY_GUIDE.md`.
中文（简体）：先看 `README.md`，再看 `docs/LEARNING_API_WALKTHROUGH.md`，最后看 `CODE_STUDY_GUIDE.md`。
日本語：まず `README.md`、次に `docs/LEARNING_API_WALKTHROUGH.md`、最後に `CODE_STUDY_GUIDE.md` を読みます。

## 1. Start Commands

```bash
cd backend
python3 -c "from app.main import app; print(app.title)"
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

If you only need a quick non-network check:

```bash
cd backend
python3 - <<'PY'
from app.main import app
print(app.title)
print(len(app.routes))
print(app.openapi()["info"]["title"])
PY
```

## 2. Swagger

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

中文（简体）：Swagger 负责看接口形状，OpenAPI JSON 负责确认路由确实注册。
日本語：Swagger は API 形状の確認、OpenAPI JSON はルート登録確認に使います。

## 3. Recommended Study Order

1. `GET /health`
2. `POST /api/tasks`
3. `GET /api/tasks/{task_id}`
4. `GET /api/tasks/{task_id}/report`
5. `POST /api/v1/documents`
6. `GET /api/v1/documents`
7. `GET /api/v1/documents/{document_id}`
8. `DELETE /api/v1/documents/{document_id}`
9. `POST /api/v1/documents/{document_id}/import`
10. `POST /api/v1/documents/{document_id}/chunks`
11. `GET /api/v1/documents/{document_id}/chunks`
12. `POST /api/v1/document-retrieval/search`
13. `POST /api/v1/internal-rag/answer`
14. `POST /api/v1/reports/{task_id}/submit-approval`
15. `GET /api/v1/approvals`
16. `GET /api/v1/approvals/{approval_id}`
17. `POST /api/v1/approvals/{approval_id}/approve`
18. `POST /api/v1/approvals/{approval_id}/reject`
19. `GET /api/v1/users/me`
20. `GET /api/v1/security/roles`
21. `GET /api/v1/security/permissions`
22. `GET /api/v1/audit-logs`

English: this order moves from the smallest health check to the most layered business flows.
中文（简体）：这个顺序从最小健康检查一路走到最复杂的业务链路。
日本語：この順序は、最小の health check から最も層の深い業務フローへ進みます。

## 4. Document Roles / 文档职责 / 文書の役割

| Document | What it answers | 不建议一开始看什么 |
| --- | --- | --- |
| `README.md` | What this project is and where to start | Full decision history |
| `docs/LEARNING_API_WALKTHROUGH.md` | How to start, what runs, what still does not run | Long backlog narratives |
| `CODE_STUDY_GUIDE.md` | Which files to read and why | Fine-grained implementation details before the runtime chain |
| `RUNBOOK_LOCAL.md` | How to start the app locally end-to-end | Frontend deep code before backend starts |
| `VERIFY_CHECKLIST.md` | Which commands prove the system works | Raw unit test internals before basic startup |
| `docs/INTERVIEW_GUIDE.md` | How to explain the project in interviews | Internal file-by-file details before the high-level story |

## 5. What Works Now

- `GET /health` returns service metadata and `request_id`.
- Task APIs create a runnable in-memory workflow and return a report.
- Document APIs support upload, list, read, archive, import, chunk, retrieval, and internal RAG without LLM.
- Approval APIs support submit, list, detail, approve, and reject.
- Security APIs expose current user, role catalog, permission catalog, and audit logs.

## 6. What Does Not Yet Work

- frontend UI polishing
- PostgreSQL repository full migration
- real authentication
- JWT/OAuth
- real LLM provider
- pgvector
- internet search
- MCP
- production deployment

中文（简体）：这些未完成项不是失败，而是当前阶段明确冻结的边界。
日本語：これらの未完了項目は失敗ではなく、現在フェーズで明示的に凍結された境界です。

## 7. Curl Examples

```bash
curl -sS http://127.0.0.1:8000/health
curl -sS -X POST http://127.0.0.1:8000/api/tasks -H 'Content-Type: application/json' -d '{"question":"売上と在庫の状況を分析してください","mode":"hybrid"}'
curl -sS http://127.0.0.1:8000/api/v1/users/me
curl -sS http://127.0.0.1:8000/api/v1/security/roles
```

For document upload, use multipart form data with `file` and `metadata`.

## 8. Expected Responses

- Health: `status=ok`
- Task create: HTTP 202 and a `task_id`
- Task status: queued/running/completed/failed
- Report: `status=generated`
- Document upload: HTTP 201 and a `document_id`
- Import / chunk / retrieval / internal RAG: HTTP 200 or 201 with deterministic local results
- Approval: HTTP 201 on submit, HTTP 200 on list/detail/approve/reject
- Security: HTTP 200 with frozen read models

## 9. Common Errors

- `VALIDATION_ERROR`: request body shape is wrong
- `document_not_found`: the document id does not exist
- `document_archived`: the document was archived before import/chunk
- `permission_denied`: RBAC blocks the approval API
- `REPORT_NOT_FOUND`: the task has not produced a report yet
- `psycopg is not installed`: PostgreSQL integration tests are skipped in this environment

## 10. Interview Points

1. The project is runnable without external LLM or PostgreSQL.
2. Task, document, approval, security, and audit are separated by service boundaries.
3. InMemory repositories make the project easy to learn and easy to reset.
4. The approval and security layers are contract-stable, so future auth or PostgreSQL work can replace implementations without rewriting API shapes.
5. The new learning walkthrough is a practical onboarding path, not a feature change.
