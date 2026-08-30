# 05｜Bootcamp Jobs / Workflows 编排实战

> 先学仓库真实存在的 orchestration，再扩展正式 Jobs / Workflows。

---

## 1. Silver Orchestration

原文件：

```text
script/silver/silver_orchestration.ipynb
```

核心代码：

```python
notebooks = [
    "./crm/silver_crm_cust_info",
    "./crm/silver_crm_prd_info",
    "./crm/silver_crm_sales_details",
    "./erp/silver_erp_cust_az12",
    "./erp/silver_erp_loc_a101",
    "./erp/silver_erp_px_cat_g1v2"
]

for nb in notebooks:
    dbutils.notebook.run(nb, timeout_seconds=0)
```

流程：

```mermaid
flowchart TB
    ORCH["silver_orchestration<br>Silver 层统一入口"]
    C1["CRM Customer<br>清洗客户"]
    C2["CRM Product<br>清洗商品"]
    C3["CRM Sales<br>清洗销售"]
    E1["ERP Customer<br>清洗 ERP 客户"]
    E2["ERP Location<br>清洗地区"]
    E3["ERP Category<br>清洗商品分类"]

    ORCH --> C1 --> C2 --> C3 --> E1 --> E2 --> E3
```

---

## 2. Gold Orchestration

真实顺序：

```mermaid
flowchart TB
    ORCH["gold_orchestration<br>Gold 层统一入口"]
    C["gold_dim_customers<br>先建立客户维表"]
    P["gold_dim_products<br>再建立商品维表"]
    F["gold_fact_sales<br>最后建立销售事实表"]

    ORCH --> C --> P --> F
```

Fact 最后，因为它依赖：

```text
gold.dim_customers
gold.dim_products
```

---

## 3. Notebook chaining ≠ 正式 Workflow

| Bootcamp orchestration | Jobs / Workflows |
|---|---|
| 调用关系写在 Python 中 | 依赖在 Workflow 层表达 |
| `dbutils.notebook.run()` | 每个 Notebook 是 Task |
| 简单统一入口 | 更适合生产调度和监控 |
| 逻辑藏在代码 | DAG 可以直接看到 |
| 基本执行 | 有 Run History / Retry / Schedule |

---

## 4. 推荐第一版正式 Workflow

直接复用原仓库现有入口：

```mermaid
flowchart TB
    INIT["Task 1: init_lakehouse<br>准备 Schema / Volume"]
    BRONZE["Task 2: bronze_layer_(improved)<br>CRM / ERP CSV → Bronze"]
    SILVER["Task 3: silver_orchestration<br>执行 6 个 Silver Notebook"]
    GOLD["Task 4: gold_orchestration<br>建立 Dimension + Fact"]
    CHECK["Task 5: Validation<br>确认 Gold 表和执行结果"]

    INIT --> BRONZE --> SILVER --> GOLD --> CHECK
```

这版最适合参画前。

---

## 5. 熟悉后再拆 Task

```mermaid
flowchart TB
    B["Bronze Ingestion<br>生成 6 张 Bronze 表"]
    C1["CRM Customer<br>客户清洗"]
    C2["CRM Product<br>商品清洗"]
    C3["CRM Sales<br>销售清洗"]
    E1["ERP Customer<br>ERP 客户清洗"]
    E2["ERP Location<br>地区清洗"]
    E3["ERP Category<br>商品分类清洗"]
    DC["Gold Customer Dimension<br>客户维表"]
    DP["Gold Product Dimension<br>商品维表"]
    FS["Gold Sales Fact<br>销售事实表"]

    B --> C1
    B --> C2
    B --> C3
    B --> E1
    B --> E2
    B --> E3

    C1 --> DC
    E1 --> DC
    E2 --> DC

    C2 --> DP
    E3 --> DP

    C3 --> FS
    DC --> FS
    DP --> FS
```

---

## 6. Workflow UI 实操目标

至少完成：

```text
Create Workflow
 ↓
Add Notebook Task
 ↓
设置 Depends on
 ↓
Run now
 ↓
查看 Task 状态
 ↓
查看 Run History
 ↓
打开失败 Task 日志
 ↓
认识 Retry / Schedule
```

---

## 7. 完整项目图

```mermaid
flowchart TB
    SRC["CRM / ERP Source Files<br>原始业务 CSV"]
    INIT["Init Task<br>Catalog / Schema / Volume"]
    BNB["Bronze Task<br>CSV → Bronze Delta"]
    BT["Bronze Tables<br>原始数据层"]
    SNB["Silver Tasks<br>PySpark 清洗 / 标准化"]
    ST["Silver Tables<br>可信数据层"]
    GNB["Gold Tasks<br>SQL JOIN + Dimension / Fact"]
    GT["Gold Tables<br>业务分析模型"]
    OUT["BI / AI Agent<br>最终消费"]
    WF["Databricks Workflow<br>依赖、调度、监控、历史"]

    SRC --> INIT --> BNB --> BT --> SNB --> ST --> GNB --> GT --> OUT
    WF -. "Task 调度" .-> INIT
    WF -. "Task 调度" .-> BNB
    WF -. "Task 调度" .-> SNB
    WF -. "Task 调度" .-> GNB
```
