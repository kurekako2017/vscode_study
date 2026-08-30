# Databricks Free Edition｜GitHub 导入简明指南

## 推荐方式：Git folder

```text
GitHub Repository
        ↓
Databricks Git folder
        ↓
Workspace
        ↓
打开 Notebook / Python / SQL
        ↓
使用 Databricks 计算资源执行
```

### 基本步骤

```text
Workspace
 ↓
自己的用户目录
 ↓
New / 新建
 ↓
Git folder
 ↓
填写 Repository URL
 ↓
Create
```

当前主学习仓库：

```text
DataWithBaraa/databricks_bootcamp_2026
```

---

## Clone 后不要直接 Run All

先：

```text
README
 ↓
目录结构
 ↓
Setup
 ↓
第一个 Notebook
 ↓
逐 Cell Run
```

因为示例可能依赖：

- Catalog
- Schema
- Volume
- 数据文件路径
- 前置 Notebook
- Free Edition 不支持的功能

---

## 每个 Notebook 固定看 5 件事

```text
1. Input 是什么？
2. 从哪里读取？
3. 做什么加工？
4. Output 到哪里？
5. 业务目的是什么？
```

---

## 最常用的结果确认

PySpark：

```python
display(df)
```

SQL：

```sql
SELECT *
FROM catalog.schema.table
LIMIT 100;
```

行数：

```sql
SELECT COUNT(*)
FROM catalog.schema.table;
```

重点不是“Cell 变绿”，而是确认数据是否真的按预期变化。
