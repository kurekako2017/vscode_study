# Retail Insight AI 企业源码架构手册

# Volume 06：AI Engine（AI 引擎）

# Chapter 38

# LangGraph Architecture（LangGraph 架构）

> Understand AI Workflow as a State Graph

---

# 文档信息

| 项目     | 内容                          |
| -------- | ----------------------------- |
| Volume   | 06                            |
| Chapter  | 38                            |
| 技术主题 | LangGraph Architecture        |
| 难度     | ⭐⭐⭐⭐⭐                    |
| 推荐程度 | ⭐⭐⭐⭐⭐                    |
| 对应源码 | backend/app/workflow/graph.py |

---

# 学习目标

阅读本章后，你应该能够回答：

- LangGraph 为什么会出现？
- 什么是 State Graph？
- 什么是 Node？
- 什么是 Edge？
- Retail Insight AI 的 AnalysisWorkflow 如何对应 LangGraph？
- 为什么企业 AI 都喜欢 Workflow？

---

# 一、为什么需要 LangGraph？

假设整个 AI Workflow 全部写在：

```python
run_task()
```

里面：

```python
KPI()

Research()

Report()

Save()

Publish()
```

开始：

只有：

几十行。

后来：

增加：

- Retry
- Approval
- Human Review
- Multi-Agent
- RAG

最终：

几千行。

维护：

几乎不可能。

所以：

Workflow：

必须：

独立出来。

---

# 二、什么是 Graph？

Graph：

不是：

流程图。

而是：

一种：

数据结构。

例如：

```text
Start

↓

KPI

↓

Research

↓

Report

↓

Finish
```

每一个：

圆点：

叫：

Node。

连接：

叫：

Edge。

整个：

就是：

Graph。

---

# 三、LangGraph 的核心思想

LangGraph：

不是：

调用：

LLM。

而是：

组织：

LLM。

例如：

```text
Node

↓

Node

↓

Node
```

每一个：

Node：

负责：

一个：

AI Task。

Workflow：

负责：

组织：

这些：

Node。

---

# 四、Retail Insight AI 当前实现（Current）

当前：

Workflow：

入口：

```text
backend/app/workflow/graph.py
```

主要类：

```text
AnalysisWorkflow
```

真正执行：

```python
stream()
```

TaskService：

负责：

启动。

Workflow：

负责：

调度。

---

# 五、Source Binding（源码绑定）

建议：

阅读：

```text
backend/app/workflow/graph.py
```

重点：

```text
AnalysisWorkflow

↓

stream()

↓

Node

↓

State
```

然后：

阅读：

```text
backend/app/services/task_service.py
```

观察：

Workflow：

如何：

启动。

---

# 六、AnalysisWorkflow 对应 LangGraph

可以理解为：

```text
AnalysisWorkflow

=

Graph
```

里面：

包含：

多个：

Node。

例如：

```text
Route

↓

KPI

↓

Research

↓

Report
```

虽然：

项目：

没有：

完全：

使用：

LangGraph API。

但是：

设计思想：

一致。

---

# 七、Node（节点）

Node：

表示：

一个：

业务步骤。

例如：

```text
Research

↓

生成：

市场分析

----------------

Report

↓

生成：

报告

----------------

Approval

↓

等待：

审批
```

Node：

不负责：

整个流程。

只负责：

自己的：

业务。

---

# 八、Edge（边）

Edge：

表示：

下一步：

去哪。

例如：

```text
Research

↓

Report
```

或者：

```text
Research

↓

Approval
```

以后：

增加：

Conditional Edge：

流程：

就会：

发生：

变化。

---

# 九、Workflow Execution

真正：

执行：

顺序：

```text
TaskService

↓

AnalysisWorkflow

↓

Node1

↓

Node2

↓

Node3

↓

Completed
```

Node：

执行完：

Workflow：

决定：

下一步。

---

# 十、Architecture Thinking

为什么：

不用：

```python
if

else

if

else
```

因为：

流程：

越来越复杂。

Workflow：

比：

if：

更容易：

维护。

---

# 十一、Current vs Enterprise

Current：

```text
Route

↓

KPI

↓

Research

↓

Report
```

Enterprise：

```text
Route

↓

Retriever

↓

Research

↓

Approval

↓

Report

↓

Audit

↓

Publish
```

Graph：

越来越大。

但是：

Workflow：

仍然：

容易维护。

---

# 十二、Java / Spring 对照

| Retail Insight AI | Java BPM        |
| ----------------- | --------------- |
| AnalysisWorkflow  | Process Engine  |
| Node              | Service Task    |
| Edge              | Gateway         |
| State             | Process Context |

---

# 十三、VS Code 阅读路线

建议：

```text
TaskService

↓

run_task()

↓

graph.py

↓

AnalysisWorkflow

↓

stream()
```

不要：

直接：

研究：

Node。

先理解：

整体：

Workflow。

---

# 十四、Learning Trace 对应

Learning Trace：

可以看到：

```text
Workflow Start

↓

Research

↓

Report

↓

Completed
```

这就是：

Workflow：

真正：

执行：

过程。

---

# 十五、企业扩展（Enterprise）

未来：

可以：

增加：

```text
Conditional Edge

↓

Parallel Node

↓

SubGraph

↓

Checkpoint

↓

Multi-Agent
```

无需：

重写：

整个：

Workflow。

---

# 十六、面试回答（中文）

为什么企业 AI 平台喜欢 LangGraph？

LangGraph 可以把复杂 AI Workflow 拆分成多个独立节点，每个节点负责单一业务，Workflow 负责流程控制。相比把所有逻辑写在一个 Service 中，这种方式更容易维护、扩展，也更适合 Multi-Agent 系统。

---

# 十七、面试回答（日文）

なぜ LangGraph を利用するのですか。

LangGraph は AI Workflow を複数の Node に分割し、それらを Graph として管理できます。各 Node は単一責任を持ち、Workflow が実行順序を制御するため、保守性・拡張性が向上します。

---

# 十八、日本 SES 常见追问

### Q：LangChain 和 LangGraph 有什么区别？

LangChain：

负责：

AI 能力。

LangGraph：

负责：

AI Workflow。

企业：

通常：

一起：

使用。

---

# 十九、本章练习

请完成：

① 阅读：

```text
backend/app/workflow/graph.py
```

↓

② 找到：

```text
AnalysisWorkflow
```

↓

③ 阅读：

```text
stream()
```

↓

④ 画出：

Workflow：

Node

Edge

关系图。

---

# 二十、本章核心记忆图

```text
TaskService

↓

AnalysisWorkflow

↓

Route

↓

Research

↓

Report

↓

Completed
```

---

# 本章总结

一句话：

```text
Workflow

负责：

组织流程

↓

Node

负责：

完成业务
```

LangGraph 的核心价值不是调用 LLM，而是**将复杂 AI Workflow 拆分为多个可维护、可扩展的节点，由 Graph 统一调度执行**。Retail Insight AI 当前的 `AnalysisWorkflow` 已经体现了这种设计思想，为未来接入 LangGraph 的高级能力（Conditional Edge、SubGraph、Multi-Agent）奠定了基础。

---

# 下一章

**Chapter 39：AI State Management（AI 状态管理）**

学习：

- State
- Context
- Memory
- Checkpoint
- Graph State
- Workflow Context
