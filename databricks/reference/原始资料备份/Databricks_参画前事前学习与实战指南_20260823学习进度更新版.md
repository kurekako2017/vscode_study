# Databricks 参画前事前学习与实战指南

> **学习目标** 本文档以项目组提供的《Databricks
> 参画前の事前学習内容》为基准进行整理。 目标不是在参画前深入掌握 Spark
> 内部架构，而是尽快达到能够参与 Databricks 数据基盘项目开发的基本水平。
>
> 最终应达到：
>
> 1.  理解 Databricks 的基本概念
> 2.  能够操作 Databricks Notebook
> 3.  能够使用 SQL 查询、加工 Databricks 中的数据
> 4.  理解 Bronze / Silver / Gold 数据分层
> 5.  能看懂并编写简单 PySpark DataFrame 代码
> 6.  能够完成 CSV → Bronze → Silver → Gold 的简单数据加工
> 7.  理解 Table / View / Temporary View
> 8.  能够理解 MERGE 等数据更新方式
> 9.  对 Job / Pipeline 有基本认识，并能区分 Notebook 内编排与正式
>     Databricks Jobs/Workflows 编排

------------------------------------------------------------------------

# 1. Databricks 是什么

## 1.1 基本理解

Databricks 是一个面向：

-   Data Engineering
-   Data Analytics
-   AI / Machine Learning
-   数据基盘
-   大规模数据处理

的统一数据平台。

Databricks 本身并不是 Azure 独有的服务，可以运行在：

-   Microsoft Azure
-   AWS
-   Google Cloud

Azure 上提供的 Databricks 服务通常称为：

**Azure Databricks**

------------------------------------------------------------------------

# 2. Databricks 与 Spark 的关系

Databricks 底层大量使用 Apache Spark 进行分布式数据处理。

可以简单理解：

``` text
Databricks
    ↓
提供 Notebook / SQL / Catalog / Job / Pipeline 等开发环境
    ↓
Apache Spark
    ↓
实际进行大规模数据处理
```

而：

``` text
PySpark
```

就是：

``` text
Python + Spark
```

也就是通过 Python API 操作 Spark。

参画前不需要深入：

-   RDD
-   Shuffle
-   Partition 调优
-   Catalyst Optimizer
-   Spark 内部执行机制

现阶段只需要做到：

> 能看懂简单 PySpark，并能够使用 DataFrame 完成基本数据加工。

------------------------------------------------------------------------

# 3. Databricks 基本组成

首先掌握以下几个概念：

``` text
Databricks
│
├── Workspace
│
├── Notebook
│
├── Catalog
│    └── Schema
│         └── Table / View
│
├── SQL Warehouse
│
├── Compute
│
└── Job / Pipeline
```

------------------------------------------------------------------------

# 4. Workspace

Workspace 可以理解为 Databricks 的开发工作区。

开发人员可以在这里管理：

-   Notebook
-   SQL
-   Python
-   PySpark
-   数据处理代码
-   开发文件
-   Job

现阶段重点不是 Workspace 的权限管理，而是熟悉：

``` text
Workspace
    ↓
创建 Notebook
    ↓
执行 SQL / Python
    ↓
查看执行结果
```

------------------------------------------------------------------------

# 5. Catalog / Schema / Table

这是 Databricks 数据管理中非常重要的结构。

基本结构：

``` text
Catalog
    ↓
Schema
    ↓
Table
```

例如：

``` text
bank
│
├── bronze
│    ├── customer
│    └── transaction
│
├── silver
│    ├── customer
│    └── transaction
│
└── gold
     └── customer_summary
```

这里：

``` text
bank
```

是 Catalog。

``` text
bronze
silver
gold
```

是 Schema。

``` text
customer
transaction
customer_summary
```

是 Table。

SQL 中可能看到：

``` sql
SELECT *
FROM bank.silver.customer;
```

含义：

``` text
bank       → Catalog
silver     → Schema
customer   → Table
```

------------------------------------------------------------------------

# 6. Data Lake 与 Lakehouse

## 6.1 Data Lake

Data Lake 用于保存大量：

-   CSV
-   JSON
-   Parquet
-   Log
-   图片
-   半结构化数据
-   原始业务数据

传统 Data Lake 比较强调：

> 大量保存各种形式的数据。

------------------------------------------------------------------------

## 6.2 Data Warehouse

传统 Data Warehouse 更强调：

-   结构化数据
-   SQL
-   BI
-   报表
-   数据分析

------------------------------------------------------------------------

## 6.3 Lakehouse

Databricks 的核心思想之一是：

``` text
Data Lake
+
Data Warehouse
=
Lakehouse
```

即同时具备：

-   大规模数据存储
-   SQL 查询
-   数据加工
-   数据分析
-   AI / ML

能力。

参画前只需要理解这个概念，不需要深入架构。

------------------------------------------------------------------------

# 7. Compute / Cluster / SQL Warehouse

Databricks 中执行程序需要计算资源。

可以简单理解：

``` text
Notebook / SQL
       ↓
Compute
       ↓
Spark 执行数据处理
```

SQL Warehouse 主要用于：

``` text
SQL 查询
BI
数据分析
```

Compute 则可以用于：

``` text
Python
PySpark
Notebook
数据加工
```

现阶段只需要理解：

> Notebook 和 SQL 的执行需要 Databricks 提供计算资源。

不需要深入学习 Cluster 配置和性能调优。

------------------------------------------------------------------------

# 8. Notebook【重点】

Notebook 是参画前必须实际操作的内容。

建议实际建立：

``` text
01_bronze_load
02_silver_transform
03_gold_customer_summary
```

三个 Notebook。

需要掌握：

-   Notebook 创建
-   Notebook 保存
-   Cell 创建
-   Cell 删除
-   Cell 执行
-   SQL 执行
-   Python 执行
-   PySpark 执行
-   Table 查询
-   执行结果查看

------------------------------------------------------------------------

# 9. Notebook 中执行 SQL

例如：

``` sql
SELECT *
FROM bank.bronze.customer;
```

过滤：

``` sql
SELECT *
FROM bank.bronze.customer
WHERE status = 'ACTIVE';
```

聚合：

``` sql
SELECT
    customer_id,
    SUM(amount) AS total_amount
FROM bank.bronze.transaction
GROUP BY customer_id;
```

------------------------------------------------------------------------

# 10. Notebook 中执行 PySpark

例如：

``` python
df = spark.read.table("bank.bronze.customer")

display(df)
```

过滤：

``` python
active_df = df.filter(
    df["status"] == "ACTIVE"
)

display(active_df)
```

字段选择：

``` python
result_df = (
    df
    .filter(df["status"] == "ACTIVE")
    .select(
        "customer_id",
        "name"
    )
)

display(result_df)
```

------------------------------------------------------------------------

# 11. Databricks SQL【重点】

已有 SQL / PL/SQL 经验时，不需要重新学习 SQL 基础。

重点是：

> 熟悉 SQL 在 Databricks 中如何使用。

至少实际执行一次以下内容。

------------------------------------------------------------------------

## 11.1 SELECT

``` sql
SELECT *
FROM bank.bronze.customer;
```

------------------------------------------------------------------------

## 11.2 WHERE

``` sql
SELECT *
FROM bank.bronze.customer
WHERE status = 'ACTIVE';
```

------------------------------------------------------------------------

## 11.3 ORDER BY

``` sql
SELECT *
FROM bank.bronze.transaction
ORDER BY amount DESC;
```

------------------------------------------------------------------------

## 11.4 GROUP BY

``` sql
SELECT
    customer_id,
    SUM(amount) AS total_amount
FROM bank.bronze.transaction
GROUP BY customer_id;
```

------------------------------------------------------------------------

## 11.5 JOIN

``` sql
SELECT
    c.customer_id,
    c.name,
    t.amount
FROM bank.silver.customer c
JOIN bank.silver.transaction t
    ON c.customer_id = t.customer_id;
```

------------------------------------------------------------------------

## 11.6 CASE WHEN

``` sql
SELECT
    customer_id,
    amount,
    CASE
        WHEN amount >= 100000 THEN 'HIGH'
        WHEN amount >= 10000 THEN 'MIDDLE'
        ELSE 'LOW'
    END AS amount_rank
FROM bank.silver.transaction;
```

------------------------------------------------------------------------

## 11.7 CTE

``` sql
WITH customer_total AS (
    SELECT
        customer_id,
        SUM(amount) AS total_amount
    FROM bank.silver.transaction
    GROUP BY customer_id
)

SELECT *
FROM customer_total
WHERE total_amount >= 100000;
```

------------------------------------------------------------------------

## 11.8 CREATE TABLE

``` sql
CREATE TABLE bank.silver.customer (
    customer_id STRING,
    name STRING,
    status STRING,
    age INT
);
```

------------------------------------------------------------------------

## 11.9 CREATE VIEW

``` sql
CREATE VIEW bank.gold.active_customer AS

SELECT *
FROM bank.silver.customer
WHERE status = 'ACTIVE';
```

------------------------------------------------------------------------

# 12. MERGE【重点】

数据基盘项目中经常会出现：

``` text
已有数据
+
当天新增/更新数据
        ↓
      MERGE
        ↓
更新后的最新数据
```

例如：

``` sql
MERGE INTO bank.silver.customer AS target

USING bank.bronze.customer_update AS source

ON target.customer_id = source.customer_id

WHEN MATCHED THEN
UPDATE SET
    target.name = source.name,
    target.status = source.status

WHEN NOT MATCHED THEN
INSERT *
```

需要理解：

``` text
MATCHED
```

表示已有客户。

进行：

``` text
UPDATE
```

而：

``` text
NOT MATCHED
```

表示新客户。

进行：

``` text
INSERT
```

------------------------------------------------------------------------

# 13. Table / View / Temporary View

## Table

真正保存数据。

例如：

``` text
bank.silver.customer
```

------------------------------------------------------------------------

## View

主要保存查询定义。

例如：

``` sql
CREATE VIEW bank.gold.active_customer AS
SELECT *
FROM bank.silver.customer
WHERE status = 'ACTIVE';
```

------------------------------------------------------------------------

## Temporary View

临时使用的 View。

通常用于：

-   Notebook 内临时加工
-   中间数据处理
-   Session 内查询

现阶段只需要理解三者的用途区别。

------------------------------------------------------------------------

# 14. Bronze / Silver / Gold【重点】

这是本次事前学习最重要的内容之一。

基本结构：

``` text
业务系统
   ↓
CSV / DB / API
   ↓
Bronze
   ↓
数据清洗 / 转换
   ↓
Silver
   ↓
JOIN / GROUP BY / 业务加工
   ↓
Gold
   ↓
AI Agent / BI / 报表 / 业务系统
```

------------------------------------------------------------------------

# 15. Bronze

Bronze 保存：

> 原始数据或者接近原始状态的数据。

例如：

``` text
customer.csv
      ↓
bank.bronze.customer
```

数据：

  customer_id   name     status      age
  ------------- -------- -------- ------
  C001          Tanaka   ACTIVE       40
  C002          Sato     NULL         35
  C003          Suzuki   ACTIVE     NULL

Bronze 阶段一般尽量保留原始数据。

------------------------------------------------------------------------

# 16. Silver

Silver 是：

> 对 Bronze 数据进行清洗、转换、标准化后的数据。

典型处理包括：

``` text
NULL处理
重复数据删除
无效数据过滤
数据类型转换
日期格式统一
Code转换
数据标准化
```

例如：

``` sql
CREATE OR REPLACE TABLE bank.silver.customer AS

SELECT
    customer_id,
    name,
    COALESCE(status, 'UNKNOWN') AS status,
    age
FROM bank.bronze.customer
WHERE customer_id IS NOT NULL;
```

现场如果说：

> BronzeからSilverへデータを加工してください。

应该能够立即理解为：

``` text
读取 Bronze
    ↓
清洗
    ↓
转换
    ↓
校验
    ↓
写入 Silver
```

------------------------------------------------------------------------

# 17. Gold

Gold 是：

> 面向具体业务、分析、BI、AI Agent 使用的数据。

例如业务要求：

> 查询每个客户的交易汇总情况。

可以：

``` text
silver.customer
        +
silver.transaction
        ↓
       JOIN
        ↓
     GROUP BY
        ↓
gold.customer_summary
```

SQL：

``` sql
CREATE OR REPLACE TABLE bank.gold.customer_summary AS

SELECT
    c.customer_id,
    c.name,
    COUNT(t.transaction_id) AS transaction_count,
    SUM(t.amount) AS total_amount,
    AVG(t.amount) AS avg_amount
FROM bank.silver.customer c
LEFT JOIN bank.silver.transaction t
    ON c.customer_id = t.customer_id
GROUP BY
    c.customer_id,
    c.name;
```

最终：

  customer_id   name       transaction_count   total_amount   avg_amount
  ------------- -------- ------------------- -------------- ------------
  C001          Tanaka                    25         580000        23200
  C002          Sato                       8         120000        15000

这张：

``` text
gold.customer_summary
```

就可以理解为一个简单的数据マート。

------------------------------------------------------------------------

# 18. 数据マート的理解

数据マート不是单纯复制一张表。

通常是：

``` text
多个业务数据
      ↓
JOIN
      ↓
过滤
      ↓
聚合
      ↓
业务规则加工
      ↓
面向特定用途的数据
```

例如：

``` text
客户数据
+
交易数据
+
账户数据
        ↓
Gold Customer Summary
        ↓
AI Agent
```

------------------------------------------------------------------------

# 19. Spark / PySpark 基础

参画前不需要深入 Spark 内部结构。

只需要理解：

``` text
Spark
    ↓
大规模分布式数据处理框架

PySpark
    ↓
使用 Python 操作 Spark
```

------------------------------------------------------------------------

# 20. DataFrame

DataFrame 可以暂时理解成：

> 有 Schema 的表格型数据集合。

例如：

``` python
df = spark.read.table(
    "bank.bronze.customer"
)
```

这里：

``` text
df
```

就是 DataFrame。

------------------------------------------------------------------------

# 21. SQL 与 PySpark 对照学习

有 SQL 经验时，推荐使用这种方法学习 PySpark。

  SQL        PySpark
  ---------- -----------
  SELECT     select()
  WHERE      filter()
  JOIN       join()
  GROUP BY   groupBy()
  ORDER BY   orderBy()
  SUM        sum()
  COUNT      count()

例如 SQL：

``` sql
SELECT
    customer_id,
    name
FROM bank.bronze.customer
WHERE status = 'ACTIVE';
```

PySpark：

``` python
df = spark.read.table(
    "bank.bronze.customer"
)

result_df = (
    df
    .filter(df["status"] == "ACTIVE")
    .select(
        "customer_id",
        "name"
    )
)

display(result_df)
```

现阶段目标：

> 看到上面的 PySpark，能够立即理解处理内容。

------------------------------------------------------------------------

# 22. 实战项目

## 项目名称

**银行客户交易数据 Bronze → Silver → Gold 数据加工**

------------------------------------------------------------------------

# 23. 项目整体结构

``` text
customer.csv
transaction.csv
       ↓
       ↓
Databricks
       ↓
01_bronze_load Notebook
       ↓
bank.bronze.customer
bank.bronze.transaction
       ↓
02_silver_transform Notebook
       ↓
NULL处理
数据类型转换
数据清洗
状态标准化
       ↓
bank.silver.customer
bank.silver.transaction
       ↓
03_gold_customer_summary Notebook
       ↓
JOIN
GROUP BY
SUM
COUNT
AVG
       ↓
bank.gold.customer_summary
       ↓
AI Agent / BI / 数据分析
```

------------------------------------------------------------------------

# 24. 实战 Step 1：准备 CSV

准备：

``` text
customer.csv
transaction.csv
```

customer.csv：

``` csv
customer_id,name,status,age
C001,Tanaka,ACTIVE,40
C002,Sato,,35
C003,Suzuki,ACTIVE,28
C004,Yamada,INACTIVE,50
```

transaction.csv：

``` csv
transaction_id,customer_id,amount
T001,C001,10000
T002,C001,50000
T003,C002,30000
T004,C003,100000
T005,C003,20000
```

------------------------------------------------------------------------

# 25. 实战 Step 2：创建 Bronze

目标：

``` text
CSV
 ↓
Bronze Table
```

建立：

``` text
bank.bronze.customer
bank.bronze.transaction
```

确认：

``` sql
SELECT *
FROM bank.bronze.customer;
```

``` sql
SELECT *
FROM bank.bronze.transaction;
```

------------------------------------------------------------------------

# 26. 实战 Step 3：Bronze → Silver

对 customer 进行：

``` text
NULL处理
无效ID过滤
status标准化
```

形成：

``` text
bank.silver.customer
```

对 transaction 进行：

``` text
NULL检查
amount类型确认
无效交易过滤
```

形成：

``` text
bank.silver.transaction
```

------------------------------------------------------------------------

# 27. 实战 Step 4：Silver → Gold

使用：

``` text
customer
+
transaction
```

进行：

``` text
JOIN
 ↓
GROUP BY
 ↓
SUM
COUNT
AVG
```

最终建立：

``` text
bank.gold.customer_summary
```

------------------------------------------------------------------------

# 28. 实战 Step 5：使用 PySpark 重做部分加工

不要另外建立复杂 PySpark 项目。

直接把已经会的 SQL 改写成 PySpark。

例如：

``` python
customer_df = spark.read.table(
    "bank.silver.customer"
)

active_df = (
    customer_df
    .filter(customer_df["status"] == "ACTIVE")
    .select(
        "customer_id",
        "name"
    )
)

display(active_df)
```

------------------------------------------------------------------------

# 29. 实战 Step 6：练习 MERGE

模拟：

``` text
customer_update
```

里面同时存在：

-   已有客户更新
-   新客户追加

然后使用：

``` sql
MERGE INTO
```

完成：

``` text
UPDATE
+
INSERT
```

理解 Databricks 数据更新的基本方式。

------------------------------------------------------------------------

# 30. Job / Pipeline / Workflows【2026-08-23 学习进度更新】

原计划这里只要求"理解 Job / Pipeline 的基本概念"。\
根据 2026-08-23 的实际练习，当前已经比原计划多完成了一步：**Notebook
内的顺序编排（Orchestration）已经实际跑通**。

今天建立并成功执行：

``` text
gold_orchestration
       ↓
gold_dim_customers
       ↓
gold_dim_products
       ↓
gold_fact_sales
```

核心代码采用：

``` python
notebooks = [
    "./gold_dim_customers",
    "./gold_dim_products",
    "./gold_fact_sales"
]

for nb in notebooks:
    print(f"Running {nb}")
    dbutils.notebook.run(nb, timeout_seconds=0)
```

执行结果中 3 个子 Notebook 均成功，因此已经理解：

``` text
多个独立 Gold Notebook
        ↓
统一入口 Notebook
        ↓
按照指定顺序执行
        ↓
任何一步失败都可以定位到具体 Notebook
```

## 30.1 今天已经掌握的编排方式

当前完成的是：

> **Notebook Orchestration / Notebook chaining**

即由一个 Notebook 使用 `dbutils.notebook.run()` 调用其他 Notebook。

它非常适合帮助理解：

-   Notebook 之间的依赖关系
-   执行顺序
-   单一入口（single entry point）
-   Gold 层批处理的整体数据流

因此，原计划中的：

> "理解为什么需要 Job / Pipeline，以及它解决什么问题"

已经达成，而且已经从"只理解概念"提升到"实际执行过简单编排"。

## 30.2 但这还不等于正式 Databricks Jobs/Workflows

需要明确区分：

``` text
【今天已完成】

gold_orchestration Notebook
        ↓
dbutils.notebook.run()
        ↓
依次调用多个 Notebook
```

与：

``` text
【后续正式练习】

Databricks Jobs / Workflows
        ↓
Task A: Bronze
        ↓
Task B: Silver
        ↓
Task C/D/E: Gold
        ↓
Schedule / Retry / Failure handling / Run history
```

真实项目中，更正规的生产编排通常会把各处理单元配置成 Workflow Task，并在
Workflow 层定义依赖关系，而不是把所有依赖关系全部硬编码在一个 Notebook
中。

## 30.3 参画前需要掌握到什么程度

建议达到以下程度即可：

-   能创建一个 Job / Workflow
-   能添加 Notebook Task
-   能设置 Task dependency
-   能理解串行与并行
-   能手动触发 Run
-   能查看 Run history
-   能定位失败 Task
-   知道 Retry / Schedule 的作用

暂时不需要深入：

-   复杂动态 DAG
-   大规模生产调度设计
-   高级告警体系
-   CI/CD 自动部署 Workflows
-   Terraform / Asset Bundles 深度配置

这部分安排在 Delta / MERGE 之后练习。

------------------------------------------------------------------------

# 31. 推荐学习顺序

## 第一优先级

``` text
1. Databricks 基本概念
        ↓
2. Free Edition 环境
        ↓
3. Workspace
        ↓
4. Notebook
        ↓
5. Catalog / Schema / Table
        ↓
6. Databricks SQL
        ↓
7. Bronze / Silver / Gold
```

------------------------------------------------------------------------

## 第二优先级

``` text
8. Delta Table
        ↓
9. Table / View / Temporary View
        ↓
10. MERGE
        ↓
11. PySpark
        ↓
12. DataFrame
```

------------------------------------------------------------------------

## 第三优先级

``` text
13. Job
14. Pipeline
15. Unity Catalog 权限管理
```

------------------------------------------------------------------------

## 现阶段低优先级

``` text
RDD
Shuffle
Partition 深入调优
Catalyst Optimizer
Spark 内部执行计划
Cluster 高级配置
高级性能调优
```

------------------------------------------------------------------------

# 32. 建议学习时间

  内容                          时间 达成目标
  -------------------------- ------- --------------------
  Databricks 基本概念             1h 理解整体结构
  Free Edition / Workspace        1h 熟悉环境
  Notebook                        1h 可以自己创建和执行
  Catalog / Schema / Table        1h 能找到和查询数据
  Databricks SQL                  2h 常用 SQL 实际执行
  Bronze / Silver / Gold          3h **重点掌握**
  Delta / MERGE / View            2h 理解数据管理方式
  PySpark / DataFrame             3h 能看懂并写简单代码
  完整实战                     3～4h CSV → Gold
  Job / Pipeline               1～2h 理解自动执行

预计：

**15～18 小时左右。**

------------------------------------------------------------------------

# 33. 建议三天学习安排

## Day 1：Databricks + SQL

完成：

-   Databricks 基本概念
-   Free Edition
-   Workspace
-   Notebook
-   Catalog
-   Schema
-   Table
-   SQL Warehouse / Compute 基本概念
-   SELECT
-   WHERE
-   GROUP BY
-   ORDER BY
-   JOIN
-   CASE WHEN
-   CTE

目标：

> 能够进入 Databricks，自己创建 Notebook，并使用 SQL 查询数据。

------------------------------------------------------------------------

## Day 2：Bronze / Silver / Gold 实战【2026-08-23 已完成主干】

完成：

``` text
CSV
 ↓
Bronze
 ↓
数据清洗
 ↓
Silver
 ↓
JOIN
 ↓
GROUP BY
 ↓
Gold
```

同时学习：

-   Delta Table
-   Table
-   View
-   Temporary View
-   INSERT
-   UPDATE
-   MERGE

目标：

> 能够理解并实际完成 Bronze → Silver → Gold。

------------------------------------------------------------------------

## Day 3：Delta / MERGE + PySpark + 正式 Workflows【下一阶段】

完成：

-   Spark 基本概念
-   PySpark
-   DataFrame
-   read.table()
-   filter()
-   select()
-   join()
-   groupBy()
-   数据写入
-   SQL 与 PySpark 对照
-   Notebook Orchestration（已完成）
-   Databricks Jobs / Workflows 正式 Task 编排（下一阶段）

最后重新独立执行：

``` text
customer.csv
transaction.csv
       ↓
Bronze
       ↓
Silver
       ↓
Gold Customer Summary
```

目标：

> SQL 能自己写，简单 PySpark 能看懂、能修改、能写基本数据加工。

------------------------------------------------------------------------

# 34. 参画前自我检查 Checklist

## Databricks

-   [ ] 我知道 Databricks 是什么
-   [ ] 我知道 Databricks 与 Spark 的关系
-   [ ] 我理解 Lakehouse 的基本概念
-   [ ] 我知道 Workspace 是什么
-   [ ] 我知道 Compute / SQL Warehouse 大致作用

## Notebook

-   [ ] 我能创建 Notebook
-   [ ] 我能创建和执行 Cell
-   [ ] 我能运行 SQL
-   [ ] 我能运行 Python / PySpark
-   [ ] 我能查看执行结果
-   [ ] 我能从 Notebook 查询 Table

## 数据管理

-   [ ] 我理解 Catalog
-   [ ] 我理解 Schema
-   [ ] 我理解 Table
-   [ ] 我理解 View
-   [ ] 我知道 Temporary View 与普通 View 的基本区别

## SQL

-   [ ] SELECT
-   [ ] WHERE
-   [ ] ORDER BY
-   [ ] GROUP BY
-   [ ] JOIN
-   [ ] CASE WHEN
-   [ ] Subquery
-   [ ] CTE
-   [ ] INSERT
-   [ ] UPDATE
-   [ ] MERGE
-   [ ] CREATE TABLE
-   [ ] CREATE VIEW

## Bronze / Silver / Gold

-   [ ] 我能解释 Bronze
-   [ ] 我能解释 Silver
-   [ ] 我能解释 Gold
-   [ ] 我理解 Bronze → Silver 做什么
-   [ ] 我理解 Silver → Gold 做什么
-   [ ] 我理解 Gold 与数据マート的关系

## PySpark

-   [ ] 我知道 Spark 是什么
-   [ ] 我知道 PySpark 是什么
-   [ ] 我知道 DataFrame 是什么
-   [ ] 我能看懂 spark.read.table()
-   [ ] 我能看懂 filter()
-   [ ] 我能看懂 select()
-   [ ] 我知道 join()
-   [ ] 我知道 groupBy()

## Orchestration / Jobs / Workflows

-   [x] 我理解为什么多个 Notebook 需要编排
-   [x] 我能使用 `dbutils.notebook.run()` 顺序调用多个 Notebook
-   [x] 我已经成功运行 `gold_orchestration`
-   [ ] 我能创建 Databricks Job / Workflow
-   [ ] 我能添加多个 Notebook Task
-   [ ] 我能设置 Task dependency
-   [ ] 我能查看 Run history 和失败 Task
-   [ ] 我理解 Schedule / Retry 的基本作用

------------------------------------------------------------------------

# 33.1 2026-08-23 实际学习成果与达成判定

根据今天在 Databricks Free Edition 中完成的实际操作，当前进度如下。

  ---------------------------------------------------------------------------------------------
  学习项目          原计划目标             当前状态                           判定
  ----------------- ---------------------- ---------------------------------- -----------------
  Workspace /       会创建、运行 Notebook  已实际操作                         ✅ 达成
  Notebook                                                                    

  Catalog / Schema  能理解并查看数据结构   已在 Catalog Explorer 中确认       ✅ 达成
  / Table                                                                     

  Bronze            理解原始层             已建立并确认多张 Bronze 表         ✅ 达成

  Silver            能完成清洗、转换       已对 ERP / CRM 数据执行 Silver     ✅ 达成
                                           加工                               

  清洗前后确认      能验证加工结果         已使用 `display()` / SQL / Catalog ✅ 达成
                                           进行确认                           

  Gold Dimension    能从 Silver            已建立                             ✅ 达成
                    建立业务维表           `dim_customers`、`dim_products`    

  Gold Fact         能建立事实表           已建立 `fact_sales`                ✅ 达成

  Gold Data Mart    理解 Dimension / Fact  已通过 Gold 模型实际练习           ✅ 达成
  思维              的业务用途                                                

  Delta Table 写入  能将 DataFrame 保存为  已使用                             ✅ 达成
                    Delta Table            `.format("delta").saveAsTable()`   

  Notebook          理解多个 Notebook      `gold_orchestration` 已成功调用 3  ✅ 超前完成
  Orchestration     的执行顺序             个 Gold Notebook                   

  MERGE / UPDATE /  理解增量更新           尚需专项练习                       ⏳ 下一步
  INSERT                                                                      

  Table / View /    理解区别并实际操作     仍需补齐实际练习                   ⏳ 待补
  Temporary View                                                              

  正式 Jobs /       能用 Task DAG 正规编排 尚未正式练习                       ⏳ MERGE 后进行
  Workflows                                                                   

  PySpark 独立编写  能独立完成简单加工     已能阅读和修改，仍需继续巩固       🟡 基本达成
  ---------------------------------------------------------------------------------------------

## 今日结论

**今天的核心目标已经达成。**

尤其是原始项目组要求中的重点：

``` text
Databricks 基本操作
+
Notebook
+
SQL
+
Bronze → Silver → Gold
+
简单 PySpark / DataFrame
```

已经不只是"看懂"，而是通过 `databricks_bootcamp_2026`
数据实际完成了数据层构建。

原始项目组要求的最终重点，本来只是做到：

> 能在 Databricks 中使用 SQL 确认和加工数据、能操作 Notebook、理解
> Bronze / Silver / Gold。

因此，以"参画前最低要求"判断，**当前已经基本达到要求**。

但为了进入项目后更稳，学习不在这里结束。接下来补齐三个高价值项目：

``` text
① Delta INSERT / UPDATE / MERGE
        ↓
② Table / View / Temporary View
        ↓
③ Databricks Jobs / Workflows 正式编排
```

完成这三项后，可以把状态从：

> **参画前基本达标**

提升到：

> **具备较完整的数据加工 + 增量更新 + 批处理编排入场准备**

------------------------------------------------------------------------

# 35. 参画前最终目标

不要求达到：

> Databricks 专家 / Spark 专家

而是达到以下状态。

### 现场说：

> BronzeのcustomerデータをSilverに加工してください。

能够理解：

``` text
Bronze读取
 ↓
数据清洗
 ↓
NULL处理
 ↓
格式/类型转换
 ↓
业务规则处理
 ↓
Silver写入
```

### 现场说：

> SilverのcustomerとtransactionをJOINして、Goldのデータマートを作成します。

能够理解：

``` text
Silver Customer
       +
Silver Transaction
       ↓
      JOIN
       ↓
业务规则
       ↓
GROUP BY / SUM / COUNT
       ↓
Gold Data Mart
```

### 看到：

``` python
df = spark.read.table("bank.bronze.customer")

result_df = (
    df
    .filter(df["status"] == "ACTIVE")
    .select(
        "customer_id",
        "name"
    )
)
```

能够立即理解：

> 从 Bronze customer 读取数据，筛选 ACTIVE 客户，只取得 customer_id 和
> name。

------------------------------------------------------------------------

# 36. 学习完成标准

最终至少独立完成一次：

``` text
CSV
 ↓
Databricks Free Edition
 ↓
Workspace
 ↓
Notebook
 ↓
Catalog / Schema / Table
 ↓
Bronze Table
 ↓
SQL 数据确认
 ↓
Silver 数据清洗
 ↓
JOIN / CASE WHEN
 ↓
Gold 数据マート
 ↓
Table / View
 ↓
MERGE
 ↓
PySpark DataFrame
 ↓
Notebook Orchestration
 ↓
Databricks Jobs / Workflows 基本 Task 编排
```

其中截至 **2026-08-23**，Bronze → Silver → Gold 与 Notebook
Orchestration 主干已经完成； 剩余重点为 **MERGE、View、正式
Jobs/Workflows**。

完成以上剩余内容后，即可认为不仅达到本次项目组提出的 **Databricks
参画前事前学习目标**， 而且具备更接近实际项目入场的数据处理基础。

------------------------------------------------------------------------

# 37. 学习原则

本次事前学习遵循：

**先会操作 → 再理解数据流 → 再补 PySpark → 最后学习内部原理。**

不要采用：

``` text
Spark原理
↓
RDD
↓
Shuffle
↓
Partition
↓
Catalyst
↓
最后才操作Databricks
```

而采用：

``` text
Databricks实际操作
↓
Notebook
↓
SQL
↓
Bronze / Silver / Gold
↓
Delta
↓
MERGE
↓
PySpark
↓
Job / Pipeline
↓
实际项目中再逐步补Spark原理
```

对于参画前准备，这是效率更高、也更符合项目组要求的学习路线。

------------------------------------------------------------------------

# 38. 2026-08-23 教程修订记录

本次根据当天实际操作结果修订：

1.  将 Bronze → Silver → Gold 主干标记为已完成。
2.  追加 Gold Dimension / Fact 实战成果。
3.  追加 `gold_orchestration` Notebook 编排成果。
4.  明确 `dbutils.notebook.run()` 与正式 Databricks Jobs/Workflows
    的区别。
5.  将后续学习重点收敛为：
    -   Delta INSERT / UPDATE / MERGE
    -   Table / View / Temporary View
    -   Databricks Jobs / Workflows 正式编排
6.  将当前总体状态定义为：
    -   **项目组参画前核心要求：基本达成**
    -   **强化入场准备：继续完成上述 3 项**
