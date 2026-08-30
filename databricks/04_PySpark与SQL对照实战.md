# 04｜PySpark 与 SQL 对照实战

## 1. 学习策略

已有 SQL 经验时，不要重新从 Python 基础开始绕远路。

采用：

```text
已经会的 SQL
      ↓
找到 PySpark 对应写法
      ↓
运行
      ↓
display()
      ↓
比较结果
```

---

## 2. 核心对应表

| SQL | PySpark |
|---|---|
| FROM / Table | `spark.read.table()` |
| SELECT | `select()` |
| WHERE | `filter()` |
| JOIN | `join()` |
| GROUP BY | `groupBy()` |
| ORDER BY | `orderBy()` |
| COUNT | `count()` / aggregation |
| SUM | `sum()` aggregation |

---

# 3. 读取 Table

SQL：

```sql
SELECT *
FROM workspace.silver.customer;
```

PySpark：

```python
df = spark.read.table("workspace.silver.customer")
display(df)
```

流程：

```text
Catalog Table
     ↓
spark.read.table()
     ↓
DataFrame
     ↓
display()
```

---

# 4. WHERE ↔ filter

SQL：

```sql
SELECT *
FROM workspace.silver.customer
WHERE status = 'ACTIVE';
```

PySpark：

```python
df = spark.read.table("workspace.silver.customer")

active_df = df.filter(
    df["status"] == "ACTIVE"
)

display(active_df)
```

---

# 5. SELECT ↔ select

SQL：

```sql
SELECT customer_id, name
FROM workspace.silver.customer;
```

PySpark：

```python
result_df = df.select(
    "customer_id",
    "name"
)

display(result_df)
```

---

# 6. WHERE + SELECT

SQL：

```sql
SELECT
    customer_id,
    name
FROM workspace.silver.customer
WHERE status = 'ACTIVE';
```

PySpark：

```python
result_df = (
    df
    .filter(df["status"] == "ACTIVE")
    .select("customer_id", "name")
)

display(result_df)
```

看到代码时按顺序读：

```text
df
 ↓
filter
 ↓
select
 ↓
result_df
```

---

# 7. JOIN

SQL：

```sql
SELECT
    c.customer_id,
    c.name,
    t.amount
FROM workspace.silver.customer c
LEFT JOIN workspace.silver.transaction t
    ON c.customer_id = t.customer_id;
```

PySpark：

```python
customer_df = spark.read.table(
    "workspace.silver.customer"
)

transaction_df = spark.read.table(
    "workspace.silver.transaction"
)

joined_df = customer_df.join(
    transaction_df,
    on="customer_id",
    how="left"
)

display(joined_df)
```

示意：

```text
customer_df             transaction_df
     │                        │
     └──────── JOIN ──────────┘
                │
                ▼
            joined_df
```

---

# 8. GROUP BY / SUM / COUNT

PySpark：

```python
from pyspark.sql import functions as F

summary_df = (
    transaction_df
    .groupBy("customer_id")
    .agg(
        F.count("transaction_id").alias("transaction_count"),
        F.sum("amount").alias("total_amount"),
        F.avg("amount").alias("avg_amount")
    )
)

display(summary_df)
```

对应 SQL：

```sql
SELECT
    customer_id,
    COUNT(transaction_id) AS transaction_count,
    SUM(amount) AS total_amount,
    AVG(amount) AS avg_amount
FROM workspace.silver.transaction
GROUP BY customer_id;
```

---

# 9. DataFrame 到底是什么

现阶段可以理解成：

> DataFrame 是 Spark 中带 Schema 的表格型数据对象。

```text
Delta Table
   ↓ read
DataFrame
   ↓ filter/select/join/groupBy
新 DataFrame
   ↓ write
Delta Table
```

它不是 Catalog 中永久存在的 Table。

例如：

```python
df = spark.read.table("workspace.silver.customer")
```

这里：

- `workspace.silver.customer`：Catalog 中的 Table；
- `df`：Notebook 程序运行时使用的 DataFrame。

---

# 10. DataFrame 写回 Delta Table

示例：

```python
(
    summary_df
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.gold.customer_summary_pyspark")
)
```

流程：

```text
DataFrame
   ↓
write
   ↓
format("delta")
   ↓
saveAsTable()
   ↓
Catalog 中的 Delta Table
```

---

# 11. DataFrame 与 Temporary View

```python
summary_df.createOrReplaceTempView("customer_summary_tmp")
```

之后 SQL：

```sql
SELECT *
FROM customer_summary_tmp;
```

关系：

```text
PySpark DataFrame
      ↓
Temporary View
      ↓
SQL
```

这也是前一章 MERGE 中 `customer_update` 的做法。

---

# 12. 学 PySpark 时每段代码只问四件事

```text
Input
→ 从哪里读？

Process
→ filter / select / join / groupBy 做了什么？

Output
→ 得到哪个 DataFrame？

Persist
→ 有没有写成 Table？
```

---

# 13. 本章完成标准

看到：

```python
result_df = (
    spark.read.table("workspace.silver.customer")
    .filter("status = 'ACTIVE'")
    .select("customer_id", "name")
)
```

不用逐行翻译 Python，也能马上理解：

> 从 Silver Customer 读取数据，筛选 ACTIVE 客户，只取得 customer_id 和 name。

达到这个水平即可继续 Workflow。
