
# Retail Insight AI 企业源码架构手册

# Volume 06：AI Engine（AI 引擎）

# Chapter 42

# RAG Architecture（Retrieval-Augmented Generation，检索增强生成）

> Build Enterprise AI with Knowledge Retrieval

---

# 文档信息

| 项目     | 内容                                      |
| -------- | ----------------------------------------- |
| Volume   | 06                                        |
| Chapter  | 42                                        |
| 技术主题 | RAG Architecture                          |
| 难度     | ⭐⭐⭐⭐⭐                                |
| 推荐程度 | ⭐⭐⭐⭐⭐                                |
| 对应源码 | backend/app/workflow/graph.py（未来扩展） |

---

# 学习目标

阅读本章后，你应该能够回答：

- 什么是 RAG？
- 为什么企业 AI 需要 RAG？
- Retriever、Embedding、Vector Database 分别负责什么？
- Retail Insight AI 如何接入 RAG？
- 如何设计企业级知识库？

---

# 一、为什么需要 RAG？

普通 LLM：

```text
Question

↓

LLM

↓

Answer
```

模型只能依赖：

训练数据。

无法知道：

企业最新知识。

例如：

```text
销售日报

公司制度

审批流程

KPI 指标

运营文档
```

因此：

企业 AI：

必须：

增加：

Knowledge Base。

---

# 二、什么是 RAG？

RAG：

Retrieval-Augmented Generation

中文：

检索增强生成。

整个流程：

```text
Question

↓

Retriever

↓

Knowledge Base

↓

Prompt

↓

LLM

↓

Answer
```

Retriever：

负责：

找资料。

LLM：

负责：

理解资料。

---

# 三、Retail Insight AI 当前实现（Current）

当前：

Workflow：

```text
Task

↓

AnalysisWorkflow

↓

Provider

↓

LLM

↓

Report
```

未来：

建议：

增加：

Retriever：

```text
Task

↓

Workflow

↓

Retriever

↓

Prompt

↓

LLM

↓

Report
```

Workflow：

无需：

大幅修改。

---

# 四、源码目录结构 ⭐

当前：

```text
backend/app/workflow/

↓

graph.py
```

建议未来新增：

```text
backend/app/retrieval/

    retriever.py

    embedding.py

    vector_store.py

backend/app/knowledge/

    loader.py

    chunker.py
```

这样：

RAG：

职责更加清晰。

---

# 五、关键源码文件 ⭐

当前：

```text
AnalysisWorkflow

↓

stream()
```

未来：

增加：

```text
Retriever.search()

↓

PromptBuilder

↓

Provider
```

Workflow：

负责：

调用：

Retriever。

Retriever：

负责：

准备：

Context。

---

# 六、RAG 执行流程 ⭐

```text
User Question

↓

Embedding

↓

Vector Search

↓

Top-K Documents

↓

Prompt Build

↓

LLM

↓

Answer
```

Retriever：

永远：

不会：

生成答案。

Retriever：

只负责：

找知识。

---

# 七、Retail Insight AI 实施方案 ⭐

建议：

未来：

Knowledge Base：

包括：

```text
销售日报

↓

KPI 指标

↓

审批记录

↓

分析报告

↓

运营手册

↓

FAQ

↓

公司制度
```

Workflow：

统一：

调用：

Retriever。

所有：

AI：

共享：

同一个：

Knowledge Base。

---

# 八、Chunk Design（文本切分）⭐

企业：

通常：

不会：

整篇：

文档：

Embedding。

建议：

```text
Chunk Size

500~800 Tokens

Overlap

50~100 Tokens
```

例如：

```text
Document

↓

Chunk1

↓

Chunk2

↓

Chunk3
```

这样：

提高：

检索质量。

---

# 九、Embedding ⭐

Embedding：

负责：

把：

文本：

转换：

向量。

例如：

```text
Document

↓

Embedding Model

↓

Vector
```

推荐：

企业：

保存：

Embedding：

不要：

重复生成。

---

# 十、Vector Database ⭐

未来：

建议：

采用：

```text
PostgreSQL

+

pgvector
```

优点：

- 一个数据库
- 管理方便
- 成本低
- 支持 SQL
- 支持向量检索

---

# 十一、AnalysisWorkflow 如何接入 RAG ⭐

未来：

Workflow：

建议：

增加：

一个：

Node：

```text
Retrieve Knowledge

↓

Research

↓

Report
```

整个：

Workflow：

变成：

```text
Task

↓

Retriever

↓

Research

↓

Report
```

---

# 十二、Learning Trace 对应 ⭐

建议：

增加：

```text
Workflow Started

↓

Retrieve Documents

↓

Top5 Documents

↓

Prompt Generated

↓

LLM Response

↓

Completed
```

帮助：

调试：

Retriever。

---

# 十三、Debug Guide ⭐

建议：

断点：

```text
① AnalysisWorkflow

↓

② Retriever.search()

↓

③ Prompt Build

↓

④ Provider

↓

⑤ Report
```

观察：

Retriever：

返回：

哪些：

文档。

---

# 十四、Performance & Cost ⭐

企业：

关注：

不仅：

正确率。

还关注：

成本。

建议：

统计：

```text
Retriever Latency

↓

Embedding Cost

↓

Prompt Tokens

↓

LLM Tokens

↓

Cache Hit Rate
```

控制：

AI：

成本。

---

# 十五、Architecture Thinking ⭐

为什么：

不用：

把：

全部：

文档：

放进 Prompt？

因为：

LLM：

Context Window：

有限。

企业：

通常：

Retriever：

返回：

Top-K：

文档。

例如：

```text
Top3

Top5

Top10
```

降低：

Token：

消耗。

---

# 十六、Current vs Enterprise

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

Vector Search

↓

Prompt

↓

LLM
```

AI：

真正：

拥有：

企业知识。

---

# 十七、Java / Spring 对照 ⭐

| Retail Insight AI | Spring AI      |
| ----------------- | -------------- |
| Retriever         | VectorStore    |
| Embedding         | EmbeddingModel |
| pgvector          | PgVectorStore  |
| Workflow          | AI Flow        |

---

# 十八、VS Code 阅读路线 ⭐

建议：

```text
graph.py

↓

AnalysisWorkflow

↓

Retriever（未来）

↓

Provider
```

理解：

Retriever：

如何：

进入：

Workflow。

---

# 十九、企业扩展（Enterprise）

建议：

未来：

增加：

```text
Hybrid Search

↓

BM25

+

Vector Search

↓

Re-Ranking

↓

Context Compression

↓

LLM
```

形成：

Hybrid RAG。

---

# 二十、面试回答（中文）

RAG 为什么比直接调用 LLM 更适合企业？

因为企业知识每天都在变化，而 LLM 的训练数据不会实时更新。RAG 可以在回答前先检索企业知识库，将最新文档作为上下文提供给模型，因此能够兼顾知识的准确性、时效性和可维护性，而无需频繁重新训练模型。

---

# 二十一、面试回答（日文）

RAG を利用するメリットは何ですか。

RAG は企業の最新ドキュメントを Retriever で検索し、その結果を Prompt に追加してから LLM が回答します。そのため、モデルを再学習しなくても最新情報を利用でき、企業システムに適しています。

---

# 二十二、日本 SES 常见追问

### Q：RAG 和 Fine-tuning 有什么区别？

| RAG          | Fine-tuning  |
| ------------ | ------------ |
| 更新知识简单 | 需要重新训练 |
| 成本较低     | 成本较高     |
| 企业文档     | 固定任务     |
| 推荐企业使用 | 推荐模型优化 |

---

# 二十三、本章练习 ⭐

完成下面练习：

① 设计：

Retail Insight AI

Knowledge Base。

② 设计：

Chunk Strategy。

③ 设计：

pgvector

数据表。

④ 思考：

Retriever

应该：

插入：

Workflow：

哪个：

Node？

---

# 二十四、本章核心记忆图 ⭐

```text
Question

↓

Retriever

↓

Embedding

↓

Vector Search

↓

Top-K Documents

↓

Prompt

↓

LLM

↓

Answer
```

---

# 本章总结

一句话：

```text
Retriever

负责找知识

↓

LLM

负责推理

↓

RAG

负责连接两者
```

RAG 的核心价值不是替代 LLM，而是**让 LLM 能够使用企业最新知识完成推理**。对于 Retail Insight AI 来说，未来在 `AnalysisWorkflow` 中增加 Retriever 节点，并结合 PostgreSQL + pgvector 构建企业知识库，将是迈向 Enterprise AI Platform 的重要一步。

---

# 下一章

**Chapter 43：Vector Search（向量检索）**

学习：

- Embedding
- Cosine Similarity
- pgvector
- ANN Search
- Top-K Ranking
- Enterprise Vector Database
