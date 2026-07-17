
# Enterprise Retail Intelligence Platform（ERIP）

# 企业业务流程学习指南

# ERIP Business Flow Learning Guide

---

# 1. 本文档目的

本指南不介绍 React、FastAPI 或 LangGraph。

本指南只回答一个问题：

> 企业为什么需要 ERIP？
>
> 用户在企业里每天是如何使用这个系统的？

理解了企业业务，再去学习源码会容易很多。

---

# 2. 企业案例背景

某日本零售企业（Retail Company）

2026 年 6 月经营会议发现：

> 关东地区饮料分类销售额比上月下降 12%。

管理层提出几个问题：

- 为什么销售下降？
- 是库存不足吗？
- 是促销活动效果不好吗？
- 是竞争店影响吗？
- 应该采取哪些改善措施？

因此经营企划部门开始使用 ERIP。

---

# 3. ERIP 在企业中的定位

ERIP 不是 ERP。

ERIP 不是 POS。

ERIP 不是 BI。

ERIP 是：

> 企业经营分析平台（Enterprise Retail Intelligence Platform）

作用：

将企业内部资料

↓

企业知识

↓

经营分析

↓

审批流程

连接成一个完整业务流程。

---

# 4. 整体业务流程

```text
文書管理
        │
        ▼
RAG検索
        │
        ▼
分析依頼
        │
        ▼
承認管理
        │
        ▼
最终经营分析报告
```

企业所有业务都围绕这一条主线展开。

---

# 5. 第一阶段：文書管理（Documents）

## 为什么需要？

企业每天都会产生大量资料：

- 销售日报
- KPI
- 门店库存
- 顾客反馈
- 活动报告
- 商品资料

这些资料如果只是放在共享文件夹里，

AI 无法理解。

因此第一步就是：

> 把企业资料登记到 ERIP。

---

## 实际业务

经营企划人员上传：

```
関東地域_飲料売上実績.md
```

里面可能包含：

```
2026 年 6 月

关东地区饮料销售下降 12%

东京西部缺货率达到 8%

促销转化率低于计划值
```

然后执行：

```
Upload

↓

Import

↓

Chunk
```

Backend 最终生成：

```
document_id

import_id

Chunk
```

这些数据以后都会成为企业知识。

---

## 本阶段输出

企业知识库增加：

```
document_id

Chunk

metadata
```

这些数据以后供 RAG 使用。

---

# 6. 第二阶段：RAG検索（Internal Knowledge Retrieval）

## 为什么需要？

企业不能靠 AI 瞎回答。

所有分析都必须：

> 有依据。

因此：

先检索企业内部资料。

---

## 实际业务

经营企划输入：

```
関東地域 飲料 売上減少
```

系统开始：

```
Keyword Retrieval

↓

找到 Chunk

↓

返回引用
```

例如：

```
Chunk 1

东京西部缺货率 8%

---------

Chunk 2

促销活动效果低于计划值
```

然后进一步提问：

```
関東地域の飲料カテゴリの売上減少原因は？
```

系统返回：

```
主要原因：

库存不足

促销效果不好

碳酸饮料需求下降
```

同时返回：

```
citation

document_id

chunk_id
```

---

## 企业意义

RAG 不负责经营决策。

RAG 负责：

> 找依据。

它回答：

"为什么这么说？"

而不是：

"应该怎么经营。"

---

# 7. 第三阶段：分析依頼（Analysis）

## 为什么需要？

RAG 只是找到资料。

真正经营分析还需要：

- KPI
- 调研
- 报告

因此开始：

分析任务。

---

## 实际业务

经营企划输入：

```
请分析：

关东地区饮料销售下降原因，

并提出改善方案。
```

Backend：

```
Task

↓

Background Task

↓

LangGraph

↓

KPI

↓

Research

↓

Report
```

最终生成：

```
task_id

report
```

例如：

```
问题：

库存不足

促销效果差

商品结构不合理

---------

建议：

增加库存

重新设计促销

调整商品组合
```

---

## 企业意义

这里开始真正生成：

经营分析报告。

不是简单检索资料。

---

# 8. 第四阶段：承認管理（Approval）

## 为什么需要？

企业分析不能直接交给董事。

必须：

审批。

因此：

报告生成后，

进入审批流程。

---

## 实际业务

负责人收到：

```
task_id
```

点击：

```
承認
```

或者：

```
却下
```

或者：

```
修正依頼
```

系统生成：

```
approval_id

report_version_id
```

记录：

谁审批？

什么时候审批？

审批意见是什么？

形成完整审计记录。

---

## 企业意义

企业真正使用的是：

经过审批的经营报告。

而不是：

任何人随便生成的 AI 内容。

---

# 9. 当前系统真实实现状态

## 已实现

✓ 文書管理

✓ Upload

✓ Import

✓ Chunk

✓ Keyword Retrieval

✓ Internal RAG

✓ Analysis Workflow

✓ Approval

---

## 部分实现

△ RAG 与 Analysis

目前：

人工衔接。

不是自动。

---

△ Analysis 与 Approval

目前：

复制 task_id。

不是自动。

---

## 尚未实现

× 真实 LLM

× pgvector

× Embedding

× 自动跨页面流程

× 最终报告汇总页面

---

# 10. 当前页面之间的数据关系

```
Documents

↓

document_id

Chunk

↓

RAG

↓

citation

↓

（人工整理）

↓

Tasks

↓

task_id

↓

Approval

↓

approval_id

↓

report_version_id
```

注意：

目前：

只有 Backend Repository 内部真正共享数据。

React 页面之间：

没有自动传递。

---

# 11. 为什么要按这个顺序学习？

建议：

① Documents

理解：

企业资料如何进入系统。

↓

② RAG

理解：

资料如何被检索。

↓

③ Tasks

理解：

资料如何变成经营分析。

↓

④ Approval

理解：

经营报告如何进入审批。

↓

⑤ 再学习源码。

这样：

看到 Router、

Service、

Workflow、

Repository

就知道：

它们分别在企业业务中负责什么。

---

# 12. 总结

ERIP 不是一个 AI Demo。

它模拟的是：

日本零售企业真实经营分析流程。

整个业务只有四个步骤：

```
Documents

↓

RAG

↓

Tasks

↓

Approval
```

先理解业务。

再理解代码。

这是学习 ERIP 最有效的方法。

## V1.0 正式业务链（增量）

```text
文書管理
→ RAG検索
→ AI分析（low_cost）
→ 董事会报告（high_quality）
→ 承認管理
→ Persistent Audit
```

- 普通 RAG / Retrieval：默认可不调用真实 Provider。
- AI 分析与董事会报告：必须经 LLM Gateway；默认 stub；Evidence Gate + Idempotency-Key。
- 审批：submit **201** `pending_approval`；employee approve **403**；manager approve **200**。
- 步骤级验收表：`TEST_CASES.md` Scenario01（24 步）；本文件不复制整表。
