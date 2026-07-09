# LangGraph 学习笔记（Retail Insight AI）

## 什么是 LangGraph？

> LangGraph 是一个用于构建 AI Workflow（工作流）的框架。

它可以把复杂的 AI
分析流程拆分成多个步骤（Node），通过执行路径（Edge）连接，并共享同一份状态（State）。

------------------------------------------------------------------------

## 四个核心概念

### 1. State（状态）

整个 Workflow 共享的数据。

``` text
State
├── question
├── mode
├── task_id
├── route
├── kpi_result
├── research_result
└── report
```

所有 Node 都可以读取和修改 State。

------------------------------------------------------------------------

### 2. Node（节点）

Node 是一个具体的业务步骤。

本项目中的 Node：

``` text
Route
↓
KPI
↓
Research
↓
Report
```

-   Route：决定分析路线
-   KPI：执行 KPI 分析
-   Research：调用 AI 检索
-   Report：生成最终报告

------------------------------------------------------------------------

### 3. Edge（边）

Edge 是连接两个 Node 的执行路径。

``` text
Route
  │
  ▼
KPI
```

箭头就是 Edge。

------------------------------------------------------------------------

### 4. Conditional Routing（条件路由）

根据条件决定下一步执行哪个 Node。

``` text
          Route
             │
     ┌───────┴────────┐
     │                │
mode=fixed      mode=research
     │                │
     ▼                ▼
   KPI          Research
```

------------------------------------------------------------------------

## Retail Insight AI 对应关系

  LangGraph             项目对应
  --------------------- --------------------------------------------
  State                 question、mode、task_id、report 等共享数据
  Node                  Route、KPI、Research、Report
  Edge                  Route → KPI → Research → Report
  Conditional Routing   根据 mode、provider、route 决定执行路径

------------------------------------------------------------------------

## AnalysisWorkflow.stream()

真正启动整个 Workflow。

``` text
AnalysisWorkflow.stream()

    │
    ├── 创建 State
    ├── 注册 Node
    ├── 定义 Edge
    ├── 配置条件路由
    └── graph.stream(state)
```

------------------------------------------------------------------------

## 项目真实执行流程

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
State
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
        │
        ▼
Repository.save()
```

------------------------------------------------------------------------

## 高速公路类比

-   State：货车（共享数据）
-   Node：收费站（执行步骤）
-   Edge：高速公路（连接节点）
-   Conditional Routing：高速分岔口（根据条件选择路线）

------------------------------------------------------------------------

## 面试回答

> LangGraph 是一个 AI Workflow 编排框架。它将复杂分析流程拆分为多个
> Node，通过 Edge 定义执行顺序，共享数据保存在 State 中，并利用
> Conditional Routing 根据不同条件动态选择执行路径，因此非常适合构建
> Agent 和复杂 AI 工作流。
