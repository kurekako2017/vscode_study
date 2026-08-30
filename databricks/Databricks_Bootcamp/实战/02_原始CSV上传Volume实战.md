# 02｜原始 CSV 上传 Volume 实战

## 源文件
```text
datasets/engineering/
├── source_crm/
│   ├── cust_info.csv
│   ├── prd_info.csv
│   └── sales_details.csv
└── source_erp/
    ├── CUST_AZ12.csv
    ├── LOC_A101.csv
    └── PX_CAT_G1V2.csv
```

## 目标
最终必须成为：
```text
/Volumes/workspace/bronze/raw_sources/
├── source_crm/...
└── source_erp/...
```

打开：
```text
Catalog → workspace → bronze → Volumes → raw_sources
```
保持 source_crm/source_erp 两个目录，分别上传对应 CSV。

验证：
```python
display(dbutils.fs.ls("/Volumes/workspace/bronze/raw_sources/source_crm"))
display(dbutils.fs.ls("/Volumes/workspace/bronze/raw_sources/source_erp"))
```

实际读一次：
```python
test_df = (spark.read.option("header","true")
          .option("inferSchema","true")
          .csv("/Volumes/workspace/bronze/raw_sources/source_crm/cust_info.csv"))
display(test_df.limit(10))
```

## PASS
- [ ] 6 个 CSV 可见
- [ ] cust_info.csv 能被 Spark 读取
