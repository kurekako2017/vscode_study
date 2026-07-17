# 启动完成检查清单

本清单用于确认文档、接口和测试入口是否按 **ERIP V1.0 当前交付状态** 正常工作。

## ERIP V1.0 当前权威启动入口

与 `docs/learning/01_Foundation/RUNBOOK_LOCAL.md` 一致（本清单不新增 Appendix，只做验收勾选入口）：

| 场景 | 权威入口 |
|---|---|
| ERIP V1.0 正式启动 | Docker Compose + PostgreSQL（RUNBOOK Appendix M） |
| 本地 PostgreSQL 联调 | `REPOSITORY_BACKEND=postgres` + Backend/Frontend |
| 快速单元测试 / 教学 | InMemory，**仅辅助**（不作业务验收） |
| 最终业务验收 | PostgreSQL + Stub E2E（RUNBOOK M/N） |

**Repository 定位**：PostgreSQL 为正式运行/业务验收权威；Compose 默认且必须 PostgreSQL。InMemory 仅快速 unittest/教学，代码保留但不补企业能力。

正式前端导航验收标准（与 `frontend/src/App.tsx` 一致）：

```text
学习总览
→ 文書管理
→ RAG/AI分析
→ KPI任务分析
→ 承認管理
→ AI管理（仅 security.manage / admin）
```

业务主链概念仍可口述为：`文書管理 → RAG検索 → AI分析(low_cost) → 董事会报告(high_quality) → 承認管理`。
页面标签「分析依頼」已拆分为 **RAG/AI分析**（文档检索 + 显式 AI）与 **KPI任务分析**（旧 Task/SSE 链路）。

说明：Frontend 为 V1.0 正式联调步骤。**业务与持久化验收以 PostgreSQL 为准**（Compose 推荐）。InMemory 仅辅助。若 Docker daemon 不可用，应如实记录未执行 Compose，不要假装通过。

## 必查规则

- Swagger 可打开。
- ReDoc 可打开。
- OpenAPI JSON 可打开。
- Swagger 能执行 `GET /health`。
- Swagger 能执行主链路 API。
- unittest 能在 `backend` 目录执行。
- 如果启动时报 `Form data requires "python-multipart" to be installed`，先看 `docs/learning/01_Foundation/RUNBOOK_LOCAL.md` 的 Appendix B。
- 不要在项目根目录直接执行 unittest（错误示范：`python3 -m unittest tests.test_api -v`）；权威命令见第 8 节 `./.venv/bin/python`。
- 如果报 `ModuleNotFoundError: No module named tests`，说明目录错了。
- V1.0 默认验收使用 `LLM_PROVIDER_MODE=stub`，不默认产生真实 LLM 费用。
- 不要用「Frontend Phase 3 / Frontend 可选 / Docker 未验证 / PostgreSQL 未完成 / 未来接入 / 计划中」等历史表述当作当前操作结论。

## 1. Swagger 可打开

验证方式：

```bash
curl -I http://127.0.0.1:8000/docs
```

预想结果：返回 `200` 或可访问页面响应。

## 2. ReDoc 可打开

验证方式：

```bash
curl -I http://127.0.0.1:8000/redoc
```

预想结果：返回 `200` 或可访问页面响应。

## 3. OpenAPI JSON 可打开

验证方式：

```bash
curl -sS http://127.0.0.1:8000/openapi.json | head
```

预想结果：能看到 JSON 开头和 `paths` / `components` 信息。

## 4. Swagger 能执行 GET /health

验证方式：

1. 打开 `/docs`
2. 执行 `GET /health`

预想结果：

- 必有：`status=ok`、`service=retail-insight-ai`、非空 `request_id`
- **正式路径**（Compose 或 `REPOSITORY_BACKEND=postgres`）：必须 `repository_backend=postgres`
- **InMemory 辅助路径**（本地脚本未设 postgres）：允许 `repository_backend=inmemory`，**不作业务验收**
- Research / KPI 等业务 provider 字段若存在，以当前配置为准
- **禁止**再把历史 Health 字段断言（旧文档中的 static provider 字段）当作 V1.0 必过条件

## 4.1 Swagger JWT 认证闭环（login → Authorize → me → 受保护 API）

验证方式：

1. `POST /api/v1/auth/login`（或 UI 登录）：使用测试账号 `admin` / `manager` / `employee` 之一
2. 从响应复制 `access_token`（**不要**写入文档、截图或 git）
3. 在 Swagger 点击 **Authorize**，填入 `Bearer <access_token>`（或 UI 等价会话注入）
4. 执行 `GET /api/v1/users/me`，确认身份与角色
5. 再执行任一受保护业务 API（例如 `GET /api/v1/documents` 或 `POST /api/v1/ai-analysis`）

预想结果：

- login：`200` + `access_token`
- users/me：`200` + 与角色一致的权限镜像
- 受保护 API：已 Authorize 时按权限返回业务结果，而不是匿名失败

### 401 与 403 区别（必会）

| 状态 | 含义 | 会话处理 | 典型场景 |
|---|---|---|---|
| **401** | 未认证 / Token 无效或过期 | 应清理会话并回到登录 | 未 Authorize、Token 损坏、过期 JWT |
| **403** | 已认证但权限不足 | **保持**当前登录会话，仅拒绝该操作 | employee 调用 approve；无 `approval.review` 读他人审批 |

## 5. Swagger 能执行主链路 API

验证方式：

1. 执行 `POST /api/tasks`
2. 用返回的 `task_id` 执行 `GET /api/tasks/{task_id}`
3. 再执行 `GET /api/tasks/{task_id}/report`

预想结果：在 **已 Authorize** 前提下，任务可创建，状态可读取，报告最终可取回；终端还能看到 `question`、`mode` 和 `task_id` 的学习日志（若该链路仍开放）。未带 Token 时优先预期 **401**，而不是把权限错误误判为业务 500。

## 6. Swagger 能执行文档主链路 API

验证方式：

1. 执行 `POST /api/v1/documents`
2. 执行 `GET /api/v1/documents`
3. 执行 `POST /api/v1/documents/{document_id}/import`
4. 执行 `POST /api/v1/documents/{document_id}/chunks`
5. 执行 `POST /api/v1/document-retrieval/search`

预想结果：在 **Bearer 已 Authorize** 下文档链路可按顺序推进（upload → import → chunk → retrieval）。

## 7. Swagger 能执行审批 / 安全 / 审计主链路 API

验证方式（均需有效 JWT；角色按步骤切换 Token）：

1. `GET /api/v1/users/me`（确认当前主体）
2. `GET /api/v1/security/roles` 与 `GET /api/v1/security/permissions`
3. 业务前置完成后 `POST /api/v1/reports/{task_id}/submit-approval`（submitter）
4. `GET /api/v1/approvals` 与 `GET /api/v1/approvals/{approval_id}`（manager/reviewer）
5. employee Token 尝试 approve → 期望 **403**（会话保持）
6. manager Token approve → 期望成功
7. `GET /api/v1/audit-logs` 核对拒绝与批准事实

预想结果：安全目录可读；审批按 RBAC 推进；403/成功路径可区分；审计可取回。

## 8. unittest 能在 backend 目录执行（权威命令）

验证方式：

```bash
cd backend
./.venv/bin/python -m unittest tests.test_api -v
```

预想结果：测试被正确发现并运行。权威解释器为 `backend/.venv/bin/python`（与 `scripts/start_backend.sh` 一致）。

## 9. 不要在项目根目录直接执行 unittest（错误示范）

以下为 **错误示范，非权威命令**（故意展示裸 `python3 -m`）：

```bash
# 错误示范：在项目根目录、且使用系统 python3
python3 -m unittest tests.test_api -v
```

如果这样执行后看到 `ModuleNotFoundError: No module named tests`，说明目录或解释器错了。请改回 `cd backend && ./.venv/bin/python -m unittest ...`。

## 10. 失败时优先看哪里

- 启动失败先看 `README.md` 和本文件的启动检查项
- 接口学习顺序先看 `docs/learning/01_Foundation/LEARNING_API_WALKTHROUGH.md`（若路径调整，以 `docs/learning/` 下最新 walkthrough 为准）
- 测试目的和程序流程先看 `docs/learning/01_Foundation/TEST_CASES.md`
- 启动与排错细节先看 `docs/learning/01_Foundation/RUNBOOK_LOCAL.md`
- 目录和整体入口先看 `README.md`

## 11. Frontend 开发服务可打开（本地脚本；正式优先 Compose :8080）

验证方式：

1. `./scripts/start_frontend.sh`（Backend 已在 8000）
2. 浏览器打开 `http://127.0.0.1:5173`

预想结果：登录后能看到正式主导航（**学习总览 → 文書管理 → RAG/AI分析 → KPI任务分析 → 承認管理**；admin 另有 **AI管理**）；不是空白连接失败页。历史英文标签 `Dashboard/Tasks/...` 与旧标签「分析依頼」不作验收标准。

## 12. Frontend 自动化测试与 production build

验证方式：

```bash
cd frontend
npm test
npm run build
```

预想结果（本轮基线）：

- 测试 **115 / 115** 通过
- `vite build` 成功

## 13. Backend 全量 unittest（InMemory，仅辅助）

验证方式：

```bash
cd backend
./.venv/bin/python -m unittest discover -s tests -v
```

预想结果（V1.0 基线，**辅助**）：

- **270 tests**，**52 skipped**
- 无 unexpected failure
- 本结果 **不作** 业务/企业能力验收结论

## 14. Backend PostgreSQL 全量 unittest（正式验收路径 / 权威）

验证方式：

```bash
cd backend
export REPOSITORY_BACKEND=postgres
export DATABASE_URL="postgresql+psycopg:///erip_integration_test?host=/var/run/postgresql"
export LLM_PROVIDER_MODE=stub
./.venv/bin/python -m unittest discover -s tests -v
```

预想结果（V1.0 基线）：

- **281 tests**，**2 skipped**（real LLM smoke 默认 skip）
- 无随机 401（JWT leeway 已覆盖时钟回拨）
- 专用库名必须是 `erip_integration_test`
- 服务健康检查：`status=ok` 且 `repository_backend=postgres`

## 15. Docker Compose 健康验收

前置：Docker Desktop Engine 与 WSL Integration 可用。宿主 5432 被占用时：

```bash
export POSTGRES_PORT=5433
export BACKEND_PORT=8000
export FRONTEND_PORT=8080
```

验证方式：

```bash
./scripts/prove_dockerignore.sh
docker compose config >/dev/null
./scripts/compose_up.sh
./scripts/compose_verify.sh
```

预想结果：

- postgres / backend / frontend healthy
- `GET http://127.0.0.1:8000/health` → `status=ok` 且 **`repository_backend=postgres`**
- `GET http://127.0.0.1:8080/` → 200
- SPA 路由 `/login` `/dashboard` `/documents` `/rag` `/analysis` `/approval` → 200（非 404）
- Alembic current → `20260717_07_fallback_chain (head)`
- 默认 `LLM_PROVIDER_MODE=stub`

## 16. Stub API E2E（零真实 LLM）

验证方式：

```bash
export E2E_BASE_URL=http://127.0.0.1:8000
export E2E_EXPECT_STUB=1
./scripts/run_api_e2e.sh
```

预想结果：

- 终端 `OK`
- 覆盖三角色登录、文档流、检索、AI 分析 stub-low-cost、董事会报告 stub-high-quality、employee approve 403、manager approve 成功、Audit
- 不输出 API Key / 完整 Token

## 17. Compose 持久化与安全 down

验证方式：

1. 创建可识别的业务数据并记录安全 ID
2. `./scripts/compose_down.sh`（确认脚本 **拒绝** `-v`）
3. `docker volume ls` 仍有 `erip_postgres_data`
4. `./scripts/compose_up.sh` + `./scripts/compose_verify.sh`
5. 确认数据仍在
6. 再次 `./scripts/compose_down.sh`，**不要**执行 `docker compose down -v`

预想结果：Volume 保留，数据可恢复。

## 18. 人工业务链（Scenario01 勾选，不复制整表）

权威详细步骤表（**24 步八列表**）见：

`docs/learning/01_Foundation/TEST_CASES.md` → 章节 **「Scenario01 详细验收表」**

辅助剧本：`docs/learning/sample-data/Scenario01_Sales_Decline/10_業務テストシナリオ.md`

本清单只做勾选，**不复制**整张 Scenario01 表：

- [ ] 登录拿到 `access_token`，Swagger Authorize / UI 会话生效
- [ ] `users/me` 角色正确
- [ ] 上传 **201** → Import **201** → Chunk **201**（与源码 `HTTP_201_CREATED` 一致；详见 TEST_CASES Scenario01）
- [ ] Retrieval + Citation（普通 RAG，HTTP **200**）
- [ ] AI 分析 **200**：low_cost Provider/Model/Usage/Cost（stub）
- [ ] 取締役会报告 **200**，报告 `status="generated"`（`ReportStatus.GENERATED`）；high_quality Provider/Model/Usage/Cost（stub）
- [ ] submit-approval **201**，Approval `pending_approval`
- [ ] employee approve → **403**（会话保持）
- [ ] manager detail/history → manager approve **200** / `approved`
- [ ] ReportVersion + Audit + Ledger 可核对
- [ ] 普通 RAG 路径无真实 Provider 外呼
- [ ] 最终报告/审计可读；默认 stub 零真实 LLM 费用

预想结果：与 TEST_CASES Scenario01 表一致；403 与 401 区分正确。

## 19. compileall 与 diff-check

验证方式：

```bash
cd backend && ./.venv/bin/python -m compileall app
cd .. && git diff --check
```

预想结果：无编译错误；diff-check 无空白错误。

## 20. V1.0 基线数字速查

| 项 | 基线 |
|---|---|
| Backend PostgreSQL（正式） | 281 tests / 2 skipped |
| Backend InMemory（辅助） | 270 tests / 52 skipped |
| Frontend | 113 / 113 |
| Alembic head | `20260717_07_fallback_chain` |
| 默认 LLM | stub，零真实费用 |
| Compose | healthy + Stub E2E + volume 保留 |

更完整的启动步骤与排错见 `docs/learning/01_Foundation/RUNBOOK_LOCAL.md` Appendix M / N；测试文件学习见 `docs/learning/01_Foundation/TEST_CASES.md`。
