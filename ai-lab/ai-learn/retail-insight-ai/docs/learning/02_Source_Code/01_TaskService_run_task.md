# ERIP 源码精读系列

# 01_TaskService_run_task.md

> Source Code Deep Dive

---

# 文档信息

  项目       内容

---

  系列       Source Code Deep Dive
  文档       01
  主题       TaskService.run_task()
  对应源码   backend/app/services/task_service.py
  难度       ★★★☆☆

---

# 学习目标

阅读完本文后，你应该能够回答：

- `run_task()` 是谁调用的？
- `run_task()` 为什么要放到 BackgroundTasks？
- `run_task()` 为什么是整个 AI Workflow 的入口？
- `trace_step()`、`log_event()`、`EventPublisher.publish()`
  为什么都会出现在这里？

---

# 一、源码位置

```text
backend/app/services/task_service.py
```

找到：

```python
async def run_task(self, task_id: str) -> None:
```

这就是整个后台 AI 分析流程真正开始执行的位置。

> 注意：它不是 HTTP 入口，而是 **后台 Workflow 的入口**。

---

# 二、谁调用 run_task()？

调用链如下：

```text
Browser
    │
POST /api/tasks
    │
Router (api/tasks.py)
    │
TaskService.create_task()
    │
BackgroundTasks.add_task()
    │
──────────────────────────────
HTTP 202 Response
──────────────────────────────
    │
TaskService.run_task()
```

因此：

- `create_task()`：负责创建任务。
- `run_task()`：负责执行任务。

两者职责完全不同。

---

# 三、为什么使用 BackgroundTasks？

如果直接执行：

```text
POST /api/tasks
        │
run_task()
        │
等待 20 秒……
        │
HTTP 200
```

用户必须一直等待。

现在采用：

```text
POST /api/tasks
        │
BackgroundTasks.add_task()
        │
HTTP 202
────────────────────
后台继续执行
        │
run_task()
```

这样浏览器立即获得 `task_id`，后台继续分析。

---

# 四、run_task() 做了什么？

可以把整个函数理解为下面的流程：

```text
run_task()
 │
 ├── 读取任务
 ├── 修改状态（RUNNING）
 ├── Repository.save()
 ├── trace_step()
 ├── log_event()
 ├── EventPublisher.publish()
 ├── AnalysisWorkflow.stream()
 ├── 保存最终结果
 ├── EventPublisher.publish()
 └── 结束
```

这就是整个 AI Workflow 的生命周期。

---

# 五、重点代码说明

## ① Repository.save()

作用：

- 保存任务状态
- 将 queued → running
- 持久化最新状态

不是 AI 分析，而是数据保存。

---

## ② trace_step()

作用：

- 输出 Learning Trace
- 记录程序执行阶段
- 帮助阅读源码

它不会改变业务逻辑。

---

## ③ log_event()

作用：

- 写入运行日志
- 记录 running / completed / failed 等业务事件

与 `trace_step()` 不同，它更偏向运行监控。

---

## ④ EventPublisher.publish()

作用：

- 发布事件
- 通知 SSE
- 推送前端 Dashboard

Workflow 不直接操作前端，而是通过事件解耦。

---

## ⑤ AnalysisWorkflow.stream()

这是整个 AI Workflow 真正开始执行的位置。

调用后进入：

```text
Route
  │
KPI
  │
Research
  │
Report
```

---

# 六、对应 Console Log

你项目中的 Console：

```text
============= Background =============

TaskRepository.save()

↓

EventPublisher.publish()

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

就是 `run_task()` 的执行过程。

---

# 七、为什么它是桥梁？

`run_task()` 同时连接：

```text
FastAPI
      │
BackgroundTasks
      │
TaskService.run_task()
      │
LangGraph Workflow
      │
EventPublisher
      │
SSE
      │
Frontend
```

它既属于 Web 层，又负责启动 AI
Workflow，因此是整个项目最重要的入口之一。

---

# 八、Java / Spring 对照

  Retail Insight AI        Spring Boot

---

  TaskService.run_task()   @Async Service
  BackgroundTasks          @Async
  EventPublisher           ApplicationEventPublisher
  SSE                      SseEmitter

---

# 九、源码阅读建议

阅读顺序：

1. `api/tasks.py`
2. `TaskService.create_task()`
3. **TaskService.run_task()（本章）**
4. `AnalysisWorkflow.stream()`
5. `graph.py`

不要直接跳到 `graph.py`，先理解 `run_task()` 如何把 FastAPI 与 LangGraph
连接起来。

---

# 本章总结

一句话记住：

```text
run_task()

=

后台 AI Workflow 的启动器（Workflow Launcher）
```

它负责：

- 启动 Workflow
- 发布事件
- 输出 Learning Trace
- 更新任务状态
- 串联整个 AI 分析流程

---

# 下一章

**02_AnalysisWorkflow_stream.md**

将继续解析：

- `AnalysisWorkflow.stream()`
- 谁调用它？
- 它如何进入 LangGraph？
- Route / KPI / Research / Report 如何执行？
