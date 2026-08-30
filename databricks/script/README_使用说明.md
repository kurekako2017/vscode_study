# Databricks Bootcamp 全量学习注释版

基于：`DataWithBaraa/databricks_bootcamp_2026`

共处理 **14 个 Notebook**，原业务代码逻辑不做重写。

## 两个版本

### 01_可执行注释版
- 原始 Code Cell 保持不变
- 每个关键 Code Cell 前新增中文 Markdown 学习说明
- 适合重新导入 Databricks 执行
- VS Code 中 `%sql` Cell 仍可能被 Python 语言服务标红，这是本地识别问题

### 02_VSCode阅读版
- 同样包含完整中文解释
- `%sql` Cell 转为 Markdown `sql` 代码块展示
- 解决 VS Code 把 `%sql` 当 Python 标红的问题
- **这版主要用于本地阅读复习，不用于直接执行 SQL Cell**

## 注释结构

每个 Notebook 尽量说明：

```text
学习目的
Input
Process / Transformation
Output
为什么这样处理
与 Bronze / Silver / Gold / Workflow 的关系
```

## 建议用法

```text
VS Code 学习复习
→ 打开 02_VSCode阅读版

Databricks 上机执行
→ 使用原仓库，或 01_可执行注释版
```

## 已处理 Notebook

- `script/bronze/bronze_layer(basic).ipynb`
- `script/bronze/bronze_layer_(improved).ipynb`
- `script/gold/gold_dim_customers.ipynb`
- `script/gold/gold_dim_products.ipynb`
- `script/gold/gold_fact_sales.ipynb`
- `script/gold/gold_orchestration.ipynb`
- `script/init_lakehouse.ipynb`
- `script/silver/crm/silver_crm_cust_info.ipynb`
- `script/silver/crm/silver_crm_prd_info.ipynb`
- `script/silver/crm/silver_crm_sales_details.ipynb`
- `script/silver/erp/silver_erp_cust_az12.ipynb`
- `script/silver/erp/silver_erp_loc_a101.ipynb`
- `script/silver/erp/silver_erp_px_cat_g1v2.ipynb`
- `script/silver/silver_orchestration.ipynb`