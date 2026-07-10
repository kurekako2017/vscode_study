# Retail Insight AI 企业源码架构手册

# Volume 05：Enterprise（企业架构）

# Chapter 26

# Repository Pattern（仓储模式）

> Why Enterprise Systems Use Repository Pattern

---

## 学习目标

- 什么是 Repository Pattern？
- 为什么企业项目要使用 Repository？
- Retail Insight AI 如何实现 Repository？
- Repository 与 DAO、ORM 的区别。

---

## Repository Pattern 是什么？

Repository Pattern（仓储模式）负责统一管理数据访问，使业务层不直接依赖数据库。

```text
Service
    ↓
Repository
    ↓
Database
```

Repository 屏蔽底层存储实现，使 Service 更容易维护、测试和扩展。

---

## Retail Insight AI 中的实现

项目调用关系：

```text
Browser
    ↓
Router
    ↓
TaskService
    ↓
TaskRepository
    ↓
SQLite / InMemory
```

源码目录：

```text
backend/app/repositories/
```

典型 Repository：

- TaskRepository
- DocumentRepository
- ApprovalRepository

---

## 为什么企业采用 Repository？

- 数据库可替换（SQLite → PostgreSQL）
- 易于单元测试（Mock / Fake Repository）
- 职责分离（Service 负责业务，Repository 负责数据）
- 提高维护性与扩展性

---

## Repository 与 DAO

DAO 更关注数据库访问。

Repository 更关注领域对象（Domain Object）管理。

```text
Service
    ↓
Repository
    ↓
ORM
    ↓
Database
```

---

## Java / Spring 对照

| Retail Insight AI | Spring Boot |
|-------------------|-------------|
| TaskRepository | JpaRepository |
| Repository | Repository Interface |
| Service | Service |
| SQLAlchemy | Hibernate |

---

## VS Code 阅读路线

```text
backend/app/repositories/
    ↓
TaskRepository
    ↓
TaskService
    ↓
AnalysisWorkflow
```

---

## 面试回答（中文）

Repository Pattern 将数据访问逻辑与业务逻辑分离，使 Service 不依赖数据库实现，便于测试、维护以及数据库迁移，是现代企业系统中最常见的架构模式之一。

---

## 面试回答（日语）

Repository Pattern は Service とデータベースを疎結合にするための設計です。Repository を介してデータアクセスを行うことで、保守性・拡張性・テスト容易性を向上できます。

---

## 本章核心记忆图

```text
Browser
    ↓
Router
    ↓
Service
    ↓
Repository
    ↓
Database
```

---

## 下一章

Chapter 27：Dependency Injection（依赖注入）
