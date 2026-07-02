# CODE STUDY GUIDE

这份指南面向第一次阅读 React、FastAPI 和 LangGraph 项目的学习者。建议先把 Backend 和 Frontend 都运行起来，再按本文顺序阅读；每读到一个步骤，就在页面或日志中观察它的实际效果。

> 路径说明：下文路径都相对于 `retail-insight-ai/`。需求中提到的 `api/routes/tasks.py` 在本项目中的实际路径是 `backend/app/api/tasks.py`，项目没有 `api/routes/` 这一层。

## 1. 项目整体运行流程

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
  用固定规则生成确定性指标（research 模式跳过）
    ↓
Research
  调用本地 StaticResearchProvider（kpi 模式跳过）
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

当前实现全部使用进程内存储和本地固定数据：不调用真实 LLM，不需要 PostgreSQL、Redis 或 RabbitMQ。Backend 重启后，任务、事件和报告都会丢失。

## 2. 后端阅读顺序

第一次阅读时不要从每个目录的 `__init__.py` 开始。按一次请求从外到内、再从内到外的顺序读：

1. `backend/app/main.py`：应用怎样启动、挂载路由和建立 `request_id`。
2. `backend/app/api/tasks.py`：四个任务 API 怎样接收和返回数据。
3. `backend/app/services/task_service.py`：任务生命周期和完整业务用例。
4. `backend/app/workflow/graph.py`，再读 `workflow/state.py`：Node、Edge、State 和模式分支。
5. `backend/app/kpi/workflow.py`：KPI 的固定计算规则。
6. `backend/app/agents/research_agent.py`，再读 `agents/providers/static_research.py`：Research 抽象与本地实现。
7. `backend/app/reports/generator.py`：最终 Markdown 如何拼装。
8. `backend/app/events/publisher.py`，再读 `events/sse.py`：事件怎样保存并编码成 SSE。
9. `backend/app/repositories/interfaces/`，再读 `repositories/implementations/in_memory/`：为什么业务层不直接依赖字典。
10. 第二轮再补读 `config/container.py`、`schemas/`、`models/`、`errors/` 和 `observability/logging.py`。

阅读 `workflow/graph.py` 时，分别用 `hybrid`、`kpi`、`research` 三种 mode 在纸上画路径：

```text
hybrid:  route → kpi → research → report
kpi:     route → kpi → report
research: route → research → report
```

## 3. 前端阅读顺序

1. `frontend/src/App.tsx`：先看顶部的七个 `useState`，理解页面保存了哪些状态。
2. `frontend/src/api.ts`：看 HTTP 请求、统一响应解包和 EventSource 订阅。
3. 回到 `App.tsx` 的 `submit()`：任务提交逻辑，重点看提交前重置状态和 `createTask()`。
4. 顺着 `subscribeToTask()` 阅读 SSE 监听逻辑：`status`、`done`、`error` 都进入 `onEvent`。
5. 看 `loadReport()` 及文件末尾的 ReportViewer：收到 `done` 后才加载并展示报告。
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

## 4. 核心文件说明

| 文件路径 | 负责什么 | 为什么需要 | 运行时什么时候被调用 | 初学者重点看哪里 |
| --- | --- | --- | --- | --- |
| `backend/app/main.py` | 创建 FastAPI、构造容器、注册 CORS/路由/异常处理和请求日志中间件 | 提供唯一的应用入口和 HTTP 外壳 | Uvicorn 导入 `app.main:app` 时；每个请求还会经过 middleware | `create_app()`、`request_context()`、`include_router()` |
| `backend/app/api/tasks.py` | 创建任务、查状态、订阅事件、取报告 | 把 HTTP 协议转换成 Service 调用 | 请求 `/api/tasks...` 时 | `create_task()` 中的 `BackgroundTasks`，以及 `StreamingResponse` |
| `backend/app/services/task_service.py` | 创建任务、推进状态、执行 Workflow、保存报告、发布事件、收敛异常 | 把一次完整用例放在一处，避免路由和节点各自管理生命周期 | 路由创建/查询任务时；后台任务运行时 | `create_task()` 与 `run_task()` 的成功/失败两条路径 |
| `backend/app/workflow/state.py` | 定义节点共享的 `AnalysisState` | 让每个节点的输入输出字段清晰且可检查 | Workflow 创建和每个节点运行时 | 必填字段与可选结果字段 |
| `backend/app/workflow/graph.py` | 声明 route/kpi/research/report 节点和条件边 | 把执行顺序显式化，并支持三种 mode | `TaskService.run_task()` 调用 `stream()` 时 | `_build_graph()`、`_after_route()`、`_after_kpi()`、增量 state 合并 |
| `backend/app/kpi/workflow.py` | 根据固定规则产生 `KPIResult` | KPI 公式必须可重复，不交给模型猜测 | kpi 节点运行时 | `question_factor` 和每个 KPI 字段 |
| `backend/app/agents/research_agent.py` | 通过 Provider 执行调查并校验结果 | 隔离“如何调查”与 Workflow 编排 | research 节点运行时 | `ResearchAgent.run()` 如何只依赖 Provider 接口 |
| `backend/app/agents/providers/static_research.py` | 返回固定 Research 结果，可注入失败 | 本地学习时不依赖网络或真实 LLM | `ResearchAgent.run()` 调用 provider 时 | 正常返回和 `fail` 分支 |
| `backend/app/reports/generator.py` | 把问题、KPI 和 Research 组合成 Markdown | 三种 mode 需要同一种报告输出 | report 节点运行时 | 两个可选结果的 `if` 和 `lines` 列表 |
| `backend/app/events/publisher.py` | 创建业务事件并写入 EventRepository | Workflow/Service 不需要知道事件存储细节 | queued、running、节点完成、done/error 时 | 自动补入 `request_id` |
| `backend/app/events/sse.py` | 轮询事件、转换为 SSE 文本、在终态结束连接 | 浏览器需要实时看到进度 | 浏览器连接 `/events` 后 | `id/event/data` 三行格式、cursor、终态 return |
| `backend/app/repositories/interfaces/` | 定义 Task/Event/Report 存储合同 | Service 依赖抽象，存储实现可替换 | 容器构造和类型检查时 | `Protocol` 中最小方法集合 |
| `backend/app/repositories/implementations/in_memory/` | 用字典、锁和深拷贝保存运行数据 | 提供无需外部数据库的本地实现 | 任务和事件每次读写时 | 为什么返回 `deepcopy`，为什么使用 `RLock` |
| `backend/app/config/container.py` | 创建并连接 Repository、Agent、Workflow、Service | 具体实现只在组合根出现 | FastAPI 应用创建时一次 | `build_container()` 的依赖连接顺序 |
| `backend/app/schemas/task_api.py` | 定义任务请求和响应的 Pydantic Schema | 在 HTTP 边界校验输入并固定合同 | FastAPI 解析请求/序列化响应时 | `question` 长度、`mode` 限制和 `from_domain()` |
| `backend/app/observability/logging.py` | JSON 日志、request_id 上下文和安全字段 | 将同一请求/任务的日志关联起来 | 应用启动、每个请求和业务关键步骤 | `bind_request_id()`、`log_event()` 允许的字段 |
| `frontend/src/App.tsx` | 页面状态、提交、SSE 回调、报告加载和渲染 | 把完整用户流程集中展示 | React 首次渲染和每次用户/网络事件发生时 | `submit()`、`loadReport()`、函数式 `setEvents()`、清理 EventSource |
| `frontend/src/api.ts` | 封装 fetch、响应解包和 EventSource | UI 不直接处理 HTTP/SSE 细节 | `App.tsx` 创建任务、订阅或取报告时 | `unwrapResponse()`、`subscribeToTask()`、业务 error 与 transport error 的区别 |
| `frontend/src/types.ts` | 定义 API 和 SSE 的 TypeScript 类型 | 编译期发现前后端合同不一致 | TypeScript 编译和开发时 | `TaskEvent` 与 Backend `TaskEventResponse` 的字段对应 |
| `frontend/src/App.test.tsx` | 模拟 fetch/EventSource 验证完整 UI 流程 | 不启动浏览器也能稳定验证成功和错误显示 | 执行 Frontend tests 时 | `FakeEventSource.emit()` 如何驱动真实 React 回调 |

## 5. 一次完整任务的源码调用链

以页面默认的 `hybrid` 任务为例：

1. 用户点击 `App.tsx` 中的“分析を開始”按钮，浏览器触发表单 `onSubmit={submit}`。
2. `submit()` 阻止页面刷新，关闭旧 SSE，清空旧 task、events、report 和 error。
3. `submit()` 调用 `api.ts:createTask()`，浏览器发送 `POST /api/tasks`。
4. Vite 开发代理把 `/api` 请求转发到 `http://127.0.0.1:8000`。
5. `main.py:request_context()` 生成或读取 `X-Request-ID`，绑定日志上下文。
6. FastAPI 用 `TaskCreateRequest` 校验 question 和 mode，再调用 `api/tasks.py:create_task()`。
7. 路由调用 `TaskService.create_task()`：生成 task_id，保存 queued Task，发布第一条 queued status 事件。
8. 路由把 `TaskService.run_task(task_id)` 加入 `BackgroundTasks`，先向浏览器返回 HTTP 202。
9. React 保存 task_id，然后 `api.ts:subscribeToTask()` 创建 `/api/tasks/{task_id}/events` 的 EventSource。
10. 后台 `run_task()` 把任务改为 running，并发布 `Task started`。
11. `run_task()` 构造 `AnalysisState`，进入 `AnalysisWorkflow.stream()`。
12. LangGraph 执行 `route`，hybrid 被路由到 `kpi`；每个节点完成后，Service 都发布一条 status 事件。
13. `FixedKPIWorkflow.run()` 计算固定 KPI，把 `kpi_result` 合并进 State。
14. `_after_kpi()` 发现 mode 是 hybrid，进入 research。
15. `ResearchAgent.run()` 调用 `StaticResearchProvider`，把 `research_result` 合并进 State。
16. `ReportGenerator.generate()` 使用已有结果生成 `report_markdown`。
17. `TaskService` 将 Markdown 保存到 ReportRepository，把 Task 改为 completed，并发布 done 事件。
18. `events/sse.py:stream_task_events()` 按 sequence 将事件编码成 `event: status` 或 `event: done`，发送给浏览器。
19. `App.tsx` 的 `onEvent` 追加时间线并更新 status；收到 done 后关闭 EventSource，调用 `loadReport()`。
20. `api.ts:getReport()` 请求 `GET /api/tasks/{task_id}/report`，路由经 TaskService 从 ReportRepository 读取报告。
21. React `setReport()` 触发重新渲染，ReportViewer 用 `<pre>` 显示 Markdown。

如果中途抛出异常，`TaskService.run_task()` 的 `except` 会把 Task 改为 failed，并发布 error；React 收到后关闭 SSE，在 `role="alert"` 区域显示 error_code 和 message，不再请求报告。

## 6. Debug 学习方法

### 6.1 Backend breakpoint

在 VS Code 中打开 Backend 代码并设置断点，推荐顺序：

1. `backend/app/api/tasks.py` 的 `create_task()`：观察 Pydantic 已校验的 `payload`。
2. `backend/app/services/task_service.py` 的 `create_task()`：观察 task_id 和初始状态。
3. 同文件 `run_task()` 的 `async for`：每停一次查看 `node_name` 和 `state` 增加了什么。
4. `backend/app/workflow/graph.py` 的 `_kpi_node()`、`_research_node()`、`_report_node()`：观察不同 mode 会跳过哪些断点。
5. `backend/app/events/sse.py` 的 `yield` 前：查看最终发给浏览器的 SSE 字符串。

`--reload` 会启动重载子进程，普通 attach 容易连错进程。学习断点时可在 `backend/` 下直接用 VS Code Python Debugger 启动 `uvicorn`，参数使用 `app.main:app --host 127.0.0.1 --port 8000`，先不加 `--reload`。

### 6.2 临时 print

只为快速理解局部值时，可以临时加入：

```python
print("DEBUG node=", node_name, "state keys=", list(state.keys()))
```

推荐只打印 ID、状态和字段名，不打印完整 question。验证后删除临时 `print`，避免和结构化日志混在一起。

### 6.3 结构化 log

要观察真实执行顺序，优先看启动 Backend 的终端。日志已有 `event`、`request_id`、`task_id`、`status`、`node`、`duration_ms` 等字段。可在允许字段范围内临时增加：

```python
log_event(logger, "info", "study_checkpoint", "Reached study checkpoint",
          task_id=task_id, status="running", node="kpi")
```

先用 `request_id` 找到一次 HTTP 请求，再用 `task_id` 串起任务创建、Workflow、SSE 和报告日志。不要记录问题全文、密钥或其它敏感内容。

### 6.4 Frontend breakpoint

在浏览器 DevTools 的 Sources 中给以下位置打断点：

1. `App.tsx:submit()` 调用 `createTask()` 前后：看 question、mode、created。
2. `api.ts:receive()`：看原始 `message.data` 与解析后的 TaskEvent。
3. `App.tsx:onEvent`：比较 status、done、error 三种事件。
4. `App.tsx:loadReport()` 的 `setReport()`：确认报告请求发生在 done 之后。
5. 两个 `catch` 和 `onTransportError`：学习业务错误与网络错误的区别。

同时打开 DevTools Network：`Fetch/XHR` 中看 POST 和 report 请求，`EventStream` 中看 SSE。这样可以把源码断点和网络时序对上。

## 7. 十个小练习

每次只做一个练习，修改前先运行 `./scripts/run_tests.sh`，修改后再运行一次。练习不要求一次全部提交。

1. **改报告标题**：修改 `reports/generator.py` 的第一行标题，并同步更新 `backend/tests/test_api.py` 的断言。
2. **改 KPI 文案**：只把报告中的“売上高”换成另一段显示文案，不修改 `KPIResult` 字段和计算公式。
3. **改 SSE status 文案**：修改 `TaskService.run_task()` 中 `messages["kpi"]`，在页面时间线确认变化。
4. **增加一个日志字段**：给 `kpi_completed` 增加已有安全字段，例如 `status="running"`（若已存在，可选择 `node`），并在日志测试中验证。
5. **增加一个 Backend 测试**：新增 research-only 测试，断言报告有 Research、没有 KPI。
6. **增加一个 Frontend 测试**：模拟 report 请求失败，断言 Error Panel 显示 `REPORT_LOAD_ERROR`。
7. **观察三条路径**：依次提交 hybrid、kpi、research，记录每条路径收到的 node 顺序，不改代码。
8. **观察输入如何影响 KPI**：提交两个不同长度的问题，比较销售额，并从 `question_factor` 解释差异。
9. **练习断线清理**：在 `subscribeToTask()` 返回的关闭函数处打断点，重复提交或卸载组件，确认旧 EventSource 被关闭。
10. **增加一个请求校验测试**：在 Backend 测试中提交未知 mode，断言 HTTP 422、`VALIDATION_ERROR` 和 request_id；不改变 Schema。

练习修改必须继续遵守本项目边界：使用 Static Provider 和 InMemory Repository，不接真实 LLM，不引入外部基础设施。

<!-- DOC-SYNC:START group=study-and-runbook -->
## 文档同步块

- group: `study-and-runbook`
- file: `retail-insight-ai/CODE_STUDY_GUIDE.md`
- self_sha256: `7835d7b286bdaad961b008b3623bf07ff31edf644e60239270d09e108eded449`
- peers:
- `retail-insight-ai/RUNBOOK_LOCAL.md` | sha256=82e649ea6d4a1124aef7bac0e5296b5bbd4077586f02199892583fefaf930f1a | # RUNBOOK_LOCAL / 这份手册用于在 VS Code + WSL Ubuntu 中，从零启动 Retail Insight AI，并亲自验证 Backend、Frontend、SSE 和 Report 全流程。所有命令默认在 WSL Ubuntu 终端执行。 / ## 1. 前提条件 / 需要以下工具：
- `retail-insight-ai/VERIFY_CHECKLIST.md` | sha256=a102715dbf95744db73011bb1df9cd7999da3fc9d576d4677eb230a34d77b925 | # VERIFY CHECKLIST / 所有命令默认先进入项目根目录： / ```bash / cd ~/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai
- `retail-insight-ai/STUDY_PLAN_DAY1_DAY3.md` | sha256=23659aa081e315f7a7cf87c0e3266ad81620d0b0577954f4138c7a1280b6f7c5 | # Retail Insight AI 学习计划（Day1～Day3） / 这是一份面向初学者的“边运行、边阅读、边验证”学习计划。所有路径都相对于 `retail-insight-ai/` 项目根目录；命令均可直接复制到 WSL Ubuntu 的 Bash 终端执行。 / ## 三天学习目标 / 通过三天时间，完成以下目标：
- `ai-agent-retail-handbook-v3/01_日本AI项目实战.md` | sha256=aa0cf1068c64dbdeedf2f1f5e38d235fab7d19a23aa2ad23ceee7645ac7ebac1 | # 01_日本AI项目实战 / ## 目录 / - [第一章 项目概述](#第一章-项目概述) / - [第二章 行业背景](#第二章-行业背景)
- `ai-agent-retail-handbook-v3/04_日本现场开发.md` | sha256=bca69b09dcf09db6f0869f4af8121a3d7f4e280757c8e377cd761370c68295e5 | # 04_日本现场开发 / ## 第一章 日本现场开发总流程 / Retail Insight AI 按日本现场流程推进：需求整理、基本設計、詳細設計、API 設計、開発、単体試験、結合試験、レビュー、部署、保守改修。 / 【TL Review】
- `ai-agent-retail-handbook-v3/05_TL代码审查.md` | sha256=797c312f4566abe80afb5f87dbbf97b22d983195cb9610de8de81f47af01c9c3 | # 05_TL代码审查 / ## 第一章 Review 总原则 / TL Review 的目标是确认 Retail Insight AI 能支撑日本小売業客户的经营分析、运用监视、障害対応和保守改修。 / 【TL Review】
- `ai-agent-retail-handbook-v3/06_学习路线.md` | sha256=1b39176bff4feb5bcde639affcec4036334622aca73dac53c321b649d8c11e3f | # 06_学习路线 / ## 第一章 成长目标 / 目标是能够在日本 AI Agent 现场说明 Retail Insight AI 的业务背景、系统架构、担当范围、设计决策、Review 观点和运用扩展。 / 【TL Review】
- `ai-agent-retail-handbook-v3/11_Project_Structure.md` | sha256=a40c03fd0eadeb68466c3a44a53ddf58769d104af40d37f6b658135157ef09bb | # 11_Project_Structure / # 目录 / - [1. 设计目标](#1-设计目标) / - [2. 顶层目录](#2-顶层目录)

说明：
- 这个块由 `scripts/sync_retail_handbook_docs.py` 自动维护。
- 只同步这个块，不覆盖各自正文。
- 任一组内文档正文变化时，整组文档的同步块都会一起刷新。
<!-- DOC-SYNC:END group=study-and-runbook -->
