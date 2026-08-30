# 03｜Bronze 完整执行实战

## 目的
完成真实链路：
```text
CSV → Spark DataFrame → Bronze Delta Table
```

## 第一轮：basic
打开：
`script/bronze/bronze_layer(basic).ipynb`

核心读取：
```python
df = (spark.read.option("header","true")
      .option("inferSchema","true")
      .csv("/Volumes/workspace/bronze/raw_sources/source_crm/cust_info.csv"))
```
观察：
```python
display(df.limit(10))
```
核心写入：
```python
df.write.mode("overwrite").saveAsTable("workspace.bronze.crm_cust_info")
```

Catalog 应看到：
```text
crm_cust_info
crm_prd_info
crm_sales_details
erp_cust_az12
erp_loc_a101
erp_px_cat_g1v2
```

验证：
```sql
SELECT * FROM workspace.bronze.crm_cust_info LIMIT 10;
SHOW TABLES IN workspace.bronze;
```

## 第二轮：improved
打开 `bronze_layer_(improved).ipynb`。

重点理解：
```text
INGESTION_CONFIG
        ↓
source + path + table
        ↓
for 循环
        ↓
同一套 ingestion 批量处理 6 个 Source
```

## PASS
- [ ] 六张 Bronze 表
- [ ] 会查询 Bronze
- [ ] 能解释 basic 与 improved
