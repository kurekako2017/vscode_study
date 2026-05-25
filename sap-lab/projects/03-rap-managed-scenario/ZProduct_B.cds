*&---------------------------------------------------------------------*
*& 行为定义: Product BO (RAP 业务对象行为)
*& 说明: 定义产品业务对象的操作权限和业务规则
*& 功能: 控制何时执行 CRUD 操作、字段可编辑性、自动触发
*&---------------------------------------------------------------------*

@EndUserText.label: 'Product BO'  // 业务对象的 UI 显示名称

// 为 ZProduct 视图定义行为规则，别名为 'Product'
define behavior for ZProduct alias Product
{
  // ===== CRUD 操作定义 =====
  // 定义用户可以执行的数据库操作
  
  create;                              // 允许创建新产品
  read;                                // 允许读取产品信息
  update;                              // 允许修改产品信息
  delete;                              // 允许删除产品

  // ===== 字段级别的控制 =====
  
  // 必填字段: 保存时必须有值
  field (mandatory) product_name;      // 产品名称不能为空
  field (mandatory) category;          // 产品类别不能为空
  field (mandatory) price;             // 产品价格不能为空
  
  // 只读字段: 创建后不能修改（由系统管理）
  field (read only) created_at,        // 创建时间由系统设置
                    created_by,        // 创建人由系统自动赋值
                    changed_at,        // 最后修改时间自动更新
                    changed_by;        // 最后修改人自动赋值

  // ===== Determination (自动触发的业务逻辑) =====
  // 在特定事件发生时自动执行，用于设置默认值
  determination set_defaults on save { create; }

  // ===== Validation (数据验证) =====
  // 在保存前验证数据，验证失败则阻止保存
  validation check_price_positive on save { create; update; }
}
