# 启动完成检查清单

本清单用于确认文档、接口和测试入口是否按当前学习阶段正常工作。

## 必查规则

- Swagger 可打开。
- ReDoc 可打开。
- OpenAPI JSON 可打开。
- Swagger 能执行 `GET /health`。
- Swagger 能执行主链路 API。
- unittest 能在 `backend` 目录执行。
- 如果启动时报 `Form data requires "python-multipart" to be installed`，先看 `docs/learning/01_Foundation/RUNBOOK_LOCAL.md` 的 Appendix B。
- 不要在项目根目录直接执行 `python3 -m unittest tests.test_api -v`。
- 如果报 `ModuleNotFoundError: No module named tests`，说明目录错了。
- V1.0 默认验收使用 `LLM_PROVIDER_MODE=stub`，不默认产生真实 LLM 费用。

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

预想结果：返回 `status=ok`、`service=retail-insight-ai`、`provider=static`、非空 `request_id`。

## 5. Swagger 能执行主链路 API

验证方式：

1. 执行 `POST /api/tasks`
2. 用返回的 `task_id` 执行 `GET /api/tasks/{task_id}`
3. 再执行 `GET /api/tasks/{task_id}/report`

预想结果：任务可创建，状态可读取，报告最终可取回；终端还能看到 `question: 你好`、`mode: hybrid` 和 `task_id` 的学习日志。

## 6. Swagger 能执行文档主链路 API

验证方式：

1. 执行 `POST /api/v1/documents`
2. 执行 `GET /api/v1/documents`
3. 执行 `POST /api/v1/documents/{document_id}/import`
4. 执行 `POST /api/v1/documents/{document_id}/chunks`
5. 执行 `POST /api/v1/document-retrieval/search`

预想结果：文档链路可按顺序推进。

## 7. Swagger 能执行审批 / 安全 / 审计主链路 API

验证方式：

1. 执行 `POST /api/v1/reports/{task_id}/submit-approval`
2. 执行 `GET /api/v1/approvals`
3. 执行 `GET /api/v1/users/me`
4. 执行 `GET /api/v1/security/roles`
5. 执行 `GET /api/v1/security/permissions`
6. 执行 `GET /api/v1/audit-logs`

预想结果：审批资源可见，安全目录可读，审计日志可取回。

## 8. unittest 能在 backend 目录执行

验证方式：

```bash
cd backend
python3 -m unittest tests.test_api -v
```

预想结果：测试被正确发现并运行。

## 9. 不要在项目根目录直接执行 unittest

这条命令不是标准做法：

```bash
python3 -m unittest tests.test_api -v
```

如果这样执行后看到 `ModuleNotFoundError: No module named tests`，说明目录错了。

## 10. 失败时优先看哪里

- 启动失败先看 `README.md` 和本文件的启动检查项
- 接口学习顺序先看 `docs/learning/01_Foundation/LEARNING_API_WALKTHROUGH.md`（若路径调整，以 `docs/learning/` 下最新 walkthrough 为准）
- 测试目的和程序流程先看 `docs/learning/01_Foundation/TEST_CASES.md`
- 启动与排错细节先看 `docs/learning/01_Foundation/RUNBOOK_LOCAL.md`
- 目录和整体入口先看 `README.md`

## 11. Frontend 开发服务可打开（原本地路径）

验证方式：

1. `./scripts/start_frontend.sh`（Backend 已在 8000）
2. 浏览器打开 `http://127.0.0.1:5173`

预想结果：能看到 Dashboard / 登录后的主导航；不是空白连接失败页。

## 12. Frontend 自动化测试与 production build

验证方式：

```bash
cd frontend
npm test
npm run build
```

预想结果（V1.0 基线）：

- 测试 **113 / 113** 通过
- `vite build` 成功

## 13. Backend 全量 unittest（InMemory 默认）

验证方式：

```bash
cd backend
python3 -m unittest discover -s tests -v
```

预想结果（V1.0 基线）：

- **270 tests**，**52 skipped**
- 无 unexpected failure

## 14. Backend PostgreSQL 全量 unittest（正式验收路径）

验证方式：

```bash
cd backend
export REPOSITORY_BACKEND=postgres
export DATABASE_URL="postgresql+psycopg:///erip_integration_test?host=/var/run/postgresql"
export LLM_PROVIDER_MODE=stub
python3 -m unittest discover -s tests -v
```

预想结果（V1.0 基线）：

- **281 tests**，**2 skipped**（real LLM smoke 默认 skip）
- 无随机 401（JWT leeway 已覆盖时钟回拨）
- 专用库名必须是 `erip_integration_test`

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
- `GET http://127.0.0.1:8000/health` → `status=ok`
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

## 18. 人工业务链（样例数据）

验证方式：按 `docs/learning/sample-data/Scenario01_Sales_Decline/10_業務テストシナリオ.md`：

```text
文書管理 → RAG検索 → 分析依頼 → 承認管理 → 最终审计报告
```

预想结果：各页面可推进；默认 stub 下无真实 LLM 费用；权限失败显示 403 Banner 而非静默成功。

## 19. compileall 与 diff-check

验证方式：

```bash
cd backend && python3 -m compileall app
cd .. && git diff --check
```

预想结果：无编译错误；diff-check 无空白错误。

## 20. V1.0 基线数字速查

| 项 | 基线 |
|---|---|
| Backend PostgreSQL | 281 tests / 2 skipped |
| Backend InMemory | 270 tests / 52 skipped |
| Frontend | 113 / 113 |
| Alembic head | `20260717_07_fallback_chain` |
| 默认 LLM | stub，零真实费用 |
| Compose | healthy + Stub E2E + volume 保留 |

更完整的启动步骤与排错见 `docs/learning/01_Foundation/RUNBOOK_LOCAL.md` Appendix M / N；测试文件学习见 `docs/learning/01_Foundation/TEST_CASES.md`。
