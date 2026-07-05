# 启动与排错指南

这份文档用于本地启动 Retail Insight AI，并区分 Swagger、ReDoc、OpenAPI JSON、unittest、前后端联调各自的作用。

## 三个文档入口不是同一个用途

- Swagger 是 API 调试与验证工具。
- ReDoc 是 API 阅读文档。
- OpenAPI JSON 是机器可读接口定义。
- 三者不是同一个用途。
- UI 完成后 Swagger 仍然可用于后端验证。
- Swagger 和 React 调用的是同一套 FastAPI API。

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
- 当前阶段主要用 Swagger 验证后端骨架。
- UI 完成后再做前后端 Integration Test。
- 发布前再考虑 E2E Test。

## 推荐启动顺序

1. 在项目根目录执行 `./scripts/check_env.sh`。
2. 在项目根目录执行 `./scripts/start_backend.sh`。
3. 打开 `http://127.0.0.1:8000/docs` 看 Swagger。
4. 打开 `http://127.0.0.1:8000/redoc` 看 ReDoc。
5. 打开 `http://127.0.0.1:8000/openapi.json` 看 OpenAPI JSON。
6. 如需前端联调，再执行 `./scripts/start_frontend.sh`。

## 如果要直接看后端原始输出

```bash
cd backend
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

这样做适合观察最原始的 FastAPI 启动日志和异常堆栈。

## Swagger / ReDoc / OpenAPI JSON 的使用方式

### Swagger

用途：手工执行接口，验证请求、响应和业务流程。

推荐先点：

1. `GET /health`
2. `POST /api/tasks`
3. `GET /api/tasks/{task_id}`
4. `GET /api/tasks/{task_id}/report`

### ReDoc

用途：阅读字段结构和响应模型，不适合高频点击调试。

### OpenAPI JSON

用途：确认接口定义是否真的注册，适合做合同检查和工具接入。

## unittest 执行规则

测试命令必须在 `backend` 目录执行：

```bash
cd backend
python3 -m unittest discover -s tests -v
```

单文件执行方式：

```bash
cd backend
python3 -m unittest tests.test_api -v
```

不要在项目根目录直接执行：

```bash
python3 -m unittest tests.test_api -v
```

如果出现 `ModuleNotFoundError: No module named tests`，说明执行目录错了，不要先怀疑测试代码本身。

## 常见问题

### Swagger 打不开

先确认后端是否真的启动，再确认访问的是 `127.0.0.1:8000/docs`。

### ReDoc 打不开

说明后端可能没起来，或者路由未正常注册。先回头验证 `/health`。

### openapi.json 打不开

优先怀疑后端启动失败、接口注册失败或访问地址错误。

### unittest 找不到 tests

大概率是因为你不在 `backend/` 目录里执行。

### 审批或安全接口是空的

先确认你不是在空白进程里刚启动后立即读取；再看 `docs/LEARNING_API_WALKTHROUGH.md` 的推荐执行顺序。

## 推荐验证顺序

```text
Swagger
→ 主链路 API
→ 文档链路 API
→ 审批 / 安全 / 审计 API
→ backend unittest
→ React + FastAPI 联调
```
