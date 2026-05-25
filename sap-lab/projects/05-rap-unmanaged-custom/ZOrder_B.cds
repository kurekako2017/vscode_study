*&---------------------------------------------------------------------*
*& 行为定义: Order BO (RAP Unmanaged 业务对象)
*& 说明: 定义订单业务对象的操作和验证规则
*& 特点: 使用 Unmanaged 模式，所有操作需要手动实现
*& 功能: CRUD、Determination、Validation、Action、组合关系
*&---------------------------------------------------------------------*

@EndUserText.label: 'Order BO'  // 业务对象显示名称

// 为 ZOrder 视图定义行为规则，别名为 'Order'
define behavior for ZOrder alias Order
{
  // ===== Unmanaged 模式 - 手动实现所有操作 =====
  use create;                           // 使用自定义创建逻辑
  use read;                             // 使用自定义读取逻辑
  use update;                           // 使用自定义更新逻辑
  use delete;                           // 使用自定义删除逻辑

  // ===== 字段级别的控制 =====
  
  // 必填字段: 订单号、客户 ID、订单日期必须有值
  field (mandatory) order_number, customer_id, order_date;
  
  // 只读字段: 订单状态、总金额、审计字段由系统管理
  field (read only) order_status,       // 订单状态（已批准/待处理等）由系统设置
                    total_amount,       // 订单总金额由系统计算
                    created_at,         // 创建时间由系统设置
                    changed_at;         // 修改时间由系统更新

  // ===== Determination (自动触发的业务逻辑) =====
  // 在 CREATE 时生成订单号
  determination set_order_number on save { create; }
  
  // 在 CREATE 和 UPDATE 时计算订单总金额
  determination calculate_total on save { create; update; }
  
  // 在 CREATE 时设置初始状态为待处理
  determination set_status on save { create; }

  // ===== Validation (数据验证) =====
  // 验证客户是否存在（在 CREATE 和 UPDATE 时）
  validation validate_customer on save { create; update; }
  
  // 验证订单项是否存在且有效（在 CREATE 和 UPDATE 时）
  validation validate_line_items on save { create; update; }

  // ===== Action (自定义操作) =====
  // 批准订单的操作
  // result [1] $self: 返回 1 条更新后的订单记录
  action approve result [1] $self;
  
  // 拒绝订单的操作
  // parameter struct { reason : String; }: 接收拒绝原因参数
  // result [1] $self: 返回 1 条更新后的订单记录
  action reject_order parameter struct { reason : String; } result [1] $self;

  // ===== 组合关系 =====
  // 订单与订单项的主从关系
  // [0..*] 一个订单可以有多个订单项
  composition [0..*] of ZOrderItem on _items
}
