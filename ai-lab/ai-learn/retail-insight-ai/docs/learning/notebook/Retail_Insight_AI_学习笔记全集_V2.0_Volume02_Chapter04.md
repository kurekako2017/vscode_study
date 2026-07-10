# Retail Insight AI 学习笔记全集（正式版 V2.0）

# Volume 02：Workflow、Learning Trace 与 LangGraph

> Chapter 04：State 深度解析（LangGraph 的核心）

------------------------------------------------------------------------

# 文档信息

  项目       内容
  ---------- -----------------
  文档版本   V2.0
  Volume     02
  Chapter    04
  状态       Draft（审阅中）

------------------------------------------------------------------------

# 本章目标

完成本章后，你将理解：

-   什么是 Workflow State
-   State 如何在 Node 间流转
-   为什么 LangGraph 以 State 为中心
-   Retail Insight AI 中 State 的设计思想

------------------------------------------------------------------------

# 1. 什么是 State？

State（状态）可以理解为：

> **整个 AI Workflow 运行过程中的共享数据对象。**

Workflow 不同节点之间不会直接互相调用，而是通过 State 传递数据。

``` text
Route
   │
更新 State
   ▼
KPI
   │
更新 State
   ▼
Research
   │
更新 State
   ▼
Report
```

------------------------------------------------------------------------

# 2. 为什么需要 State？

如果没有 State：

``` text
Route
  │
  ├── question
  ├── mode
  ├── task_id

KPI
  │
  ├── 再传一次

Research
  │
  ├── 再传一次
```

每个函数都要传递大量参数。

使用 State 后：

``` text
State
 ├── question
 ├── mode
 ├── task_id
 ├── kpi_result
 ├── research_result
 └── report
```

所有节点共享同一个上下文。

------------------------------------------------------------------------

# 3. Retail Insight AI 中的 State

虽然具体字段会随着项目演进而变化，但通常会包含：

``` text
WorkflowState
├── task_id
├── question
├── mode
├── route
├── kpi_result
├── research_result
├── report
└── status
```

这些数据会随着 Workflow 执行不断更新。

------------------------------------------------------------------------

# 4. State 的生命周期

``` text
TaskService.run_task()
        │
创建初始 State
        │
Route
        │
更新 State
        │
KPI
        │
更新 State
        │
Research
        │
更新 State
        │
Report
        │
最终 State
```

最终 Report 也是 State 的一部分。

------------------------------------------------------------------------

# 5. State 与 Node 的关系

Node 的职责不是保存数据。

Node：

-   读取 State
-   处理业务
-   更新 State
-   返回新的 State

``` text
State
   │
Node
   │
New State
```

因此：

**State 是数据，Node 是行为。**

------------------------------------------------------------------------

# 6. State 与 Learning Trace

Learning Trace 记录的是：

``` text
Route
 ↓
KPI
 ↓
Research
 ↓
Report
```

真正的数据变化发生在 State 中。

因此：

-   Learning Trace：记录执行过程
-   State：保存执行结果

两者职责不同。

------------------------------------------------------------------------

# 7. 企业为什么这样设计（Why）

如果每个 Node 都保存自己的数据：

``` text
Route
Question

KPI
Question

Research
Question
```

容易出现：

-   数据不同步
-   参数越来越多
-   修改困难

统一 State 后：

``` text
WorkflowState
       │
所有 Node 共用
```

更容易维护和扩展。

------------------------------------------------------------------------

# 8. Java 对照

  LangGraph         Java 概念
  ----------------- -----------------
  State             Context / DTO
  WorkflowState     Process Context
  Node 更新 State   修改共享上下文

------------------------------------------------------------------------

# 9. Learning Tip

★★★★★

阅读 graph.py 时，请始终思考两个问题：

1.  当前 Node 从 State 中读取了什么？
2.  当前 Node 往 State 中写回了什么？

这样比只看 Python 代码更容易理解 Workflow。

------------------------------------------------------------------------

# 本章总结

一句话记忆：

``` text
State
   │
Node A
   │
State
   │
Node B
   │
State
   │
Node C
```

Workflow 的核心不是 Node，而是不断流转、不断更新的 **State**。

------------------------------------------------------------------------

# 下一章预告

**Volume 02 · Chapter 05：Node 深度解析**

将结合 Retail Insight AI 的 KPI、Research、Report 节点，讲解：

-   Node 如何设计
-   Node 如何更新 State
-   Node 如何组合成完整 AI Workflow
