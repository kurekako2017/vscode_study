# Retail Insight AI 学习笔记全集（正式版 V2.0）

# Volume 02：Workflow、Learning Trace 与 LangGraph

> Chapter 03：`graph.py` 源码精读（第一部分）

------------------------------------------------------------------------

# 文档信息

  项目       内容
  ---------- -----------------
  文档版本   V2.0
  Volume     02
  Chapter    03
  状态       Draft（审阅中）

------------------------------------------------------------------------

# 本章目标

完成本章后，你将能够：

-   找到 Workflow 的真正入口。
-   理解 `AnalysisWorkflow.stream()` 如何启动 LangGraph。
-   学会阅读 `backend/app/workflow/graph.py`。
-   理解 `StateGraph` 的构建过程。

------------------------------------------------------------------------

# 1. graph.py 在哪里？

源码位置：

``` text
backend/app/workflow/graph.py
```

这是整个 AI Workflow 的核心文件。

它的职责不是执行业务，而是**组织整个 AI 工作流**。

------------------------------------------------------------------------

# 2. 谁调用 graph.py？

真实调用关系：

``` text
Browser
    │
POST /api/tasks
    │
Router
    │
TaskService.create_task()
    │
BackgroundTasks
    │
TaskService.run_task()
    │
AnalysisWorkflow.stream()
    │
graph.py
```

重点：

> **graph.py 不是 HTTP 入口，而是后台 AI Workflow 的入口。**

------------------------------------------------------------------------

# 3. 为什么不是 Router 调用 LangGraph？

项目采用分层设计：

``` text
Router
    │
Service
    │
Workflow
```

原因：

-   Router 负责 HTTP
-   Service 负责业务编排
-   Workflow 负责 AI 流程

这样每层职责单一，更容易维护。

------------------------------------------------------------------------

# 4. StateGraph()

在 `graph.py` 中，首先会创建：

``` python
workflow = StateGraph(...)
```

可以理解为：

``` text
Workflow Blueprint
        │
        ▼
StateGraph
```

此时只是创建"流程设计图"，还没有真正运行。

------------------------------------------------------------------------

# 5. add_node()

接下来会不断注册节点：

``` python
workflow.add_node(...)
```

每个 Node 表示一个业务步骤。

在 Retail Insight AI 中可以对应：

``` text
Route
   │
KPI
   │
Research
   │
Report
```

每个节点都负责一种独立能力。

------------------------------------------------------------------------

# 6. add_edge()

节点创建完成后，需要连接：

``` python
workflow.add_edge(...)
```

例如：

``` text
Route
   │
Edge
   ▼
KPI
   │
Edge
   ▼
Research
```

Edge 决定了工作流执行顺序。

------------------------------------------------------------------------

# 7. add_conditional_edges()

真实企业项目并不是所有请求都走同一条流程。

例如：

``` text
Route
 ├── fast
 │      ▼
 │   Report
 │
 └── hybrid
        ▼
    KPI
        ▼
    Research
```

条件路由根据 State 决定下一步执行哪个 Node。

------------------------------------------------------------------------

# 8. compile()

Workflow 定义完成后：

``` python
workflow.compile()
```

作用：

``` text
StateGraph
      │
      ▼
Executable Workflow
```

只有 compile() 之后，Workflow 才能真正执行。

------------------------------------------------------------------------

# 9. stream()

真正执行 Workflow：

``` python
AnalysisWorkflow.stream(...)
```

执行过程：

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

项目选择 `stream()` 而不是 `invoke()`，因为：

-   可以边执行边推送事件
-   配合 EventPublisher
-   支持 SSE 实时更新
-   更适合长时间 AI 分析

------------------------------------------------------------------------

# 10. 对应 Learning Trace

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

Learning Trace 会记录每一个节点的执行过程，帮助开发者学习和调试。

------------------------------------------------------------------------

# 11. Java 对照

  LangGraph    Java 概念
  ------------ -------------------------------
  StateGraph   Workflow Builder
  add_node()   注册处理步骤
  add_edge()   流程连接
  compile()    初始化流程
  stream()     Reactive Pipeline（概念类似）

------------------------------------------------------------------------

# Learning Tip

★★★★★

阅读 `graph.py` 时，不要先看每一行 Python。

建议先在纸上画出：

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

然后再去对应：

-   add_node()
-   add_edge()
-   compile()
-   stream()

理解速度会快很多。

------------------------------------------------------------------------

# 本章总结

`graph.py` 可以理解为：

``` text
Workflow 设计中心
        │
创建 StateGraph
        │
注册 Node
        │
连接 Edge
        │
定义 Conditional Routing
        │
compile()
        │
stream()
```

它负责组织 AI 工作流，而不是实现具体业务。

------------------------------------------------------------------------

# 下一章预告

**Volume 02 · Chapter 04：State 深度解析**

将结合 Retail Insight AI 的实际数据结构，深入讲解：

-   State 保存什么？
-   State 如何在 Node 间传递？
-   为什么 State 是 LangGraph 的核心？
