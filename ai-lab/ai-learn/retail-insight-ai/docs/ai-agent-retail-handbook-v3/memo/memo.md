# AI Learn Concept Map（企业 AI 后端学习地图）

> **文档定位**

本系列文档用于建立企业 AI 后端项目的知识体系。

它不是：

- 术语手册
- API 文档
- 源码说明

而是：

> 建立知识之间联系（Concept Map）。

正式术语统一维护在：

```
ai-lab/术语速查表.md
```

---

# 为什么要写 Concept Map？

很多知识点单独看都懂：

- HTTP
- FastAPI
- Swagger
- RAG
- Workflow
- Repository

但是不知道：

它们之间是什么关系？

企业为什么这么设计？

Concept Map 就是回答：

> 为什么？

---

# 学习目标

本系列主要帮助建立：

- 企业 AI 后端整体认识
- 企业项目开发流程
- 系统架构理解
- 源码阅读能力
- 日本企业面试表达能力

---

# 学习路线

建议严格按照下面顺序。

```
Python
    ↓
FastAPI
    ↓
HTTP
    ↓
OpenAPI
    ↓
Swagger
    ↓
Router
    ↓
Service
    ↓
Repository
    ↓
Database
    ↓
Document
    ↓
RAG
    ↓
Workflow
    ↓
Approval
    ↓
RBAC
    ↓
Audit
    ↓
Enterprise AI Backend
```

---

# Concept Map 目录

|编号|主题|状态|
|------|--------------------------|------|
|01|Python → FastAPI → OpenAPI → Swagger → ReDoc|✅|
|02|HTTP（GET / POST / PUT / DELETE）|计划|
|03|FastAPI 生命周期|计划|
|04|Router → Service → Repository|计划|
|05|Request / Response / Schema|计划|
|06|Document System|计划|
|07|RAG 全流程|计划|
|08|Workflow 与 Agent|计划|
|09|Approval Workflow|计划|
|10|RBAC 与 Audit|计划|
|11|Repository Pattern|计划|
|12|Provider Pattern|计划|
|13|Enterprise AI Backend Architecture|计划|
|14|企业测试体系|计划|
|15|前后端联调|计划|
|16|企业部署流程|计划|

---

# 与其它文档的关系

|文档|作用|
|------|----------------------------|
|Concept Map|理解为什么这样设计|
|术语速查表|理解术语是什么意思|
|LEARNING_API_WALKTHROUGH|学习接口|
|TEST_CASES|学习测试|
|CODE_STUDY_GUIDE|学习源码|

---

# 学习建议

每学习一个模块：

① 阅读 memo

↓

② Swagger 实际调用

↓

③ 阅读源码

↓

④ 看测试

↓

⑤ 自己总结

---

# 最终目标

最终形成属于自己的：

> Enterprise AI Backend Notebook

以后：

- 日本面试
- 阅读源码
- 工作开发

全部使用这一套知识体系。
