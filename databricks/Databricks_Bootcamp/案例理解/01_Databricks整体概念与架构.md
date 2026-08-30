# 01｜Databricks 整体概念与架构｜结合 Bootcamp 实际项目

## 1. 项目整体架构

```mermaid
flowchart TB
    DBX["Databricks<br>统一的数据工程、SQL 分析和 AI 数据平台"]
    WS["Workspace<br>保存和编辑 Bootcamp Notebook / Git 项目代码"]
    NB["Notebook<br>执行 SQL、Python、PySpark 数据处理代码"]
    CMP["Compute / Serverless<br>真正负责运行 Notebook 代码的计算资源"]
    CAT["Catalog: workspace<br>统一管理本项目的数据资产"]
    SCH["Schema<br>bronze / silver / gold 三个数据层"]
    VOL["Volume: raw_sources<br>保存 CRM / ERP 原始 CSV 文件"]
    DT["Delta Tables<br>保存 Bronze / Silver / Gold 正式数据"]
    JOB["Jobs / Workflows<br>自动按依赖关系执行多个 Notebook"]

    DBX --> WS --> NB
    CMP --> NB
    DBX --> CAT --> SCH
    SCH --> VOL
    SCH --> DT
    NB -. "读取 / 写入" .-> VOL
    NB -. "读取 / 写入" .-> DT
    JOB -. "调度执行" .-> NB
```

## 2. Workspace：代码在哪里

```text
Workspace
└── databricks_bootcamp_2026
    └── script
        ├── init_lakehouse.ipynb
        ├── bronze
        ├── silver
        └── gold
```

Workspace 主要回答：**代码在哪里？**

---

## 3. Catalog：数据在哪里

`init_lakehouse.ipynb` 实际执行：

```sql
USE CATALOG workspace;
```

然后创建：

```sql
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
```

所以：

```text
workspace.bronze.crm_cust_info
    │       │        │
    │       │        └─ Table
    │       └────────── Schema
    └────────────────── Catalog
```

---

## 4. Workspace 和 `workspace` Catalog 不是一个东西

```mermaid
flowchart LR
    W["Workspace<br>开发区域：Notebook / Git / 代码"]
    N["silver_crm_cust_info.ipynb<br>一份实际开发代码"]
    C["Catalog: workspace<br>数据资产的顶层容器"]
    T["workspace.bronze.crm_cust_info<br>一张正式数据表"]

    W --> N
    N -. "spark.table() 读取" .-> T
    C --> T
```

---

## 5. Volume：原始 CSV 放在哪里

原项目创建：

```sql
CREATE VOLUME IF NOT EXISTS workspace.bronze.raw_sources;
```

Bronze Notebook 读取：

```text
/Volumes/workspace/bronze/raw_sources/source_crm/cust_info.csv
```

关系：

```mermaid
flowchart LR
    LOCAL["GitHub datasets<br>本地仓库里的 CSV 示例"]
    VOL["Unity Catalog Volume<br>Databricks 中保存原始文件"]
    NB["Bronze Notebook<br>spark.read.csv() 读取"]
    T["Bronze Delta Table<br>写成正式可查询的数据表"]

    LOCAL --> VOL --> NB --> T
```

---

## 6. Notebook：实际开发工作台

Bronze basic：

```python
df = spark.read.option("header", "true") \
    .option("inferSchema", "true") \
    .csv("/Volumes/workspace/bronze/raw_sources/source_crm/cust_info.csv")

df.write.mode("overwrite").saveAsTable(
    "workspace.bronze.crm_cust_info"
)
```

读成：

```text
Input
cust_info.csv
 ↓
Process
Spark 读取 CSV
 ↓
Output
workspace.bronze.crm_cust_info
```

---

## 7. Compute / Serverless

```text
Notebook
 ↓
提交 SQL / Python / PySpark
 ↓
Compute / Serverless
 ↓
Spark 执行
 ↓
读写 Delta Table
```

Notebook = 写什么；Compute = 谁来执行。

---

## 8. Spark / PySpark 在项目中的位置

Silver：

```python
df = spark.table("workspace.bronze.crm_cust_info")
df = df.filter(col("cst_id").isNotNull())
```

最终：

```python
df.write.mode("overwrite").format("delta") \
  .saveAsTable("workspace.silver.crm_customers")
```

真实流程：

```text
Bronze Delta Table
 ↓
PySpark DataFrame
 ↓
清洗 / 转换
 ↓
Silver Delta Table
```

---

## 9. Spark SQL 在项目中的位置

Gold 主要用 SQL：

```python
query = """
SELECT ...
FROM silver.crm_customers ci
LEFT JOIN silver.erp_customers ca
  ON ci.customer_number = ca.customer_number
"""

df = spark.sql(query)
```

所以这个项目是：

```text
Bronze → PySpark ingestion
Silver → PySpark transformation
Gold   → Spark SQL 建模
```

---

## 10. Delta Table 和 Bronze/Silver/Gold 的关系

```mermaid
flowchart LR
    B["Bronze<br>接近原始状态的数据层"]
    BD["Delta Table<br>实际表格式和管理能力"]
    S["Silver<br>清洗后的可信数据层"]
    SD["Delta Table<br>支持可靠读写"]
    G["Gold<br>业务模型层"]
    GD["Delta Table<br>提供给分析和下游"]

    B --- BD
    S --- SD
    G --- GD
```

Bronze/Silver/Gold 是数据层；Delta 是表能力，不是第四层。

---

## 11. Bootcamp 整体技术关系

```mermaid
flowchart TB
    FILE["CRM / ERP CSV<br>原始源文件"]
    VOLUME["Volume raw_sources<br>原始文件存储"]
    BRONZE["Bronze Notebook<br>CSV → Bronze"]
    BT["Bronze Delta Tables<br>6 张原始数据表"]
    SILVER["Silver Notebooks<br>PySpark 清洗 / 标准化"]
    ST["Silver Delta Tables<br>6 张可信数据表"]
    GOLD["Gold Notebooks<br>Spark SQL JOIN / 建模"]
    GT["Gold Delta Tables<br>Dimension / Fact"]
    BI["BI / Analysis / AI<br>最终消费层"]

    FILE --> VOLUME --> BRONZE --> BT --> SILVER --> ST --> GOLD --> GT --> BI
```
