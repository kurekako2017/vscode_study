# 代码学习指南


> **项目正式名称：Enterprise Retail Intelligence Platform（ERIP）V1.0**  
> 历史名称：Retail Insight AI（仅早期说明）。正式 Repository：PostgreSQL；InMemory 仅 unittest。  
> 基线：PG **297/6 skip** · IM **286/62 skip** · FE **116/116** · head **`20260717_08_ai_runtime`** · 默认 **stub**。

这份指南面向第一次阅读 `React`、`FastAPI` 和 `LangGraph` 项目的学习者。建议先把后端和前端都运行起来，再按本文顺序阅读；每读到一个步骤，就在页面或日志中观察它的实际效果。

> 路径说明：下文路径都相对于 `retail-insight-ai/`。如果你在别处看到类似 `api/routes/tasks.py` 的写法，在本项目中对应的是 `backend/app/api/tasks.py`。

## 最短学习路径

| 顺序 | 先看什么                                                                                | 先解决什么问题                       | 不建议一开始看什么          |
| ---- | --------------------------------------------------------------------------------------- | ------------------------------------ | --------------------------- |
| 1    | [README.md](./README.md)                                                                 | 先知道项目是什么、当前边界是什么     | backlog 历史和完整 ADR 细节 |
| 2    | [docs/learning/01_Foundation/LEARNING_API_WALKTHROUGH.md](./LEARNING_API_WALKTHROUGH.md) | 先知道怎么启动、怎么验证最小可运行版 | 过深实现和未来平台化规划    |
| 3    | 本文                                                                                    | 先知道代码应该按什么顺序读           | 先看前端实现和测试细枝末节  |

## 主阅读顺序

```text
Swagger
↓
API
↓
Service
↓
Repository
↓
Domain
↓
Tests
```

如果需要看前端，只作为附录，放在最后。

## Domain 和 Tests 怎么看

- `Domain` 先看模型、状态、约束和不变量。
- `Tests` 再看这些约束是怎么被保护的。
- 看到 `Service` 或 `Repository` 的实现时，先回到对应的 `Domain` 和 `Tests`，不要反着跳。

## 为什么要分层

- `Service` 的存在，是为了把一次业务用例的顺序、状态、错误和输出收在一起。
- `Repository` 的存在，是为了把业务和存储方式解耦，未来切 InMemory、Local 或 PostgreSQL 时不用改业务流程。
- `Provider` 的存在，是为了把可替换能力隔离出来，例如 Research、LLM、外部搜索。
- `Workflow` 的存在，是为了把多步骤流程显式化，避免把执行顺序藏进路由或单个 service。

如果不分层，面试时很难解释“为什么这里是业务规则，那里是存储规则，这一步为什么必须独立出来”。

## 1. 项目整体运行流程

### 为什么先看这一层

- 学习目标：先建立“请求从哪里进、结果从哪里出”的整体心智模型。
- 推荐阅读文件：`README.md`、`docs/learning/01_Foundation/LEARNING_API_WALKTHROUGH.md`
- 推荐阅读时间：15 分钟。
- 推荐顺序：第 1 遍。
- 看完应该掌握什么：知道 `React`、`FastAPI`、`Workflow`、`SSE`、`Report` 是怎么串起来的。
- 下一步看哪里：`backend/app/main.py`

```text
React
  点击“分析を開始”
    ↓ POST /api/tasks
FastAPI
  校验请求，创建后台任务
    ↓
TaskService
  保存任务、管理 queued/running/completed/failed
    ↓
Workflow (LangGraph)
  route 节点决定执行路径
    ↓
KPI
  从本地 CSV 生成确定性指标（research 模式跳过）
    ↓
Research
  调用本地 StaticResearchProvider，并从 JSON 读取 Research 数据（kpi 模式跳过）
    ↓
Report
  把已有结果组合成 Markdown
    ↓
SSE
  持续发送 status，最后发送 done 或 error
    ↓
React
  收到 done 后 GET report，并显示报告
```

一句话记忆：**HTTP 创建任务，Workflow 做分析，SSE 报进度，HTTP 再取报告。**

当前默认学习路径仍使用进程内 InMemory 与本地样例输入，且默认 `LLM_PROVIDER_MODE=stub`（不产生真实 LLM 费用）。**V1.0** 同时具备 PostgreSQL/pgvector 企业验收路径（Alembic `20260717_08_ai_runtime`）、JWT 登录、`/users/me` 真实身份、冻结 RBAC、Persistent Audit、LLM Gateway 与 Ledger。Redis/RabbitMQ 不是本仓默认可运行依赖。

安全读模型：`users/me` / roles / permissions / audit-logs 已与 JWT 身份和 Persistent Audit 对齐（详见 `ARCHITECTURE.md` 与 `frontend` Auth 链）。

## 2. 后端阅读顺序

### 为什么先看这一层

- 学习目标：按请求路径从外到内，读懂后端如何分层。
- 推荐阅读文件：`backend/app/main.py`、`backend/app/api/tasks.py`、`backend/app/services/task_service.py`
- 推荐阅读时间：30 分钟。
- 推荐顺序：第 2 遍。
- 看完应该掌握什么：知道路由、Service、Workflow、Provider、Repository 各自负责什么。
- 下一步看哪里：`backend/app/api/tasks.py`

第一次阅读时不要从每个目录的 `__init__.py` 开始。按一次请求从外到内、再从内到外的顺序读：

1. `backend/app/main.py`：应用怎样启动、挂载路由和建立 `request_id`。
2. `backend/app/api/tasks.py`：四个任务 API 怎样接收和返回数据。
3. `backend/app/api/security.py`、`backend/app/api/audit_logs.py`：安全读模型和审计读模型怎样对外暴露。
4. `backend/app/services/task_service.py`：任务生命周期和完整业务用例。
5. `backend/app/services/security_service.py`、`backend/app/services/audit_service.py`：placeholder principal、静态目录和 append-only 审计 seam。
6. `backend/app/workflow/graph.py`，再读 `workflow/state.py`：Node、Edge、State 和模式分支。
7. `backend/app/kpi/workflow.py`，再读 `backend/app/data_loaders/local_files.py`：KPI 如何从 CSV 聚合。
8. `backend/app/agents/research_agent.py`，再读 `agents/providers/static_research.py`：Research 抽象与本地 JSON 实现。
9. `backend/app/reports/generator.py`：最终 Markdown 如何拼装。
10. `backend/app/events/publisher.py`，再读 `events/sse.py`：事件怎样保存并编码成 SSE。
11. `backend/app/repositories/interfaces/`，再读 `repositories/implementations/in_memory/` 与 `repositories/postgres/`：为什么业务层不直接依赖具体存储。
12. 第二轮再补读 `config/container.py`、`app/db/connection.py`、`schemas/`、`models/`、`errors/` 和 `observability/logging.py`。

阅读 `workflow/graph.py` 时，分别用 `hybrid`、`kpi`、`research` 三种 mode 在纸上画路径：

```text
hybrid:  route -> kpi -> research -> report
kpi:     route -> kpi -> report
research: route -> research -> report
```

## 3. 为什么要 Service / Repository / Provider / Workflow

### Service

- 它负责“一个业务用例怎么完成”。
- 它会调用 Repository、Workflow、Provider、Report Generator。
- 它接收的是业务请求，输出的是业务结果。
- 面试时可以说：`Service` 是业务编排层，不让路由直接堆业务规则。

### Repository 仓储层

- 它负责“数据从哪里来、往哪里去”。
- 它隐藏 InMemory 和 PostgreSQL 的差异。
- 它让业务层只关心数据语义，不关心 SQL、文件还是内存。
- 面试时可以说：`Repository` 的价值是替换存储实现时不动业务流程。

### Provider

- 它负责“可替换能力的接缝”。
- 当前 `StaticResearchProvider` 提供本地静态研究结果，未来可以替换真实服务。
- 面试时可以说：`Provider` 是外部能力的适配层，便于逐步升级。

### Workflow

- 它负责“多步骤流程的执行顺序”。
- 任务到底先走 KPI 还是先走 Research，由 Workflow 的分支控制。
- 面试时可以说：`Workflow` 是流程编排层，让状态流转可视化、可测试。

## 4. 前端阅读顺序（附录）

### 为什么先看这一层

- 学习目标：看懂页面状态如何和后端事件、报告加载联动。
- 推荐阅读文件：`frontend/src/App.tsx`、`frontend/src/api.ts`
- 推荐阅读时间：20 分钟。
- 推荐顺序：第 3 遍。
- 看完应该掌握什么：知道 `React` 里哪些状态对应请求、SSE、报告和错误展示。
- 下一步看哪里：`frontend/src/App.tsx`

1. `frontend/src/App.tsx`：先看顶部的七个 `useState`，理解页面保存了哪些状态。
2. `frontend/src/api.ts`：看 `fetch` 请求、统一响应解包和 `EventSource` 订阅。
3. 回到 `App.tsx` 的 `submit()`：任务提交逻辑，重点看提交前重置状态和 `createTask()`。
4. 顺着 `subscribeToTask()` 阅读 SSE 监听逻辑：`status`、`done`、`error` 都进入 `onEvent`。
5. 看 `loadReport()` 及文件末尾的 `ReportViewer`：收到 `done` 后才加载并展示报告。
6. 看两个 `catch`、`onTransportError` 和 `role="alert"`：创建失败、报告加载失败、任务失败和连接失败如何统一显示。
7. 最后读 `frontend/src/types.ts`：核对前端类型与 Backend Schema 是否一致。
8. 用 `frontend/src/App.test.tsx` 和 `api.test.ts` 回顾成功与失败路径。

前端最重要的状态关系是：

```text
status 决定表单是否 busy
events 决定时间线内容
report 决定是否显示 Markdown
error 决定是否显示 Error Panel
unsubscribeRef 负责关闭旧 EventSource
```

## 5. 核心文件说明

### 为什么要先看核心文件

- 学习目标：把“文件职责”与“运行时调用时机”对应起来。
- 推荐阅读文件：`backend/app/main.py`、`backend/app/api/tasks.py`、`backend/app/events/sse.py`、`frontend/src/App.tsx`
- 推荐阅读时间：30 分钟。
- 推荐顺序：第 4 遍。
- 看完应该掌握什么：知道每个核心文件为什么存在，以及面试时怎么解释。
- 下一步看哪里：`backend/app/api/tasks.py`

| 文件路径                                                                   | 负责什么                                                        | 为什么需要                                             | 运行时什么时候被调用                                                                                    | 初学者重点看哪里                                                                  |
| -------------------------------------------------------------------------- | --------------------------------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `backend/app/main.py`                                                    | 创建 FastAPI、构造容器、注册 CORS/路由/异常处理和请求日志中间件 | 提供唯一的应用入口和 HTTP 外壳                         | Uvicorn 导入`app.main:app` 时；每个请求还会经过 middleware                                            | `create_app()`、`request_context()`、`include_router()`                     |
| `backend/app/api/tasks.py`                                               | 创建任务、查状态、订阅事件、取报告                              | 把 HTTP 协议转换成 Service 调用                        | 请求`/api/tasks...` 时                                                                                | `create_task()` 中的 `BackgroundTasks`，以及 `StreamingResponse`            |
| `backend/app/services/task_service.py`                                   | 创建任务、推进状态、执行 Workflow、保存报告、发布事件、收敛异常 | 把一次完整用例放在一处，避免路由和节点各自管理生命周期 | 路由创建/查询任务时；后台任务运行时                                                                     | `create_task()` 与 `run_task()` 的成功/失败两条路径                           |
| `backend/app/workflow/state.py`                                          | 定义节点共享的`AnalysisState`                                 | 让每个节点的输入输出字段清晰且可检查                   | Workflow 创建和每个节点运行时                                                                           | 必填字段与可选结果字段                                                            |
| `backend/app/workflow/graph.py`                                          | 声明 route/kpi/research/report 节点和条件边                     | 把执行顺序显式化，并支持三种 mode                      | `TaskService.run_task()` 调用 `stream()` 时                                                         | `_build_graph()`、`_after_route()`、`_after_kpi()`、增量 state 合并         |
| `backend/app/kpi/workflow.py`                                            | 根据固定规则产生`KPIResult`                                   | KPI 公式必须可重复，不交给模型猜测                     | kpi 节点运行时                                                                                          | `question_factor` 和每个 KPI 字段                                               |
| `backend/app/agents/research_agent.py`                                   | 通过 Provider 执行调查并校验结果                                | 隔离“如何调查”与 Workflow 编排                       | research 节点运行时                                                                                     | `ResearchAgent.run()` 如何只依赖 Provider 接口                                  |
| `backend/app/agents/providers/static_research.py`                        | 返回固定 Research 结果，可注入失败                              | 本地学习时不依赖网络或真实 LLM                         | `ResearchAgent.run()` 调用 provider 时                                                                | 正常返回和`fail` 分支                                                           |
| `backend/app/reports/generator.py`                                       | 把问题、KPI 和 Research 组合成 Markdown                         | 三种 mode 需要同一种报告输出                           | report 节点运行时                                                                                       | 两个可选结果的`if` 和 `lines` 列表                                            |
| `backend/app/events/publisher.py`                                        | 创建业务事件并写入 EventRepository                              | Workflow/Service 不需要知道事件存储细节                | queued、running、节点完成、done/error 时                                                                | 自动补入`request_id`                                                            |
| `backend/app/events/sse.py`                                              | 轮询事件、转换为 SSE 文本、在终态结束连接                       | 浏览器需要实时看到进度                                 | 浏览器连接`/events` 后                                                                                | `id/event/data` 三行格式、cursor、终态 return                                   |
| `backend/app/api/security.py`                                            | 暴露 current user、roles、permissions 的安全读接口              | 先把未来 RBAC 的读模型固定下来                         | 浏览器或 curl 请求`/api/v1/users/me`、`/api/v1/security/roles`、`/api/v1/security/permissions` 时 | placeholder principal、冻结目录和 response model                                  |
| `backend/app/api/audit_logs.py`                                          | 暴露 append-only audit read 接口                                | 给未来审计查看和支持流程预留读模型                     | 请求`/api/v1/audit-logs` 时                                                                           | 只读、append-only、`next_cursor` 占位                                           |
| `backend/app/services/security_service.py`                               | 维护 current user 和静态角色/权限目录                           | 避免把目录散落在路由里                                 | 安全读接口调用时                                                                                        | `system` placeholder principal 与 frozen catalog                                |
| `backend/app/services/audit_service.py`                                  | 追加和读取审计事实，并记录成功/失败日志                         | 把 audit append-only seam 固定在 service 层            | 未来写审计事实或测试 seed 时                                                                            | `audit.log.created` / `audit.log.failed`                                      |
| `backend/app/models/security.py`                                         | 定义 user、org、department、role、permission、policy            | 先固定安全域概念层                                     | service / schema / repository 读取时                                                                    | 当前用户快照和 static catalog 的字段                                              |
| `backend/app/models/audit.py`                                            | 定义 append-only`AuditLog` 领域对象                           | 审计事实必须 write-once                                | audit service / repository 读写时                                                                       | `result`、`metadata` 和 `timestamp`                                         |
| `backend/app/repositories/interfaces/audit_repository.py`                | 定义审计追加与读取合同                                          | 后续换 PostgreSQL 时不改 service                       | 容器组装和测试时                                                                                        | 只有 append 与 list_all                                                           |
| `backend/app/repositories/implementations/in_memory/audit_repository.py` | 用列表和锁保存审计事实                                          | 本地学习时不依赖数据库                                 | audit append / read 时                                                                                  | 不能 update/delete，只能 append                                                   |
| `backend/app/repositories/interfaces/`                                   | 定义 Task/Event/Report 存储合同                                 | Service 依赖抽象，存储实现可替换                       | 容器构造和类型检查时                                                                                    | `Protocol` 中最小方法集合                                                       |
| `backend/app/repositories/implementations/in_memory/`                    | 用字典、锁和深拷贝保存运行数据                                  | 提供无需外部数据库的本地实现                           | 任务和事件每次读写时                                                                                    | 为什么返回`deepcopy`，为什么使用 `RLock`                                      |
| `backend/app/config/container.py`                                        | 创建并连接 Repository、Agent、Workflow、Service                 | 具体实现只在组合根出现                                 | FastAPI 应用创建时一次                                                                                  | `build_container()` 的依赖连接顺序                                              |
| `backend/app/schemas/task_api.py`                                        | 定义任务请求和响应的 Pydantic Schema                            | 在 HTTP 边界校验输入并固定合同                         | FastAPI 解析请求/序列化响应时                                                                           | `question` 长度、`mode` 限制和 `from_domain()`                              |
| `backend/app/schemas/security_api.py`                                    | 定义 current user、role、permission 的 HTTP Schema              | 固定 security read model 的公开字段                    | FastAPI 解析/序列化时                                                                                   | `from_domain()` 如何扁平化主体快照                                              |
| `backend/app/schemas/audit_api.py`                                       | 定义 audit log 的 HTTP Schema                                   | 固定 append-only 审计读模型                            | FastAPI 解析/序列化时                                                                                   | `timestamp`、`metadata`、`next_cursor`                                      |
| `backend/app/observability/logging.py`                                   | JSON 日志、request_id 上下文和安全字段                          | 将同一请求/任务的日志关联起来                          | 应用启动、每个请求和业务关键步骤                                                                        | `bind_request_id()`、`log_event()` 允许的字段                                 |
| `frontend/src/App.tsx`                                                   | 页面状态、提交、SSE 回调、报告加载和渲染                        | 把完整用户流程集中展示                                 | React 首次渲染和每次用户/网络事件发生时                                                                 | `submit()`、`loadReport()`、函数式 `setEvents()`、清理 EventSource          |
| `frontend/src/api.ts`                                                    | 封装 fetch、响应解包和 EventSource                              | UI 不直接处理 HTTP/SSE 细节                            | `App.tsx` 创建任务、订阅或取报告时                                                                    | `unwrapResponse()`、`subscribeToTask()`、业务 error 与 transport error 的区别 |
| `frontend/src/types.ts`                                                  | 定义 API 和 SSE 的 TypeScript 类型                              | 编译期发现前后端合同不一致                             | TypeScript 编译和开发时                                                                                 | `TaskEvent` 与 Backend `TaskEventResponse` 的字段对应                         |
| `frontend/src/App.test.tsx`                                              | 模拟 fetch/EventSource 验证完整 UI 流程                         | 不启动浏览器也能稳定验证成功和错误显示                 | 执行 Frontend tests 时                                                                                  | `FakeEventSource.emit()` 如何驱动真实 React 回调                                |

## 6. 一次完整任务的源码调用链

### 为什么要看这一段

- 学习目标：把一次 `hybrid` 请求从按钮点击追踪到最终报告。
- 推荐阅读文件：`backend/app/api/tasks.py`、`backend/app/services/task_service.py`、`backend/app/events/sse.py`、`backend/app/reports/generator.py`
- 推荐阅读时间：20 分钟。
- 推荐顺序：第 5 遍。
- 看完应该掌握什么：知道任务、事件、Workflow、报告和前端状态如何串联。
- 下一步看哪里：`backend/app/events/sse.py`

以页面默认的 `hybrid` 任务为例：

1. 用户点击 `App.tsx` 中的“分析を開始”按钮，浏览器触发表单 `onSubmit={submit}`。
2. `submit()` 阻止页面刷新，关闭旧 SSE，清空旧 task、events、report 和 error。
3. `submit()` 调用 `api.ts:createTask()`，浏览器发送 `POST /api/tasks`。
4. Vite 开发代理把 `/api` 请求转发到 `http://127.0.0.1:8000`。
5. `main.py:request_context()` 生成或读取 `X-Request-ID`，绑定日志上下文。
6. FastAPI 用 `TaskCreateRequest` 校验 `question` 和 `mode`，再调用 `api/tasks.py:create_task()`。
7. 路由调用 `TaskService.create_task()`：先打印 `[LEARNING REQUEST BODY]`，把 `task_id`、`question`、`mode` 记到终端，再生成 `task_id`、保存 `queued` Task、发布第一条 `queued` status 事件。
8. 路由把 `TaskService.run_task(task_id)` 加入 `BackgroundTasks`，先向浏览器返回 HTTP 202。
9. React 保存 `task_id`，然后 `api.ts:subscribeToTask()` 创建 `/api/tasks/{task_id}/events` 的 `EventSource`。
10. 后台 `run_task()` 把任务改为 `running`，并发布 `Task started`。
11. `run_task()` 构造 `AnalysisState`，进入 `AnalysisWorkflow.stream()`。
12. `LangGraph` 执行 `route`，`hybrid` 被路由到 `kpi`；每个节点完成后，Service 都发布一条 status 事件。
13. `FixedKPIWorkflow.run()` 计算固定 KPI，把 `kpi_result` 合并进 State。
14. `_after_kpi()` 发现 mode 是 `hybrid`，进入 research。
15. `ResearchAgent.run()` 调用 `StaticResearchProvider`，把 `research_result` 合并进 State。
16. `ReportGenerator.generate()` 使用已有结果生成 `report_markdown`。
17. `TaskService` 将 Markdown 保存到 `ReportRepository`，把 Task 改为 `completed`，并发布 done 事件。
18. `events/sse.py:stream_task_events()` 按 sequence 将事件编码成 `event: status` 或 `event: done`，发送给浏览器。
19. `App.tsx` 的 `onEvent` 追加时间线并更新 status；收到 done 后关闭 `EventSource`，调用 `loadReport()`。
20. `api.ts:getReport()` 请求 `GET /api/tasks/{task_id}/report`，路由经 `TaskService` 从 `ReportRepository` 读取报告。
21. React `setReport()` 触发重新渲染，`ReportViewer` 用 `<pre>` 显示 Markdown。

如果中途抛出异常，`TaskService.run_task()` 的 `except` 会把 Task 改为 `failed`，并发布 `error`；React 收到后关闭 SSE，在 `role="alert"` 区域显示 `error_code` 和 `message`，不再请求报告。

## 7. 调试学习方法

### 为什么要学调试

- 学习目标：学会用断点、日志和网络面板定位问题。
- 推荐阅读文件：`backend/app/observability/logging.py`、`backend/app/main.py`、`frontend/src/api.ts`
- 推荐阅读时间：20 分钟。
- 推荐顺序：第 6 遍。
- 看完应该掌握什么：知道怎样在 Backend 和 Frontend 两边同时观察同一次请求。
- 下一步看哪里：`backend/app/observability/logging.py`

#### Backend breakpoint

在 VS Code 中打开 Backend 代码并设置断点，推荐顺序：

1. `backend/app/api/tasks.py` 的 `create_task()`：观察 Pydantic 已校验的 `payload`。
2. `backend/app/services/task_service.py` 的 `create_task()`：观察 `task_id` 和初始状态。
3. 同文件 `run_task()` 的 `async for`：每停一次查看 `node_name` 和 `state` 增加了什么。
4. `backend/app/workflow/graph.py` 的 `_kpi_node()`、`_research_node()`、`_report_node()`：观察不同 mode 会跳过哪些断点。
5. `backend/app/events/sse.py` 的 `yield` 前：查看最终发给浏览器的 SSE 字符串。

`--reload` 会启动重载子进程，普通 attach 容易连错进程。学习断点时可在 `backend/` 下直接用 VS Code Python Debugger 启动 `uvicorn`，参数使用 `app.main:app --host 127.0.0.1 --port 8000`，先不加 `--reload`。

#### 临时 print

只为快速理解局部值时，可以临时加入：

```python
print("DEBUG node=", node_name, "state keys=", list(state.keys()))
```

推荐只打印 ID、状态和字段名，不打印完整 question。验证后删除临时 `print`，避免和结构化日志混在一起。

#### 结构化 log

要观察真实执行顺序，优先看启动 Backend 的终端。日志已有 `event`、`request_id`、`task_id`、`status`、`node`、`duration_ms` 等字段。可在允许字段范围内临时增加：

```python
log_event(logger, "info", "study_checkpoint", "Reached study checkpoint",
          task_id=task_id, status="running", node="kpi")
```

先用 `request_id` 找到一次 HTTP 请求，再用 `task_id` 串起任务创建、Workflow、SSE 和报告日志。不要记录问题全文、密钥或其它敏感内容。

#### Frontend breakpoint

在浏览器 DevTools 的 Sources 中给以下位置打断点：

1. `App.tsx:submit()` 调用 `createTask()` 前后：看 `question`、`mode`、`created`。
2. `api.ts:receive()`：看原始 `message.data` 与解析后的 `TaskEvent`。
3. `App.tsx:onEvent`：比较 `status`、`done`、`error` 三种事件。
4. `App.tsx:loadReport()` 的 `setReport()`：确认报告请求发生在 `done` 之后。
5. 两个 `catch` 和 `onTransportError`：学习业务错误与网络错误的区别。

同时打开 DevTools Network：`Fetch/XHR` 中看 POST 和 report 请求，`EventStream` 中看 SSE。这样可以把源码断点和网络时序对上。

## V1.0 前端与治理阅读入口

> 增量入口，不替代上文后端主阅读顺序。

| 顺序 | 看什么                                                                    | 解决什么                   |
| ---- | ------------------------------------------------------------------------- | -------------------------- |
| A    | `frontend/src` Login / AuthContext / ProtectedRoute                     | JWT、401/403、fail-closed  |
| B    | 正式导航与业务页                                                          | 文書→RAG→分析→承認      |
| C    | Lifecycle Live Status / Learning Dashboard                                | 本地学习 trace，不回传后端 |
| D    | `backend/app` LLM Gateway / ai_analysis / executive_reports / approvals | 成本边界与审批状态机       |
| E    | RUNBOOK Appendix L/M/N、VERIFY_CHECKLIST                                  | 启动与验收数字             |

业务链记忆：

```text
文書管理 → RAG検索 → AI分析(low_cost) → 董事会报告(high_quality) → 承認管理 → Persistent Audit
```
