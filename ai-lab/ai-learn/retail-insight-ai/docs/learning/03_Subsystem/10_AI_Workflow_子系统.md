# ERIP 企业源码架构手册

# Part 02：子系统架构

# 10_AI_Workflow_子系统（源码绑定升级版 V2）

> Enterprise Subsystem Deep Dive

---

# 文档信息

| 项目     | 内容                          |
| -------- | ----------------------------- |
| 系列     | 企业源码架构手册              |
| Part     | 02 子系统架构                 |
| 文档     | 10                            |
| 版本     | V2（Source Binding Edition）  |
| 主题     | AI Workflow Subsystem         |
| 对应源码 | backend/app/workflow/graph.py |

---

# 学习目标

阅读完本章后，你应该能够回答：

- AnalysisWorkflow 为什么存在？
- Workflow 为什么独立于 TaskService？
- stream() 是整个项目最重要的方法吗？
- State 如何在各 Node 之间流转？
- LangGraph 在本项目中如何落地？

---

# 一、子系统定位

AI Workflow 是整个 ERIP 的核心。

它负责：

- AI 流程编排（Workflow Orchestration）
- State 管理
- Node 调度
- AI 分析
- 最终 Report 生成

一句话：

> Workflow 决定 **AI 如何工作**。

---

# 二、源码目录结构 ⭐

```text
backend/
└── app/
    ├── workflow/
    │      └── graph.py
    │
    ├── kpi/
    │      └── workflow.py
    │
    ├── agents/
    │      └── providers/
    │              └── static_research.py
    │
    └── reports/
            └── generator.py
```

可以理解成：

```
graph.py

↓

组织整个 Workflow

↓

调用 KPI

↓

调用 Research

↓

调用 Report
```

---

# 三、关键源码文件 ⭐

## graph.py

整个 AI Workflow 入口。

核心类：

```
AnalysisWorkflow
```

核心函数：

```
stream()
```

所有 Workflow 都从这里开始。

---

## workflow.py

负责：

```
KPI Workflow
```

---

## static_research.py

负责：

```
Research
```

未来：

这里会扩展：

- LangChain
- Internet Search
- Internal RAG

---

## generator.py

负责：

```
生成最终 Report
```

---

# 四、关键类与关键函数 ⭐

## AnalysisWorkflow

整个 Workflow 控制器。

---

### stream()

整个项目最重要的方法。

作用：

```
驱动整个 Workflow。
```

执行：

```
Route

↓

KPI

↓

Research

↓

Report
```

---

## Route

职责：

决定：

```
走哪条分析路线。
```

---

## KPI

职责：

执行 KPI Workflow。

输出：

```
KPI Result
```

---

## Research

职责：

执行 AI Research。

输出：

```
Research Result
```

---

## Report

职责：

整合：

```
KPI

+

Research

↓

Final Report
```

---

# 五、调用关系图 ⭐

```
POST /api/tasks

↓

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

Repository.save()

↓

EventPublisher.publish()
```

这就是：

整个项目最重要的一张图。

---

# 六、State 生命周期 ⭐

Workflow 本质：

不是函数调用。

而是：

```
State

↓

Node

↓

State

↓

Node

↓

State
```

例如：

```
Initial State

↓

question

↓

Route

↓

route

↓

KPI

↓

kpi_result

↓

Research

↓

research_result

↓

Report

↓

report

↓

Final State
```

State 一直在变化。

---

# 七、Learning Trace 对应 ⭐

Background：

```
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

Learning Trace：

记录：

Workflow 每一步。

---

# 八、Console Log 对应 ⭐

Console：

```
Running

↓

Route

↓

Research

↓

Report

↓

Completed
```

Learning Trace：

记录：

调用链。

Console：

记录：

执行状态。

---

# 九、实际运行示例 ⭐

Request：

```
POST /api/tasks
```

返回：

```
HTTP 202
```

随后：

```
run_task()

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
```

最后：

```
completed
```

---

# 十、为什么采用 Workflow（Why）

如果：

全部写：

```
run_task()
```

以后：

代码：

```
3000+

行
```

Workflow：

把：

```
Route

KPI

Research

Report
```

拆成：

独立 Node。

方便：

维护。

---

# 十一、LangGraph 对应 ⭐

Retail Insight AI：

```
AnalysisWorkflow

↓

Route

↓

KPI

↓

Research

↓

Report
```

对应：

LangGraph：

| 本项目   | LangGraph |
| -------- | --------- |
| Workflow | Graph     |
| Route    | Node      |
| KPI      | Node      |
| Research | Node      |
| Report   | Node      |
| State    | State     |
| stream() | stream()  |

几乎：

一一对应。

---

# 十二、VS Code 阅读路线 ⭐

建议：

```
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

建议：

边运行：

```
./scripts/start_backend.sh
```

边观察：

```
============= Background =============
```

理解最快。

---

# 十三、阅读源码建议 ⭐

建议：

第一遍：

只看：

```
stream()
```

第二遍：

再看：

Route。

第三遍：

看：

Research。

第四遍：

看：

Report。

不要：

第一次：

全部阅读。

---

# 十四、面试回答

如果面试官问：

> AI Workflow 为什么独立？

可以回答：

> Workflow 负责整个 AI Agent 的流程编排。TaskService 只负责启动任务，而真正的 AI 分析由 AnalysisWorkflow.stream() 驱动，通过 Route、KPI、Research、Report 等节点完成。Workflow 与 Repository、EventPublisher 解耦，使整个系统具备良好的扩展性，也方便未来接入 LangGraph、LangChain 和更多 AI 能力。

---

# 本章总结

一句话：

```
TaskService

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
```

AnalysisWorkflow 是整个 ERIP 的核心调度器，也是学习 LangGraph 最重要的源码入口。

---

# 下一章

**11_事件通信子系统（源码绑定升级版 V2）**

将结合：

- publisher.py
- publish()
- SSE
- EventSource
- Dashboard
- Learning Trace

完整解析企业事件通信架构。
