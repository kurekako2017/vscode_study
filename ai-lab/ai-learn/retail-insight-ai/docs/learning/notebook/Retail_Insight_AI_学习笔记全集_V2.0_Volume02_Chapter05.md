# Retail Insight AI 学习笔记全集（正式版 V2.0）

# Volume 02：Workflow、Learning Trace 与 LangGraph

> Chapter 05：Node 深度解析（Route / KPI / Research / Report）

------------------------------------------------------------------------

# 文档信息

  项目       内容
  ---------- -----------------
  文档版本   V2.0
  Volume     02
  Chapter    05
  状态       Draft（审阅中）

------------------------------------------------------------------------

# 本章目标

完成本章后，你将能够：

-   理解 LangGraph 中 Node 的真正职责。
-   理解 Retail Insight AI 中四个核心节点的作用。
-   理解 Node 如何读取和更新 State。
-   学会分析一个 AI Workflow 节点。

------------------------------------------------------------------------

# 1. 什么是 Node？

Node（节点）是 Workflow 中**完成一个独立业务步骤**的处理单元。

可以把它理解为：

> **Node = 一个只做一件事情的函数。**

Node 不负责整个流程，只负责自己的任务。

------------------------------------------------------------------------

# 2. Retail Insight AI 的 Workflow

``` text
AnalysisWorkflow.stream()
        │
        ▼
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

这四个节点共同组成完整的 AI 分析流程。

------------------------------------------------------------------------

# 3. Route 节点

## 职责

决定 Workflow 下一步应该如何执行。

## 输入

``` text
State
├── question
├── mode
```

## 输出

``` text
State
└── route
```

## 为什么存在？

Route 将"流程判断"与"业务处理"分离，使后续节点无需关心执行策略。

------------------------------------------------------------------------

# 4. KPI 节点

## 职责

生成 KPI 分析结果。

## 输入

``` text
question
route
```

## 输出

``` text
kpi_result
```

KPI 节点只负责 KPI，不负责 Research 或 Report。

------------------------------------------------------------------------

# 5. Research 节点

## 职责

结合数据、知识或模型完成分析。

## 输入

``` text
question
kpi_result
```

## 输出

``` text
research_result
```

这一节点通常也是未来接入 LangChain、RAG 或互联网搜索的位置。

------------------------------------------------------------------------

# 6. Report 节点

## 职责

整合所有分析结果，生成最终报告。

## 输入

``` text
kpi_result
research_result
```

## 输出

``` text
report
status=completed
```

Report 是 Workflow 的最后一个业务节点。

------------------------------------------------------------------------

# 7. Node 如何修改 State？

每个 Node 都遵循同一个模式：

``` text
读取 State
      │
处理业务
      │
更新 State
      │
返回新 State
```

因此：

> **Node 负责行为（Behavior），State 负责数据（Data）。**

------------------------------------------------------------------------

# 8. Node 与 Learning Trace

Workflow 执行时：

``` text
Route
   │
trace_step()
   │
KPI
   │
trace_step()
   │
Research
   │
trace_step()
   │
Report
```

Learning Trace 记录节点执行顺序，帮助开发者理解调用流程。

------------------------------------------------------------------------

# 9. Node 与 EventPublisher

节点执行过程中，可以发布事件：

``` text
Node
   │
EventPublisher.publish()
   │
SSE
   │
Frontend
```

因此前端能够实时看到：

-   Running
-   KPI Completed
-   Research Completed
-   Report Completed

------------------------------------------------------------------------

# 10. 企业为什么这样设计（Why）

如果把所有逻辑写进一个函数：

``` text
run_task()
 ├── Route
 ├── KPI
 ├── Research
 ├── Report
```

代码会越来越复杂。

拆分 Node 后：

-   单一职责
-   易测试
-   易替换
-   易扩展
-   更适合 AI Workflow

------------------------------------------------------------------------

# 11. Java 对照

  LangGraph     Java 概念
  ------------- -------------------
  Node          Service Step
  Route Node    Strategy Selector
  KPI Node      Business Service
  Report Node   Report Builder

------------------------------------------------------------------------

# Learning Tip

★★★★★

阅读每一个 Node 时，请固定思考四个问题：

1.  它读取哪些 State？
2.  它修改哪些 State？
3.  它是否发布 Event？
4.  下一步会进入哪个 Node？

------------------------------------------------------------------------

# 本章总结

一句话记忆：

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
   │
Final State
```

Node 负责一步一步推动 Workflow 前进，而不是一次完成全部业务。

------------------------------------------------------------------------

# 下一章预告

**Volume 02 · Chapter 06：Learning Trace 与 EventPublisher**

将深入分析：

-   trace_step()
-   log_event()
-   EventPublisher.publish()
-   SSE 如何实时更新前端
-   为什么 Learning Trace 不属于业务逻辑
