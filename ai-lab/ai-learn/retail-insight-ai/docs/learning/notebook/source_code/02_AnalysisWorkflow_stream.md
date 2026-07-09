# Retail Insight AI 源码精读系列

# 02_AnalysisWorkflow_stream.md

> Source Code Deep Dive

------------------------------------------------------------------------

# 文档信息

  项目       内容
  ---------- -------------------------------
  系列       Source Code Deep Dive
  文档       02
  主题       AnalysisWorkflow.stream()
  对应源码   backend/app/workflow/graph.py
  难度       ★★★★☆

------------------------------------------------------------------------

# 学习目标

阅读完本文后，你应该能够回答：

-   `AnalysisWorkflow.stream()` 是谁调用的？
-   它为什么是 AI Workflow 的真正执行入口？
-   它如何串联 Route、KPI、Research、Report？
-   它和 `TaskService.run_task()`、Learning Trace、EventPublisher
    有什么关系？

------------------------------------------------------------------------

# 一、源码位置

``` text
backend/app/workflow/graph.py
```

重点关注：

``` python
AnalysisWorkflow.stream()
```

这是后台 AI 分析流程进入 LangGraph / Workflow 的核心入口。

------------------------------------------------------------------------

# 二、谁调用 AnalysisWorkflow.stream()？

调用链如下：

``` text
POST /api/tasks
    │
TaskService.create_task()
    │
BackgroundTasks.add_task()
    │
HTTP 202
    │
TaskService.run_task()
    │
AnalysisWorkflow.stream()
```

因此：

> `AnalysisWorkflow.stream()` 不是 HTTP 接口直接调用的，而是由后台任务
> `TaskService.run_task()` 调用。

------------------------------------------------------------------------

# 三、它在项目中的位置

``` text
FastAPI
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
```

`TaskService.run_task()` 负责启动后台任务。

`AnalysisWorkflow.stream()` 负责真正推动 AI Workflow 执行。

------------------------------------------------------------------------

# 四、stream() 为什么重要？

因为它把"任务执行"拆成多个阶段：

``` text
Route
    │
KPI
    │
Research
    │
Report
```

如果不用 Workflow，代码可能会变成：

``` text
run_task()
 ├── 判断模式
 ├── 计算 KPI
 ├── 调用 Research
 ├── 生成 Report
 ├── 保存结果
 └── 发布事件
```

这样 `run_task()` 会越来越大。

使用 `AnalysisWorkflow.stream()` 后，`run_task()`
只需要启动工作流，具体流程交给 Workflow 管理。

------------------------------------------------------------------------

# 五、stream() 的核心职责

可以把 `stream()` 理解成：

``` text
stream()
 │
 ├── 准备初始 State
 ├── 启动 Workflow
 ├── 按节点顺序执行
 ├── 边执行边产出事件
 ├── 返回中间结果
 └── 返回最终结果
```

重点：

> `stream()` 不是普通函数调用，而是"边执行、边输出"的流程执行器。

------------------------------------------------------------------------

# 六、为什么用 stream()，不是 invoke()？

## invoke()

``` text
开始
  │
  ▼
执行所有节点
  │
  ▼
一次性返回最终结果
```

适合短任务。

------------------------------------------------------------------------

## stream()

``` text
开始
  │
  ▼
Route 执行完成 → 返回一次事件
  │
  ▼
KPI 执行完成 → 返回一次事件
  │
  ▼
Research 执行完成 → 返回一次事件
  │
  ▼
Report 执行完成 → 返回最终事件
```

适合长时间 AI 分析任务。

Retail Insight AI 使用 `stream()`，因为它需要：

-   实时更新任务状态
-   配合 EventPublisher
-   配合 SSE
-   让前端看到执行进度

------------------------------------------------------------------------

# 七、与 Learning Trace 的关系

`AnalysisWorkflow.stream()` 执行时，Learning Trace 会记录后台阶段：

``` text
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

Learning Trace 的作用是：

-   给开发者看执行顺序
-   帮助学习源码
-   帮助排查调用链

它不改变 Workflow 本身。

------------------------------------------------------------------------

# 八、与 EventPublisher 的关系

Workflow 执行过程中，每完成一个阶段，通常会发布事件。

``` text
AnalysisWorkflow.stream()
        │
        ▼
EventPublisher.publish()
        │
        ▼
SSE
        │
        ▼
Frontend
```

因此：

-   `stream()`：负责推动流程
-   `EventPublisher`：负责通知外部
-   SSE：负责把事件推给浏览器

------------------------------------------------------------------------

# 九、与 State 的关系

`stream()` 执行时，会不断传递和更新 State。

``` text
Initial State
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

所以：

> `stream()` 的本质是推动 State 在不同 Node 之间流动。

------------------------------------------------------------------------

# 十、完整关系图

``` text
TaskService.run_task()
        │
        ▼
AnalysisWorkflow.stream()
        │
        ├── State
        │
        ├── Route Node
        │
        ├── KPI Node
        │
        ├── Research Node
        │
        └── Report Node
        │
        ▼
Final Result
        │
        ▼
TaskRepository.save()
        │
        ▼
EventPublisher.publish()
```

------------------------------------------------------------------------

# 十一、Java / Spring 对照

  Retail Insight AI           Java / Spring
  --------------------------- ----------------------------------
  AnalysisWorkflow.stream()   Workflow Executor
  State                       Process Context
  Node                        Step / Handler
  stream()                    Reactive Stream / Step Execution
  Final State                 Process Result

------------------------------------------------------------------------

# 十二、面试回答

如果面试官问：

> `AnalysisWorkflow.stream()` 在项目中负责什么？

可以回答：

> `AnalysisWorkflow.stream()` 是后台 AI Workflow 的核心执行入口。它由
> `TaskService.run_task()` 调用，负责创建并推进整个分析流程，按
> Route、KPI、Research、Report
> 等节点依次执行，并通过流式执行方式支持任务进度更新。它将 FastAPI
> 的后台任务与 LangGraph 风格的 AI Workflow 串联起来。

------------------------------------------------------------------------

# 十三、源码阅读建议

阅读顺序：

``` text
01_TaskService_run_task.md
        │
        ▼
02_AnalysisWorkflow_stream.md
        │
        ▼
backend/app/workflow/graph.py
        │
        ▼
State / Node / Edge
```

不要直接先看 `StateGraph`，先理解 `stream()` 在整个后台流程中的位置。

------------------------------------------------------------------------

# 本章总结

一句话记住：

``` text
AnalysisWorkflow.stream()
=
AI Workflow 的执行器
```

它负责：

-   接收初始 State
-   推动 Route / KPI / Research / Report
-   产出中间执行结果
-   支持事件发布与实时更新
-   将后台任务真正转化为 AI 分析流程

------------------------------------------------------------------------

# 下一章

**03_graph.py.md**

将继续解析：

-   `backend/app/workflow/graph.py`
-   `StateGraph`
-   `add_node()`
-   `add_edge()`
-   `add_conditional_edges()`
-   `compile()`
