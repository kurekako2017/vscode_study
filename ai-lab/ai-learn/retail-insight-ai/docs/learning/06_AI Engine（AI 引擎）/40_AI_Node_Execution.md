# Retail Insight AI 企业源码架构手册

# Volume 06：AI Engine（AI 引擎）

# Chapter 40

# AI Node Execution（AI 节点执行机制）

> Understand How AI Workflow Executes Each Node

---

# 文档信息

| 项目     | 内容                          |
| -------- | ----------------------------- |
| Volume   | 06                            |
| Chapter  | 40                            |
| 技术主题 | AI Node Execution             |
| 难度     | ⭐⭐⭐⭐⭐                    |
| 推荐程度 | ⭐⭐⭐⭐⭐                    |
| 对应源码 | backend/app/workflow/graph.py |

---

# 学习目标

阅读本章后，你应该能够回答：

- 什么是 Node？
- Node 与 Workflow 的关系是什么？
- Node 生命周期包含哪些阶段？
- Retail Insight AI 如何执行每个 Node？
- 顺序执行与并行执行有什么区别？

---

# 一、什么是 Node？

在 AI Workflow 中：

**Node（节点）** 表示一个独立的业务处理单元。

例如：

```text
Research

↓

Report

↓

Approval

↓

Publish
```

每一个步骤都是一个 Node。

Node 只负责完成自己的工作，不负责控制整个流程。

---

# 二、Workflow 与 Node 的关系

Workflow 可以理解为：

```text
Workflow

↓

Node A

↓

Node B

↓

Node C

↓

Finish
```

Workflow：

负责调度。

Node：

负责执行。

Workflow 不关心 Node 的内部实现。

Node 也不知道整个流程。

这就是职责分离（Separation of Concerns）。

---

# 三、Retail Insight AI 当前实现（Current）

当前项目：

Workflow 入口：

```text
backend/app/workflow/graph.py
```

主要类：

```text
AnalysisWorkflow
```

执行入口：

```python
stream()
```

整个执行过程：

```text
TaskService

↓

AnalysisWorkflow.stream()

↓

Research

↓

Report

↓

Repository

↓

Publisher
```

每一步都可以理解为一个逻辑 Node。

---

# 四、源码目录结构 ⭐

建议阅读：

```text
backend/app/workflow/

↓

graph.py
```

同时打开：

```text
backend/app/services/

↓

task_service.py
```

理解：

TaskService 如何启动 Workflow。

---

# 五、关键源码文件 ⭐

重点：

```text
graph.py

↓

AnalysisWorkflow

↓

stream()
```

阅读时重点关注：

- Node 如何开始？
- Node 如何结束？
- Node 完成后谁决定下一步？

---

# 六、关键类与关键函数 ⭐

重点函数：

```text
TaskService.run_task()

↓

AnalysisWorkflow.stream()
```

建议结合日志观察：

```text
Workflow Start

↓

Research

↓

Report

↓

Completed
```

每条日志都对应一个 Node 生命周期。

---

# 七、Node 生命周期 ⭐

一个典型 Node：

```text
Created

↓

Executing

↓

Completed
```

如果发生异常：

```text
Executing

↓

Failed
```

未来企业版还可以增加：

```text
Retry

↓

Completed
```

---

# 八、顺序执行（Sequential Execution）

当前 Retail Insight AI：

采用：

```text
Research

↓

Report

↓

Save

↓

Publish
```

前一个 Node 完成后，

下一个 Node 才开始。

这种方式：

逻辑简单、

容易调试。

---

# 九、并行执行（Parallel Execution）

企业 AI 平台可能需要：

```text
Research
      │
      ├────► Competitor Analysis
      │
      └────► Market Analysis

↓

Merge Result

↓

Report
```

多个 Node 可以同时运行。

最终汇总结果。

这可以明显提升执行效率。

---

# 十、Architecture Thinking ⭐

为什么要拆分 Node？

如果把所有逻辑写在：

```python
run_task()
```

未来增加：

- Approval
- Retry
- Human Review
- Multi-Agent

整个函数会越来越复杂。

拆分 Node 后：

每个 Node 只负责一个职责，

Workflow 负责组织。

符合单一职责原则（SRP）。

---

# 十一、Current vs Enterprise

Current：

```text
Workflow

↓

Research

↓

Report
```

Enterprise：

```text
Workflow

↓

Parallel Research

↓

Approval

↓

Retry

↓

Publish

↓

Audit
```

Workflow 可以不断扩展，

Node 保持独立。

---

# 十二、Java / Spring 对照 ⭐

| Retail Insight AI | Java BPM        |
| ----------------- | --------------- |
| Workflow          | Process Engine  |
| Node              | Service Task    |
| Execute           | Task Executor   |
| State             | Process Context |

---

# 十三、VS Code 阅读路线 ⭐

建议：

```text
task_service.py

↓

run_task()

↓

graph.py

↓

stream()

↓

Node Execute
```

阅读时：

先理解 Workflow，

再深入 Node。

---

# 十四、Debug Guide（调试指南）⭐

建议设置断点：

```text
① TaskService.run_task()

↓

② AnalysisWorkflow.stream()

↓

③ 第一个 Node

↓

④ Repository.save()

↓

⑤ EventPublisher.publish()
```

每执行一步，

观察：

- 当前 Node
- State 是否变化
- Learning Trace 是否同步更新

---

# 十五、Learning Trace 对应 ⭐

建议：

Learning Trace 增加：

```text
Workflow Started

↓

Node = Research

↓

Node Completed

↓

Node = Report

↓

Node Completed

↓

Workflow Completed
```

这样可以快速定位 Workflow 的执行位置。

---

# 十六、企业扩展（Enterprise）

未来：

Node 可以增加：

```text
Retry Node

↓

Approval Node

↓

Human Review Node

↓

Tool Calling Node

↓

Multi-Agent Node
```

无需修改已有 Node。

---

# 十七、面试回答（中文）

为什么企业 AI Workflow 要拆分为多个 Node？

拆分 Node 可以降低业务耦合，每个 Node 负责独立职责，Workflow 负责整体调度。这样便于维护、测试和扩展，也更适合实现 Retry、Approval、Parallel Execution 等高级功能。

---

# 十八、面试回答（日文）

なぜ Workflow を複数の Node に分割するのですか。

各 Node が単一責任を持つことで保守性・拡張性が向上します。また Workflow が実行順序を管理するため、Retry や Parallel Execution などの機能も追加しやすくなります。

---

# 十九、日本 SES 常见追问

### Q：Node 和 Service 有什么区别？

Service：

关注业务逻辑。

Node：

关注 Workflow 中的一个执行步骤。

一个 Node 内部可以调用多个 Service。

---

# 二十、本章练习 ⭐

请完成：

① 阅读：

```text
backend/app/workflow/graph.py
```

↓

② 找出：

Workflow 中有哪些逻辑 Node？

↓

③ 画出：

Node 生命周期图。

↓

④ 思考：

哪些 Node 可以改为并行执行？

---

# 二十一、本章核心记忆图 ⭐

```text
TaskService

↓

AnalysisWorkflow

↓

Research Node

↓

Report Node

↓

Repository

↓

Publisher

↓

Completed
```

---

# 本章总结

一句话：

```text
Workflow

负责调度

↓

Node

负责执行
```

AI Node Execution 的核心思想是：

**将复杂 AI Workflow 拆分为多个独立节点，由 Workflow 统一调度执行。**

这种设计能够提高系统的可维护性、可测试性和可扩展性，也是现代企业 AI 平台普遍采用的架构模式。

---

# 下一章

**Chapter 41：Prompt Engineering（Prompt 工程）**

学习：

- System Prompt
- User Prompt
- Prompt Template
- Structured Output
- Prompt Versioning
- 企业 Prompt 管理
