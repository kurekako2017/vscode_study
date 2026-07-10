
# Retail Insight AI 企业源码架构手册

# Volume 04：Execution Flow（源码执行流程）

# Chapter 18

# Documents API 执行全过程

> Enterprise Knowledge Management

---

# 文档信息

| 项目       | 内容                                            |
| ---------- | ----------------------------------------------- |
| Volume     | 04                                              |
| Chapter    | 18                                              |
| API        | Documents API                                   |
| 入口文件   | backend/app/api/documents.py                    |
| Service    | backend/app/services/document_service.py        |
| Repository | backend/app/repositories/document_repository.py |
| 推荐程度   | ⭐⭐⭐⭐⭐                                      |

---

# 学习目标

阅读本章后，你应该能够回答：

- Documents API 的执行流程是什么？
- 文档为什么不直接交给 Workflow？
- DocumentService 为什么存在？
- Repository 为什么独立？
- Workflow 是什么时候读取文档的？

---

# 一、接口说明（API）

Documents API 负责整个系统的文档管理。

主要包括：

```http
POST /api/documents

GET /api/documents

DELETE /api/documents/{id}
```

作用：

- 上传文档
- 查询文档
- 删除文档

Documents API

负责：

知识管理。

不是：

AI 分析。

---

# 二、HTTP Request 生命周期

上传文档：

```text
Browser

↓

POST /api/documents

↓

FastAPI

↓

documents.py

↓

DocumentService

↓

DocumentRepository

↓

Storage

↓

HTTP Response
```

整个过程：

没有：

Workflow。

---

# 三、源码入口 ⭐⭐⭐⭐⭐

打开：

```text
backend/app/api/documents.py
```

找到：

```python
@router.post(...)
```

或：

```python
@router.get(...)
```

这里就是：

Documents API

入口。

随后：

调用：

```python
DocumentService
```

处理业务。

---

# 四、源码执行流程 ⭐⭐⭐⭐⭐

上传：

```text
Browser

↓

POST /api/documents

↓

documents.py

↓

DocumentService

↓

DocumentRepository.save()

↓

Storage

↓

HTTP Response
```

查询：

```text
Browser

↓

GET /api/documents

↓

documents.py

↓

DocumentService

↓

Repository.list()

↓

JSON
```

删除：

```text
Browser

↓

DELETE

↓

DocumentService

↓

Repository.delete()
```

---

# 五、关键源码文件

| 文件                   | 职责              |
| ---------------------- | ----------------- |
| documents.py           | Router            |
| document_service.py    | 文档业务          |
| document_repository.py | 文档存储          |
| graph.py               | Workflow 调用入口 |

---

# 六、关键函数

## upload_document()

负责：

上传文档。

---

## get_document()

负责：

查询文档。

---

## list_documents()

负责：

返回：

文档列表。

---

## delete_document()

负责：

删除文档。

---

# 七、调用关系图 ⭐⭐⭐⭐⭐

```text
Browser
    │
    ▼
POST /documents
    │
    ▼
documents.py
    │
    ▼
DocumentService
    │
    ▼
DocumentRepository
    │
    ▼
Storage
```

Workflow：

不会：

直接：

保存文档。

---

# 八、Learning Trace 对应

Learning Trace：

例如：

```text
Documents API

↓

DocumentService

↓

Repository
```

不会：

进入：

Background。

因为：

这里只是：

文档管理。

---

# 九、Console Log 对应

Console：

例如：

```text
Document Uploaded

↓

Repository.save()

↓

200 OK
```

Learning Trace：

负责：

调用关系。

Console：

负责：

执行结果。

---

# 十、VS Code 阅读路线 ⭐⭐⭐⭐⭐

建议：

```text
documents.py

↓

DocumentService

↓

DocumentRepository

↓

graph.py
```

最后：

观察：

Research

如何：

读取：

Document。

---

# 十一、项目当前实现（Current Implementation）

Retail Insight AI 当前：

已经实现：

✅ Documents API

✅ 文档上传

✅ 文档查询

✅ 文档删除

✅ Repository

目前：

Workflow：

可以：

读取：

文档信息。

但是：

还没有：

完整：

Vector Search。

---

# 十二、企业版扩展（Future Enterprise Architecture）

未来：

推荐：

```text
Upload

↓

Chunk

↓

Embedding

↓

Vector Database

↓

Retriever

↓

Reranker

↓

LLM
```

推荐技术：

- LangChain
- pgvector
- Milvus
- Qdrant
- Hybrid Search

形成：

Enterprise RAG。

---

# 十三、为什么采用 Repository（Why）

如果：

Workflow：

直接：

操作：

Document。

以后：

Storage：

变化。

Workflow：

全部修改。

现在：

```text
Workflow

↓

DocumentService

↓

Repository

↓

Storage
```

职责：

完全分离。

---

# 十四、Java / Spring 对照

| Retail Insight AI | Spring Boot   |
| ----------------- | ------------- |
| Documents API     | Controller    |
| DocumentService   | Service       |
| Repository        | JpaRepository |
| Storage           | Database      |

设计：

一致。

---

# 十五、常见问题（FAQ）

### 为什么 Documents 不属于 Workflow？

因为：

Documents：

负责：

管理知识。

Workflow：

负责：

使用知识。

职责不同。

---

### Workflow 为什么不能直接访问数据库？

为了：

解耦。

统一：

Repository。

---

### 为什么现在没有 Vector DB？

因为：

当前：

属于：

Internal Document Retrieval。

未来：

升级：

Enterprise RAG。

---

# 十六、面试回答（中文）

面试官：

> Documents API 的执行流程是什么？

回答：

> Documents API 首先进入 documents.py，然后调用 DocumentService 处理业务逻辑，再通过 DocumentRepository 完成文档的保存、查询或删除。Workflow 不直接管理文档，而是在 Research 阶段通过 Repository 获取文档作为 AI 分析的上下文，实现文档管理与 AI Workflow 的解耦。

---

# 十七、面试回答（日语）

面接官：

> Documents API の実行フローを説明してください。

回答例：

> Documents API は documents.py を入口として、DocumentService が文書の登録・検索・削除などの業務処理を行います。その後 DocumentRepository がデータを保存・取得します。AI Workflow は文書を直接管理するのではなく、Research フェーズで Repository を通して必要な文書を取得し、AI のコンテキストとして利用する設計になっています。

---

# 十八、日本SES常见追问

### 为什么 Documents 不直接调用 LLM？

回答：

企业：

Document

与

AI

属于：

两个子系统。

Documents：

负责：

管理知识。

Workflow：

负责：

调用 AI。

保持：

职责单一。

---

# 十九、本章源码阅读任务 ⭐⭐⭐⭐⭐

完成下面练习：

① 打开：

```text
backend/app/api/documents.py
```

↓

② 阅读：

```text
DocumentService
```

↓

③ 阅读：

```text
DocumentRepository
```

↓

④ 打开：

```text
graph.py
```

↓

⑤ 找到：

Research

如何：

读取：

Document。

---

# 本章总结

一句话：

```text
Documents API

↓

DocumentService

↓

DocumentRepository

↓

Storage

↓

Workflow（Research）
```

Documents 子系统负责知识管理。

Workflow 子系统负责知识使用。

两者职责分离，是企业 AI Agent 的标准架构。

---

# 下一章

**Chapter 19：Approval API**

学习：

- Pending
- Approve
- Reject
- Workflow Resume
- Human-in-the-Loop
