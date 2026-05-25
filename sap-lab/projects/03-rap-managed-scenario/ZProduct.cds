*&---------------------------------------------------------------------*
*& CDS 视图: ZProduct (RAP 根视图)
*& 说明: 产品业务对象的根视图 - 定义产品的基本结构
*& 特点: 这是 RAP Managed Scenario 的基础数据模型
*& 功能: 提供产品的 CRUD 操作的数据基础
*&---------------------------------------------------------------------*

@AccessControl.authorizationCheck: #CHECK  // 启用权限检查
@EndUserText.label: 'Product'               // UI 显示名称

// 'root' 关键词: 表示这是 RAP 业务对象的根实体
// 可以与其他子实体关联，形成主从关系
define root view entity ZProduct
  as select from zproducts
{
  // ===== 主键字段 =====
  key product_id,                       // 产品唯一编号
  
  // ===== 基本信息字段 =====
      product_name,                     // 产品名称 (必填)
      description,                      // 产品详细描述
      category,                         // 产品所属类别
      price,                            // 产品价格
      stock_quantity,                   // 库存数量
  
  // ===== 审计字段 (系统自动管理) =====
  // 用于跟踪记录的创建和修改历史
      created_at,                       // 创建日期时间
      changed_at,                       // 最后修改日期时间
      created_by,                       // 创建人用户名
      changed_by                        // 最后修改人用户名
}
