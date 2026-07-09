# Retail Insight AI 源码精读系列

# 03_graph.py.md

> Source Code Deep Dive

------------------------------------------------------------------------

# 文档信息

  -----------------------------------------------------------------------
  项目                                内容
  ----------------------------------- -----------------------------------
  系列                                Source Code Deep Dive

  文档                                03

  主题                                backend/app/workflow/graph.py

  对应源码                            backend/app/workflow/graph.py

  关联文档                            01_TaskService_run_task.md /
                                      02_AnalysisWorkflow_stream.md

  难度                                ★★★★☆
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 学习目标

阅读完本文后，你应该能够回答：

-   `graph.py` 在整个项目中负责什么？
-   `AnalysisWorkflow` 为什么放在 `workflow/graph.py` 中？
-   `StateGraph`、Node、Edge、Conditional Routing 在源码中分别对应什么？
-   `graph.py` 与
    `TaskService.run_task()`、`Learning Trace`、`EventPublisher`
    的关系是什么？

------------------------------------------------------------------------

# 一、源码位置

``` text
backend/app/workflow/graph.py
```

这是 Retail Insight AI 中 AI Workflow 的核心文件。

它不是 HTTP 入口，也不是 Service 层，而是：

> **后台 AI 分析流程的编排中心。**

------------------------------------------------------------------------

# 二、谁调用 graph.py？

真实调用链：

``` text
Browser
    │
POST /api/tasks
    │
backend/app/api/tasks.py
    │
create_task()
    │
TaskService.create_task()
    │
BackgroundTasks.add_task()
    │
HTTP 202 返回
    │
TaskService.run_task()
    │
AnalysisWorkflow.stream()
    │
backend/app/workflow/graph.py
```

重点：

> `graph.py` 是在 Background 阶段被调用的，不是在 Request
> 阶段直接调用的。

------------------------------------------------------------------------

# 三、graph.py 的核心职责

`graph.py` 负责：

``` text
创建 Workflow
    │
定义 State
    │
注册 Node
    │
连接 Edge
    │
设置条件路由
    │
执行 stream()
```

可以理解为：

> **它负责设计和执行 AI 分析流程。**

------------------------------------------------------------------------

# 四、为什么叫 graph.py？

因为 LangGraph 的核心思想是：

``` text
Node + Edge = Graph
```

也就是：

``` text
Route Node
    │
    ▼
KPI Node
    │
    ▼
Research Node
    │
    ▼
Report Node
```

这些节点和连接线组合起来，就是一个 Graph。

------------------------------------------------------------------------

# 五、graph.py 不负责什么？

`graph.py` 不负责：

-   接收 HTTP 请求
-   解析 Request Body
-   直接返回 HTTP Response
-   直接操作前端页面
-   决定 API 路由

这些职责分别属于：

  职责          所属位置
  ------------- ---------------------------------
  HTTP 请求     `backend/app/api/`
  业务编排      `backend/app/services/`
  数据保存      `backend/app/repositories/`
  AI Workflow   `backend/app/workflow/graph.py`
  前端通知      `backend/app/events/` + SSE

------------------------------------------------------------------------

# 六、graph.py 的整体结构

可以把 `graph.py` 理解成下面结构：

``` text
graph.py
│
├── Workflow State
│
├── AnalysisWorkflow
│
├── Route Node
│
├── KPI Node
│
├── Research Node
│
├── Report Node
│
├── Edges
│
├── Conditional Routing
│
└── stream()
```

------------------------------------------------------------------------

# 七、StateGraph

在 LangGraph 中，通常会先创建 `StateGraph`。

概念上可以理解为：

``` text
StateGraph
    │
    ├── 管理 State
    ├── 注册 Node
    ├── 管理 Edge
    └── 编译成可执行 Workflow
```

`StateGraph` 不是业务结果，而是 Workflow 的设计图。

------------------------------------------------------------------------

# 八、Node

Node 是 Graph 中的处理步骤。

Retail Insight AI 中常见 Node：

``` text
Route
KPI
Research
Report
```

每个 Node 只负责一件事情：

  Node       职责
  ---------- ---------------------------
  Route      判断执行路线
  KPI        执行 KPI 分析
  Research   执行调研 / 检索 / AI 分析
  Report     生成最终报告

------------------------------------------------------------------------

# 九、Edge

Edge 表示 Node 之间的连接。

例如：

``` text
Route
  │
  ▼
KPI
```

这条箭头就是 Edge。

在源码中通常对应：

``` text
add_edge()
```

或者条件边：

``` text
add_conditional_edges()
```

------------------------------------------------------------------------

# 十、Conditional Routing

条件路由用于根据 State 决定下一步。

例如：

``` text
Route
 ├── fixed
 │     ▼
 │   KPI
 │
 └── hybrid
       ▼
    Research
```

它的价值在于：

> 同一个 Workflow 可以根据输入条件走不同路线。

这也是 AI Agent / AI Workflow 和普通线性程序的重要区别。

------------------------------------------------------------------------

# 十一、compile()

Graph 定义完成后，需要 compile。

概念上：

``` text
StateGraph
    │
compile()
    │
Executable Workflow
```

可以把它理解成：

> 把流程设计图变成真正可执行的 Workflow。

------------------------------------------------------------------------

# 十二、stream()

`stream()` 是执行 Workflow 的重要方式。

``` text
Workflow.stream()
    │
Route 完成 → 产出事件
    │
KPI 完成 → 产出事件
    │
Research 完成 → 产出事件
    │
Report 完成 → 产出结果
```

Retail Insight AI 使用 stream 的原因：

-   AI 分析可能耗时
-   需要实时更新状态
-   可以配合 EventPublisher
-   可以配合 SSE 推送前端

------------------------------------------------------------------------

# 十三、与 TaskService.run_task() 的关系

`TaskService.run_task()` 负责启动后台任务。

`AnalysisWorkflow.stream()` 负责执行 AI Workflow。

关系：

``` text
TaskService.run_task()
        │
        ▼
AnalysisWorkflow.stream()
        │
        ▼
graph.py
```

所以：

-   Service 是业务调度者
-   Workflow 是流程执行者
-   Graph 是流程结构本身

------------------------------------------------------------------------

# 十四、与 Learning Trace 的关系

Learning Trace 记录的是 graph.py 的执行顺序：

``` text
Background
    │
AnalysisWorkflow.stream()
    │
Route
    │
KPI
    │
Research
    │
Report
```

这帮助开发者理解：

> 后台任务到底执行到了哪一步。

------------------------------------------------------------------------

# 十五、与 EventPublisher 的关系

Workflow 执行过程中，会发布事件：

``` text
graph.py
    │
Node 执行完成
    │
EventPublisher.publish()
    │
SSE
    │
Frontend
```

因此：

-   graph.py 推动 AI 流程
-   EventPublisher 发布状态
-   SSE 推送给浏览器

三者职责不同，但配合完成实时分析体验。

------------------------------------------------------------------------

# 十六、企业为什么这样设计（Why）

如果没有 graph.py：

``` text
TaskService.run_task()
 ├── route()
 ├── kpi()
 ├── research()
 ├── report()
 ├── save()
 ├── publish()
 └── error handling
```

`run_task()` 会变成一个巨大函数。

有了 graph.py：

``` text
TaskService.run_task()
    │
    ▼
AnalysisWorkflow.stream()
    │
    ▼
graph.py
```

优点：

-   Service 变简单
-   Workflow 可扩展
-   Node 可替换
-   流程清晰
-   更适合 Agent / RAG / 多步骤 AI 分析

------------------------------------------------------------------------

# 十七、Java / Spring 对照

  Retail Insight AI     Java / Spring 概念
  --------------------- --------------------------------------
  graph.py              Workflow Configuration
  StateGraph            State Machine / Process Builder
  Node                  Step / Handler
  Edge                  Step Transition
  Conditional Routing   Strategy / Condition Branch
  stream()              Reactive Pipeline / Stream Execution

------------------------------------------------------------------------

# 十八、面试回答

如果面试官问：

> `graph.py` 在项目中负责什么？

可以回答：

> `graph.py` 是 Retail Insight AI 中 AI Workflow
> 的核心编排文件。它定义了分析流程中的 State、Node、Edge
> 和条件路由，并通过 `AnalysisWorkflow.stream()` 在后台任务中执行
> Route、KPI、Research、Report 等节点。它将复杂的 AI 分析流程从 Service
> 层中拆分出来，使业务流程更清晰、更容易扩展，也更适合后续接入
> LangGraph、LangChain 和 RAG。

------------------------------------------------------------------------

# 十九、源码阅读建议

建议阅读顺序：

``` text
01_TaskService_run_task.md
    │
    ▼
02_AnalysisWorkflow_stream.md
    │
    ▼
03_graph.py.md
    │
    ▼
04_trace_step.md
    │
    ▼
05_EventPublisher.md
```

不要一开始就看 `add_node()` 的实现细节。

先理解：

``` text
graph.py = Workflow 编排中心
```

再看具体 Node 和 Edge。

------------------------------------------------------------------------

# 本章总结

一句话记住：

``` text
graph.py
=
AI Workflow 的流程图和执行编排中心
```

它负责：

-   定义 State
-   注册 Node
-   连接 Edge
-   设置条件路由
-   执行 stream
-   将 AI 分析拆成可维护的工作流

------------------------------------------------------------------------

# 下一章

**04_trace_step.md**

将继续精读：

-   `trace_step()` 是什么？
-   它为什么不是业务逻辑？
-   它如何记录 Learning Trace？
-   它和 Console Log、Execution Flow 的关系是什么？
