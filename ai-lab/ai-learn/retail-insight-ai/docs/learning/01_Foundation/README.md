
# Retail Insight AI 企业源码架构手册

# Volume 01：Foundation（基础篇）

> Everything starts here.

---

# 本册定位

Foundation（基础篇）负责建立整个项目的学习基础。

这一册不会深入讲解具体源码，而是帮助读者理解：

- 项目整体结构
- 学习路线
- 环境启动
- API 调试
- 测试方法
- 阅读源码的方法

建议第一次阅读 Retail Insight AI 时，从本册开始。

---

# 学习目标

完成本册后，你应该能够：

✅ 启动整个项目

✅ 理解项目目录结构

✅ 阅读 API 文档

✅ 理解 HTTP 请求生命周期

✅ 知道源码应该从哪里开始阅读

---

# 学习路线

建议按照下面顺序阅读：

```
CODE_STUDY_GUIDE

↓

LEARNING_API_WALKTHROUGH

↓

RUNBOOK_LOCAL

↓

TEST_CASES
```

不要跳着阅读。

---

# 对应源码

主要对应：

```
backend/

↓

main.py

↓

api/

↓

services/
```

本册不会深入研究具体业务代码。

重点：

建立整体认识。

---

# 本册目录

## LEARNING_API_WALKTHROUGH.md

学习：

整个项目：

HTTP 生命周期。

推荐指数：

⭐⭐⭐⭐⭐

---

## RUNBOOK_LOCAL.md

学习：

项目如何启动。

包括：

- Backend
- Frontend
- Docker

推荐指数：

⭐⭐⭐⭐

---

## TEST_CASES.md

学习：

如何验证：

整个系统。

推荐指数：

⭐⭐⭐

---

# 阅读建议

第一次：

快速阅读。

↓

第二次：

边运行项目边阅读。

↓

第三次：

结合 Learning Trace。

效果最佳。

---

# 阅读完成后

继续阅读：

```
02_Source_Code
```

开始真正阅读源码。

---

# 学习路线总览

```
Foundation

↓

Source Code

↓

Subsystem

↓

Execution Flow

↓

Enterprise

↓

AI

↓

Interview
```

---

# 本册总结

Foundation 的目标只有一个：

**帮助你建立整个 Retail Insight AI 的整体认识。**

不要急于研究源码。

先知道：

整个系统是什么。

下一册：

**Volume 02：Source Code（源码精读）**

## V1.0 阅读顺序（增量）

1. `RUNBOOK_LOCAL.md` 顶部权威入口（L/M/N）
2. `LEARNING_API_WALKTHROUGH.md` 接口学习
3. `TEST_CASES.md` 测试含义 + Scenario01
4. `CODE_STUDY_GUIDE.md` 源码顺序
5. `ERIP_BUSINESS_FLOW_LEARNING_GUIDE.md` 业务链
6. `../02_Frontend/FRONTEND_SOURCE_LEARNING_GUIDE.md` 前端与 Lifecycle/Dashboard

数字与启动命令以 RUNBOOK / VERIFY 为准，本 README 不重复大段命令。
