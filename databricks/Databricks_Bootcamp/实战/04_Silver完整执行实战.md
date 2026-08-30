# 04｜Silver 完整执行实战

## 目的
```text
Bronze 原始数据 → 清洗/标准化 → Silver 可信数据
```

依次执行：
```text
CRM:
silver_crm_cust_info
silver_crm_prd_info
silver_crm_sales_details

ERP:
silver_erp_cust_az12
silver_erp_loc_a101
silver_erp_px_cat_g1v2
```

重点观察真实规则：
```text
Customer: Trim；S/M→Single/Married；F/M→Female/Male；NULL ID过滤
Product: cost 空→0；商品线标准化；日期转换
Sales: 无效日期→NULL；price 异常时重新计算
ERP Customer: NASAW00011000 → AW00011000
ERP Location: AW-00011000 → AW00011000
ERP Category: YES/NO → true/false
```

验证：
```sql
SHOW TABLES IN workspace.silver;
SELECT * FROM workspace.silver.crm_customers LIMIT 20;
SELECT * FROM workspace.silver.crm_sales LIMIT 20;
```

预期 6 张：
```text
crm_customers
crm_products
crm_sales
erp_customers
erp_customer_location
erp_product_category
```

然后执行：
`script/silver/silver_orchestration.ipynb`

理解：
```text
一个入口 Notebook → dbutils.notebook.run() → 顺序执行 6 个 Notebook
```

## PASS
- [ ] 6 张 Silver 表
- [ ] 能说出至少 3 个清洗规则
- [ ] 能解释为什么 CRM/ERP Key 要统一
