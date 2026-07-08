# 启动完成检查清单

本清单用于确认文档、接口和测试入口是否按当前学习阶段正常工作。

## 必查规则

- Swagger 可打开。
- ReDoc 可打开。
- OpenAPI JSON 可打开。
- Swagger 能执行 `GET /health`。
- Swagger 能执行主链路 API。
- unittest 能在 `backend` 目录执行。
- 如果启动时报 `Form data requires "python-multipart" to be installed`，先看 `docs/learning/RUNBOOK_LOCAL.md` 的 Appendix B。
- 不要在项目根目录直接执行 `python3 -m unittest tests.test_api -v`。
- 如果报 `ModuleNotFoundError: No module named tests`，说明目录错了。

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
- 接口学习顺序先看 `docs/learning/LEARNING_API_WALKTHROUGH.md`
- 测试目的和程序流程先看 `docs/learning/TEST_CASES.md`
- 目录和整体入口先看 `README.md`
