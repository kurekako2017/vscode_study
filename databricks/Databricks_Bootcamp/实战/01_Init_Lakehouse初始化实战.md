# 01｜Init Lakehouse 初始化实战

## 使用文件
`script/init_lakehouse.ipynb`

## 目的
创建后续所有 Notebook 依赖的数据空间。

打开：
```text
Workspace → databricks_bootcamp_2026 → script → init_lakehouse
```

逐 Cell 执行核心逻辑：
```sql
USE CATALOG workspace;
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
CREATE VOLUME IF NOT EXISTS workspace.bronze.raw_sources;
```

UI 验证：
```text
Catalog → workspace
├── bronze
│   └── Volumes → raw_sources
├── silver
└── gold
```

SQL 验证：
```sql
SHOW SCHEMAS IN workspace;
```

## PASS
四个对象都存在：bronze、silver、gold、raw_sources。
