# Bootcamp 仓库实物对照表

## Engineering 数据

| 文件 | 行数 | 用途 |
|---|---:|---|
| `source_crm/cust_info.csv` | 18,494 | CRM 客户 |
| `source_crm/prd_info.csv` | 397 | CRM 商品 |
| `source_crm/sales_details.csv` | 60,398 | CRM 销售 |
| `source_erp/CUST_AZ12.csv` | 18,484 | ERP 客户补充 |
| `source_erp/LOC_A101.csv` | 18,484 | ERP 地区 |
| `source_erp/PX_CAT_G1V2.csv` | 37 | ERP 商品分类 |

## Bronze 映射

| Source | Bronze Table |
|---|---|
| `cust_info.csv` | `workspace.bronze.crm_cust_info` |
| `prd_info.csv` | `workspace.bronze.crm_prd_info` |
| `sales_details.csv` | `workspace.bronze.crm_sales_details` |
| `CUST_AZ12.csv` | `workspace.bronze.erp_cust_az12` |
| `LOC_A101.csv` | `workspace.bronze.erp_loc_a101` |
| `PX_CAT_G1V2.csv` | `workspace.bronze.erp_px_cat_g1v2` |

## Silver 映射

| Notebook | 输入 | 输出 |
|---|---|---|
| `silver_crm_cust_info` | `bronze.crm_cust_info` | `silver.crm_customers` |
| `silver_crm_prd_info` | `bronze.crm_prd_info` | `silver.crm_products` |
| `silver_crm_sales_details` | `bronze.crm_sales_details` | `silver.crm_sales` |
| `silver_erp_cust_az12` | `bronze.erp_cust_az12` | `silver.erp_customers` |
| `silver_erp_loc_a101` | `bronze.erp_loc_a101` | `silver.erp_customer_location` |
| `silver_erp_px_cat_g1v2` | `bronze.erp_px_cat_g1v2` | `silver.erp_product_category` |

## Gold 映射

| Notebook | 输入 | 输出 |
|---|---|---|
| `gold_dim_customers` | CRM Customer + ERP Customer + ERP Location | `gold.dim_customers` |
| `gold_dim_products` | CRM Product + ERP Product Category | `gold.dim_products` |
| `gold_fact_sales` | CRM Sales + 两张 Gold Dimension | `gold.fact_sales` |
