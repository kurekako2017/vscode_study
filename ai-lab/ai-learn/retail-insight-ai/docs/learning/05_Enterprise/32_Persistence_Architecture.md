# Retail Insight AI 企业源码架构手册

# Volume 05：Enterprise（企业架构）

# Chapter 32

# Persistence Architecture（企业持久化架构）

> Build Reliable Enterprise Data Systems

---

# 文档信息

| 项目     | 内容                                |
| -------- | ----------------------------------- |
| Volume   | 05                                  |
| Chapter  | 32                                  |
| 技术主题 | Persistence Architecture            |
| 难度     | ⭐⭐⭐⭐⭐                          |
| 推荐程度 | ⭐⭐⭐⭐⭐                          |
| 对应模块 | Repository / Database / Transaction |

---

# 学习目标

阅读本章后，你应该能够回答：

- 什么是 Persistence（持久化）？
- Repository 与 Database 的关系是什么？
- SQLite、PostgreSQL、Redis 分别负责什么？
- 什么是 Transaction（事务）？
- 什么是 Unit of Work？
- 企业 AI 平台为什么需要 pgvector？

---

# 一、什么是 Persistence？

Persistence（持久化）是指：

> **把程序运行过程中产生的数据安全地保存下来，并在程序重启后仍然能够读取。**

例如：

```text
Task

↓

Repository

↓

Database
```

如果没有持久化：

程序关闭以后：

所有任务都会消失。

因此：

企业系统必须实现可靠的数据持久化。

---

# 二、Retail Insight AI 当前实现（Current）

当前项目的数据流：

```text
Browser

↓

TaskService

↓

Repository

↓

SQLite
```

Repository 是唯一的数据访问入口。

Service 不直接操作数据库。

这样数据库可以随时替换。

---

# 三、Source Binding（源码绑定）

建议阅读：

```text
backend/app/repositories/
```

重点查看：

```text
task_repository.py
document_repository.py
approval_repository.py
```

再结合：

```text
backend/app/services/task_service.py
```

观察：

Service 如何通过 Repository 完成数据访问。

---

# 四、企业数据库分层

在企业项目中：

不同数据库承担不同职责。

```text
                Application
                     │
                     ▼
                Repository Layer
      ┌──────────┬──────────┬──────────┐
      ▼          ▼          ▼
 PostgreSQL    Redis     Vector DB
      │          │          │
  Business    Cache     Embedding
    Data
```

不要让一个数据库承担所有工作。

---

# 五、SQLite、PostgreSQL、Redis 的定位

## SQLite

适合：

- MVP
- Demo
- 本地开发

优点：

- 无需安装
- 文件型数据库
- 部署简单

缺点：

- 并发能力有限
- 不适合大型企业系统

---

## PostgreSQL

适合：

- 企业生产环境
- 高并发
- ACID 事务

优点：

- 稳定
- 扩展能力强
- 支持 JSON、全文检索、pgvector

Retail Insight AI 企业版推荐采用 PostgreSQL。

---

## Redis

Redis 不是数据库替代品。

主要负责：

```text
Cache

Session

Queue

Lock
```

例如：

AI Workflow：

生成结果后：

可以缓存到 Redis。

减少重复计算。

---

# 六、Transaction（事务）

事务（Transaction）保证：

> **一组操作要么全部成功，要么全部失败。**

例如：

```text
Create Task

↓

Save Report

↓

Publish Event
```

如果：

第二步失败：

第一步也必须回滚。

这就是事务。

---

# 七、Unit of Work

Unit of Work（工作单元）负责：

统一管理：

多个 Repository 操作。

例如：

```text
TaskRepository

↓

DocumentRepository

↓

ApprovalRepository
```

一起提交。

一起回滚。

企业系统常与 Repository Pattern 配合使用。

---

# 八、Connection Pool（连接池）

数据库连接：

创建成本很高。

企业项目通常采用：

```text
Application

↓

Connection Pool

↓

Database
```

连接可以重复使用。

提高性能。

FastAPI 常与 SQLAlchemy Connection Pool 配合使用。

---

# 九、Migration（数据库迁移）

企业项目不会：

手工修改数据库。

而是使用：

```text
Migration

↓

Alembic

↓

Database
```

优点：

- 可追踪
- 可回滚
- 多人协作一致

---

# 十、pgvector 与 AI 系统

AI 系统除了业务数据：

还需要保存：

Embedding。

例如：

```text
Document

↓

Embedding

↓

pgvector

↓

Semantic Search
```

因此：

PostgreSQL + pgvector

已经成为企业 AI 平台的主流方案之一。

---

# 十一、Architecture Thinking（架构思考）

为什么：

不用：

一个数据库：

解决所有问题？

因为：

不同类型数据：

访问模式不同。

例如：

```text
Task

↓

PostgreSQL

----------------

Cache

↓

Redis

----------------

Embedding

↓

pgvector
```

分层后：

系统更容易扩展。

---

# 十二、Java / Spring 对照

| Retail Insight AI | Spring Boot        |
| ----------------- | ------------------ |
| Repository        | JpaRepository      |
| Transaction       | @Transactional     |
| Migration         | Flyway / Liquibase |
| PostgreSQL        | PostgreSQL         |
| Redis             | Redis              |

---

# 十三、VS Code 阅读路线

建议：

```text
backend/app/repositories/

↓

TaskRepository

↓

TaskService

↓

Database Config
```

观察：

数据如何进入 Repository。

---

# 十四、Learning Trace 对应

Learning Trace：

通常会看到：

```text
TaskService

↓

Repository

↓

Save Task

↓

Completed
```

帮助确认：

数据持久化已经完成。

---

# 十五、Enterprise Roadmap

Retail Insight AI 企业版建议：

```text
SQLite

↓

PostgreSQL

↓

pgvector

↓

Redis

↓

RabbitMQ
```

形成：

完整企业数据平台。

---

# 十六、面试回答（中文）

为什么企业 AI 平台推荐 PostgreSQL + pgvector？

PostgreSQL 提供稳定的事务能力和丰富的数据类型，而 pgvector 可以直接存储 Embedding，并支持向量相似度检索。对于需要 RAG、语义搜索和知识库检索的 AI 系统，这种组合能够同时满足业务数据和 AI 数据的存储需求。

---

# 十七、面试回答（日语）

なぜ PostgreSQL と pgvector を利用するのですか。

PostgreSQL は高い信頼性とトランザクション機能を備えています。また pgvector を利用することで Embedding を保存し、ベクトル検索を実現できます。そのため、RAG や AI Knowledge Base を構築する企業システムで広く利用されています。

---

# 十八、日本 SES 常见追问

### Q：Redis 可以替代 PostgreSQL 吗？

回答：

不能。

Redis：

负责：

缓存。

PostgreSQL：

负责：

业务数据。

两者：

职责不同。

通常：

一起使用。

---

# 十九、本章练习

请完成：

① 查看：

```text
backend/app/repositories/
```

↓

② 思考：

哪些数据应该进入 PostgreSQL？

↓

③ 思考：

哪些数据适合 Redis？

↓

④ 思考：

未来哪些数据应该保存到 pgvector？

---

# 二十、本章核心记忆图

```text
Application
      │
      ▼
 Repository
      │
 ┌────┼─────────────┐
 ▼    ▼             ▼
PostgreSQL      Redis      pgvector
 │               │            │
Business      Cache     Embedding
 Data
```

---

# 本章总结

一句话：

```text
Business Data

↓

PostgreSQL

----------------

Cache

↓

Redis

----------------

AI Knowledge

↓

pgvector
```

Persistence Architecture 的目标不是"选择一个数据库"，而是**根据数据类型选择合适的存储方案**。Repository 统一访问入口，Transaction 保证一致性，pgvector 支撑 AI 检索能力，共同构成企业级 AI 平台的数据基础。

---

# 下一章

**Chapter 33：Scalability Architecture（可扩展架构）**

学习：

- Horizontal Scaling
- Load Balancer
- Redis
- RabbitMQ
- Worker
- 高并发 AI Workflow
