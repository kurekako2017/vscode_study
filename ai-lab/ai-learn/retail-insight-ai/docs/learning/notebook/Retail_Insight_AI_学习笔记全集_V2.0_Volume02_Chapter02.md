# Retail Insight AI 学习笔记全集（正式版 V2.0）
> **历史学习笔记**：项目现名 ERIP V1.0；本文保留教学叙述。现状数字与架构以 handbook 权威材料与源码为准。


# Volume 02：Workflow、Learning Trace 与 LangGraph

> Chapter 02：LangGraph 核心概念（State / Node / Edge）

------------------------------------------------------------------------

# 文档信息

  项目       内容
  ---------- -----------------
  文档版本   V2.0
  Volume     02
  Chapter    02
  状态       Draft（审阅中）

------------------------------------------------------------------------

# 本章目标

完成本章后，你将能够：

-   理解 LangGraph 为什么出现。
-   理解 State、Node、Edge 的概念。
-   理解 Conditional Routing、compile()、stream()。
-   对照 `backend/app/workflow/graph.py` 阅读源码。

------------------------------------------------------------------------

# 1. 为什么需要 LangGraph？

传统 AI 程序通常是：

``` text
Question
   │
   ▼
LLM
   │
   ▼
Answer
```

当流程变复杂时：

``` text
Question
   │
Route
 ├── KPI
 ├── Research
 └── Report
```

代码会越来越难维护。

LangGraph 就是专门解决**AI 工作流编排（Workflow
Orchestration）**的问题。

------------------------------------------------------------------------

# 2. LangGraph 在 Retail Insight AI 中的位置

``` text
TaskService.run_task()
        │
        ▼
AnalysisWorkflow.stream()
        │
        ▼
StateGraph
        │
        ├── State
        ├── Node
        ├── Edge
        └── Conditional Routing
```

真正负责组织 AI 流程的是 `StateGraph`。

------------------------------------------------------------------------

# 3. State（状态）

State 可以理解为：

> **整个 Workflow 在运行过程中共享的数据。**

例如：

``` text
State
├── question
├── mode
├── task_id
├── kpi_result
├── research_result
└── report
```

每个 Node 都可以读取或更新 State。

------------------------------------------------------------------------

# 4. Node（节点）

Node 表示 Workflow 中的一个处理步骤。

在本项目中可以理解为：

``` text
Route
KPI
Research
Report
```

执行顺序：

``` text
Route
   │
   ▼
KPI
   │
   ▼
Research
   │
   ▼
Report
```

每个 Node 只负责一件事情。

------------------------------------------------------------------------

# 5. Edge（边）

Edge 用来连接两个 Node。

``` text
Route
   │
Edge
   ▼
KPI
```

它定义了**下一步执行谁**。

------------------------------------------------------------------------

# 6. Conditional Routing（条件路由）

企业 Workflow 很少只有固定流程。

例如：

``` text
Route
 ├── hybrid
 │      │
 │      ▼
 │   Research
 │
 └── fast
        │
        ▼
     Report
```

根据 State 中的数据决定下一步执行哪个 Node，这就是条件路由。

------------------------------------------------------------------------

# 7. compile()

Workflow 创建完成后，需要：

``` text
StateGraph
      │
      ▼
compile()
      │
      ▼
Executable Workflow
```

可以把它理解为：

> **把设计图编译成真正可执行的工作流。**

------------------------------------------------------------------------

# 8. stream() 与 invoke()

## 方法：invoke()

``` text
Workflow
    │
执行
    │
最终返回结果
```

适合同步任务。

------------------------------------------------------------------------

## 方法：stream()

``` text
Workflow
    │
执行
    │
边执行边返回事件
```

Retail Insight AI 使用 `stream()`，因为：

-   可以实时更新进度
-   可以配合 EventPublisher
-   可以通过 SSE 推送给前端

------------------------------------------------------------------------

# 9. Learning Trace 对照

``` text
TaskService.run_task()
        │
trace_step()
        │
AnalysisWorkflow.stream()
        │
trace_step()
        │
Route
        │
trace_step()
        │
KPI
        │
Research
        │
Report
```

Learning Trace 记录了 Workflow 的每一步执行阶段。

------------------------------------------------------------------------

# 10. Java 对照

  LangGraph             Java 概念
  --------------------- -----------------------------
  State                 Context / DTO
  Node                  Service Step
  Edge                  流程连接
  Conditional Routing   if / Strategy
  compile()             初始化流程
  stream()              Reactive Stream（概念类似）

------------------------------------------------------------------------

# Learning Tip

★★★★★

阅读 `graph.py` 时，请不要先看代码。

先画出：

``` text
State
   │
Route
   │
KPI
   │
Research
   │
Report
```

理解流程后，再去阅读 `add_node()`、`add_edge()` 等源码，会轻松很多。

------------------------------------------------------------------------

# 下一章预告

**Volume 02 · Chapter 03：graph.py 源码精读（第一部分）**

将结合 Retail Insight AI 的真实
`backend/app/workflow/graph.py`，逐段解析：

-   StateGraph()
-   add_node()
-   add_edge()
-   add_conditional_edges()
-   compile()
