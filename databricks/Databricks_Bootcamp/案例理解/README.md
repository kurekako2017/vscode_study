# Databricks 参画前学习资料 V2｜以 `DataWithBaraa/databricks_bootcamp_2026` 为主线

> 本教程不再另外虚构一套 customer / transaction 示例。
>
> **所有主教程均以你本地已经复制的 `DataWithBaraa/databricks_bootcamp_2026` 为基准。**
>
> 原仓库已有内容直接按原 Notebook 学；项目组要求但原仓库没有完整覆盖的内容（例如 MERGE、正式 Jobs/Workflows UI）明确标记为 **【扩展实战】**。

---

## 1. Bootcamp 项目整体地图

```mermaid
flowchart TB
    SRC["datasets/engineering<br>CRM + ERP 原始 CSV 数据"]
    INIT["init_lakehouse.ipynb<br>创建 bronze / silver / gold Schema 和 Volume"]
    VOL["Volume: workspace.bronze.raw_sources<br>保存上传后的 CRM / ERP CSV 文件"]
    BRONZE["script/bronze<br>读取 CSV，写入 Bronze Delta Table"]
    BT["Bronze Delta Tables<br>6 张接近原始状态的 CRM / ERP 表"]
    SILVER["script/silver<br>清洗、标准化、类型转换、字段改名"]
    ST["Silver Delta Tables<br>6 张清洗后的可信业务明细表"]
    GOLD["script/gold<br>SQL JOIN + Dimension / Fact 建模"]
    GT["Gold Delta Tables<br>dim_customers / dim_products / fact_sales"]
    OUT["BI / Analysis / AI Agent<br>面向业务分析和 AI 使用的数据"]
    ORCH["silver_orchestration / gold_orchestration<br>按顺序调用多个 Notebook"]

    SRC --> INIT --> VOL --> BRONZE --> BT --> SILVER --> ST --> GOLD --> GT --> OUT
    ORCH -. "自动调用各层 Notebook" .-> SILVER
    ORCH -. "自动调用各层 Notebook" .-> GOLD
```

---

## 2. 仓库真实目录

```text
databricks_bootcamp_2026-main/
├── datasets/
│   ├── engineering/
│   │   ├── source_crm/
│   │   │   ├── cust_info.csv
│   │   │   ├── prd_info.csv
│   │   │   └── sales_details.csv
│   │   └── source_erp/
│   │       ├── CUST_AZ12.csv
│   │       ├── LOC_A101.csv
│   │       └── PX_CAT_G1V2.csv
│   └── analysts/
└── script/
    ├── init_lakehouse.ipynb
    ├── bronze/
    │   ├── bronze_layer(basic).ipynb
    │   └── bronze_layer_(improved).ipynb
    ├── silver/
    │   ├── silver_orchestration.ipynb
    │   ├── crm/
    │   └── erp/
    └── gold/
        ├── gold_dim_customers.ipynb
        ├── gold_dim_products.ipynb
        ├── gold_fact_sales.ipynb
        └── gold_orchestration.ipynb
```

---

## 3. 真实数据流

```mermaid
flowchart LR
    CRM["CRM CSV<br>客户 / 商品 / 销售数据"]
    ERP["ERP CSV<br>客户补充 / 地区 / 商品分类数据"]
    BCRM["Bronze CRM Tables<br>原始 CRM 数据表"]
    BERP["Bronze ERP Tables<br>原始 ERP 数据表"]
    SCRM["Silver CRM Tables<br>清洗后的客户 / 商品 / 销售"]
    SERP["Silver ERP Tables<br>清洗后的客户补充 / 地区 / 分类"]
    DC["gold.dim_customers<br>客户维表"]
    DP["gold.dim_products<br>商品维表"]
    FS["gold.fact_sales<br>销售事实表"]

    CRM --> BCRM --> SCRM
    ERP --> BERP --> SERP
    SCRM --> DC
    SERP --> DC
    SCRM --> DP
    SERP --> DP
    SCRM --> FS
    DC --> FS
    DP --> FS
```

---

## 4. 教程阅读顺序

| 顺序 | 文档 | 目的 |
|---|---|---|
| 1 | `01_Databricks整体概念与架构.md` | 把 Workspace、Catalog、Volume、Delta、Notebook 放回 Bootcamp |
| 2 | `02_Bootcamp_Bronze_Silver_Gold完整实战.md` | 逐层理解原仓库 Notebook |
| 3 | `03_Bootcamp_Delta_Table与MERGE实战.md` | 先理解原项目 Delta，再做项目组要求的 MERGE 扩展 |
| 4 | `04_Bootcamp_PySpark与SQL代码解读.md` | 直接读原项目 PySpark / Spark SQL |
| 5 | `05_Bootcamp_Jobs_Workflows编排实战.md` | 从原仓库 orchestration 过渡到正式 Workflow |

---

## 5. 原仓库与扩展练习分开

### Bootcamp 原版已有

- init Lakehouse
- Volume
- Bronze ingestion
- Bronze / Silver / Gold Delta Table
- Silver PySpark 清洗
- Gold Dimension / Fact
- Spark SQL
- Unity Catalog
- `dbutils.notebook.run()` orchestration

### 参画要求扩展

- Table / View / Temporary View
- INSERT / UPDATE / MERGE
- 正式 Jobs / Workflows

本教程会在 **Bootcamp 现有表上继续练**，但会明确标记哪些不是仓库原版。

---

## 6. 推荐学习顺序

```mermaid
flowchart LR
    A["init_lakehouse<br>准备 Catalog / Schema / Volume"]
    B["Bronze basic<br>先看最直白的 CSV → Table"]
    C["Bronze improved<br>理解配置化批量 Ingestion"]
    D["Silver CRM<br>重点学习 PySpark 清洗"]
    E["Silver ERP<br>理解跨系统标准化"]
    F["Silver orchestration<br>理解 Notebook 编排"]
    G["Gold dimensions<br>理解 JOIN + Dimension"]
    H["Gold fact<br>理解 Fact Table"]
    I["Gold orchestration<br>理解统一入口"]
    J["MERGE 扩展<br>在现有 Delta 表上练增量更新"]
    K["正式 Workflow<br>把各 Notebook 配成 Task DAG"]

    A --> B --> C --> D --> E --> F --> G --> H --> I --> J --> K
```
