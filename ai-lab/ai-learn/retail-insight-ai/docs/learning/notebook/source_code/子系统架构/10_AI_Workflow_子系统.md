# Retail Insight AI 企业源码架构手册

# Part 02：子系统架构

# 10_AI_Workflow_子系统

> Enterprise Subsystem Deep Dive

---

# 文档信息

---

  项目                                内容

---

  系列                                企业源码架构手册

  Part                                02 子系统架构

  文档                                10

  主题                                AI Workflow 子系统

对应源码                            backend/app/workflow/graph.py、backend/app/services/task_service.py
-------------------------------------------------------------------------------------------------------

---

# 学习目标

完成本章后，你应该能够回答：

- AI Workflow 子系统负责什么？
- Workflow 为什么独立于 Service？
- State 如何在各节点之间流转？
- Route、KPI、Research、Report 如何协同工作？
- Workflow 与 Learning Trace、EventPublisher、SSE 的关系是什么？

---

# 一、AI Workflow 子系统概述

AI Workflow 子系统是整个 Retail Insight AI 的核心。

它负责：

- 组织 AI 分析流程
- 管理执行顺序
- 控制状态流转
- 生成最终分析结果

一句话：

> **Workflow 决定"如何分析"，而不是"如何接收 HTTP 请求"。**

---

# 二、源码位置

```text
backend/
└── app/
    ├── workflow/
    │    └── graph.py
    ├── services/
    │    └── task_service.py
    ├── kpi/
    ├── reports/
    └── agents/
```

---

# 三、整体架构

```text
Browser
    │
POST /api/tasks
    │
TaskService.create_task()
    │
BackgroundTasks
    │
TaskService.run_task()
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
    │
Repository.save()
    │
EventPublisher.publish()
```

---

# 四、Workflow 生命周期

```text
创建初始 State
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

每个节点读取 State、处理业务，再写回 State。

---

# 五、State 的作用

State 是整个 Workflow 的共享数据对象。

```text
Initial State
    │
question
mode
task_id
    │
Route 更新 route
    │
KPI 更新 kpi_result
    │
Research 更新 research_result
    │
Report 更新 report
    │
Final State
```

Workflow 的本质就是 **State 在节点之间不断流动和演化**。

---

# 六、四个核心节点

## Route

决定执行策略。

输入：

- question
- mode

输出：

- route

---

## KPI

负责 KPI 分析。

输出：

- kpi_result

---

## Research

负责检索、AI 分析、知识整合。

输出：

- research_result

未来也是接入 RAG、LangChain、互联网搜索的重要位置。

---

## Report

负责汇总所有分析结果。

输出：

- report
- completed

---

# 七、为什么拆分 Node？

如果全部写在：

```text
run_task()
```

里面：

```text
run_task()
 ├── Route
 ├── KPI
 ├── Research
 ├── Report
```

函数会越来越复杂。

拆分后：

```text
Workflow
 ├── Route
 ├── KPI
 ├── Research
 └── Report
```

符合单一职责原则。

---

# 八、Workflow 与 Learning Trace

Learning Trace 记录：

```text
============= Background =============

AnalysisWorkflow.stream()

↓

Route

↓

KPI

↓

Research

↓

Report
```

帮助开发者理解 Workflow 的执行顺序。

---

# 九、Workflow 与 EventPublisher

每完成一个重要阶段：

```text
Node

↓

Repository.save()

↓

EventPublisher.publish()

↓

SSE

↓

Browser
```

Workflow 负责处理业务。

EventPublisher 负责通知外部。

---

# 十、Workflow 与 LangGraph

对应关系：

  Workflow 概念   LangGraph 概念

---

  State           Shared State
  Route/KPI/...   Node
  执行顺序        Edge
  条件分支        Conditional Edge
  stream()        Streaming Execution

项目已经采用了典型的 LangGraph 工作流设计思想。

---

# 十一、企业为什么这样设计

优点：

- AI 流程清晰
- 节点可复用
- 易测试
- 易扩展
- 容易增加新节点（Approval、RAG、Tool Calling 等）

Workflow 成为整个 AI Agent 的调度中心。

---

# 十二、Java / Spring 对照

  Retail Insight AI   Java / Spring

---

  Workflow            Process Engine
  Node                Step / Handler
  State               Process Context
  stream()            Reactive Pipeline
  TaskService         Workflow Launcher

---

# 十三、VS Code 阅读路线

```text
task_service.py
        │
run_task()
        │
graph.py
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

建议一边阅读源码，一边对照 Console Log 与 Learning Trace。

---

# 十四、面试回答

如果面试官问：

> AI Workflow 子系统负责什么？

可以回答：

> AI Workflow 子系统负责组织整个 AI 分析流程。它以 State 为共享数据，在
> Route、KPI、Research、Report 等节点之间流转，并通过
> AnalysisWorkflow.stream() 驱动整个流程执行。同时结合 Repository
> 保存状态、EventPublisher 发布事件，实现后台 AI Workflow
> 与前端实时更新的解耦。

---

# 本章总结

```text
AI Workflow 子系统

=

整个 AI Agent 的流程调度中心
```

它负责：

- 管理 Workflow
- 管理 State
- 调度 Node
- 控制执行顺序![1783640856807](image/10_AI_Workflow_子系统/1783640856807.png)
- 与 Repository、Learning Trace、EventPublisher 协同工作

---

# 下一章

**11_事件通信子系统.md**

将解析：

- EventPublisher
- Event Model
- Event Queue
- SSE
- 前端实时更新
- 为什么采用发布/订阅模式
