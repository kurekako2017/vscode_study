
# Retail Insight AI 企业源码架构手册

# Volume 04：Execution Flow（源码执行流程）

# Chapter 22

# AI Workflow 执行全过程

> AnalysisWorkflow Execution Flow

---

# 文档信息

| 项目     | 内容                          |
| -------- | ----------------------------- |
| Volume   | 04                            |
| Chapter  | 22                            |
| 核心类   | AnalysisWorkflow              |
| 核心文件 | backend/app/workflow/graph.py |
| 推荐程度 | ⭐⭐⭐⭐⭐                    |

---

# 学习目标

阅读本章后，你应该能够回答：

- AI Workflow 是什么时候开始执行的？
- AnalysisWorkflow.stream() 做了什么？
- Workflow 为什么采用 State？
- Route、KPI、Research、Report 如何串联？
- LangGraph 在整个系统中的作用是什么？

---

# 一、AI Workflow 是什么？

AI Workflow 是整个 Retail Insight AI 的核心。

它负责组织 AI 的完整执行流程。

Workflow 本身并不直接处理 HTTP 请求，而是在后台任务启动后开始运行。

启动顺序如下：

```text
Browser

↓

POST /api/tasks

↓

TaskService.create_task()

↓

BackgroundTasks

↓

TaskService.run_task()

↓

AnalysisWorkflow.stream()
```

真正的 AI 分析，从 `stream()` 开始。

---

# 二、源码入口 ⭐⭐⭐⭐⭐

打开：

```text
backend/app/workflow/graph.py
```

找到：

```python
class AnalysisWorkflow
```

随后找到：

```python
stream(...)
```

这是整个 Workflow 的入口。

所有节点（Node）都由这里统一调度。

---

# 三、Workflow 执行流程 ⭐⭐⭐⭐⭐

```text
TaskService.run_task()

↓

AnalysisWorkflow.stream()

↓

Route

↓

KPI Analysis

↓

Research

↓

Report

↓

Repository.save()

↓

EventPublisher.publish()

↓

Completed
```

整个流程始终由 `AnalysisWorkflow.stream()` 驱动。

---

# 四、LangGraph 执行模型

在 LangGraph 中，一个 Workflow 可以抽象为：

```text
State

↓

Node

↓

Edge

↓

Next Node

↓

State Update
```

Retail Insight AI 当前采用的执行思想与 LangGraph 一致：

```text
Task State

↓

Route

↓

KPI

↓

Research

↓

Report
```

每完成一个阶段，

State 都会更新一次。

---

# 五、State 生命周期 ⭐⭐⭐⭐⭐

任务创建后：

```text
Created
```

开始分析：

```text
Running
```

进入 KPI：

```text
Running
```

进入 Research：

```text
Running
```

生成 Report：

```text
Running
```

全部结束：

```text
Completed
```

如果异常：

```text
Failed
```

State 会随着 Workflow 推进不断变化。

---

# 六、关键源码文件

| 文件              | 职责          |
| ----------------- | ------------- |
| graph.py          | Workflow 定义 |
| task_service.py   | 启动 Workflow |
| publisher.py      | 发布事件      |
| learning_trace.py | 输出调用链    |

---

# 七、关键函数

## AnalysisWorkflow.stream()

作用：

整个 Workflow 的入口。

负责：

- 调度各节点
- 更新 State
- 返回执行结果

---

## Route

作用：

决定后续处理路径。

例如：

```text
Task

↓

Route

↓

Research
```

---

## KPI

作用：

分析 KPI 数据。

生成 KPI 分析结果。

---

## Research

作用：

查询知识。

分析资料。

生成 AI 上下文。

---

## Report

作用：

生成最终分析报告。

Workflow 在这里接近结束。

---

# 八、调用关系图 ⭐⭐⭐⭐⭐

```text
TaskService.run_task()
        │
        ▼
AnalysisWorkflow.stream()
        │
        ▼
      Route
        │
        ▼
   KPI Analysis
        │
        ▼
    Research
        │
        ▼
 Report Generator
        │
        ▼
Repository.save()
        │
        ▼
EventPublisher.publish()
```

---

# 九、Learning Trace 对应

Workflow 开始：

```text
============= Background =============

TaskService.run_task()

↓

AnalysisWorkflow.stream()
```

随后：

每个节点：

都会输出：

对应的 Learning Trace。

帮助开发者观察 Workflow 的执行顺序。

---

# 十、Console Log 对应

Console：

例如：

```text
Workflow Started

↓

KPI Running

↓

Research Running

↓

Report Generated

↓

Workflow Completed
```

Learning Trace：

关注：

调用关系。

Console：

关注：

执行状态。

---

# 十一、VS Code 阅读路线 ⭐⭐⭐⭐⭐

建议按照下面顺序阅读：

```text
task_service.py

↓

run_task()

↓

graph.py

↓

AnalysisWorkflow

↓

stream()

↓

Route

↓

KPI

↓

Research

↓

Report
```

不要直接阅读所有节点，

先理解 Workflow 主流程。

---

# 十二、当前源码实现（Current）

Retail Insight AI 当前已经实现：

- AnalysisWorkflow
- stream()
- Workflow 调度
- Repository 更新
- EventPublisher 通知

已经形成完整的 AI Workflow。

---

# 十三、企业扩展（Enterprise）

未来可扩展为：

```text
State

↓

Conditional Edge

↓

Parallel Node

↓

Retry

↓

Approval

↓

Sub Graph
```

并结合：

- LangGraph
- LangChain
- RAG
- Multi-Agent

形成企业级 Agent Workflow。

---

# 十四、为什么采用 Workflow（Why）

如果把所有 AI 逻辑写在一个函数中：

```text
run_task()

↓

几千行代码
```

将难以维护。

采用 Workflow 后：

```text
Route

↓

KPI

↓

Research

↓

Report
```

每个节点职责单一，

便于维护和扩展。

---

# 十五、Java / Spring 对照

| Retail Insight AI | Java / Spring   |
| ----------------- | --------------- |
| AnalysisWorkflow  | Process Engine  |
| State             | Process Context |
| Node              | Service Task    |
| Edge              | Flow Transition |
| Route             | Gateway         |

---

# 十六、面试回答（中文）

面试官：

> AI Workflow 是如何执行的？

回答：

> POST /api/tasks 创建任务后，TaskService 通过 BackgroundTasks 启动 run_task()，随后进入 AnalysisWorkflow.stream()。Workflow 按照 Route、KPI、Research、Report 的顺序依次执行，每个阶段都会更新任务状态，并通过 Repository 持久化，最后由 EventPublisher 发布事件，通过 SSE 实时通知前端。这种设计将 HTTP 请求与 AI 分析解耦，提高了系统的响应速度和可维护性。

---

# 十七、面试回答（日语）

面接官：

> AI Workflow の実行フローを説明してください。

回答例：

> POST /api/tasks の実行後、TaskService は BackgroundTasks を利用して run_task() を非同期で開始します。その後 AnalysisWorkflow.stream() が呼び出され、Route、KPI、Research、Report の各ステップを順番に実行します。各ステップでタスク状態を更新し、Repository に保存するとともに EventPublisher を介して SSE でフロントエンドへ通知します。これにより HTTP リクエストと AI 処理を疎結合にした構成になっています。

---

# 十八、日本SES常见追问

### 为什么采用 Workflow，而不是一个大的 Service？

回答：

Workflow 可以把复杂业务拆分为多个节点。

每个节点职责单一，

既方便测试，也方便扩展。

当未来增加 Approval、RAG、Multi-Agent 时，

只需增加新的节点，而无需修改整个流程。

---

# 十九、本章源码阅读任务 ⭐⭐⭐⭐⭐

完成下面练习：

① 打开：

```text
backend/app/workflow/graph.py
```

↓

② 找到：

```python
class AnalysisWorkflow
```

↓

③ 阅读：

```python
stream()
```

↓

④ 找到：

Route

↓

KPI

↓

Research

↓

Report

↓

⑤ 运行：

```http
POST /api/tasks
```

结合：

- Learning Trace
- Console Log
- Workflow 执行顺序

验证每一个节点的调用过程。

---

# 本章总结

一句话：

```text
TaskService.run_task()

↓

AnalysisWorkflow.stream()

↓

Route

↓

KPI

↓

Research

↓

Report

↓

Repository

↓

EventPublisher

↓

SSE
```

AnalysisWorkflow 是整个 Retail Insight AI 的执行引擎。

它负责组织 AI Workflow，驱动所有分析节点，并通过 Repository 和 EventPublisher 将结果保存并实时通知前端。

---

# 下一章

**Chapter 23：Learning Trace 执行全过程**

学习：

- trace_step()
- trace_enter()
- trace_exit()
- log_event()
- Request / Background 为什么分开
- 如何利用 Learning Trace 阅读源码
