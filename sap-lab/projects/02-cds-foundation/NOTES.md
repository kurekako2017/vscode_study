## CDS 学习笔记

### 基本语法
```sql
define view entity VIEW_NAME 
  as select from source_table {
    -- 字段定义
    key field1,
        field2,
        -- 计算字段
        cast(field3 as type) as calculated_field
  }
```

### 重要注解
- `@AccessControl.authorizationCheck: #CHECK` - 权限检查
- `@EndUserText.label` - UI 显示标签
- `@Metadata.ignorePropagatedAnnotations` - 忽略传播注解
- `@ObjectModel.readOnly: true` - 只读视图
- `@UI.hidden: true` - 隐藏字段

### 关联（Association）
```sql
association [0..*] to TARGET_VIEW as _target 
  on _target.key = source.key
```

### 计算字段
```sql
cast(condition as type) as field_name
```
