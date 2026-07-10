# Retail Insight AI 企业源码架构手册

# Volume 06：AI Engine（AI 引擎）

# Chapter 43

# Vector Search（向量检索）

> Search Knowledge by Meaning Instead of Keywords

---

# 文档信息

| 项目     | 内容                               |
| -------- | ---------------------------------- |
| Volume   | 06                                 |
| Chapter  | 43                                 |
| 技术主题 | Vector Search                      |
| 难度     | ⭐⭐⭐⭐⭐                         |
| 推荐程度 | ⭐⭐⭐⭐⭐                         |
| 对应源码 | backend/app/retrieval/（未来扩展） |

---

# 学习目标

阅读本章后，你应该能够回答：

- 什么是 Vector Search？
- Embedding 是什么？
- Cosine Similarity 如何工作？
- 为什么企业 AI 使用 pgvector？
- Retail Insight AI 如何实现向量检索？

---

# 一、为什么需要 Vector Search？

传统数据库：

采用：

```text
Keyword

↓

SQL

↓

Result
```

例如：

```sql
WHERE title LIKE '%Sales%'
```

只能找到：

包含：

Sales

的文档。

但是：

如果用户问：

```text
销售下降原因
```

数据库：

无法知道：

它和：

```text
Revenue Decrease
```

其实：

意思：

相近。

所以：

需要：

Semantic Search。

---

# 二、什么是 Vector？

Vector：

就是：

Embedding：

生成的一组数字。

例如：

```text
销售分析

↓

Embedding

↓

[0.23,0.81,-0.12,...]
```

以后：

所有：

文档：

都会：

转换：

Vector。

---

# 三、Embedding 是什么？

Embedding：

负责：

把：

自然语言

转换：

向量。

例如：

```text
Customer

↓

Embedding

↓

Vector
```

Embedding：

不会：

回答问题。

它：

只负责：

表示：

语义。

---

# 四、Vector Search 工作流程 ⭐

整个流程：

```text
Question

↓

Embedding

↓

Query Vector

↓

Vector Database

↓

Top-K Documents

↓

Prompt

↓

LLM
```

Retriever：

负责：

组织：

整个过程。

---

# 五、源码目录结构 ⭐

建议未来：

增加：

```text
backend/app/retrieval/

    embedding.py

    vector_store.py

    similarity.py
```

Workflow：

直接：

调用：

Retriever。

Retriever：

负责：

Vector Search。

---

# 六、关键源码文件 ⭐

未来：

建议：

```text
embedding.py

↓

vector_store.py

↓

retriever.py
```

Workflow：

无需：

知道：

Vector：

细节。

---

# 七、Cosine Similarity ⭐

企业：

最常见：

计算方式：

```text
Cosine Similarity
```

例如：

```text
Question Vector

↓

Document Vector

↓

Similarity

↓

0.98
```

数值：

越接近：

1。

说明：

越相似。

---

# 八、Top-K Ranking ⭐

企业：

不会：

返回：

全部：

文档。

通常：

```text
Top3

Top5

Top10
```

例如：

```text
Similarity

0.97

0.93

0.90
```

只保留：

最高：

几个。

---

# 九、pgvector ⭐

建议：

企业：

采用：

```text
PostgreSQL

+

pgvector
```

原因：

- 一个数据库
- SQL 管理
- 支持向量
- 运维简单

Retail Insight AI：

推荐：

未来：

采用：

pgvector。

---

# 十、Architecture Thinking ⭐

为什么：

不用：

Elasticsearch？

因为：

企业：

通常：

需要：

```text
Business Data

+

Vector

一起：

管理
```

PostgreSQL

pgvector：

更加简单。

---

# 十一、Retail Insight AI 实施方案 ⭐

未来：

建议：

增加：

```text
Knowledge Loader

↓

Chunk

↓

Embedding

↓

pgvector

↓

Retriever

↓

Workflow
```

Workflow：

无需：

修改。

---

# 十二、Learning Trace 对应 ⭐

建议：

增加：

```text
Embedding Created

↓

Vector Search

↓

Top5 Selected

↓

Prompt Ready
```

方便：

观察：

Retriever。

---

# 十三、Debug Guide ⭐

建议：

断点：

```text
① Embedding

↓

② Vector Search

↓

③ Top-K

↓

④ Prompt

↓

⑤ LLM
```

---

# 十四、Performance & Cost ⭐

建议：

统计：

```text
Embedding Time

↓

Vector Search Time

↓

Prompt Tokens

↓

LLM Cost
```

帮助：

优化：

RAG。

---

# 十五、Current vs Enterprise

Current：

```text
Workflow

↓

LLM
```

Enterprise：

```text
Workflow

↓

Retriever

↓

Embedding

↓

pgvector

↓

Prompt

↓

LLM
```

---

# 十六、Java / Spring 对照 ⭐

| Retail Insight AI | Spring AI            |
| ----------------- | -------------------- |
| Embedding         | EmbeddingModel       |
| Vector Store      | PgVectorStore        |
| Retriever         | VectorStoreRetriever |
| Similarity        | Similarity Search    |

---

# 十七、VS Code 阅读路线 ⭐

建议：

```text
retriever.py

↓

embedding.py

↓

vector_store.py

↓

Workflow
```

---

# 十八、企业扩展（Enterprise）

未来：

建议：

增加：

```text
ANN Search

↓

Hybrid Search

↓

Re-Ranking

↓

Semantic Cache
```

进一步：

提升：

RAG。

---

# 十九、面试回答（中文）

为什么企业 AI 使用 Vector Search？

因为自然语言表达方式很多，仅依靠关键词检索容易遗漏相关内容。Vector Search 利用 Embedding 将文本转换为向量，通过语义相似度进行检索，即使表达不同，也能找到真正相关的知识。

---

# 二十、面试回答（日文）

なぜ Vector Search を利用するのですか。

Vector Search は単なるキーワード検索ではなく、意味の近い文章を検索できます。そのため、企業の Knowledge Base 検索や RAG システムで広く利用されています。

---

# 二十一、日本 SES 常见追问

### Q：为什么 pgvector 很受欢迎？

因为：

- PostgreSQL 扩展
- 运维简单
- SQL 与向量统一管理
- 成本低
- 与业务数据天然集成

---

# 二十二、本章练习 ⭐

完成下面练习：

① 设计：

Knowledge Table。

② 设计：

Embedding Table。

③ 思考：

为什么：

Top-100

通常：

没有：

Top-5：

效果好？

---

# 二十三、本章核心记忆图 ⭐

```text
Question

↓

Embedding

↓

Query Vector

↓

pgvector

↓

Top-K

↓

Prompt

↓

LLM
```

---

# 二十四、本章总结

一句话：

```text
Embedding

负责：

理解语义

↓

Vector Search

负责：

寻找知识

↓

LLM

负责：

完成推理
```

Vector Search 是企业 RAG 系统的核心能力，它通过 Embedding 和向量数据库实现语义检索，为 LLM 提供最相关的上下文，从而提高 AI 回答的准确性与可靠性。

---

# 下一章

**Chapter 44：AI Streaming（AI 流式输出）**

学习：

- Token Streaming
- SSE
- Progressive Response
- Real-time AI
- Streaming Architecture
