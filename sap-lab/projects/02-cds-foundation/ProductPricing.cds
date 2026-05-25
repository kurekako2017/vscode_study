*&---------------------------------------------------------------------*
*& CDS 视图: ZProductPricing
*& 说明: 产品定价视图 - 管理产品的多货币价格和折扣信息
*& 功能: 查询产品价格，自动计算净价（已扣除折扣）
*& 特点: 支持多货币，支持折扣管理
*&---------------------------------------------------------------------*

@AccessControl.authorizationCheck: #CHECK  // 启用权限检查
@EndUserText.label: 'Product Pricing'       // UI 显示标签

define view entity ZProductPricing
  as select from zproduct_prices as prices
{
  // ===== 复合主键: 同一产品在不同货币下有不同价格 =====
  key prices.product_id,                // 产品 ID (主键部分 1)
  key prices.currency_code,            // 货币代码 如 USD/CNY (主键部分 2)
  
  // ===== 价格信息 =====
      prices.price,                    // 原始价格（未扣除折扣）
      prices.discount_pct,             // 折扣百分比 (0-100)
      
  // ===== 计算字段: 净价计算 =====
  // 公式: 净价 = 原始价格 × (1 - 折扣% / 100)
  // 示例: 价格 100 元，折扣 10% -> 净价 = 90 元
      cast(
        prices.price * ( 1 - prices.discount_pct / 100 )
        as decimal(16,2)               // 2 位小数的十进制数
      ) as net_price                   // 净价（扣除折扣后）
}
