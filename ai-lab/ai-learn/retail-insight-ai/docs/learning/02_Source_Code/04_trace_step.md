# ERIP 源码精读系列

# 04_trace_step.md

> Source Code Deep Dive

------------------------------------------------------------------------

# 文档信息

  --------------------------------------------------------------------------
  项目                                内容
  ----------------------------------- --------------------------------------
  系列                                Source Code Deep Dive

  文档                                04

  主题                                trace_step()

  对应源码                            backend/app/core/learning_trace.py

  关联源码                            backend/app/services/task_service.py /
                                      backend/app/api/tasks.py /
                                      backend/app/workflow/graph.py

  难度                                ★★★★☆
  --------------------------------------------------------------------------

------------------------------------------------------------------------

# 学习目标

阅读完本文后，你应该能够回答：

-   `trace_step()` 是什么？
-   它为什么不是业务逻辑？
-   它如何记录 Learning Trace？
-   它和 Console Log、Execution Flow 的关系是什么？
-   为什么 `trace_step()` 经常和
    `log_event()`、`EventPublisher.publish()` 一起出现？

------------------------------------------------------------------------

# 一、源码位置

``` text
backend/app/core/learning_trace.py
```

重点关注：

``` python
def trace_step(...):
```

`trace_step()` 是 Retail Insight AI 中 Learning Trace 的核心函数之一。

------------------------------------------------------------------------

# 二、trace_step() 是什么？

一句话：

> **trace_step() 是学习用调用链记录器。**

它的作用不是执行业务，而是记录：

``` text
程序当前执行到了哪一层？
当前执行的是哪个类？
当前执行的是哪个方法？
当前属于 Request 还是 Background？
```

例如：

``` text
TaskService.create_task()
    ↓
TaskRepository.create()
    ↓
EventPublisher.publish()
```

这些 Console Log 中看到的调用链，就是通过 `trace_step()`
等函数收集并渲染出来的。

------------------------------------------------------------------------

# 三、trace_step() 不做什么？

`trace_step()` 不负责：

-   创建任务
-   保存数据
-   执行 Workflow
-   调用 AI
-   返回 HTTP Response
-   推送 SSE

它只做一件事：

> **把当前执行步骤记录到 Learning Trace Session 中。**

即使删除所有 `trace_step()`，业务仍然可以运行，只是学习日志没有了。

------------------------------------------------------------------------

# 四、trace_step() 在调用链中的位置

以 `POST /api/tasks` 为例：

``` text
Router
    │
trace_step()
    │
TaskService.create_task()
    │
trace_step()
    │
TaskRepository.create()
    │
trace_step()
    │
EventPublisher.publish()
```

每次调用 `trace_step()`，都相当于在执行流程中打一个学习标记。

------------------------------------------------------------------------

# 五、trace_step() 与 Console Log

`trace_step()` 本身通常不立即打印。

它会先把步骤保存起来。

完整流程类似：

``` text
trace_enter()
    │
创建 Learning Trace Session
    │
trace_step()
    │
记录 Router
    │
trace_step()
    │
记录 Service
    │
trace_step()
    │
记录 Repository
    │
trace_exit() / finalize_learning_trace()
    │
统一输出 Console Log
```

因此：

> `trace_step()` 是"记录"，最终打印通常发生在 `trace_exit()` 或
> `finalize_learning_trace()`。

------------------------------------------------------------------------

# 六、常见参数说明

典型调用：

``` python
trace_step(
    "POST",
    "/api/tasks",
    "Event",
    "publish running event",
    class_name="EventPublisher",
    method_name="publish",
    file_path="backend/app/events/publisher.py",
    task_id=task_id,
    status="running",
    phase="background",
)
```

含义：

  参数                        说明
  --------------------------- --------------------------------
  `"POST"`                    HTTP 方法
  `"/api/tasks"`              API 路径
  `"Event"`                   Learning Trace 分类
  `"publish running event"`   当前步骤说明
  `class_name`                当前执行类
  `method_name`               当前执行方法
  `file_path`                 对应源码文件
  `task_id`                   当前任务 ID
  `status`                    当前任务状态
  `phase`                     执行阶段：Request / Background

------------------------------------------------------------------------

# 七、phase 为什么重要？

`phase` 决定这条记录属于哪个执行阶段。

例如：

``` python
phase="background"
```

表示它属于后台阶段。

Console Log 中会显示在：

``` text
============= Background =============
```

如果没有 Background 区分，长任务调用链会混在一起，初学者很难理解：

``` text
HTTP 已经返回
但后台还在执行
```

------------------------------------------------------------------------

# 八、trace_step() 与 Learning Trace 的关系

`trace_step()` 是 Learning Trace 的"记录点"。

``` text
Learning Trace
    │
    ├── trace_enter()
    ├── trace_step()
    ├── trace_step()
    ├── trace_step()
    └── trace_exit()
```

可以把 Learning Trace 理解为一个录像系统：

``` text
trace_enter()   开始录像
trace_step()    记录一个镜头
trace_step()    再记录一个镜头
trace_exit()    输出整段录像
```

------------------------------------------------------------------------

# 九、trace_step() 与 log_event() 的区别

  trace_step()                         log_event()
  ------------------------------------ -----------------------
  学习调用链                           业务日志
  给开发者学习源码                     给运维/调试看运行状态
  记录执行到了哪一步                   记录发生了什么事件
  输出 Source Chain / Execution Flow   输出结构化日志

例如：

``` python
trace_step(...)
log_event(...)
```

两者经常一起出现，但职责不同。

------------------------------------------------------------------------

# 十、trace_step() 与 EventPublisher.publish() 的区别

  trace_step()          EventPublisher.publish()
  --------------------- --------------------------
  记录学习日志          发布业务事件
  给开发者看            给前端 / SSE 看
  不改变业务状态        触发前端更新
  属于 Learning Trace   属于事件系统

例如：

``` text
Task running
    │
trace_step()
    │
记录：EventPublisher.publish()
    │
EventPublisher.publish()
    │
真正发布 running 事件
```

------------------------------------------------------------------------

# 十一、为什么 trace_step() 不应该写太多？

如果每一行代码都写 `trace_step()`：

``` text
代码会变吵
日志会变长
学习重点会消失
```

因此它只适合放在关键节点：

-   Router
-   Service
-   Repository
-   Workflow
-   EventPublisher
-   Schema
-   Background

不适合记录普通变量、普通 if、普通 return。

------------------------------------------------------------------------

# 十二、对应 Console Log

例如：

``` text
============= Request =============

backend/app/api/tasks.py
create_task()
    ↓
backend/app/services/task_service.py
TaskService.create_task()
    ↓
backend/app/repositories/...
TaskRepository.create()
```

这些步骤都来自 `trace_step()` 或 `trace_source_chain()` 记录的数据。

------------------------------------------------------------------------

# 十三、企业为什么这样设计（Why）

普通日志只能看到：

``` text
Task created
Task running
Task completed
```

但初学者看不到：

``` text
Router
    ↓
Service
    ↓
Repository
    ↓
Workflow
```

Learning Trace 解决的是：

> **源码学习和调用链理解问题。**

因此它是教学辅助能力，不是业务能力。

------------------------------------------------------------------------

# 十四、Java / Spring 对照

  Retail Insight AI   Java / Spring 概念
  ------------------- -------------------------
  trace_step()        调用链调试日志
  Learning Trace      Debug Trace / AOP Trace
  phase               请求阶段 / 异步阶段
  file_path           源码定位
  method_name         方法名

------------------------------------------------------------------------

# 十五、面试回答

如果面试官问：

> `trace_step()` 是什么？

可以回答：

> `trace_step()` 是项目中用于 Learning Trace
> 的调用链记录函数。它不参与业务处理，而是在
> Router、Service、Repository、Workflow
> 等关键节点记录执行步骤，最终生成可读的 Console Log，帮助开发者理解
> Request 和 Background 两个阶段的源码调用流程。

------------------------------------------------------------------------

# 十六、源码阅读建议

阅读顺序：

``` text
backend/app/core/learning_trace.py
    │
trace_enter()
    │
trace_step()
    │
trace_exit()
    │
finalize_learning_trace()
```

然后对照：

``` text
backend/app/api/tasks.py
backend/app/services/task_service.py
backend/app/workflow/graph.py
```

理解不同地方为什么调用 `trace_step()`。

------------------------------------------------------------------------

# 本章总结

一句话记住：

``` text
trace_step()
=
Learning Trace 的步骤记录器
```

它负责：

-   记录当前执行节点
-   标记 Request / Background
-   连接源码与 Console Log
-   帮助学习调用链
-   不改变任何业务逻辑

------------------------------------------------------------------------

# 下一章

**05_EventPublisher.md**

将继续精读：

-   `EventPublisher.publish()` 是什么？
-   它和 SSE 的关系是什么？
-   为什么 Workflow 不直接通知前端？
-   它和 `trace_step()`、`log_event()` 如何配合？
