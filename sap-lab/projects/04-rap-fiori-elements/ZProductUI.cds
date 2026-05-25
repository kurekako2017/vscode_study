*&---------------------------------------------------------------------*
*& CDS 视图: ZProductUI (Fiori Elements UI 模型)
*& 说明: 定义产品在 UI 上的显示方式和用户交互
*& 特点: 包含列表、对象页、搜索、过滤等 UI 控制
*& 功能: 自动生成 Fiori Elements 应用界面
*&---------------------------------------------------------------------*

// =====================================================
// 权限和元数据注解
// =====================================================
@AccessControl.authorizationCheck: #CHECK  // 启用权限检查
@EndUserText.label: 'Product List'          // 应用标题
@ObjectModel.usageType.serviceQuality: #HIGH // 高品质服务
@ObjectModel.usageType.sizeCategory: #M      // 中等数据量
@Search.searchable: true                     // 启用全文搜索

// =====================================================
// 列表报告和对象页配置
// =====================================================
@UI.headerInfo: { 
  typeName: 'Product',                      // 单数形式
  typeNamePlural: 'Products'                // 复数形式
}
@UI.presentationVariant: [{ 
  sortOrder: [{ by: 'product_name', direction: #ASC }]  // 默认按产品名称升序
}]

define root view entity ZProductUI
  as select from ZProduct
{
  // ===== 对象页分区定义 =====
  @UI.facet: [
    { id: 'ProductInfo', purpose: #STANDARD, label: 'Product Information', position: 10 },
    { id: 'Pricing', purpose: #STANDARD, label: 'Pricing', position: 20 }
  ]
  // ===== 产品 ID =====
  @UI.lineItem: [ { position: 10 } ]       // 列表中第 10 位
  @UI.identification: [ { position: 10 } ] // 对象页表头第 10 位
  key product_id,

  // ===== 产品名称 =====
  @UI.lineItem: [ { position: 20 } ]       // 列表中第 20 位
  @UI.selectionField: [ { position: 10 } ] // 搜索/过滤字段第 1 个
  @UI.identification: [ { position: 20 } ] // 对象页表头第 20 位
  @Search.defaultSearchElement: true       // 全文搜索的默认字段
  product_name,

  // ===== 产品描述 =====
  @UI.lineItem: [ { position: 30 } ]       // 列表中第 30 位
  @UI.identification: [ { position: 30 } ] // 对象页表头第 30 位
  description,

  // ===== 产品分类 =====
  @UI.lineItem: [ { position: 40 } ]       // 列表中第 40 位
  @UI.selectionField: [ { position: 20 } ] // 搜索/过滤字段第 2 个
  @UI.identification: [ { position: 40 } ] // 对象页表头第 40 位
  category,

  // ===== 产品价格 =====
  @UI.lineItem: [ { position: 50 } ]       // 列表中第 50 位
  @UI.identification: [ { position: 50 }, { facetId: 'Pricing', position: 10 } ]  // Pricing 分区
  price,

  // ===== 库存数量 =====
  @UI.lineItem: [ { position: 60 } ]       // 列表中第 60 位
  @UI.identification: [ { position: 60 } ] // 对象页表头第 60 位
  stock_quantity,

  // ===== 审计字段 =====
  created_at,                              // 创建时间
  changed_at,                              // 修改时间
  created_by,                              // 创建人
  changed_by                               // 修改人
}
