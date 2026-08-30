# 00｜环境准备与 Bootcamp 导入

## 目的
把 Bootcamp 代码放入 Databricks Workspace。

## 操作
Databricks 左侧：
```text
Workspace → 自己的用户目录 → New → Git folder
```
Repository：
```text
https://github.com/DataWithBaraa/databricks_bootcamp_2026
```

完成后确认：
```text
databricks_bootcamp_2026/
├── datasets/
└── script/
    ├── init_lakehouse.ipynb
    ├── bronze/
    ├── silver/
    └── gold/
```

不要 Run All。正确顺序：
```text
init_lakehouse → 上传 CSV → Bronze → Silver → Gold
```

## PASS
- [ ] 能打开 init_lakehouse
- [ ] 能找到两个 Bronze Notebook
- [ ] 能找到 Silver CRM/ERP
- [ ] 能找到 Gold Dimension/Fact
