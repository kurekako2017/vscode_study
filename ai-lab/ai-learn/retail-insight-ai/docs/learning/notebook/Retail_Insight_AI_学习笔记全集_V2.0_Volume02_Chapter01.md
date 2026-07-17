# Retail Insight AI 学习笔记全集（正式版 V2.0）

> **历史学习笔记（保留不删除）**  
> 当前正式项目名：**Enterprise Retail Intelligence Platform（ERIP）V1.0**。  
> 面试与现状以 `docs/ai-agent-retail-handbook-v3/` 权威面试材料 + 主 README 为准。  
> 基线：PG 297/6 · IM 286/62 · FE 116 · head `20260717_08_ai_runtime` · 默认 stub。

# Volume 02：Workflow、Learning Trace 与 LangGraph

> Chapter 01：AI Workflow 总览

------------------------------------------------------------------------

# 文档信息

  项目       内容
  ---------- -----------------
  文档版本   V2.0
  Volume     02
  Chapter    01
  状态       Draft（审阅中）

------------------------------------------------------------------------

# 本章目标

完成本章后，你将理解：

-   为什么项目需要 Workflow。
-   TaskService 如何启动 Workflow。
-   Learning Trace、EventPublisher、LangGraph 三者之间的关系。
-   后续 LangGraph 学习主线。

------------------------------------------------------------------------

# 1. 什么是 Workflow？

Workflow（工作流）就是把复杂业务拆分成多个步骤，并按照固定顺序执行。

在 Retail Insight AI 中：

``` text
POST /api/tasks
      │
      ▼
TaskService.run_task()
      │
      ▼
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

每一个步骤都有明确职责。

------------------------------------------------------------------------

# 2. 为什么不用一个大函数？

不推荐：

``` text
run_task()
 ├── KPI
 ├── Research
 ├── Report
 └── Save
```

推荐：

``` text
Workflow
    │
    ├── Route
    ├── KPI
    ├── Research
    └── Report
```

优势：

-   容易维护
-   可扩展
-   易于测试
-   每个节点职责单一

------------------------------------------------------------------------

# 3. Workflow 在项目中的位置

``` text
Browser
    │
Router
    │
TaskService
    │
AnalysisWorkflow.stream()
    │
LangGraph
    │
Route
    │
KPI
    │
Research
    │
Report
```

Workflow 是 Service 与 AI Agent 之间的桥梁。

------------------------------------------------------------------------

# 4. 谁启动 Workflow？

真正启动 Workflow 的不是 Router，而是：

``` text
TaskService.run_task()
        │
        ▼
AnalysisWorkflow.stream()
```

因此：

-   Router：负责 HTTP
-   Service：负责业务编排
-   Workflow：负责 AI 分析流程

------------------------------------------------------------------------

# 5. Learning Trace 在哪里？

Learning Trace 负责记录执行过程。

``` text
TaskService.run_task()
        │
trace_step()
        │
AnalysisWorkflow.stream()
        │
trace_step()
        │
KPI
        │
trace_step()
        │
Research
```

它只记录流程，不改变业务逻辑。

------------------------------------------------------------------------

# 6. EventPublisher 在哪里？

Workflow 运行过程中：

``` text
Workflow
    │
EventPublisher.publish()
    │
SSE
    │
React Dashboard
```

作用：

-   推送运行状态
-   推送分析进度
-   推送完成事件

------------------------------------------------------------------------

# 7. LangGraph 在哪里？

Workflow 内部使用 LangGraph 来组织执行流程。

``` text
AnalysisWorkflow
        │
StateGraph
        │
State
        │
Node
        │
Edge
        │
Conditional Routing
```

后续章节会分别讲解每个概念。

------------------------------------------------------------------------

# 8. 整体关系图

``` text
HTTP Request
      │
Router
      │
TaskService
      │
AnalysisWorkflow
      │
LangGraph
      │
├── State
├── Node
├── Edge
└── Conditional Routing
      │
EventPublisher
      │
Learning Trace
      │
SSE
      │
Browser
```

------------------------------------------------------------------------

# 9. Java 对照

  Retail Insight AI   Java / Spring
  ------------------- ---------------------------------------
  Workflow            Process Engine（概念类似）
  LangGraph           工作流框架
  EventPublisher      ApplicationEventPublisher（概念类似）
  Learning Trace      调试调用链日志

------------------------------------------------------------------------

# Learning Tip

★★★★★

先理解整体调用关系，不要急着阅读 graph.py。

记住：

TaskService ↓

AnalysisWorkflow

↓

LangGraph

↓

AI 分析

------------------------------------------------------------------------

# 下一章预告

**Chapter 02：LangGraph 核心概念**

将详细讲解：

-   State
-   Node
-   Edge
-   Conditional Routing
-   compile()
-   stream()
-   invoke()
