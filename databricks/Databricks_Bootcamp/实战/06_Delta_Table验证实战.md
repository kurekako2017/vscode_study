# 06｜Delta Table 验证实战

## 目的
确认 Bronze/Silver/Gold 的“层”和 Delta 的“表能力”不是同一个概念。

查看：
```sql
DESCRIBE EXTENDED workspace.silver.crm_customers;
DESCRIBE HISTORY workspace.silver.crm_customers;
```

重点观察 version、timestamp、operation 等历史信息。

为 MERGE 创建安全副本：
```sql
CREATE OR REPLACE TABLE workspace.silver.crm_customers_merge_lab
USING DELTA
AS
SELECT * FROM workspace.silver.crm_customers;
```

验证：
```sql
SELECT COUNT(*) FROM workspace.silver.crm_customers_merge_lab;
```

记住：
```text
Bronze/Silver/Gold = 数据加工阶段
Delta = 表格式/事务和更新能力
```

## PASS
- [ ] 会 DESCRIBE HISTORY
- [ ] 已创建 merge_lab
