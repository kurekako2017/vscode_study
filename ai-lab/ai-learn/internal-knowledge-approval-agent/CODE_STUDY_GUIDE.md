# CODE_STUDY_GUIDE

## 1. 先理解整体流程

先记住系统边界：

```text
React
→ FastAPI
→ QuestionService
→ Workflow
→ Retriever
→ RiskClassifier
→ AnswerGenerator
→ Approval
→ SSE
→ React
```

这是组件全景，不是严格执行顺序。当前代码实际先执行 `RiskClassifier`：LOW 才立即 Retriever/AnswerGenerator；HIGH 先进入 Approval，Approve 后才 Retriever/AnswerGenerator。SQLite 同时保存问题、审批和事件。

## 2. 后端阅读顺序

### 2.1 `backend/app/main.py`

- 负责什么：创建 FastAPI、配置 CORS、请求 ID、中间件、异常处理和路由。
- 谁调用它：Uvicorn 通过 `app.main:app` 加载。
- 它调用谁：Container、日志配置和 `app.api.routes`。
- 输入是什么：HTTP Request 和可选 `Settings`。
- 输出是什么：FastAPI application、HTTP Response。
- 初学者重点：`create_app()`、`request_context()`、exception handler。
- 常见误区：把业务判断写进 main；混淆 JSON 中的 request ID 与响应头 `X-Request-ID`。

### 2.2 `backend/app/api/routes/questions.py`（不是旧的单文件 `routes.py`）

- 负责什么：创建问题、查询状态、读取报告。
- 谁调用它：FastAPI Router 接收 `/api/questions` 请求。
- 它调用谁：依赖注入得到 `QuestionService`，再调用 Service。
- 输入是什么：`QuestionCreateRequest` 或 URL 中的 `question_id`。
- 输出是什么：统一 `ApiResponse`，创建接口返回 HTTP 202。
- 初学者重点：Route 只做协议转换，业务流程由 Service 负责。
- 常见误区：认为 POST 返回的对象一定是最终状态；创建返回后应按 ID 查询或订阅 SSE。

补充阅读 `backend/app/api/routes/approvals.py`：它把 URL 中的 `question_id` 和 approve/reject 决策交给 `ApprovalService`。不要把 `approval_id` 放进公开审批 URL。

### 2.3 `backend/app/services/question_service.py`

- 负责什么：协调 Question 生命周期、Workflow、SQLite、审批记录、SSE 事件和日志。
- 谁调用它：Questions Route、ApprovalService 和 Events Route。
- 它调用谁：`SQLiteRepository`、`KnowledgeApprovalWorkflow`、结构化 logger。
- 输入是什么：问题文本、`question_id`、`approval_id`、`request_id` 和决策。
- 输出是什么：问题/报告/审批字典，或持久化后的状态与事件。
- 初学者重点：`create_question()`、`_run_graph()`、`_apply_node()`、`_transition()`、`_publish()`。
- 常见误区：把 Graph 的临时 state 当成长期事实；真正可恢复状态在 SQLite。

### 2.4 `backend/app/workflow/graph.py`

- 负责什么：构建首次执行 Graph 和审批恢复 Graph，定义节点、边与条件路由。
- 谁调用它：QuestionService 调用 `stream()`。
- 它调用谁：`workflow.nodes` 中的风险检查与回答生成函数。
- 输入是什么：`WorkflowState`。
- 输出是什么：逐节点的 `(node_name, patch)` 更新流。
- 初学者重点：`START/END`、`add_conditional_edges()`、initial/resume 两张图。
- 常见误区：以为 `approval_wait` 会一直占用线程；当前实现到此结束，审批后从 SQLite 重建 state 并运行 resume Graph。

### 2.5 `backend/app/workflow/nodes.py`

- 负责什么：把 Workflow 节点连接到风险策略、Retriever 和 AnswerGenerator。
- 谁调用它：`KnowledgeApprovalWorkflow` 的包装节点。
- 它调用谁：`classify_risk()`、`retrieve_documents()`、`generate_answer()`。
- 输入是什么：`WorkflowState`。
- 输出是什么：只包含本节点新增字段的 state patch。
- 初学者重点：节点返回增量，不直接修改数据库。
- 常见误区：在节点里混入 HTTP 或 UI 逻辑；状态持久化仍由 Service 负责。

### 2.6 `backend/app/rag/retriever.py`

- 负责什么：返回固定本地文档集合，是第二阶段的确定性 Retriever。
- 谁调用它：`answer_generated()` 节点。
- 它调用谁：读取 `rag/documents.py` 中的 `DOCUMENTS`。
- 输入是什么：问题字符串；当前实现尚未用它做相关性过滤。
- 输出是什么：`tuple[Document, ...]`。
- 初学者重点：接口边界已经存在，但当前不是向量检索。
- 常见误区：看到 Retriever 就以为调用了 Embedding、向量数据库或 LLM。

### 2.7 `backend/app/approval/policy.py`

- 负责什么：维护 HIGH 关键词并执行大小写不敏感的包含匹配。
- 谁调用它：`workflow.nodes.risk_checked()`。
- 它调用谁：无外部服务。
- 输入是什么：问题文本。
- 输出是什么：`LOW` 或 `HIGH`。
- 初学者重点：`HIGH_RISK_KEYWORDS` 和 `classify_risk()`。
- 常见误区：把关键词规则当成语义分类器；子串命中也会判定 HIGH。

### 2.8 `backend/app/agents/answer_generator.py`

- 负责什么：基于 Workflow state 和本地文档生成固定 Markdown 报告。
- 谁调用它：`workflow.nodes.answer_generated()`。
- 它调用谁：不调用 LLM 或网络。
- 输入是什么：`WorkflowState` 和文档 tuple。
- 输出是什么：报告字符串。
- 初学者重点：LOW 与 approved HIGH 的 `approval_note` 不同。
- 常见误区：文件名包含 agent 就认为存在模型推理；当前是确定性模板函数。

### 2.9 `backend/app/events/sse.py`

- 负责什么：从 SQLite 顺序读取事件，编码为 SSE，并发送 keep-alive。
- 谁调用它：`routes/events.py` 的 StreamingResponse。
- 它调用谁：Repository 的 `list_events_after()` 和 logger。
- 输入是什么：Repository、`question_id`、可选起始 sequence。
- 输出是什么：异步文本流，终止事件为 completed/rejected/error。
- 初学者重点：`id/event/data` 三行格式和 `TERMINAL_EVENTS`。
- 常见误区：认为 SSE 会创建业务事件；事件由 QuestionService 发布，SSE 只读取和传输。

### 2.10 `backend/app/repositories/sqlite_repository.py`

- 负责什么：管理 questions、approvals、events 三类 SQLite 数据和事务。
- 谁调用它：QuestionService、ApprovalService 间接调用、SSE stream。
- 它调用谁：Python `sqlite3` 和本地数据库文件。
- 输入是什么：ID、状态、事件内容和查询游标。
- 输出是什么：字典、字典列表，或 not-found/conflict 异常。
- 初学者重点：表结构、`update_question()`、`decide_approval()` 的 pending 条件、event sequence。
- 常见误区：绕过 Repository 直接写数据库；或把本地 SQLite 当成多实例生产数据库。

## 3. 前端阅读顺序

### 3.1 `frontend/src/main.tsx`

- 负责什么：创建 React Root 并渲染 `<App />`。
- Backend 对应：无直接 API；它只是前端入口。
- 初学者重点：应用从这里启动，业务状态不放在入口文件。

### 3.2 `frontend/src/App.tsx`

- 负责什么：组合提交、状态、审批和结果四个视图。
- Backend 对应：Questions、Approvals、Report 和 SSE API。
- 初学者重点：`submit()`、`watch()`、`decide()` 以及条件渲染。

### 3.3 `frontend/src/api.ts`

- 负责什么：封装 fetch、统一错误、EventSource 订阅。
- Backend 对应：`POST /api/questions`、`GET /api/approvals`、Approve/Reject、Report、Events。
- 初学者重点：`unwrap()` 如何把非成功响应变为 `ApiClientError`；Vite proxy 让相对 `/api` 指向 Backend。

### 3.4 状态管理部分

- 负责什么：App 内 `useState` 保存 view、questionId、status、events、approvals、report、error。
- Backend 对应：API 响应和 SSE event 字段。
- 初学者重点：业务状态和当前页面 `view` 是两类状态；`setEvents(current => ...)` 避免连续事件互相覆盖。

### 3.5 SSE 处理部分

- 负责什么：`watch()` 调用 `subscribeQuestion()`，根据事件更新 timeline 和页面。
- Backend 对应：`GET /api/questions/{question_id}/events`。
- 初学者重点：approval_required、completed、rejected、error 四个分支，以及 cleanup 时关闭 EventSource。

### 3.6 审批按钮部分

- 负责什么：审批列表渲染 Approve/Reject，并调用 `decide()`。
- Backend 对应：`GET /api/approvals` 和 `POST /api/approvals/{question_id}/approve|reject`。
- 初学者重点：UI 显示 `approval_id`，但公开决策 API 使用 `question_id`。

### 3.7 错误显示部分

- 负责什么：`showError()` 规范化错误，`role="alert"` 区域显示错误码和消息。
- Backend 对应：统一错误 envelope 和 SSE `error` event。
- 初学者重点：HTTP 业务错误与 SSE 传输错误走不同路径。

## 4. 一次 LOW 风险请求调用链

1. 用户点击提交，`App.submit()` 调用 `createQuestion()`。
2. Vite 将 `/api/questions` 代理到 FastAPI。
3. Questions Route 校验文本并调用 `QuestionService.create_question()`。
4. Service 写 Question 和 `received` event，再运行 initial Graph。
5. `risk_classifier` 调用 policy，得到 LOW；Service 保存 `risk_checked`。
6. Graph 路由到 `answer_generator`。
7. Node 调用 Retriever 取得固定文档，再由 AnswerGenerator 生成报告。
8. Service 保存报告，发布 `answer_generated` 和 `completed`。
9. React 的 EventSource 收到事件；completed 后调用 Report API 并展示回答。

## 5. 一次 HIGH 风险请求调用链

1. 提交路径与 LOW 相同，直到 RiskClassifier 得到 HIGH。
2. Graph 路由到 `approval_wait`；Service 创建 Approval，问题变成 `approval_required`。
3. React 收到事件后切换到审批列表并显示按钮。
4. Approve：`ApprovalService.decide()` 把审批改为 approved，重建 state，resume Graph 经过 approved → answer_generator → completed，React 最终读取报告。
5. Reject：resume Graph 经过 rejected 后结束，问题状态为 rejected，不生成正式报告。

## 6. Debug 方法

- `print`：只用于短期学习，可在 `workflow/nodes.py` 打印 `state`，或在 `rag/retriever.py` 打印文档标题；验证后删除，避免污染结构化日志。
- `logger`：业务排查优先使用 `config.logging.log_event()`；适合在 QuestionService 状态转换附近记录安全字段，不要记录问题全文或报告全文。
- `breakpoint()`：可放在 Route 入口、`QuestionService._apply_node()`、`classify_risk()` 或前端浏览器 DevTools 的 `watch()` 分支。Backend 使用 reload 时断点体验可能受重启影响。

初学者先观察五个值：

1. `question_id`：跨请求追踪同一问题。
2. `status`：确认状态是否按预期流转。
3. `event`：确认 UI 为什么切换视图。
4. retrieved documents：确认回答引用了哪些固定文档。
5. risk level：确认关键词为何得到 LOW/HIGH。

## 7. 小练习

以下是后续独立练习，不属于本轮修改。

### 练习 1：修改 LOW 风险回答文案

- 目标：调整固定正式回答文字。
- 修改文件：`backend/app/agents/answer_generator.py`。
- 验证方法：提交 LOW 问题并读取 report，再运行 Backend tests。

### 练习 2：新增一个 HIGH 风险关键词

- 目标：让新词进入审批。
- 修改文件：`backend/app/approval/policy.py`、`backend/tests/test_api.py`。
- 验证方法：提交含新词的问题，确认 approval_required。

### 练习 3：修改审批按钮文字

- 目标：把英文按钮改成日文或中文。
- 修改文件：`frontend/src/App.tsx`。
- 验证方法：启动 Frontend，检查按钮；运行 Frontend tests。

### 练习 4：修改 SSE 时间线显示

- 目标：为事件增加更清楚的标签。
- 修改文件：`frontend/src/App.tsx`、必要时 `styles.css`。
- 验证方法：跑一次 LOW/HIGH，确认事件顺序未改变。

### 练习 5：新增一个文档类型

- 目标：增加一份固定社内文档。
- 修改文件：`backend/app/rag/documents.py`。
- 验证方法：读取 LOW report，确认参照资料出现新标题。

### 练习 6：新增一个测试

- 目标：覆盖一个尚未覆盖的错误路径。
- 修改文件：`backend/tests/test_api.py` 或 `frontend/src/*.test.tsx`。
- 验证方法：执行 `./scripts/run_tests.sh`。

### 练习 7：修改日志 message

- 目标：让某个状态转换日志更易读。
- 修改文件：`backend/app/services/question_service.py`。
- 验证方法：运行请求，在 Backend 终端确认字段未丢失。

### 练习 8：修改错误显示

- 目标：为 API 与 SSE 错误提供不同样式或文案。
- 修改文件：`frontend/src/App.tsx`、`frontend/src/styles.css`、相关测试。
- 验证方法：停止 Backend 后提交，确认 alert 显示并跑测试。

### 练习 9：新增一个 department

- 目标：真正接收、保存并返回 department，而不是忽略兼容性字段。
- 修改文件：Schema、Route、Service、Repository、Frontend 和测试；先写清数据迁移影响。
- 验证方法：POST 后 GET 能返回 department，重启 Backend 后数据仍存在。

### 练习 10：修改 report 标题

- 目标：调整 Markdown 报告第一行标题。
- 修改文件：`backend/app/agents/answer_generator.py` 和相关断言。
- 验证方法：LOW/Approve HIGH 的 report 都出现新标题，Reject 仍没有报告。
