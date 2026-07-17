
# Enterprise Retail Intelligence Platform (ERIP) 企业源码架构手册

# 📖 READ FIRST（开始阅读前请先阅读）

> Welcome to the ERIP Learning Handbook（历史名称：Retail Insight AI）

---

# 为什么会有这套教材？

ERIP 不只是一个 AI 项目。

它也是一套专门为了学习企业级 AI 系统开发而整理的源码教材。

这套教材遵循一个原则：

> **从"会运行"到"会理解"，最终达到"会设计"。**

阅读完成后，你不仅能够理解 ERIP 的源码，还能够掌握现代企业 AI Agent 项目的设计思想。

---

# 本套教材适合谁？

本教材适合：

- Python 开发者
- FastAPI 初学者
- Java / Spring Boot 工程师
- AI Agent 学习者
- LangGraph 学习者
- 日本 SES 面试准备者
- 企业 AI 系统开发者

如果你能够阅读 Python 基础语法，就可以开始学习。

---

# 推荐阅读顺序（★★★★★）

请不要跳着阅读。

建议按照下面顺序学习：

```text
Volume 01

Foundation

↓

Volume 02

Source Code

↓

Volume 03

Subsystem

↓

Volume 04

Execution Flow

↓

Volume 05

Enterprise

↓

Volume 06

AI

↓

Volume 07

Interview
```

这是整套教材最重要的阅读路线。

---

# 每一册学习什么？

| Volume | 内容           | 学习目标                      |
| ------ | -------------- | ----------------------------- |
| 01     | Foundation     | 认识项目                      |
| 02     | Source Code    | 理解源码文件                  |
| 03     | Subsystem      | 理解系统模块                  |
| 04     | Execution Flow | 理解程序执行过程              |
| 05     | Enterprise     | 理解企业架构设计              |
| 06     | AI             | 理解 AI Agent、LangGraph、RAG |
| 07     | Interview      | 面试与项目表达                |

每一册都会建立在上一册基础上。

---

# 如何学习？

建议采用：

```text
阅读 Markdown

↓

打开 VS Code

↓

找到对应源码

↓

运行程序

↓

观察 Learning Trace

↓

观察 Console Log

↓

再次阅读源码
```

不要只阅读文档。

一定要结合源码一起学习。

---

# 推荐学习工具

建议准备：

- VS Code
- Python 3.12+
- FastAPI
- Docker
- Git
- 浏览器（Developer Tools）
- Postman（或 curl）

同时打开：

```text
Markdown

+

VS Code

+

Terminal

+

Browser
```

学习效果最好。

---

# 如何阅读源码？

每一章都建议按照下面顺序：

```text
README

↓

源码位置

↓

Router

↓

Service

↓

Repository

↓

Workflow

↓

Learning Trace

↓

Console Log
```

不要直接阅读整个项目。

按照调用顺序阅读效率最高。

---

# Learning Trace 是什么？

Learning Trace 是 Retail Insight AI 为学习源码专门设计的调用链记录机制。

它不是普通日志。

作用：

- 记录调用顺序
- 区分 Request / Background
- 帮助理解 Workflow
- 配合 VS Code 阅读源码

建议阅读：

```text
Volume 04

↓

Chapter 23
```

---

# 阅读过程中建议完成的练习

建议每完成一章，都完成下面四件事：

✅ 阅读源码

✅ 运行程序

✅ 对照 Learning Trace

✅ 用自己的语言解释执行流程

只有做到最后一步，才真正掌握了这一章。

---

# 与源码对应关系

教材中的所有内容，都尽量对应项目源码。

例如：

| 文档           | 对应源码                             |
| -------------- | ------------------------------------ |
| TaskService    | backend/app/services/task_service.py |
| Workflow       | backend/app/workflow/graph.py        |
| Repository     | backend/app/repositories/            |
| Learning Trace | backend/app/core/learning_trace.py   |
| EventPublisher | backend/app/events/publisher.py      |

建议一边阅读文档，一边打开对应源码。

---

# 如何使用本教材准备日本 SES 面试？

建议顺序：

```text
Volume 01

↓

Volume 02

↓

Volume 03

↓

Volume 04

↓

Volume 07
```

完成后，你应该能够：

- 介绍整个项目
- 解释程序执行流程
- 解释系统架构
- 回答 Agent 项目常见问题
- 用中文和日语介绍项目

---

# 学习完成后的能力成长

```text
不会

↓

能运行项目

↓

能阅读源码

↓

能理解架构

↓

能解释设计思想

↓

能够独立开发企业 AI 系统
```

这也是整套教材希望帮助你完成的成长路径。

---

# 本套教材目录

```text
docs/learning/

├── 00_READ_FIRST.md
├── 01_Foundation/
├── 02_Source_Code/
├── 03_Subsystem/
├── 04_Execution_Flow/
├── 05_Enterprise/
├── 06_AI/
└── 07_Interview/
```

每个 Volume 都包含独立的 README，建议按顺序阅读。

---

# 最后的建议

不要把这套教材当作一本普通的笔记。

建议采用下面的学习循环：

```text
阅读文档

↓

阅读源码

↓

运行程序

↓

观察 Learning Trace

↓

观察 Console Log

↓

Debug

↓

再次阅读文档

↓

总结

↓

向别人讲解
```

当你能够不看文档，仅凭源码解释整个执行流程时，就真正掌握了 Retail Insight AI。

---

# Welcome

欢迎开始学习 **Retail Insight AI 企业源码架构手册**。

建议现在打开：

```text
Volume 01

README.md
```

然后按照推荐顺序，一步一步完成整个学习旅程。

祝学习顺利！
