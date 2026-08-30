# Databricks GitHub 学习资源推荐与项目组事前学习结合指南

## 1. 目的

本文档用于配合项目组提供的《Databricks
参画前の事前学習内容》，筛选适合入门和实战的 GitHub 学习项目。

当前学习目标不是深入 Spark 内部原理，而是优先达到：

1.  理解 Databricks 基本概念
2.  能操作 Notebook
3.  能在 Databricks 中使用 SQL 查询和加工数据
4.  理解 Bronze / Silver / Gold
5.  能看懂和编写简单 PySpark DataFrame
6.  理解 Delta Table、MERGE
7.  对 Job / Pipeline 有基本认识

------------------------------------------------------------------------

## 2. 截图中的 GitHub 项目是否官方

截图中的仓库：

`yunnadatabricks/adb-data-engineering-20221025`

不是 Databricks 官方 GitHub 仓库。

从仓库信息来看，它是一个 2022 年 Azure Databricks Data Engineering
Workshop 学习资料，更适合作为旧版培训参考。

### 判断

-   可以参考：是
-   Databricks 官方：不是
-   是否适合作为当前主学习资料：不推荐
-   原因：资料较旧，而且当前有更完整、更适合 Bronze / Silver / Gold
    实战的项目

------------------------------------------------------------------------

## 3. 推荐 GitHub 项目排名

  --------------------------------------------------------------------------------------------------------------------------------
  排名        GitHub 项目                                     官方性         难度        与项目组要求匹配度   推荐用途
  ----------- ----------------------------------------------- -------------- ----------- -------------------- --------------------
  1           DataWithBaraa/databricks_bootcamp_2026          第三方         ★★          ★★★★★                第一阶段主学习项目

  2           databricks-demos/dbdemos                        Databricks     ★★★         ★★★★★                Pipeline / 企业 Demo
                                                              Demo 团队                                       

  3           delta-io/delta-examples                         Delta Lake     ★★★         ★★★★                 Delta / MERGE 专项
                                                              官方生态                                        

  4           databricks/reference-apps                       Databricks     ★★★★        ★★★                  Spark 应用进阶
                                                              官方                                            

  5           yunnadatabricks/adb-data-engineering-20221025   第三方旧资料   ★★          ★★★                  仅作为参考
  --------------------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# 4. 第一推荐：databricks_bootcamp_2026

GitHub：

`DataWithBaraa/databricks_bootcamp_2026`

这是目前最适合当前学习目标的项目之一。

虽然它不是 Databricks 官方仓库，但它的优势是学习路径非常接近项目组要求。

主要涉及：

-   Databricks
-   Spark
-   PySpark
-   Spark SQL
-   Delta Lake
-   Unity Catalog
-   Notebook / Script
-   数据清洗
-   数据标准化
-   Bronze / Silver / Gold
-   Gold 业务模型

项目明确面向没有 Databricks 实务经验的学习者。

## 为什么最适合当前阶段

项目组要求重点掌握：

``` text
Notebook
↓
SQL
↓
Bronze
↓
Silver
↓
Gold
↓
PySpark基础
```

这个 Bootcamp 基本就是围绕这个数据处理流程展开。

因此建议将其作为第一阶段的主实战项目。

------------------------------------------------------------------------

# 5. 第二推荐：databricks-demos/dbdemos

GitHub：

`databricks-demos/dbdemos`

这是 Databricks Demo / Best Practices 相关项目。

它比第一个 Bootcamp 更接近企业实际应用。

内容可能涉及：

-   Data Ingestion
-   Delta Lake
-   Lakehouse
-   Pipeline
-   SQL Dashboard
-   CDC
-   Auto Loader
-   Unity Catalog
-   Machine Learning / AI

典型流程：

``` text
Data Source
↓
Data Ingestion
↓
Delta Lake
↓
Bronze
↓
Silver
↓
Gold
↓
Pipeline
↓
SQL / Dashboard / AI
```

## 为什么不建议第一天直接学习

项目组已经明确：

> 参画前不需要深入 Spark 内部处理和复杂架构。

当前最高优先级仍然是：

``` text
Notebook
SQL
Bronze / Silver / Gold
```

所以 `dbdemos` 更适合完成基础学习后，用于学习：

-   Job
-   Pipeline
-   CDC
-   Auto Loader
-   企业级数据处理流程

------------------------------------------------------------------------

# 6. 第三推荐：delta-io/delta-examples

GitHub：

`delta-io/delta-examples`

这是 Delta Lake 官方生态的示例项目。

特别适合第二阶段补充：

-   Delta Table
-   INSERT
-   UPDATE
-   MERGE
-   PySpark + Delta
-   数据更新
-   数据版本管理相关概念

项目组特别要求掌握：

``` text
INSERT
UPDATE
MERGE
CREATE TABLE
CREATE VIEW
```

因此完成 Bronze / Silver / Gold 基础后，建议专门使用这个项目练习 Delta。

------------------------------------------------------------------------

# 7. MERGE 为什么值得重点学习

数据 Pipeline 中经常出现：

``` text
昨天的数据
+
今天的新数据/更新数据
↓
MERGE
↓
最新 Silver 数据
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
→ 已存在
→ UPDATE

NOT MATCHED
→ 不存在
→ INSERT
```

对于数据基盘项目，这是非常实用的知识。

------------------------------------------------------------------------

# 8. Databricks 官方 reference-apps

GitHub：

`databricks/reference-apps`

这是 Databricks 官方项目。

但是它更偏向：

-   Spark Application
-   大规模数据处理
-   Log Analysis
-   Spark 开发
-   Application Architecture

当前项目组已经明确：

> Spark 内部结构和高级处理暂时优先级较低。

因此：

**官方并不代表当前阶段最适合。**

建议完成 Notebook、SQL、Bronze/Silver/Gold、PySpark 基础后再学习。

------------------------------------------------------------------------

# 9. Databricks Academy

Databricks 有官方 Academy 学习体系。

GitHub 中也存在：

`databricks-academy`

不过现在很多官方培训课程已经转移到 Databricks Academy /
官方培训平台，并不是所有新课程都继续通过 GitHub 发布。

因此当前学习不需要执着于：

> 必须找"官方 GitHub"。

更高效的组合是：

``` text
官方文档
+
Databricks Free Edition
+
容易运行的 GitHub 实战项目
```

------------------------------------------------------------------------

# 10. 项目组学习内容与 GitHub 的对应关系

建议不要把 GitHub 当成另外一套学习体系。

直接将 GitHub 项目映射到项目组要求。

``` text
项目组要求
│
├── ① Databricks基本概念
│       ↓
│   Databricks官方文档
│
├── ② Notebook
│       ↓
│   Databricks Free Edition实际操作
│
├── ③ Databricks SQL
│       ↓
│   Notebook自己编写SQL
│
├── ④ Bronze / Silver / Gold
│       ↓
│   ★ databricks_bootcamp_2026
│
├── ⑤ Spark / PySpark基础
│       ↓
│   ★ databricks_bootcamp_2026
│
├── ⑥ Delta / MERGE
│       ↓
│   ★ delta-examples
│
└── ⑦ Job / Pipeline
        ↓
    ★ databricks-demos/dbdemos
```

------------------------------------------------------------------------

# 11. 推荐学习主线

## 第一阶段：Databricks 基础

使用：

-   Databricks Free Edition
-   Databricks 官方文档

学习：

``` text
Databricks
↓
Workspace
↓
Notebook
↓
Catalog
↓
Schema
↓
Table
↓
SQL
```

目标：

> 可以自己创建 Notebook，并使用 SQL 查询 Table。

------------------------------------------------------------------------

# 12. 第二阶段：第一个完整 GitHub 项目

主项目：

`DataWithBaraa/databricks_bootcamp_2026`

重点学习：

``` text
Source Data
↓
Bronze
↓
数据清洗
↓
Silver
↓
JOIN / GROUP BY
↓
Gold
```

同时掌握：

-   SQL
-   PySpark
-   DataFrame
-   Delta
-   Unity Catalog 基础

这是当前最重要的 GitHub 项目。

------------------------------------------------------------------------

# 13. 第三阶段：Delta / MERGE

使用：

`delta-io/delta-examples`

重点学习：

``` text
Delta Table
↓
INSERT
↓
UPDATE
↓
MERGE
```

目标：

> 能够理解数据基盘中增量数据更新的基本方式。

------------------------------------------------------------------------

# 14. 第四阶段：Job / Pipeline

使用：

`databricks-demos/dbdemos`

学习：

``` text
Bronze Notebook
↓
Silver Notebook
↓
Gold Notebook
↓
Job / Pipeline
↓
自动执行
```

进一步了解：

-   Auto Loader
-   CDC
-   Pipeline
-   企业数据处理流程

------------------------------------------------------------------------

# 15. 最推荐的三个 GitHub

当前不需要同时研究很多仓库。

重点只看三个即可。

## No.1

``` text
DataWithBaraa/databricks_bootcamp_2026
```

用途：

``` text
Bronze
Silver
Gold
SQL
PySpark
Unity Catalog
```

这是第一优先级。

------------------------------------------------------------------------

## No.2

``` text
delta-io/delta-examples
```

用途：

``` text
Delta Table
MERGE
UPDATE
PySpark + Delta
```

这是第二优先级。

------------------------------------------------------------------------

## No.3

``` text
databricks-demos/dbdemos
```

用途：

``` text
Job
Pipeline
CDC
Auto Loader
企业级数据流程
```

这是第三优先级。

------------------------------------------------------------------------

# 16. 不建议当前优先学习的内容

当前不要把大量时间投入：

``` text
Spark RDD
Shuffle
Partition 深度调优
Catalyst Optimizer
Spark内部执行机制
Cluster高级调优
复杂ML
复杂AI
复杂Streaming
```

这些内容可以参画后根据实际项目需要继续学习。

------------------------------------------------------------------------

# 17. 推荐完整学习路线

``` text
Databricks Free Edition
        ↓
Workspace
        ↓
Notebook
        ↓
Catalog / Schema / Table
        ↓
SQL
        ↓
────────────────────
databricks_bootcamp_2026
        ↓
Bronze
        ↓
Silver
        ↓
Gold
        ↓
PySpark
        ↓
────────────────────
delta-examples
        ↓
Delta Table
        ↓
MERGE / UPDATE
        ↓
────────────────────
dbdemos
        ↓
Job
        ↓
Pipeline
        ↓
企业级数据处理
```

------------------------------------------------------------------------

# 18. 与银行 AI Agent 数据基盘项目的对应关系

学习这些内容并不是为了单纯学习 Databricks。

实际项目中的：

``` text
数据源
↓
数据整备
↓
数据加工
↓
数据Pipeline
↓
数据マート
↓
AI Agent
```

可以对应为：

``` text
银行业务数据
↓
Bronze
↓
Silver
↓
Gold
↓
Data Mart
↓
AI Agent
```

因此学习时应该始终围绕：

> 数据是怎么进入 Databricks、怎么加工、怎么形成最终业务可使用的数据。

而不是优先研究 Spark 底层实现。

------------------------------------------------------------------------

# 19. 最终学习目标

完成第一阶段后，应能够理解：

> BronzeのデータをSilverに加工します。

也就是：

``` text
Bronze
↓
清洗
↓
转换
↓
标准化
↓
Silver
```

完成第二阶段后，应能够理解：

> SilverのデータをJOINしてGoldのデータマートを作成します。

即：

``` text
Silver Customer
+
Silver Transaction
↓
JOIN
↓
GROUP BY
↓
Gold Data Mart
```

完成 PySpark 学习后，应能够看懂：

``` python
df = spark.read.table("bronze.customer")

df.filter(df["status"] == "ACTIVE") \
  .select("customer_id", "name")
```

并理解为：

> 从 Bronze customer 读取数据，只筛选 ACTIVE 客户，并取得 customer_id 和
> name。

------------------------------------------------------------------------

# 20. 结论

当前最推荐的学习组合：

``` text
【基础】
Databricks Free Edition
+
官方文档

        ↓

【第一实战】
DataWithBaraa/databricks_bootcamp_2026

        ↓

【Delta专项】
delta-io/delta-examples

        ↓

【Pipeline进阶】
databricks-demos/dbdemos
```

截图中的：

``` text
yunnadatabricks/adb-data-engineering-20221025
```

可以作为参考，但不建议作为当前主学习资料。

参画前最重要的是达到：

**Databricks 能操作 + Notebook 会使用 + SQL 能加工 + Bronze/Silver/Gold
能理解和实际完成 + 简单 PySpark 能看懂和修改。**

达到这个水平后，再继续学习 Job / Pipeline 和 Spark 更深入的内容。
