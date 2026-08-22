# Databricks Free Edition：利用 GitHub 示例快速上手实战操作指南

> **适用环境**：Databricks Free Edition（2026）\
> **目标**：不从零手敲一个大项目，而是先把 GitHub 中现成的 Databricks
> 示例导入 Workspace，运行起来、看到结果，再反过来理解
> Notebook、SQL、PySpark、Bronze / Silver / Gold。\
> **当前推荐主项目**：`DataWithBaraa/databricks_bootcamp_2026`

------------------------------------------------------------------------

# 1. 先明确：GitHub 示例和 Databricks 是什么关系

最容易产生的误解是：

``` text
GitHub 示例
↓
下载到电脑
↓
在本地运行 Databricks
```

对于现在的学习阶段，不建议这么做。

更简单的方式是：

``` text
GitHub Repository
        ↓
Databricks Git folder
        ↓
代码直接出现在 Databricks Workspace
        ↓
打开 Notebook / .py / .sql
        ↓
使用 Databricks Serverless Compute 执行
        ↓
查看 Table / DataFrame / SQL 结果
```

也就是说：

-   GitHub：保存别人已经写好的学习代码和数据文件
-   Databricks：真正执行这些 Notebook、SQL、PySpark 的环境
-   Git folder：把 GitHub Repository 直接连接/克隆到 Databricks
    Workspace

Databricks 现在把旧教程里的 **Repos** 政名为 **Git
folders**。看到旧视频说 `Repos`，不要困惑，它基本就是现在的 Git folder。

------------------------------------------------------------------------

# 2. 你现在截图所在的位置是正确的

当前已经进入：

``` text
Databricks Free Edition
→ 工作区（Workspace）
→ Users
→ 自己的用户目录
```

截图中已经有：

``` text
Drafts
_assistant
Bakehouse Sales Starter Space
notebook_20260822
```

说明 Free Edition Workspace 已经可以正常使用。

下一步不需要安装：

-   Java
-   Spark
-   Hadoop
-   Python 本地环境
-   Docker
-   Azure VM

Free Edition 使用 Serverless Compute，可以直接在 Databricks
中运行学习代码。

------------------------------------------------------------------------

# 3. 最推荐的快速学习方法

不要先花几天阅读 README。

采用：

> **导入 → 运行 → 看结果 → 修改 → 再理解**

学习循环：

``` text
GitHub 找到示例
       ↓
导入 Databricks
       ↓
找到最简单 Notebook
       ↓
Run
       ↓
看到结果
       ↓
理解代码
       ↓
修改一个条件
       ↓
再次 Run
       ↓
观察结果变化
```

这是当前最快的学习方法。

------------------------------------------------------------------------

# 4. 第一种导入方式：Git folder【最推荐】

这是以后实际开发也会用到的方式。

在当前 Databricks 页面：

``` text
左侧
工作区
```

进入自己的目录。

然后：

``` text
新建
↓
Git folder
```

中文界面中可能显示：

``` text
Git 文件夹
```

如果看不到，可以从 Workspace 内某个目录的：

``` text
新建 / Create
```

菜单中寻找。

------------------------------------------------------------------------

# 5. 从 GitHub Clone 项目

以推荐项目为例：

``` text
https://github.com/DataWithBaraa/databricks_bootcamp_2026
```

在 Git folder 创建画面填写：

``` text
Git repository URL:
https://github.com/DataWithBaraa/databricks_bootcamp_2026
```

Git Provider：

``` text
GitHub
```

Repository name 通常会自动成为：

``` text
databricks_bootcamp_2026
```

点击：

``` text
Create Git folder
```

或者中文界面的：

``` text
创建 Git 文件夹
```

完成后 Workspace 中会出现类似：

``` text
Workspace
└── Users
    └── <你的用户>
        └── databricks_bootcamp_2026
```

------------------------------------------------------------------------

# 6. Public GitHub 与 GitHub 登录

如果是公开 Repository，通常可以直接 Clone。

如果 Databricks 要求 GitHub 授权，按照画面连接 GitHub 即可。

对于：

-   Private Repository
-   Push
-   Commit
-   Pull
-   自己的公司 GitHub

则需要正式配置 Git credentials / GitHub App。

**学习公开 Demo 时，不要一开始研究 PAT、CI/CD、Branch Strategy。**

当前目标只是：

> 把示例跑起来。

------------------------------------------------------------------------

# 7. Clone 完以后不要马上全部 Run

这是非常重要的一点。

很多 GitHub 教程项目包含：

``` text
README
Setup
Dataset
Bronze
Silver
Gold
Pipeline
Dashboard
Unity Catalog
```

不要点击：

``` text
Run All
```

原因是别人项目可能依赖：

-   特定 Catalog
-   特定 Schema
-   特定 Volume
-   特定数据文件路径
-   其他 Notebook
-   非 Free Edition 功能
-   已经创建好的 Table

所以正确方法是：

``` text
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

------------------------------------------------------------------------

# 8. Clone 后第一件事：看目录，不是看代码

先搞清楚 Repository 有什么。

例如可能看到：

``` text
databricks_bootcamp_2026/
│
├── README.md
├── datasets/
├── bronze/
├── silver/
├── gold/
├── notebooks/
└── scripts/
```

看到这些名字时，先建立整体概念：

``` text
datasets
   ↓
原始数据

bronze
   ↓
数据导入

silver
   ↓
清洗、转换

gold
   ↓
业务聚合 / Data Mart
```

这一步比马上研究每一行代码更重要。

------------------------------------------------------------------------

# 9. 第二件事：打开 README

README 不需要逐字翻译。

只寻找以下信息：

``` text
Prerequisites
Setup
Getting Started
Dataset
Run
Notebook
Catalog
Schema
```

重点回答四个问题：

1.  数据在哪里？
2.  第一个执行文件是什么？
3.  是否需要先创建 Catalog / Schema？
4.  Notebook 的执行顺序是什么？

------------------------------------------------------------------------

# 10. 第三个动作：找到 Setup

如果 Repository 有：

``` text
setup
setup.py
setup.sql
00_setup
01_setup
```

通常先看这个。

例如可能存在：

``` sql
CREATE CATALOG ...
CREATE SCHEMA ...
```

或者：

``` python
spark.sql(...)
```

先理解它准备了什么环境，再执行。

------------------------------------------------------------------------

# 11. 不要因为示例名字不同而困惑

GitHub 示例可能不是：

``` text
bank.bronze.customer
```

可能是：

``` text
workspace.bronze.customers
sales.bronze.orders
demo.silver.products
```

名字完全不重要。

你只要把它映射成：

``` text
Catalog
   ↓
Schema
   ↓
Table
```

例如：

``` text
sales.gold.customer_summary
```

就是：

``` text
sales
→ Catalog

gold
→ Schema

customer_summary
→ Table
```

------------------------------------------------------------------------

# 12. Notebook 怎么运行

打开一个 Notebook 后，不要马上 Run All。

第一遍采用：

``` text
Cell 1
↓
Run
↓
看结果

Cell 2
↓
Run
↓
看结果

Cell 3
↓
Run
↓
看结果
```

每个 Cell 都问自己：

> 输入是什么？处理了什么？输出是什么？

例如：

``` python
df = spark.read.table("bronze.customer")
```

理解为：

``` text
输入：
bronze.customer

处理：
读取 Table

输出：
DataFrame df
```

------------------------------------------------------------------------

# 13. SQL Cell 怎么看

例如：

``` sql
SELECT *
FROM bronze.customer
WHERE status = 'ACTIVE';
```

不要学习 SQL 本身。

重点观察：

``` text
Databricks Notebook
       ↓
执行 SQL
       ↓
读取 Delta Table
       ↓
结果直接显示在 Cell 下方
```

SQL 已经熟悉时，真正需要学习的是：

> Databricks 怎么组织、执行和保存这些数据。

------------------------------------------------------------------------

# 14. PySpark Cell 怎么学最快

例如：

``` python
df = spark.read.table("bronze.customer")

result = (
    df
    .filter(df["status"] == "ACTIVE")
    .select("customer_id", "name")
)

display(result)
```

不要先学 Spark 原理。

直接与 SQL 对照：

``` sql
SELECT
    customer_id,
    name
FROM bronze.customer
WHERE status = 'ACTIVE';
```

对应关系：

  SQL            PySpark
  -------------- --------------------
  FROM / Table   spark.read.table()
  WHERE          filter()
  SELECT         select()
  JOIN           join()
  GROUP BY       groupBy()
  ORDER BY       orderBy()

这就是最快的 PySpark 入门方式。

------------------------------------------------------------------------

# 15. 一定要使用 display()

学习时看到：

``` python
display(df)
```

非常重要。

它可以直接把 DataFrame 显示出来。

学习过程：

``` python
df = spark.read.table("bronze.customer")
display(df)
```

先看到数据。

然后：

``` python
active_df = df.filter(df["status"] == "ACTIVE")
display(active_df)
```

再看数据少了哪些。

这种：

``` text
代码
↓
立即看到数据变化
```

比单纯阅读 PySpark 教程快很多。

------------------------------------------------------------------------

# 16. 学 JOIN 也采用"运行后看结果"

例如：

``` python
customer_df = spark.read.table("silver.customer")
transaction_df = spark.read.table("silver.transaction")

result_df = customer_df.join(
    transaction_df,
    "customer_id",
    "left"
)

display(result_df)
```

不要只背：

``` text
join()
```

而要观察：

``` text
Customer
+
Transaction
↓
JOIN
↓
结果列增加
↓
同一个客户可能出现多行交易
```

这才是真正理解数据加工。

------------------------------------------------------------------------

# 17. Bronze / Silver / Gold 要这样看 GitHub 示例

看到 Bronze Notebook 时问：

``` text
数据从哪里来？
↓
CSV？
JSON？
Table？
Volume？

最后写到哪里？
↓
Bronze Table？
```

看到 Silver Notebook 时问：

``` text
从哪个 Bronze Table 读取？
↓
做了哪些：
NULL
Filter
Cast
Deduplicate
Rename
Join
↓
写到哪个 Silver Table？
```

看到 Gold Notebook 时问：

``` text
读取哪些 Silver Table？
↓
JOIN 什么？
↓
GROUP BY 什么？
↓
SUM / COUNT 什么？
↓
最终建立什么 Gold Table？
```

------------------------------------------------------------------------

# 18. 最重要的学习视角

不要：

``` text
Notebook 1
→ 记代码

Notebook 2
→ 记代码

Notebook 3
→ 记代码
```

而应该始终画：

``` text
Source
↓
Bronze
↓
Silver
↓
Gold
↓
业务用途
```

每打开一个 Notebook，就问：

> 它在这条数据链路的哪一步？

------------------------------------------------------------------------

# 19. 如何快速看出效果

Databricks 学习时主要通过四种方式确认效果。

## 方法 1：display()

``` python
display(df)
```

最适合 PySpark。

## 方法 2：SELECT

``` sql
SELECT *
FROM catalog.schema.table
LIMIT 100;
```

最适合确认 Table。

## 方法 3：Catalog Explorer

左侧：

``` text
目录
```

或者 Catalog 页面中查看：

``` text
Catalog
↓
Schema
↓
Table
```

可以查看：

-   Table 名称
-   Columns
-   Schema
-   Sample Data
-   Metadata

## 方法 4：COUNT

``` sql
SELECT COUNT(*)
FROM silver.customer;
```

加工前后比较：

``` text
Bronze 1000 rows
↓
清洗
↓
Silver 970 rows
```

然后思考：

> 为什么少了 30 条？

这就是数据工程实际工作中的思维。

------------------------------------------------------------------------

# 20. 第一次运行 GitHub Demo 的正确目标

第一次不要追求：

> 全部理解。

只追求：

``` text
Clone成功
↓
Notebook打开
↓
Cell运行成功
↓
Table创建成功
↓
SELECT看到数据
↓
PySpark display看到数据
```

达到这里，第一次学习已经成功。

------------------------------------------------------------------------

# 21. 第二遍才开始修改代码

第一次：

``` python
df.filter(df["status"] == "ACTIVE")
```

第二遍修改成：

``` python
df.filter(df["status"] == "INACTIVE")
```

观察结果。

然后修改：

``` python
.select("customer_id", "name")
```

变成：

``` python
.select(
    "customer_id",
    "name",
    "status"
)
```

再次观察。

------------------------------------------------------------------------

# 22. 第三遍开始自己写

原示例：

``` python
df.filter(df["status"] == "ACTIVE")
```

自己尝试：

``` python
df.filter(df["age"] >= 30)
```

再尝试 SQL：

``` sql
SELECT *
FROM silver.customer
WHERE age >= 30;
```

这样完成：

``` text
模仿
↓
修改
↓
自己写
```

------------------------------------------------------------------------

# 23. 第二种方式：直接 Import Notebook

如果 GitHub Repository 很复杂，不想整个 Clone，可以只下载一个：

``` text
.py
.sql
.ipynb
.dbc
```

然后在 Databricks：

``` text
Workspace
↓
选择自己的文件夹
↓
右键 / ...
↓
Import
```

Databricks 支持导入：

-   `.py`
-   `.sql`
-   `.scala`
-   `.r`
-   `.ipynb`
-   `.dbc`
-   Databricks 导出的 ZIP

适合：

> 我只想快速运行一个 Notebook 看效果。

------------------------------------------------------------------------

# 24. DBC 文件是什么

你之前截图中的旧 Workshop 有：

``` text
ADB-bootcamp-20201025-to-be-shared.dbc
```

`.dbc` 是 Databricks Notebook Archive。

它通常包含一个或多个 Databricks Notebook。

可以：

``` text
下载 .dbc
↓
Databricks Workspace
↓
Import
↓
选择 .dbc
↓
导入
```

然后 Notebook 会出现在 Workspace。

所以旧教程经常让你：

``` text
Download DBC
↓
Import Databricks
```

这是正常的。

------------------------------------------------------------------------

# 25. 2026 年更推荐 Git folder

如果 GitHub Repository 本身就是完整项目：

**优先：**

``` text
Git folder
```

而不是：

``` text
下载 ZIP
↓
手工上传
```

原因：

``` text
GitHub
↕
Databricks Git folder
```

以后可以继续：

-   Pull
-   查看更新
-   Branch
-   Commit
-   Push

也更接近真实项目开发方式。

------------------------------------------------------------------------

# 26. GitHub 示例无法运行时，先检查这 6 项

## ① Catalog 不存在

例如：

``` text
CATALOG_NOT_FOUND
```

检查代码是否假定存在：

``` text
main.demo.xxx
```

------------------------------------------------------------------------

## ② Schema 不存在

例如：

``` text
SCHEMA_NOT_FOUND
```

先确认是否漏执行 Setup。

------------------------------------------------------------------------

## ③ Table 不存在

例如：

``` text
TABLE_OR_VIEW_NOT_FOUND
```

检查：

``` text
Bronze Notebook 是否先运行？
```

------------------------------------------------------------------------

## ④ 文件路径不存在

例如代码读取：

``` python
"/Volumes/demo/data/customer.csv"
```

但 Demo 数据还没有上传。

检查 README / datasets / Setup。

------------------------------------------------------------------------

## ⑤ Notebook 执行顺序错误

例如直接运行：

``` text
03_gold
```

但：

``` text
01_bronze
02_silver
```

还没执行。

------------------------------------------------------------------------

## ⑥ Free Edition 不支持某项功能

Free Edition 有功能和资源限制。

如果一个企业 Demo 使用 Free Edition 没有的功能：

> 不要为了一个 Demo 去折腾环境。

先跳过该功能，继续学习 Notebook / SQL / PySpark / Delta /
Bronze-Silver-Gold。

------------------------------------------------------------------------

# 27. 推荐第一个 GitHub 学习项目

第一阶段：

``` text
DataWithBaraa/databricks_bootcamp_2026
```

GitHub：

`https://github.com/DataWithBaraa/databricks_bootcamp_2026`

学习目的不是全部完成。

第一轮只寻找：

``` text
Setup
↓
Data
↓
Bronze
↓
Silver
↓
Gold
```

------------------------------------------------------------------------

# 28. 第一个项目建议学习顺序

``` text
Step 1
Clone GitHub 到 Git folder
        ↓
Step 2
打开 README
        ↓
Step 3
确认目录
        ↓
Step 4
找到 Setup
        ↓
Step 5
运行最基础 Notebook
        ↓
Step 6
查看 Bronze 数据
        ↓
Step 7
运行 Silver
        ↓
Step 8
比较 Bronze / Silver
        ↓
Step 9
运行 Gold
        ↓
Step 10
查看 Gold Table
        ↓
Step 11
找 PySpark 代码
        ↓
Step 12
修改 filter / select
        ↓
Step 13
重新执行
```

------------------------------------------------------------------------

# 29. 第一轮只学习这些代码

PySpark：

``` python
spark.read.table()
display()
filter()
select()
join()
groupBy()
```

SQL：

``` sql
SELECT
WHERE
JOIN
GROUP BY
CASE WHEN
CREATE TABLE
CREATE VIEW
MERGE
```

数据结构：

``` text
Catalog
Schema
Table
View
DataFrame
```

数据层：

``` text
Bronze
Silver
Gold
```

先不要扩大范围。

------------------------------------------------------------------------

# 30. 推荐的"1 小时快速上手法"

## 0～10 分钟

``` text
GitHub
↓
Git folder Clone
```

目标：

> Repository 出现在 Workspace。

## 10～20 分钟

``` text
README
↓
目录
↓
Setup
```

目标：

> 知道执行顺序。

## 20～35 分钟

运行第一个 Notebook：

``` text
Cell 1 Run
↓
Cell 2 Run
↓
Cell 3 Run
```

目标：

> 第一次看到 Databricks 执行结果。

## 35～45 分钟

找到：

``` python
display(df)
```

或者：

``` sql
SELECT *
```

目标：

> 真正看到数据。

## 45～60 分钟

修改：

``` text
WHERE条件
filter条件
select字段
```

再次运行。

目标：

> 第一次主动改变执行结果。

------------------------------------------------------------------------

# 31. 推荐的 3 小时实战路线

## 第 1 小时：运行

``` text
Clone
↓
Setup
↓
Notebook
↓
Run
↓
看到结果
```

## 第 2 小时：理解

``` text
Source
↓
Bronze
↓
Silver
↓
Gold
```

自己画出数据流。

## 第 3 小时：修改

修改：

``` text
WHERE
filter
select
JOIN
GROUP BY
```

然后重新运行。

------------------------------------------------------------------------

# 32. 与项目组事前学习要求的对应关系

  项目组要求        GitHub 实战怎么学
  ----------------- ----------------------------------
  Databricks 概念   Clone 后认识 Workspace / Compute
  Notebook          直接运行 GitHub Notebook
  SQL               修改 Demo SQL
  Table             Catalog Explorer 查看
  View              Demo 中创建并 SELECT
  Bronze            看原始数据如何进入
  Silver            看清洗代码
  Gold              看 JOIN / 聚合
  Spark             知道 Databricks 使用 Spark
  PySpark           修改 DataFrame 代码
  MERGE             第二阶段 Delta 示例
  Pipeline          基础完成后再学

------------------------------------------------------------------------

# 33. 和银行数据基盘项目对应起来

以后现场可能是：

``` text
银行系统
↓
数据连携
↓
Databricks Bronze
↓
清洗 / 标准化
↓
Silver
↓
JOIN / Aggregation
↓
Gold
↓
Data Mart
↓
AI Agent
```

所以看任何 GitHub Demo 时，不要在意：

> Demo 是销售数据还是电商数据。

重点看：

``` text
Source是什么
↓
Bronze怎么建立
↓
Silver做了什么加工
↓
Gold为什么这样聚合
```

业务数据换了，数据工程思想仍然类似。

------------------------------------------------------------------------

# 34. 当前不要学习 GitHub 的哪些东西

看到这些可以暂时跳过：

``` text
CI/CD
GitHub Actions
Terraform
Docker
Production Deployment
Complex Streaming
MLflow高级功能
Spark内部优化
复杂Cluster配置
```

不是这些没用，而是它们不是当前参画前最高优先级。

------------------------------------------------------------------------

# 35. 最快学习原则

## 错误方式

``` text
先读300页Databricks资料
↓
再学Spark原理
↓
再学PySpark
↓
再学Git
↓
最后打开Databricks
```

## 推荐方式

``` text
今天就打开Databricks
↓
Clone GitHub
↓
Run Notebook
↓
看到数据
↓
修改代码
↓
再查不懂的概念
```

------------------------------------------------------------------------

# 36. 每个 Notebook 只回答 5 个问题

以后看到任何 Notebook，都用这 5 个问题分析：

### Q1. 输入是什么？

``` text
CSV？
JSON？
Table？
DataFrame？
```

### Q2. 从哪里读取？

``` text
Bronze？
Silver？
Volume？
```

### Q3. 做什么加工？

``` text
Filter？
Select？
JOIN？
GROUP BY？
NULL处理？
```

### Q4. 输出到哪里？

``` text
DataFrame？
Silver Table？
Gold Table？
```

### Q5. 业务目的是什么？

``` text
数据清洗？
客户汇总？
交易汇总？
Data Mart？
AI Agent使用？
```

能回答这五个问题，就说明这个 Notebook 基本看懂了。

------------------------------------------------------------------------

# 37. 第一次学习的完成标准

第一天不要要求自己掌握整个 Databricks。

只要完成：

-   [ ] GitHub Repository 成功 Clone 到 Databricks
-   [ ] 能打开 Git folder
-   [ ] 能打开 README
-   [ ] 能打开 Notebook
-   [ ] 能执行 Cell
-   [ ] 能看到 SQL 结果
-   [ ] 能 `display(df)`
-   [ ] 能找到 Catalog / Schema / Table
-   [ ] 能理解一个 Bronze → Silver 加工
-   [ ] 能理解一个 Silver → Gold 加工
-   [ ] 能修改一个 WHERE / filter 条件并重新运行

做到这些，就已经真正开始使用 Databricks，而不再只是看教程。

------------------------------------------------------------------------

# 38. 后续学习顺序

完成第一个 Demo 后再进入：

``` text
第一阶段
databricks_bootcamp_2026
↓
Notebook / SQL / PySpark
Bronze / Silver / Gold

第二阶段
delta-io/delta-examples
↓
Delta Table
UPDATE
MERGE

第三阶段
databricks-demos/dbdemos
↓
Job
Pipeline
Auto Loader
CDC
```

不要三个 Repository 同时学习。

------------------------------------------------------------------------

# 39. 最终目标

目标不是记住 GitHub 示例代码。

而是以后拿到项目代码时，可以迅速判断：

``` text
这个 Notebook
↓
读取什么数据
↓
使用 SQL 还是 PySpark
↓
进行了什么加工
↓
属于 Bronze / Silver / Gold 哪一层
↓
输出什么 Table
↓
后续哪个 Notebook 使用它
```

达到这个水平，就已经具备 Databricks 数据基盘项目最重要的入门阅读能力。

------------------------------------------------------------------------

# 40. 现在立刻执行的操作

不要继续看更多教程。

直接在当前 Databricks Free Edition：

``` text
1. 左侧「工作区」
2. 进入自己的用户目录
3. 点击「新建」
4. 找「Git 文件夹 / Git folder」
5. 输入：
   https://github.com/DataWithBaraa/databricks_bootcamp_2026
6. 创建
7. 打开 Repository
8. 先看 README
9. 找 Setup / 第一个 Notebook
10. 不要 Run All，逐 Cell 执行
```

如果第 5～10 步出现错误，先记录：

``` text
错误画面
+
正在执行的 Notebook 名
+
当前 Cell
```

再针对这个错误处理。

这比继续泛泛学习 Databricks 概念更快。
