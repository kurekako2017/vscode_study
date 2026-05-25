*&---------------------------------------------------------------------*
*& CDS 视图: ZProductMaster
*& 说明: 产品主数据视图 - 展示产品的基本信息和定价分类
*& 功能: 查询产品信息，自动计算价格等级（Premium/Standard/Economy）
*& 关联: 与定价视图关联，一个产品可以有多个价格记录
*&---------------------------------------------------------------------*

@AccessControl.authorizationCheck: #CHECK  // 启用权限检查
@EndUserText.label: 'Product Master Data'   // UI 显示标签
@Metadata.ignorePropagatedAnnotations: true // 忽略传播的注解

define view entity ZProductMaster
  as select from zproducts as products
  // 关联定义: 一个产品可以有多个价格记录
  association [0..*] to ZProductPricing as _pricing on _pricing.product_id = products.product_id
{
  // ===== 主键字段 =====
  key products.product_id,              // 产品唯一标识
  
  // ===== 基本信息 =====
      products.product_name,            // 产品名称
      products.description,             // 产品描述
      products.category,                // 产品类别
  
  // ===== 审计字段 =====
      products.created_at,              // 创建时间
      products.changed_at,              // 最后修改时间
      
  // ===== 计算字段: 价格等级 =====
  // 根据价格自动分配等级
  // 价格 > 1000 -> 'Premium' (高端)
  // 价格 > 500  -> 'Standard' (标准)
  // 其他         -> 'Economy' (经济)
      cast(
        case
          when products.price > 1000
            then 'Premium'
          when products.price > 500
            then 'Standard'
          else 'Economy'
        end
        as zproduct_category
      ) as price_category,              // 价格等级
      
      // ===== 关联字段 =====
      _pricing                          // 关联到定价视图
}
