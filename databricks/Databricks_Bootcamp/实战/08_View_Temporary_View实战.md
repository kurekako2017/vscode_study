# 08｜Table / View / Temporary View 实战

## Table
正式数据：
```sql
SELECT * FROM workspace.silver.crm_customers LIMIT 10;
```

## 永久 View
```sql
CREATE OR REPLACE VIEW workspace.gold.customer_basic_view AS
SELECT customer_id, customer_number, first_name, last_name
FROM workspace.silver.crm_customers;
```
验证：
```sql
SELECT * FROM workspace.gold.customer_basic_view LIMIT 10;
```

## Temporary View
```python
temp_df = spark.table("workspace.silver.crm_customers").limit(10)
temp_df.createOrReplaceTempView("temp_customer_10")
```
```sql
SELECT * FROM temp_customer_10;
```

|对象|保存正式数据|持久|用途|
|---|---:|---:|---|
|Table|是|是|Bronze/Silver/Gold|
|View|保存查询定义|是|复用查询|
|Temporary View|否|会话级|中间加工/MERGE Source|

## PASS
- [ ] 永久 View 可查询
- [ ] Temporary View 可查询
- [ ] 能解释区别
